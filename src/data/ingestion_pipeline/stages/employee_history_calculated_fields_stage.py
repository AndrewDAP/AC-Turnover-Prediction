"""
This module contains the EmployeeHistoryStage class which is responsible for
"""
from src.data.transforms.calculated_fields.compute_adl_completion_rate import (
    ComputeADLCompletionRate,
)
from src.data.transforms.calculated_fields.compute_employee_tenure import (
    ComputeDynamicEmployeeTenure,
)
from src.data.transforms.calculated_fields.compute_days_to_first_visit import (
    ComputeDaysToFirstVisit,
)
from src.data.transforms.clean.keep_columns import KeepColumns
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.transforms.clean.remove_nan import RemoveNan
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.schema.employee_history_schema import EmployeeHistorySchema

from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)
from src.data.transforms.calculated_fields.did_overtime_calculated_field import (
    DidOvertimeInPeriodCalculatedField,
)


# pylint: disable=unused-argument
def build_employee_history_calculated_fields_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the employee history stage of the ingestion pipeline.
    """

    return IngestionPipelineStage(
        name=IngestionPipelineStages.EMPLOYEE_HISTORY_CALCULATED_FIELDS_STAGE,
        from_schema=AugmentedVisitSchema,
        to_schema=EmployeeHistorySchema,
        config=conf,
        required_stages_names=[
            IngestionPipelineStages.EMPLOYEE_HISTORY_FILL_GAPS_STAGE,
        ],
        transforms=[
            ComputeADLCompletionRate(),
            DidOvertimeInPeriodCalculatedField(),
            ComputeDaysToFirstVisit(),
            ComputeDynamicEmployeeTenure(),
            KeepColumns(
                drop=True,
                columns=[
                    EmployeeHistorySchema.EMPLOYEE_TERMINATION_DATE,
                    EmployeeHistorySchema.EMPLOYEE_START_ON,
                ],
            ),
            RemoveNan(),
        ],
    )
