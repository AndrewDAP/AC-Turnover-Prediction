"""
GenerateStatistics
"""

from typing import Tuple
from pandas import DataFrame
from colored import Fore, Style
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.analysis.generate_statistics import generate_statistics
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform


class GenerateStatistics(DataframeTransform):
    """
    This class is used to generate statistics for the dataframe.

    Args:
        sub_directory: The directory name.
        filename: The filename.
    """

    def __init__(
        self,
        *,
        sub_directory: str,
        filename: str,
    ) -> None:
        self.sub_directory = sub_directory
        self.filename = filename

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        try:
            generate_statistics(
                input_df=dataframe,
                env=env,
                sub_directory=self.sub_directory,
                filename=f"stats_{self.filename}.csv",
            )
        # pylint: disable=broad-except
        except Exception as err:
            print(f"{Fore.red}ERROR: {Style.reset} {self.__class__.__name__} - {err}")
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "sub_directory": self.sub_directory,
            "filename": self.filename,
        }
