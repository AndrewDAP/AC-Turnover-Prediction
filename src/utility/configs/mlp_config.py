"""
MultiLayerPerceptron config
"""
from datetime import datetime
from pandas import Timestamp
from src.utility.configs.config import Config

MLP_CONFIG = Config(
    load_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
    split_seed=5832391,
    n_splits=2,
    log_every_n_steps=50,
    training_window_size=1,
    n_epochs=5,
    limit_dataframe_size=None,
    batch_size=256,
    cutoff=0.5,
    label_policy="90Days",
    period_duration="1D",
    period_start=Timestamp(year=2019, month=1, day=1),
    period_end=Timestamp(year=2023, month=9, day=1),
    oversampler="RandomOverSampler",
    oversampler_args={},
    model="MultiLayerPerceptron",
    data_module="AlayaCareDataModule",
    data_module_args=None,
    model_config={
        "hidden_layer_sizes": (100,),
        "activation": "relu",
        "solver": "adam",
        "alpha": 0.0001,
        "batch_size": "auto",
        "learning_rate": "constant",
        "learning_rate_init": 0.001,
        "power_t": 0.5,
        "max_iter": 200,
        "shuffle": True,
        "random_state": None,
        "tol": 1e-4,
        "verbose": False,
        "warm_start": False,
        "momentum": 0.9,
        "nesterovs_momentum": True,
        "early_stopping": False,
        "validation_fraction": 0.1,
        "beta_1": 0.9,
        "beta_2": 0.999,
        "epsilon": 1e-8,
        "n_iter_no_change": 10,
        "max_fun": 15000,
    },
    is_test_run=False,
)
