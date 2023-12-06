"""
This module contains the stage that cleans the visit data and adds calculated fields.
"""
from os import path
from data.transforms.calculated_fields.visit_data.has_adl_completed import (
    HasADLComplete,
)
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.schema.visit_schema import VisitSchemaRaw, VisitSchema
from src.data.transforms.clean.set_date_value_range import SetDateValueRange
from src.data.transforms.types.set_types_visit import SetTypesVisit
from src.data.transforms.clean.keep_columns import KeepColumns
from src.data.transforms.clean.value_must_equal import ValueMustEqual
from src.data.transforms.clean.set_value_range import SetValueRange
from src.data.transforms.calculated_fields.visit_data.sum_salary_per_visit import (
    SumSalaryPerVisit,
)
from src.data.transforms.calculated_fields.visit_data.hourly_pay import (
    HourlyPay,
)
from src.data.transforms.clean.visit_data.replace_invalid_computed_rate import (
    ReplaceInvalidComputedRate,
)
from src.data.transforms.clean.rename_columns import RenameColumns
from src.data.transforms.clean.visit_data.clean_service_description import (
    CleanServiceDescription,
)
from src.data.transforms.calculated_fields.work_hours_deviation_calculated_field import (
    WorkHoursDeviationCalculatedField,
)
from src.data.transforms.clean.remove_nan import RemoveNan
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)


# pylint: disable=unused-argument
def build_visit_data_cleaning_calculated_fields_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the visit data cleaning calculated fields stage of the ingestion pipeline.

    Args:
        env (Environment): The environment object.
    """
    return IngestionPipelineStage(
        name=IngestionPipelineStages.VISIT_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
        from_schema=VisitSchemaRaw,
        to_schema=VisitSchema,
        config=conf,
        load_dataframe_csv_path=path.join(env.data_dir, "visit_data.csv"),
        transforms=[
            RenameColumns(
                to_schema=VisitSchema,
            ),
            SetTypesVisit(),
            ValueMustEqual(
                column=VisitSchema.EMPLOYEE_ID,
                value=2,
                invert=True,
            ),
            HasADLComplete(),
            KeepColumns(
                columns=[
                    VisitSchema.VISIT_ID,
                    VisitSchema.EMPLOYEE_ID,
                    VisitSchema.CLIENT_ID,
                    VisitSchema.VISIT_CANCEL_CODE,
                    VisitSchema.VISIT_START_AT,
                    VisitSchema.VISIT_END_AT,
                    VisitSchema.VISIT_START_AT_UTC,
                    VisitSchema.VISIT_END_AT_UTC,
                    VisitSchema.VISIT_SERVICE_DESCRIPTION,
                    VisitSchema.VISIT_IS_PAID,
                    VisitSchema.VISIT_IN_OUT_OF_RECURRENCE_STATUS,
                    VisitSchema.VISIT_RECURRENCE,
                    VisitSchema.VISIT_APPROVAL_STATUS,
                    VisitSchema.VISIT_COMPLETED,
                    VisitSchema.VISIT_COMPUTED_RATE,
                    VisitSchema.VISIT_COMPUTED_RATE_UNITS,
                    VisitSchema.VISIT_SCHEDULED_DURATION,
                    VisitSchema.VISIT_UNIT_QTY,
                    VisitSchema.VISIT_HOURS_APPROVED,
                    VisitSchema.VISIT_ON_HOLD_REASON,
                    VisitSchema.VISIT_HAS_ADL_COMPLETED,
                    VisitSchema.VISIT_HAS_ADL,
                ],
            ),
            RemoveNan(
                columns=[
                    VisitSchema.VISIT_CANCEL_CODE,
                    VisitSchema.VISIT_COMPUTED_RATE_UNITS,
                    VisitSchema.VISIT_ON_HOLD_REASON,
                ],
            ),
            SetDateValueRange(
                columns=[
                    VisitSchema.VISIT_START_AT,
                    VisitSchema.VISIT_END_AT,
                ],
                min_value=conf.period_start,
                max_value=conf.period_end,
            ),
            SetDateValueRange(
                columns=[
                    VisitSchema.VISIT_START_AT_UTC,
                    VisitSchema.VISIT_END_AT_UTC,
                ],
                min_value=conf.period_start.tz_localize("UTC"),
                max_value=conf.period_end.tz_localize("UTC"),
            ),
            SetValueRange(
                columns=[VisitSchema.VISIT_SCHEDULED_DURATION],
                max_value=35,
            ),
            SetValueRange(
                columns=[VisitSchema.VISIT_UNIT_QTY],
                max_value=20,
            ),
            SetValueRange(
                columns=[VisitSchema.VISIT_HOURS_APPROVED],
                max_value=50,
            ),
            CleanServiceDescription(column=VisitSchema.VISIT_SERVICE_DESCRIPTION),
            ReplaceInvalidComputedRate(),
            SumSalaryPerVisit(),
            HourlyPay(),
            WorkHoursDeviationCalculatedField(),
        ],
    )
