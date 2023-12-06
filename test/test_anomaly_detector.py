"""
This module contains the tests for the AnomalyDetector class
"""
from datetime import datetime
import pandas as pd
from src.data.transforms.analysis.anomaly_detector import AnomalyDetector

# Mock data for testing.
mock_df = pd.DataFrame(
    {
        "EMPLOYEE_ID": [
            100,
            100,
            100,
            100,
            101,
            101,
            101,
            101,
        ],
        "PERIOD_START": [
            datetime(2019, 1, 1),
            datetime(2019, 1, 2),
            datetime(2019, 1, 3),
            datetime(2019, 1, 4),
            datetime(2019, 1, 1),
            datetime(2019, 1, 2),
            datetime(2019, 1, 3),
            datetime(2019, 1, 4),
        ],
        "EMPLOYEE_AGE": [  # Should be ignored in anomaly detection
            51,
            51,
            51,
            51,
            20,
            20,
            20,
            20,
        ],
        "VISIT_HOURS_PER_PERIOD": [8, 4, 8, 16, 10, 10, 12, 6],
        "AVERAGE_AGE_OF_PATIENTS_PER_PERIOD": [60, 60, 60, 60, 70, 74, 67, 100],
    }
)

expected_column_names = [
    "ANOMALY_DETECTED_VISIT_HOURS_PER_PERIOD",
    "ANOMALY_DETECTED_AVERAGE_AGE_OF_PATIENTS_PER_PERIOD",
]


def test_anomaly_detector():
    """
    This method tests if the anomaly detector class adds an anomaly column for each
    feature
    """
    # Create an instance of AnomalyDetector
    transformer = AnomalyDetector()
    transformer.to_dict()

    # Call the transformer
    transformed_df, _ = transformer(mock_df, errors=None, conf=None, env=None)

    # Verify that columns were added
    assert transformed_df.shape[1] > mock_df.shape[1]

    assert "ANOMALY_DETECTION_EMPLOYEE_AGE" not in transformed_df.columns.to_list()

    for column_name in expected_column_names:
        # Verify that added column names are in the right format
        assert column_name in transformed_df.columns.to_list()
        # Verify that the values in the anomaly columns are only true or false
        assert transformed_df[column_name].isin([True, False]).all()
