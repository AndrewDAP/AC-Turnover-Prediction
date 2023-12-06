"""This DataframeTransform class computes the amount of days to the first
   visit of every employee.
"""

from re import search
from typing import Tuple
from pandas import DataFrame
from numpy import where
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.data.transforms.transform import DataframeTransform
from src.utility.configs.config import Config
from src.utility.environment import Environment


class ComputeDaysToFirstVisit(DataframeTransform):
    """Computes the amount of days to the first visit for every employee"""

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataframe.sort_values(
            [
                EmployeeHistorySchema.PERIOD_START,
                EmployeeHistorySchema.EMPLOYEE_ID,
            ]
        )

        cumulative_count_dataframe = (
            dataframe.groupby(EmployeeHistorySchema.EMPLOYEE_ID)
            .cumcount()
            .reset_index()
        )

        # Fill the DAYS_TO_FIRST_VISIT column with a chronological count of periods
        # for each employee (1, 2, 3, etc.)
        dataframe[
            EmployeeHistorySchema.DAYS_TO_FIRST_VISIT
        ] = cumulative_count_dataframe[0]

        # Set DAYS_TO_FIRST_VISIT to 0 if...
        dataframe[EmployeeHistorySchema.DAYS_TO_FIRST_VISIT] = where(
            (
                # the first visit has already happened OR
                dataframe[EmployeeHistorySchema.PERIOD_START]
                > dataframe[EmployeeHistorySchema.EMPLOYEE_FIRST_VISIT]
            )
            | (
                # the employee's start date precedes the period of validity.
                dataframe[EmployeeHistorySchema.EMPLOYEE_START_ON]
                < conf.period_start
            ),
            0,
            dataframe[EmployeeHistorySchema.DAYS_TO_FIRST_VISIT],
        )

        # Multiply the DAYS_TO_FIRST_VISIT values by the period duration
        dataframe[EmployeeHistorySchema.DAYS_TO_FIRST_VISIT] = dataframe[
            EmployeeHistorySchema.DAYS_TO_FIRST_VISIT
        ] * self.parse_period_duration(conf.period_duration)

        return super().__call__(dataframe, errors, conf, env)

    def parse_period_duration(self, period_duration):
        """Returns the numeric part of the period_duration string

        Args:
            period_duration (str): one of  '1D', '2D', '3D', '4D', '5D', '7D', '14D', '30D'

        Returns:
            int: the period duration in days
        """
        match = search(r"\d+", period_duration)
        if match:
            return int(match.group())
        return 1

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
        }
