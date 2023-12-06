"""
This module contains the tensor index schema.
"""
from pandas import DataFrame


class _TensorSchema:
    """
    This class is the tensor schema.
    """

    def __init__(self):
        self.mapping = {}

    def set_mapping(self, dataframe: DataFrame) -> None:
        """
        This method sets the mapping.

        Args:
            dataframe (DataFrame): The dataframe.
        """
        for index, column in enumerate(
            dataframe.columns[2:]
        ):  # skip employee id and period start
            self.mapping[column] = index

    def __getitem__(self, key) -> int:
        """
        This method returns the index of the column.
        """
        return self.mapping[key]


TensorSchema = _TensorSchema()
