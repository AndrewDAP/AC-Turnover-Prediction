"""
This module contains the tests for the ComputeADLCompletionRate class
"""
import pandas as pd
from src.data.transforms.calculated_fields.compute_adl_completion_rate import (
    ComputeADLCompletionRate,
)

SUM_HAS_ADL_COMPLETE = 50
SUM_HAS_ADL = 60

mock_df = pd.DataFrame(
    {
        "VISIT_HAS_ADL_COMPLETE": [SUM_HAS_ADL_COMPLETE],
        "VISIT_HAS_ADL": [SUM_HAS_ADL],
    }
)


def test_complete_adl_completion_rate():
    """
    This method tests if this transform computes the correct adl completion rate
    """
    transformer = ComputeADLCompletionRate()
    transformer.to_dict()

    # Call the transformer
    transformed_df, _ = transformer(mock_df, errors=None, conf=None, env=None)

    result = round(transformed_df["ADL_COMPLETION_RATE_PER_PERIOD"][0], 2)
    adl_completion_rate = round(SUM_HAS_ADL_COMPLETE / SUM_HAS_ADL, 2)
    assert result == adl_completion_rate
    # The columns used for the calculation should be dropped
    assert len(transformed_df.columns) == 1
