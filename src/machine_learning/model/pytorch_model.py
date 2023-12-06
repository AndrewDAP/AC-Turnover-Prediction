"""
PyTorch model
"""
from os import path, walk
from re import compile as re_compile
from typing import Type
from torch import save, Tensor, load
from torch.nn import BCELoss
from wandb import Artifact
from src.utility.logger import Logger
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.machine_learning.model.model import Model


class PyTorchModel(Model):
    """
    This class implements a PyTorchModel model.

    Args:
        config (Config): The experiment configuration.
        environment (Environment): The environment.
        example_input_array (Tensor): The example input array.
        logger (Logger): The logger.
    """

    def __init__(
        self,
        *,
        model_type: Type = None,
        config: Config = None,
        loss_function=BCELoss(),
        environment: Environment,
        example_input_array: Tensor = None,
        logger: Logger = None,
        is_single_batch_training=False,
    ):
        assert model_type is not None
        self.model_type = model_type
        super().__init__(
            model_config=config,
            loss_function=loss_function,
            example_input_array=example_input_array,
            environment=environment,
            custom_logger=logger,
            is_single_batch_training=is_single_batch_training,
        )

    def export(self):
        """
        This method exports the model.
        """
        artifact = Artifact(name="model.ckpt", type="model")
        file_name = "model_weights.pt"
        save(self.state_dict(), path.join(self.environment.model_dir, file_name))
        artifact.add_file(path.join(self.environment.model_dir, file_name))
        self.logger.experiment.log_artifact(artifact)

    def from_file(self, artifact_dir: str) -> Model:
        """
        This method loads the model from a file.

        Args:
            artifact_dir (str): The artifact directory.
        """
        regex = re_compile(r".*\.pt")

        model = self.model_type(
            config=self.config,
            environment=self.environment,
            example_input_array=self.example_input_array,
            logger=self.logger,
        )
        for root, _, files in walk(str(artifact_dir)):
            for file in files:
                if regex.match(file):
                    model.load_state_dict(load(path.join(root, file)))
                    model.eval()
                    break
        return model
