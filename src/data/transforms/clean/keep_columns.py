"""
KeepColumns is a class used to keep columns in the dataframe.
"""

from typing import List, Union, Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame


class KeepColumns(DataframeTransform):
    """
    This class is used to keep columns in the dataframe.

    Args:
        columns: The columns to keep.
        drop: Drop the columns.
    """

    def __init__(
        self,
        *,
        columns: Union[str, List[str]] = None,
        drop: bool = False,
    ) -> None:
        assert columns is not None
        self.drop = drop
        self.columns = columns if isinstance(columns, list) else [columns]

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        if self.drop:
            dataframe = dataframe.drop(columns=self.columns)
        else:
            dataframe = dataframe[self.columns]
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
            "drop": self.drop,
        }
