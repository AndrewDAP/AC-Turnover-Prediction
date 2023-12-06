"""
Temporal Embedding
"""
from torch import Tensor
from torch.nn import Module, Embedding
from src.machine_learning.layers.embedding.fixed_embedding import FixedEmbedding


class TemporalEmbedding(Module):
    """
    This class implements the temporal embedding.

    Args:
        d_model (int): The model dimension.
        embed_type (str): The embedding type.
        freq (str): The frequency.
    """

    def __init__(self, d_model, embed_type="fixed", freq="h"):
        super().__init__()

        minute_size = 4
        hour_size = 24
        weekday_size = 7
        day_size = 32
        month_size = 13

        embed_type = FixedEmbedding if embed_type == "fixed" else Embedding
        if freq == "t":
            self.minute_embed = embed_type(minute_size, d_model)
        self.hour_embed = embed_type(hour_size, d_model)
        self.weekday_embed = embed_type(weekday_size, d_model)
        self.day_embed = embed_type(day_size, d_model)
        self.month_embed = embed_type(month_size, d_model)

    def forward(self, x: Tensor):
        """
        This method performs a forward pass.
        """
        x = x.long()
        minute_x = (
            self.minute_embed(x[:, :, 4]) if hasattr(self, "minute_embed") else 0.0
        )
        hour_x = self.hour_embed(x[:, :, 3])
        weekday_x = self.weekday_embed(x[:, :, 2])
        day_x = self.day_embed(x[:, :, 1])
        month_x = self.month_embed(x[:, :, 0])

        return hour_x + weekday_x + day_x + month_x + minute_x
