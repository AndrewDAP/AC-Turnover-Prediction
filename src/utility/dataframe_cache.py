"""
A module to represent a dataframe cache.
"""
from os import path, removedirs, makedirs
from typing import Optional
from pandas import DataFrame, read_pickle
from src.utility.environment import Environment


class DataFrameCache:
    """
    A class to represent a dataframe cache.

    Args:
        environment (Environment): The environment.
    """

    def __init__(self, environment: Environment) -> None:
        self.cache_dir = environment.cache_dir

    def add(self, *, key: int, value: DataFrame, sub_directory: str) -> None:
        """
        Cache the dataframe.

        Args:
            key (str): The key.
            value (DataFrame): The value.
        """
        directory_path = path.join(self.cache_dir, sub_directory)
        if not path.exists(directory_path):
            makedirs(directory_path)
        cache_path = path.join(self.cache_dir, sub_directory, f"{str(key)}.pkl")
        value.to_pickle(cache_path)

    def has(self, *, key: int, sub_directory: str) -> bool:
        """
        Whether the dataframe is cached.

        Args:
            key (str): The key.

        Returns:
            bool: Whether the dataframe is cached.
        """
        cache_path = path.join(self.cache_dir, sub_directory, f"{str(key)}.pkl")
        return path.exists(cache_path)

    def get(self, *, key: int, sub_directory: str) -> DataFrame:
        """
        Get the dataframe.

        Args:
            key (str): The key.

        Returns:
            DataFrame: The dataframe.
        """
        if not self.has(key=key, sub_directory=sub_directory):
            raise OSError(
                f"The dataframe {key} in sub_directory {sub_directory} is not present in cache."
            )

        cache_path = path.join(self.cache_dir, sub_directory, f"{str(key)}.pkl")

        return read_pickle(cache_path)

    def clear(self, sub_directory: Optional[str] = None) -> None:
        """
        Clear the cache.
        """
        cached_dir = (
            path.join(self.cache_dir, sub_directory)
            if sub_directory
            else self.cache_dir
        )

        removedirs(cached_dir)
