"""
This module contains a class used to calculate a visit's hour distribution between day, night, weekday and weekend
"""

from typing import Tuple
from pandas import DataFrame, date_range, Timedelta, to_datetime, concat
from tqdm.autonotebook import tqdm
from src.data.transforms.transform import DataframeTransform
from src.utility.configs.config import Config
from src.utility.environment import Environment
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.clock_schema import ClockSchema


class ShiftHoursCalculatedFields(DataframeTransform):
    """
    This class is used to calculate a visit's hour distribution between day, night, weekday and weekend
    """

    DAY_SHIFT_START_STR = " 07:00:00"
    DAY_SHIFT_END_STR = " 17:00:00"
    DATE_RANGE = "DATE_RANGE"

    DAY_SHIFT_START = "DAY_SHIFT_START"
    DAY_SHIFT_END = "DAY_SHIFT_END"
    IN_FIRST_THIRD = "IN_FIRST_THIRD"
    IN_THIRD_THIRD = "IN_THIRD_THIRD"

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(
            desc="Settings time ranges",
            position=4,
            leave=False,
        )

        with tqdm(total=7, position=3, leave=False) as progress_bar:
            progress_bar.set_description("Drop null values")
            dataframe = dataframe.dropna(
                subset=[ClockSchema.START_TIME, ClockSchema.END_TIME]
            )
            progress_bar.update(1)

            progress_bar.set_description("Isolate punches longer than 24 hours")
            too_long_punch_df = dataframe[
                dataframe[ClockSchema.START_TIME].dt.day_of_year
                != dataframe[ClockSchema.END_TIME].dt.day_of_year
            ]

            left_over_dataframe = dataframe[
                dataframe[ClockSchema.START_TIME].dt.day_of_year
                == dataframe[ClockSchema.END_TIME].dt.day_of_year
            ]

            progress_bar.update(1)

            progress_bar.set_description("Calculate time ranges")
            too_long_punch_df[self.DATE_RANGE] = too_long_punch_df.progress_apply(
                lambda row: [
                    date.strftime("%Y-%m-%d")
                    for date in date_range(
                        row[ClockSchema.START_TIME].floor("d"),
                        row[ClockSchema.END_TIME].floor("d"),
                        freq="d",
                    )
                ],
                axis=1,
            )
            progress_bar.update(1)

            progress_bar.set_description(
                "Exploding time ranges for punches less than 24 hours"
            )
            too_long_punch_df = too_long_punch_df.explode(self.DATE_RANGE)
            progress_bar.update(1)

            too_long_punch_df[self.DATE_RANGE] = to_datetime(
                too_long_punch_df[self.DATE_RANGE]
            )

            progress_bar.set_description(
                "Calculating new start and end times for punches less than 24 hours"
            )
            too_long_punch_df[ClockSchema.START_TIME] = too_long_punch_df[
                [
                    ClockSchema.START_TIME,
                    self.DATE_RANGE,
                ]
            ].max(axis=1)

            too_long_punch_df[self.DATE_RANGE] = (
                too_long_punch_df[self.DATE_RANGE]
                + Timedelta(days=1)
                - Timedelta(seconds=1)
            )
            too_long_punch_df[ClockSchema.END_TIME] = too_long_punch_df[
                [
                    ClockSchema.END_TIME,
                    self.DATE_RANGE,
                ]
            ].min(axis=1)
            too_long_punch_df = too_long_punch_df.drop(columns=[self.DATE_RANGE])
            progress_bar.update(1)

            progress_bar.set_description("Recombining dataframes")
            dataframe = concat([too_long_punch_df, left_over_dataframe])
            progress_bar.update(1)

            progress_bar.set_description("Calculating hours")
            dataframe[self.DAY_SHIFT_START] = to_datetime(
                dataframe[ClockSchema.START_TIME].dt.strftime("%Y-%m-%d")
                + self.DAY_SHIFT_START_STR
            )

            dataframe[self.DAY_SHIFT_END] = to_datetime(
                dataframe[ClockSchema.START_TIME].dt.strftime("%Y-%m-%d")
                + self.DAY_SHIFT_END_STR
            )

            dataframe[self.IN_FIRST_THIRD] = (
                dataframe[[self.DAY_SHIFT_START, ClockSchema.END_TIME]].min(axis=1)
                - dataframe[ClockSchema.START_TIME]
            )
            dataframe.loc[
                dataframe[self.IN_FIRST_THIRD] < Timedelta(seconds=0),
                self.IN_FIRST_THIRD,
            ] = Timedelta(seconds=0)

            dataframe[self.IN_THIRD_THIRD] = dataframe[
                ClockSchema.END_TIME
            ] - dataframe[[self.DAY_SHIFT_END, ClockSchema.START_TIME]].max(axis=1)
            dataframe.loc[
                dataframe[self.IN_THIRD_THIRD] < Timedelta(seconds=0),
                self.IN_THIRD_THIRD,
            ] = Timedelta(seconds=0)

            dataframe[ClockSchema.NIGHT_HOURS] = (
                dataframe[self.IN_FIRST_THIRD] + dataframe[self.IN_THIRD_THIRD]
            )

            dataframe[ClockSchema.DAY_HOURS] = dataframe[
                [ClockSchema.END_TIME, self.DAY_SHIFT_END]
            ].min(axis=1) - dataframe[
                [ClockSchema.START_TIME, self.DAY_SHIFT_START]
            ].max(
                axis=1
            )
            dataframe.loc[
                dataframe[ClockSchema.DAY_HOURS] < Timedelta(seconds=0),
                ClockSchema.DAY_HOURS,
            ] = Timedelta(seconds=0)

            dataframe[ClockSchema.NIGHT_HOURS] = (
                dataframe[ClockSchema.NIGHT_HOURS].dt.total_seconds() / 3600
            )
            dataframe[ClockSchema.DAY_HOURS] = (
                dataframe[ClockSchema.DAY_HOURS].dt.total_seconds() / 3600
            )

            dataframe[ClockSchema.WEEKDAY_HOURS] = (
                dataframe[ClockSchema.DAY_HOURS] + dataframe[ClockSchema.NIGHT_HOURS]
            )
            dataframe[ClockSchema.WEEKEND_HOURS] = (
                dataframe[ClockSchema.DAY_HOURS] + dataframe[ClockSchema.NIGHT_HOURS]
            )

            dataframe.loc[
                dataframe[ClockSchema.START_TIME].dt.dayofweek < 5,
                ClockSchema.WEEKEND_HOURS,
            ] = 0

            dataframe.loc[
                dataframe[ClockSchema.START_TIME].dt.dayofweek >= 5,
                ClockSchema.WEEKDAY_HOURS,
            ] = 0
            progress_bar.update(1)

            dataframe = dataframe.drop(
                columns=[
                    self.IN_FIRST_THIRD,
                    self.IN_THIRD_THIRD,
                    self.DAY_SHIFT_START,
                    self.DAY_SHIFT_END,
                ]
            )

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
        }
