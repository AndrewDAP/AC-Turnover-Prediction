"""
This module contains the EmployeeHistoryStage class which is responsible for
"""
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)
from src.data.transforms.clean.fill_na_transform import FillNaTransform, FillNaColumn
from src.data.transforms.clean.drop_after_fill_na import DropAfterFillNa


# pylint: disable=unused-argument
def build_employee_history_fill_na_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the employee history stage of the ingestion pipeline.
    """

    return IngestionPipelineStage(
        name=IngestionPipelineStages.EMPLOYEE_HISTORY_FILL_NA_STAGE,
        from_schema=AugmentedVisitSchema,
        to_schema=EmployeeHistorySchema,
        config=conf,
        required_stages_names=[
            IngestionPipelineStages.EMPLOYEE_HISTORY_ROLLING_FEATURES_STAGE,
        ],
        transforms=[
            FillNaTransform(
                # Fill according to specific employee's data
                columns=[
                    FillNaColumn(
                        column=EmployeeHistorySchema.VISIT_HOURS_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.DAY_HOURS_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.NIGHT_HOURS_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.WEEKDAY_HOURS_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.WEEKEND_HOURS_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.WORK_HOURS_DEVIATION_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.AVERAGE_AGE_OF_PATIENTS_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.AVERAGE_VISIT_DURATION_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.AVERAGE_EMPLOYEE_COMMUTE_DISTANCE_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.DISTINCT_PATIENT_COUNT_PER_PERIOD,
                        method="mode",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.AVERAGE_HOURLY_PAY_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.ADL_COMPLETION_RATE_PER_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.AVERAGE_LATE_BY_IN_PERIOD,
                        method="mean",
                        fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
                    ),
                ],
            ),
            FillNaTransform(
                # Fill according to all employees data
                columns=[
                    FillNaColumn(
                        column=EmployeeHistorySchema.PERIOD_START,
                        fill_policy="drop",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.EMPLOYEE_AGE,
                        fill_policy="drop",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.EMPLOYEE_GENDER,
                        fill_policy="fill_with_default",
                        fill_default_value="U",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.EMPLOYEE_STATE,
                        fill_policy="fill_with_default",
                        fill_default_value="Unknown",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.VISIT_COUNT_PER_PERIOD,
                        fill_policy="drop",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.VISIT_HOURS_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.DAY_HOURS_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.NIGHT_HOURS_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.WEEKDAY_HOURS_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.WEEKEND_HOURS_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.WORK_HOURS_DEVIATION_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.AVERAGE_AGE_OF_PATIENTS_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.AVERAGE_VISIT_DURATION_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.EMPLOYEE_TENURE,
                        method="median",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.DISTINCT_PATIENT_COUNT_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.AVERAGE_EMPLOYEE_COMMUTE_DISTANCE_PER_PERIOD,
                        method="mode",
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.DID_OVERTIME_IN_PERIOD,
                        fill_policy="fill_with_default",
                        fill_default_value=0,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.AVERAGE_HOURLY_PAY_PER_PERIOD,
                        fill_policy="fill_with_default",
                        fill_default_value=0,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.PAY_PER_PERIOD,
                        fill_policy="fill_with_default",
                        fill_default_value=0,
                    ),
                    FillNaColumn(
                        column=EmployeeHistorySchema.EMPLOYEE_JOB_TITLE, method="mode"
                    ),
                ],
            ),
            DropAfterFillNa(),
        ],
    )
