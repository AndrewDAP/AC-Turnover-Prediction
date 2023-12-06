"""
This module is used to generate the y label.
"""

from typing import Literal, Tuple
from pandas import DataFrame, date_range, MultiIndex, Timedelta, Timestamp
from tqdm.autonotebook import tqdm
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.schema.status_schema import StatusSchema
from src.data.schema.y_label_schema import YLabelSchema


def label_policy_30_days(current_date, termination_date) -> bool:
    """
    This function is used to label the employee as churned if the termination date is
    within 30 days of the current date.

    Args:
        current_date (Timestamp): The current date.
        termination_date (Timestamp): The termination date.
    """
    return (
        current_date <= termination_date
        and termination_date - current_date <= Timedelta(days=30)
    )


def label_policy_90_days(current_date, termination_date) -> bool:
    """
    This function is used to label the employee as churned if the termination date is
    within 90 days of the current date.

    Args:
        current_date (Timestamp): The current date.
        termination_date (Timestamp): The termination date.
    """
    return (
        current_date <= termination_date
        and termination_date - current_date <= Timedelta(days=90)
    )


class GenerateYLabelTransform(DataframeTransform):
    """
    This class is used to generate the y label.

    Args:
        label_policy: The label policy.
    """

    def __init__(
        self,
        label_policy: Literal["30Days", "90Days"] = None,
    ) -> None:
        assert label_policy in ["30Days", "90Days"]
        self.label_policy = label_policy
        self.label_function = None

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(desc="Generating Y Label", position=3, leave=False)

        if self.label_policy == "30Days":
            self.label_function = label_policy_30_days
        elif self.label_policy == "90Days":
            self.label_function = label_policy_90_days

        dataframe[YLabelSchema.STATUS_DATE] = dataframe[
            StatusSchema.STATUS_START_DATE
        ].progress_map(lambda x: x.floor("D"))

        # remove duplicates for same day update
        dataframe = dataframe.sort_values(
            by=[StatusSchema.STATUS_START_DATE], ascending=False
        )
        dataframe = dataframe.drop_duplicates(
            subset=[YLabelSchema.STATUS_DATE, StatusSchema.EMPLOYEE_ID], keep="first"
        )

        # keep only terminated status
        dataframe[dataframe[StatusSchema.STATUS_HISTORICAL] != "terminated"] = None
        dataframe = dataframe.dropna(subset=[StatusSchema.STATUS_HISTORICAL])
        dataframe = dataframe[[YLabelSchema.STATUS_DATE, StatusSchema.EMPLOYEE_ID]]

        # create the indexes for the y label dataframe
        last_status = dataframe[YLabelSchema.STATUS_DATE].max()
        first_status = dataframe[YLabelSchema.STATUS_DATE].min()
        indexes = MultiIndex.from_product(
            [
                dataframe[StatusSchema.EMPLOYEE_ID],
                date_range(start=first_status, end=last_status, freq="D"),
            ],
            names=[YLabelSchema.EMPLOYEE_ID, YLabelSchema.PERIOD_START],
        )

        employee_termination_date_mapping = (
            dataframe.groupby(StatusSchema.EMPLOYEE_ID)
            .progress_apply(lambda x: x[YLabelSchema.STATUS_DATE].tolist())
            .to_dict()
        )

        def compute_label(index):
            employee_id = index[0]
            current_date = Timestamp(index[1])

            if employee_id not in employee_termination_date_mapping:
                return None

            dates: list = employee_termination_date_mapping[employee_id]

            for date in dates:
                if self.label_function(current_date, Timestamp(date)):
                    return 1
            return 0

        label_dataframe = DataFrame(index=indexes, columns=[YLabelSchema.Y_LABEL])
        label_dataframe[YLabelSchema.Y_LABEL] = label_dataframe.index.map(compute_label)
        label_dataframe = label_dataframe.dropna().reset_index()

        return super().__call__(label_dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "label_policy": self.label_policy,
        }
