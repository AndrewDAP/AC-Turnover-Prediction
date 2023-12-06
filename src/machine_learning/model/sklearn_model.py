"""
SkLearnModel model
"""
from os import path, makedirs, walk
from re import compile as re_compile
from typing import Type, Union
from pickle import dump, load
from numpy import ndarray
from torch import Tensor
from wandb import Artifact
from src.machine_learning.model.model import Model
from src.utility.logger import Logger
from src.utility.environment import Environment
from src.utility.configs.config import Config


class SkLearnModel(Model):
    """
    This class implements a SkLearnModel model.

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
        environment: Environment,
        example_input_array: Tensor = None,
        logger: Logger = None,
    ):
        assert model_type is not None
        super().__init__(
            model_config=config,
            loss_function=lambda _, __: 0,
            example_input_array=example_input_array,
            environment=environment,
            custom_logger=logger,
            is_single_batch_training=True,
        )
        self.model = model_type(**config.model_config)

    def fit(self, x: Union[ndarray, Tensor], y: Union[ndarray, Tensor]):
        """
        This method performs a forward pass.

        Args:
            xs (ndarray): The input tensor. The shape is (batch_size, in_features).
            ys (ndarray): The input tensor. The shape is (batch_size, in_features).
        """
        if not isinstance(x, ndarray):
            x = x.numpy()
        if not isinstance(y, ndarray):
            y = y.numpy()
        self.model.fit(x, y)

    def forward(self, x: Tensor):
        """
        This method performs a forward pass.

        Args:
            x (Tensor): The input tensor. The shape is (batch_size, in_features).
        """

        use_numpy = False
        if not isinstance(x, ndarray):
            x = x.numpy()
            use_numpy = True

        y = self.model.predict_proba(x)
        if isinstance(y, ndarray) and y.shape[1] == 2:
            y = y[:, 1]

        if use_numpy and isinstance(y, Tensor):
            y = y.detach().numpy()
        return y.squeeze()

    def export(self):
        """
        This method exports the model.
        """
        artifact = Artifact(name="model.ckpt", type="model")
        model_dir = path.join(
            self.environment.model_dir,
            str(self.__class__.__name__),
        )
        if not path.exists(model_dir):
            makedirs(model_dir)
        model_path = path.join(model_dir, f"model_{str(self.global_step).zfill(5)}.pkl")
        with open(model_path, "wb") as file:
            dump(self.model, file)
        artifact.add_file(model_path)
        self.custom_logger.log_artifact(artifact)

    def from_file(self, artifact_dir: str) -> Model:
        """
        This method loads the model from a file.

        Args:
            artifact_dir (str): for the file directory.
        """
        regex = re_compile(r".*\.pkl")
        for _, __, files in walk(str(artifact_dir)):
            for file in files:
                if regex.match(file):
                    with open(file, "rb") as file:
                        return load(file)

        raise FileNotFoundError(
            f"Could not find a model file in {artifact_dir} with the regex {regex}"
        )
