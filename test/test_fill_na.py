"""
This module contains the tests for the FillNaTransform class
"""

from datetime import datetime
from pandas import DataFrame, isna

from src.data.transforms.clean.fill_na_transform import FillNaTransform, FillNaColumn
from src.data.schema.employee_history_schema import EmployeeHistorySchema
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
    oversampler="SMOTE",
    oversampler_args={},
    model="ExplainableBoostingMachine",
    model_config={},
)

env = Environment()

dataframe = DataFrame(
    {
        EmployeeHistorySchema.EMPLOYEE_ID: [1, 1, 1, 2, 2, 2, 3],
        EmployeeHistorySchema.VISIT_COUNT_PER_PERIOD: [1, 2, None, None, 5, 6, 4],
        EmployeeHistorySchema.EMPLOYEE_AGE: [None, 20, 30, 40, 50, 60, None],
        EmployeeHistorySchema.ADL_COMPLETION_RATE_PER_PERIOD: [
            1,
            None,
            None,
            2,
            1,
            6,
            4,
        ],
        EmployeeHistorySchema.EMPLOYEE_FIRST_VISIT: [0, 0, 1, 2, 1, 6, None],
        EmployeeHistorySchema.AVERAGE_AGE_OF_PATIENTS_PER_PERIOD: [
            None,
            0,
            0,
            2,
            1,
            6,
            None,
        ],
    },
)
expected_dataframe = DataFrame(
    {
        EmployeeHistorySchema.EMPLOYEE_ID: [1, 1, 1, 2, 2, 2],
        EmployeeHistorySchema.VISIT_COUNT_PER_PERIOD: [1, 2, 1.5, 5.5, 5, 6],
        EmployeeHistorySchema.EMPLOYEE_AGE: [-1, 20, 30, 40, 50, 60],
        EmployeeHistorySchema.ADL_COMPLETION_RATE_PER_PERIOD: [1, 1, 1, 2, 1, 6],
        EmployeeHistorySchema.EMPLOYEE_FIRST_VISIT: [0, 0, 1, 2, 1, 6],
        EmployeeHistorySchema.AVERAGE_AGE_OF_PATIENTS_PER_PERIOD: [1.8, 0, 0, 2, 1, 6],
    },
)


def test_fill_na():
    """
    This method tests the FillNaTransform transform.
    """

    transformer = FillNaTransform(
        columns=[
            FillNaColumn(
                column=EmployeeHistorySchema.VISIT_COUNT_PER_PERIOD,
                fill_policy="fill",
                method="mean",
                fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
            ),
            FillNaColumn(
                column=EmployeeHistorySchema.EMPLOYEE_AGE,
                fill_policy="fill_with_default",
                fill_default_value=-1,
            ),
            FillNaColumn(
                column=EmployeeHistorySchema.ADL_COMPLETION_RATE_PER_PERIOD,
                fill_policy="fill",
                method="mode",
            ),
            FillNaColumn(
                column=EmployeeHistorySchema.ADL_COMPLETION_RATE_PER_PERIOD,
                fill_policy="fill",
                method="mode",
                fill_by=EmployeeHistorySchema.EMPLOYEE_ID,
            ),
            FillNaColumn(
                column=EmployeeHistorySchema.EMPLOYEE_FIRST_VISIT,
                fill_policy="drop",
            ),
            FillNaColumn(
                column=EmployeeHistorySchema.AVERAGE_AGE_OF_PATIENTS_PER_PERIOD,
                fill_policy="fill",
                method="mean",
            ),
        ],
    )
    transformer.to_dict()

    result_df, errors = transformer(
        dataframe,
        ErrorDataFrame(dataframe, config=conf),
        conf=conf,
        env=env,
    )

    for column in result_df.columns:
        for i in range(len(result_df[column])):
            assert not isna(result_df[column][i])
            assert round(result_df[column][i], 3) == round(
                expected_dataframe[column][i], 3
            )
    assert len(errors) == 0
    assert (
        transformer.to_dict().items()
        == {
            "name": "FillNaTransform",
            "columns": [
                {
                    "column": EmployeeHistorySchema.VISIT_COUNT_PER_PERIOD.name,
                    "fill_policy": "fill",
                    "method": "mean",
                    "fill_by": EmployeeHistorySchema.EMPLOYEE_ID.name,
                    "fill_default_value": None,
                },
                {
                    "column": EmployeeHistorySchema.EMPLOYEE_AGE.name,
                    "fill_policy": "fill_with_default",
                    "method": None,
                    "fill_by": None,
                    "fill_default_value": -1,
                },
                {
                    "column": EmployeeHistorySchema.ADL_COMPLETION_RATE_PER_PERIOD.name,
                    "fill_policy": "fill",
                    "method": "mode",
                    "fill_by": None,
                    "fill_default_value": None,
                },
                {
                    "column": EmployeeHistorySchema.ADL_COMPLETION_RATE_PER_PERIOD.name,
                    "fill_policy": "fill",
                    "method": "mode",
                    "fill_by": EmployeeHistorySchema.EMPLOYEE_ID.name,
                    "fill_default_value": None,
                },
                {
                    "column": EmployeeHistorySchema.EMPLOYEE_FIRST_VISIT.name,
                    "fill_policy": "drop",
                    "method": None,
                    "fill_by": None,
                    "fill_default_value": None,
                },
                {
                    "column": EmployeeHistorySchema.AVERAGE_AGE_OF_PATIENTS_PER_PERIOD.name,
                    "fill_policy": "fill",
                    "method": "mean",
                    "fill_by": None,
                    "fill_default_value": None,
                },
            ],
        }.items()
    )
