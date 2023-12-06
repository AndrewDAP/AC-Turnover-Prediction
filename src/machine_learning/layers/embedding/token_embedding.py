"""
Token Embedding
"""
from torch import Tensor
from torch.nn import Module, Conv1d
from torch.nn.init import kaiming_normal_


class TokenEmbedding(Module):
    """
    This class implements the token embedding.

    Args:
        c_in (int): The number of input channels.
        d_model (int): The model dimension.
    """

    def __init__(self, c_in, d_model):
        super().__init__()
        padding = 1
        self.token_conv = Conv1d(
            in_channels=c_in,
            out_channels=d_model,
            kernel_size=3,
            padding=padding,
            padding_mode="circular",
            bias=False,
        )
        for module in self.modules():
            if isinstance(module, Conv1d):
                kaiming_normal_(module.weight, mode="fan_in", nonlinearity="leaky_relu")

    def forward(self, x: Tensor):
        """
        The forward pass
        """
        x = self.token_conv(x.permute(0, 2, 1)).transpose(1, 2)
        return x
