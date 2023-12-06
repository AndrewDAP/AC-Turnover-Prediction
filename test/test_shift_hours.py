"""
Test that the shift hours transform works as expected
"""
from pandas import DataFrame
from pandas import Timestamp
from src.data.transforms.calculated_fields.clock_data.shift_hours_calculated_field import (
    ShiftHoursCalculatedFields,
)
from src.data.schema.clock_schema import ClockSchema

# Daytime and weekday only shift
visit_case_1 = {
    "start_time": Timestamp(year=2023, month=1, day=2, hour=8),
    "end_time": Timestamp(year=2023, month=1, day=2, hour=14),
}

# Nighttime and weekend only shift
visit_case_2 = {
    "start_time": Timestamp(year=2023, month=1, day=7, hour=18),
    "end_time": Timestamp(year=2023, month=1, day=7, hour=22),
}

# Shift that covers all types of hours (spans over two days)
# 22:00 - 23:59 (night) weekday
# 00:00 - 07:00 (night) + 07:00 - 10:00 (day) weekend
visit_case_3 = {
    "start_time": Timestamp(year=2023, month=1, day=6, hour=22),
    "end_time": Timestamp(year=2023, month=1, day=7, hour=10),
}

initial_df = DataFrame(
    {
        "START_TIME": [
            visit_case_1["start_time"],
            visit_case_2["start_time"],
            visit_case_3["start_time"],
        ],
        "END_TIME": [
            visit_case_1["end_time"],
            visit_case_2["end_time"],
            visit_case_3["end_time"],
        ],
    }
)

expected_results_case_1 = {
    "day_hours": 6.0,
    "night_hours": 0.0,
    "weekday_hours": 6.0,
    "weekend_hours": 0.0,
}

expected_results_case_2 = {
    "day_hours": 0.0,
    "night_hours": 4.0,
    "weekday_hours": 0.0,
    "weekend_hours": 4.0,
}

expected_results_case_3 = {
    "day_hours": [0.0, 3.0],
    "night_hours": [2.0, 7.0],
    "weekday_hours": [2.0, 0.0],
    "weekend_hours": [0.0, 10.0],
}

expected_results = {
    "DAY_HOURS": [
        *expected_results_case_3["day_hours"],
        expected_results_case_1["day_hours"],
        expected_results_case_2["day_hours"],
    ],
    "NIGHT_HOURS": [
        *expected_results_case_3["night_hours"],
        expected_results_case_1["night_hours"],
        expected_results_case_2["night_hours"],
    ],
    "WEEKDAY_HOURS": [
        *expected_results_case_3["weekday_hours"],
        expected_results_case_1["weekday_hours"],
        expected_results_case_2["weekday_hours"],
    ],
    "WEEKEND_HOURS": [
        *expected_results_case_3["weekend_hours"],
        expected_results_case_1["weekend_hours"],
        expected_results_case_2["weekend_hours"],
    ],
}


def test_shift_hours_transform() -> None:
    """
    Test that the shift hours transform works as expected
    """
    transformer = ShiftHoursCalculatedFields()
    transformer.to_dict()
    results_df, _ = transformer(initial_df, errors=None, conf=None, env=None)

    for result, expected in zip(
        results_df[ClockSchema.DAY_HOURS].to_list(), expected_results["DAY_HOURS"]
    ):
        assert round(result, 3) == round(expected, 3)

    for result, expected in zip(
        results_df[ClockSchema.NIGHT_HOURS].to_list(),
        expected_results["NIGHT_HOURS"],
    ):
        assert round(result, 3) == round(expected, 3)

    for result, expected in zip(
        results_df[ClockSchema.WEEKDAY_HOURS].to_list(),
        expected_results["WEEKDAY_HOURS"],
    ):
        assert round(result, 3) == round(expected, 3)

    for result, expected in zip(
        results_df[ClockSchema.WEEKEND_HOURS].to_list(),
        expected_results["WEEKEND_HOURS"],
    ):
        assert round(result, 3) == round(expected, 3)
