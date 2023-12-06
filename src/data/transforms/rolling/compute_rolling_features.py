"""
This class performs a rolling window on the dataframe
"""

from collections import deque
from typing import Tuple

import pandas as pd
from pandas import DataFrame

from adtk.transformer import RollingAggregate
from adtk.data import validate_series

from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.configs.config import Config
from src.utility.environment import Environment

from src.data.schema.employee_history_schema import EmployeeHistorySchema


class ComputeRollingFeatures(DataframeTransform):
    """
    This class performs a rolling window on the dataframe
    """

    def __init__(self, params=None) -> None:
        self.params = params

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        transformed_queue = deque()

        window_size_fill = None

        for param in self.params:
            agg_function = param["agg_function"]
            arguments = param["arguments"]
            columns = param["columns"]
            window_size = param["window_size"]
            sub_name = param["sub_name"]

            dataframe = dataframe.ffill()
            dataframe = dataframe.bfill()

            sub_df = dataframe.loc[:, columns]

            window_size_fill = window_size - 1

            transformed_queue.append(
                self.rolling_window(
                    sub_df, agg_function, arguments, window_size, sub_name
                )
            )

        dataframe[EmployeeHistorySchema.PERIOD_START] = dataframe[
            EmployeeHistorySchema.PERIOD_START
        ].dt.strftime("%Y-%m-%d")

        while len(transformed_queue) != 0:
            dataframe = dataframe.merge(
                transformed_queue.popleft(),
                on=EmployeeHistorySchema.PERIOD_START.name,
                how="left",
            )

        new_columns = []
        fill_name = {}

        for column in dataframe.columns:
            if "mean" in column or "quantile" in column:
                new_columns.append(column)
                fill_name[column] = column.split("_rolling")[0]

        sub_df = dataframe[new_columns]

        for column in new_columns:
            sub_df.head(window_size_fill).loc[
                0:window_size_fill, column
            ] = dataframe.head(window_size_fill).loc[
                0:window_size_fill, fill_name[column]
            ]

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "params": [str(param) for param in self.params],
        }

    def rolling_window(
        self,
        dataframe: DataFrame,
        agg_function: str,
        arguments,
        window_size: int,
        sub_name: str,
    ) -> DataFrame:
        """
        a rolling window is passed through the dataframe
        """

        dataframe[EmployeeHistorySchema.PERIOD_START] = pd.to_datetime(
            dataframe[EmployeeHistorySchema.PERIOD_START]
        )

        dataframe.set_index(EmployeeHistorySchema.PERIOD_START, inplace=True)
        time_series = validate_series(dataframe)

        if agg_function == "quantile":
            transformed_df = RollingAggregate(
                agg=agg_function, agg_params=arguments, window=window_size
            ).transform(time_series)
        else:
            transformed_df = RollingAggregate(
                agg=agg_function, window=window_size
            ).transform(time_series)

        for column in transformed_df.columns:
            if column != EmployeeHistorySchema.PERIOD_START:
                transformed_df.rename(
                    columns={column: column + "_rolling_" + sub_name},
                    inplace=True,
                )

        transformed_df.reset_index(inplace=True)

        transformed_df[EmployeeHistorySchema.PERIOD_START] = transformed_df[
            EmployeeHistorySchema.PERIOD_START
        ].dt.strftime("%Y-%m-%d")

        return transformed_df
