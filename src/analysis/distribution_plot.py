"""
Distribution Plot
"""
from os import makedirs, path
from typing import List, Literal, Union
from pandas.plotting import PlotAccessor
from pandas import DataFrame, Series
from tqdm.autonotebook import tqdm
from src.utility.environment import Environment


def distribution_plot(
    dataframe: DataFrame,
    columns: Union[str, List[str]],
    env: Environment,
    sub_directory: str = ".",
    date_by: Literal["day_of_week", "month", "year", "hour"] = "day_of_week",
    save: bool = True,
) -> None:
    """
    This function is used to plot the distribution of a column.

    Args:
        dataframe (DataFrame): The dataframe to plot.
        columns (Union[str, List[str]]): The column to plot.
        sub_directory (str): The subdirectory to save the plot. Defaults to ".".
        date_by (Literal["day_of_week", "month", "year"]): The date breakdown to plot. Defaults to "day_of_week".
        save (bool): Whether to save the plot. Defaults to True.
    """
    tqdm.pandas(
        desc=f"Plotting Distribution for {sub_directory}", position=3, leave=False
    )
    for column in [columns] if isinstance(columns, str) else columns:
        if dataframe[column].isna().all().all():
            continue

        plot: PlotAccessor
        values: Series = dataframe[column]
        if dataframe[column].dtype in [
            "datetime64[ns]",
            "<M8[ns]",
            "datetime64[ns, UTC]",
            "<M8[ns, UTC]",
        ]:
            if date_by == "day_of_week":
                values = dataframe[column].progress_apply(lambda x: x.dayofweek)
            elif date_by == "month":
                values = dataframe[column].progress_apply(lambda x: x.month)
            elif date_by == "year":
                values = dataframe[column].progress_apply(lambda x: x.year)
            elif date_by == "hour":
                values = dataframe[column].progress_apply(lambda x: x.hour)

        values = values.value_counts().sort_index()
        plot = values.plot(
            kind="line" if len(values.index) > 15 else "bar",
            title=f"{column} Distribution",
        )
        plot.set_ylabel("Count")

        if save:
            if not path.exists(path.join(env.plots_dir, sub_directory)):
                makedirs(path.join(env.plots_dir, sub_directory))

            plot.figure.savefig(
                path.join(env.plots_dir, sub_directory, f"{column}_distribution.png"),
                bbox_inches="tight",
            )
        plot.figure.clf()
