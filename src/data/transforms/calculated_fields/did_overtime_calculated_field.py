"""
This module contains a class that calculates if an employee did overtime
"""

from typing import Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.employee_history_schema import EmployeeHistorySchema

# Working more than 5 minutes above shift duration is considered overtime
OVERTIME_THRESHOLD = 5 / 60


class DidOvertimeInPeriodCalculatedField(DataframeTransform):
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
        dataframe[EmployeeHistorySchema.DID_OVERTIME_IN_PERIOD] = 0
        dataframe.loc[
            dataframe[EmployeeHistorySchema.WORK_HOURS_DEVIATION_PER_PERIOD]
            > OVERTIME_THRESHOLD,
            EmployeeHistorySchema.DID_OVERTIME_IN_PERIOD,
        ] = 1
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
