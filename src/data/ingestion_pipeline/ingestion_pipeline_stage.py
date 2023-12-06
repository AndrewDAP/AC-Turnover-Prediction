"""
Ingestion pipeline stage.
"""
from typing import List
from hashlib import new
from json import dumps
from colored import Fore, Style
from src.data.transforms.transform import DataframeTransform
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.schema.schema import Schema
from src.data.schema.employee_schema import EmployeeSchema
from src.data.process_dataframe import process_dataframe
from src.data.transforms.clean.join import Join
from src.data.transforms.analysis.data_slice import DataSlice
from src.data.transforms.analysis.generate_statistics import GenerateStatistics
from src.data.transforms.analysis.plot_distribution import PlotDistribution


class IngestionPipelineStage:
    """
    A class to represent a stage in the ingestion pipeline.

    Args:
        name (str): The name of the stage.
        required_stages_names (List[str]): The names of the required stages.
        config (Config): The config.
        load_dataframe_csv_path (str): The path to the csv to load.
        from_schema (Schema): The schema of the dataframe before the transforms.
        to_schema (Schema): The schema of the dataframe after the transforms.
        transforms (List[DataframeTransform]): The transforms to apply.
    """

    def __init__(
        self,
        *,
        name: str = None,
        config: Config = None,
        required_stages_names: List[str] = None,
        load_dataframe_csv_path: str = None,
        from_schema: Schema = None,
        to_schema: Schema = None,
        transforms: List[DataframeTransform] = None,
    ):
        assert name is not None
        assert from_schema is not None
        assert to_schema is not None
        assert transforms is not None
        assert load_dataframe_csv_path is not None or len(required_stages_names) > 0
        self.name = name
        self.config = config
        self.transforms = transforms
        self.from_schema = from_schema
        self.to_schema = to_schema
        self.load_dataframe_csv_path = load_dataframe_csv_path
        self.required_stages_names = required_stages_names or []
        self.required_stages = []
        self.children_stages = []
        self.dataframe = None
        self.errors = None

        if self.config.debug_flags["data_slice"]:
            self.transforms = [
                DataSlice(
                    sub_directory=f"data_slice/{self.name}",
                    slice_by=self.__get_slice_by_for_schema(self.from_schema),
                    filename=f"{self.name}_before",
                    slice_size=2,
                ),
                *self.transforms,
                DataSlice(
                    sub_directory=f"data_slice/{self.name}",
                    slice_by=self.__get_slice_by_for_schema(self.to_schema),
                    filename=f"{self.name}_after",
                    slice_size=2,
                ),
            ]
        if self.config.debug_flags["generate_statistics"]:
            self.transforms = [
                GenerateStatistics(
                    sub_directory=f"{self.name}",
                    filename=f"{self.name}_before",
                ),
                *self.transforms,
                GenerateStatistics(
                    sub_directory=f"{self.name}",
                    filename=f"{self.name}_after",
                ),
            ]
        if self.config.debug_flags["plot_distribution"]:
            self.transforms = [
                PlotDistribution(
                    dir_name=f"{self.name}/before",
                    date_by="year",
                ),
                *self.transforms,
                PlotDistribution(
                    dir_name=f"{self.name}/after",
                    date_by="year",
                ),
            ]

    def set_parent_nodes(self, parent_nodes: List["IngestionPipelineStage"]):
        """
        Set the parent nodes.
        """
        self.required_stages = parent_nodes

    def add_child_node(self, child_node: "IngestionPipelineStage"):
        """
        Set the child nodes.
        """
        for child in self.children_stages:
            if child.name == child_node.name:
                break
        else:
            self.children_stages.append(child_node)

    def run(
        self,
        *,
        config: Config,
        environment: Environment,
        limit: int = None,
    ) -> "IngestionPipelineStage":
        """
        Run the stage.

        Args:
            config (Config): The config.
            environment (Environment): The environment.
            limit (int): The limit of the dataframe.
        """
        for transform in self.transforms:
            if isinstance(transform, Join):
                for stage in self.required_stages:
                    if stage.name == transform.right:
                        transform.right = stage.dataframe
                        break
        self.dataframe, self.errors = process_dataframe(
            dataframe=self.required_stages[0].dataframe
            if len(self.required_stages) > 0
            else None,
            load_dataframe_csv_path=self.load_dataframe_csv_path,
            transforms=self.transforms,
            conf=config,
            env=environment,
            limit=limit,
        )
        return self

    def __get_slice_by_for_schema(self, schema: Schema) -> str:
        """
        Get the slice by for the schema.

        Args:
            schema (Schema): The schema.
        """
        ids_column = [
            column for column in schema.columns if "id" in column.name.lower()
        ]
        if EmployeeSchema.EMPLOYEE_ID.name in [column.name for column in ids_column]:
            return EmployeeSchema.EMPLOYEE_ID.name

        if len(ids_column) > 0:
            return ids_column[0].name

        return schema.columns[0].name

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.name,
            "required_stages_names": tuple(self.required_stages_names),
            "load_dataframe_csv_path": self.load_dataframe_csv_path,
            "from_schema": self.from_schema.__class__.__name__,
            "to_schema": self.to_schema.__class__.__name__,
            "transforms": [transform.to_dict() for transform in self.transforms],
        }

    def __hash__(self) -> int:
        """
        This method returns the hash of the class.

        Returns:
            int: The hash of the class.
        """
        parent_hashes = [hash(parent_stage) for parent_stage in self.required_stages]
        hasher = new("sha256")
        dump = ""

        try:
            dump = dumps(self.to_dict(), sort_keys=True).encode()
        except TypeError as err:
            print(f"{Fore.red}ERROR: {Style.reset} not serializable{self.to_dict()}")
            raise err

        hasher.update(dump)
        number = int(hasher.hexdigest(), 16) + sum(parent_hashes)
        return number

    def data_integrity_test(self, threshold: float = 0.3):
        """
        This method performs a data integrity test on the stage.

        Args:
            threshold (float, optional): The threshold for the number of errors. Defaults to 0.3.
        """
        if self.errors is None or self.dataframe is None:
            return
        if len(self.errors) > threshold * len(self.dataframe):
            print(
                f"{Fore.red}ERROR: {Style.reset}The number of errors is greater than"
                + f" the number of rows in {self.name}"
            )
            return
        print(
            f"{Fore.green}SUCCESS: {Style.reset} {self.name}'s Data integrity test has passed."
        )
