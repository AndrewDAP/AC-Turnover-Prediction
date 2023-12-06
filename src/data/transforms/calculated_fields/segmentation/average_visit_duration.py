"""
This module contains a class that calculates the average visit duration
"""

from typing import Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.segmentation_schema import SegmentationSchema


class AverageVisitDuration(DataframeTransform):
    """
    This class is used to the average visit duration
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataframe[SegmentationSchema.AVG_VISIT_DURATION] = (
            dataframe[SegmentationSchema.TOTAL_VISIT_HOURS]
            / dataframe[SegmentationSchema.VISITS]
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
