"""
DataSlice is a class used to a log a data slice for better understanding.
"""

from os import path, makedirs
from typing import Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform


class DataSlice(DataframeTransform):
    """
    This class is used to a log a data slice for better understanding.
    Uses the cached directory to store the data slice.

    Args:
        sub_directory: The directory name.
        filename: The filename.
        slice_by: The column name on witch to slice.
    """

    def __init__(
        self,
        *,
        sub_directory: str = None,
        filename: str = None,
        slice_by: str = None,
        slice_size: int = 1,
    ) -> None:
        assert sub_directory is not None
        assert filename is not None
        assert slice_by is not None
        assert slice_size > 0
        self.sub_directory = sub_directory
        self.filename = filename
        self.slice_by = slice_by
        self.slice_size = slice_size

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        item_to_slice_on = (
            dataframe[self.slice_by].sort_values().unique()[: self.slice_size + 1]
        )
        output_df = dataframe[dataframe[self.slice_by].isin(item_to_slice_on)]

        if not path.exists(path.join(env.stats_dir, self.sub_directory)):
            makedirs(path.join(env.stats_dir, self.sub_directory))

        output_df.to_csv(
            path.join(env.stats_dir, self.sub_directory, f"{self.filename}.csv"),
            index=False,
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
            "slice_by": str(self.slice_by),
            "filename": self.filename,
            "slice_size": self.slice_size,
            "sub_directory": self.sub_directory,
        }
