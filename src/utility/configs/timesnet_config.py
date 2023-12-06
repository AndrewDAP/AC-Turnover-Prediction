"""
TimesNet config
"""
from datetime import datetime
from pandas import Timestamp
from src.utility.configs.config import Config
from src.data.schema.employee_history_schema import EmployeeHistorySchema

TIMESNET_CONFIG = Config(
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
    model="TimesNet",
    data_module="TimesNetDataModule",
    data_module_args={
        "sequence_length": 90 * 3,
        "columns": [
            EmployeeHistorySchema.VISIT_COUNT_PER_PERIOD,
            EmployeeHistorySchema.DAY_HOURS_PER_PERIOD,
            EmployeeHistorySchema.NIGHT_HOURS_PER_PERIOD,
            EmployeeHistorySchema.WEEKEND_HOURS_PER_PERIOD,
            EmployeeHistorySchema.WORK_HOURS_DEVIATION_PER_PERIOD,
            EmployeeHistorySchema.WEEKDAY_HOURS_PER_PERIOD,
            EmployeeHistorySchema.DID_OVERTIME_IN_PERIOD,
            EmployeeHistorySchema.AVERAGE_EMPLOYEE_COMMUTE_DISTANCE_PER_PERIOD,
            EmployeeHistorySchema.PAY_PER_PERIOD,
            EmployeeHistorySchema.VISIT_HOURS_PER_PERIOD,
        ],
    },
    model_config={
        # basic config
        "task_name": "classification",
        "freq": "d",
        "num_class": 1,
        # forecasting task
        "seq_len": 90 * 3,
        "label_len": 1,
        "pred_len": 0,
        # model define
        "top_k": 3,
        "num_kernels": 6,
        "enc_in": 10,
        "dec_in": 10,
        "c_out": 10,
        "d_model": 32,
        "n_heads": 8,
        "e_layers": 4,
        "d_layers": 3,
        "d_ff": 256,
        "moving_avg": 25,
        "factor": 1,
        "distil": True,
        "dropout": 0.1,
        "embed": "timeF",
        "activation": "gelu",
        "output_attention": False,
    },
    is_test_run=False,
)
