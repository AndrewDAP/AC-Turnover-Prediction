"""
Y label data schema.
"""

from src.data.schema.schema import Schema
from src.data.schema.schema_column import SchemaColumn
from src.data.schema.status_schema import StatusSchema


class _YLabelSchema(Schema):
    """
    Y label schema
    """

    EMPLOYEE_ID = SchemaColumn(
        name="EMPLOYEE_ID",
        parents=[StatusSchema.EMPLOYEE_ID],
    )

    PERIOD_START = SchemaColumn(
        name="PERIOD_START",
        is_datetime=True,
    )

    STATUS_DATE = SchemaColumn(
        name="STATUS_DATE",
        parents=[StatusSchema.STATUS_START_DATE],
    )

    Y_LABEL = SchemaColumn(
        name="Y_LABEL",
    )


YLabelSchema = _YLabelSchema(
    parents=[StatusSchema],
)
