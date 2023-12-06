"""
This module contains the tests for the RemoveNan class
"""
import pandas as pd
from src.data.transforms.clean.remove_nan import RemoveNan

# Mock data for testing
df = pd.DataFrame({"ID": [1, 2, "nan", 4, 5]})


def test_remove_nan():
    """
    This method tests if RemoveNan replaces the NaN values by None
    """
    # Create an instance of CSVRemoveNan
    transformer = RemoveNan(columns=["ID"])
    transformer.to_dict()

    # Call the transformer
    transformed_df, _ = transformer(df, errors=None, conf=None, env=None)

    assert transformed_df["ID"].tolist() == [1, 2, None, 4, 5]
