"""
Employee data schema.
"""

from src.data.schema.schema import Schema
from src.data.schema.schema_column import SchemaColumn


class _EmployeeSchemaRaw(Schema):
    """
    Employee schema.
    """

    EMPLOYEE_ID = SchemaColumn(name="EMPLOYEE_ID")
    STATUS = SchemaColumn(name="STATUS")
    HAS_SKILLS = SchemaColumn(name="HAS_SKILLS")
    COUNTRY = SchemaColumn(name="COUNTRY")
    GENDER = SchemaColumn(name="GENDER")
    JOB_TITLE = SchemaColumn(name="JOB_TITLE")
    START_ON = SchemaColumn(name="START_ON")
    STATE = SchemaColumn(name="STATE")
    TERMINATION_DATE = SchemaColumn(name="TERMINATION_DATE")
    USER_SETTINGS_STAFFING_EMPLOYEE_POSITION_TYPE = SchemaColumn(
        name="USER_SETTINGS:STAFFING_EMPLOYEE_POSITION_TYPE",
    )
    EMPLOYEE_AVAILABILITY = SchemaColumn(name="EMPLOYEE_AVAILABILITY")
    EMPLOYEE_MINIMUM_DAILY_CAPACITY = SchemaColumn(
        name="EMPLOYEE_MINIMUM_DAILY_CAPACITY"
    )
    EMPLOYEE_MAXIMUM_DAILY_CAPACITY = SchemaColumn(
        name="EMPLOYEE_MAXIMUM_DAILY_CAPACITY"
    )
    EMPLOYEE_MINIMUM_WEEKLY_CAPACITY = SchemaColumn(
        name="EMPLOYEE_MINIMUM_WEEKLY_CAPACITY"
    )
    EMPLOYEE_MAXIMUM_WEEKLY_CAPACITY = SchemaColumn(
        name="EMPLOYEE_MAXIMUM_WEEKLY_CAPACITY"
    )
    LANGUAGE = SchemaColumn(name="LANGUAGE")
    AGE = SchemaColumn(name="age")
    LATITUDE = SchemaColumn(name="latitute")
    LONGITUDE = SchemaColumn(name="longitude")


EmployeeSchemaRaw = _EmployeeSchemaRaw()


class _EmployeeSchema(Schema):
    EMPLOYEE_ID = SchemaColumn(
        name="EMPLOYEE_ID",
        parents=[EmployeeSchemaRaw.EMPLOYEE_ID],
    )

    EMPLOYEE_STATUS = SchemaColumn(
        name="EMPLOYEE_STATUS",
        parents=[EmployeeSchemaRaw.STATUS],
    )

    EMPLOYEE_HAS_SKILLS = SchemaColumn(
        name="EMPLOYEE_HAS_SKILLS",
        parents=[EmployeeSchemaRaw.HAS_SKILLS],
    )

    EMPLOYEE_COUNTRY = SchemaColumn(
        name="EMPLOYEE_COUNTRY",
        parents=[EmployeeSchemaRaw.COUNTRY],
    )

    EMPLOYEE_GENDER = SchemaColumn(
        name="EMPLOYEE_GENDER",
        parents=[EmployeeSchemaRaw.GENDER],
    )

    EMPLOYEE_JOB_TITLE = SchemaColumn(
        name="EMPLOYEE_JOB_TITLE",
        parents=[EmployeeSchemaRaw.JOB_TITLE],
    )

    EMPLOYEE_START_ON = SchemaColumn(
        name="EMPLOYEE_START_ON",
        parents=[EmployeeSchemaRaw.START_ON],
        is_datetime=True,
    )

    EMPLOYEE_STATE = SchemaColumn(
        name="EMPLOYEE_STATE",
        parents=[EmployeeSchemaRaw.STATE],
    )

    EMPLOYEE_TERMINATION_DATE = SchemaColumn(
        name="EMPLOYEE_TERMINATION_DATE",
        parents=[EmployeeSchemaRaw.TERMINATION_DATE],
        is_datetime=True,
    )

    EMPLOYEE_AVAILABILITY = SchemaColumn(
        name="EMPLOYEE_AVAILABILITY",
        parents=[EmployeeSchemaRaw.EMPLOYEE_AVAILABILITY],
    )

    EMPLOYEE_LANGUAGE = SchemaColumn(
        name="EMPLOYEE_LANGUAGE",
        parents=[EmployeeSchemaRaw.LANGUAGE],
    )

    EMPLOYEE_AGE = SchemaColumn(
        name="EMPLOYEE_AGE",
        parents=[EmployeeSchemaRaw.AGE],
    )

    EMPLOYEE_LATITUDE = SchemaColumn(
        name="EMPLOYEE_LATITUDE",
        parents=[EmployeeSchemaRaw.LATITUDE],
    )

    EMPLOYEE_LONGITUDE = SchemaColumn(
        name="EMPLOYEE_LONGITUDE",
        parents=[EmployeeSchemaRaw.LONGITUDE],
    )

    EMPLOYEE_MINIMUM_DAILY_CAPACITY = SchemaColumn(
        name="EMPLOYEE_MINIMUM_DAILY_CAPACITY",
        parents=[EmployeeSchemaRaw.EMPLOYEE_MINIMUM_DAILY_CAPACITY],
    )

    EMPLOYEE_MAXIMUM_DAILY_CAPACITY = SchemaColumn(
        name="EMPLOYEE_MAXIMUM_DAILY_CAPACITY",
        parents=[EmployeeSchemaRaw.EMPLOYEE_MAXIMUM_DAILY_CAPACITY],
    )

    EMPLOYEE_MINIMUM_WEEKLY_CAPACITY = SchemaColumn(
        name="EMPLOYEE_MINIMUM_WEEKLY_CAPACITY",
        parents=[EmployeeSchemaRaw.EMPLOYEE_MINIMUM_WEEKLY_CAPACITY],
    )

    EMPLOYEE_MAXIMUM_WEEKLY_CAPACITY = SchemaColumn(
        name="EMPLOYEE_MAXIMUM_WEEKLY_CAPACITY",
        parents=[EmployeeSchemaRaw.EMPLOYEE_MAXIMUM_WEEKLY_CAPACITY],
    )

    EMPLOYEE_TENURE = SchemaColumn(
        name="EMPLOYEE_TENURE",
        parents=[EmployeeSchemaRaw.START_ON, EmployeeSchemaRaw.TERMINATION_DATE],
    )

    USER_SETTINGS_STAFFING_EMPLOYEE_POSITION_TYPE = SchemaColumn(
        name="USER_SETTINGS:STAFFING_EMPLOYEE_POSITION_TYPE",
        parents=[EmployeeSchemaRaw.USER_SETTINGS_STAFFING_EMPLOYEE_POSITION_TYPE],
    )


EmployeeSchema = _EmployeeSchema(
    parents=[EmployeeSchemaRaw],
)
