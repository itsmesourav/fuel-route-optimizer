from .geocoding import geocode_location
from .routing import get_route
from .station_finder import find_nearby_stations
from .fuel_optimizer import optimize_fuel_stops


def calculate_route(start_location, finish_location):
    """
    Complete fuel-route calculation.

    Flow:
        location
        -> geocoding
        -> OSRM route
        -> nearby fuel stations
        -> fuel optimization
    """

    # --------------------------------------------------
    # 1. Geocode start
    # --------------------------------------------------

    start = geocode_location(
        start_location
    )

    # --------------------------------------------------
    # 2. Geocode finish
    # --------------------------------------------------

    finish = geocode_location(
        finish_location
    )

    # --------------------------------------------------
    # 3. Get road route
    # --------------------------------------------------

    route = get_route(
        start,
        finish
    )

    route_distance_miles = (
        route["distance_meters"]
        / 1609.344
    )

    route_duration_minutes = (
        route["duration_seconds"]
        / 60
    )

    # --------------------------------------------------
    # 4. Find fuel stations near route
    # --------------------------------------------------

    nearby_stations = (
        find_nearby_stations(
            route["geometry"],
            radius_miles=10
        )
    )

    # --------------------------------------------------
    # 5. Optimize fuel stops
    # --------------------------------------------------

    fuel_result = (
        optimize_fuel_stops(
            nearby_stations,
            route_distance_miles
        )
    )

    # --------------------------------------------------
    # 6. Build response
    # --------------------------------------------------

    return {
        "start": {
            "input": start_location,
            "latitude": start["latitude"],
            "longitude": start["longitude"],
            "display_name": start["display_name"],
        },

        "finish": {
            "input": finish_location,
            "latitude": finish["latitude"],
            "longitude": finish["longitude"],
            "display_name": finish["display_name"],
        },

        "route": {
            "distance_miles": round(
                route_distance_miles,
                2
            ),

            "duration_minutes": round(
                route_duration_minutes,
                2
            ),

            "geometry": route["geometry"],
        },

        "fuel": {
            "mpg": 10,

            "maximum_range_miles": 500,

            "starting_fuel_gallons": 50,

            "total_gallons_purchased": (
                fuel_result[
                    "total_gallons_purchased"
                ]
            ),

            "total_fuel_cost": (
                fuel_result[
                    "total_fuel_cost"
                ]
            ),

            "stops": fuel_result[
                "fuel_stops"
            ],
        },

        "candidate_station_count": len(
            nearby_stations
        ),
    }