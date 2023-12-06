"""
SumSalaryPerVisit is a class used to calculate the total pay per visit
"""
from typing import Tuple
from pandas import DataFrame
from tqdm.autonotebook import tqdm

from src.data.schema.visit_schema import VisitSchema
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.utility.environment import Environment
from src.utility.configs.config import Config


class SumSalaryPerVisit(DataframeTransform):
    """
    This class is used to calculate the total pay per visit
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(desc="Summing salary per visit", position=3, leave=False)
        dataframe[VisitSchema.VISIT_TOTAL_PAY] = dataframe.progress_apply(
            self.compute_total_pay, axis=1
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

    def compute_total_pay(self, row):
        """
        This method computes the total pay per visit
        """
        if row[VisitSchema.VISIT_COMPUTED_RATE_UNITS] == "hours":
            return (
                row[VisitSchema.VISIT_COMPUTED_RATE]
                * row[VisitSchema.VISIT_HOURS_APPROVED]
            )
        if row[VisitSchema.VISIT_COMPUTED_RATE_UNITS] == "visits":
            return row[VisitSchema.VISIT_COMPUTED_RATE]
        return None
