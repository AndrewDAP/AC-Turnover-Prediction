"""Helper class to set dataframe types
"""

from pandas import DataFrame, to_datetime


def set_datetime(dataframe: DataFrame, column_names: [str]):
    """helper function to set dataframe columns as datetime

    Args:
        dataframe (DataFrame): the dataframe to modify
        column_names (str]): the columns for which to set the type as datetime

    Returns:
        Dataframe: the updated dataframe
    """
    for column_name in column_names:
        dataframe[column_name] = to_datetime(
            dataframe[column_name]
            .astype(str, errors="ignore")
            .apply(lambda x: x.replace('"', "")),
            errors="coerce",
            format="%Y-%m-%d",
        )
    return dataframe
