"""
This module contains the test for the CategorizeTextField transform
"""
import os
from pandas import DataFrame
from src.data.transforms.clean.categorize_text_field import (
    CategorizeTextField,
)

initial_df = DataFrame(
    {"TEST_VALUES": ["Bob", "Dylan", "Kyle", "Bob", "Dylan", "Kyle"]}
)

expected_result = [0, 1, 2, 0, 1, 2]


def test_categorize_text_field():
    """
    This function runs the test for CategorizeTextField
    """
    transformer = CategorizeTextField(columns=["TEST_VALUES"])
    transformer.to_dict()
    result_df, _ = transformer(initial_df, errors=None, conf=None, env=None)

    if os.path.isfile("src/mappings/TEST_VALUES_mapping.json"):
        os.remove("src/mappings/TEST_VALUES_mapping.json")

    assert result_df["TEST_VALUES"].to_list() == expected_result
