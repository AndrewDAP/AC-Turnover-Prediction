"""
This module contains the tests for the GenerateYLabelTransform class
"""

from os import path
from datetime import datetime
from pandas import read_csv
from src.data.transforms.target_variable.generate_y_label_transform import (
    GenerateYLabelTransform,
)
from src.data.schema.status_schema import StatusSchema
from src.data.schema.y_label_schema import YLabelSchema
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
    oversampler="SMOTE",
    oversampler_args={},
    model="ExplainableBoostingMachine",
    model_config={},
)

INPUT_DATAFRAME_PATH = path.join("test", "csv", "test_y_label_input.csv")
EXPECTED_DATAFRAME_PATH = path.join("test", "csv", "test_y_label_expected.csv")

env = Environment()

input_df = read_csv(INPUT_DATAFRAME_PATH, encoding="utf-8", low_memory=False)
expected_df = read_csv(EXPECTED_DATAFRAME_PATH, encoding="utf-8", low_memory=False)

input_df = set_datetime(
    input_df,
    [
        StatusSchema.STATUS_START_DATE,
        StatusSchema.STATUS_END_DATE,
    ],
)
expected_df = set_datetime(
    expected_df,
    [
        YLabelSchema.PERIOD_START,
    ],
)


def test_y_label():
    """
    This method tests the GenerateYLabelTransform transform.
    """

    transformer = GenerateYLabelTransform(
        label_policy="90Days",
    )
    transformer.to_dict()

    result_df, errors = transformer(
        input_df,
        ErrorDataFrame(input_df, config=conf),
        conf=conf,
        env=env,
    )

    assert result_df.equals(expected_df)
    assert len(errors) == 0
