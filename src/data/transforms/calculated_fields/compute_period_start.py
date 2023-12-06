"""
This class splits row into period using period parameter
"""

from typing import Tuple

from pandas import DataFrame
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.transforms.transform import DataframeTransform

from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.configs.config import Config
from src.utility.environment import Environment


class ComputePeriodStart(DataframeTransform):
    """
    This class splits row into period using period parameter
    """

    def __init__(
        self,
        period: str = "",
    ) -> None:
        self.period = period

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataframe = self.split_per_period(dataframe, self.period)
        return super().__call__(dataframe, errors, conf, env)

    def split_per_period(self, dataframe: DataFrame, period: str):
        """
        This function creates a new column PERIOD_START for each row
        """
        dataframe[AugmentedVisitSchema.PERIOD_START] = dataframe[
            AugmentedVisitSchema.VISIT_START_AT
        ].dt.floor(period)
        return dataframe

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {"name": self.__class__.__name__, "period": self.period}
