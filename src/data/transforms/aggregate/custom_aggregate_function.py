"""
This file contain custom aggregation function
"""

from typing import Dict, Union
import numpy as np


def quantile_25(x):
    """
    This function finds the 25 quantile of VISIT_HOURS in a period
    """
    return np.percentile(x, 25)


def quantile_50(x):
    """
    This function finds the 50 quantile of VISIT_HOURS in a period
    """
    return np.percentile(x, 50)


def quantile_75(x):
    """
    This function finds the 75 quantile of VISIT_HOURS in a period
    """
    return np.percentile(x, 75)


custom_functions: Dict[str, Union[str, callable]] = {
    "quantile_25": quantile_25,
    "quantile_50": quantile_50,
    "quantile_75": quantile_75,
}
