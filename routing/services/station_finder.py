from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


EARTH_RADIUS_MILES = 3958.8


def latlon_to_xy(latitude, longitude):
    """
    Convert latitude/longitude to approximate
    x/y coordinates in miles.
    """

    lat = np.radians(latitude)
    lon = np.radians(longitude)

    x = EARTH_RADIUS_MILES * lon * np.cos(lat)
    y = EARTH_RADIUS_MILES * lat

    return x, y


def haversine_distance(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculate distance between two coordinates
    in miles.
    """

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)

    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arcsin(
        np.sqrt(a)
    )

    return EARTH_RADIUS_MILES * c


def calculate_route_distances(route_coordinates):
    """
    Calculate cumulative distance from the beginning
    of the route for every route point.

    Returns an array where:

    index 0 = 0 miles
    index 1 = distance from start
    index 2 = distance from start
    ...
    """

    longitudes = route_coordinates[:, 0]
    latitudes = route_coordinates[:, 1]

    cumulative_distances = np.zeros(
        len(route_coordinates)
    )

    for i in range(1, len(route_coordinates)):

        distance = haversine_distance(
            latitudes[i - 1],
            longitudes[i - 1],
            latitudes[i],
            longitudes[i]
        )

        cumulative_distances[i] = (
            cumulative_distances[i - 1]
            + distance
        )

    return cumulative_distances


def load_stations():
    """
    Load the preprocessed fuel station dataset.
    """

    project_root = Path(
        __file__
    ).resolve().parents[2]

    file_path = (
        project_root
        / "routing"
        / "data"
        / "fuel-stations.csv"
    )

    return pd.read_csv(file_path)


def find_nearby_stations(
    route_geometry,
    radius_miles=10
):
    """
    Find fuel stations close to the route.

    Also calculates approximately how far each
    station is from the beginning of the route.
    """

    stations = load_stations()

    route_coordinates = np.array(
        route_geometry["coordinates"]
    )

    # --------------------------------------------
    # Calculate cumulative route distance
    # --------------------------------------------

    cumulative_distances = (
        calculate_route_distances(
            route_coordinates
        )
    )

    # --------------------------------------------
    # Convert route coordinates
    # --------------------------------------------

    route_longitudes = (
        route_coordinates[:, 0]
    )

    route_latitudes = (
        route_coordinates[:, 1]
    )

    route_x, route_y = latlon_to_xy(
        route_latitudes,
        route_longitudes
    )

    route_points = np.column_stack(
        (route_x, route_y)
    )

    # --------------------------------------------
    # Convert station coordinates
    # --------------------------------------------

    station_x, station_y = latlon_to_xy(
        stations["latitude"].values,
        stations["longitude"].values
    )

    station_points = np.column_stack(
        (station_x, station_y)
    )

    # --------------------------------------------
    # Spatial index
    # --------------------------------------------

    tree = cKDTree(route_points)

    distances, nearest_route_indexes = (
        tree.query(
            station_points,
            distance_upper_bound=radius_miles
        )
    )

    # --------------------------------------------
    # Add route information
    # --------------------------------------------

    stations["distance_to_route_miles"] = (
        distances
    )

    stations["route_position_miles"] = np.nan

    valid = (
        distances
        <= radius_miles
    )

    stations.loc[
        valid,
        "route_position_miles"
    ] = cumulative_distances[
        nearest_route_indexes[valid]
    ]

    # --------------------------------------------
    # Keep only nearby stations
    # --------------------------------------------

    nearby = stations[
        stations["distance_to_route_miles"]
        <= radius_miles
    ].copy()

    # --------------------------------------------
    # Sort by position along route
    # --------------------------------------------

    nearby = nearby.sort_values(
        by="route_position_miles"
    )

    return nearby.reset_index(
        drop=True
    )