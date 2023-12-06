"""
This module builds the client data cleaning calculated fields stage
"""

from os import path
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.schema.client_schema import ClientSchema, ClientSchemaRaw
from src.data.transforms.types.set_types_client import SetTypesClient
from src.data.transforms.clean.keep_columns import KeepColumns
from src.data.transforms.clean.set_value_range import SetValueRange
from src.data.transforms.clean.rename_columns import RenameColumns
from src.data.transforms.clean.clean_gender import CleanGender
from src.data.transforms.calculated_fields.client_data.coded_diagnosis_count import (
    CodedDiagnosticCount,
)
from src.data.transforms.clean.client_data.clean_diagnosis import CleanDiagnosis
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)


def build_client_data_cleaning_calculated_fields_stage(
    # pylint: disable=unused-argument
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the client data cleaning calculated fields stage

    Args:
        env (Environment): The environment
    """
    return IngestionPipelineStage(
        name=IngestionPipelineStages.CLIENT_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
        from_schema=ClientSchemaRaw,
        to_schema=ClientSchema,
        config=conf,
        load_dataframe_csv_path=path.join(env.data_dir, "client_data.csv"),
        transforms=[
            RenameColumns(
                to_schema=ClientSchema,
            ),
            SetTypesClient(),
            KeepColumns(
                columns=[
                    ClientSchema.CLIENT_ID,
                    ClientSchema.CLIENT_AGE,
                    ClientSchema.CLIENT_ADMISSION_DATE,
                    ClientSchema.CLIENT_GENDER,
                    ClientSchema.CLIENT_LATITUDE,
                    ClientSchema.CLIENT_LONGITUDE,
                    ClientSchema.CLIENT_DIAGNOSIS,
                ],
            ),
            SetValueRange(
                columns=[ClientSchema.CLIENT_AGE],
                min_value=0,
                max_value=125,
            ),
            CleanGender(
                column=ClientSchema.CLIENT_GENDER,
            ),
            CleanDiagnosis(
                column=ClientSchema.CLIENT_DIAGNOSIS,
            ),
            CodedDiagnosticCount(
                column=ClientSchema.CLIENT_DIAGNOSIS,
                column_count_name=ClientSchema.CLIENT_CODED_DIAGNOSIS_COUNT,
            ),
        ],
    )
