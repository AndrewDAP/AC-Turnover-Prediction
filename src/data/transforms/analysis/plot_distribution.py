"""
PlotDistribution is a class used to plot the distribution of the dataframe.
"""
from typing import Literal, Tuple
from pandas import DataFrame
from colored import Fore, Style
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.analysis.distribution_plot import distribution_plot
from src.data.error.error_dataframe import ErrorDataFrame


class PlotDistribution(DataframeTransform):
    """
    This class is used to plot the distribution of the dataframe.

    Args:
        dir_name: The directory name.
        date_by: The date by which to plot the distribution.
    """

    def __init__(
        self,
        dir_name: str,
        date_by: Literal["day_of_week", "month", "year", "hour"] = "day_of_week",
    ) -> None:
        self.dir_name = dir_name
        self.date_by = date_by

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        try:
            distribution_plot(
                dataframe,
                columns=dataframe.columns,
                env=env,
                date_by=self.date_by,
                sub_directory=self.dir_name,
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
            "dir_name": self.dir_name,
            "date_by": self.date_by,
        }
