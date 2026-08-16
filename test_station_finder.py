from routing.services.geocoding import geocode_location
from routing.services.routing import get_route
from routing.services.station_finder import find_nearby_stations


print("1. Geocoding start...")

start = geocode_location("New York, NY")

print("Start:", start)


print("\n2. Geocoding finish...")

finish = geocode_location("Chicago, IL")

print("Finish:", finish)


print("\n3. Getting route...")

route = get_route(start, finish)

route_distance_miles = (
    route["distance_meters"] / 1609.344
)

print(
    "Route distance:",
    round(route_distance_miles, 2),
    "miles"
)


print("\n4. Finding fuel stations near route...")

nearby_stations = find_nearby_stations(
    route["geometry"],
    radius_miles=10
)


print(
    "Nearby stations found:",
    len(nearby_stations)
)


print("\n5. Stations along the route:")

print(
    nearby_stations[
        [
            "station_id",
            "station_name",
            "city",
            "state",
            "price",
            "distance_to_route_miles",
            "route_position_miles",
        ]
    ].head(20).to_string(
        index=False
    )
)