"""
This module contains the TimesNetDataset class.
"""

from typing import Optional
from pandas import DataFrame, Timedelta
from numpy import float64, ndarray, pad, nan_to_num, concatenate
from torch.utils.data.dataset import Dataset
from torch import is_tensor, from_numpy
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.utility.configs.config import Config


class TimesNetDataset(Dataset):
    """
    This class is the dataset for the TimesNet model.

    Args:
        name: The name of the dataset.
        dataframe: The dataframe containing the data.
        config: The experiment configuration.
        sequence_length: The length of the sequence.
        columns: The columns to use as features.
        is_running_inference: Whether this is running inference.
    """

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        dataframe: DataFrame = None,
        config: Config = None,
        sequence_length: int = None,
        columns: [str] = None,
        is_running_inference: bool = False,
    ) -> None:
        assert config is not None
        assert dataframe is not None
        assert sequence_length is not None
        super().__init__()
        self.config = config
        self.name = name
        self.sequence_length: int = sequence_length
        self.is_running_inference: bool = is_running_inference
        self.columns = [
            str(column) for column in columns if column != EmployeeHistorySchema.Y_LABEL
        ]

        dataframe = dataframe.sort_values(
            [EmployeeHistorySchema.EMPLOYEE_ID, EmployeeHistorySchema.PERIOD_START]
        )
        if self.is_running_inference:
            self.__inference_init(dataframe)
        else:
            self.__init(dataframe)

    def __inference_init(self, dataframe):
        self.features_dataframe = dataframe.set_index(
            [EmployeeHistorySchema.EMPLOYEE_ID, EmployeeHistorySchema.PERIOD_START]
        )[self.columns]
        self.dataframe_index = (
            dataframe[
                [
                    EmployeeHistorySchema.EMPLOYEE_ID,
                    EmployeeHistorySchema.PERIOD_START,
                ]
            ]
            .groupby(EmployeeHistorySchema.EMPLOYEE_ID)
            .apply(lambda x: x.iloc[self.sequence_length :])
        )

    def __init(self, dataframe):
        self.features_dataframe = dataframe.set_index(
            [EmployeeHistorySchema.EMPLOYEE_ID, EmployeeHistorySchema.PERIOD_START]
        )[[*self.columns, EmployeeHistorySchema.Y_LABEL]]
        self.dataframe_index = (
            dataframe[
                [
                    EmployeeHistorySchema.EMPLOYEE_ID,
                    EmployeeHistorySchema.PERIOD_START,
                    EmployeeHistorySchema.Y_LABEL,
                ]
            ]
            .groupby(EmployeeHistorySchema.EMPLOYEE_ID)
            .apply(lambda x: x.iloc[self.sequence_length :])
        )
        self.dataframe_index = self.dataframe_index.drop(
            self.dataframe_index[
                self.dataframe_index[EmployeeHistorySchema.Y_LABEL] == 0
            ]
            .sample(frac=0.75)
            .index
        )
        self.dataframe_index = self.dataframe_index.drop(
            columns=EmployeeHistorySchema.Y_LABEL
        )

    def __getitem__(self, idx):
        if isinstance(idx, int):
            idx = [idx]

        if is_tensor(idx):
            idx = idx.tolist()

        if isinstance(idx, slice):
            idx = list(range(*idx.indices(len(self))))

        if self.is_running_inference:
            features, target = self.__inference_get_item(idx)
        else:
            features, target = self.__get_item(idx)

        return from_numpy(features).float(), from_numpy(target).float()

    def __inference_get_item(self, idx):
        features = ndarray((0, self.sequence_length, len(self.columns)), dtype=float64)

        target = ndarray(shape=(len(idx),), dtype=float64)
        for i in idx:
            employee, date = tuple(self.dataframe_index.iloc[i])
            values = (
                self.features_dataframe.loc[employee]
                .loc[date - Timedelta(days=self.sequence_length - 1) : date]
                .to_numpy()
            )
            x = values[: self.sequence_length]
            if x.shape[0] < self.sequence_length:
                x = pad(
                    x, ((self.sequence_length - x.shape[0], 0), (0, 0)), mode="mean"
                )
            features = concatenate([features, nan_to_num(x).reshape((1, *x.shape))])
            if len(idx) == 1:
                features = features.squeeze()
        return features, target

    def __get_item(self, idx):
        features = ndarray(
            shape=(len(idx), self.sequence_length, len(self.columns)), dtype=float64
        )
        target = ndarray(shape=(len(idx),), dtype=float64)
        for i in idx:
            employee, date = tuple(self.dataframe_index.iloc[i])
            values = (
                self.features_dataframe.loc[employee]
                .loc[date - Timedelta(days=self.sequence_length - 1) : date]
                .to_numpy()
            )
            x = values[: self.sequence_length, :-1]
            if x.shape[0] < self.sequence_length:
                x = pad(
                    x, ((self.sequence_length - x.shape[0], 0), (0, 0)), mode="mean"
                )

            features[i] = nan_to_num(x)
            target[i] = nan_to_num(values[-1, -1])
        return features, target

    def __len__(self):
        return len(self.dataframe_index)

    def __repr__(self):
        return f"TimesNetDataset(name={self.name})"
