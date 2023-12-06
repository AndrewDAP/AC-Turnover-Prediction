"""
This module contains the test for the HourlyPay transform
"""

from pandas import DataFrame
import numpy as np
from src.data.schema.visit_schema import VisitSchema
from src.data.transforms.calculated_fields.visit_data.hourly_pay import HourlyPay

initial_df = DataFrame(
    {
        VisitSchema.VISIT_TOTAL_PAY: [20, None, 10],
        VisitSchema.VISIT_HOURS_APPROVED: [1, 1, 0],
    }
)

expected_results = [20.0, np.nan, np.nan]


def test_hourly_pay_transform():
    """
    This function runs the test for HourlyPay
    """
    transformer = HourlyPay()
    transformer.to_dict()
    result_df, _ = transformer(initial_df, errors=None, conf=None, env=None)
    result_list = result_df[VisitSchema.VISIT_HOURLY_PAY].to_list()

    assert result_list[0] == 20.0 and expected_results[0] == 20.0
    assert np.isnan(result_list[1]) and np.isnan(expected_results[1])
    assert np.isnan(result_list[2]) and np.isnan(expected_results[2])
