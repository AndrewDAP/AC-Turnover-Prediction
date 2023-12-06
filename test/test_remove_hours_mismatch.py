"""
This module contains the tests for the RemoveHoursMismatch class
"""

from os import path
from datetime import datetime
from pandas import read_csv, Timestamp
from src.data.transforms.clean.visit_data.remove_hours_mismatch import (
    RemoveHoursMismatch,
)
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.configs.config import Config
from src.utility.environment import Environment

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

INPUT_DATAFRAME_PATH = path.join("test", "csv", "test_remove_hours_mismatch.csv")
EXPECTED_DATAFRAME_PATH = path.join(
    "test", "csv", "test_remove_hours_mismatch_expected.csv"
)

env = Environment()

input_df = read_csv(INPUT_DATAFRAME_PATH, encoding="utf-8", low_memory=False)
expected_df = read_csv(EXPECTED_DATAFRAME_PATH, encoding="utf-8", low_memory=False)


def test_remove_hours_mismatch():
    """
    This method tests the RemoveHoursMismatch transform.
    """

    transformer = RemoveHoursMismatch()

    result_df, errors = transformer(
        input_df,
        ErrorDataFrame(input_df, config=conf),
        conf=conf,
        env=env,
    )
    transformer.to_dict()

    assert result_df.round(3).equals(expected_df.round(3))
    assert len(errors) == 0
