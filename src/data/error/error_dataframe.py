"""
This module contains the function to create an error table from a dataframe.
"""

from typing import Optional
from pandas import DataFrame, Series, concat
from src.data.error.error_id import ErrorId
from src.utility.configs.config import Config


class ErrorDataFrame(DataFrame):
    """
    This class is the error dataframe.

    Args:
        data: Data to initialize the dataframe's columns with.
        fill: Fill the dataframe with the data.
        load_id: The load id.
        error_id: The error id.
        error: The error.
        copy: Copy data from inputs.
        shallow_copy: Copy data from inputs.
    """

    def __init__(
        self,
        data=None,
        fill=False,
        config: Optional[Config] = None,
        error_id: Optional[ErrorId] = None,
        error: Optional[str] = None,
        shallow_copy=False,
        copy: Optional[bool] = None,
    ) -> None:
        assert not (config is None and not shallow_copy)
        if not shallow_copy:
            dataframe = DataFrame(data)
            error_dataframe = DataFrame(
                columns=dataframe.columns, index=dataframe.index if fill else None
            )
            if fill:
                error_dataframe[dataframe.columns] = dataframe[dataframe.columns]
            error_dataframe.insert(0, "error", error)
            error_dataframe.insert(0, "error_id", error_id)
            error_dataframe.insert(0, "load_id", config.load_id)

        super().__init__(
            data=error_dataframe if not shallow_copy else data,
            copy=copy,
        )

    def add_errors(
        self,
        dataframe: DataFrame,
        idx: Series,
        config: Optional[Config],
        error_id: ErrorId,
        error: str,
    ) -> DataFrame:
        """
        This function adds errors to the error dataframe.

        Args:
            dataframe: The dataframe from which the errors ocurred.
            idx: The indexes for the error.
            load_id: The load id.
            error_id: The error id.
            error: The error.

        Returns:
            The error dataframe.
        """

        errors = ErrorDataFrame(
            dataframe.loc[idx],
            fill=True,
            config=config,
            error_id=error_id.name,
            error=error,
        )

        if len(self) == 0:
            return errors

        errors = ErrorDataFrame(
            concat(
                [
                    self,
                    errors,
                ],
                axis="rows",
                ignore_index=True,
            ),
            shallow_copy=True,
        )
        return errors

    @property
    def _constructor_expanddim(
        self,
    ):
        return ErrorDataFrame
