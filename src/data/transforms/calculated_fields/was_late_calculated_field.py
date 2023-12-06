"""
This module contains a class that calculates if an employee did overtime
"""

from typing import Tuple
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema

# Working more than 5 minutes above shift duration is considered overtime
LATE_THRESHOLD = 15 / 60


class WasLateToVisitCalculatedField(DataframeTransform):
    """
    This class is used to calculate if an employee did overtime
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(
            desc="Computing if employee was late to visit", position=3, leave=False
        )
        dataframe[AugmentedVisitSchema.WAS_LATE_TO_VISIT] = (
            dataframe[AugmentedVisitSchema.START_TIME]
            > dataframe[AugmentedVisitSchema.VISIT_START_AT]
        ).astype(int)

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
        }
