"""
This module contains the tests for WasLateBy class
"""

from pandas import DataFrame

import pandas as pd

from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.transforms.calculated_fields.was_late_by import WasLateBy


df = DataFrame(
    {
        "START_TIME": [
            pd.to_datetime("8/20/2022 7:45:00 AM"),
            pd.to_datetime("8/20/2022 8:15:00 AM"),
        ],
        "VISIT_START_AT": [
            pd.to_datetime("8/20/2022 8:00:00 AM"),
            pd.to_datetime("8/20/2022 8:00:00 AM"),
        ],
    }
)


def test_was_late_by():
    """
    This function test if the time late to a visit is correctly computed
    """
    transformer = WasLateBy()
    transformer.to_dict()
    transformed_df, _ = transformer(df, errors=None, conf=None, env=None)

    assert transformed_df[AugmentedVisitSchema.WAS_LATE_BY].tolist() == [0.0, 15.0]
