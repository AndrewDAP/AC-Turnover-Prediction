"""
This module contains the SetTypesEmployee class, which is used to set the types of the employee data.
"""
from pandas import DataFrame, to_datetime
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.employee_schema import EmployeeSchema


class SetTypesEmployee(DataframeTransform):
    """
    This class is used to set the types of the employee data.
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> DataFrame:
        dataframe[EmployeeSchema.EMPLOYEE_ID] = dataframe[
            EmployeeSchema.EMPLOYEE_ID
        ].astype(int, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_STATUS] = dataframe[
            EmployeeSchema.EMPLOYEE_STATUS
        ].astype(int, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_HAS_SKILLS] = dataframe[
            EmployeeSchema.EMPLOYEE_HAS_SKILLS
        ].astype(int, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_COUNTRY] = dataframe[
            EmployeeSchema.EMPLOYEE_COUNTRY
        ].astype(str, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_GENDER] = dataframe[
            EmployeeSchema.EMPLOYEE_GENDER
        ].astype(str, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_JOB_TITLE] = dataframe[
            EmployeeSchema.EMPLOYEE_JOB_TITLE
        ].astype(str, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_START_ON] = to_datetime(
            dataframe[EmployeeSchema.EMPLOYEE_START_ON]
            .astype(str, errors="ignore")
            .apply(lambda x: x.replace('"', "")),
            errors="coerce",
            format="%Y-%m-%d",
        )

        dataframe[EmployeeSchema.EMPLOYEE_STATE] = dataframe[
            EmployeeSchema.EMPLOYEE_STATE
        ].astype(str, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_TERMINATION_DATE] = to_datetime(
            dataframe[EmployeeSchema.EMPLOYEE_TERMINATION_DATE]
            .astype(str, errors="ignore")
            .apply(lambda x: x.replace('"', "")),
            errors="coerce",
            format="%Y-%m-%d",
        )

        dataframe[
            EmployeeSchema.USER_SETTINGS_STAFFING_EMPLOYEE_POSITION_TYPE
        ] = dataframe[
            EmployeeSchema.USER_SETTINGS_STAFFING_EMPLOYEE_POSITION_TYPE
        ].astype(
            str, errors="ignore"
        )

        dataframe[EmployeeSchema.EMPLOYEE_AVAILABILITY] = dataframe[
            EmployeeSchema.EMPLOYEE_AVAILABILITY
        ].astype(str, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_MINIMUM_DAILY_CAPACITY] = dataframe[
            EmployeeSchema.EMPLOYEE_MINIMUM_DAILY_CAPACITY
        ].astype(int, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_MAXIMUM_DAILY_CAPACITY] = dataframe[
            EmployeeSchema.EMPLOYEE_MAXIMUM_DAILY_CAPACITY
        ].astype(int, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_MINIMUM_WEEKLY_CAPACITY] = dataframe[
            EmployeeSchema.EMPLOYEE_MINIMUM_WEEKLY_CAPACITY
        ].astype(int, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_MAXIMUM_WEEKLY_CAPACITY] = dataframe[
            EmployeeSchema.EMPLOYEE_MAXIMUM_WEEKLY_CAPACITY
        ].astype(int, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_LANGUAGE] = dataframe[
            EmployeeSchema.EMPLOYEE_LANGUAGE
        ].astype(str, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_AGE] = dataframe[
            EmployeeSchema.EMPLOYEE_AGE
        ].astype(int, errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_LATITUDE] = dataframe[
            EmployeeSchema.EMPLOYEE_LATITUDE
        ].astype("float", errors="ignore")

        dataframe[EmployeeSchema.EMPLOYEE_LONGITUDE] = dataframe[
            EmployeeSchema.EMPLOYEE_LONGITUDE
        ].astype("float", errors="ignore")

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {"name": self.__class__.__name__}
