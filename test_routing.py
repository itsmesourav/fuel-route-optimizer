from routing.services.geocoding import geocode_location
from routing.services.routing import get_route


print("Geocoding start...")

start = geocode_location("New York, NY")

print("Start:")
print(start)


print("\nGeocoding finish...")

finish = geocode_location("Chicago, IL")

print("Finish:")
print(finish)


print("\nGetting route...")

route = get_route(start, finish)

print("\nRoute result:")

print(
    "Distance:",
    route["distance_meters"],
    "meters"
)

print(
    "Duration:",
    route["duration_seconds"],
    "seconds"
)

print(
    "Geometry type:",
    route["geometry"]["type"]
)

print(
    "Number of route points:",
    len(route["geometry"]["coordinates"])
)