from routing.services.geocoding import geocode_location
from routing.services.routing import get_route
from routing.services.station_finder import find_nearby_stations
from routing.services.fuel_optimizer import optimize_fuel_stops


print("1. Geocoding start...")

start = geocode_location("Los Angeles, CA")

print("Start:", start)


print("\n2. Geocoding finish...")

finish = geocode_location("Chicago, IL")

print("Finish:", finish)


print("\n3. Getting route...")

route = get_route(
    start,
    finish
)

route_distance_miles = (
    route["distance_meters"] / 1609.344
)

print(
    "Route distance:",
    round(route_distance_miles, 2),
    "miles"
)


print("\n4. Finding nearby fuel stations...")

nearby_stations = find_nearby_stations(
    route["geometry"],
    radius_miles=10
)

print(
    "Nearby stations:",
    len(nearby_stations)
)


print("\n5. Optimizing fuel stops...")

result = optimize_fuel_stops(
    nearby_stations,
    route_distance_miles
)


print("\n================================")
print("FUEL OPTIMIZATION RESULT")
print("================================")

print(
    "Total gallons purchased:",
    result["total_gallons_purchased"]
)

print(
    "Total fuel cost: $",
    result["total_fuel_cost"]
)

print(
    "\nRecommended fuel stops:"
)

for stop in result["fuel_stops"]:

    print(
        f"{stop['station_name']} "
        f"({stop['city']}, {stop['state']})"
    )

    print(
        f"  Position: "
        f"{stop['route_position_miles']:.2f} miles"
    )

    print(
        f"  Price: "
        f"${stop['price_per_gallon']:.3f}/gallon"
    )

    print(
        f"  Gallons: "
        f"{stop['gallons_purchased']:.3f}"
    )

    print(
        f"  Cost: "
        f"${stop['fuel_cost']:.2f}"
    )

    print()