"""
This class is used to categorize text fields
"""

import json
import os
from typing import Tuple
import pandas as pd
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.utility.environment import Environment
from src.utility.configs.config import Config

MAPPING_FOLDER = "src/mappings/"


class CategorizeTextField(DataframeTransform):
    """
    This class is used to categorize text fields

    Args:
        column: The column name.
    """

    def __init__(
        self,
        columns: [str] = None,
    ) -> None:
        assert columns is not None
        self.columns = columns

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        if not os.path.isdir(MAPPING_FOLDER):
            os.makedirs(MAPPING_FOLDER, exist_ok=True)

        tqdm.pandas(
            desc=f"Categorizing Text Column(s): {self.columns}", position=3, leave=False
        )

        for column in self.columns:
            category_mapping = dict(enumerate(dataframe[column].unique()))

            with open(
                f"{MAPPING_FOLDER}/{column}_mapping.json", "w", encoding="utf-8"
            ) as json_file:
                json.dump(category_mapping, json_file, indent=4)

            dataframe[column] = pd.Categorical(
                dataframe[column], categories=dataframe[column].unique(), ordered=True
            )
            dataframe[column] = dataframe[column].cat.codes

        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "columns": [str(column) for column in self.columns],
        }
