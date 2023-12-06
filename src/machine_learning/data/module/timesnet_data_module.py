# pylint: disable=duplicate-code
"""
This module contains the TimesNet data module.
"""
from typing import Literal, Optional
from numpy import zeros, arange
from torch import Tensor, from_numpy, reshape
from torch.utils.data import DataLoader, Dataset, TensorDataset
from pytorch_lightning import LightningDataModule
from sklearn.model_selection import StratifiedKFold, train_test_split
from src.utility.configs.config import Config
from src.data.ingestion_pipeline.ingestion_pipeline import IngestionPipeline
from src.data.ingestion_pipeline.ingestion_pipeline_stages import (
    IngestionPipelineStages,
)
from src.machine_learning.data.tensor_schema import TensorSchema
from src.machine_learning.data.over_sampler import OverSampler
from src.machine_learning.data.dataset.timesnet_dataset import TimesNetDataset


class TimesNetDataModule(LightningDataModule):
    """
    This class is the TimesNet data module.

    Args:
        ingestion_pipeline (IngestionPipeline): The ingestion pipeline.
        config (Config): The experiment configuration.
        sequence_length (int): The sequence length.
    """

    def __init__(
        self,
        *,
        ingestion_pipeline: IngestionPipeline,
        config: Config,
        sequence_length: int = None,
        columns: [str] = None,
    ):
        super().__init__()
        self.ingestion_pipeline = ingestion_pipeline
        self.config = config
        self.fold_number = 0
        self.sequence_length = sequence_length
        self.columns = columns

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
    def feature_names(self) -> [str]:
        """
        Give the feature names in the dataset.
        """
        return self.dataset.features_dataframe.columns[:-1].tolist()

    def prepare_data(self) -> "AlayaCareDataModule":
        """
        This method prepares the data.
        """
        self.ingestion_pipeline.build_pipeline()
        self.ingestion_pipeline.run_pipeline(
            stage_name=IngestionPipelineStages.TRAINING_EMPLOYEE_HISTORY_STAGE
        )
        self.dataset = TimesNetDataset(
            dataframe=self.ingestion_pipeline.dataframes[
                IngestionPipelineStages.TRAINING_EMPLOYEE_HISTORY_STAGE
            ],
            config=self.config,
            sequence_length=self.sequence_length,
            columns=self.columns,
        )
        TensorSchema.set_mapping(self.dataset.features_dataframe)

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
            features, labels = self.__generate_train_test_split()
            self.__generate_cross_validation_split(features, labels)

        return self

    def train_dataloader(self) -> DataLoader:
        """
        This method returns the training dataloader.
        """
        train_x, train_y = self.training_dataset[:]
        train_x, train_y = self.over_sample(train_x, train_y)
        train_dataset = TensorDataset(
            train_x,
            train_y,
        )
        return DataLoader(
            dataset=train_dataset,
            batch_size=self.config.batch_size,
            shuffle=True,
        )

    def over_sample(self, x: Tensor, y: Tensor):
        """
        This method performs oversampling.

        Args:
            x (Tensor): The features.
            y (Tensor): The labels.
        """
        x = x.reshape(x.shape[0], -1)
        x, y = OverSampler(
            name=self.config.oversampler, **self.config.oversampler_args
        ).fit_resample(x.numpy(), y.numpy())
        x, y = from_numpy(x), from_numpy(y)
        x = reshape(x, (x.shape[0], -1, len(self.feature_names)))
        return x, y

    def val_dataloader(self) -> DataLoader:
        """
        This method returns the validation dataloader.
        """
        validation_x, validation_y = self.validation_dataset[:]
        validation_x, validation_y = self.over_sample(validation_x, validation_y)
        validation_dataset = TensorDataset(
            validation_x,
            validation_y,
        )
        return DataLoader(
            dataset=validation_dataset,
            batch_size=self.config.batch_size,
        )

    def test_dataloader(self) -> DataLoader:
        """
        This method returns the test dataloader.
        """
        return DataLoader(
            dataset=self.test_dataset,
            batch_size=self.config.batch_size,
        )

    def __generate_train_test_split(self):
        """
        This method generates the train test split.
        """
        features, y_labels = self.dataset[:]
        train_idx, test_idx, *_ = train_test_split(
            arange(len(y_labels)),
            y_labels,
            test_size=0.20,
            random_state=self.config.split_seed,
            stratify=y_labels,
        )

        self.test_dataset = TensorDataset(
            features[test_idx],
            y_labels[test_idx],
        )

        return features[train_idx], y_labels[train_idx]

    def __generate_cross_validation_split(self, features, y_labels) -> None:
        """
        This method generates the cross validation split.

        Args:
            features: The features.
            y_labels: The labels.
        """
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

        self.training_dataset = TensorDataset(
            features[training_indexes],
            y_labels[training_indexes],
        )
        self.validation_dataset = TensorDataset(
            features[validation_indexes],
            y_labels[validation_indexes],
        )
