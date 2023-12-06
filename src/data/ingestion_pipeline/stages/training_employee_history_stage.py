"""
Training employee history stage of the ingestion pipeline.
"""
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.transforms.clean.join import Join
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.data.transforms.clean.fill_na_transform import FillNaTransform, FillNaColumn
from src.data.transforms.target_variable.generate_training_window_id import (
    GenerateTrainingWindowId,
)
from src.data.transforms.types.set_numerical_to_float64 import SetNumericalToFloat
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)
from src.data.transforms.clean.keep_columns import KeepColumns
from src.data.transforms.calculated_fields.timesnet_inference import TimesNetInference
from src.machine_learning.inference_runner import InferenceRunner


# pylint: disable=unused-argument
def build_training_employee_history_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the training employee history stage of the ingestion pipeline.

    Args:
        env (Environment): The environment object.
    """
    return IngestionPipelineStage(
        name=IngestionPipelineStages.TRAINING_EMPLOYEE_HISTORY_STAGE,
        from_schema=EmployeeHistorySchema,
        to_schema=EmployeeHistorySchema,
        config=conf,
        required_stages_names=[
            IngestionPipelineStages.EMPLOYEE_HISTORY_FILL_NA_STAGE,
            IngestionPipelineStages.Y_LABELS_GENERATION_STAGE,
        ],
        transforms=[
            GenerateTrainingWindowId(
                window_size=conf.training_window_size,
            ),
            Join(
                right=IngestionPipelineStages.Y_LABELS_GENERATION_STAGE,
                how="left",
                on=[
                    EmployeeHistorySchema.EMPLOYEE_ID,
                    EmployeeHistorySchema.PERIOD_START,
                ],
            ),
            FillNaTransform(
                columns=[
                    FillNaColumn(
                        column=EmployeeHistorySchema.Y_LABEL,
                        fill_policy="fill_with_default",
                        fill_default_value=0,
                    ),
                ],
            ),
            SetNumericalToFloat(),
            TimesNetInference(
                inference_column_name=EmployeeHistorySchema.TIMESNET_INFERENCE,
                inference_runner=InferenceRunner(
                    name="TimesNet Inference's Runner",
                    environment=env,
                    config=conf,
                    model_tag="timesnet",
                    run_group="TimesNet Feature Engineering",
                    run_id_that_produce_the_model="uwnleeju",
                ),
            ),
            KeepColumns(
                columns=[
                    EmployeeHistorySchema.TRAINING_WINDOW_ID,
                    EmployeeHistorySchema.EMPLOYEE_ID,
                    EmployeeHistorySchema.PERIOD_START,
                    EmployeeHistorySchema.EMPLOYEE_AGE,
                    EmployeeHistorySchema.EMPLOYEE_STATE,
                    EmployeeHistorySchema.EMPLOYEE_TENURE,
                    EmployeeHistorySchema.DAYS_TO_FIRST_VISIT,
                    EmployeeHistorySchema.TIMESNET_INFERENCE,
                    EmployeeHistorySchema.Y_LABEL,
                ]
            ),
        ],
    )
