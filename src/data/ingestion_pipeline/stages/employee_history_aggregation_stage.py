"""
This module contains the EmployeeHistoryStage class which is responsible for
"""

from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.data.transforms.aggregate.aggregate_by import (
    AggregateBy,
)
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)


# pylint: disable=unused-argument
def build_employee_history_aggregation_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the employee history stage of the ingestion pipeline.
    """

    return IngestionPipelineStage(
        name=IngestionPipelineStages.EMPLOYEE_HISTORY_AGGREGATION_STAGE,
        from_schema=AugmentedVisitSchema,
        to_schema=EmployeeHistorySchema,
        config=conf,
        required_stages_names=[
            IngestionPipelineStages.AUGMENT_VISIT_STAGE,
        ],
        transforms=[
            AggregateBy(
                [
                    AugmentedVisitSchema.EMPLOYEE_ID.name,
                    AugmentedVisitSchema.PERIOD_START.name,
                ],
                aggregation_functions={
                    AugmentedVisitSchema.EMPLOYEE_AGE: "mean",
                    AugmentedVisitSchema.EMPLOYEE_GENDER: "max",
                    AugmentedVisitSchema.EMPLOYEE_STATE: "max",
                    AugmentedVisitSchema.EMPLOYEE_TENURE: "max",
                    AugmentedVisitSchema.EMPLOYEE_START_ON: "max",
                    AugmentedVisitSchema.EMPLOYEE_FIRST_VISIT: "max",
                    AugmentedVisitSchema.EMPLOYEE_TERMINATION_DATE: "max",
                    AugmentedVisitSchema.EMPLOYEE_JOB_TITLE: "median",
                    AugmentedVisitSchema.VISIT_ID: "count",
                    AugmentedVisitSchema.EMPLOYEE_COMMUTE_DISTANCE: "mean",
                    AugmentedVisitSchema.VISIT_HOURS_APPROVED: "sum",
                    AugmentedVisitSchema.DAY_HOURS: "sum",
                    AugmentedVisitSchema.NIGHT_HOURS: "sum",
                    AugmentedVisitSchema.WEEKDAY_HOURS: "sum",
                    AugmentedVisitSchema.WEEKEND_HOURS: "sum",
                    AugmentedVisitSchema.VISIT_WORK_HOURS_DEVIATION: "sum",
                    AugmentedVisitSchema.CLIENT_AGE: "mean",
                    AugmentedVisitSchema.VISIT_SCHEDULED_DURATION: "mean",
                    AugmentedVisitSchema.CLIENT_CODED_DIAGNOSIS_COUNT: "sum",
                    AugmentedVisitSchema.CLIENT_ID: "nunique",
                    AugmentedVisitSchema.HOURLY_PAY: "mean",
                    AugmentedVisitSchema.VISIT_TOTAL_PAY: "sum",
                    AugmentedVisitSchema.VISIT_HAS_ADL_COMPLETE: "sum",
                    AugmentedVisitSchema.VISIT_HAS_ADL: "sum",
                    AugmentedVisitSchema.WAS_LATE_BY: "mean",
                },
            ),
        ],
    )
