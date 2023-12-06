"""
CSV Must Value Equal
"""

from typing import Optional, Union, Tuple
from pandas import DataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.error.error_id import ErrorId


class ValueMustEqual(DataframeTransform):
    """
    This class is used to keep rows where a column equals a value.

    Args:
        column: The column to keep.
        value: The value to keep.
        invert: Invert the condition. Default is False.
    """

    def __init__(
        self,
        column: Optional[str] = None,
        value: Optional[Union[int, float]] = None,
        invert: bool = False,
    ) -> None:
        assert column is not None
        assert value is not None
        self.column = column
        self.value = value
        self.invert = invert

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        if self.invert:
            errors = errors.add_errors(
                dataframe=dataframe,
                idx=dataframe[self.column] == self.value,
                config=conf,
                error_id=ErrorId.INVALID_VALUE,
                error=f"{self.column} is equal to {self.value}",
            )
            dataframe = dataframe[dataframe[self.column] != self.value]
        else:
            errors = errors.add_errors(
                dataframe=dataframe,
                idx=dataframe[self.column] != self.value,
                config=conf,
                error_id=ErrorId.INVALID_VALUE,
                error=f"{self.column} is not equal to {self.value}",
            )
            dataframe = dataframe[dataframe[self.column] == self.value]
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """

        return {
            "name": self.__class__.__name__,
            "column": self.column.name,
            "value": self.value,
            "invert": self.invert,
        }
