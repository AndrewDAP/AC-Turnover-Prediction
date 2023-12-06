"""
This module contains a class that aggregates by the given column and by the specified methods
"""

from typing import Tuple, Union
from typing import Dict
from pandas import DataFrame
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.configs.config import Config
from src.utility.environment import Environment
from src.data.transforms.aggregate.custom_aggregate_function import custom_functions


class AggregateBy(DataframeTransform):
    """
    This class aggregates by the given column and by the specified methods
    """

    def __init__(
        self, columns: [str] = None, aggregation_functions: Dict[str, str] = None
    ) -> None:
        self.columns = columns
        self.aggregation_functions = aggregation_functions

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        callable_functions = self.build_callable_functions(self.aggregation_functions)

        dataframe = (
            dataframe.groupby(self.columns).agg(callable_functions).reset_index()
        )
        return super().__call__(dataframe, errors, conf, env)

    def build_callable_functions(
        self, aggregation_functions: Dict[str, str]
    ) -> Dict[str, Union[str, callable]]:
        """
        This function replaces any custom function key with the real function
        """
        callable_functions = {}
        for key, value in aggregation_functions.items():
            if value in custom_functions:
                callable_functions[key] = custom_functions[value]
            else:
                callable_functions[key] = value
        return callable_functions

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "aggregation_functions": {
                str(key): str(value)
                for key, value in self.aggregation_functions.items()
            },
        }
