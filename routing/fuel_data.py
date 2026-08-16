from pathlib import Path
import pandas as pd


# Find the project folder
BASE_DIR = Path(__file__).resolve().parent


# Location of our CSV file
CSV_FILE = BASE_DIR / "data" / "fuel-prices.csv"


def load_fuel_stations():
    """
    Load fuel station data from the CSV file.
    """

    df = pd.read_csv(CSV_FILE)

    # Keep only the columns we need
    df = df[
        [
            "OPIS Truckstop ID",
            "Truckstop Name",
            "Address",
            "City",
            "State",
            "Retail Price",
        ]
    ]

    # Remove rows where important information is missing
    df = df.dropna(
        subset=[
            "Truckstop Name",
            "City",
            "State",
            "Retail Price",
        ]
    )

    return df