""" Class ComputeFirstVisitDate
"""

from typing import Tuple
from pandas import DataFrame
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.transforms.transform import DataframeTransform
from src.utility.configs.config import Config
from src.utility.environment import Environment


class ComputeFirstVisitDate(DataframeTransform):
    """Computes the field EMPLOYEE_FIRST_VISIT"""

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        """
        Calculate and fill the EMPLOYEE_FIRST_VISIT field in the DataFrame.

        Args:
            dataframe (DataFrame): The input DataFrame.
            errors (ErrorDataFrame): The error DataFrame.
            conf (Config): The configuration object.
            env (Environment): The environment object.

        Returns:
            Tuple[DataFrame, ErrorDataFrame]: A tuple containing the modified DataFrame
            and the error DataFrame.
        """

        employee_first_visit = (
            dataframe.groupby(AugmentedVisitSchema.EMPLOYEE_ID)
            .agg(EMPLOYEE_FIRST_VISIT=(AugmentedVisitSchema.VISIT_START_AT, "min"))
            .reset_index()
        )

        dataframe = dataframe.merge(
            employee_first_visit, on=AugmentedVisitSchema.EMPLOYEE_ID, how="left"
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
        }
