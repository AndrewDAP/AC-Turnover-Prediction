"""
This function builds the employee history stage of the ingestion pipeline.
"""

from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage

from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.schema.employee_history_schema import EmployeeHistorySchema

from src.data.transforms.rolling.compute_rolling_features import ComputeRollingFeatures

from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)


# pylint: disable=unused-argument
def build_employee_history_rolling_features_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the employee history stage of the ingestion pipeline.
    """

    return IngestionPipelineStage(
        name=IngestionPipelineStages.EMPLOYEE_HISTORY_ROLLING_FEATURES_STAGE,
        from_schema=AugmentedVisitSchema,
        to_schema=EmployeeHistorySchema,
        config=conf,
        required_stages_names=[
            IngestionPipelineStages.EMPLOYEE_HISTORY_CALCULATED_FIELDS_STAGE,
        ],
        transforms=[
            ComputeRollingFeatures(
                # cannot use identical columns elsewhere lint will crash
                params=[
                    {
                        "agg_function": "mean",
                        "arguments": None,
                        "columns": [
                            EmployeeHistorySchema.PERIOD_START,
                            EmployeeHistorySchema.VISIT_HOURS_PER_PERIOD,
                        ],
                        "window_size": 3,
                        "sub_name": "mean",
                    },
                    {
                        "agg_function": "quantile",
                        "arguments": {"q": 0.25},
                        "columns": [
                            EmployeeHistorySchema.PERIOD_START,
                            EmployeeHistorySchema.VISIT_HOURS_PER_PERIOD,
                        ],
                        "window_size": 3,
                        "sub_name": "quantile_25",
                    },
                    {
                        "agg_function": "quantile",
                        "arguments": {"q": 0.50},
                        "columns": [
                            EmployeeHistorySchema.PERIOD_START,
                            EmployeeHistorySchema.VISIT_HOURS_PER_PERIOD,
                        ],
                        "window_size": 3,
                        "sub_name": "quantile_50",
                    },
                    {
                        "agg_function": "quantile",
                        "arguments": {"q": 0.75},
                        "columns": [
                            EmployeeHistorySchema.PERIOD_START,
                            EmployeeHistorySchema.VISIT_HOURS_PER_PERIOD,
                        ],
                        "window_size": 3,
                        "sub_name": "quantile_75",
                    },
                ]
            ),
        ],
    )
