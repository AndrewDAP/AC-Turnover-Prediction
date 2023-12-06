"""
This module contains the anomaly detection class.
"""
from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

from adtk.visualization import plot
from adtk.detector import QuantileAD

from src.utility.configs.config import Config
from src.utility.environment import Environment
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.data.transforms.transform import DataframeTransform

# Those columns have the same value for an employee regardless of the period
COLUMNS_TO_IGNORE = [
    EmployeeHistorySchema.EMPLOYEE_AGE,
    EmployeeHistorySchema.EMPLOYEE_GENDER,
    EmployeeHistorySchema.EMPLOYEE_TENURE,
    EmployeeHistorySchema.EMPLOYEE_STATE,
    EmployeeHistorySchema.EMPLOYEE_START_ON,
    EmployeeHistorySchema.EMPLOYEE_TERMINATION_DATE,
]

# View plots locally
ANOMALY_DETECTION_PLOTS_FOLDER = ".plots/Anomaly_Detection"


class AnomalyDetector(DataframeTransform):
    """
    This class is use to detect anomalies using the adtk library
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        # Convert the indexes to datetime to avoid errors during the left join
        dataframe[EmployeeHistorySchema.PERIOD_START] = pd.to_datetime(
            dataframe[EmployeeHistorySchema.PERIOD_START]
        )
        dataframe = self.detect_anomalies(dataframe)
        return super().__call__(dataframe, errors, conf, env)

    def detect_anomalies(self, dataframe: DataFrame) -> DataFrame:
        """
        This function detects anomalies for every feature
        It uses the QuantileAD detector with 0.99 and 0.01 values
        Args :
            dataframe: Main dataframe in which we will add anomaly detection columns.
        """
        anomaly_df = self.prepare_dataframe(dataframe=dataframe)
        employee_ids = dataframe[EmployeeHistorySchema.EMPLOYEE_ID].unique()

        # Dataframe that will contain anomalies detection for all employees
        merged_anomalies = pd.DataFrame()

        for employee_id in employee_ids:
            # Filter to keep only 1 employee's data
            data: DataFrame = anomaly_df[
                anomaly_df[EmployeeHistorySchema.EMPLOYEE_ID] == employee_id
            ]

            # Ignore employees if their row count is lower than 2
            if len(data.index) < 2:
                continue

            # Initialize a DataFrame to store anomalies for this employee
            employee_anomalies = pd.DataFrame(
                {"PERIOD_START": data.index.tolist(), "EMPLOYEE_ID": employee_id}
            )

            # Perform anomaly detection on the features
            for column in data.iloc[:, 1:]:
                feature = data[column]
                quantile_ad = QuantileAD(high=0.99, low=0.01)
                anomalies = quantile_ad.fit_detect(feature)

                # Reformat the anomalies into a DataFrame
                anomalies = anomalies.reset_index()
                anomalies.rename(
                    columns={column: f"ANOMALY_DETECTED_{column}"}, inplace=True
                )

                # Add the anomalies to the employee's DataFrame
                employee_anomalies = pd.merge(
                    employee_anomalies,
                    anomalies,
                    on=["PERIOD_START"],
                    how="left",
                )

            # Append the employee's anomalies DataFrame to the list
            merged_anomalies = pd.concat(
                [merged_anomalies, employee_anomalies], ignore_index=True
            )

        # Merge the anomalies with the main dataframe
        dataframe = dataframe.merge(
            merged_anomalies, on=["PERIOD_START", "EMPLOYEE_ID"], how="left"
        )
        dataframe.reset_index(inplace=True)
        return dataframe

    def plot_anomalies(self, dataframe):
        """
        This function plots detected anomalies for a given feature for every employee.
        """
        anomaly_df = self.prepare_dataframe(dataframe=dataframe)
        employee_ids = dataframe[EmployeeHistorySchema.EMPLOYEE_ID].unique()

        for employee_id in employee_ids:
            # Filter to keep only 1 employee's data
            data = anomaly_df[
                anomaly_df[EmployeeHistorySchema.EMPLOYEE_ID] == employee_id
            ]
            for column in data.iloc[:, 1:]:
                feature = data[column]
                quantile_ad = QuantileAD(high=0.99, low=0.01)
                anomalies = quantile_ad.fit_detect(feature)
                plot(
                    feature,
                    anomaly=anomalies,
                    anomaly_color="red",
                    anomaly_tag="marker",
                )
                plt.title(
                    f"Anomaly detections for employee {employee_id} using QuantileAD detector"
                )
                plt.savefig(
                    f"{ANOMALY_DETECTION_PLOTS_FOLDER}/{employee_id}_{column}.png"
                )
                plt.clf()

    def prepare_dataframe(self, dataframe: DataFrame) -> DataFrame:
        """
        Preparing the dataframe for the anomaly detection using adtk
        """
        anomaly_df = dataframe
        anomaly_df = anomaly_df.set_index(EmployeeHistorySchema.PERIOD_START)
        anomaly_df.index = pd.to_datetime(anomaly_df.index)
        anomaly_df = anomaly_df.drop(columns=COLUMNS_TO_IGNORE, errors="ignore")
        return anomaly_df

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
        }
