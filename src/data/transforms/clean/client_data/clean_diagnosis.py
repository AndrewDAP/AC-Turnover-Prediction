"""
This class is used to clean the diagnosis of the client
"""

from typing import Tuple
import ast
import nltk
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from src.data.transforms.clean.client_data.diagnosis_const import (
    TRAILING_KEY_WORDS,
    CUSTOM_STOP_WORDS,
    COMPOSED_TERMS_ROOTS,
    REPLACEABLE_CHARACTERS,
)
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.transforms.transform import DataframeTransform
from src.utility.environment import Environment
from src.utility.configs.config import Config
from src.utility.nlp import NLP


class CleanDiagnosis(DataframeTransform):
    """
    This class is used to clean the diagnosis of the client.

    Args:
        column: The column name.
    """

    def __init__(
        self,
        column: str = None,
    ) -> None:
        assert column is not None
        self.column = column

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

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(
            desc=f"CleanDiagnosis Cleaning {self.column}", position=3, leave=False
        )
        diagnosis_column = dataframe[self.column]
        nlp_helper = NLP()
        nlp_helper.stopwords = set(
            nltk.corpus.stopwords.words("english") + CUSTOM_STOP_WORDS
        )
        dataframe[self.column] = diagnosis_column.progress_apply(
            self.clean_diagnosis, args=(nlp_helper,)
        )
        return super().__call__(dataframe, errors, conf, env)

    def clean_diagnosis(self, initial_diagnosis_string: str, nlp_helper: NLP) -> [str]:
        """
        This function cleans out the diagnosis value
        """

        # Ignore instances where DIAGNOSIS is empty
        if initial_diagnosis_string == "":
            return []

        joined_diagnosis_list = []

        # Takes  dict
        initial_dict = ast.literal_eval(initial_diagnosis_string.lower())

        for initial_entry in initial_dict.values():
            if initial_entry == "":
                continue

            for keyword in TRAILING_KEY_WORDS:
                initial_entry = self.remove_trailing_information(keyword, initial_entry)

            joined_diagnosis_list = self.concat_diagnosis(
                initial_entry, joined_diagnosis_list
            )

        # Removes all duplicate entries, as some diagnosis entries were doubled
        joined_diagnoses_string = " ".join(set(joined_diagnosis_list))

        tokens = self.tokenize_diagnosis(joined_diagnoses_string, nlp_helper)
        nlp_helper.update_corpus(tokens)
        return tokens

    def concat_diagnosis(self, raw_diagnosis: str, joined_diagnosis_list: []) -> [str]:
        """
        This function concatenates sub-diagnoses that start with a " " to the last main diagnosis
        """

        # For the one row, who's first diagnosis start with a " " (typo)
        if len(joined_diagnosis_list) == 0:
            raw_diagnosis = raw_diagnosis.strip()

        # Main diagnoses are appended to the list
        if raw_diagnosis[0] != " ":
            joined_diagnosis_list.append(raw_diagnosis)

        # - Sub diagnoses are concatenated to the last main diagnosis in the list
        #   (sub diagnoses always start with a whitespace)
        else:
            joined_diagnosis_list.append(
                joined_diagnosis_list.pop() + "," + raw_diagnosis
            )

        return joined_diagnosis_list

    def remove_trailing_information(self, keyword: str, text: str) -> str:
        """
        Remove any information following the words "without", "except" and "not" as any following
        information is unwanted information
        """

        word_pos = text.find(keyword)
        if word_pos != -1:
            return text[:word_pos]

        return text

    # Tokenizing the diagnosis is more complex and thus has it's own method
    # Will be refactored to use NLP functions at a later date
    def tokenize_diagnosis(self, joined_diagnosis, nlp_helper: NLP) -> [str]:
        """
        This function removes stopwords from the diagnosis
        """

        for character in REPLACEABLE_CHARACTERS:
            joined_diagnosis = joined_diagnosis.replace(character[0], character[1])

        tokens = []

        for token in nltk.tokenize.word_tokenize(joined_diagnosis):
            # Multiple instances of single characters or dates and years in the diagnoses, all considered noise
            is_number = token.isdigit()
            in_stopwords = token in nlp_helper.stopwords
            is_single_letter = is_number and len(token) == 1

            # Concatenate numbers to words 'stage', 'covid' and 'type' and append as single token
            if len(tokens) != 0 and is_number and tokens[-1] in COMPOSED_TERMS_ROOTS:
                tokens.append(tokens.pop() + token)

            elif (
                not (in_stopwords or is_single_letter or is_number)
                and token not in tokens
            ):
                tokens.append(token)

        return tokens
