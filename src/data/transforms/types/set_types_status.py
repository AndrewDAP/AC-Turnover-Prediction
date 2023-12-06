"""
This module contains the SetTypesStatus class, which is used to set the types of the status data.
"""
from pandas import DataFrame, to_datetime
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.status_schema import StatusSchema


class SetTypesStatus(DataframeTransform):
    """
    This class is used to set the types of the status data.
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> DataFrame:
        dataframe[StatusSchema.EMPLOYEE_ID] = dataframe[
            StatusSchema.EMPLOYEE_ID
        ].astype(int, errors="ignore")
        dataframe[StatusSchema.STATUS_HISTORICAL] = dataframe[
            StatusSchema.STATUS_HISTORICAL
        ].astype(str, errors="ignore")
        dataframe[StatusSchema.STATUS_START_DATE] = to_datetime(
            dataframe[StatusSchema.STATUS_START_DATE],
            errors="coerce",
        )
        dataframe[StatusSchema.STATUS_END_DATE] = to_datetime(
            dataframe[StatusSchema.STATUS_END_DATE],
            errors="coerce",
        )
        dataframe[StatusSchema.STATUS_DAYS] = dataframe[
            StatusSchema.STATUS_DAYS
        ].astype(int, errors="ignore")
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {"name": self.__class__.__name__}
