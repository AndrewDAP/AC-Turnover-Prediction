"""
ExplainableBoostingMachine model
"""
from logging import getLogger
from typing import Any, Optional
from itertools import count
from sklearn.utils.validation import check_is_fitted
from interpret.glassbox import ExplainableBoostingClassifier
from numpy import ndarray, count_nonzero, bool_
from torch import Tensor
from wandb import Plotly
from src.machine_learning.model.sklearn_model import SkLearnModel
from src.utility.environment import Environment
from src.utility.configs.config import Config


class ExplainableBoostingMachine(SkLearnModel):
    """
    This class implements ExplainableBoostingMachine model.

    Args:
        config (Config): The experiment configuration.
        environment (Environment): The environment.
        example_input_array (Tensor): The example input array.
        custom_logger (Any): The custom logger.
    """

    def __init__(
        self,
        *,
        config: Config = None,
        environment: Environment,
        example_input_array: Tensor = None,
        logger: Optional[Any] = None,
    ):
        self.model = None
        super().__init__(
            config=config,
            model_type=ExplainableBoostingClassifier,
            example_input_array=example_input_array,
            environment=environment,
            logger=logger,
        )

    def fit(self, x: ndarray | Tensor, y: ndarray | Tensor):
        """
        This method fits the model.

        Args:
            x (ndarray | Tensor): The input data.
            y (ndarray | Tensor): The output data.
        """
        super().fit(x, y)
        self.model = self.sweep(terms=True, bins=True)

    def log_model_summary(self):
        """
        This method logs the model summary.
        """
        explanation = self.model.explain_global(name="Explainable boosting machine")
        self.log(
            "explainable_boosting_machine/explain_global",
            Plotly(explanation.visualize()),
        )

        for i, feature in enumerate(explanation.feature_names):
            self.log(
                f"explainable_boosting_machine/features/{str(feature)}",
                Plotly(explanation.visualize(i)),
            )

    def sweep(
        self,
        terms=True,
        bins=True,
    ):
        """Purges unused elements from a fitted EBM.

        Args:
            terms: Boolean indicating if zeroed terms that do not affect the output
                should be purged from the model.
            bins: Boolean indicating if unused bin levels that do not affect the output
                should be purged from the model.

        Returns:
            Itself.
        """

        check_is_fitted(self.model, "has_fitted_")
        _log = getLogger("_ebm")

        if terms is True:
            terms = [
                i
                for i, v in enumerate(self.model.term_scores_)
                if count_nonzero(v) == 0
            ]
            self.remove_terms(terms)
        elif terms is not False:
            msg = "terms must be True or False"
            _log.error(msg)
            raise ValueError(msg)

        if bins is True:
            self.remove_unused_higher_bins(self.model.term_features_, self.model.bins_)
            self.deduplicate_bins(self.model.bins_)
        elif bins is not False:
            msg = "bins must be True or False"
            _log.error(msg)
            raise ValueError(msg)

        return self.model

    def remove_terms(self, terms):
        """Removes terms (and their associated components) from a fitted EBM. Note
        that this will change the structure (i.e., by removing the specified
        indices) of the following components of ``self``: ``term_features_``,
        ``term_names_``, ``term_scores_``, ``bagged_scores_``,
        ``standard_deviations_``, and ``bin_weights_``.

        Args:
            terms: A list (or other enumerable object) of term names or indices or booleans.

        Returns:
            Itself.
        """
        check_is_fitted(self.model, "has_fitted_")

        # If terms contains term names, convert them to indices
        terms = self.clean_indexes(
            terms,
            len(self.model.term_features_),
            getattr(self.model, "term_names_", None),
            "terms",
            "self.term_names_",
        )

        def _remove_indices(x, idx):
            """
            Remove elements of a list based on provided index
            """
            return [i for j, i in enumerate(x) if j not in idx]

        term_features = _remove_indices(self.model.term_features_, idx=terms)
        term_names = _remove_indices(self.model.term_names_, idx=terms)
        term_scores = _remove_indices(self.model.term_scores_, idx=terms)
        bagged_scores = _remove_indices(self.model.bagged_scores_, idx=terms)
        standard_deviations = _remove_indices(
            self.model.standard_deviations_, idx=terms
        )
        bin_weights = _remove_indices(self.model.bin_weights_, idx=terms)

        # Update components of self
        self.model.term_features_ = term_features
        self.model.term_names_ = term_names
        self.model.term_scores_ = term_scores
        self.model.bagged_scores_ = bagged_scores
        self.model.standard_deviations_ = standard_deviations
        self.model.bin_weights_ = bin_weights

        return self.model

    def remove_unused_higher_bins(self, term_features, bins):
        """
        many features are not used in pairs, so we can simplify the model
        by removing the extra higher interaction level bins
        """

        highest_levels = [0] * len(bins)
        for feature_idxs in term_features:
            for feature_idx in feature_idxs:
                highest_levels[feature_idx] = max(
                    highest_levels[feature_idx], len(feature_idxs)
                )

        for bin_levels, max_level in zip(bins, highest_levels):
            del bin_levels[max_level:]

    def deduplicate_bins(self, bins):
        """
        calling this function before calling score_terms allows score_terms to operate more efficiently since it'll
        be able to avoid re-binning data for pairs that have already been processed in mains or other pairs since we
        use the id of the bins to identify feature data that was previously binned
        """

        uniques = {}
        # pylint: disable=consider-using-enumerate
        for feature_idx in range(len(bins)):
            bin_levels = bins[feature_idx]
            highest_key = None
            highest_idx = -1
            for level_idx, feature_bins in enumerate(bin_levels):
                if isinstance(feature_bins, dict):
                    key = frozenset(feature_bins.items())
                else:
                    key = tuple(feature_bins)
                existing = uniques.get(key, None)
                if existing is None:
                    uniques[key] = feature_bins
                else:
                    bin_levels[level_idx] = existing

                if highest_key != key:
                    highest_key = key
                    highest_idx = level_idx
            del bin_levels[highest_idx + 1 :]

    # pylint: disable=too-many-branches
    def clean_indexes(self, indexes, n_items, names, param_name, attribute_name):
        """
        This method cleans the indexes.
        """
        _log = getLogger("_ebm")
        if names is not None:
            names = dict(zip(names, count()))
        n_bools = 0
        n_indexes = 0
        result = set()
        for i, v in enumerate(indexes):
            n_indexes += 1
            if isinstance(v, (bool, bool_)):
                n_bools += 1
                if v:
                    v = i
            elif isinstance(v, str):
                if names is None:
                    msg = f"{param_name} cannot be indexed by name since {attribute_name} has been removed."
                    _log.error(msg)
                    raise ValueError(msg)
                try:
                    v = names[v]
                except KeyError as exc:
                    msg = f'{attribute_name} does not contain "{v}".'
                    _log.error(msg)
                    raise ValueError(msg) from exc
            else:
                if isinstance(v, float):
                    if v.is_integer():
                        v = int(v)
                    else:
                        msg = f"{param_name} contains {v}, which is not an integer."
                        _log.error(msg)
                        raise ValueError(msg)
                else:
                    msg = f"{param_name} must contain integer indexes or string names or booleans."
                    _log.error(msg)
                    raise ValueError(msg)

                if v < 0 or n_items <= v:
                    msg = f"{param_name} index {v} out of bounds."
                    _log.error(msg)
                    raise ValueError(msg)

            result.add(v)

        if n_bools != 0:
            if n_indexes != n_bools:
                msg = f"If {param_name} contains booleans, they must all be booleans."
                _log.error(msg)
                raise ValueError(msg)
            if n_items != n_bools:
                msg = f"If {param_name} contains booleans, it must be the same length as in the EBM."
                _log.error(msg)
                raise ValueError(msg)

        return result
