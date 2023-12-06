"""
Join two dataframes together.
"""

from typing import Tuple, Union
from pandas import DataFrame, Series
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform


class Join(DataframeTransform):
    """
    Join two dataframes together.

    Args:
        right (Union[DataFrame, Series, str]): The right dataframe , series or name of stage in pipeline.
        how (MergeHow, optional): The merge how. Defaults to "inner".
        on (Optional[IndexLabel], optional): The index label. Defaults to None.
        left_on (Optional[IndexLabel], optional): The left index label. Defaults to None.
        right_on (Optional[IndexLabel], optional): The right index label. Defaults to None.
        left_index (bool, optional): Whether to use left index. Defaults to False.
        right_index (bool, optional): Whether to use right index. Defaults to False.
        suffixes (Suffixes, optional): The suffixes. Defaults to ("_x", "_y").
    """

    def __init__(
        self,
        *,
        right: Union[DataFrame, Series, str],
        how="inner",
        on=None,
        left_on=None,
        right_on=None,
        left_index: bool = False,
        right_index: bool = False,
        suffixes=("_x", "_y"),
    ) -> None:
        self.right = right
        self.right_name = right if isinstance(right, str) else None
        self.how = how
        self.on = on
        self.left_on = left_on
        self.right_on = right_on
        self.left_index = left_index
        self.right_index = right_index
        self.suffixes = suffixes

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataframe = dataframe.merge(
            right=self.right,
            how=self.how,
            on=self.on,
            left_on=self.left_on,
            right_on=self.right_on,
            left_index=self.left_index,
            right_index=self.right_index,
            suffixes=self.suffixes,
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
            "right": self.right_name,
            "how": self.how,
            "on": [on.name for on in self.on] if self.on else None,
            "left_on": [left_on.name for left_on in self.left_on]
            if self.left_on
            else None,
            "right_on": [right_on.name for right_on in self.right_on]
            if self.right_on
            else None,
            "left_index": self.left_index,
            "right_index": self.right_index,
            "suffixes": self.suffixes,
        }
