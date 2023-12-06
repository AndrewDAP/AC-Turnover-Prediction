"""
Configs
"""
from src.utility.configs.timesnet_config import TIMESNET_CONFIG
from src.utility.configs.explainable_boosting_machine_config import (
    EBM_CONFIG,
)
from src.utility.configs.mlp_config import MLP_CONFIG
from src.utility.configs.hgb_model import HGB_CONFIG


class Configs:
    """
    This class contains the configs.
    """

    TIMESNET_CONFIG = TIMESNET_CONFIG
    EXPLAINABLE_BOOSTING_MACHINE_CONFIG = EBM_CONFIG
    MLP_CONFIG = MLP_CONFIG
    HGB_CONFIG = HGB_CONFIG
