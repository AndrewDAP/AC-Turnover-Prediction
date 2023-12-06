# pylint: disable=duplicate-code
"""
Segmentation schema for clustering
"""

from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.schema.client_schema import ClientSchema
from src.data.schema.schema_column import SchemaColumn
from src.data.schema.schema import Schema


class _SegmentationSchema(Schema):
    """
    SegmentationSchema to generate employee clusters
    _RATIO: The proportion of feature X within the context of the specific employee
    _RATE: The variation of feature X compared to the mean of all employees
    """

    EMPLOYEE_ID = SchemaColumn(
        name="EMPLOYEE_ID",
        parents=[AugmentedVisitSchema.EMPLOYEE_ID],
    )

    EMPLOYEE_AGE = SchemaColumn(
        name="EMPLOYEE_AGE",
        parents=[AugmentedVisitSchema.EMPLOYEE_AGE],
    )

    EMPLOYEE_GENDER = SchemaColumn(
        name="EMPLOYEE_GENDER",
        parents=[AugmentedVisitSchema.EMPLOYEE_GENDER],
    )

    EMPLOYEE_JOB_TITLE = SchemaColumn(
        name="EMPLOYEE_JOB_TITLE",
        parents=[AugmentedVisitSchema.EMPLOYEE_JOB_TITLE],
    )

    EMPLOYEE_STATE = SchemaColumn(
        name="EMPLOYEE_STATE",
        parents=[AugmentedVisitSchema.EMPLOYEE_STATE],
    )

    EMPLOYEE_TENURE = SchemaColumn(
        name="EMPLOYEE_TENURE",
        parents=[AugmentedVisitSchema.EMPLOYEE_TENURE],
    )

    VISITS = SchemaColumn(name="VISITS", parents=[AugmentedVisitSchema.VISIT_ID])

    AVG_VISITS_PER_WEEK = SchemaColumn(
        name="AVG_VISITS_PER_WEEK",
    )

    TOTAL_VISIT_HOURS = SchemaColumn(
        name="TOTAL_VISIT_HOURS",
        parents=[AugmentedVisitSchema.VISIT_HOURS_APPROVED],
    )

    AVG_VISIT_DURATION = SchemaColumn(
        name="AVG_VISIT_DURATION",
    )

    AVG_VISIT_HOURS_PER_WEEK = SchemaColumn(
        name="AVG_VISIT_HOURS_PER_WEEK",
    )

    AVG_WORK_HOURS_DEVIATION = SchemaColumn(
        name="AVG_WORK_HOURS_DEVIATION",
        parents=[AugmentedVisitSchema.VISIT_WORK_HOURS_DEVIATION],
    )

    AVG_HOURLY_PAY = SchemaColumn(
        name="AVG_HOURLY_PAY", parents=[AugmentedVisitSchema.HOURLY_PAY]
    )

    ADL_COUNT = SchemaColumn(
        name="ADL_COUNT",
        parents=[
            AugmentedVisitSchema.VISIT_HAS_ADL,
        ],
    )

    COMPLETED_ADL = SchemaColumn(
        name="COMPLETED_ADL",
        parents=[
            AugmentedVisitSchema.VISIT_HAS_ADL_COMPLETE,
        ],
    )

    COMPLETED_ADL_RATIO = SchemaColumn(
        name="COMPLETED_ADL_RATIO",
    )

    AVG_DISTANCE_TO_PATIENT = SchemaColumn(
        name="AVG_DISTANCE_TO_PATIENT",
        parents=[AugmentedVisitSchema.EMPLOYEE_COMMUTE_DISTANCE],
    )

    AVG_CODED_DIAGNOSIS_PER_PATIENT = SchemaColumn(
        name="AVG_CODED_DIAGNOSIS_PER_PATIENT",
        parents=[AugmentedVisitSchema.CLIENT_CODED_DIAGNOSIS_COUNT],
    )

    LATE_ARRIVALS = SchemaColumn(
        name="LATE_ARRIVALS",
        parents=[AugmentedVisitSchema.WAS_LATE_TO_VISIT],
    )

    AVG_LATE_ARRIVALS_PER_WEEK = SchemaColumn(name="AVG_LATE_ARRIVALS_PER_WEEK")

    AVG_WAS_LATE_BY = SchemaColumn(
        name="AVG_WAS_LATE_BY",
        parents=[AugmentedVisitSchema.WAS_LATE_BY],
    )

    UNIQUE_CLIENTS = SchemaColumn(
        name="UNIQUE_CLIENTS", parents=[AugmentedVisitSchema.CLIENT_ID]
    )

    UNIQUE_CLIENTS_RATIO = SchemaColumn(name="UNIQUE_CLIENTS_RATIO")


SegmentationSchema = _SegmentationSchema(parents=[AugmentedVisitSchema, ClientSchema])
