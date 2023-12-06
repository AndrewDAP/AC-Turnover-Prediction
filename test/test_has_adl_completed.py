"""
This module contains the tests for the HasADLCompleted class
"""
import pandas as pd
from src.data.transforms.calculated_fields.visit_data.has_adl_completed import (
    HasADLComplete,
)

SUM_HAS_ADL_COMPLETE = 50
SUM_HAS_ADL = 60

mock_df = pd.DataFrame(
    {
        "VISIT_ADL_COMPLETE": [0, 1, 0],
        "VISIT_HAS_ADL": [1, 1, 0],
    }
)

expected_result = [0, 1, 0]  # VISIT_ADL_COMPLETE * VISIT_HAS_ADL


def test_has_adl_completed():
    """
    This method tests the HasADLCompleted transformed
    """
    transformer = HasADLComplete()
    transformer.to_dict()
    transformed_df, _ = transformer(mock_df, errors=None, conf=None, env=None)
    assert transformed_df["VISIT_HAS_ADL_COMPLETED"].to_list() == expected_result
