"""
This module contains the AlayaCare data module.
"""
from typing import Literal, Optional
from numpy import zeros, arange
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from torch import Tensor
from torch.utils.data import DataLoader, Dataset, TensorDataset
from pytorch_lightning import LightningDataModule
from sklearn.model_selection import StratifiedKFold, train_test_split
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline import IngestionPipeline
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)
from src.machine_learning.data.dataset.alayacare_dataset import AlayaCareDataset
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.machine_learning.data.tensor_schema import TensorSchema
from src.machine_learning.data.over_sampler import OverSampler


class AlayaCareDataModule(LightningDataModule):
    """
    This class is the AlayaCare data module.

    Args:
        ingestion_pipeline (IngestionPipeline): The ingestion pipeline.
        config (Config): The experiment configuration.
        k_fold_number (int): The k-fold number.
    """

    def __init__(
        self,
        *,
        ingestion_pipeline: IngestionPipeline,
        config: Config,
    ):
        super().__init__()
        self.ingestion_pipeline = ingestion_pipeline
        self.config = config
        self.fold_number = 0

        self.dataset: Optional[Dataset] = None
        self.training_dataset: Optional[Dataset] = None
        self.validation_dataset: Optional[Dataset] = None
        self.test_dataset: Optional[Dataset] = None
        self.save_hyperparameters(
            {
                "config": config.to_dict(),
                "ingestion_pipeline": ingestion_pipeline.to_dict(),
            }
        )

    @property
    def n_genders(self) -> int:
        """
        Give the number of unique gender in the dataset.
        """
        if self.dataset is None:
            return 0
        return len(
            self.dataset.dataframe[EmployeeHistorySchema.EMPLOYEE_GENDER].unique()
        )

    @property
    def n_states(self) -> int:
        """
        Give the number of unique states in the dataset.
        """
        if self.dataset is None:
            return 0
        return len(
            self.dataset.dataframe[EmployeeHistorySchema.EMPLOYEE_STATE].unique()
        )

    @property
    def n_features(self) -> int:
        """
        Give the number of features in the dataset.
        """
        if self.dataset is None:
            return 0
        sample_x, _ = self.dataset[0]
        return sample_x.shape[-1]

    @property
    def n_classes(self) -> int:
        """
        Give the number of features in the dataset.
        """
        return 1

    @property
    def feature_names(self) -> [str]:
        """
        Give the feature names in the dataset.
        """
        return self.dataset.dataframe.columns[2:-1]

    def prepare_data(self) -> "AlayaCareDataModule":
        """
        This method prepares the data.
        """
        self.ingestion_pipeline.build_pipeline()
        self.ingestion_pipeline.run_pipeline(
            stage_name=IngestionPipelineStages.TRAINING_EMPLOYEE_HISTORY_STAGE
        )
        dataframe = self.ingestion_pipeline.dataframes[
            IngestionPipelineStages.TRAINING_EMPLOYEE_HISTORY_STAGE
        ]

        dataframe = dataframe[
            [
                EmployeeHistorySchema.TRAINING_WINDOW_ID,
                EmployeeHistorySchema.EMPLOYEE_ID,
                EmployeeHistorySchema.PERIOD_START,
                *[
                    column
                    for column in dataframe.columns
                    if column
                    not in [
                        EmployeeHistorySchema.TRAINING_WINDOW_ID,
                        EmployeeHistorySchema.EMPLOYEE_ID,
                        EmployeeHistorySchema.PERIOD_START,
                        EmployeeHistorySchema.Y_LABEL,
                    ]
                ],
                EmployeeHistorySchema.Y_LABEL,
            ]
        ]

        dataframe = dataframe.set_index(EmployeeHistorySchema.TRAINING_WINDOW_ID)
        if self.config.limit_dataframe_size is not None:
            dataframe = dataframe.iloc[: self.config.limit_dataframe_size]
        self.dataset = AlayaCareDataset(
            dataframe=dataframe,
            transform=Tensor,
            target_transform=Tensor,
            config=self.config,
        )
        TensorSchema.set_mapping(self.dataset.dataframe)

        super().prepare_data()
        return self

    def setup(
        self, stage: Literal = None, fold_number: int = None
    ) -> "AlayaCareDataModule":
        """
        This method sets up the data module.
        """
        if stage == "setup_splits":
            self.fold_number = fold_number
            training_dataframe = self.__generate_train_test_split()
            self.__generate_cross_validation_split(training_dataframe)

        return self

    def train_dataloader(self) -> DataLoader:
        """
        This method returns the training dataloader.
        """
        train_x, train_y = self.training_dataset[:]
        train_x, train_y = OverSampler(
            name=self.config.oversampler, **self.config.oversampler_args
        ).fit_resample(train_x, train_y)
        train_dataset = TensorDataset(
            Tensor(train_x.tolist()),
            Tensor(train_y.tolist()),
        )
        return DataLoader(
            dataset=train_dataset,
            batch_size=self.config.batch_size,
            shuffle=True,
            num_workers=self.config.num_workers,
        )

    def val_dataloader(self) -> DataLoader:
        """
        This method returns the validation dataloader.
        """
        validation_x, validation_y = self.validation_dataset[:]
        validation_x, validation_y = OverSampler(
            name=self.config.oversampler, **self.config.oversampler_args
        ).fit_resample(validation_x, validation_y)
        validation_dataset = TensorDataset(
            Tensor(validation_x.tolist()),
            Tensor(validation_y.tolist()),
        )
        return DataLoader(
            dataset=validation_dataset,
            batch_size=self.config.batch_size,
            num_workers=self.config.num_workers,
        )

    def test_dataloader(self) -> DataLoader:
        """
        This method returns the test dataloader.
        """
        test_x, test_y = self.test_dataset[:]
        test_dataset = TensorDataset(
            Tensor(test_x.tolist()),
            Tensor(test_y.tolist()),
        )
        return DataLoader(
            dataset=test_dataset,
            batch_size=self.config.batch_size,
            num_workers=self.config.num_workers,
        )

    def __generate_train_test_split(self) -> DataFrame:
        """
        This method generates the train test split.
        """
        y_labels = (
            self.dataset.dataframe[EmployeeHistorySchema.Y_LABEL]
            .groupby(self.dataset.dataframe.index)
            .max()
            .values
        )
        train_idx, test_idx, *_ = train_test_split(
            arange(len(y_labels)),
            y_labels,
            test_size=0.20,
            random_state=self.config.split_seed,
            stratify=y_labels,
        )

        self.test_dataset = AlayaCareDataset(
            name=f"Test for fold {self.fold_number}",
            dataframe=self.dataset.dataframe.loc[test_idx],
            transform=self.dataset.transform,
            target_transform=self.dataset.target_transform,
            config=self.config,
        )

        training_dataframe = self.dataset.dataframe.loc[train_idx]
        training_dataframe = training_dataframe.reset_index(drop=True).reset_index()
        training_dataframe = training_dataframe.rename(
            columns={"index": EmployeeHistorySchema.TRAINING_WINDOW_ID}
        )
        tqdm.pandas(desc="Indexing training dataframe", position=3, leave=True)
        training_dataframe[
            EmployeeHistorySchema.TRAINING_WINDOW_ID
        ] = training_dataframe[EmployeeHistorySchema.TRAINING_WINDOW_ID].progress_apply(
            lambda x: x // self.config.training_window_size
        )
        training_dataframe = training_dataframe.set_index(
            EmployeeHistorySchema.TRAINING_WINDOW_ID
        )
        return training_dataframe

    def __generate_cross_validation_split(self, training_dataframe: DataFrame) -> None:
        """
        This method generates the cross validation split.

        Args:
            training_dataframe (DataFrame): The training dataframe.
        """
        y_labels = (
            training_dataframe[EmployeeHistorySchema.Y_LABEL]
            .groupby(training_dataframe.index)
            .max()
            .values
        )

        k_fold = StratifiedKFold(
            n_splits=self.config.n_splits,
            shuffle=True,
            random_state=self.config.split_seed,
        )

        all_splits = list(
            k_fold.split(
                zeros(len(y_labels)),
                y=y_labels,
            ),
        )

        training_indexes, validation_indexes = all_splits[self.fold_number]
        training_indexes, validation_indexes = (
            training_indexes.tolist(),
            validation_indexes.tolist(),
        )

        self.training_dataset = AlayaCareDataset(
            name=f"Training for fold {self.fold_number}",
            dataframe=training_dataframe.loc[training_indexes],
            transform=self.dataset.transform,
            target_transform=self.dataset.target_transform,
            config=self.config,
        )
        self.validation_dataset = AlayaCareDataset(
            name=f"Validation for fold {self.fold_number}",
            dataframe=training_dataframe.loc[validation_indexes],
            transform=self.dataset.transform,
            target_transform=self.dataset.target_transform,
            config=self.config,
        )
