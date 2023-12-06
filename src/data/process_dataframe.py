"""
This module is used to process a dataframe
"""

from os import path
from typing import List, Optional, Tuple
from tqdm.autonotebook import tqdm
from pandas import DataFrame, read_csv, concat
from src.utility.configs.config import Config
from src.utility.environment import Environment
from src.data.transforms.transform import DataframeTransform
from src.data.error.error_dataframe import ErrorDataFrame


def process_dataframe(
    *,
    dataframe: DataFrame = None,
    load_dataframe_csv_path: path = None,
    transforms: Optional[List[DataframeTransform]] = None,
    conf: Config = None,
    env: Environment = None,
    limit: int = None,
) -> Tuple[DataFrame, ErrorDataFrame]:
    """
    This function is used to process a dataframe

    Args:
        dataframe (DataFrame): The dataframe to process
        load_dataframe_csv_path (os.path): The path to the csv file to load
        transforms (Optional[List[CSVTransform]]): The transforms to apply to the dataframe
        conf (Config): The config.
        env (Environment): The environment
        limit (int): The number of rows to process

    Returns:
        Tuple[DataFrame, ErrorDataFrame]: The processed dataframe and the errors
    """
    assert dataframe is not None or load_dataframe_csv_path is not None
    assert conf is not None
    assert env is not None

    if dataframe is None:
        dataframe = read_csv(
            load_dataframe_csv_path, encoding="utf-8", low_memory=False
        )

        if conf.is_test_run:
            dataframe_copy = dataframe.copy()
            for column in dataframe_copy.columns:
                if "_ID" in column:
                    offset = max(dataframe_copy[column].unique()) + 1
                    dataframe_copy[column].add(offset)

            dataframe = concat([dataframe, dataframe_copy], ignore_index=True)

        if limit is not None:
            dataframe = dataframe.head(limit)
    errors = ErrorDataFrame(dataframe, config=conf)

    if transforms is not None:
        with tqdm(total=len(transforms), position=1, leave=False) as progress_bar:
            for transform in transforms:
                progress_bar.set_description(f"Applying {transform.__class__.__name__}")
                dataframe, errors = transform(dataframe, errors, conf, env)
                progress_bar.update(1)

    return dataframe, errors
