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

# pylint: disable=unused-argument
def build_employee_history_anomaly_detection_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the employee history stage of the ingestion pipeline.
    """

    return IngestionPipelineStage(
        name=IngestionPipelineStages.EMPLOYEE_HISTORY_ANOMALY_DETECTION_STAGE,
        from_schema=AugmentedVisitSchema,
        to_schema=EmployeeHistorySchema,
        config=conf,
        required_stages_names=[
            IngestionPipelineStages.EMPLOYEE_HISTORY_FILL_NA_STAGE,
        ],
        transforms=[
            # AnomalyDetector(),
        ],
    )
