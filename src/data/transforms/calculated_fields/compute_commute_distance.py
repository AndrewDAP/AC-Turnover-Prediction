"""
Commute
"""

from typing import Optional, Tuple
import math
from pandas import DataFrame
from tqdm.autonotebook import tqdm
from src.data.transforms.transform import DataframeTransform
from src.utility.configs.config import Config
from src.utility.environment import Environment
from src.data.error.error_dataframe import ErrorDataFrame
from src.data.schema.augmented_visit_schema import AugmentedVisitSchema


class ComputeCommuteDistance(DataframeTransform):
    """
    This class defines dataframe transformations related to employee commute
    """

    def __init__(self, max_distance_km: Optional[int] = 150) -> None:
        self.max_distance_km = max_distance_km
        super().__init__()

    def __call__(
        self,
        dataframe: DataFrame,
        errors: ErrorDataFrame,
        conf: Config,
        env: Environment,
    ) -> Tuple[DataFrame, ErrorDataFrame]:
        tqdm.pandas(desc="Computing commute distance", position=3, leave=False)

        dataframe[
            AugmentedVisitSchema.EMPLOYEE_COMMUTE_DISTANCE.name
        ] = dataframe.progress_apply(self.compute_commute_distance, axis=1)
        return super().__call__(dataframe, errors, conf, env)

    def to_dict(self) -> dict:
        """
        This method returns the dictionary representation of the class.

        Returns:
            dict: The dictionary representation of the class.
        """
        return {
            "name": self.__class__.__name__,
        }

    def compute_commute_distance(self, row):
        """Computes the estimated commute distance of an employee for a given visit using the Haversine formula.

        Args:
            row (_type_): _description_
        """
        return self.haversine_distance(
            row[AugmentedVisitSchema.CLIENT_LATITUDE.name],
            row[AugmentedVisitSchema.CLIENT_LONGITUDE.name],
            row[AugmentedVisitSchema.EMPLOYEE_LATITUDE.name],
            row[AugmentedVisitSchema.EMPLOYEE_LONGITUDE.name],
        )

    def haversine_distance(
        self,
        lat1: Optional[float],
        lon1: Optional[float],
        lat2: Optional[float],
        lon2: Optional[float],
    ):
        """
        Calculate the Haversine distance between two sets of coordinates in kilometers.

        Parameters:
            lat1 (float or None): Latitude of the first point (in degrees).
            lon1 (float or None): Longitude of the first point (in degrees).
            lat2 (float or None): Latitude of the second point (in degrees).
            lon2 (float or None): Longitude of the second point (in degrees).

        Returns:
            float or None: The distance between the two points in kilometers, or None if any input is invalid.
        """
        # pylint: disable=invalid-name
        # Check if any input is None
        if None in {lat1, lon1, lat2, lon2}:
            return None

        try:
            # Convert latitude and longitude from degrees to radians
            lat1_rad = math.radians(lat1)
            lon1_rad = math.radians(lon1)
            lat2_rad = math.radians(lat2)
            lon2_rad = math.radians(lon2)
        except (TypeError, ValueError):
            # Handle invalid input data types or values
            return None

        # Radius of the Earth in kilometers
        earth_radius = 6371.0

        # Haversine formula
        distance_lon = lon2_rad - lon1_rad
        distance_lat = lat2_rad - lat1_rad
        a = (
            math.sin(distance_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(distance_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c

        if distance > self.max_distance_km:
            return None

        return distance
