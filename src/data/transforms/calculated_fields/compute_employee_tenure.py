"""Compute Employee Tenure Class
"""

from typing import Tuple
from pandas import DataFrame
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.data.transforms.transform import DataframeTransform
from src.utility.configs.config import Config
from src.utility.environment import Environment


class ComputeDynamicEmployeeTenure(DataframeTransform):
    """This transform computes employee tenures dynamically"""

    DAYS_IN_YEAR = 365
    CAREER_START = "CAREER_START"

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        # Group by EMPLOYEE_ID and find the minimum date
        min_dates = dataframe.groupby(EmployeeHistorySchema.EMPLOYEE_ID)[
            [
                EmployeeHistorySchema.PERIOD_START,
                EmployeeHistorySchema.EMPLOYEE_START_ON,
            ]
        ].min()

        min_dates.reset_index(inplace=True)

        def find_min_date(row):
            return min(
                row[EmployeeHistorySchema.PERIOD_START],
                row[EmployeeHistorySchema.EMPLOYEE_START_ON],
            )

        min_dates["CAREER_START"] = min_dates.apply(find_min_date, axis=1)

        min_dates = min_dates.drop(
            columns=[
                EmployeeHistorySchema.PERIOD_START,
                EmployeeHistorySchema.EMPLOYEE_START_ON,
            ]
        )

        # Merge the minimum dates back into the original DataFrame
        dataframe = dataframe.merge(
            min_dates,
            on=EmployeeHistorySchema.EMPLOYEE_ID,
            how="left",
        )

        # Calculate the difference in days
        dataframe[EmployeeHistorySchema.EMPLOYEE_TENURE] = (
            dataframe[EmployeeHistorySchema.PERIOD_START] - dataframe["CAREER_START"]
        ).dt.days / self.DAYS_IN_YEAR

        dataframe[EmployeeHistorySchema.EMPLOYEE_TENURE].round(2)

        # Drop the intermediate column
        dataframe = dataframe.drop(
            columns=["CAREER_START"],
        )

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
