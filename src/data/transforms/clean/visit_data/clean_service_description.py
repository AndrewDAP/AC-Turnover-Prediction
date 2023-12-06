"""
This class is used to clean the service description of the visit
"""

from typing import Tuple
import nltk
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from src.data.transforms.clean.visit_data.service_description_const import (
    MIN_FREQUENCY,
    EQUIVALENT_TERMS,
    STOP_WORDS_MASK,
    CUSTOM_STOP_WORDS,
)
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.utility.nlp import NLP


class CleanServiceDescription(DataframeTransform):
    """
    This class is used to clean the service description of the visit

    Args:
        column: The column to clean.
    """

    def __init__(
        self,
        column: str = None,
    ) -> None:
        assert column is not None
        self.column = column

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(
            desc=f"CleanServiceDescription cleaning {self.column}",
            position=3,
            leave=False,
        )
        service_description_column = dataframe[self.column]
        nlp_helper = NLP()

        nlp_helper.stopwords = set(
            nltk.corpus.stopwords.words("english") + CUSTOM_STOP_WORDS
        ) - set(STOP_WORDS_MASK)

        dataframe[self.column] = service_description_column.progress_apply(
            nlp_helper.create_corpus
        )
        additional_token_conditions = [
            self.token_is_alpha,
            self.token_has_min_frequency,
        ]

        dataframe[self.column] = service_description_column.progress_apply(
            nlp_helper.clean_string,
            args=(EQUIVALENT_TERMS, additional_token_conditions),
        )

        return super().__call__(dataframe, errors, conf, env)

    def token_is_alpha(self, token: str, _) -> bool:
        """
        This function returns if the token consist of only alphabetical characters
        """
        return token.isalpha()

    def token_has_min_frequency(self, token: str, corpus: dict) -> bool:
        """
        This function returns if the token meets the minimal frequency to be maintained
        """
        if token not in corpus:
            return False
        return corpus[token] >= MIN_FREQUENCY

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
            "column": self.column.name,
        }
