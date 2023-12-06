"""
Generate Statistics
"""

from os import makedirs, path
from pandas import DataFrame
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
from src.utility.environment import Environment
from src.data.schema.statistics_schema import StatisticSchema


def generate_statistics(
    input_df: DataFrame,
    env: Environment,
    filename: str,
    sub_directory: str = ".",
    save: bool = True,
) -> DataFrame:
    """
    This function computes statistics for the columns of a dataframe and stores them to a csv file.

    Args:
        input_df (pd.DataFrame): The dataframe for which to generate statistics
        env (Environment): An Environment object containing the environment variables
        filename (str): The filename
        sub_directory (str): The subdirectory to save the csv file. Defaults to ".".
        save (bool): Whether to save the stats to a csv file. Defaults to True.
    """

    # Initialize an empty DataFrame to store the statistics
    statistics_list = []

    # Iterate over each column in the input DataFrame
    for column_name in input_df.columns:
        column_data = input_df[column_name]
        data_type = str(column_data.dtype)
        row_count = len(column_data)
        null_count = column_data.isnull().sum()

        # Initialize statistics dictionary
        statistics = {
            StatisticSchema.COLUMN_NAME: str(
                column_name
            ).upper(),  # SCREAMING_SNAKE_CASE
            StatisticSchema.DATA_TYPE: data_type,
            StatisticSchema.ROW_COUNT: row_count,
            StatisticSchema.NULL_COUNT: null_count,
        }

        # For numeric columns, calculate additional statistics
        if is_numeric_dtype(column_data):
            statistics[StatisticSchema.MIN] = column_data.min()
            statistics[StatisticSchema.FIRST_QUARTILE] = column_data.quantile(0.25)
            statistics[StatisticSchema.MEDIAN] = column_data.median()
            statistics[StatisticSchema.THIRD_QUARTILE] = column_data.quantile(0.75)
            statistics[StatisticSchema.MAX] = column_data.max()
            statistics[StatisticSchema.MEAN] = column_data.mean()
            statistics[StatisticSchema.STD_DEV] = column_data.std()
            statistics[StatisticSchema.MODE] = column_data.mode().iloc[0]

        # For date-like columns, calculate MIN and MAX as the earliest and latest dates
        elif is_datetime64_any_dtype(column_data):
            statistics[StatisticSchema.MIN] = column_data.min()
            statistics[StatisticSchema.MAX] = column_data.max()

        # Append the statistics to the list
        statistics_list.append(statistics)

    # Create the output DataFrame from the list of dictionaries
    output_df = DataFrame(statistics_list)

    if save:
        if not path.exists(path.join(env.stats_dir, sub_directory)):
            makedirs(path.join(env.stats_dir, sub_directory))

        output_df.to_csv(path.join(env.stats_dir, sub_directory, f"{filename}.csv"))

    return output_df
