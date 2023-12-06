"""
ExplainableBoostingMachine config file.
"""
from datetime import datetime
from pandas import Timestamp
from src.utility.configs.config import Config

EBM_CONFIG = Config(
    load_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
    split_seed=5832391,
    n_splits=2,
    log_every_n_steps=50,
    training_window_size=1,
    n_epochs=5,
    batch_size=16_000,
    cutoff=0.5,
    label_policy="90Days",
    period_duration="1D",
    period_start=Timestamp(year=2019, month=1, day=1),
    period_end=Timestamp(year=2023, month=9, day=1),
    oversampler="RandomOverSampler",
    oversampler_args={
        "sampling_strategy": 0.70,
    },
    data_module="AlayaCareDataModule",
    data_module_args={},
    model="ExplainableBoostingMachine",
    model_config={
        "feature_types": [
            # EmployeeHistorySchema.EMPLOYEE_AGE,
            "uniform",
            # EmployeeHistorySchema.EMPLOYEE_STATE,
            "nominal",
            # EmployeeHistorySchema.EMPLOYEE_TENURE,
            "continuous",
            # EmployeeHistorySchema.DAYS_TO_FIRST_VISIT,
            "continuous",
            # EmployeeHistorySchema.TIMESNET_INFERENCE,
            "continuous",
        ],
        "max_bins": 1024,
        "max_rounds": 15_000,
    },
    is_test_run=False,
)
