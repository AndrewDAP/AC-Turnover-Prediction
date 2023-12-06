"""
This class is use to calculate the employee tenure
"""

from ast import Tuple
import pandas as pd
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.utility.configs.config import Config

from src.utility.environment import Environment


class ComputeStaticEmployeeTenure(DataframeTransform):
    """
    This class is use to calculate the employee tenure
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple(DataFrame, ErrorDataFrame):
        tqdm.pandas(desc="Computing employee tenure", position=3, leave=False)
        dataframe[AugmentedVisitSchema.EMPLOYEE_TENURE] = dataframe.progress_apply(
            self.compute_static_employee_tenure, axis=1
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

    def compute_static_employee_tenure(self, row, total_days=365.0):
        """
        Method computes how many years of employment
        """
        termination_date = row[AugmentedVisitSchema.EMPLOYEE_TERMINATION_DATE]
        if pd.notna(termination_date):
            return (
                row[AugmentedVisitSchema.EMPLOYEE_TERMINATION_DATE]
                - row[AugmentedVisitSchema.EMPLOYEE_START_ON]
            ).days / total_days
        return (
            row[AugmentedVisitSchema.PERIOD_START]
            - row[AugmentedVisitSchema.EMPLOYEE_START_ON]
        ).days / total_days
