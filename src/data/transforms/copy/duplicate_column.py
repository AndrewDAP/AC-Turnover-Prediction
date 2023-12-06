"""
This class adds copy columns to the dataframe under another name
"""

from typing import Dict, Tuple
from pandas import DataFrame

from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame

from src.utility.configs.config import Config

from src.utility.environment import Environment


class DuplicateColumn(DataframeTransform):
    """
    This class adds copy columns to the dataframe under another name
    """

    def __init__(self, columns: Dict[str, str] = None) -> None:
        self.columns = columns

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        for new_name, old_name in self.columns.items():
            dataframe = self.duplicate_column(dataframe, old_name, new_name)
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "columns": {str(key): str(value) for key, value in self.columns.items()},
        }

    def duplicate_column(
        self, dataframe: DataFrame, name: str, new_name: str
    ) -> DataFrame:
        """
        This function duplicates and rename a column
        """
        dataframe[new_name] = dataframe[name].copy()
        return dataframe
