# pylint: disable=wrong-import-position, duplicate-code
"""
Main that runs on polytechnique compute cluster
"""
from sys import path

path.append("src")
from warnings import filterwarnings
from wandb import login
from src.utility.environment import Environment
from src.data.ingestion_pipeline.ingestion_pipeline import IngestionPipeline
from src.data.ingestion_pipeline.stages.cleaning.client_data_cleaning_calculated_fields_stage import (
    build_client_data_cleaning_calculated_fields_stage,
)
from src.data.ingestion_pipeline.stages.cleaning.clock_data_cleaning_calculated_fields_stage import (
    build_clock_data_cleaning_calculated_fields_stage,
)
from src.data.ingestion_pipeline.stages.cleaning.employee_data_cleaning_calculated_fields_stage import (
    build_employee_data_cleaning_calculated_fields_stage,
)
from src.data.ingestion_pipeline.stages.cleaning.visit_data_cleaning_calculated_fields_stage import (
    build_visit_data_cleaning_calculated_fields_stage,
)
from src.data.ingestion_pipeline.stages.augmented_visit_stage import (
    build_augmented_visit_stage,
)
from src.data.ingestion_pipeline.stages.employee_history_aggregation_stage import (
    build_employee_history_aggregation_stage,
)
from src.data.ingestion_pipeline.stages.employee_history_fill_gaps_stage import (
    build_employee_history_fill_gaps_stage,
)
from src.data.ingestion_pipeline.stages.employee_history_calculated_fields_stage import (
    build_employee_history_calculated_fields_stage,
)
from src.data.ingestion_pipeline.stages.employee_history_fill_na_stage import (
    build_employee_history_fill_na_stage,
)
from src.data.ingestion_pipeline.stages.segmentation_stage import (
    build_segmentation_stage,
)
from src.data.ingestion_pipeline.stages.training_employee_history_stage import (
    build_training_employee_history_stage,
)
from src.data.ingestion_pipeline.stages.y_labels_generation_stage import (
    build_y_labels_generation_stage,
)
from src.data.ingestion_pipeline.stages.employee_rolling_features_stage import (
    build_employee_history_rolling_features_stage,
)
from src.utility.configs.configs import Configs
from src.machine_learning.trainer import train

filterwarnings("ignore")

env = Environment()
# Please use your Key here
login(key=env.wandb_api)
conf = Configs.EXPLAINABLE_BOOSTING_MACHINE_CONFIG

ingestion_pipeline = (
    IngestionPipeline(
        config=conf,
        environment=env,
        use_caching=True,
        limit_dataframe_size=conf.limit_dataframe_size,
        stages=[
            build_client_data_cleaning_calculated_fields_stage(conf, env),
            build_clock_data_cleaning_calculated_fields_stage(conf, env),
            build_employee_data_cleaning_calculated_fields_stage(conf, env),
            build_visit_data_cleaning_calculated_fields_stage(conf, env),
            build_augmented_visit_stage(conf, env),
            build_employee_history_aggregation_stage(conf, env),
            build_employee_history_fill_gaps_stage(conf, env),
            build_employee_history_calculated_fields_stage(conf, env),
            build_employee_history_rolling_features_stage(conf, env),
            build_employee_history_fill_na_stage(conf, env),
            build_y_labels_generation_stage(conf, env),
            build_segmentation_stage(conf, env),
            build_training_employee_history_stage(conf, env),
        ],
    )
    .build_pipeline()
    .run_pipeline(stage_name="Training_Employee_History_Stage")
)

train(
    ingestion_pipeline=ingestion_pipeline,
    config=conf,
    environment=env,
    limit=1,
    use_k_fold=False,
    use_sweep=True,
)
