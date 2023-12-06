"""
This module contains the ExplanationConfig class.
"""

from hashlib import new
from json import dumps


class ExplanationConfig:
    """
    This class is used to specify the configuration for the explanation phase.

        Args:
        nsamples: The number of samples to use for each shap explanation.
        seed: The seed to use for the explanation.
        sample_size: The size of the sample to use for the explanation.
    """

    def __init__(
        self,
        *,
        nsamples: int = None,
        seed: int = None,
        sample_size: int = None,
    ) -> None:
        assert nsamples is not None
        assert seed is not None
        assert sample_size is not None
        self.nsamples = nsamples
        self.seed = seed
        self.sample_size = sample_size

    def to_dict(self) -> dict:
        """
        This method returns the configuration as a dictionary.

        Returns:
            dict: The configuration as a dictionary.
        """

        return {
            "nsamples": self.nsamples,
            "seed": self.seed,
            "sample_size": self.sample_size,
        }

    def __hash__(self) -> int:
        hasher = new("sha256")
        hasher.update(dumps(self.to_dict(), sort_keys=True).encode())
        return int(hasher.hexdigest(), 16)

    def __repr__(self) -> str:
        return str(self.to_dict())
