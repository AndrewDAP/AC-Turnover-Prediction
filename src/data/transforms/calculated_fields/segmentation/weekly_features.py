"""
This module contains a class that calculates feature averages per employed week
"""

from typing import Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.segmentation_schema import SegmentationSchema


class WeeklyFeatures(DataframeTransform):
    """
    This class is used to calculate feature averages per employed week
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        number_of_weeks_employed = (
            dataframe[SegmentationSchema.EMPLOYEE_TENURE] * 365 / 7
        )
        dataframe[SegmentationSchema.AVG_VISIT_HOURS_PER_WEEK] = (
            dataframe[SegmentationSchema.TOTAL_VISIT_HOURS] / number_of_weeks_employed
        )
        dataframe[SegmentationSchema.AVG_VISITS_PER_WEEK] = (
            dataframe[SegmentationSchema.VISITS] / number_of_weeks_employed
        )
        dataframe[SegmentationSchema.AVG_LATE_ARRIVALS_PER_WEEK] = (
            dataframe[SegmentationSchema.LATE_ARRIVALS] / number_of_weeks_employed
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
