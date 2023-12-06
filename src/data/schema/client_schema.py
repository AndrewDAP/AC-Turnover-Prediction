"""
Client data schema.
"""

from src.data.schema.schema import Schema
from src.data.schema.schema_column import SchemaColumn


class _ClientSchemaRaw(Schema):
    """
    Client schema. Raw data.
    """

    CLIENT_ID = SchemaColumn(name="CLIENT_ID")
    AGE = SchemaColumn(name="AGE")
    ADMISSION_DATE = SchemaColumn(name="ADMISSION_DATE")
    DISCHARGE_DATE = SchemaColumn(name="DISCHARGE_DATE")
    PREFERRED_LANGUAGE = SchemaColumn(name="PREFERRED_LANGUAGE")
    LENGTH_OF_STAY = SchemaColumn(name="LENGTH_OF_STAY")
    HAS_ADLS = SchemaColumn(name="HAS_ADLS")
    COUNTRY = SchemaColumn(name="COUNTRY")
    GENDER = SchemaColumn(name="GENDER")
    LATITUDE = SchemaColumn(name="latitute")
    LONGITUDE = SchemaColumn(name="longitude")
    DIAGNOSIS = SchemaColumn(name="DIAGNOSIS")


ClientSchemaRaw = _ClientSchemaRaw()


class _ClientSchema(Schema):
    """
    Client schema. after cleaning
    """

    CLIENT_ID = SchemaColumn(
        name="CLIENT_ID",
        parents=[ClientSchemaRaw.CLIENT_ID],
    )

    CLIENT_AGE = SchemaColumn(
        name="CLIENT_AGE",
        parents=[ClientSchemaRaw.AGE],
    )

    CLIENT_ADMISSION_DATE = SchemaColumn(
        name="CLIENT_ADMISSION_DATE",
        parents=[ClientSchemaRaw.ADMISSION_DATE],
        is_datetime=True,
    )

    CLIENT_DISCHARGE_DATE = SchemaColumn(
        name="CLIENT_DISCHARGE_DATE",
        parents=[ClientSchemaRaw.DISCHARGE_DATE],
        is_datetime=True,
    )

    CLIENT_PREFERRED_LANGUAGE = SchemaColumn(
        name="CLIENT_PREFERRED_LANGUAGE",
        parents=[ClientSchemaRaw.PREFERRED_LANGUAGE],
    )

    CLIENT_LENGTH_OF_STAY = SchemaColumn(
        name="CLIENT_LENGTH_OF_STAY",
        parents=[ClientSchemaRaw.LENGTH_OF_STAY],
    )

    CLIENT_HAS_ADLS = SchemaColumn(
        name="CLIENT_HAS_ADLS",
        parents=[ClientSchemaRaw.HAS_ADLS],
    )

    CLIENT_COUNTRY = SchemaColumn(
        name="CLIENT_COUNTRY",
        parents=[ClientSchemaRaw.COUNTRY],
    )

    CLIENT_GENDER = SchemaColumn(
        name="CLIENT_GENDER",
        parents=[ClientSchemaRaw.GENDER],
    )

    CLIENT_LATITUDE = SchemaColumn(
        name="CLIENT_LATITUDE",
        parents=[ClientSchemaRaw.LATITUDE],
    )

    CLIENT_LONGITUDE = SchemaColumn(
        name="CLIENT_LONGITUDE",
        parents=[ClientSchemaRaw.LONGITUDE],
    )

    CLIENT_DIAGNOSIS = SchemaColumn(
        name="CLIENT_DIAGNOSIS",
        parents=[ClientSchemaRaw.DIAGNOSIS],
    )

    CLIENT_CODED_DIAGNOSIS_COUNT = SchemaColumn(
        name="CLIENT_CODED_DIAGNOSIS_COUNT",
        parents=[CLIENT_DIAGNOSIS],
    )


ClientSchema = _ClientSchema(
    parents=[ClientSchemaRaw],
)
