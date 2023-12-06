"""
Visit data schema.
"""

from src.data.schema.schema import Schema
from src.data.schema.schema_column import SchemaColumn


class _VisitSchemaRaw(Schema):
    """
    Visit schema.
    """

    VISIT_ID = SchemaColumn(name="VISIT_ID")
    SERVICE_DESCRIPTION = SchemaColumn(name="SERVICE_DESCRIPTION")
    CLIENT_ID = SchemaColumn(name="CLIENT_ID")
    EMPLOYEE_ID = SchemaColumn(name="EMPLOYEE_ID")
    CREATED_AT = SchemaColumn(name="CREATED_AT")
    UPDATED_AT = SchemaColumn(name="UPDATED_AT")
    START_AT = SchemaColumn(name="START_AT")
    END_AT = SchemaColumn(name="END_AT")
    START_AT_UTC = SchemaColumn(name="START_AT_UTC")
    END_AT_UTC = SchemaColumn(name="END_AT_UTC")
    HOLIDAY_DATE = SchemaColumn(name="HOLIDAY_DATE")
    VISIT_COMPLETED = SchemaColumn(name="VISIT_COMPLETED")
    IN_OUT_OF_RECURRENCE_STATUS = SchemaColumn(name="IN_OUT_OF_RECURRENCE_STATUS")
    VISIT_RECURRENCE = SchemaColumn(name="VISIT_RECURRENCE")
    IS_PAID = SchemaColumn(name="IS_PAID")
    ADL_COMPLETE = SchemaColumn(name="ADL_COMPLETE")
    HAS_ADL = SchemaColumn(name="HAS_ADL")
    BREAK_MINUTES = SchemaColumn(name="BREAK_MINUTES")
    BREAK_HOURS = SchemaColumn(name="BREAK_HOURS")
    VISIT_APPROVAL_STATUS = SchemaColumn(name="VISIT_APPROVAL_STATUS")
    VISIT_UNIT_QTY = SchemaColumn(name="VISIT_UNIT_QTY")
    VISIT_ON_HOLD_REASON = SchemaColumn(name="VISIT_ON_HOLD_REASON")
    VISIT_COMPUTED_RATE_UNITS = SchemaColumn(name="VISIT_COMPUTED_RATE_UNITS")
    VISIT_COMPUTED_RATE = SchemaColumn(name="VISIT_COMPUTED_RATE")
    CANCEL_CODE = SchemaColumn(name="CANCEL_CODE")
    VISIT_HOURS_APPROVED = SchemaColumn(name="VISIT_HOURS_APPROVED")
    VISIT_SCHEDULED_DURATION = SchemaColumn(name="VISIT_SCHEDULED_DURATION")


VisitSchemaRaw = _VisitSchemaRaw()


