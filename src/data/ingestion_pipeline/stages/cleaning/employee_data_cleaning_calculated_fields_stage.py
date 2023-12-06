"""
This module builds the employee data cleaning calculated fields stage of the ingestion pipeline.
"""
from os import path
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.schema.employee_schema import EmployeeSchema, EmployeeSchemaRaw
from src.data.transforms.clean.keep_columns import KeepColumns
from src.data.transforms.clean.set_value_range import SetValueRange
from src.data.transforms.clean.rename_columns import RenameColumns
from src.data.transforms.clean.remove_nan import RemoveNan
from src.data.transforms.clean.clean_gender import CleanGender
from src.data.transforms.types.set_types_employee import SetTypesEmployee
from src.data.transforms.clean.employee_data.clean_state import CleanState
from src.data.transforms.clean.categorize_text_field import CategorizeTextField
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)


# pylint: disable=unused-argument
def build_employee_data_cleaning_calculated_fields_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the employee data cleaning calculated fields stage of the ingestion pipeline.

    Args:
        env (Environment): The environment object.
    """
    return IngestionPipelineStage(
        name=IngestionPipelineStages.EMPLOYEE_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
        from_schema=EmployeeSchemaRaw,
        to_schema=EmployeeSchema,
        config=conf,
        load_dataframe_csv_path=path.join(env.data_dir, "employee_data.csv"),
        transforms=[
            RenameColumns(
                to_schema=EmployeeSchema,
            ),
            SetTypesEmployee(),
            KeepColumns(
                columns=[
                    EmployeeSchema.EMPLOYEE_ID,
                    EmployeeSchema.EMPLOYEE_AGE,
                    EmployeeSchema.EMPLOYEE_GENDER,
                    EmployeeSchema.EMPLOYEE_JOB_TITLE,
                    EmployeeSchema.EMPLOYEE_LATITUDE,
                    EmployeeSchema.EMPLOYEE_LONGITUDE,
                    EmployeeSchema.EMPLOYEE_START_ON,
                    EmployeeSchema.EMPLOYEE_STATE,
                    EmployeeSchema.EMPLOYEE_STATUS,
                    EmployeeSchema.EMPLOYEE_TERMINATION_DATE,
                ],
            ),
            RemoveNan(
                columns=[
                    EmployeeSchema.EMPLOYEE_GENDER,
                ],
            ),
            SetValueRange(
                columns=[EmployeeSchema.EMPLOYEE_AGE],
                min_value=16,
                max_value=90,
            ),
            CleanGender(
                column=EmployeeSchema.EMPLOYEE_GENDER,
            ),
            CleanState(
                column=EmployeeSchema.EMPLOYEE_STATE,
            ),
            CategorizeTextField(
                columns=[
                    EmployeeSchema.EMPLOYEE_JOB_TITLE,
                    EmployeeSchema.EMPLOYEE_GENDER,
                    EmployeeSchema.EMPLOYEE_STATE,
                ],
            ),
        ],
    )
