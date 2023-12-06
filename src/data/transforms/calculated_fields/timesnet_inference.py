"""
This module contains the TimesNetInference class.
"""
from typing import Tuple
from pandas import DataFrame
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.machine_learning.inference_runner import InferenceRunner
from src.machine_learning.data.dataset.timesnet_dataset import TimesNetDataset


class TimesNetInference(DataframeTransform):
    """
    This class is the TimesNet inference transform.

    Args:
        inference_runner (InferenceRunner): The inference runner.
        inference_column_name (str): The name of the inference column.
    """

    def __init__(
        self,
        inference_runner: InferenceRunner = None,
        inference_column_name: str = EmployeeHistorySchema.TIMESNET_INFERENCE,
    ) -> None:
        super().__init__()
        assert inference_runner is not None
        self.inference_runner = inference_runner
        self.inference_column_name = str(inference_column_name)

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataset = TimesNetDataset(
            name=f"TimesNetInferenceDataset For {self.inference_column_name}",
            config=self.inference_runner.run_config,
            dataframe=dataframe,
            **self.inference_runner.run_config.data_module_args,
            is_running_inference=True,
        )

        dataframe[self.inference_column_name] = -1
        dataframe = dataframe.set_index(
            [EmployeeHistorySchema.EMPLOYEE_ID, EmployeeHistorySchema.PERIOD_START]
        ).drop_duplicates()

        idx = dataset.dataframe_index.reset_index(drop=True)[
            [EmployeeHistorySchema.EMPLOYEE_ID, EmployeeHistorySchema.PERIOD_START]
        ].values.tolist()

        required_columns = self.inference_runner.run_config.data_module_args["columns"]

        inference_dataframe = dataframe.loc[idx, required_columns]
        outputs = self.inference_runner.infer(dataset)
        inference_dataframe[self.inference_column_name] = outputs.squeeze().tolist()

        dataframe.loc[
            idx,
            [
                *required_columns,
                self.inference_column_name,
            ],
        ] = inference_dataframe.loc[
            :,
            [
                *required_columns,
                self.inference_column_name,
            ],
        ]
        dataframe = dataframe.reset_index()

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "inference_runner": self.inference_runner.to_dict(),
            "inference_column_name": self.inference_column_name,
        }
