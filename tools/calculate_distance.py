import math
from typing import Tuple

from smolagents import tool


@tool
def calculate_distance(
    origin_coords: Tuple[float, float],
    destination_coords: Tuple[float, float],
) -> float:
    """
    Calculate the great-circle distance between two points on Earth.

    Args:
        origin_coords: Tuple of (latitude, longitude) for the starting point
        destination_coords: Tuple of (latitude, longitude) for the destination

    Returns:
        float: The distance in kilometers

    Example:
        >>> # Chicago (41.8781° N, 87.6298° W) to Sydney (33.8688° S, 151.2093° E)
        >>> result = calculate_distance((41.8781, -87.6298), (-33.8688, 151.2093))
    """
    def to_radians(degrees: float) -> float:
        return degrees * (math.pi / 180)

    # Extract coordinates
    lat1, lon1 = map(to_radians, origin_coords)
    lat2, lon2 = map(to_radians, destination_coords)

    # Earth's radius in kilometers
    EARTH_RADIUS_KM = 6371.0

    # Calculate great-circle distance using the haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    distance = EARTH_RADIUS_KM * c

    return round(distance, 2)


if __name__ == "__main__":
    # Test the calculate_distance function
    distance = calculate_distance((41.8781, -87.6298), (-33.8688, 151.2093))
    print(f"Distance: {distance} km")
