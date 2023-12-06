"""
FixedEmbedding
"""
from math import log
from torch import Tensor, zeros, arange, sin, cos
from torch.nn import Module, Embedding, Parameter


class FixedEmbedding(Module):
    """
    This class implements the fixed embedding.

    Args:
        c_in (int): The number of input channels.
        d_model (int): The model dimension.
    """

    def __init__(self, c_in, d_model):
        super().__init__()

        weights = zeros(c_in, d_model).float()
        weights.require_grad = False

        position = arange(0, c_in).float().unsqueeze(1)
        div_term = (arange(0, d_model, 2).float() * -(log(10000.0) / d_model)).exp()

        weights[:, 0::2] = sin(position * div_term)
        weights[:, 1::2] = cos(position * div_term)

        self.embedding = Embedding(c_in, d_model)
        self.embedding.weight = Parameter(weights, requires_grad=False)

    def forward(self, x: Tensor):
        """
        This method performs a forward pass.
        """
        return self.embedding(x).detach()
