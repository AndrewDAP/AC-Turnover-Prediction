"""
This module contains the tests for the SumSalaryPerVisit class
"""
from pandas import DataFrame
from src.data.transforms.calculated_fields.visit_data.sum_salary_per_visit import (
    SumSalaryPerVisit,
)
from src.data.schema.visit_schema import VisitSchema

# Mock data for testing
df = DataFrame(
    {
        "VISIT_HOURS_APPROVED": [8, 8],
        "VISIT_COMPUTED_RATE_UNITS": ["hours", "visits"],
        "VISIT_COMPUTED_RATE": [20, 300],
    }
)


def test_compute_total_pay():
    """
    This method tests if the class SumSalaryPerVisit computes the total pay per visit
    according to the computed rate units
    """
    # Create an instance of SumSalaryPerVisit
    transformer = SumSalaryPerVisit()
    transformer.to_dict()

    # Call the transformer
    transformed_df, _ = transformer(df, errors=None, conf=None, env=None)

    assert transformed_df[VisitSchema.VISIT_TOTAL_PAY].tolist() == [160, 300]
