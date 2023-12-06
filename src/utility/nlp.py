"""
This module contains an NLP class for text cleaning
"""
import re
import json
import os
import nltk
import gensim
import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
from torch.nn.utils.rnn import pad_sequence
from src.utility.tsne_helper import default_tsne_config, build_tsne

MODEL_FOLDER = ".models/w2v_models/"


class NLP:
    """
    This class contains functions commonly used for treating textual data
    """

    def __init__(self, stopwords: set = None, corpus: dict = None) -> None:
        if stopwords is None:
            stopwords = set()
        if corpus is None:
            corpus = {}
        self.stopwords = stopwords
        self.corpus = corpus
        nltk.download("stopwords", quiet=True)
        nltk.download("punkt", quiet=True)

    def remove_numbers(self, text: str) -> str:
        """
        This function removes all numerical characters in a string
        """
        clean_text = re.sub(r"\d", " ", text)
        return clean_text

    def remove_special_chars(self, text: str) -> str:
        """
        This function removes all special characters in a string
        """
        clean_text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        return clean_text

    def remove_non_alpha(self, text: str) -> str:
        """
        This function removes all non alphabetical characters in a string
        """
        no_specials_text = self.remove_special_chars(text)
        clean_text = self.remove_numbers(no_specials_text)
        return clean_text

    def clean_string(
        self, text: str, equivalent_terms: dict, additional_token_conditions: [] = None
    ) -> [str]:
        """
        This function cleans a string by analyzing it and appends equivalent terms based on it's tokens
        """
        tokens = self.analyze_string(text, additional_token_conditions)
        augmented_tokens = self.augment_tokens(tokens, equivalent_terms)
        return augmented_tokens

    def analyze_string(
        self,
        text: str,
        additional_token_conditions: [] = None,
    ) -> [str]:
        """
        This function removes non alphabetical characters from a string and tokenizes it
        """
        text = self.remove_non_alpha(text.lower())
        tokens = self.tokenize_string(text, additional_token_conditions)
        return tokens

    def tokenize_string(
        self, text: str, additional_token_conditions: [] = None
    ) -> [str]:
        """
        This function tokenizes words of a string if they meet certain conditions
        """
        tokens = []
        for token in nltk.tokenize.word_tokenize(text):
            if self.token_meets_conditions(token, additional_token_conditions):
                tokens.append(token)

        return tokens

    def token_meets_conditions(
        self, token: str, additional_token_conditions: [] = None
    ) -> bool:
        """
        This function checks if a token meets the specified conditions, minimally checks if the token is a stopword
        """
        if not additional_token_conditions:
            return token not in self.stopwords

        # Check additional conditions if provided
        for condition in additional_token_conditions:
            if not condition(token, self.corpus):
                return False

        # Always check if the token is not in stopwords
        return token not in self.stopwords

    def augment_tokens(self, tokens: [str], equivalent_terms: dict) -> [str]:
        """
        This function appends the equivalent tokens when meeting certain typing errors or abbreviations
        """
        for token in tokens:
            if token in equivalent_terms:
                tokens.extend(equivalent_terms[token])

        return tokens

    def create_corpus(self, text: str) -> [str]:
        """
        This function creates the corpus
        """
        tokens = self.analyze_string(text, [])
        self.update_corpus(tokens)
        return tokens

    def update_corpus(self, tokens: [str]) -> None:
        """
        This function updates the corpus
        """
        for token in tokens:
            if token in self.corpus:
                self.corpus[token] += 1
            else:
                self.corpus[token] = 1

    def write_corpus_to_file(self, path: str, file_name: str) -> None:
        """
        This function writes the entire corpus in a JSON file at the specified path
        """
        file_path = f"{path}/{file_name}"

        with open(file_path, "w", encoding="utf-8") as unique_words_file:
            json.dump(
                dict(
                    sorted(self.corpus.items(), key=lambda item: item[1], reverse=True)
                ),
                unique_words_file,
                indent=2,
            )

    def create_word2vec_model(
        self,
        tokenized_data: [[str]],
        model_name: str,
        model_folder: str = MODEL_FOLDER,
        vector_size: int = 100,
        window: int = 5,
        min_count: int = 1,
        skip_gram: int = 0,
        negative: int = 5,
        hierarchical_softmax: int = 0,
        workers: int = 4,
        epochs: int = 10,
    ) -> any:
        """
        This function creates a W2V model for specific data
        """

        if not os.path.isdir(model_folder):
            os.makedirs(model_folder, exist_ok=True)

        model_location = model_folder + model_name
        model = gensim.models.Word2Vec(
            tokenized_data,
            vector_size=vector_size,
            window=window,
            min_count=min_count,
            sg=skip_gram,
            negative=negative,
            hs=hierarchical_softmax,
            workers=workers,
            epochs=epochs,
        )

        model.save(model_location)
        return model

    def vectorize_tokens(
        self, tokens: [str], model: any, add_padding: bool = False
    ) -> any:
        """
        This function creates padded tensors from tokens using a W2V model
        """
        tensor_sequences = []
        for token in tokens:
            if str(token) in model.wv:
                tensor_sequences.append(torch.Tensor([model.wv[str(token)]]))

        # Pad sequences for constant size
        if add_padding:
            tensor_sequences = pad_sequence(
                tensor_sequences, batch_first=True, padding_value=0.0
            )

        return tensor_sequences

    def visualize_vectors(
        self,
        model_name: str,
        tsne_config: dict = None,
        model_folder: str = MODEL_FOLDER,
        graph_folder: str = ".plots/W2V_Models/",
    ) -> dict:
        """
        This function creates a 2d graph to represent the token vectors and saves it to a png
        """

        if not os.path.isdir(graph_folder):
            os.makedirs(graph_folder, exist_ok=True)

        model_location = model_folder + model_name
        model = gensim.models.KeyedVectors.load(model_location)
        word_vectors_dict = {word: model.wv[word] for word in model.wv.index_to_key}
        dataframe = pd.DataFrame.from_dict(word_vectors_dict, orient="index")

        if tsne_config is None:
            tsne_config = default_tsne_config

        # Perplexity is a hyperparameter that should be tweaked, however must be lower than df.shape(0)
        tsne_config["perplexity"] = dataframe.shape[0] - 1

        tsne = build_tsne(tsne_config=tsne_config)
        tsne_df = tsne.fit_transform(dataframe)

        sns.set()

        plt.subplots(figsize=(11.7, 8.27))
        sns.scatterplot(x=tsne_df[:, 0], y=tsne_df[:, 1], alpha=0.5)

        texts = []
        words_to_plot = list(np.arange(0, 400, 10))

        for word_index in words_to_plot:
            if word_index < len(tsne_df):
                texts.append(
                    plt.text(
                        tsne_df[word_index, 0],
                        tsne_df[word_index, 1],
                        dataframe.index[word_index],
                        fontsize=14,
                    )
                )

        adjust_text(
            texts,
            force_points=0.4,
            force_text=0.4,
            expand_points=(2, 1),
            expand_text=(1, 2),
            arrowprops={"arrowstyle": "-", "color": "black", "lw": 0.5},
        )
        plt.savefig(f"{graph_folder}/{model_name.upper()}_TOKEN_VECTORS_PLOT.png")
        plt.clf()

        return tsne_config
