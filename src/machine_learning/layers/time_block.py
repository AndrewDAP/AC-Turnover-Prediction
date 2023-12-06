"""
TimeBlock
"""
from torch import Tensor, topk, stack, sum as torch_sum, zeros, cat
from torch.fft import rfft
from torch.nn import Module, Sequential, GELU
from torch.nn.functional import softmax
from src.machine_learning.layers.convolution_blocks import InceptionBlock


def fft_for_period(x: Tensor, k: int = 2):
    """
    This method performs FFT to find the period of the time series.

    Args:
        x (Tensor): The input tensor.
        k (int): The number of periods to find. Default is 2.
    """
    # [batch_size, time_series_size, n_features]
    # pylint: disable=not-callable
    x_frequency = rfft(x, dim=1)
    # find period by amplitudes
    frequency_list = abs(x_frequency).mean(0).mean(-1)
    frequency_list[0] = 0
    _, top_list = topk(frequency_list, k)
    top_list = top_list.detach().cpu().numpy()
    period = x.shape[1] // top_list
    return period, abs(x_frequency).mean(-1)[:, top_list]


class TimesBlock(Module):
    """
    TimesBlock

    Args:
        configs (Config): The configuration.
    """

    def __init__(self, configs):
        super().__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        self.k = configs.top_k
        # parameter-efficient design
        self.conv = Sequential(
            InceptionBlock(
                configs.d_model, configs.d_ff, num_kernels=configs.num_kernels
            ),
            GELU(),
            InceptionBlock(
                configs.d_ff, configs.d_model, num_kernels=configs.num_kernels
            ),
        )

    def forward(self, x: Tensor):
        """
        This method performs a forward pass.
        """
        batch_size, seq_length, d_model = x.size()
        period_list, period_weight = fft_for_period(x, self.k)

        res = []
        for i in range(self.k):
            period = period_list[i]
            # padding
            if (self.seq_len + self.pred_len) % period != 0:
                length = (((self.seq_len + self.pred_len) // period) + 1) * period
                padding = zeros(
                    [x.shape[0], (length - (self.seq_len + self.pred_len)), x.shape[2]]
                ).to(x.device)
                out = cat([x, padding], dim=1)
            else:
                length = self.seq_len + self.pred_len
                out = x
            # reshape
            out = (
                out.reshape(batch_size, length // period, period, d_model)
                .permute(0, 3, 1, 2)
                .contiguous()
            )
            # 2D conv: from 1d Variation to 2d Variation
            out = self.conv(out)
            # reshape back
            out = out.permute(0, 2, 3, 1).reshape(batch_size, -1, d_model)
            res.append(out[:, : (self.seq_len + self.pred_len), :])
        res = stack(res, dim=-1)
        # adaptive aggregation
        period_weight = softmax(period_weight, dim=1)
        period_weight = (
            period_weight.unsqueeze(1).unsqueeze(1).repeat(1, seq_length, d_model, 1)
        )
        res = torch_sum(res * period_weight, -1)
        # residual connection
        res = res + x
        return res
