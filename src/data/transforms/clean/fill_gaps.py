"""
Transformation that fills in missing rows with padding in the EmployeeHistory dataframe
"""


from typing import Optional, Tuple
from pandas import DataFrame, date_range
from tqdm.autonotebook import tqdm
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.feature_type import FeatureType
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.data.transforms.transform import DataframeTransform
from src.utility.configs.config import Config
from src.utility.environment import Environment


class FillGaps(DataframeTransform):
    """
    Transformation that fills in missing rows with padding in the EmployeeHistory dataframe

    Args:
        period_duration: The period duration to fill in the gaps with
    """

    PERIOD_START_2 = "PERIOD_START_2"
    CAREER_START = "CAREER_START"
    CAREER_END = "CAREER_END"
    IS_ORIGINAL_ROW = "IS_ORIGINAL_ROW"

    def __init__(
        self,
        period_duration: Optional[str] = "1D",
    ) -> None:
        self.period_duration = period_duration

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        with tqdm(
            total=7,
            desc=f"Filling gaps with period_duration {self.period_duration}",
            position=3,
            leave=False,
        ) as progress_bar:
            original_dataframe = dataframe
            original_dataframe[self.IS_ORIGINAL_ROW] = 1

            dataframe = dataframe[
                [
                    EmployeeHistorySchema.PERIOD_START,
                    EmployeeHistorySchema.EMPLOYEE_START_ON,
                    EmployeeHistorySchema.EMPLOYEE_ID,
                    EmployeeHistorySchema.EMPLOYEE_TERMINATION_DATE,
                    EmployeeHistorySchema.EMPLOYEE_FIRST_VISIT,
                ]
            ]

            progress_bar.set_description(
                f"Filling gaps : Copying {EmployeeHistorySchema.PERIOD_START} to {self.PERIOD_START_2}"
            )
            dataframe[self.PERIOD_START_2] = dataframe[
                EmployeeHistorySchema.PERIOD_START
            ].copy()
            progress_bar.update(1)

            progress_bar.set_description(
                f"Filling gaps : Calculating {EmployeeHistorySchema.EMPLOYEE_START_ON} and"
                + f" {EmployeeHistorySchema.EMPLOYEE_TERMINATION_DATE}"
            )
            dataframe = (
                dataframe.groupby([EmployeeHistorySchema.EMPLOYEE_ID])
                .aggregate(
                    {
                        EmployeeHistorySchema.PERIOD_START: "min",
                        EmployeeHistorySchema.EMPLOYEE_START_ON: "min",
                        self.PERIOD_START_2: "max",
                        EmployeeHistorySchema.EMPLOYEE_TERMINATION_DATE: "max",
                        EmployeeHistorySchema.EMPLOYEE_FIRST_VISIT: "max",
                    }
                )
                .reset_index()
            )
            progress_bar.update(1)

            progress_bar.set_description(
                f"Filling gaps : Calculating {self.CAREER_START} and {self.CAREER_END}"
            )
            dataframe[self.CAREER_START] = dataframe[
                [
                    EmployeeHistorySchema.PERIOD_START,
                    EmployeeHistorySchema.EMPLOYEE_START_ON,
                ]
            ].min(axis=1)
            dataframe[self.CAREER_END] = dataframe[
                [
                    self.PERIOD_START_2,
                    EmployeeHistorySchema.EMPLOYEE_TERMINATION_DATE,
                ]
            ].max(axis=1)
            dataframe = dataframe[
                [
                    EmployeeHistorySchema.EMPLOYEE_ID,
                    self.CAREER_START,
                    self.CAREER_END,
                ]
            ]
            progress_bar.update(1)

            progress_bar.set_description(
                f"Filling gaps : Calculating {EmployeeHistorySchema.PERIOD_START} for each employee"
            )
            mapping_employee_id_to_date_range = {}

            def update_mapping_employee_id_to_date_range(row):
                mapping_employee_id_to_date_range[
                    row[EmployeeHistorySchema.EMPLOYEE_ID]
                ] = date_range(
                    start=row[self.CAREER_START],
                    end=row[self.CAREER_END],
                    freq=self.period_duration,
                )

            dataframe = dataframe.apply(
                update_mapping_employee_id_to_date_range, axis=1
            )
            dataframe = DataFrame.from_dict(
                mapping_employee_id_to_date_range, orient="index"
            ).stack()
            dataframe = dataframe.reset_index().drop(columns=["level_1"])
            dataframe.columns = [
                EmployeeHistorySchema.EMPLOYEE_ID,
                EmployeeHistorySchema.PERIOD_START,
            ]
            progress_bar.update(1)

            progress_bar.set_description(
                "Filling gaps : Join filled gaps to original dataframe"
            )
            dataframe = dataframe.merge(
                original_dataframe,
                on=[
                    EmployeeHistorySchema.EMPLOYEE_ID,
                    EmployeeHistorySchema.PERIOD_START,
                ],
                how="left",
            )
            progress_bar.update(1)

            progress_bar.set_description(
                "Filling gaps : Fill missing values with previous values for demographics"
            )
            demographics_columns = [
                col.name
                for col in EmployeeHistorySchema.columns
                if (
                    (col.feature_type == FeatureType.DEMOGRAPHIC)
                    and (
                        col.name != EmployeeHistorySchema.EMPLOYEE_TENURE.name
                    )  # EMPLOYEE_TENURE is computed after FillGaps
                )
            ]
            dataframe = dataframe.sort_values(
                [EmployeeHistorySchema.EMPLOYEE_ID, EmployeeHistorySchema.PERIOD_START]
            )
            dataframe = dataframe.set_index(
                [EmployeeHistorySchema.EMPLOYEE_ID, EmployeeHistorySchema.PERIOD_START]
            )
            dataframe[demographics_columns] = dataframe.groupby(level=0).ffill()[
                demographics_columns
            ]
            dataframe[demographics_columns] = dataframe.groupby(level=0).bfill()[
                demographics_columns
            ]
            dataframe = dataframe.reset_index()
            progress_bar.update(1)

            progress_bar.set_description(
                "Filling gaps : Fill missing values with 0 for behavioral totals"
            )
            behavioral_columns = [
                col.name
                for col in EmployeeHistorySchema.columns
                if col.feature_type == FeatureType.BEHAVIORAL
            ]

            dataframe.loc[dataframe[self.IS_ORIGINAL_ROW] != 1, behavioral_columns] = 0
            progress_bar.update(1)

            dataframe = dataframe.drop(columns=[self.IS_ORIGINAL_ROW])
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "period_duration": self.period_duration,
        }
