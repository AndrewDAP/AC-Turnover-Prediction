"""
Perceptron model
"""
from functools import lru_cache
from numpy import ndarray

# pylint: disable=E0611
from torch import nn, Tensor, concat, from_numpy
from src.utility.logger import Logger
from src.utility.configs.config import Config
from src.utility.environment import Environment
from src.data.schema.employee_history_schema import EmployeeHistorySchema
from src.machine_learning.data.tensor_schema import TensorSchema
from src.machine_learning.model.pytorch_model import PyTorchModel


class Perceptron(PyTorchModel):
    """
    This class implements a perceptron model.

    Args:
        config (Config): The experiment configuration.
        model_config : {
            in_features (int): The number of input features.
            out_features (int): The number of output features.
            state_embedding_size (int): The number of states.
            state_embedding_dim (int): The dimension of the state embedding.
            gender_embedding_size (int): The number of genders.
            gender_embedding_dim (int): The dimension of the state embedding.
        }
        example_input_array (Tensor): The example input array.
        environment (Environment): The environment.
        logger (Logger): The logger.
    """

    def __init__(
        self,
        *,
        config: Config = None,
        environment: Environment,
        example_input_array: Tensor = None,
        logger: Logger = None,
    ):
        super().__init__(
            model_type=Perceptron,
            config=config,
            example_input_array=example_input_array,
            environment=environment,
            logger=logger,
        )
        self.out_features: int = config.model_config.get("out_features")
        self.in_features: int = config.model_config.get("in_features")
        self.state_embedding_size: int = config.model_config.get("state_embedding_size")
        self.gender_embedding_size: int = config.model_config.get(
            "gender_embedding_size"
        )
        self.state_embedding_dim: int = config.model_config.get("state_embedding_dim")
        self.gender_embedding_dim: int = config.model_config.get("gender_embedding_dim")

        self.state_embedding = nn.Embedding(
            num_embeddings=self.state_embedding_size,
            embedding_dim=self.state_embedding_dim,
        )

        self.gender_embedding = nn.Embedding(
            num_embeddings=self.gender_embedding_size,
            embedding_dim=self.gender_embedding_dim,
        )

        # in_features plus the embedding added and minus the two columns that are not used
        in_features_linear_layer = (
            self.in_features - 2 + self.gender_embedding_dim + self.state_embedding_dim
        )

        self.layers = nn.Sequential(
            nn.BatchNorm1d(
                num_features=in_features_linear_layer,
            ),
            nn.Linear(
                in_features=in_features_linear_layer,
                out_features=self.out_features,
            ),
            nn.Sigmoid(),
        )

        self.save_hyperparameters()

    def forward(self, x: Tensor):
        """
        This method performs a forward pass.

        Args:
            x (Tensor): The input tensor. The shape is (batch_size, in_features).
        """
        use_numpy = False
        if isinstance(x, ndarray):
            x = from_numpy(x).to(self.device, dtype=self.dtype)
            use_numpy = True

        if len(x.shape) == 1:
            x = x.unsqueeze(dim=0)

        x = concat(
            tensors=[
                x[:, self.__get_indexes(n_features=x.shape[-1])],
                self.state_embedding(
                    x[:, TensorSchema[EmployeeHistorySchema.EMPLOYEE_STATE]].long()
                ),
                self.gender_embedding(
                    x[:, TensorSchema[EmployeeHistorySchema.EMPLOYEE_GENDER]].long()
                ),
            ],
            dim=-1,
        )

        y = self.layers(x)
        if use_numpy:
            y = y.detach().numpy()
        return y

    @lru_cache()
    def __get_indexes(self, n_features: int):
        """
        This method returns the indexes for the linear layer.

        Args:
            n_features (int): The number of features.
        """
        # all indexes except the one for state en gender
        idx = []
        for i in range(n_features):
            if i in [
                TensorSchema[EmployeeHistorySchema.EMPLOYEE_STATE],
                TensorSchema[EmployeeHistorySchema.EMPLOYEE_GENDER],
            ]:
                continue
            idx.append(i)

        return idx
