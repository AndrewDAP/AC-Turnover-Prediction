"""
This module contains the tests for the WorkHoursDeviationCalculatedField class
"""

from datetime import datetime
from pandas import DataFrame

from src.data.transforms.calculated_fields.work_hours_deviation_calculated_field import (
    WorkHoursDeviationCalculatedField,
)
from src.data.schema.visit_schema import VisitSchema
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

input_columns = [
    VisitSchema.VISIT_ID,
    VisitSchema.VISIT_SCHEDULED_DURATION,
    VisitSchema.VISIT_HOURS_APPROVED,
]

output_columns = [
    VisitSchema.VISIT_ID,
    VisitSchema.VISIT_SCHEDULED_DURATION,
    VisitSchema.VISIT_HOURS_APPROVED,
    VisitSchema.VISIT_WORK_HOURS_DEVIATION,
]

# Test case 1 is a visit with no work hours deviation
test_case_1 = {
    VisitSchema.VISIT_ID: 1,
    VisitSchema.VISIT_SCHEDULED_DURATION: 8,
    VisitSchema.VISIT_HOURS_APPROVED: 8,
    VisitSchema.VISIT_WORK_HOURS_DEVIATION: 0,
}

# Test case 2 is a visit with positive work hours deviation
test_case_2 = {
    VisitSchema.VISIT_ID: 2,
    VisitSchema.VISIT_SCHEDULED_DURATION: 8,
    VisitSchema.VISIT_HOURS_APPROVED: 10,
    VisitSchema.VISIT_WORK_HOURS_DEVIATION: 2,
}

# Test case 3 is a visit with negative work hours deviation
test_case_3 = {
    VisitSchema.VISIT_ID: 3,
    VisitSchema.VISIT_SCHEDULED_DURATION: 8,
    VisitSchema.VISIT_HOURS_APPROVED: 6,
    VisitSchema.VISIT_WORK_HOURS_DEVIATION: -2,
}

# Test case 4 is a visit with nan work hours deviation
test_case_4 = {
    VisitSchema.VISIT_ID: 4,
    VisitSchema.VISIT_SCHEDULED_DURATION: 8,
    VisitSchema.VISIT_HOURS_APPROVED: None,
    VisitSchema.VISIT_WORK_HOURS_DEVIATION: None,
}

test_cases = DataFrame(
    [
        test_case_1,
        test_case_2,
        test_case_3,
        test_case_4,
    ],
)

dataframe = test_cases[input_columns]
expected_dataframe = test_cases[output_columns]


def test_work_hours_deviation_calculated_field():
    """
    This method tests the WorkHoursDeviationCalculatedField transform.
    """

    transformer = WorkHoursDeviationCalculatedField()
    transformer.to_dict()

    result_df, errors = transformer(
        dataframe,
        ErrorDataFrame(dataframe, config=conf),
        conf=conf,
        env=env,
    )

    assert result_df.equals(expected_dataframe)
    assert len(errors) == 0
