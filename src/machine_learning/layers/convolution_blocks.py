"""
Convolution Blocks.
"""
from torch import stack, Tensor
from torch.nn import Module, ModuleList, Conv2d
from torch.nn.init import kaiming_normal_, constant_


class InceptionBlock(Module):
    """
    Inception Block V1.

    Args:
        in_channels (int): The number of input channels.
        out_channels (int): The number of output channels.
        num_kernels (int): The number of kernels.
        init_weight (bool): Whether to initialize the weight.
    """

    def __init__(self, in_channels, out_channels, num_kernels=6, init_weight=True):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_kernels = num_kernels
        kernels = []
        for i in range(self.num_kernels):
            kernels.append(
                Conv2d(in_channels, out_channels, kernel_size=2 * i + 1, padding=i)
            )
        self.kernels = ModuleList(kernels)
        if init_weight:
            self._initialize_weights()

    def _initialize_weights(self):
        """
        This method initializes the weights.
        """
        for module in self.modules():
            if isinstance(module, Conv2d):
                kaiming_normal_(module.weight, mode="fan_out", nonlinearity="relu")
                if module.bias is not None:
                    constant_(module.bias, 0)

    def forward(self, x: Tensor):
        """
        This method performs a forward pass.
        """
        res_list = []
        for i in range(self.num_kernels):
            res_list.append(self.kernels[i](x))
        res = stack(res_list, dim=-1).mean(-1)
        return res
