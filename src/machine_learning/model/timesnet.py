# pylint: disable=duplicate-code
"""
TimesNet model.
"""
from numpy import ndarray
from torch import Tensor, from_numpy
from torch.nn import ModuleList, LayerNorm, Dropout, Linear, Sigmoid
from torch.nn.functional import gelu
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.utility.logger import Logger
from src.utility.dotdict import Dotdict
from src.machine_learning.layers.embedding.data_embedding import DataEmbedding
from src.machine_learning.layers.time_block import TimesBlock
from src.machine_learning.model.pytorch_model import PyTorchModel


class TimesNet(PyTorchModel):
    """
    TimesNet model. Paper link: https://openreview.net/pdf?id=ju_Uqw384Oq

    Args:
        config (Config): The configuration.
        environment (Environment): The environment.
        example_input_array (torch.Tensor): The example input array.
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
            model_type=TimesNet,
            config=config,
            example_input_array=example_input_array,
            environment=environment,
            logger=logger,
        )
        configs = Dotdict(config.model_config)
        self.configs = configs
        self.task_name = configs.task_name
        self.seq_len = configs.seq_len
        self.label_len = configs.label_len
        self.pred_len = configs.pred_len
        self.model = ModuleList([TimesBlock(configs) for _ in range(configs.e_layers)])
        self.enc_embedding = DataEmbedding(
            configs.enc_in,
            configs.d_model,
            configs.embed,
            configs.freq,
            configs.dropout,
        )
        self.layer = configs.e_layers
        self.layer_norm = LayerNorm(configs.d_model)
        self.act = gelu
        self.dropout = Dropout(configs.dropout)
        self.projection = Linear(configs.d_model * configs.seq_len, configs.num_class)
        self.sigmoid = Sigmoid()
        self.float()

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

        enc_out = self.enc_embedding(
            x, None
        )  # [batch_size, time_series_size, n_features]
        for i in range(self.layer):
            enc_out = self.layer_norm(self.model[i](enc_out))

        # Output
        # pylint: disable=not-callable
        output = self.act(enc_out)
        output = self.dropout(output)
        # (batch_size, seq_length * d_model)
        output = output.reshape(output.shape[0], -1)
        output = self.projection(output).squeeze()  # (batch_size, num_classes)

        y = self.sigmoid(output)
        if use_numpy:
            y = y.detach().numpy()
        return y
