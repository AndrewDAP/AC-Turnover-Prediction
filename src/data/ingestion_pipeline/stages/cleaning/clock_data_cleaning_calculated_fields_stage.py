"""
This module contains the stage that cleans the clock data and adds calculated fields.
"""
from os import path
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.transforms.clean.set_date_value_range import SetDateValueRange
from src.data.transforms.clean.set_value_range import SetValueRange
from src.data.transforms.clean.keep_columns import KeepColumns
from src.data.transforms.clean.rename_columns import RenameColumns
from src.data.transforms.types.set_types_clock import SetTypesClock
from src.data.transforms.calculated_fields.clock_data.shift_hours_calculated_field import (
    ShiftHoursCalculatedFields,
)
from src.data.transforms.aggregate.aggregate_by import AggregateBy
from src.data.schema.clock_schema import ClockSchema, ClockSchemaRaw
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)


# pylint: disable=unused-argument
def build_clock_data_cleaning_calculated_fields_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This stage cleans the clock data and adds calculated fields.

    Args:
        env (Environment): The environment object.
    """
    return IngestionPipelineStage(
        name=IngestionPipelineStages.CLOCK_DATA_CLEANING_CALCULATED_FIELDS_STAGE,
        from_schema=ClockSchemaRaw,
        to_schema=ClockSchema,
        config=conf,
        load_dataframe_csv_path=path.join(env.data_dir, "clock_data.csv"),
        transforms=[
            RenameColumns(
                to_schema=ClockSchema,
            ),
            SetTypesClock(),
            KeepColumns(
                columns=[
                    ClockSchema.VISIT_ID,
                    ClockSchema.START_TIME,
                    ClockSchema.END_TIME,
                ],
            ),
            SetDateValueRange(
                columns=[
                    ClockSchema.START_TIME,
                    ClockSchema.END_TIME,
                ],
                min_value=conf.period_start,
                max_value=conf.period_end,
            ),
            ShiftHoursCalculatedFields(),
            AggregateBy(
                [ClockSchema.VISIT_ID.name],
                {
                    ClockSchema.START_TIME: "min",
                    ClockSchema.END_TIME: "max",
                    ClockSchema.DAY_HOURS: "sum",
                    ClockSchema.NIGHT_HOURS: "sum",
                    ClockSchema.WEEKDAY_HOURS: "sum",
                    ClockSchema.WEEKEND_HOURS: "sum",
                },
            ),
            SetValueRange(
                columns=[
                    ClockSchema.DAY_HOURS,
                    ClockSchema.NIGHT_HOURS,
                    ClockSchema.WEEKDAY_HOURS,
                    ClockSchema.WEEKEND_HOURS,
                ],
                min_value=0,
                # 2 weeks
                max_value=336,
            ),
        ],
    )
