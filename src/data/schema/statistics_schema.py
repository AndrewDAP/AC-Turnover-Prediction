"""
Statistics schema.
"""

from src.data.schema.schema import Schema
from src.data.schema.schema_column import SchemaColumn


class _StatisticSchema(Schema):
    """
    A class to represent the statistic schema.
    """

    COLUMN_NAME = SchemaColumn(
        name="COLUMN_NAME",
    )

    DATA_TYPE = SchemaColumn(
        name="DATA_TYPE",
    )

    ROW_COUNT = SchemaColumn(
        name="ROW_COUNT",
    )

    NULL_COUNT = SchemaColumn(
        name="NULL_COUNT",
    )

    MIN = SchemaColumn(
        name="MIN",
    )

    FIRST_QUARTILE = SchemaColumn(
        name="Q1",
    )

    MEDIAN = SchemaColumn(
        name="MEDIAN",
    )

    THIRD_QUARTILE = SchemaColumn(
        name="Q3",
    )

    MAX = SchemaColumn(
        name="MAX",
    )

    MEAN = SchemaColumn(
        name="MEAN",
    )

    STD_DEV = SchemaColumn(
        name="STD_DEV",
    )

    MODE = SchemaColumn(
        name="MODE",
    )


StatisticSchema = _StatisticSchema()
