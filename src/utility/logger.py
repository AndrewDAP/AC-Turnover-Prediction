"""
This module contains a class used to interact with Weights & Biases
"""

from os import path, makedirs
from PIL import Image
from matplotlib.figure import Figure
import wandb
from src.utility.environment import Environment


class Logger:
    """
    This class contains functions to interact with Weights & Biases
    """

    def __init__(self, *, env: Environment = None) -> None:
        assert env is not None
        self.wandb = wandb
        self.env = env

    def save_w2v_model(
        self,
        model_name: str,
        run_config: {},
        model_path: str = ".models/w2v_models/",
        plot_path: str = ".plots/W2V_Models/",
    ) -> None:
        """
        This function logs the model and it's config to W&B
        """
        self.wandb.init(
            project="alayacare",
            name=model_name,
            job_type="Word2Vec Model Creation",
            group="Word2Vec Model Creation",
            config=run_config,
        )

        # Save the model
        self.log_artifact(
            artifact_name=model_name,
            artifact_location=model_path,
            artifact_type="model",
        )

        # Save the vector plot
        plot_image_name = model_name.upper() + "_TOKEN_VECTORS_PLOT.png"
        self.log_image(image_path=plot_path, image_name=plot_image_name)
        self.wandb.finish()

    def save_segmentation_run(
        self,
        run_config: {},
        segmentation_name: str,
        figure: Figure,
        job_type: str,
    ) -> None:
        """
        This function logs a segmentation run to W&B
        """
        self.wandb.init(
            project="alayacare",
            name=f"{segmentation_name} Graph",
            job_type=job_type,
            group="Data Segmentation",
            config=run_config,
        )

        self.log_figure(segmentation_name, figure)
        self.wandb.finish()

    def save_cluster_analysis(
        self,
        run_config: {},
        method_name: str,
        figure: Figure,
        job_type: str,
    ) -> None:
        """
        This function logs the clusters analysis run to W&B
        """
        self.wandb.init(
            project="alayacare",
            name=f"{method_name} Graph",
            job_type=job_type,
            group="Cluster analysis",
            config=run_config,
        )

        self.log_figure(method_name, fig=figure)
        self.wandb.finish()

    def log_artifact(
        self,
        artifact_name: str,
        artifact_location: str,
        artifact_type: str,
    ) -> None:
        """
        This function creates and logs an artifact
        """
        artifact = wandb.Artifact(artifact_name, type=artifact_type)
        artifact.add_file(artifact_location + artifact_name)
        self.wandb.run.log_artifact(artifact)

    def log_image(self, image_path: str, image_name: str):
        """
        This function creates and logs an image
        """
        image = Image.open(image_path + image_name)
        self.wandb.log({image_name: wandb.Image(image)})

    def log_plot(self, section: str, name: str, figure: Figure) -> None:
        """
        This function logs a plot to W&B

        Args:
            section (str): The section of the plot
            name (str): The name of the plot
            figure (Figure): The figure to log
        """
        fig_path = path.join(self.env.plots_dir, section, f"{name}.png")
        if not path.exists(fig_path):
            makedirs(path.dirname(fig_path), exist_ok=True)
        figure.savefig(fig_path, bbox_inches="tight")
        self.wandb.run.log({f"{section}/{name}": wandb.Image(fig_path)})

    def log_figure(self, fig_name: str, fig: Figure) -> None:
        """
        This function logs a 2D or 3D Matplotlib figure to W&B
        """
        self.wandb.run.log({fig_name: fig})
