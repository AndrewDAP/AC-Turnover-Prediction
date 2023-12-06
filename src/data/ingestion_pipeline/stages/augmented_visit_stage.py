"""
This module contains the augment visit stage of the ingestion pipeline.
"""
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.schema.visit_schema import VisitSchema
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.transforms.calculated_fields.was_late_calculated_field import (
    WasLateToVisitCalculatedField,
)
from src.data.transforms.calculated_fields.was_late_by import WasLateBy
from src.data.transforms.clean.visit_data.remove_hours_mismatch import (
    RemoveHoursMismatch,
)
from src.data.transforms.clean.join import Join
from src.data.transforms.clean.create_column import CreateColumn
from src.data.transforms.calculated_fields.compute_commute_distance import (
    ComputeCommuteDistance,
)
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)
from src.data.transforms.calculated_fields.compute_period_start import (
    ComputePeriodStart,
)
from src.data.transforms.calculated_fields.employee_data.compute_static_employee_tenure import (
    ComputeStaticEmployeeTenure,
)
from src.data.transforms.calculated_fields.compute_first_visit_date import (
    ComputeFirstVisitDate,
)
from src.data.transforms.clean.rename_columns import RenameColumns


# pylint: disable=unused-argument
def build_augmented_visit_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the augment visit stage of the ingestion pipeline.

    Args:
        env (Environment): The environment object.
    """
    return IngestionPipelineStage(
        name=IngestionPipelineStages.AUGMENT_VISIT_STAGE,
        from_schema=AugmentedVisitSchema,
        to_schema=AugmentedVisitSchema,
        config=conf,
        required_stages_names=[
            IngestionPipelineStages.VISIT_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
            IngestionPipelineStages.EMPLOYEE_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
            IngestionPipelineStages.CLIENT_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
            IngestionPipelineStages.CLOCK_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
        ],
        transforms=[
            Join(
                right=IngestionPipelineStages.CLOCK_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
                how="left",
                on=[VisitSchema.VISIT_ID],
            ),
            RemoveHoursMismatch(),
            Join(
                right=IngestionPipelineStages.EMPLOYEE_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
                how="left",
                on=[VisitSchema.EMPLOYEE_ID],
            ),
            Join(
                right=IngestionPipelineStages.CLIENT_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
                how="left",
                on=[VisitSchema.CLIENT_ID],
            ),
            CreateColumn(
                {
                    AugmentedVisitSchema.WAS_LATE_TO_VISIT: 0.0,
                }
            ),
            ComputeCommuteDistance(),
            ComputePeriodStart(period=conf.period_duration),
            ComputeStaticEmployeeTenure(),
            WasLateToVisitCalculatedField(),
            WasLateBy(),
            ComputeFirstVisitDate(),
            RenameColumns(to_schema=AugmentedVisitSchema),
        ],
    )
