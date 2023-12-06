"""
This module contains the SetTypesVisit class, which is used to set the types of the visit data.
"""
from pandas import DataFrame, to_datetime
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.visit_schema import VisitSchema


class SetTypesVisit(DataframeTransform):
    """
    This class is used to set the types of the visit data.
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> DataFrame:
        dataframe[VisitSchema.VISIT_ID] = dataframe[VisitSchema.VISIT_ID].astype(
            int, errors="ignore"
        )

        dataframe[VisitSchema.VISIT_SERVICE_DESCRIPTION] = dataframe[
            VisitSchema.VISIT_SERVICE_DESCRIPTION
        ].astype(str, errors="ignore")

        dataframe[VisitSchema.CLIENT_ID] = dataframe[VisitSchema.CLIENT_ID].astype(
            int, errors="ignore"
        )

        dataframe[VisitSchema.EMPLOYEE_ID] = dataframe[VisitSchema.EMPLOYEE_ID].astype(
            int, errors="ignore"
        )

        dataframe[VisitSchema.VISIT_CREATED_AT] = to_datetime(
            dataframe[VisitSchema.VISIT_CREATED_AT],
            errors="coerce",
        )

        dataframe[VisitSchema.VISIT_UPDATED_AT] = to_datetime(
            dataframe[VisitSchema.VISIT_UPDATED_AT],
            errors="coerce",
        )

        dataframe[VisitSchema.VISIT_START_AT] = to_datetime(
            dataframe[VisitSchema.VISIT_START_AT],
            errors="coerce",
        )

        dataframe[VisitSchema.VISIT_END_AT] = to_datetime(
            dataframe[VisitSchema.VISIT_END_AT],
            errors="coerce",
        )

        dataframe[VisitSchema.VISIT_START_AT_UTC] = to_datetime(
            dataframe[VisitSchema.VISIT_START_AT_UTC],
            utc=True,
            errors="coerce",
        )

        dataframe[VisitSchema.VISIT_END_AT_UTC] = to_datetime(
            dataframe[VisitSchema.VISIT_END_AT_UTC],
            utc=True,
            errors="coerce",
        )

        dataframe[VisitSchema.VISIT_HOLIDAY_DATE] = to_datetime(
            dataframe[VisitSchema.VISIT_HOLIDAY_DATE],
            format="%Y-%m-%d",
            errors="coerce",
        )

        dataframe[VisitSchema.VISIT_COMPLETED] = dataframe[
            VisitSchema.VISIT_COMPLETED
        ].astype(int, errors="ignore")

        dataframe[VisitSchema.VISIT_IN_OUT_OF_RECURRENCE_STATUS] = dataframe[
            VisitSchema.VISIT_IN_OUT_OF_RECURRENCE_STATUS
        ].astype(str, errors="ignore")

        dataframe[VisitSchema.VISIT_RECURRENCE] = dataframe[
            VisitSchema.VISIT_RECURRENCE
        ].astype(int, errors="ignore")

        dataframe[VisitSchema.VISIT_IS_PAID] = dataframe[
            VisitSchema.VISIT_IS_PAID
        ].astype(int, errors="ignore")

        dataframe[VisitSchema.VISIT_ADL_COMPLETE] = dataframe[
            VisitSchema.VISIT_ADL_COMPLETE
        ].astype(int, errors="ignore")

        dataframe[VisitSchema.VISIT_HAS_ADL] = dataframe[
            VisitSchema.VISIT_HAS_ADL
        ].astype(int, errors="ignore")

        dataframe[VisitSchema.VISIT_BREAK_MINUTES] = dataframe[
            VisitSchema.VISIT_BREAK_MINUTES
        ].astype(int, errors="ignore")

        dataframe[VisitSchema.VISIT_BREAK_HOURS] = dataframe[
            VisitSchema.VISIT_BREAK_HOURS
        ].astype(int, errors="ignore")

        dataframe[VisitSchema.VISIT_APPROVAL_STATUS] = dataframe[
            VisitSchema.VISIT_APPROVAL_STATUS
        ].astype(int, errors="ignore")

        dataframe[VisitSchema.VISIT_SCHEDULED_DURATION] = dataframe[
            VisitSchema.VISIT_SCHEDULED_DURATION
        ].astype(float, errors="ignore")

        dataframe[VisitSchema.VISIT_UNIT_QTY] = dataframe[
            VisitSchema.VISIT_UNIT_QTY
        ].astype(float, errors="ignore")

        dataframe[VisitSchema.VISIT_ON_HOLD_REASON] = dataframe[
            VisitSchema.VISIT_ON_HOLD_REASON
        ].astype(str, errors="ignore")

        dataframe[VisitSchema.VISIT_COMPUTED_RATE_UNITS] = dataframe[
            VisitSchema.VISIT_COMPUTED_RATE_UNITS
        ].astype(str, errors="ignore")

        dataframe[VisitSchema.VISIT_COMPUTED_RATE] = dataframe[
            VisitSchema.VISIT_COMPUTED_RATE
        ].astype(float, errors="ignore")

        dataframe[VisitSchema.VISIT_CANCEL_CODE] = dataframe[
            VisitSchema.VISIT_CANCEL_CODE
        ].astype(str, errors="ignore")

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {"name": self.__class__.__name__}
