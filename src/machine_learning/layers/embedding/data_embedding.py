"""
Data Embedding
"""
from torch import Tensor
from torch.nn import Module, Dropout
from src.machine_learning.layers.embedding.token_embedding import TokenEmbedding
from src.machine_learning.layers.embedding.positional_embedding import (
    PositionalEmbedding,
)
from src.machine_learning.layers.embedding.temporal_embedding import TemporalEmbedding
from src.machine_learning.layers.embedding.time_feature_embedding import (
    TimeFeatureEmbedding,
)


class DataEmbedding(Module):
    """
    This class implements the data embedding.

    Args:
        c_in (int): The number of input channels.
        d_model (int): The model dimension.
        embed_type (str): The embedding type.
        freq (str): The frequency.
        dropout (float): The dropout rate.
    """

    def __init__(
        self,
        c_in,
        d_model,
        embed_type="fixed",
        freq="h",
        dropout=0.1,
    ):
        super().__init__()

        self.value_embedding = TokenEmbedding(c_in=c_in, d_model=d_model)
        self.position_embedding = PositionalEmbedding(d_model=d_model)
        self.temporal_embedding = (
            TemporalEmbedding(d_model=d_model, embed_type=embed_type, freq=freq)
            if embed_type != "timeF"
            else TimeFeatureEmbedding(d_model=d_model, embed_type=embed_type, freq=freq)
        )
        self.dropout = Dropout(p=dropout)

    def forward(self, x: Tensor, x_mark: Tensor):
        """
        This method performs a forward pass.
        """
        if x_mark is None:
            x = self.value_embedding(x) + self.position_embedding(x)
        else:
            x = (
                self.value_embedding(x)
                + self.temporal_embedding(x_mark)
                + self.position_embedding(x)
            )
        return self.dropout(x)
