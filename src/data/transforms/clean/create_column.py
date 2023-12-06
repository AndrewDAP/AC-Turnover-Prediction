"""
This module contains a class to create new float columns
"""
from typing import Tuple
from pandas import DataFrame
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform


class CreateColumn(DataframeTransform):
    """
    This class is used to create new columns

    Args:
        columns: The columns to remove the nan values from.
    """

    def __init__(self, columns: {} = None) -> None:
        self.columns = columns if columns is not None else {}

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        for column, value in self.columns.items():
            dataframe[column] = value

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "columns": [column.name for column in self.columns],
        }
