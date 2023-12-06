"""
This class checks if any rows still have None values after fillna, display and drops them
"""

from typing import Tuple

from pandas import DataFrame

from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.configs.config import Config
from src.utility.environment import Environment


class DropAfterFillNa(DataframeTransform):
    """
    This class checks if any rows still have None values after fillna, display and drops them
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataframe = self.drop_na_rows(dataframe)
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

    def drop_na_rows(self, dataframe: DataFrame):
        """
        This function checks if a row has None value and drops it
        """
        rows_with_none = dataframe[dataframe.isna().any(axis=1)]
        if len(rows_with_none) > 0:
            dataframe = dataframe.dropna()
        return dataframe
