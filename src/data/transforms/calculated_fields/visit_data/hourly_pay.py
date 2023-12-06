"""
This module contains the HourlyPay class
"""
from typing import Tuple
from pandas import DataFrame
from tqdm.autonotebook import tqdm

from src.data.schema.visit_schema import VisitSchema
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.utility.environment import Environment
from src.utility.configs.config import Config


class HourlyPay(DataframeTransform):
    """
    This class is used to calculate the hourly pay during a visit
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(desc="Calculating visit hourly rate", position=3, leave=False)
        dataframe[VisitSchema.VISIT_HOURLY_PAY] = (
            dataframe[VisitSchema.VISIT_TOTAL_PAY]
            / dataframe[VisitSchema.VISIT_HOURS_APPROVED]
        )
        dataframe[VisitSchema.VISIT_HOURLY_PAY][
            dataframe[VisitSchema.VISIT_HOURLY_PAY] == "nan"
        ] = None
        dataframe[VisitSchema.VISIT_HOURLY_PAY][
            dataframe[VisitSchema.VISIT_HOURLY_PAY] == float("inf")
        ] = None
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "columns": [
                VisitSchema.VISIT_HOURLY_PAY.name,
                VisitSchema.VISIT_TOTAL_PAY.name,
                VisitSchema.VISIT_HOURS_APPROVED.name,
            ],
        }
