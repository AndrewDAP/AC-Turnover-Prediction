"""
Model Factory
"""
from typing import Any, Optional
from torch import Tensor
from src.machine_learning.model.model import Model
from src.utility.factory import Factory
from src.utility.configs.config import Config
from src.utility.environment import Environment
from src.machine_learning.model.explainable_boosting_machine import (
    ExplainableBoostingMachine,
)
from src.machine_learning.model.perceptron import Perceptron
from src.machine_learning.model.support_vector_machine import SupportVectorMachine
from src.machine_learning.model.decision_tree import DecisionTree
from src.machine_learning.model.hist_gradient_boosting import HistGradientBoosting
from src.machine_learning.model.multi_layer_perceptron import MultiLayerPerceptron
from src.machine_learning.model.timesnet import TimesNet


class ModelFactory:
    """
    This class builds the model.

    Args:
        config (Config): The configuration.
        environment (Environment): The environment.
        example_input_array (Tensor): The example input array.
        logger (Logger): The logger.
    """

    def __init__(
        self,
        config: Config = None,
        environment: Environment = None,
        example_input_array: Tensor = None,
        logger: Optional[Any] = None,
    ) -> None:
        self.config = config
        self.environment = environment
        self.example_input_array = example_input_array
        self.logger = logger
        self.factory = Factory(
            registry={
                "ExplainableBoostingMachine": ExplainableBoostingMachine,
                "Perceptron": Perceptron,
                "SupportVectorMachine": SupportVectorMachine,
                "DecisionTree": DecisionTree,
                "HistGradientBoosting": HistGradientBoosting,
                "MultiLayerPerceptron": MultiLayerPerceptron,
                "TimesNet": TimesNet,
            },
        )

    def build(self) -> Model:
        """
        This method builds the model.

        Returns:
            ModelBase: The model.
        """
        return self.factory.create(
            self.config.model,
            config=self.config,
            environment=self.environment,
            example_input_array=self.example_input_array,
            logger=self.logger,
        )
