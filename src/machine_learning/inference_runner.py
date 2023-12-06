"""
Inference Runner
"""
from typing import Optional
from tqdm.autonotebook import tqdm
from numpy import ndarray, concatenate
from torch import no_grad, cuda
from torch.utils.data import Dataset, DataLoader
from src.utility.logger import Logger
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.machine_learning.model.model_factory import ModelFactory
from src.machine_learning.model.model import Model


class InferenceRunner:
    """
    This class implements the inference runner.

    Args:
        name (str): The name.
        environment (Environment): The environment.
        config (Config): The config.
        model_tag (str): The model tag.
        run_group (str): The run group.
        run_id_that_produce_the_model (str): The run id that produce the model.
    """

    def __init__(
        self,
        name: str = "Inference Runner",
        config: Config = None,
        environment: Environment = None,
        model_tag: str = None,
        run_group: Optional[str] = None,
        run_id_that_produce_the_model: str = None,
    ) -> None:
        assert environment is not None
        assert model_tag is not None
        assert run_group is not None
        self.name = name
        self.environment = environment
        self.config = config
        self.model_tag = model_tag
        self.run_group = run_group
        self.run_id_that_produce_the_model = run_id_that_produce_the_model
        self.model = self.load_model()
        self.run_config = self.model.config

    def load_model(self) -> Model:
        """
        This method loads the model.
        """
        logger = Logger(env=self.environment)
        logger.wandb.login(key=self.environment.wandb_api)
        run = logger.wandb.init(
            project="alayacare",
            group=self.run_group,
        )
        artifact = run.use_artifact(
            f"alayacare/alayacare/model.ckpt:{self.model_tag}",
            type="model",
            aliases=["model"],
            use_as="model",
        )
        artifact_dir = artifact.download()
        logger.wandb.finish()

        # restore the config
        api = logger.wandb.Api()
        run = api.run(f"alayacare/alayacare/runs/{self.run_id_that_produce_the_model}")
        run_config = Config.from_dict(run.config)

        return (
            ModelFactory(
                config=run_config,
                environment=self.environment,
                example_input_array=[],
                logger=logger,
            )
            .build()
            .from_file(artifact_dir)
        )

    def infer(self, dataset: Dataset) -> ndarray:
        """
        This method performs inference.

        Args:
            dataset (Dataset): The dataset.
        """
        if not self.model.is_single_batch_training:
            device = "cuda" if cuda.is_available() else "cpu"
            self.model.to(device)
        outputs = ndarray((0,))
        with no_grad():
            for inputs, _ in tqdm(
                DataLoader(
                    dataset=dataset,
                    batch_size=self.config.batch_size,
                    num_workers=self.config.num_workers,
                ),
                desc=f"{self.name} : Infer",
                leave=False,
                position=3,
            ):
                if not self.model.is_single_batch_training:
                    inputs = inputs.to(device)
                    outs = self.model(inputs).cpu().detach().numpy()
                else:
                    outs = self.model(inputs)
                outputs = concatenate([outputs, outs])
        return outputs

    def to_dict(self):
        """
        This method converts the object to a dictionary.
        """
        return {
            "name": self.name,
            "model_tag": self.model_tag,
            "run_group": self.run_group,
            "run_id_that_produce_the_model": self.run_id_that_produce_the_model,
            "run_config": self.run_config.to_dict(),
        }
