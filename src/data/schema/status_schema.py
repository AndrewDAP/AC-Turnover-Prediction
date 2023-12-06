"""
Status data schema.
"""

from src.data.schema.schema import Schema
from src.data.schema.schema_column import SchemaColumn


class _StatusSchemaRaw(Schema):
    """
    Status schema. before cleaning
    """

    EMPLOYEE_ID = SchemaColumn(name="EMPLOYEE_ID")
    STATUS_HISTORICAL = SchemaColumn(name="STATUS_HISTORICAL")
    STATUS_START_DATE = SchemaColumn(name="STATUS_START_DATE")
    STATUS_END_DATE = SchemaColumn(name="STATUS_END_DATE")
    STATUS_DAYS = SchemaColumn(name="STATUS_DAYS")


StatusSchemaRaw = _StatusSchemaRaw()


class _StatusSchema(Schema):
    """
    Status schema. after cleaning
    """

    EMPLOYEE_ID = SchemaColumn(
        name="EMPLOYEE_ID",
        parents=[StatusSchemaRaw.EMPLOYEE_ID],
    )

    STATUS_HISTORICAL = SchemaColumn(
        name="STATUS_HISTORICAL",
        parents=[StatusSchemaRaw.STATUS_HISTORICAL],
    )

    STATUS_START_DATE = SchemaColumn(
        name="STATUS_START_DATE",
        parents=[StatusSchemaRaw.STATUS_START_DATE],
        is_datetime=True,
    )

    STATUS_END_DATE = SchemaColumn(
        name="STATUS_END_DATE",
        parents=[StatusSchemaRaw.STATUS_END_DATE],
        is_datetime=True,
    )

    STATUS_DAYS = SchemaColumn(
        name="STATUS_DAYS",
        parents=[StatusSchemaRaw.STATUS_DAYS],
    )


StatusSchema = _StatusSchema(
    parents=[StatusSchemaRaw],
)
