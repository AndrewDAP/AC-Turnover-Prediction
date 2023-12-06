"""
A module for the SchemaElement class.
"""

from typing import List, Optional

from src.data.schema.feature_type import FeatureType


class SchemaColumn:
    """
    A class to represent a column in a schema.

    Args:
        name (str): The name of the column.
        parents (List[SchemaColumn]): The parent columns.
        comments (Optional[str]): The comments for the column.
        is_datetime (bool): Whether the column is a datetime column.
    """

    def __init__(
        self,
        name: str = None,
        parents: List["SchemaColumn"] = None,
        feature_type: Optional[FeatureType] = None,
        comments: Optional[str] = None,
        is_datetime: bool = False,
    ) -> None:
        assert isinstance(name, str)

        self.name = name
        self.parents = parents if parents else []
        self.feature_type = feature_type
        self.comments = comments
        self.is_datetime = is_datetime

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.name,
            "parents": [parent.to_dict() for parent in self.parents],
            "comments": self.comments,
            "is_datetime": self.is_datetime,
        }

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __lt__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name < other.name
        if isinstance(other, str):
            return self.name < other
        return False

    def __gt__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name > other.name
        if isinstance(other, str):
            return self.name > other
        return False

    def __le__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name <= other.name
        if isinstance(other, str):
            return self.name <= other
        return False

    def __ge__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name >= other.name
        if isinstance(other, str):
            return self.name >= other
        return False

    def __ne__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name != other.name
        if isinstance(other, str):
            return self.name != other
        return False

    def __contains__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name in other.name
        if isinstance(other, str):
            return self.name in other
        return False

    def __add__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name + other.name
        if isinstance(other, str):
            return self.name + other
        return False

    def __sub__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name - other.name
        if isinstance(other, str):
            return self.name - other
        return False

    def __mul__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name * other.name
        if isinstance(other, str):
            return self.name * other
        return False

    def __truediv__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name / other.name
        if isinstance(other, str):
            return self.name / other
        return False

    def __floordiv__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name // other.name
        if isinstance(other, str):
            return self.name // other
        return False

    def __mod__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name % other.name
        if isinstance(other, str):
            return self.name % other
        return False

    def __pow__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name**other.name
        if isinstance(other, str):
            return self.name**other
        return False

    def __lshift__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name << other.name
        if isinstance(other, str):
            return self.name << other
        return False

    def __rshift__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name >> other.name
        if isinstance(other, str):
            return self.name >> other
        return False

    def __and__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name & other.name
        if isinstance(other, str):
            return self.name & other
        return False

    def __xor__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name ^ other.name
        if isinstance(other, str):
            return self.name ^ other
        return False

    def __or__(self, other: str) -> bool:
        if isinstance(other, SchemaColumn):
            return self.name | other.name
        if isinstance(other, str):
            return self.name | other
        return False
