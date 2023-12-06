"""
This module contains the SetTypesClock class, which is used to set the types of the clock data.
"""
from pandas import DataFrame, to_datetime
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.clock_schema import ClockSchema


class SetTypesClock(DataframeTransform):
    """
    This class is used to set the types of the clock data.
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> DataFrame:
        dataframe[ClockSchema.VISIT_ID] = dataframe[ClockSchema.VISIT_ID].astype(
            int, errors="ignore"
        )
        dataframe[ClockSchema.PUNCH] = dataframe[ClockSchema.PUNCH].astype(
            int, errors="ignore"
        )
        dataframe[ClockSchema.START_TIME] = to_datetime(
            dataframe[ClockSchema.START_TIME],
            errors="coerce",
        )
        dataframe[ClockSchema.END_TIME] = to_datetime(
            dataframe[ClockSchema.END_TIME],
            errors="coerce",
        )
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {"name": self.__class__.__name__}
