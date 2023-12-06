"""
This module is used to generate the training window id.
"""
from typing import Tuple
from pandas import DataFrame, to_datetime
from tqdm.autonotebook import tqdm
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.schema.employee_history_schema import EmployeeHistorySchema


class GenerateTrainingWindowId(DataframeTransform):
    """
    This class is used to generate the training window id.

    Args:
        window_size (int): The size of the window.
    """

    def __init__(
        self,
        *,
        window_size: int = None,
    ) -> None:
        assert window_size > 0
        self.window_size = window_size

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(desc="Generating training window id", position=3, leave=False)
        dataframe[EmployeeHistorySchema.PERIOD_START] = to_datetime(
            dataframe[EmployeeHistorySchema.PERIOD_START]
        )
        dataframe = dataframe.sort_values(
            by=[EmployeeHistorySchema.EMPLOYEE_ID, EmployeeHistorySchema.PERIOD_START],
            ascending=False,
        )

        # drop the first row for each employee where it is the most recent period
        dataframe = (
            dataframe.groupby(
                by=[EmployeeHistorySchema.EMPLOYEE_ID],
                as_index=False,
            )
            .progress_apply(lambda x: x.iloc[1:])
            .reset_index(
                drop=True,
            )
        )

        # add training window id ignoring the fact that there is there are invalid windows
        dataframe.insert(
            loc=0,
            column=EmployeeHistorySchema.TRAINING_WINDOW_ID.name,
            value=0,
        )

        dataframe[EmployeeHistorySchema.TRAINING_WINDOW_ID] = dataframe.groupby(
            by=[EmployeeHistorySchema.EMPLOYEE_ID],
            as_index=False,
        ).cumcount()

        dataframe[EmployeeHistorySchema.TRAINING_WINDOW_ID] = dataframe[
            EmployeeHistorySchema.TRAINING_WINDOW_ID
        ].progress_apply(lambda x: x // self.window_size)

        # keep only valid windows
        valid_window_size = dataframe.groupby(
            by=[
                EmployeeHistorySchema.EMPLOYEE_ID,
                EmployeeHistorySchema.TRAINING_WINDOW_ID,
            ],
        ).size()
        valid_window_size = valid_window_size[valid_window_size == self.window_size]
        valid_window_size = valid_window_size.reset_index().drop(columns=[0])

        dataframe = dataframe.merge(
            right=valid_window_size,
            how="inner",
            on=[
                EmployeeHistorySchema.EMPLOYEE_ID,
                EmployeeHistorySchema.TRAINING_WINDOW_ID,
            ],
        ).drop(columns=[EmployeeHistorySchema.TRAINING_WINDOW_ID])

        # reindex with the proper training window id
        dataframe = dataframe.reset_index(drop=True).reset_index()
        dataframe = dataframe.rename(
            columns={"index": EmployeeHistorySchema.TRAINING_WINDOW_ID.name}
        )
        dataframe[EmployeeHistorySchema.TRAINING_WINDOW_ID] = dataframe[
            EmployeeHistorySchema.TRAINING_WINDOW_ID
        ].progress_apply(lambda x: x // self.window_size)

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "window_size": self.window_size,
        }
