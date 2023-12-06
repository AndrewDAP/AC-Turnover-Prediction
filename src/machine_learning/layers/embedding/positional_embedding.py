"""
This module implements the positional embedding.
"""
from math import log
from torch import zeros, arange, sin, cos, Tensor
from torch.nn import Module


class PositionalEmbedding(Module):
    """
    This class implements the positional embedding.

    Args:
        d_model (int): The model dimension.
        max_len (int): The maximum length.
    """

    def __init__(self, d_model, max_len=5000):
        super().__init__()
        # Compute the positional encodings once in log space.
        positional_encoding = zeros(max_len, d_model).float()
        positional_encoding.require_grad = False

        position = arange(0, max_len).float().unsqueeze(1)
        div_term = (arange(0, d_model, 2).float() * -(log(10000.0) / d_model)).exp()

        positional_encoding[:, 0::2] = sin(position * div_term)
        positional_encoding[:, 1::2] = cos(position * div_term)

        positional_encoding = positional_encoding.unsqueeze(0)
        self.register_buffer("pe", positional_encoding)

    def forward(self, x: Tensor):
        """
        This method performs a forward pass.
        """
        return self.pe[:, : x.size(1)]
