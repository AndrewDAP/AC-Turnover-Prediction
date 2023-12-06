"""
This module contains the SetNumericalToFloat class, which is used to set the types of numerical columns 
in a dataframe to float64
"""
from pandas import DataFrame, api
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame


class SetNumericalToFloat(DataframeTransform):
    """
    This class is used to set numerical column types of a dataframe to float64
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> DataFrame:
        for column in dataframe.columns:
            if api.types.is_numeric_dtype(dataframe[column]):
                dataframe[column] = dataframe[column].astype("float64").round(2)
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {"name": self.__class__.__name__}
