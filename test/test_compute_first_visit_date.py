"""
This module contains the tests for the ComputeFirstVisitDate class
"""

from os import path
from datetime import datetime
from pandas import read_csv, Timestamp
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.calculated_fields.compute_first_visit_date import (
    ComputeFirstVisitDate,
)
from src.utility.configs.config import Config
from src.utility.environment import Environment
from src.utility.dataframe_set_types import set_datetime

conf = Config(
    load_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
    n_splits=2,
    split_seed=5832391,
    log_every_n_steps=50,
    training_window_size=1,
    n_epochs=5,
    batch_size=16384,
    label_policy="90Days",
    period_duration="1D",
    cutoff=0.5,
    period_start=Timestamp(year=2018, month=1, day=1),
    oversampler="SMOTE",
    oversampler_args={},
    model="ExplainableBoostingMachine",
    model_config={},
)

INPUT_DATAFRAME_PATH = path.join(
    "test", "csv", "test_compute_first_visit_date_input.csv"
)
EXPECTED_DATAFRAME_PATH = path.join(
    "test", "csv", "test_compute_first_visit_date_expected.csv"
)

env = Environment()

input_df = read_csv(INPUT_DATAFRAME_PATH, encoding="utf-8", low_memory=False)
expected_df = read_csv(EXPECTED_DATAFRAME_PATH, encoding="utf-8", low_memory=False)

input_df = set_datetime(
    input_df,
    [
        AugmentedVisitSchema.VISIT_START_AT,
    ],
)
expected_df = set_datetime(
    expected_df,
    [
        AugmentedVisitSchema.VISIT_START_AT,
        AugmentedVisitSchema.EMPLOYEE_FIRST_VISIT,
    ],
)


def test_compute_first_visit_date():
    """
    This method tests the ComputeFirstVisitDate transform.
    """

    transformer = ComputeFirstVisitDate()
    transformer.to_dict()

    result_df, errors = transformer(
        input_df,
        ErrorDataFrame(input_df, config=conf),
        conf=conf,
        env=env,
    )

    assert result_df.equals(expected_df)
    assert len(errors) == 0
