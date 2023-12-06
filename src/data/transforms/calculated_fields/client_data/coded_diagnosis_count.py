"""
This class is used to clean the diagnosis of the client
"""

import re

from typing import Tuple
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.utility.environment import Environment
from src.utility.configs.config import Config


class CodedDiagnosticCount(DataframeTransform):
    """
    This class is used to clean the diagnosis of the client.

    Args:
        column: The column name.
        column_count_name: The column name for the count of coded diagnoses.
    """

    def __init__(
        self,
        column: str = None,
        column_count_name: str = None,
    ) -> None:
        assert column is not None
        self.column = column
        self.column_count_name = column_count_name

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(desc="Counting coded diagnoses", position=3, leave=False)

        diagnosis_column = dataframe[self.column]
        dataframe[self.column_count_name] = diagnosis_column.progress_apply(
            self.count_coded_diagnoses
        )
        return super().__call__(dataframe, errors, conf, env)

    def count_coded_diagnoses(self, tokens):
        """
        This function returns the number of coded diagnoses found in the DIAGNOSIS column
        """
        # REGEX pattern for codes in ICD-10-CM Diagnostic Coding System
        pattern = r"\b[a-z]{1,2}\d+((\.\d+)?[a-z]*)?\b"
        count = 0
        for token in tokens:
            if re.match(pattern, token):
                count += 1
        return count

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "column": self.column.name,
            "column_count_name": self.column_count_name.name,
        }
