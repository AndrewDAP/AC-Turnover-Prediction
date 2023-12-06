"""
This module contains the AlayaCareDataset class.
"""

from typing import Optional
from pandas import DataFrame
from numpy import float64, ndarray
from tqdm.autonotebook import tqdm
from torch.utils.data.dataset import Dataset
from torch import is_tensor
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.utility.configs.config import Config


class AlayaCareDataset(Dataset):
    """
    This class is the dataset for the AlayaCare data.

    Args:
        name: The name of the dataset.
        dataframe: The dataframe containing the data.
        transform: The transform to apply to the features.
        target_transform: The transform to apply to the target.
        config: The experiment configuration.
        is_running_inference: Whether this is running inference.
    """

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        dataframe: DataFrame = None,
        transform=None,
        target_transform=None,
        config: Config = None,
        is_running_inference: bool = False,
    ) -> None:
        assert dataframe is not None
        assert config is not None
        super().__init__()
        self.is_running_inference: bool = is_running_inference

        tqdm.pandas(
            desc=f"Constructing {name} dataset"
            if name is not None
            else "Constructing dataset"
        )
        dataframe = dataframe.reset_index(drop=True).reset_index()
        dataframe = dataframe.rename(
            columns={"index": EmployeeHistorySchema.TRAINING_WINDOW_ID}
        )
        dataframe[EmployeeHistorySchema.TRAINING_WINDOW_ID] = dataframe[
            EmployeeHistorySchema.TRAINING_WINDOW_ID
        ].progress_apply(lambda x: x // config.training_window_size)
        if not is_running_inference:
            dataframe = dataframe.set_index(EmployeeHistorySchema.TRAINING_WINDOW_ID)
        self.transform = transform
        self.target_transform = target_transform
        self.dataframe = dataframe
        self.config = config

    def __getitem__(self, idx):
        if isinstance(idx, int):
            idx = [idx]

        if is_tensor(idx):
            idx = idx.tolist()

        dataframe_slice = self.dataframe.loc[idx]
        features = (
            dataframe_slice.drop(
                columns=[
                    EmployeeHistorySchema.Y_LABEL,
                    EmployeeHistorySchema.EMPLOYEE_ID,
                    EmployeeHistorySchema.PERIOD_START,
                ]
            )
            .to_numpy()
            .squeeze()
            .astype(float64)
        )
        if self.is_running_inference:
            target = ndarray((len(features),))
        else:
            target = (
                dataframe_slice[EmployeeHistorySchema.Y_LABEL]
                .groupby(dataframe_slice.index)
                .max()
                .to_numpy()
                .squeeze()
                .astype(float64)
            )

        if self.transform is not None:
            features = self.transform(features)
        if self.target_transform is not None:
            target = self.target_transform(target)
        return features, target

    def __len__(self):
        return len(self.dataframe) // self.config.training_window_size
