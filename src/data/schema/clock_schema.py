"""
Clock data schema.
"""

from src.data.schema.schema import Schema
from src.data.schema.schema_column import SchemaColumn


class _ClockSchemaRaw(Schema):
    """
    Clock schema. before cleaning
    """

    VISIT_ID = SchemaColumn(name="VISIT_ID")
    PUNCH_ID = SchemaColumn(name="PUNCH_ID")
    START_TIME = SchemaColumn(name="START_TIME")
    END_TIME = SchemaColumn(name="END_TIME")


ClockSchemaRaw = _ClockSchemaRaw()


class _ClockSchema(Schema):
    """
    Clock schema. after cleaning
    """

    VISIT_ID = SchemaColumn(
        name="VISIT_ID",
        parents=[ClockSchemaRaw.VISIT_ID],
    )

    PUNCH = SchemaColumn(
        name="PUNCH",
        parents=[ClockSchemaRaw.PUNCH_ID],
    )

    START_TIME = SchemaColumn(
        name="START_TIME",
        parents=[ClockSchemaRaw.START_TIME],
        is_datetime=True,
    )

    END_TIME = SchemaColumn(
        name="END_TIME",
        parents=[ClockSchemaRaw.END_TIME],
        is_datetime=True,
    )

    DAY_HOURS = SchemaColumn(
        name="DAY_HOURS",
        parents=[ClockSchemaRaw.START_TIME, ClockSchemaRaw.END_TIME],
    )

    NIGHT_HOURS = SchemaColumn(
        name="NIGHT_HOURS",
        parents=[ClockSchemaRaw.START_TIME, ClockSchemaRaw.END_TIME],
    )

    WEEKDAY_HOURS = SchemaColumn(
        name="WEEKDAY_HOURS",
        parents=[ClockSchemaRaw.START_TIME, ClockSchemaRaw.END_TIME],
    )

    WEEKEND_HOURS = SchemaColumn(
        name="WEEKEND_HOURS",
        parents=[ClockSchemaRaw.START_TIME, ClockSchemaRaw.END_TIME],
    )


ClockSchema = _ClockSchema(
    parents=[ClockSchemaRaw],
)
