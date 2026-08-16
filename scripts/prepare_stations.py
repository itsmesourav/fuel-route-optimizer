from pathlib import Path
import io
import requests
import pandas as pd


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FUEL_FILE = PROJECT_ROOT / "routing" / "data" / "fuel-prices.csv"
OUTPUT_FILE = PROJECT_ROOT / "routing" / "data" / "fuel-stations.csv"


# Public US city coordinate dataset
CITY_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "kelvins/US-Cities-Database/main/csv/us_cities.csv"
)


# ---------------------------------------------------------
# US states
# ---------------------------------------------------------

US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO",
    "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA",
    "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN",
    "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC"
}


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def normalize_city(city):
    """
    Make city names easier to match.

    Example:
        "New York " -> "new york"
    """

    return (
        str(city)
        .strip()
        .lower()
        .replace(" city", "")
        .replace(" town", "")
        .replace(" village", "")
        .replace(" borough", "")
        .replace(" CDP", "")
    )


# ---------------------------------------------------------
# Download city coordinates
# ---------------------------------------------------------

def download_city_data():
    print("Downloading US city coordinate data...")

    response = requests.get(
        CITY_DATA_URL,
        timeout=60
    )

    response.raise_for_status()

    print("City coordinate data downloaded.")

    return pd.read_csv(io.BytesIO(response.content))


# ---------------------------------------------------------
# Main preprocessing
# ---------------------------------------------------------

def main():

    print("Loading fuel price data...")

    fuel_df = pd.read_csv(FUEL_FILE)

    print(f"Fuel records loaded: {len(fuel_df)}")

    # Keep only US fuel stations
    fuel_df = fuel_df[
        fuel_df["State"].isin(US_STATES)
    ].copy()

    print(
        f"US fuel records after filtering: {len(fuel_df)}"
    )

    # Normalize city names
    fuel_df["city_key"] = (
        fuel_df["City"]
        .apply(normalize_city)
    )

    fuel_df["state_key"] = (
        fuel_df["State"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Download city coordinates
    city_df = download_city_data()

    print(
        f"US cities loaded: {len(city_df)}"
    )

    print(
        "City dataset columns:",
        list(city_df.columns)
    )

    # Normalize city dataset
    city_df["city_key"] = (
        city_df["CITY"]
        .apply(normalize_city)
    )

    city_df["state_key"] = (
        city_df["STATE_CODE"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Keep only fields we need
    city_coordinates = city_df[
        [
            "city_key",
            "state_key",
            "LATITUDE",
            "LONGITUDE"
        ]
    ].copy()

    # Remove duplicate city/state combinations
    city_coordinates = (
        city_coordinates
        .drop_duplicates(
            subset=["city_key", "state_key"]
        )
    )

    # Merge fuel stations with coordinates
    merged = fuel_df.merge(
        city_coordinates,
        on=["city_key", "state_key"],
        how="left"
    )

    # Count unmatched stations
    unmatched = merged[
        merged["LATITUDE"].isna()
        | merged["LONGITUDE"].isna()
    ]

    print(
        f"Stations without coordinates: "
        f"{len(unmatched)}"
    )

    # Keep only stations with coordinates
    merged = merged.dropna(
        subset=[
            "LATITUDE",
            "LONGITUDE"
        ]
    )

    # Create clean final dataset
    result = merged[
        [
            "OPIS Truckstop ID",
            "Truckstop Name",
            "Address",
            "City",
            "State",
            "LATITUDE",
            "LONGITUDE",
            "Retail Price"
        ]
    ].copy()

    # Rename columns
    result = result.rename(
        columns={
            "OPIS Truckstop ID": "station_id",
            "Truckstop Name": "station_name",
            "Address": "address",
            "City": "city",
            "State": "state",
            "LATITUDE": "latitude",
            "LONGITUDE": "longitude",
            "Retail Price": "price"
        }
    )

    # Save final station dataset
    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("======================================")
    print("Station preprocessing completed!")
    print("======================================")
    print(
        f"Stations with coordinates: {len(result)}"
    )
    print(
        f"Output file: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()