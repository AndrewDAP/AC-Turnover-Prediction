"""
TimeFeatureEmbedding
"""

from torch import Tensor
from torch.nn import Module, Linear


class TimeFeatureEmbedding(Module):
    """
    This class implements the time feature embedding.

    Args:
        d_model (int): The model dimension.
        embed_type (str): The embedding type.
        freq (str): The frequency.
    """

    # pylint: disable=unused-argument
    def __init__(self, d_model, embed_type="timeF", freq="h"):
        super().__init__()

        freq_map = {"h": 4, "t": 5, "s": 6, "m": 1, "a": 1, "w": 2, "d": 3, "b": 3}
        d_inp = freq_map[freq]
        self.embed = Linear(d_inp, d_model, bias=False)

    def forward(self, x: Tensor):
        """
        This method performs a forward pass.
        """
        return self.embed(x)
