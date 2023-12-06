"""
Config for the Histogram-based Gradient Boosting Classifier model

Link to doc:
https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html#sklearn.ensemble.HistGradientBoostingClassifier
"""
from datetime import datetime
from pandas import Timestamp
from src.utility.configs.config import Config

HGB_CONFIG = Config(
    load_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
    split_seed=5832391,
    n_splits=2,
    log_every_n_steps=50,
    training_window_size=1,
    n_epochs=5,
    batch_size=256,
    cutoff=0.5,
    label_policy="90Days",
    period_duration="1D",
    period_start=Timestamp(year=2019, month=1, day=1),
    period_end=Timestamp(year=2023, month=9, day=1),
    oversampler="SMOTE",
    oversampler_args={},
    model="HistGradientBoosting",
    data_module="AlayaCareDataModule",
    data_module_args=None,
    model_config={
        "loss": "log_loss",
        "learning_rate": 0.1,
        "max_iter": 100,
        "max_leaf_nodes": 31,
        "max_depth": None,
        "min_sample_leaf": 20,
        "l2_regularization": 0,
        "max_bins": 255,
        "categorical_features": None,
        "monotonic_cst": None,
        "interaction_cst": None,
        "warm_start": False,
        "early_stopping": "auto",
        "scoring": "loss",
        "validation_fraction": 0.1,
        "n_iter_no_change": 10,
        "tol": 1e-7,
        "verbose": 0,
        "random_state": None,
        "class_weight": None,
    },
    is_test_run=False,
)
