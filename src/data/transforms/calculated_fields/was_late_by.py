"""
This module contains a class that calculates the amount of time an employee was late by
"""

from typing import Tuple
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema


class WasLateBy(DataframeTransform):
    """
    This class is used to calculate the amount of time an employee was late by
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

        dataframe[AugmentedVisitSchema.WAS_LATE_BY] = (
            dataframe[AugmentedVisitSchema.START_TIME]
            - dataframe[AugmentedVisitSchema.VISIT_START_AT]
        ).dt.total_seconds() / 60

        dataframe[AugmentedVisitSchema.WAS_LATE_BY] = dataframe[
            AugmentedVisitSchema.WAS_LATE_BY
        ].apply(lambda x: max(0, x))

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