class _VisitSchema(Schema):
    """
    Visit schema. after cleaning
    """

    VISIT_ID = SchemaColumn(
        name="VISIT_ID",
        parents=[VisitSchemaRaw.VISIT_ID],
    )

    VISIT_SERVICE_DESCRIPTION = SchemaColumn(
        name="VISIT_SERVICE_DESCRIPTION",
        parents=[VisitSchemaRaw.SERVICE_DESCRIPTION],
    )

    CLIENT_ID = SchemaColumn(
        name="CLIENT_ID",
        parents=[VisitSchemaRaw.CLIENT_ID],
    )

    EMPLOYEE_ID = SchemaColumn(
        name="EMPLOYEE_ID",
        parents=[VisitSchemaRaw.EMPLOYEE_ID],
    )

    VISIT_CREATED_AT = SchemaColumn(
        name="VISIT_CREATED_AT",
        parents=[VisitSchemaRaw.CREATED_AT],
        is_datetime=True,
    )

    VISIT_UPDATED_AT = SchemaColumn(
        name="VISIT_UPDATED_AT",
        parents=[VisitSchemaRaw.UPDATED_AT],
        is_datetime=True,
    )

    VISIT_START_AT = SchemaColumn(
        name="VISIT_START_AT",
        parents=[VisitSchemaRaw.START_AT],
        is_datetime=True,
    )

    VISIT_END_AT = SchemaColumn(
        name="VISIT_END_AT",
        parents=[VisitSchemaRaw.END_AT],
        is_datetime=True,
    )

    VISIT_START_AT_UTC = SchemaColumn(
        name="VISIT_START_AT_UTC",
        parents=[VisitSchemaRaw.START_AT_UTC],
        is_datetime=True,
    )

    VISIT_END_AT_UTC = SchemaColumn(
        name="VISIT_END_AT_UTC",
        parents=[VisitSchemaRaw.END_AT_UTC],
        is_datetime=True,
    )

    VISIT_HOLIDAY_DATE = SchemaColumn(
        name="VISIT_HOLIDAY_DATE",
        parents=[VisitSchemaRaw.HOLIDAY_DATE],
        is_datetime=True,
    )

    VISIT_COMPLETED = SchemaColumn(
        name="VISIT_COMPLETED",
        parents=[VisitSchemaRaw.VISIT_COMPLETED],
    )

    VISIT_IN_OUT_OF_RECURRENCE_STATUS = SchemaColumn(
        name="VISIT_IN_OUT_OF_RECURRENCE_STATUS",
        parents=[VisitSchemaRaw.IN_OUT_OF_RECURRENCE_STATUS],
    )

    VISIT_RECURRENCE = SchemaColumn(
        name="VISIT_RECURRENCE",
        parents=[VisitSchemaRaw.VISIT_RECURRENCE],
    )

    VISIT_IS_PAID = SchemaColumn(
        name="VISIT_IS_PAID",
        parents=[VisitSchemaRaw.IS_PAID],
    )

    VISIT_ADL_COMPLETE = SchemaColumn(
        name="VISIT_ADL_COMPLETE",
        parents=[VisitSchemaRaw.ADL_COMPLETE],
    )

    VISIT_HAS_ADL = SchemaColumn(
        name="VISIT_HAS_ADL",
        parents=[VisitSchemaRaw.HAS_ADL],
    )

    VISIT_BREAK_MINUTES = SchemaColumn(
        name="VISIT_BREAK_MINUTES",
        parents=[VisitSchemaRaw.BREAK_MINUTES],
    )

    VISIT_BREAK_HOURS = SchemaColumn(
        name="VISIT_BREAK_HOURS",
        parents=[VisitSchemaRaw.BREAK_HOURS],
    )

    VISIT_APPROVAL_STATUS = SchemaColumn(
        name="VISIT_APPROVAL_STATUS",
        parents=[VisitSchemaRaw.VISIT_APPROVAL_STATUS],
    )

    VISIT_UNIT_QTY = SchemaColumn(
        name="VISIT_UNIT_QTY",
        parents=[VisitSchemaRaw.VISIT_UNIT_QTY],
    )

    VISIT_ON_HOLD_REASON = SchemaColumn(
        name="VISIT_ON_HOLD_REASON",
        parents=[VisitSchemaRaw.VISIT_ON_HOLD_REASON],
    )

    VISIT_COMPUTED_RATE_UNITS = SchemaColumn(
        name="VISIT_COMPUTED_RATE_UNITS",
        parents=[VisitSchemaRaw.VISIT_COMPUTED_RATE_UNITS],
    )

    VISIT_COMPUTED_RATE = SchemaColumn(
        name="VISIT_COMPUTED_RATE",
        parents=[VisitSchemaRaw.VISIT_COMPUTED_RATE],
    )

    VISIT_CANCEL_CODE = SchemaColumn(
        name="VISIT_CANCEL_CODE",
        parents=[VisitSchemaRaw.CANCEL_CODE],
    )

    VISIT_HOURS_APPROVED = SchemaColumn(
        name="VISIT_HOURS_APPROVED",
        parents=[VisitSchemaRaw.VISIT_HOURS_APPROVED],
    )

    VISIT_SCHEDULED_DURATION = SchemaColumn(
        name="VISIT_SCHEDULED_DURATION",
        parents=[VisitSchemaRaw.VISIT_SCHEDULED_DURATION],
    )

    VISIT_WORK_HOURS_DEVIATION = SchemaColumn(
        name="VISIT_WORK_HOURS_DEVIATION",
        parents=[VISIT_HOURS_APPROVED, VISIT_SCHEDULED_DURATION],
        comments="VISIT_HOURS_APPROVED - VISIT_SCHEDULED_DURATION",
    )

    VISIT_TOTAL_PAY = SchemaColumn(
        name="VISIT_TOTAL_PAY",
        parents=[VISIT_COMPUTED_RATE, VISIT_UNIT_QTY, VISIT_COMPUTED_RATE_UNITS],
        comments="VISIT_COMPUTED_RATE * VISIT_UNIT_QTY",
    )

    VISIT_HOURLY_PAY = SchemaColumn(
        name="VISIT_HOURLY_PAY",
        parents=[VISIT_TOTAL_PAY, VISIT_HOURS_APPROVED],
    )

    VISIT_HAS_ADL_COMPLETED = SchemaColumn(
        name="VISIT_HAS_ADL_COMPLETED",
        parents=[VISIT_HAS_ADL, VISIT_ADL_COMPLETE],
        comments="VISIT_HAS_ADL * VISIT_ADL_COMPLETE",
    )

    VISIT_HAS_ADL = SchemaColumn(name="VISIT_HAS_ADL", parents=[VisitSchemaRaw.HAS_ADL])


VisitSchema = _VisitSchema(
    parents=[VisitSchemaRaw],
)
