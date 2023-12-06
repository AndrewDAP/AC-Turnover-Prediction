"""
This module contains the tests for the FillGaps class
"""

from os import path
from datetime import datetime
from pandas import read_csv
from numpy import isnan
from src.data.transforms.clean.rename_columns import RenameColumns
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.clean.fill_gaps import FillGaps
from src.utility.configs.config import Config
from src.utility.environment import Environment
from src.utility.dataframe_set_types import set_datetime

INPUT_DATAFRAME_PATH = path.join("test", "csv", "test_fill_gaps_input.csv")
EXPECTED_DATAFRAME_PATH = path.join("test", "csv", "test_fill_gaps_expected.csv")

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

env = Environment()

input_df = read_csv(
    INPUT_DATAFRAME_PATH,
    encoding="utf-8",
    low_memory=False,
)

input_df = set_datetime(
    input_df,
    [
        EmployeeHistorySchema.EMPLOYEE_TERMINATION_DATE,
        EmployeeHistorySchema.PERIOD_START,
        EmployeeHistorySchema.EMPLOYEE_START_ON,
    ],
)

expected_df = read_csv(
    EXPECTED_DATAFRAME_PATH,
    encoding="utf-8",
    low_memory=False,
)

expected_df = set_datetime(
    expected_df,
    [
        EmployeeHistorySchema.EMPLOYEE_TERMINATION_DATE,
        EmployeeHistorySchema.PERIOD_START,
        EmployeeHistorySchema.EMPLOYEE_START_ON,
    ],
)


def test_fill_gaps():
    """
    This method tests the ComputeCommuteDistance transform.
    """

    transform1 = RenameColumns(to_schema=EmployeeHistorySchema)
    transform2 = FillGaps()
    transform1.to_dict()
    transform2.to_dict()

    result_df, errors = transform1(
        input_df,
        ErrorDataFrame(input_df, config=conf),
        conf=conf,
        env=env,
    )
    result_df, errors = transform2(
        input_df,
        ErrorDataFrame(input_df, config=conf),
        conf=conf,
        env=env,
    )

    for column in result_df.columns:
        for i in range(len(result_df[column])):
            if isinstance(result_df[column][i], (datetime, str)):
                if isinstance(result_df[column][i], datetime):
                    # Comparing datetime objects as strings
                    assert str(result_df[column][i]) == str(expected_df[column][i])
                else:
                    # For string columns, direct string comparison
                    assert result_df[column][i] == expected_df[column][i]
            elif isnan(result_df[column][i]) and isnan(expected_df[column][i]):
                # Check if both values are NaN
                assert isnan(result_df[column][i]) == isnan(expected_df[column][i])
            else:
                # For non-datetime, non-string, and non-NaN columns, rounding for floating-point comparison
                assert round(result_df[column][i], 3) == round(
                    expected_df[column][i], 3
                )

    assert len(errors) == 0
