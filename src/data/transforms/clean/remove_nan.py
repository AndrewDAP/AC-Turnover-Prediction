"""
This class is used to remove the nan values from the dataframe. and replace them with None
"""
from typing import List, Tuple
from pandas import DataFrame
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform


class RemoveNan(DataframeTransform):
    """
    This class is used to remove the nan values from the dataframe. and replace them with None

    Args:
        columns: The columns to remove the nan values from.
    """

    def __init__(
        self,
        columns: List[str] = None,
    ) -> None:
        self.columns = columns if columns is not None else []

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        for column in self.columns:
            dataframe[column][dataframe[column] == "nan"] = None

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "columns": [str(column) for column in self.columns],
        }
