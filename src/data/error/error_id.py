"""
Error id's for the data validation errors
"""
from enum import Enum


class ErrorId(Enum):
    """
    Enum class for error id's
    """

    MISSING_VALUE = "missing_value"
    OUT_OF_RANGE = "out_of_range"
    INVALID_VALUE = "invalid_value"
    INVALID_TYPE = "invalid_type"
    INVALID_DATETIME = "invalid_datetime"
    INVALID_FORMAT = "invalid_format"
    LOGICAL_ERROR = "logical_error"
