"""
This module contains the tests for the ReplaceInvalidComputedRate class
"""
import pandas as pd
from src.data.schema.visit_schema import VisitSchema
from src.data.transforms.clean.visit_data.replace_invalid_computed_rate import (
    ReplaceInvalidComputedRate,
)

# Mock data for testing. First and fourth column's computed rate are invalid
df = pd.DataFrame(
    {
        "VISIT_HOURS_APPROVED": [8, 8, 8, 15],
        "VISIT_APPROVAL_STATUS": [1, 1, 1, 1],
        "VISIT_COMPUTED_RATE": [0, 50, 300, 0],
        "VISIT_CANCEL_CODE": [None, None, None, None],
        "VISIT_COMPUTED_RATE_UNITS": ["hours", "hours", "visits", "visits"],
    }
)


def test_replace_invalid_computed_rate():
    """
    This method tests if the class ReplaceInvalidComputedRate replaces invalid
    computed rates by the mean
    """
    # Create an instance of SumSalaryPerVisit
    transformer = ReplaceInvalidComputedRate()
    transformer.to_dict()

    # Call the transformer
    transformed_df, _ = transformer(df, errors=None, conf=None, env=None)

    # Assert that the invalid computed rate have been replaced by the mean of the units
    assert transformed_df.loc[0][VisitSchema.VISIT_COMPUTED_RATE] == 25
    assert transformed_df.loc[3][VisitSchema.VISIT_COMPUTED_RATE] == 150

    # Assert that the valid computed rate haven't been replaced
    assert transformed_df.loc[1][VisitSchema.VISIT_COMPUTED_RATE] == 50
    assert transformed_df.loc[2][VisitSchema.VISIT_COMPUTED_RATE] == 300
