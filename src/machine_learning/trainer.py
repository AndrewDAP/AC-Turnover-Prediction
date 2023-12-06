"""
Trainer module
"""
from datetime import datetime
from typing import Literal

# pylint: disable=no-name-in-module
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning import seed_everything, Trainer
from tqdm.autonotebook import tqdm
import torch
import numpy as np
from numpy import floor
import wandb
from src.data.ingestion_pipeline.ingestion_pipeline import IngestionPipeline
from src.machine_learning.data.module.alayacare_data_module import AlayaCareDataModule
from src.utility.configs.config import Config
from src.utility.logger import Logger
from src.utility.environment import Environment
from src.machine_learning.model.model_factory import ModelFactory
from src.machine_learning.data.module.timesnet_data_module import TimesNetDataModule


# pylint: disable=too-many-arguments, too-many-locals
def train(
    ingestion_pipeline: IngestionPipeline = None,
    config: Config = None,
    environment: Environment = None,
    limit: float = 0.1,
    use_k_fold: bool = False,
    accelerator: Literal["gpu", "cpu"] = "gpu",
    use_sweep: bool = False,
) -> None:
    """
    This method trains the model.

    Args:
        ingestion_pipeline (IngestionPipeline): The ingestion pipeline.
        config (Config): The configuration.
        limit (float): The limit of data used for training between 0 and 1. Default is 0.1.
        environment (Environment): The environment.
        use_k_fold (bool): Whether to use K-Fold.
        use_sweep (bool): Whether to wandb sweep.
    """
    seed_everything(hash("alayacare") % 2**32 - 1)
    wandb.login(key=environment.wandb_api)
    logger = Logger(env=environment)

    datamodule = (
        TimesNetDataModule(
            ingestion_pipeline=ingestion_pipeline,
            config=config,
            **config.data_module_args,
        )
        if config.data_module == "TimesNetDataModule"
        else AlayaCareDataModule(
            ingestion_pipeline=ingestion_pipeline,
            config=config,
        )
    )

    datamodule.prepare_data()
    job_type_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    if config.model == "ExplainableBoostingMachine":
        config.model_config["feature_names"] = datamodule.feature_names

    if use_sweep:
        run = wandb.init(project="alayacare")
        for key, item in run.config.items():
            config.model_config[key] = item

    ## K-Fold training loop
    for k in range(config.n_splits):
        model = ModelFactory(
            config=config,
            environment=environment,
            example_input_array=datamodule.dataset[0][0],
            logger=logger,
        ).build()
        if model.is_single_batch_training:
            logger.wandb.init(
                project="alayacare",
                job_type=job_type_id,
                group="Model",
            )

            datamodule.setup("setup_splits", fold_number=k)

            xs_train, ys_train = np.ndarray(
                (0, len(datamodule.feature_names))
            ), np.ndarray((0,))
            for inputs, labels in tqdm(
                datamodule.train_dataloader(),
                desc="Loading Training data",
                leave=False,
                position=3,
            ):
                xs_train = np.concatenate((xs_train, inputs.numpy()))
                ys_train = np.concatenate((ys_train, labels.numpy()))

            xs_train = torch.tensor(xs_train.tolist())[
                : int(floor(limit * len(datamodule.training_dataset)))
            ]
            ys_train = torch.tensor(ys_train.tolist())[
                : int(floor(limit * len(datamodule.training_dataset)))
            ]
            model.fit(xs_train, ys_train)

            for i, validation_batch in tqdm(
                enumerate(datamodule.val_dataloader()),
                desc="Running Validation data",
                leave=False,
                position=3,
            ):
                model.validation_step(validation_batch, i)
            model.on_validation_epoch_end()

            for i, test_batch in tqdm(
                enumerate(datamodule.test_dataloader()),
                desc="Running Test data",
                leave=False,
                position=3,
            ):
                model.test_step(test_batch, i)
            model.on_test_epoch_end()

            model.log_model_summary()

            logger.wandb.finish()
        else:
            wandb_logger = WandbLogger(
                project="alayacare",
                job_type=job_type_id,
                group="Model",
            )

            datamodule.setup("setup_splits", fold_number=k)

            trainer = Trainer(
                logger=wandb_logger,
                log_every_n_steps=config.log_every_n_steps,
                max_epochs=config.n_epochs,
                accelerator=accelerator,
                deterministic="warn",
                limit_train_batches=floor(limit * len(datamodule.training_dataset)),
                limit_val_batches=floor(limit * len(datamodule.validation_dataset)),
                limit_test_batches=floor(limit * len(datamodule.test_dataset)),
            )

            trainer.fit(model, datamodule)

            trainer.test(
                datamodule=datamodule,
                ckpt_path=None,
            )

            wandb.finish()
        if not use_k_fold:
            break
