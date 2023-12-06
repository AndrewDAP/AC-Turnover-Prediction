"""
This module is used to load the environment variables
"""

from dataclasses import dataclass
from os import getenv, environ
from dotenv import load_dotenv


@dataclass
class Environment:
    """
    This class is used to load the environment variables
    from the .env file.
    """

    def __init__(self):
        load_dotenv()
        environ["WANDB_NOTEBOOK_NAME "] = "AlayaCare_notebook"
        self.data_dir = getenv("DATA_DIR")
        self.cache_dir = getenv("CACHE_DIR")
        self.plots_dir = getenv("PLOTS_DIR")
        self.stats_dir = getenv("STATS_DIR")
        self.model_dir = getenv("MODEL_DIR")
        self.visual_dir = getenv("VISUAL_DIR")
        self.wandb_api = getenv("WANDB_API_KEY")

    def __hash__(self) -> int:
        return (
            hash(self.data_dir)
            + hash(self.cache_dir)
            + hash(self.plots_dir)
            + hash(self.stats_dir)
            + hash(self.model_dir)
            + hash(self.visual_dir)
            + hash(self.wandb_api)
        )
