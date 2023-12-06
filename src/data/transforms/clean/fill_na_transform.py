"""
FillNaTransform class. A transform to fill na values in a dataframe.
"""
from typing import List, Literal, Optional, Tuple
from pandas import DataFrame
from tqdm.autonotebook import tqdm

from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.data.schema.schema_column import SchemaColumn


def mode_agg(x):
    """
    Calculate the mode of a series.
    """
    if isinstance(x, float):
        return x
    modes = x.mode()
    return modes[0] if len(modes) > 1 else 0


class FillNaColumn:
    """
    A class to represent a column in a schema.

    Args:
        column (SchemaColumn): The column.
        fill_policy (Literal["drop", "fill", "fill_with_default"]): The fill policy.
        method (Literal["mean", "median", "mode", "min", "max"]): The method for fill function.
        fill_by (Optional[str]): The column to group by.
        fill_default_value (Optional[SchemaColumn]): The default value to fill with.
    """

    def __init__(
        self,
        column: SchemaColumn,
        fill_policy: Literal["drop", "fill", "fill_with_default"] = "fill",
        method: Literal["mean", "median", "mode", "min", "max"] = None,
        fill_by: Optional[str] = None,
        fill_default_value: Optional["SchemaColumn"] = None,
    ) -> None:
        assert fill_policy in ["drop", "fill", "fill_with_default"]
        if fill_policy == "fill_with_default":
            assert fill_default_value is not None
        elif fill_policy == "fill":
            assert method in ["mean", "median", "mode", "min", "max"]
        self.column = column
        self.fill_policy = fill_policy
        self.fill_default_value = fill_default_value
        self.method = method
        self.is_mode = self.method == "mode"
        if self.is_mode:
            self.method = mode_agg
        self.fill_by = fill_by

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "column": self.column.name,
            "fill_policy": self.fill_policy,
            "method": self.method if not self.is_mode else "mode",
            "fill_by": self.fill_by.name if self.fill_by is not None else None,
            "fill_default_value": self.fill_default_value,
        }


class FillNaTransform(DataframeTransform):
    """
    A class to represent the fillna transform.

    Args:
        columns (List[FillNAColumn]): The columns.
    """

    def __init__(
        self,
        *,
        columns: List[FillNaColumn] = None,
    ) -> None:
        assert columns is not None
        self.columns = columns

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(desc="Filling NA values", position=4, leave=False)

        with tqdm(
            total=len(self.columns),
            desc="Filling NA values",
            unit="column",
            position=3,
            leave=False,
        ) as progress_bar:
            drop_columns = [
                column for column in self.columns if column.fill_policy == "drop"
            ]
            progress_bar.set_description(
                f"Dropping NA values for {[fill_na_column.to_dict() for fill_na_column in drop_columns]}"
            )
            dataframe = dataframe.dropna(
                subset=[fill_na_column.column.name for fill_na_column in drop_columns]
            )
            progress_bar.update(len(drop_columns))

            to_fill_by_columns = {}
            for fill_na_column in self.columns:
                if fill_na_column.fill_by is not None:
                    if fill_na_column.fill_by.name not in to_fill_by_columns:
                        to_fill_by_columns[fill_na_column.fill_by.name] = []
                    to_fill_by_columns[fill_na_column.fill_by.name].append(
                        fill_na_column
                    )
            for fill_by, fill_na_columns in to_fill_by_columns.items():
                progress_bar.set_description(
                    f"Filling NA values for {[fill_na_column.to_dict() for fill_na_column in fill_na_columns]}"
                )
                dataframe[
                    [fill_na_column.column.name for fill_na_column in fill_na_columns]
                ] = dataframe.groupby(fill_by)[
                    [fill_na_column.column.name for fill_na_column in fill_na_columns]
                ].progress_apply(
                    lambda x: x.fillna(
                        {
                            fill_na_column.column.name: x[
                                fill_na_column.column.name
                            ].agg(fill_na_column.method)
                            if not fill_na_column.is_mode
                            else x[fill_na_column.column.name].mode()[0]
                            if len(x[fill_na_column.column.name].mode() > 1)
                            else 0
                            # pylint: disable=cell-var-from-loop
                            for fill_na_column in fill_na_columns
                        }
                    )
                )
                progress_bar.update(len(fill_na_columns))

            fill_na_columns = [
                column
                for column in self.columns
                if column.fill_by is None and column.fill_policy != "drop"
            ]
            progress_bar.set_description(
                f"Filling NA values for {[fill_na_column.to_dict() for fill_na_column in fill_na_columns]}"
            )
            columns_names = [
                fill_na_column.column.name for fill_na_column in fill_na_columns
            ]
            dataframe[columns_names] = dataframe[columns_names].fillna(
                {
                    fill_na_column.column.name: fill_na_column.fill_default_value
                    if fill_na_column.fill_policy == "fill_with_default"
                    else dataframe[fill_na_column.column.name].agg(
                        fill_na_column.method
                    )
                    if not fill_na_column.is_mode
                    else dataframe[fill_na_column.column.name].mode()[0]
                    if len(dataframe[fill_na_column.column.name].mode() > 1)
                    else 0
                    # pylint: disable=cell-var-from-loop
                    for fill_na_column in fill_na_columns
                }
            )

            progress_bar.update(len(fill_na_columns))

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "columns": [column.to_dict() for column in self.columns],
        }
