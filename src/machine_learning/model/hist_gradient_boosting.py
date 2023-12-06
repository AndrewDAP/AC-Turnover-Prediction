"""
HistGradientBoosting model.
"""
from sklearn.ensemble import HistGradientBoostingClassifier
from torch import Tensor
from src.machine_learning.model.sklearn_model import SkLearnModel
from src.utility.environment import Environment
from src.utility.logger import Logger
from src.utility.configs.config import Config


class HistGradientBoosting(SkLearnModel):
    """
    This class implements a HistGradientBoosting model.
    https://scikit-learn.org/stable/modules/ensemble.html#ensembles-gradient-boosting-random-forests-bagging-voting-stacking

    Args:
        config (Config): The experiment configuration.
        environment (Environment): The environment.
        example_input_array (Tensor): The example input array.
        logger (Logger): The logger.
    """

    def __init__(
        self,
        *,
        config: Config = None,
        environment: Environment,
        example_input_array: Tensor = None,
        logger: Logger = None
    ):
        super().__init__(
            model_type=HistGradientBoostingClassifier,
            config=config,
            environment=environment,
            example_input_array=example_input_array,
            logger=logger,
        )
