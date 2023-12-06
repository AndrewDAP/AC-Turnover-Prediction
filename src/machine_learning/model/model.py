"""
A base for a model
"""

from abc import abstractmethod
from typing import Dict, Tuple, Union, Optional
from numpy import ndarray, float64
from pytorch_lightning import LightningModule

# pylint: disable=no-name-in-module
from torch import nn, Tensor, optim, flatten, cat, from_numpy
from torchmetrics.classification import (
    BinaryAccuracy,
    BinaryConfusionMatrix,
    BinaryF1Score,
    BinaryPrecision,
    BinaryRecall,
    BinarySpecificity,
    BinaryROC,
    BinaryAUROC,
)
from wandb import Histogram, Image
from src.utility.configs.config import Config
from src.utility.logger import Logger
from src.utility.environment import Environment


class Model(LightningModule):
    """
    This class implements a perceptron model.

    Args:
        model_config (Config): The experiment configuration.
        loss_function (nn.Module): The loss function.
        example_input_array (Tensor): The example input array.
        environment (Environment): The environment.
        custom_logger (Optional[Any]): The custom logger.
    """

    def __init__(
        self,
        *,
        model_config: Config,
        environment: Environment = None,
        loss_function: nn.Module = None,
        example_input_array: Tensor = None,
        custom_logger: Optional[Logger] = None,
        is_single_batch_training: bool = None,
    ):
        assert model_config is not None
        assert example_input_array is not None
        assert environment is not None
        assert is_single_batch_training is not None
        super().__init__()
        self.is_single_batch_training = is_single_batch_training
        self.custom_logger = custom_logger.wandb if custom_logger is not None else None
        self.config = model_config
        self.environment = environment
        self.loss_function = (
            loss_function if loss_function is not None else nn.BCELoss()
        )
        self.validation_step_outputs = []
        self.example_input_tensor = example_input_array

        self.test_confusion_matrix = BinaryConfusionMatrix()

        self.training_accuracy = BinaryAccuracy()
        self.validation_accuracy = BinaryAccuracy()
        self.test_accuracy = BinaryAccuracy()

        self.training_f1_score = BinaryF1Score()
        self.validation_f1_score = BinaryF1Score()
        self.test_f1_score = BinaryF1Score()

        self.training_precision = BinaryPrecision()
        self.validation_precision = BinaryPrecision()
        self.test_precision = BinaryPrecision()

        self.training_recall = BinaryRecall()
        self.validation_recall = BinaryRecall()
        self.test_recall = BinaryRecall()

        self.training_specificity = BinarySpecificity()
        self.validation_specificity = BinarySpecificity()
        self.test_specificity = BinarySpecificity()

        self.test_roc = BinaryROC()

        self.training_auroc = BinaryAUROC()
        self.validation_auroc = BinaryAUROC()
        self.test_auroc = BinaryAUROC()

    @property
    def example_input_array(self) -> Optional[Union[Tensor, Tuple, Dict]]:
        """
        This property returns the example input array.
        """
        return self.example_input_tensor

    def loss(self, batch: Tuple[Union[Tensor, ndarray], Union[Tensor, ndarray]]):
        """
        This method calculates the loss.
        """
        x, y = batch
        logits: Union[Tensor, ndarray] = self(x)
        loss = self.loss_function(logits, y)
        if isinstance(logits, ndarray):
            logits = from_numpy(logits.astype(float64))
        if isinstance(y, ndarray):
            y = from_numpy(y.astype(float64))
        predictions = logits > self.config.cutoff

        return logits, predictions, loss, y

    def fit(self, x: Union[ndarray, Tensor], y: Union[ndarray, Tensor]):
        """
        This method performs one batch training.

        Args:
            x (Union[ndarray, Tensor]): The input tensor.
            y (Union[ndarray, Tensor]): The output tensor.
        """

    def predict(self, *args, **kwargs):
        """
        This method predicts the output.
        """
        return self(*args, **kwargs)

    def training_step(self, batch: Tuple[Tensor, Tensor], _: int):
        """
        This method performs a training step.
        """
        logits, predictions, loss, y = self.loss(batch)

        self.log("training/loss", loss)

        self.training_accuracy.update(predictions, y)
        self.training_f1_score.update(predictions, y)
        self.training_precision.update(predictions, y)
        self.training_recall.update(predictions, y)
        self.training_specificity.update(predictions, y)
        self.training_auroc.update(logits, y.long())
        return loss

    def on_train_epoch_end(self) -> None:
        """
        This method is called at the end of the training epoch.
        """
        self.log("training/accuracy", self.training_accuracy.compute())
        self.training_accuracy.reset()
        self.log("training/f1_score", self.training_f1_score.compute())
        self.training_f1_score.reset()
        self.log("training/precision", self.training_precision.compute())
        self.training_precision.reset()
        self.log("training/recall", self.training_recall.compute())
        self.training_recall.reset()
        self.log("training/specificity", self.training_specificity.compute())
        self.training_specificity.reset()
        self.log("training/auroc", self.training_auroc.compute())
        self.training_auroc.reset()
        return super().on_train_epoch_end()

    def validation_step(self, batch: Tuple[Tensor, Tensor], _: int):
        """
        This method performs a validation step.
        """
        logits, predictions, loss, y = self.loss(batch)
        self.validation_step_outputs.append(logits)

        self.log("validation/loss", loss)

        self.validation_accuracy.update(predictions, y)
        self.validation_f1_score.update(predictions, y)
        self.validation_precision.update(predictions, y)
        self.validation_recall.update(predictions, y)
        self.validation_specificity.update(predictions, y)
        self.validation_auroc.update(logits, y.long())

        return logits

    def on_validation_epoch_end(self) -> None:
        """
        This method is called at the end of the validation epoch.
        """
        self.export()

        flattened_logits = flatten(cat(self.validation_step_outputs))
        self.log("validation/logits", Histogram(flattened_logits.to("cpu")))
        self.log(
            "global_step",
            self.global_step,
        )
        self.validation_step_outputs.clear()

        self.log("validation/accuracy", self.validation_accuracy.compute())
        self.validation_accuracy.reset()
        self.log("validation/f1_score", self.validation_f1_score.compute())
        self.validation_f1_score.reset()
        self.log("validation/precision", self.validation_precision.compute())
        self.validation_precision.reset()
        self.log("validation/recall", self.validation_recall.compute())
        self.validation_recall.reset()
        self.log("validation/specificity", self.validation_specificity.compute())
        self.validation_specificity.reset()
        self.log("validation/auroc", self.validation_auroc.compute())
        self.validation_auroc.reset()

        return super().on_validation_epoch_end()

    def on_train_start(self) -> None:
        """
        This method is called at the start of the training.
        """
        # log gradients, parameter histogram and model topology
        self.logger.watch(self, log="all")
        return super().on_train_start()

    def on_train_end(self) -> None:
        """
        This method is called at the end of the training.
        """
        self.logger.experiment.unwatch(self)
        return super().on_train_end()

    def test_step(self, batch: Tuple[Tensor, Tensor], _: int):
        """
        This method performs a test step.

        Args:
            batch (Tensor): The batch.
        """
        logits, predictions, loss, y = self.loss(batch)

        self.log("test/loss", loss, on_step=False, on_epoch=True)
        self.test_accuracy.update(predictions, y)
        self.test_f1_score.update(predictions, y)
        self.test_precision.update(predictions, y)
        self.test_recall.update(predictions, y)
        self.test_specificity.update(predictions, y)
        self.test_roc.update(logits, y.long())
        self.test_auroc.update(logits, y.long())
        self.test_confusion_matrix.update(predictions, y)

    def configure_optimizers(self):
        """
        This method configures the optimizers.
        """
        return optim.Adam(
            self.parameters(),
            lr=self.config.learning_rate,
        )

    def on_test_epoch_end(self) -> None:
        """
        This method is called at the end of the test epoch.
        """
        self.export()

        self.log(
            "test/accuracy",
            self.test_accuracy.compute(),
            on_step=False,
        )
        self.log(
            "test/f1_score",
            self.test_f1_score.compute(),
            on_step=False,
        )
        self.log(
            "test/precision",
            self.test_precision.compute(),
            on_step=False,
        )
        self.log(
            "test/recall",
            self.test_recall.compute(),
            on_step=False,
        )
        self.log(
            "test/specificity",
            self.test_specificity.compute(),
            on_step=False,
        )

        fig, _ = self.test_roc.plot()
        self.log("test/roc", Image(fig))

        self.log(
            "test/auroc",
            self.test_auroc.compute(),
            on_step=False,
        )

        fig, axis = self.test_confusion_matrix.plot()
        for text in axis.texts:
            text.set_color("white")
        self.log("test/confusion_matrix", Image(fig))

        return super().on_test_epoch_end()

    def log_model_summary(self):
        """
        This method logs the model summary.
        """

    @abstractmethod
    def export(self):
        """
        This method exports the model.
        """

    @abstractmethod
    def from_file(self, artifact_dir: str) -> "Model":
        """
        This method loads the model from a file.

        Args:
            artifact_dir (str): for the file directory.
        """

    def log(self, *arg, **kwargs) -> None:
        """
        This method logs the metrics.
        """
        if self.custom_logger is not None:
            key_word_arguments = {}
            for key, value in kwargs.items():
                if key not in ["on_step", "on_epoch", "prog_bar", "logger"]:
                    key_word_arguments[key] = value
            self.custom_logger.log(
                {arg[i]: arg[i + 1] for i in range(0, len(arg), 2)},
                **key_word_arguments,
            )
        else:
            super().log(*arg, **kwargs)
