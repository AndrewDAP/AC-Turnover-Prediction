"""
Work hours deviation calculated field
"""

from typing import Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.visit_schema import VisitSchema


class WorkHoursDeviationCalculatedField(DataframeTransform):
    """
    This class is used to calculate the work hours deviation
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataframe[VisitSchema.VISIT_WORK_HOURS_DEVIATION.name] = (
            dataframe[VisitSchema.VISIT_HOURS_APPROVED]
            - dataframe[VisitSchema.VISIT_SCHEDULED_DURATION]
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
            "column": VisitSchema.VISIT_WORK_HOURS_DEVIATION.name,
        }
