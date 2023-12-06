"""
This module contains a class that calculates the ratio of a feature
"""

from typing import Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame


class FeatureRatios(DataframeTransform):
    """
    This class is used to calculate the ratio of a feature
    """

    def __init__(self, *, target_columns: [str] = None, key_column: str = None) -> None:
        assert target_columns is not None
        assert key_column is not None
        self.key_column = key_column
        self.target_columns = target_columns

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        for column in self.target_columns:
            dataframe[f"{column}_RATIO"] = (
                dataframe[column] / dataframe[self.key_column]
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
            "target_columns": [column.name for column in self.target_columns],
            "key_column": self.key_column.name,
        }
