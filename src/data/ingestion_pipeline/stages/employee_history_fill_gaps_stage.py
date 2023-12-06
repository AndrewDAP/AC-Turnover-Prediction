"""
This module contains the EmployeeHistoryStage class which is responsible for
"""

from src.data.transforms.clean.fill_gaps import FillGaps
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.transforms.clean.rename_columns import RenameColumns
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.data.transforms.clean.set_value_range import SetValueRange
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)


# pylint: disable=unused-argument
def build_employee_history_fill_gaps_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the employee history stage of the ingestion pipeline.
    """

    return IngestionPipelineStage(
        name=IngestionPipelineStages.EMPLOYEE_HISTORY_FILL_GAPS_STAGE,
        from_schema=AugmentedVisitSchema,
        to_schema=EmployeeHistorySchema,
        config=conf,
        required_stages_names=[
            IngestionPipelineStages.EMPLOYEE_HISTORY_AGGREGATION_STAGE,
        ],
        transforms=[
            RenameColumns(
                to_schema=EmployeeHistorySchema,
            ),
            SetValueRange(
                columns=[
                    EmployeeHistorySchema.DAY_HOURS_PER_PERIOD,
                    EmployeeHistorySchema.NIGHT_HOURS_PER_PERIOD,
                    EmployeeHistorySchema.WEEKDAY_HOURS_PER_PERIOD,
                    EmployeeHistorySchema.WEEKEND_HOURS_PER_PERIOD,
                    EmployeeHistorySchema.VISIT_HOURS_PER_PERIOD,
                    EmployeeHistorySchema.AVERAGE_VISIT_DURATION_PER_PERIOD,
                ],
                min_value=0,
                max_value=24,
            ),
            SetValueRange(
                columns=[EmployeeHistorySchema.WORK_HOURS_DEVIATION_PER_PERIOD],
                min_value=-6,
                max_value=6,
            ),
            SetValueRange(
                columns=[EmployeeHistorySchema.AVERAGE_HOURLY_PAY_PER_PERIOD],
                min_value=0,
                max_value=100,
            ),
            SetValueRange(
                columns=[
                    EmployeeHistorySchema.AVERAGE_EMPLOYEE_COMMUTE_DISTANCE_PER_PERIOD
                ],
                min_value=0,
                max_value=200,
            ),
            FillGaps(),
        ],
    )
