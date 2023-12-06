"""
Y Labels Generation Stage
"""
from os import path
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.transforms.clean.set_date_value_range import SetDateValueRange
from src.data.transforms.clean.keep_columns import KeepColumns
from src.data.transforms.clean.rename_columns import RenameColumns
from src.data.schema.status_schema import StatusSchemaRaw, StatusSchema
from src.data.schema.y_label_schema import YLabelSchema
from src.data.transforms.types.set_types_status import SetTypesStatus
from src.data.transforms.target_variable.generate_y_label_transform import (
    GenerateYLabelTransform,
)
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)


def build_y_labels_generation_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the y labels generation stage of the ingestion pipeline.

    Args:
        env (Environment): The environment object.
        config (Config): The config object.
    """
    return IngestionPipelineStage(
        name=IngestionPipelineStages.Y_LABELS_GENERATION_STAGE,
        from_schema=StatusSchemaRaw,
        to_schema=YLabelSchema,
        config=conf,
        load_dataframe_csv_path=path.join(env.data_dir, "status_data.csv"),
        transforms=[
            RenameColumns(
                to_schema=StatusSchema,
            ),
            SetTypesStatus(),
            KeepColumns(
                columns=[
                    StatusSchema.EMPLOYEE_ID,
                    StatusSchema.STATUS_START_DATE,
                    StatusSchema.STATUS_HISTORICAL,
                ],
            ),
            SetDateValueRange(
                columns=[
                    StatusSchema.STATUS_START_DATE,
                ],
                min_value=conf.period_start,
                max_value=conf.period_end,
            ),
            GenerateYLabelTransform(
                label_policy=conf.label_policy,
            ),
        ],
    )
