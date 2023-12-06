"""
Shap explanation class.
"""
from typing import Optional, Union, List
from matplotlib.figure import Figure
from matplotlib.pyplot import gcf, clf
from pandas import DataFrame
from numpy import ndarray
from shap import decision_plot
from shap.plots import waterfall, scatter
from shap._explanation import Explanation
from src.analysis.shap.plots.bee_swarm import beeswarm
from src.utility.configs.config import Config
from src.machine_learning.model.model import Model


class ShapExplanation:
    """
    Class that represents a shap explanation.

    Args:
        explanation (Explanation): The explanation object.
        feature_names (list): The list of feature names.
        features_dataframe (DataFrame): The dataframe containing the features.
    """

    def __init__(
        self,
        explanation: Explanation,
        shap_values: Optional[Union[List[ndarray], ndarray]],
        feature_names: list,
        expected_value: float,
        features_dataframe: DataFrame,
        model: Model,
    ) -> None:
        self.explanation = explanation
        self.feature_names = feature_names
        self.shap_values = shap_values
        self.features_dataframe = features_dataframe
        self.model = model
        self.expected_value = expected_value
        self.feature_idx = None
        self.xlim = None

    def get_prediction(self, index: int) -> Explanation:
        """
        Returns the prediction for the given index.

        Args:
            index (int): The index of the prediction.
        """
        return self.explanation[index][:, 0]

    def get_feature_predictions(self, feature_name: str) -> Explanation:
        """
        Returns the predictions for the given feature.

        Args:
            feature_name (str): The name of the feature.
        """
        feature_name = str(feature_name)
        feature_index = self.explanation.feature_names.index(feature_name)
        return self.explanation[:, feature_index, 0]

    def waterfall_plot(
        self,
        *,
        prediction_index: int = None,
        show: bool = False,
    ) -> Figure:
        """
        Returns the waterfall plot for the given prediction index.

        Args:
            prediction_index (int): The index of the prediction.
            show (bool): Whether to show the plot.
        """
        assert prediction_index is not None
        prediction = self.get_prediction(prediction_index)
        clf()
        waterfall(prediction, show=show, max_display=99999)
        return gcf()

    def dependency_scatter_plot(
        self,
        *,
        feature_name: str,
        show: bool = False,
    ) -> Figure:
        """
        Returns the dependency scatter plot for the given feature.

        Args:
            feature_name (str): The name of the feature.
            show (bool): Whether to show the plot.
        """
        assert feature_name is not None
        feature_predictions = self.get_feature_predictions(feature_name)

        clf()
        scatter(
            feature_predictions,
            show=show,
            color=feature_predictions,
        )
        return gcf()

    def bee_swarm_plot(
        self,
        *,
        show: bool = False,
    ) -> Figure:
        """
        Returns the bee swarm plot.

        Args:
            show (bool): Whether to show the plot.
        """
        clf()
        beeswarm(self.explanation[:, :, 0], show=show, max_display=99999)
        return gcf()

    def decision_plot(
        self,
        show: bool = False,
    ) -> Figure:
        """
        Returns the decision plot.

        Args:
            show (bool): Whether to show the plot.
        """
        clf()
        plot_info = decision_plot(
            self.expected_value,
            self.shap_values,
            self.features_dataframe,
            link="logit",
            feature_order=self.feature_idx,
            xlim=self.xlim,
            return_objects=True,
            feature_display_range=slice(-1, -99999, -1),
            show=show,
        )
        self.feature_idx = plot_info.feature_idx
        self.xlim = plot_info.xlim
        return gcf()

    def decision_plot_misclassified(
        self,
        config: Config,
        y_true: ndarray,
        show: bool = False,
    ) -> Figure:
        """
        Returns the decision plot. Only miss classified samples are shown.

        Args:
            config (Config): The experiment configuration.
            y_true (ndarray): The true labels.
            show (bool): Whether to show the plot.
        """
        clf()
        logits = self.model.predict(self.features_dataframe.values).squeeze()
        y_prediction = logits > config.cutoff
        misclassified = y_prediction != y_true

        plot_info = decision_plot(
            self.expected_value,
            self.shap_values[misclassified],
            self.features_dataframe[misclassified],
            link="logit",
            feature_order=self.feature_idx,
            xlim=self.xlim,
            return_objects=True,
            feature_display_range=slice(-1, -99999, -1),
            show=show,
        )
        self.feature_idx = plot_info.feature_idx
        self.xlim = plot_info.xlim
        return gcf()
