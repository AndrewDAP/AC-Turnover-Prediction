"""
SHAPExplainer explainer class.
"""

from time import time
from numpy import stack, tile
from pandas import DataFrame
from shap import KernelExplainer, sample
from shap._explanation import Explanation
from src.machine_learning.model.model import Model
from src.analysis.shap.shap_explanation import ShapExplanation


class SHAPExplainer:
    """
    Class that represents a shap explainer.

    Args:
        model (Model): The model to explain.
        dataframe (DataFrame): The dataframe containing the dataset.
        nsamples (int): The number of samples to use.
        seed (int): The seed to use.
    """

    def __init__(
        self,
        *,
        model: Model = None,
        dataframe: DataFrame = None,
        nsamples: int = None,
        seed: int = None,
    ) -> None:
        assert model is not None
        assert dataframe is not None
        assert nsamples is not None
        assert seed is not None
        self.model = model
        self.dataframe = dataframe
        self.feature_names = dataframe.columns
        self.seed = seed
        self.explainer = KernelExplainer(
            model=self.model,
            data=sample(self.dataframe, nsamples, self.seed),
            link="logit",
            feature_names=self.feature_names,
        )

    def explain(self, sample_dataframe: DataFrame) -> ShapExplanation:
        """
        Explains the model.

        Args:
            sample_dataframe (DataFrame): The sample to explain.
        """
        start_time = time()

        shap_values = self.explainer.shap_values(sample_dataframe)
        if isinstance(shap_values, list):
            shap_values = stack(shap_values, axis=-1)  # put outputs at the end

        # the explanation object expects an expected value for each row
        if hasattr(self.explainer.expected_value, "__len__"):
            base_values = tile(self.explainer.expected_value, (shap_values.shape[0], 1))
        else:
            base_values = tile(self.explainer.expected_value, shap_values.shape[0])

        explanation = Explanation(
            shap_values,
            base_values=base_values,
            data=sample_dataframe.to_numpy(),
            feature_names=self.feature_names,
            compute_time=time() - start_time,
        )
        return ShapExplanation(
            explanation=explanation,
            shap_values=self.explainer.shap_values(sample_dataframe)[0],
            feature_names=self.feature_names,
            expected_value=self.explainer.expected_value,
            features_dataframe=sample_dataframe,
            model=self.model,
        )
