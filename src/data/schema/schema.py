"""
A module for the Schema class.
"""
from typing import List
from src.data.schema.schema_column import SchemaColumn


class Schema:
    """
    A class to represent a schema.

    Args:
        parents (List[Schema]): The parent schemas.
    """

    def __init__(
        self,
        parents: List["Schema"] = None,
    ):
        self.parents = parents if parents else []

    @property
    def columns(self) -> List[SchemaColumn]:
        """
        Return the columns in the schema.
        """
        columns = []
        for attr in dir(self):
            if attr in ["columns", "datetime_columns"]:
                continue
            if isinstance(getattr(self, attr), SchemaColumn):
                columns.append(getattr(self, attr))
        return columns

    @property
    def datetime_columns(self) -> List[SchemaColumn]:
        """
        Return the datetime columns in the schema.
        """
        datetime_columns = []
        for column in self.columns:
            if column.is_datetime:
                datetime_columns.append(column)
        return datetime_columns

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {"columns": [column.name for column in self.columns]}
