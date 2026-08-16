MAX_RANGE_MILES = 500.0
MPG = 10.0
MAX_FUEL_GALLONS = MAX_RANGE_MILES / MPG


def optimize_fuel_stops(
    stations,
    route_distance_miles,
    starting_fuel_gallons=MAX_FUEL_GALLONS,
):
    """
    Optimize fuel purchases along a route.

    Assumptions:
    - Vehicle starts with a full tank.
    - Maximum range = 500 miles.
    - Fuel economy = 10 MPG.
    - Maximum fuel capacity = 50 gallons.

    Strategy:
    - Travel to a station first.
    - Once we arrive, decide how much fuel to buy.
    - If a cheaper reachable station exists, buy only enough
      fuel to reach that cheaper station.
    - Otherwise fill the tank.
    - If the destination is reachable, buy only enough to finish.
    """

    if route_distance_miles <= 0:
        return {
            "fuel_stops": [],
            "total_fuel_cost": 0.0,
            "total_gallons_purchased": 0.0,
        }

    stations = stations.copy()

    # --------------------------------------------------
    # Only stations between start and destination
    # --------------------------------------------------

    stations = stations[
        (stations["route_position_miles"] > 0)
        & (
            stations["route_position_miles"]
            < route_distance_miles
        )
    ].copy()

    stations = stations.sort_values(
        "route_position_miles"
    ).reset_index(drop=True)

    # Remove duplicate station records.
    stations = stations.drop_duplicates(
        subset=["station_id"]
    ).reset_index(drop=True)

    if stations.empty:
        raise ValueError(
            "No fuel stations were found along the route."
        )

    # --------------------------------------------------
    # Vehicle state
    # --------------------------------------------------

    current_position = 0.0

    current_fuel = min(
        float(starting_fuel_gallons),
        MAX_FUEL_GALLONS,
    )

    total_cost = 0.0
    total_gallons = 0.0

    fuel_stops = []

    # --------------------------------------------------
    # Process stations in route order
    # --------------------------------------------------

    for index in range(len(stations)):

        station = stations.iloc[index]

        station_position = float(
            station["route_position_miles"]
        )

        distance_to_station = (
            station_position
            - current_position
        )

        # --------------------------------------------------
        # Can we reach this station?
        # --------------------------------------------------

        fuel_needed_to_station = (
            distance_to_station / MPG
        )

        if fuel_needed_to_station > current_fuel + 1e-9:
            raise ValueError(
                "Vehicle cannot reach the next "
                "fuel station within the 500-mile range."
            )

        # --------------------------------------------------
        # TRAVEL FIRST
        # --------------------------------------------------

        current_fuel -= fuel_needed_to_station

        current_position = station_position

        # --------------------------------------------------
        # Now we have ARRIVED at the station.
        # --------------------------------------------------

        current_price = float(
            station["price"]
        )

        # Distance remaining to destination.
        distance_to_destination = (
            route_distance_miles
            - current_position
        )

        # Fuel needed to reach destination.
        fuel_needed_to_destination = (
            distance_to_destination / MPG
        )

        # --------------------------------------------------
        # If destination is reachable, buy only enough
        # to finish.
        # --------------------------------------------------

        if fuel_needed_to_destination <= current_fuel:

            gallons_to_buy = 0.0

        elif (
            fuel_needed_to_destination
            <= MAX_FUEL_GALLONS
        ):

            gallons_to_buy = (
                fuel_needed_to_destination
                - current_fuel
            )

        else:

            # Destination is not reachable with one tank.
            # We need to look for a cheaper station.
            gallons_to_buy = None

        # --------------------------------------------------
        # If destination cannot be reached yet,
        # search for a cheaper reachable station.
        # --------------------------------------------------

        if gallons_to_buy is None:

            cheaper_station = None

            for future_index in range(
                index + 1,
                len(stations)
            ):

                future_station = (
                    stations.iloc[future_index]
                )

                future_position = float(
                    future_station[
                        "route_position_miles"
                    ]
                )

                distance_to_future = (
                    future_position
                    - current_position
                )

                fuel_required = (
                    distance_to_future / MPG
                )

                # Cannot reach this station.
                if fuel_required > current_fuel * MPG:
                    break

                # Actually, we can only travel using
                # the fuel currently in the tank.
                if fuel_required > (
                    current_fuel * MPG
                ):
                    continue

                future_price = float(
                    future_station["price"]
                )

                if future_price < current_price:
                    cheaper_station = (
                        future_station
                    )
                    break

            # --------------------------------------------------
            # If a cheaper station is reachable:
            # buy only enough to reach it.
            # --------------------------------------------------

            if cheaper_station is not None:

                future_position = float(
                    cheaper_station[
                        "route_position_miles"
                    ]
                )

                distance_to_future = (
                    future_position
                    - current_position
                )

                fuel_needed = (
                    distance_to_future / MPG
                )

                gallons_to_buy = max(
                    0.0,
                    fuel_needed - current_fuel
                )

            else:

                # No cheaper station is reachable.
                # Fill the tank.
                gallons_to_buy = (
                    MAX_FUEL_GALLONS
                    - current_fuel
                )

        # --------------------------------------------------
        # Safety limit
        # --------------------------------------------------

        gallons_to_buy = max(
            0.0,
            min(
                gallons_to_buy,
                MAX_FUEL_GALLONS - current_fuel
            )
        )

        # --------------------------------------------------
        # Record purchase
        # --------------------------------------------------

        if gallons_to_buy > 0.0001:

            fuel_cost = (
                gallons_to_buy
                * current_price
            )

            fuel_stops.append({
    "station_id": int(
        station["station_id"]
    ),

    "station_name": (
        station["station_name"]
    ),

    "city": station["city"],

    "state": station["state"],

    "latitude": float(
        station["latitude"]
    ),

    "longitude": float(
        station["longitude"]
    ),

                "price_per_gallon": round(
                    current_price,
                    3
                ),

                "route_position_miles": round(
                    current_position,
                    2
                ),

                "distance_to_route_miles": round(
                    float(
                        station[
                            "distance_to_route_miles"
                        ]
                    ),
                    2
                ),

                "gallons_purchased": round(
                    gallons_to_buy,
                    3
                ),

                "fuel_cost": round(
                    fuel_cost,
                    2
                ),
            })

            current_fuel += gallons_to_buy

            total_gallons += gallons_to_buy

            total_cost += fuel_cost

        # --------------------------------------------------
        # Can we finish now?
        # --------------------------------------------------

        if (
            route_distance_miles
            - current_position
        ) <= current_fuel * MPG:

            break

    # --------------------------------------------------
    # Final validation
    # --------------------------------------------------

    remaining_distance = (
        route_distance_miles
        - current_position
    )

    if remaining_distance > current_fuel * MPG + 1e-6:
        raise ValueError(
            "The selected fuel stations cannot "
            "complete the route within the 500-mile range."
        )

    return {
        "fuel_stops": fuel_stops,

        "total_fuel_cost": round(
            total_cost,
            2
        ),

        "total_gallons_purchased": round(
            total_gallons,
            3
        ),
    }