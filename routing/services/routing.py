import requests


OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def get_route(start, finish):
    """
    Get the driving route between two coordinates.

    start and finish must contain:
        latitude
        longitude
    """

    start_coordinates = (
        f"{start['longitude']},{start['latitude']}"
    )

    finish_coordinates = (
        f"{finish['longitude']},{finish['latitude']}"
    )

    coordinates = (
        f"{start_coordinates};"
        f"{finish_coordinates}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
    }

    url = f"{OSRM_URL}/{coordinates}"

    response = requests.get(
        url,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        raise ValueError(
            f"Routing failed: {data.get('code')}"
        )

    route = data["routes"][0]

    return {
        "distance_meters": route["distance"],
        "duration_seconds": route["duration"],
        "geometry": route["geometry"],
    }