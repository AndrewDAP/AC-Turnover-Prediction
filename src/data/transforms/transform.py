"""
DataframeTransform is an abstract class that defines the interface for all DataframeTransform.
"""
from abc import ABC, abstractmethod
from typing import Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.error.error_dataframe import ErrorDataFrame


class DataframeTransform(ABC):
    """
    This class is an abstract class that defines the interface for all DataframeTransforms.
    """

    @abstractmethod
    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataframe.columns = dataframe.columns.astype(str)
        return dataframe, errors

    @abstractmethod
    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
