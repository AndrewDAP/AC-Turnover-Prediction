"""
This module contains the RenameColumns class.
"""

from typing import Tuple
from pandas import DataFrame
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.schema.schema import Schema


class RenameColumns(DataframeTransform):
    """
    This class is used to rename the columns in the dataframe.

    Args:
        to_schema: The schema to rename the columns to.
    """

    def __init__(
        self,
        to_schema: Schema,
    ) -> None:
        self.to_schema = to_schema

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        for column in self.to_schema.columns:
            if len(column.parents) != 1:
                continue
            parent = column.parents[0]

            if parent.name not in dataframe.columns:
                continue

            dataframe.rename(
                columns={
                    parent.name: column.name,
                },
                inplace=True,
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
            "to_schema": self.to_schema.to_dict(),
        }
