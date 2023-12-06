"""
This module contains the tests for the ComputeCommuteDistance class
"""

from datetime import datetime
from pandas import DataFrame
from numpy import isnan
from src.data.transforms.calculated_fields.compute_commute_distance import (
    ComputeCommuteDistance,
)
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
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
    AugmentedVisitSchema.CLIENT_LATITUDE,
    AugmentedVisitSchema.CLIENT_LONGITUDE,
    AugmentedVisitSchema.EMPLOYEE_LATITUDE,
    AugmentedVisitSchema.EMPLOYEE_LONGITUDE,
]

output_columns = [
    AugmentedVisitSchema.CLIENT_LATITUDE,
    AugmentedVisitSchema.CLIENT_LONGITUDE,
    AugmentedVisitSchema.EMPLOYEE_LATITUDE,
    AugmentedVisitSchema.EMPLOYEE_LONGITUDE,
    AugmentedVisitSchema.EMPLOYEE_COMMUTE_DISTANCE,
]

# Test case 1 with normal employee and client coordinates
test_case_1 = {
    AugmentedVisitSchema.CLIENT_LATITUDE: 42.48,
    AugmentedVisitSchema.CLIENT_LONGITUDE: -70.94,
    AugmentedVisitSchema.EMPLOYEE_LATITUDE: 42.54,
    AugmentedVisitSchema.EMPLOYEE_LONGITUDE: -71.1,
    AugmentedVisitSchema.EMPLOYEE_COMMUTE_DISTANCE: 14.714385,
}

# Test case 2 is missing a coordinate
test_case_2 = {
    AugmentedVisitSchema.CLIENT_LATITUDE: None,
    AugmentedVisitSchema.CLIENT_LONGITUDE: -70.94,
    AugmentedVisitSchema.EMPLOYEE_LATITUDE: 42.54,
    AugmentedVisitSchema.EMPLOYEE_LONGITUDE: -71.1,
    AugmentedVisitSchema.EMPLOYEE_COMMUTE_DISTANCE: None,
}

test_cases = DataFrame(
    [
        test_case_1,
        test_case_2,
    ],
)

input_df = test_cases[input_columns]
expected_df = test_cases[output_columns]


def test_employee_commute_distance_calculated_field():
    """
    This method tests the ComputeCommuteDistance transform.
    """

    transformer = ComputeCommuteDistance()
    transformer.to_dict()

    result_df, errors = transformer(
        input_df,
        ErrorDataFrame(input_df, config=conf),
        conf=conf,
        env=env,
    )

    for column in result_df.columns:
        for i in range(len(result_df[column])):
            if isnan(expected_df[column][i]):
                assert isnan(result_df[column][i])
                continue
            assert round(result_df[column][i], 3) == round(expected_df[column][i], 3)

    assert len(errors) == 0
    assert transformer.to_dict()["name"] == "ComputeCommuteDistance"
