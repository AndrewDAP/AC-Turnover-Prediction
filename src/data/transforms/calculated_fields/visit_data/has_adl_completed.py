"""
Has ADL completed calculated field
"""

from typing import Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.visit_schema import VisitSchema


class HasADLComplete(DataframeTransform):
    """
    This class is used to know if a visit had a scheduled ADL that is completed.
    Will be used in employee history calculated field stage to compute ADL completion rate.
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataframe[VisitSchema.VISIT_HAS_ADL_COMPLETED.name] = (
            dataframe[VisitSchema.VISIT_HAS_ADL]
            * dataframe[VisitSchema.VISIT_ADL_COMPLETE]
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
            "column": VisitSchema.VISIT_HAS_ADL_COMPLETED.name,
        }
