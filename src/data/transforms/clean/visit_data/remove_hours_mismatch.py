"""
This module contains the RemoveHoursMismatch class.
"""
from typing import Tuple
from pandas import DataFrame

from src.data.schema.augmented_visit_schema import AugmentedVisitSchema
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.error.error_id import ErrorId


class RemoveHoursMismatch(DataframeTransform):
    """
     This class class removes rows where the approves hours and calculated hours don't match

    Args:
        error_threshold: The allowed error theshold.
    """

    TO_REMOVE = "TO_REMOVE"

    def __init__(
        self,
        error_threshold: float = 5.0 / 60.0,
    ) -> None:
        self.error_threshold = error_threshold

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        dataframe[self.TO_REMOVE] = dataframe[
            AugmentedVisitSchema.VISIT_HOURS_APPROVED
        ] - (
            dataframe[AugmentedVisitSchema.DAY_HOURS]
            + dataframe[AugmentedVisitSchema.NIGHT_HOURS]
        )
        dataframe[self.TO_REMOVE] = dataframe[self.TO_REMOVE].abs()

        errors = errors.add_errors(
            dataframe=dataframe,
            idx=dataframe[self.TO_REMOVE] >= self.error_threshold,
            config=conf,
            error_id=ErrorId.INVALID_VALUE,
            error=f"{AugmentedVisitSchema.VISIT_HOURS_APPROVED} - ({AugmentedVisitSchema.DAY_HOURS}"
            + f" + {AugmentedVisitSchema.NIGHT_HOURS} )",
        )
        dataframe = dataframe[dataframe[self.TO_REMOVE] < self.error_threshold]
        dataframe = dataframe.drop(columns=[self.TO_REMOVE])

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "columns": [
                AugmentedVisitSchema.VISIT_HOURS_APPROVED.name,
                AugmentedVisitSchema.DAY_HOURS.name,
                AugmentedVisitSchema.NIGHT_HOURS.name,
            ],
            "error_threshold": self.error_threshold,
        }
