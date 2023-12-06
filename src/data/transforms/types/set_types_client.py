"""
This module contains the SetTypesClient class, which is used to set the types of the client data.
"""
from pandas import DataFrame, to_datetime
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.client_schema import ClientSchema


class SetTypesClient(DataframeTransform):
    """
    This class is used to set the types of the client data.
    """

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> DataFrame:
        dataframe[ClientSchema.CLIENT_ID] = dataframe[ClientSchema.CLIENT_ID].astype(
            int, errors="ignore"
        )

        dataframe[ClientSchema.CLIENT_AGE] = dataframe[ClientSchema.CLIENT_AGE].astype(
            int, errors="ignore"
        )

        dataframe[ClientSchema.CLIENT_ADMISSION_DATE] = to_datetime(
            dataframe[ClientSchema.CLIENT_ADMISSION_DATE],
            errors="coerce",
        )

        dataframe[ClientSchema.CLIENT_DISCHARGE_DATE] = to_datetime(
            dataframe[ClientSchema.CLIENT_DISCHARGE_DATE],
            errors="coerce",
        )

        dataframe[ClientSchema.CLIENT_PREFERRED_LANGUAGE] = dataframe[
            ClientSchema.CLIENT_PREFERRED_LANGUAGE
        ].astype(str, errors="ignore")

        dataframe[ClientSchema.CLIENT_LENGTH_OF_STAY] = dataframe[
            ClientSchema.CLIENT_LENGTH_OF_STAY
        ].astype(int, errors="ignore")

        dataframe[ClientSchema.CLIENT_HAS_ADLS] = dataframe[
            ClientSchema.CLIENT_HAS_ADLS
        ].astype(int, errors="ignore")

        dataframe[ClientSchema.CLIENT_COUNTRY] = dataframe[
            ClientSchema.CLIENT_COUNTRY
        ].astype(str, errors="ignore")

        dataframe[ClientSchema.CLIENT_GENDER] = (
            dataframe[ClientSchema.CLIENT_GENDER]
            .fillna("O")
            .astype(str, errors="ignore")
        )

        dataframe[ClientSchema.CLIENT_LATITUDE] = dataframe[
            ClientSchema.CLIENT_LATITUDE
        ].astype(float, errors="ignore")

        dataframe[ClientSchema.CLIENT_LONGITUDE] = dataframe[
            ClientSchema.CLIENT_LONGITUDE
        ].astype(float, errors="ignore")

        dataframe[ClientSchema.CLIENT_DIAGNOSIS] = (
            dataframe[ClientSchema.CLIENT_DIAGNOSIS]
            .fillna("")
            .astype(str, errors="ignore")
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
