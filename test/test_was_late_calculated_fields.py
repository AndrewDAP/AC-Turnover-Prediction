"""
This module contains the tests for WasLateToVisitCalculatedField class
"""
from pandas import DataFrame

import pandas as pd

from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.transforms.calculated_fields.was_late_calculated_field import (
    WasLateToVisitCalculatedField,
)

df = DataFrame(
    {
        "START_TIME": [
            pd.to_datetime("8/20/2022 7:45:00 AM"),
            pd.to_datetime("8/20/2022 8:15:00 AM"),
        ],
        "VISIT_START_AT": [
            pd.to_datetime("8/20/2022  8:00:00 AM"),
            pd.to_datetime("8/20/2022  8:00:00 AM"),
        ],
    }
)


def test_was_late_calculated_field():
    """
    This method tests if the class WasLateToVisitCalculatedField computes 1 for late or 0 for in time
    """
    transformer = WasLateToVisitCalculatedField()
    transformer.to_dict()
    transformed_df, _ = transformer(df, errors=None, conf=None, env=None)

    assert transformed_df[AugmentedVisitSchema.WAS_LATE_TO_VISIT].tolist() == [0, 1]
