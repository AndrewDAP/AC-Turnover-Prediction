"""
The ingestion pipeline module.
"""
from typing import Dict, List, Optional
from pandas import DataFrame, pivot_table
from tqdm.autonotebook import tqdm
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.utility.dataframe_cache import DataFrameCache
from src.data.ingestion_pipeline.ingestion_pipeline_stage import IngestionPipelineStage
from src.data.error.error_dataframe import ErrorDataFrame


class IngestionPipeline:
    """
    A class to represent the ingestion pipeline.

    Args:
        environment (Environment, optional): The environment. Defaults to None.
        config (Config, optional): The config. Defaults to None.
        use_caching (bool, optional): Whether to use caching. Defaults to False.
        stages (List[IngestionPipelineStage], optional): The stages. Defaults to None.
        force_stage_calculation_and_not_use_cache_stage_name (Optional[str], optional):
            The stage name to force calculation and not use cache. Defaults to None.
    """

    def __init__(
        self,
        *,
        environment: Environment = None,
        config: Config = None,
        use_caching: bool = False,
        stages: List[IngestionPipelineStage] = None,
        force_stage_calculation_and_not_use_cache_stage_name: Optional[str] = None,
        limit_dataframe_size: Optional[int] = None,
    ) -> None:
        self.environment = environment
        self.config = config
        self.use_caching = use_caching
        self.stages = {stage.name: stage for stage in stages}
        self.completed_stages = {}
        self.cache = DataFrameCache(environment=environment)
        self.force_stage_calculation_and_not_use_cache_stage_name = (
            force_stage_calculation_and_not_use_cache_stage_name
        )
        self.limit_dataframe_size = limit_dataframe_size

    @property
    def dataframes(self) -> Dict[str, DataFrame]:
        """
        Get the dataframes.
        """
        return {stage.name: stage.dataframe for stage in self.stages.values()}

    def build_pipeline(self) -> "IngestionPipeline":
        """
        Build the pipeline. This will set the parent nodes for each stage.
        """
        for stage in self.stages.values():
            stage.set_parent_nodes(
                [self.stages[stage_name] for stage_name in stage.required_stages_names]
            )
            for parent_stage in stage.required_stages:
                parent_stage.children_stages.append(stage)
        return self

    def run_pipeline(self, stage_name: Optional[str] = None) -> "IngestionPipeline":
        """
        Run the pipeline. or read from cache if stage is cached.

        Args:
            stage_name (str): stage name to run only.
        """

        with tqdm(
            total=len(self.stages),
            desc="Running pipeline",
            position=0,
            leave=True,
        ) as progress_bar:
            if (
                self.use_caching
                and stage_name is not None
                and self.cache.has(
                    key=hash(self.stages[stage_name]),
                    sub_directory=f"{self.stages[stage_name].name}/dataframe",
                )
            ):
                self.__run_stage(
                    stage=self.stages[stage_name], progress_bar=progress_bar
                )
                progress_bar.update(len(self.stages) - 1)
                return self
            roots = [
                stage
                for stage in self.stages.values()
                if len(stage.required_stages) == 0
            ]

            for root in roots:
                self.__run_stage(stage=root, progress_bar=progress_bar)
            next_stage = self.__find_next_stage_to_execute()
            while next_stage is not None:
                self.__run_stage(stage=next_stage, progress_bar=progress_bar)
                next_stage = self.__find_next_stage_to_execute()

        return self

    def __run_stage(self, *, stage: IngestionPipelineStage, progress_bar) -> None:
        """
        Run the stage. or read from cache if stage is cached.
        """
        progress_bar.set_description(f"Running {stage.name}")

        if (
            self.use_caching
            and self.cache.has(key=hash(stage), sub_directory=f"{stage.name}/dataframe")
            and stage.name != self.force_stage_calculation_and_not_use_cache_stage_name
        ):
            stage.dataframe = self.cache.get(
                key=hash(stage), sub_directory=f"{stage.name}/dataframe"
            )
            if self.limit_dataframe_size is not None:
                stage.dataframe = stage.dataframe.head(self.limit_dataframe_size)
            if self.cache.has(key=hash(stage), sub_directory=f"{stage.name}/errors"):
                stage.errors = self.cache.get(
                    key=hash(stage), sub_directory=f"{stage.name}/errors"
                )
            else:
                stage.errors = ErrorDataFrame(stage.dataframe, config=self.config)
        else:
            stage.run(
                config=self.config,
                environment=self.environment,
                limit=self.limit_dataframe_size,
            )
            if self.limit_dataframe_size is not None:
                stage.dataframe = stage.dataframe.head(self.limit_dataframe_size)
        self.completed_stages[stage.name] = stage
        if (
            self.use_caching
            and stage.name != self.force_stage_calculation_and_not_use_cache_stage_name
        ):
            if not self.cache.has(
                key=hash(stage), sub_directory=f"{stage.name}/dataframe"
            ):
                self.cache.add(
                    key=hash(stage),
                    value=stage.dataframe,
                    sub_directory=f"{stage.name}/dataframe",
                )
            if not self.cache.has(
                key=hash(stage), sub_directory=f"{stage.name}/errors"
            ):
                self.cache.add(
                    key=hash(stage),
                    value=stage.errors,
                    sub_directory=f"{stage.name}/errors",
                )
        progress_bar.update(1)

    def data_integrity_test(self, threshold: float = 0.3) -> DataFrame:
        """
        Run the data integrity test.

        Args:
            threshold (float, optional): The threshold. Defaults to 0.3.
        """
        for stage in self.stages.values():
            if stage.errors is not None:
                stage.data_integrity_test(threshold=threshold)
        return self.get_errors()

    def get_errors(self) -> DataFrame:
        """
        Get the errors.

        Returns:
            DataFrame: The errors.
        """
        dataframe = DataFrame([], columns=["error_id", "error", "count"])
        for error in [
            stage.errors for stage in self.stages.values() if stage.errors is not None
        ]:
            table = pivot_table(error, index=["error_id", "error"], aggfunc="size")
            table = table.reset_index()
            table.columns = ["error_id", "error", "count"]
            dataframe = dataframe.append(table)
        return dataframe

    def __find_next_stage_to_execute(self) -> Optional[IngestionPipelineStage]:
        """ "
        Find the next stage to execute. This will find the next stage to execute
        """
        uncompleted_stages = [
            stage
            for stage in self.stages.values()
            if stage.name not in self.completed_stages
        ]

        for stage in uncompleted_stages:
            for parent_stage in stage.required_stages:
                if parent_stage.name not in self.completed_stages:
                    break
            return stage
        return None

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "use_caching": self.use_caching,
            "stages": [stage.to_dict() for stage in self.stages.values()],
        }
