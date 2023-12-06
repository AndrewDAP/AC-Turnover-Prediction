"""
This module contains the segmentation stage of the ingestion pipeline.
"""
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.schema.segmentation_schema import SegmentationSchema
from src.data.transforms.clean.rename_columns import RenameColumns
from src.data.transforms.aggregate.aggregate_by import AggregateBy
from src.data.transforms.clean.fill_na_transform import FillNaTransform, FillNaColumn
from src.data.transforms.types.set_numerical_to_float64 import SetNumericalToFloat
from src.data.transforms.calculated_fields.segmentation.feature_ratios import (
    FeatureRatios,
)
from src.data.transforms.calculated_fields.segmentation.weekly_features import (
    WeeklyFeatures,
)
from src.data.transforms.calculated_fields.segmentation.average_visit_duration import (
    AverageVisitDuration,
)
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)
from src.data.transforms.clean.set_value_range import SetValueRange


# pylint: disable=unused-argument
def build_segmentation_stage(
    conf: Config,
    env: Environment,
) -> IngestionPipelineStage:
    """
    This function builds the segmentation stage of the ingestion pipeline.
    """
    return IngestionPipelineStage(
        name=IngestionPipelineStages.SEGMENTATION_STAGE,
        from_schema=AugmentedVisitSchema,
        to_schema=SegmentationSchema,
        config=conf,
        required_stages_names=[
            IngestionPipelineStages.AUGMENT_VISIT_STAGE,
        ],
        transforms=[
            AggregateBy(
                [AugmentedVisitSchema.EMPLOYEE_ID.name],
                aggregation_functions={
                    AugmentedVisitSchema.EMPLOYEE_AGE: "max",
                    AugmentedVisitSchema.EMPLOYEE_GENDER: "max",
                    AugmentedVisitSchema.EMPLOYEE_JOB_TITLE: "max",
                    AugmentedVisitSchema.EMPLOYEE_STATE: "max",
                    AugmentedVisitSchema.EMPLOYEE_TENURE: "max",
                    AugmentedVisitSchema.CLIENT_AGE: "mean",
                    AugmentedVisitSchema.VISIT_ID: "count",
                    AugmentedVisitSchema.HOURLY_PAY: "mean",
                    AugmentedVisitSchema.VISIT_HOURS_APPROVED: "sum",
                    AugmentedVisitSchema.VISIT_WORK_HOURS_DEVIATION: "mean",
                    AugmentedVisitSchema.VISIT_HAS_ADL: "sum",
                    AugmentedVisitSchema.VISIT_HAS_ADL_COMPLETE: "sum",
                    AugmentedVisitSchema.EMPLOYEE_COMMUTE_DISTANCE: "mean",
                    AugmentedVisitSchema.CLIENT_CODED_DIAGNOSIS_COUNT: "mean",
                    AugmentedVisitSchema.WAS_LATE_TO_VISIT: "sum",
                    AugmentedVisitSchema.WAS_LATE_BY: "mean",
                    AugmentedVisitSchema.CLIENT_ID: "nunique",
                },
            ),
            RenameColumns(
                to_schema=SegmentationSchema,
            ),
            FillNaTransform(
                columns=[
                    FillNaColumn(
                        column=SegmentationSchema.EMPLOYEE_AGE,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.EMPLOYEE_GENDER,
                        fill_policy="fill_with_default",
                        fill_default_value=3.0,
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.EMPLOYEE_JOB_TITLE,
                        fill_policy="fill_with_default",
                        fill_default_value=10.0,
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.EMPLOYEE_STATE,
                        fill_policy="fill_with_default",
                        fill_default_value=31.0,
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.EMPLOYEE_TENURE,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.VISITS,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.TOTAL_VISIT_HOURS,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_WORK_HOURS_DEVIATION,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_HOURLY_PAY,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.ADL_COUNT,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.COMPLETED_ADL,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_DISTANCE_TO_PATIENT,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_CODED_DIAGNOSIS_PER_PATIENT,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.LATE_ARRIVALS,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_WAS_LATE_BY,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.UNIQUE_CLIENTS,
                        fill_policy="fill",
                        method="mean",
                    ),
                ],
            ),
            AverageVisitDuration(),
            WeeklyFeatures(),
            FeatureRatios(
                target_columns=[
                    SegmentationSchema.UNIQUE_CLIENTS,
                ],
                key_column=SegmentationSchema.VISITS,
            ),
            FeatureRatios(
                target_columns=[
                    SegmentationSchema.COMPLETED_ADL,
                ],
                key_column=SegmentationSchema.ADL_COUNT,
            ),
            FillNaTransform(
                columns=[
                    FillNaColumn(
                        column=SegmentationSchema.AVG_VISIT_DURATION,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_VISIT_HOURS_PER_WEEK,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_VISITS_PER_WEEK,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_HOURLY_PAY,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.COMPLETED_ADL_RATIO,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_DISTANCE_TO_PATIENT,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_CODED_DIAGNOSIS_PER_PATIENT,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_LATE_ARRIVALS_PER_WEEK,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.AVG_WAS_LATE_BY,
                        fill_policy="fill",
                        method="mean",
                    ),
                    FillNaColumn(
                        column=SegmentationSchema.UNIQUE_CLIENTS_RATIO,
                        fill_policy="fill",
                        method="mean",
                    ),
                ],
            ),
            SetValueRange(
                columns=[SegmentationSchema.AVG_HOURLY_PAY],
                min_value=0,
                max_value=100,
            ),
            SetValueRange(
                columns=[SegmentationSchema.AVG_WAS_LATE_BY],
                min_value=0,
                max_value=60,
            ),
            SetValueRange(
                columns=[SegmentationSchema.AVG_VISIT_HOURS_PER_WEEK],
                min_value=0,
                max_value=168,
            ),
            SetNumericalToFloat(),
        ],
    )
