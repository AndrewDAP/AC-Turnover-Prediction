"""
EmployeeHistorySchema after groupby
"""

from src.data.schema.feature_type import FeatureType
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.schema.client_schema import ClientSchema
from src.data.schema.schema_column import SchemaColumn
from src.data.schema.schema import Schema
from src.data.schema.y_label_schema import YLabelSchema


class _EmployeeHistorySchema(Schema):
    """
    EmployeeHistorySchema after groupby
    """

    EMPLOYEE_ID = SchemaColumn(
        name="EMPLOYEE_ID",
        parents=[AugmentedVisitSchema.EMPLOYEE_ID],
        feature_type=FeatureType.PRIMARY_KEY,
    )
    PERIOD_START = SchemaColumn(
        name="PERIOD_START",
        parents=[AugmentedVisitSchema.VISIT_START_AT],
        feature_type=FeatureType.PRIMARY_KEY,
        is_datetime=True,
    )
    EMPLOYEE_AGE = SchemaColumn(
        name="EMPLOYEE_AGE",
        parents=[AugmentedVisitSchema.EMPLOYEE_AGE],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    EMPLOYEE_GENDER = SchemaColumn(
        name="EMPLOYEE_GENDER",
        parents=[AugmentedVisitSchema.EMPLOYEE_GENDER],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    EMPLOYEE_STATE = SchemaColumn(
        name="EMPLOYEE_STATE",
        parents=[AugmentedVisitSchema.EMPLOYEE_STATE],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    EMPLOYEE_START_ON = SchemaColumn(
        name="EMPLOYEE_START_ON",
        parents=[AugmentedVisitSchema.EMPLOYEE_START_ON],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    EMPLOYEE_TERMINATION_DATE = SchemaColumn(
        name="EMPLOYEE_TERMINATION_DATE",
        parents=[AugmentedVisitSchema.EMPLOYEE_TERMINATION_DATE],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    EMPLOYEE_FIRST_VISIT = SchemaColumn(
        name="EMPLOYEE_FIRST_VISIT",
        parents=[AugmentedVisitSchema.EMPLOYEE_FIRST_VISIT],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    EMPLOYEE_JOB_TITLE = SchemaColumn(
        name="EMPLOYEE_JOB_TITLE",
        parents=[AugmentedVisitSchema.EMPLOYEE_JOB_TITLE],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    DAYS_TO_FIRST_VISIT = SchemaColumn(
        name="DAYS_TO_FIRST_VISIT",
        parents=[EMPLOYEE_FIRST_VISIT, PERIOD_START],
        feature_type=FeatureType.BEHAVIORAL,
    )
    VISIT_COUNT_PER_PERIOD = SchemaColumn(
        name="VISIT_COUNT_PER_PERIOD",
        parents=[AugmentedVisitSchema.VISIT_ID],
        feature_type=FeatureType.BEHAVIORAL,
    )
    VISIT_HOURS_PER_PERIOD = SchemaColumn(
        name="VISIT_HOURS_PER_PERIOD",
        parents=[AugmentedVisitSchema.VISIT_HOURS_APPROVED],
        feature_type=FeatureType.BEHAVIORAL,
    )
    DAY_HOURS_PER_PERIOD = SchemaColumn(
        name="DAY_HOURS_PER_PERIOD",
        parents=[AugmentedVisitSchema.DAY_HOURS],
        feature_type=FeatureType.BEHAVIORAL,
    )
    NIGHT_HOURS_PER_PERIOD = SchemaColumn(
        name="NIGHT_HOURS_PER_PERIOD",
        parents=[AugmentedVisitSchema.NIGHT_HOURS],
        feature_type=FeatureType.BEHAVIORAL,
    )
    WEEKDAY_HOURS_PER_PERIOD = SchemaColumn(
        name="WEEKDAY_HOURS_PER_PERIOD",
        parents=[AugmentedVisitSchema.WEEKDAY_HOURS],
        feature_type=FeatureType.BEHAVIORAL,
    )
    WEEKEND_HOURS_PER_PERIOD = SchemaColumn(
        name="WEEKEND_HOURS_PER_PERIOD",
        parents=[AugmentedVisitSchema.WEEKEND_HOURS],
        feature_type=FeatureType.BEHAVIORAL,
    )
    WORK_HOURS_DEVIATION_PER_PERIOD = SchemaColumn(
        name="WORK_HOURS_DEVIATION_PER_PERIOD",
        parents=[AugmentedVisitSchema.VISIT_WORK_HOURS_DEVIATION],
        feature_type=FeatureType.BEHAVIORAL,
    )
    AVERAGE_AGE_OF_PATIENTS_PER_PERIOD = SchemaColumn(
        name="AVERAGE_AGE_OF_PATIENTS_PER_PERIOD",
        parents=[AugmentedVisitSchema.CLIENT_AGE],
        feature_type=FeatureType.BEHAVIORAL,
    )
    AVERAGE_VISIT_DURATION_PER_PERIOD = SchemaColumn(
        name="AVERAGE_VISIT_DURATION_PER_PERIOD",
        parents=[AugmentedVisitSchema.VISIT_SCHEDULED_DURATION],
        feature_type=FeatureType.BEHAVIORAL,
    )
    AVERAGE_PATIENT_DIAGNOSIS_COUNT_PER_PERIOD = SchemaColumn(
        name="AVERAGE_PATIENT_DIAGNOSIS_COUNT_PER_PERIOD",
        parents=[ClientSchema.CLIENT_CODED_DIAGNOSIS_COUNT],
        feature_type=FeatureType.BEHAVIORAL,
    )
    AVERAGE_EMPLOYEE_COMMUTE_DISTANCE_PER_PERIOD = SchemaColumn(
        name="AVERAGE_EMPLOYEE_COMMUTE_DISTANCE_PER_PERIOD",
        parents=[AugmentedVisitSchema.EMPLOYEE_COMMUTE_DISTANCE],
        feature_type=FeatureType.BEHAVIORAL,
    )
    DISTINCT_PATIENT_COUNT_PER_PERIOD = SchemaColumn(
        name="DISTINCT_PATIENT_COUNT_PER_PERIOD",
        parents=[AugmentedVisitSchema.CLIENT_ID],
        feature_type=FeatureType.BEHAVIORAL,
    )
    EMPLOYEE_TENURE = SchemaColumn(
        name="EMPLOYEE_TENURE",
        parents=[AugmentedVisitSchema.EMPLOYEE_TENURE],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    DID_OVERTIME_IN_PERIOD = SchemaColumn(
        name="DID_OVERTIME_IN_PERIOD",
        parents=[WORK_HOURS_DEVIATION_PER_PERIOD],
        feature_type=FeatureType.BEHAVIORAL,
    )
    AVERAGE_HOURLY_PAY_PER_PERIOD = SchemaColumn(
        name="AVERAGE_HOURLY_PAY_PER_PERIOD",
        parents=[AugmentedVisitSchema.HOURLY_PAY],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    PAY_PER_PERIOD = SchemaColumn(
        name="PAY_PER_PERIOD",
        parents=[AugmentedVisitSchema.VISIT_TOTAL_PAY],
        feature_type=FeatureType.DEMOGRAPHIC,
    )
    ADL_COMPLETION_RATE_PER_PERIOD = SchemaColumn(
        name="ADL_COMPLETION_RATE_PER_PERIOD",
        parents=[
            AugmentedVisitSchema.VISIT_HAS_ADL_COMPLETE,
            AugmentedVisitSchema.VISIT_HAS_ADL,
        ],
        feature_type=FeatureType.BEHAVIORAL,
    )
    AVERAGE_LATE_BY_IN_PERIOD = SchemaColumn(
        name="AVERAGE_LATE_BY_IN_PERIOD",
        parents=[
            AugmentedVisitSchema.WAS_LATE_BY,
        ],
        feature_type=FeatureType.BEHAVIORAL,
    )
    TIMESNET_INFERENCE = SchemaColumn(
        name="TIMESNET_INFERENCE",
    )

    # Training-Related Variables
    TRAINING_WINDOW_ID = SchemaColumn(
        name="TRAINING_WINDOW_ID",
        feature_type=FeatureType.TRAINING_RELATED,
    )
    Y_LABEL = SchemaColumn(
        name="Y_LABEL",
        parents=[YLabelSchema.Y_LABEL],
        feature_type=FeatureType.TRAINING_RELATED,
    )


EmployeeHistorySchema = _EmployeeHistorySchema(
    parents=[
        AugmentedVisitSchema,
        ClientSchema,
        YLabelSchema,
    ]
)
