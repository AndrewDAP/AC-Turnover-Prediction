"""
Oversample the data using the given sampler.
"""
from typing import Tuple
from imblearn.over_sampling import (
    BorderlineSMOTE,
    KMeansSMOTE,
    SMOTEN,
    SVMSMOTE,
    SMOTENC,
    ADASYN,
    RandomOverSampler,
    SMOTE,
)
from numpy import ndarray
from src.utility.factory import Factory


class NoOverSampler:
    """
    No oversampling is performed.
    """

    def fit_resample(self, x: ndarray, y: ndarray) -> Tuple[ndarray, ndarray]:
        """
        args:
            x: The data to oversample.
            y: The labels to oversample.
        """
        return x, y


class OverSampler:
    """
    Oversample the data using the given sampler.

    args:
        name: The name of the sampler to use.
        *args: Positional arguments to pass to the sampler.
        **kwargs: Keyword arguments to pass to the sampler.
    """

    def __init__(self, name: str, *args, **kwargs):
        self.factory = Factory(
            registry={
                "BorderlineSMOTE": BorderlineSMOTE,
                "KMeansSMOTE": KMeansSMOTE,
                "SMOTEN": SMOTEN,
                "SVMSMOTE": SVMSMOTE,
                "SMOTENC": SMOTENC,
                "ADASYN": ADASYN,
                "RandomOverSampler": RandomOverSampler,
                "SMOTE": SMOTE,
                "NoOverSampler": NoOverSampler,
            }
        )
        self.sampler = self.factory.create(name, *args, **kwargs)

    def fit_resample(self, x: ndarray, y: ndarray) -> Tuple[ndarray, ndarray]:
        """
        args:
            x: The data to oversample.
            y: The labels to oversample.
        """
        return self.sampler.fit_resample(x, y)
