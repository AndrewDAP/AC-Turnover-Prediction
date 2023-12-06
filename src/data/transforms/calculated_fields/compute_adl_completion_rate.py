"""
ADL completion rate calculated field
"""

from typing import Tuple
from pandas import DataFrame
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame


class ComputeADLCompletionRate(DataframeTransform):
    """
    This class is used to calculate ADL completion rate
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        sum_adl_completed = dataframe[AugmentedVisitSchema.VISIT_HAS_ADL_COMPLETE.name]
        total_adl = dataframe[AugmentedVisitSchema.VISIT_HAS_ADL.name]
        dataframe[EmployeeHistorySchema.ADL_COMPLETION_RATE_PER_PERIOD] = (
            sum_adl_completed / total_adl
        )

        # Dropping VISIT_HAS_ADL and VISIT_HAS_ADL_COMPLETE as they are no longer necessary
        columns_to_drop = [
            AugmentedVisitSchema.VISIT_HAS_ADL.name,
            AugmentedVisitSchema.VISIT_HAS_ADL_COMPLETE.name,
        ]
        dataframe.drop(columns_to_drop, axis=1, inplace=True)

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "column": EmployeeHistorySchema.ADL_COMPLETION_RATE_PER_PERIOD.name,
        }
