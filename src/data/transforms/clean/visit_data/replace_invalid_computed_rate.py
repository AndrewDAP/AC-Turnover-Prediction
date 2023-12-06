"""
ReplaceInvalidComputedRate is a class used to replace invalid computed rate
"""
from typing import Tuple
from pandas import DataFrame

from src.data.schema.visit_schema import VisitSchema
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.utility.environment import Environment
from src.utility.configs.config import Config


class ReplaceInvalidComputedRate(DataframeTransform):
    """
    This class is used to replace invalid computed rate by the average hourly or visit rate.
    A computed rate is invalid if the computed rate is equal to zero, the visit hours approved is
    higher than zero, the approval status is 1 and there is no cancel code.
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        # Get the rows with invalid computed rate
        invalid_computed_rate = dataframe.loc[
            (dataframe[VisitSchema.VISIT_COMPUTED_RATE] == 0)
            & (dataframe[VisitSchema.VISIT_APPROVAL_STATUS] == 1)
            & (dataframe[VisitSchema.VISIT_CANCEL_CODE].isnull())
            & (dataframe[VisitSchema.VISIT_HOURS_APPROVED] > 0)
        ]

        # Get the mean hourly rate
        mean_hourly_pay = dataframe.loc[
            dataframe[VisitSchema.VISIT_COMPUTED_RATE_UNITS] == "hours",
            VisitSchema.VISIT_COMPUTED_RATE,
        ].mean()

        # Replace the invalid hourly computed rate by the mean
        invalid_computed_rate.loc[
            dataframe[VisitSchema.VISIT_COMPUTED_RATE_UNITS] == "hours",
            VisitSchema.VISIT_COMPUTED_RATE,
        ] = mean_hourly_pay

        dataframe.update(invalid_computed_rate)

        # Get the mean visit rate
        mean_visit_rate = dataframe.loc[
            dataframe[VisitSchema.VISIT_COMPUTED_RATE_UNITS] == "visits",
            VisitSchema.VISIT_COMPUTED_RATE,
        ].mean()

        # Replace the invalid visit computed rate by the mean
        invalid_computed_rate.loc[
            dataframe[VisitSchema.VISIT_COMPUTED_RATE_UNITS] == "visits",
            VisitSchema.VISIT_COMPUTED_RATE,
        ] = mean_visit_rate

        dataframe.update(invalid_computed_rate)

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
