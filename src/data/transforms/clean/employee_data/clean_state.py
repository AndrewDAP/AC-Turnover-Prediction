"""
This class is used to clean the state.
"""
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from src.data.error.error_dataframe import ErrorDataFrame
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform


class CleanState(DataframeTransform):
    """
    This class is used to clean the state.

    Args:
        column (str): The column to clean.
    """

    def __init__(
        self,
        column: str = None,
    ) -> None:
        assert column is not None
        self.column = column

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> DataFrame:
        tqdm.pandas(desc=f"Cleaning {self.column}", position=3, leave=False)
        dataframe[self.column] = dataframe[self.column].progress_apply(
            lambda x: x.strip('"')
        )
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "column": self.column.name,
        }
