"""
This module contains the Config class.
"""


from typing import Literal

from pandas import Timestamp


class Config:
    """
    This class is used to specify the configuration of for the experiment.
        Args:
        load_id: The load id. This is used to identify when the experiment occurred.
        n_split: The number of splits to use for the cross validation.
        split_seed: The seed to use for the cross validation.
        n_epochs: The number of epochs to use for the training.
        log_every_n_steps: The number of steps to log the training.
        debug_flags: (dict) The debug flags to use.
            {
                "plot_distribution": (bool) Whether to plot the distribution of the data.
                "generate_statistics": (bool) Whether to generate statistics for the data.
                "data_slice": (bool) Whether to slice the data.
            }
        batch_size: The batch size to use for the training.
        training_window_size: The size of the training window.
        label_policy: The label policy to use.
        limit_dataframe_size: The limit of the dataframe size.
        period_duration: The duration of the period.
        cutoff: The cutoff to use for the training.
        oversampler: The oversampler to use.
        oversampler_args: The arguments to pass to the oversampler.
        model: The model to use.
        model_config: The configuration of the model.
        data_module: The data module to use.
        is_test_run: Whether this is a test run.
    """

    # pylint: disable=too-many-arguments, too-many-instance-attributes, too-many-locals
    def __init__(
        self,
        *,
        load_id: str = None,
        n_splits: int = None,
        split_seed: int = None,
        n_epochs: int = None,
        log_every_n_steps: int = None,
        batch_size: int = None,
        learning_rate: float = 0.001,
        training_window_size: int = None,
        limit_dataframe_size: int = None,
        debug_flags: dict = None,
        label_policy: Literal["30Days", "90Days"] = None,
        period_start: Timestamp = None,
        period_end: Timestamp = None,
        period_duration: Literal[
            "1D", "2D", "3D", "4D", "5D", "7D", "14D", "30D"
        ] = None,
        cutoff: float = None,
        model: Literal[
            "ExplainableBoostingMachine",
            "Perceptron",
            "SupportVectorMachine",
            "DecisionTree",
            "HistGradientBoosting",
            "MultiLayerPerceptron",
            "TimesNet",
        ] = None,
        model_config: dict = None,
        oversampler: Literal[
            "BorderlineSMOTE",
            "KMeansSMOTE",
            "SMOTEN",
            "SVMSMOTE",
            "SMOTENC",
            "ADASYN",
            "RandomOverSampler",
            "SMOTE",
            "NoOverSampler",
        ] = None,
        oversampler_args: dict = None,
        data_module: Literal[
            "AlayaCareDataModule",
            "TimesNetDataModule",
        ] = "AlayaCareDataModule",
        data_module_args: dict = None,
        is_test_run: bool = False,
        num_workers: int = 0,
    ) -> None:
        assert load_id is not None
        assert n_splits is not None
        assert split_seed is not None
        assert n_epochs is not None
        assert log_every_n_steps is not None
        assert batch_size is not None
        assert training_window_size is not None
        assert label_policy is not None
        assert period_duration is not None
        assert label_policy in ["30Days", "90Days"]
        assert period_duration in ["1D", "2D", "3D", "4D", "5D", "7D", "14D", "30D"]
        assert model is not None
        assert cutoff is not None
        assert oversampler is not None
        assert is_test_run is not None
        self.load_id = load_id
        self.n_splits = n_splits
        self.split_seed = split_seed
        self.n_epochs = n_epochs
        self.log_every_n_steps = log_every_n_steps
        self.batch_size = batch_size
        self.limit_dataframe_size = limit_dataframe_size
        self.training_window_size = training_window_size
        self.label_policy = label_policy
        self.period_start = period_start
        self.period_end = period_end
        self.period_duration = period_duration
        self.cutoff = cutoff
        self.model = model
        self.learning_rate = learning_rate
        self.model_config = model_config if model_config is not None else {}
        self.oversampler = oversampler
        self.oversampler_args = oversampler_args if oversampler_args is not None else {}
        self.data_module = data_module
        self.data_module_args = data_module_args if data_module_args is not None else {}
        self.is_test_run = is_test_run
        self.num_workers = num_workers
        self.debug_flags = (
            debug_flags
            if debug_flags is not None
            else {
                "plot_distribution": False,
                "generate_statistics": False,
                "data_slice": False,
            }
        )

    def to_dict(self) -> dict:
        """
        This method returns the configuration as a dictionary.

        Returns:
            dict: The configuration as a dictionary.
        """

        return {
            "load_id": self.load_id,
            "n_splits": self.n_splits,
            "split_seed": self.split_seed,
            "n_epochs": self.n_epochs,
            "log_every_n_steps": self.log_every_n_steps,
            "batch_size": self.batch_size,
            "learning_rate": self.learning_rate,
            "training_window_size": self.training_window_size,
            "label_policy": self.label_policy,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "period_duration": self.period_duration,
            "cutoff": self.cutoff,
            "limit_dataframe_size": self.limit_dataframe_size,
            "model": self.model,
            "model_config": self.model_config,
            "oversampler": self.oversampler,
            "oversampler_args": self.oversampler_args,
            "data_module": self.data_module,
            "data_module_args": self.data_module_args,
            "is_test_run": self.is_test_run,
            "num_workers": self.num_workers,
            "debug_flags": self.debug_flags,
        }

    @staticmethod
    def from_dict(config_dict: dict) -> "Config":
        """
        This method is a factory method that creates a Config object from a wandb dictionary.

        Args:
            config_dict (dict): The wandb dictionary.
        """
        config = Config(
            batch_size=config_dict["config"]["batch_size"],
            cutoff=config_dict["config"]["cutoff"],
            data_module=config_dict["config"]["data_module"],
            data_module_args=config_dict["config"]["data_module_args"],
            is_test_run=config_dict["config"]["is_test_run"],
            label_policy=config_dict["config"]["label_policy"],
            learning_rate=config_dict["config"]["learning_rate"],
            limit_dataframe_size=config_dict["config"]["limit_dataframe_size"],
            load_id=config_dict["config"]["load_id"],
            log_every_n_steps=config_dict["config"]["log_every_n_steps"],
            model=config_dict["config"]["model"],
            model_config=config_dict["config"]["model_config"],
            n_epochs=config_dict["config"]["n_epochs"],
            n_splits=config_dict["config"]["n_splits"],
            oversampler=config_dict["config"]["oversampler"],
            oversampler_args=config_dict["config"]["oversampler_args"],
            period_duration=config_dict["config"]["period_duration"],
            period_start=config_dict["config"]["period_start"],
            period_end=config_dict["config"]["period_end"],
            training_window_size=config_dict["config"]["training_window_size"],
            split_seed=config_dict["config"]["split_seed"],
            num_workers=config_dict["config"]["num_workers"]
            if "num_workers" in config_dict["config"]
            else 0,
            debug_flags=config_dict["config"]["debug_flags"]
            if "debug_flags" in config_dict["config"]
            else {
                "distributed_plot": False,
                "statistics": False,
                "data_slice": False,
            },
        )

        # Adjust the config for sweep runs
        for key, value in config_dict.items():
            if key in config.model_config:
                config.model_config[key] = value
        return config

    def __hash__(self) -> int:
        return hash(self.load_id)

    def __repr__(self) -> str:
        return str(self.to_dict())
