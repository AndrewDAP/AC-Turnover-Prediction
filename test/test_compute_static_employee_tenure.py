"""
This module contains the tests for the ComputeStaticEmployeeTenure class
"""

from os import path
from datetime import datetime
from pandas import read_csv, Timestamp
from src.data.transforms.calculated_fields.employee_data.compute_static_employee_tenure import (
    ComputeStaticEmployeeTenure,
)
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.error.error_dataframe import ErrorDataFrame
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
    "test", "csv", "test_compute_static_employee_tenure_input.csv"
)
EXPECTED_DATAFRAME_PATH = path.join(
    "test", "csv", "test_compute_static_employee_tenure_expected.csv"
)

env = Environment()

input_df = read_csv(INPUT_DATAFRAME_PATH, encoding="utf-8", low_memory=False)
expected_df = read_csv(EXPECTED_DATAFRAME_PATH, encoding="utf-8", low_memory=False)

input_df = set_datetime(
    input_df,
    [
        AugmentedVisitSchema.PERIOD_START,
        AugmentedVisitSchema.EMPLOYEE_START_ON,
        AugmentedVisitSchema.EMPLOYEE_TERMINATION_DATE,
    ],
)
expected_df = set_datetime(
    expected_df,
    [
        AugmentedVisitSchema.PERIOD_START,
        AugmentedVisitSchema.EMPLOYEE_START_ON,
        AugmentedVisitSchema.EMPLOYEE_TERMINATION_DATE,
    ],
)


def test_compute_static_employee_tenure():
    """
    This method tests the ComputeStaticEmployeeTenure transform.
    """

    transformer = ComputeStaticEmployeeTenure()
    transformer.to_dict()

    result_df, errors = transformer(
        input_df,
        ErrorDataFrame(input_df, config=conf),
        conf=conf,
        env=env,
    )

    assert result_df.round(3).equals(expected_df.round(3))
    assert len(errors) == 0
