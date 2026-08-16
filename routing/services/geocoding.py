import requests
from functools import lru_cache


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "FuelRouteOptimizer/1.0 (backend assessment project)"
}


@lru_cache(maxsize=128)
def geocode_location(location):
    """
    Convert a location such as 'New York, NY'
    into latitude and longitude.

    Results are cached so repeated requests do not
    repeatedly call the geocoding service.
    """

    params = {
        "q": f"{location}, USA",
        "format": "json",
        "limit": 1,
        "countrycodes": "us",
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=HEADERS,
        timeout=10,
    )

    response.raise_for_status()

    results = response.json()

    if not results:
        raise ValueError(
            f"Could not find location: {location}"
        )

    result = results[0]

    return {
        "latitude": float(result["lat"]),
        "longitude": float(result["lon"]),
        "display_name": result["display_name"],
    }