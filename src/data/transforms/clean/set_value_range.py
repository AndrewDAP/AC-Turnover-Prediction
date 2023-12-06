# pylint: disable=duplicate-code

"""
SetValueRange is a class used to set a range of valid values for a column.
"""

from typing import Optional, Union, Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.error.error_id import ErrorId


class SetValueRange(DataframeTransform):
    """
    This class is used to set a range of valid values for a column.

    Args:
        column: The column.
        min_value: The minimum value.
        max_value: The maximum value.
    """

    def __init__(
        self,
        columns: Optional[str] = None,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
    ) -> None:
        assert columns is not None
        self.columns = columns
        self.min_value = min_value
        self.max_value = max_value

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        for column in self.columns:
            if self.min_value is not None:
                errors = errors.add_errors(
                    dataframe=dataframe,
                    idx=dataframe[column] < self.min_value,
                    config=conf,
                    error_id=ErrorId.OUT_OF_RANGE,
                    error=f"{column} is less than {self.min_value}",
                )
                dataframe = dataframe[dataframe[column] >= self.min_value]
            if self.max_value is not None:
                errors = errors.add_errors(
                    dataframe=dataframe,
                    idx=dataframe[column] > self.max_value,
                    config=conf,
                    error_id=ErrorId.OUT_OF_RANGE,
                    error=f"{column} is greater than {self.max_value}",
                )
                dataframe = dataframe[dataframe[column] <= self.max_value]
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
            "min_value": self.min_value,
            "max_value": self.max_value,
        }
