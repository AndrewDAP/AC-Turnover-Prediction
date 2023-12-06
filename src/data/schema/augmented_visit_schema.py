"""
Augmented visit schema. after joining
"""
from src.data.schema.schema import Schema
from src.data.schema.schema_column import SchemaColumn
from src.data.schema.client_schema import ClientSchema
from src.data.schema.clock_schema import ClockSchema
from src.data.schema.visit_schema import VisitSchema
from src.data.schema.employee_schema import EmployeeSchema


class _AugmentedVisitSchema(Schema):
    """
    Augmented visit schema. after joining
    """

    VISIT_ID = SchemaColumn(
        name="VISIT_ID",
        parents=[VisitSchema.VISIT_ID],
    )

    EMPLOYEE_ID = SchemaColumn(
        name="EMPLOYEE_ID",
        parents=[VisitSchema.EMPLOYEE_ID],
    )

    CLIENT_ID = SchemaColumn(
        name="CLIENT_ID",
        parents=[VisitSchema.CLIENT_ID],
    )

    VISIT_CANCEL_CODE = SchemaColumn(
        name="VISIT_CANCEL_CODE",
        parents=[VisitSchema.VISIT_CANCEL_CODE],
    )

    VISIT_START_AT = SchemaColumn(
        name="VISIT_START_AT",
        parents=[VisitSchema.VISIT_START_AT],
        is_datetime=True,
    )

    VISIT_END_AT = SchemaColumn(
        name="VISIT_END_AT",
        parents=[VisitSchema.VISIT_END_AT],
        is_datetime=True,
    )

    VISIT_START_AT_UTC = SchemaColumn(
        name="VISIT_START_AT_UTC",
        parents=[VisitSchema.VISIT_START_AT_UTC],
        is_datetime=True,
    )

    VISIT_END_AT_UTC = SchemaColumn(
        name="VISIT_END_AT_UTC",
        parents=[VisitSchema.VISIT_END_AT_UTC],
        is_datetime=True,
    )

    VISIT_SERVICE_DESCRIPTION = SchemaColumn(
        name="VISIT_SERVICE_DESCRIPTION",
        parents=[VisitSchema.VISIT_SERVICE_DESCRIPTION],
    )

    VISIT_IS_PAID = SchemaColumn(
        name="VISIT_IS_PAID",
        parents=[VisitSchema.VISIT_IS_PAID],
    )

    VISIT_IN_OUT_OF_RECURRENCE_STATUS = SchemaColumn(
        name="VISIT_IN_OUT_OF_RECURRENCE_STATUS",
        parents=[VisitSchema.VISIT_IN_OUT_OF_RECURRENCE_STATUS],
    )

    VISIT_RECURRENCE = SchemaColumn(
        name="VISIT_RECURRENCE",
        parents=[VisitSchema.VISIT_RECURRENCE],
    )

    VISIT_APPROVAL_STATUS = SchemaColumn(
        name="VISIT_APPROVAL_STATUS",
        parents=[VisitSchema.VISIT_APPROVAL_STATUS],
    )

    VISIT_COMPLETED = SchemaColumn(
        name="VISIT_COMPLETED",
        parents=[VisitSchema.VISIT_COMPLETED],
    )

    VISIT_COMPUTED_RATE = SchemaColumn(
        name="VISIT_COMPUTED_RATE",
        parents=[VisitSchema.VISIT_COMPUTED_RATE],
    )

    VISIT_COMPUTED_RATE_UNITS = SchemaColumn(
        name="VISIT_COMPUTED_RATE_UNITS",
        parents=[VisitSchema.VISIT_COMPUTED_RATE_UNITS],
    )

    VISIT_SCHEDULED_DURATION = SchemaColumn(
        name="VISIT_SCHEDULED_DURATION",
        parents=[VisitSchema.VISIT_SCHEDULED_DURATION],
    )

    VISIT_UNIT_QTY = SchemaColumn(
        name="VISIT_UNIT_QTY",
        parents=[VisitSchema.VISIT_UNIT_QTY],
    )

    VISIT_HOURS_APPROVED = SchemaColumn(
        name="VISIT_HOURS_APPROVED",
        parents=[VisitSchema.VISIT_HOURS_APPROVED],
    )

    VISIT_ON_HOLD_REASON = SchemaColumn(
        name="VISIT_ON_HOLD_REASON",
        parents=[VisitSchema.VISIT_ON_HOLD_REASON],
    )

    VISIT_TOTAL_PAY = SchemaColumn(
        name="VISIT_TOTAL_PAY",
        parents=[VisitSchema.VISIT_TOTAL_PAY],
    )

    VISIT_WORK_HOURS_DEVIATION = SchemaColumn(
        name="VISIT_WORK_HOURS_DEVIATION",
        parents=[VisitSchema.VISIT_WORK_HOURS_DEVIATION],
    )

    VISIT_HAS_ADL_COMPLETE = SchemaColumn(
        name="VISIT_HAS_ADL_COMPLETE",
        parents=[VisitSchema.VISIT_HAS_ADL_COMPLETED],
    )

    VISIT_HAS_ADL = SchemaColumn(
        name="VISIT_HAS_ADL", parents=[VisitSchema.VISIT_HAS_ADL]
    )

    EMPLOYEE_AGE = SchemaColumn(
        name="EMPLOYEE_AGE",
        parents=[EmployeeSchema.EMPLOYEE_AGE],
    )

    EMPLOYEE_GENDER = SchemaColumn(
        name="EMPLOYEE_GENDER",
        parents=[EmployeeSchema.EMPLOYEE_GENDER],
    )

    EMPLOYEE_JOB_TITLE = SchemaColumn(
        name="EMPLOYEE_JOB_TITLE",
        parents=[EmployeeSchema.EMPLOYEE_JOB_TITLE],
    )

    EMPLOYEE_LATITUDE = SchemaColumn(
        name="EMPLOYEE_LATITUDE",
        parents=[EmployeeSchema.EMPLOYEE_LATITUDE],
    )

    EMPLOYEE_LONGITUDE = SchemaColumn(
        name="EMPLOYEE_LONGITUDE",
        parents=[EmployeeSchema.EMPLOYEE_LONGITUDE],
    )

    EMPLOYEE_START_ON = SchemaColumn(
        name="EMPLOYEE_START_ON",
        parents=[EmployeeSchema.EMPLOYEE_START_ON],
        is_datetime=True,
    )

    EMPLOYEE_STATE = SchemaColumn(
        name="EMPLOYEE_STATE",
        parents=[EmployeeSchema.EMPLOYEE_STATE],
    )

    EMPLOYEE_STATUS = SchemaColumn(
        name="EMPLOYEE_STATUS",
        parents=[EmployeeSchema.EMPLOYEE_STATUS],
    )

    EMPLOYEE_TERMINATION_DATE = SchemaColumn(
        name="EMPLOYEE_TERMINATION_DATE",
        parents=[EmployeeSchema.EMPLOYEE_TERMINATION_DATE],
        is_datetime=True,
    )

    EMPLOYEE_TENURE = SchemaColumn(
        name="EMPLOYEE_TENURE",
        parents=[EmployeeSchema.EMPLOYEE_TENURE],
    )

    EMPLOYEE_COMMUTE_DISTANCE = SchemaColumn(
        name="EMPLOYEE_COMMUTE_DISTANCE",
        parents=[
            EmployeeSchema.EMPLOYEE_LATITUDE,
            EmployeeSchema.EMPLOYEE_LONGITUDE,
            ClientSchema.CLIENT_LATITUDE,
            ClientSchema.CLIENT_LONGITUDE,
        ],
    )

    EMPLOYEE_FIRST_VISIT = SchemaColumn(
        name="EMPLOYEE_FIRST_VISIT",
    )

    CLIENT_AGE = SchemaColumn(
        name="CLIENT_AGE",
        parents=[ClientSchema.CLIENT_AGE],
    )

    CLIENT_ADMISSION_DATE = SchemaColumn(
        name="CLIENT_ADMISSION_DATE",
        parents=[ClientSchema.CLIENT_ADMISSION_DATE],
        is_datetime=True,
    )

    CLIENT_GENDER = SchemaColumn(
        name="CLIENT_GENDER",
        parents=[ClientSchema.CLIENT_GENDER],
    )

    CLIENT_LATITUDE = SchemaColumn(
        name="CLIENT_LATITUDE",
        parents=[ClientSchema.CLIENT_LATITUDE],
    )

    CLIENT_LONGITUDE = SchemaColumn(
        name="CLIENT_LONGITUDE",
        parents=[ClientSchema.CLIENT_LONGITUDE],
    )

    CLIENT_DIAGNOSIS = SchemaColumn(
        name="CLIENT_DIAGNOSIS",
        parents=[ClientSchema.CLIENT_DIAGNOSIS],
    )

    CLIENT_CODED_DIAGNOSIS_COUNT = SchemaColumn(
        name="CLIENT_CODED_DIAGNOSIS_COUNT",
        parents=[ClientSchema.CLIENT_CODED_DIAGNOSIS_COUNT],
    )

    NIGHT_HOURS = SchemaColumn(
        name="NIGHT_HOURS",
        parents=[ClockSchema.NIGHT_HOURS],
    )

    DAY_HOURS = SchemaColumn(
        name="DAY_HOURS",
        parents=[ClockSchema.DAY_HOURS],
    )

    WEEKEND_HOURS = SchemaColumn(
        name="WEEKEND_HOURS",
        parents=[ClockSchema.WEEKEND_HOURS],
    )

    WEEKDAY_HOURS = SchemaColumn(
        name="WEEKDAY_HOURS",
        parents=[ClockSchema.WEEKDAY_HOURS],
    )

    START_TIME = SchemaColumn(
        name="START_TIME",
        parents=[ClockSchema.START_TIME],
        is_datetime=True,
    )

    WAS_LATE_TO_VISIT = SchemaColumn(
        name="WAS_LATE_TO_VISIT",
        parents=[VisitSchema.VISIT_START_AT, ClockSchema.START_TIME],
    )

    PERIOD_START = SchemaColumn(
        name="PERIOD_START",
        is_datetime=True,
    )

    HOURLY_PAY = SchemaColumn(name="HOURLY_PAY", parents=[VisitSchema.VISIT_HOURLY_PAY])

    WAS_LATE_BY = SchemaColumn(name="WAS_LATE_BY")


AugmentedVisitSchema = _AugmentedVisitSchema(
    parents=[
        VisitSchema,
        EmployeeSchema,
        ClientSchema,
        ClockSchema,
    ]
)
