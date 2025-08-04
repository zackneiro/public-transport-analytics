import sqlite3 as sql
from sqlite3 import Connection, Cursor
from typing import Final, List, Tuple

import pandas as pd
from pandas import DataFrame

TRIPS1_CSV_PATH: Final[str] = (
    "/workspaces/public-transport-analytics/"
    "required_data/data/gtfs/trips.txt"
)
TRIPS2_CSV_PATH: Final[str] = (
    "/workspaces/public-transport-analytics"
    "/required_data/data/gtfs/trips2.txt"
)
INSERT_TRIPS_SQL: Final[str] = """
INSERT OR IGNORE INTO trips (
    trip_id, 
    route_id, 
    service_id
) VALUES (?, ?, ?);
"""
DB_PATH: Final[str] = "/workspaces/public-transport-analytics/gtfs.db"


def main() -> None:
    """Populates the 'trips' table from GTFS trips1- trips2.txt."""
    
    # Read CSV files and save their data to the dataframes
    trip1_df: DataFrame = pd.read_csv(
        TRIPS1_CSV_PATH, usecols=["trip_id", "route_id", "service_id"],
    )
    trip2_df: DataFrame = pd.read_csv(
        TRIPS2_CSV_PATH, usecols=["trip_id", "route_id", "service_id"],
    )

    # Concatenate them
    df_trips = pd.concat([trip1_df, trip2_df], ignore_index=True)

    # Drop duplicates by trip_id if needed:
    df_trips = df_trips.drop_duplicates(subset=["trip_id"])

    # Connect to the GTFS database and create cursor
    conn: Connection = sql.connect(DB_PATH)
    cur: Cursor = conn.cursor()

    # Prepare the data for insertion
    rows: List[Tuple[str, str, str]] = list(df_trips.itertuples(index=False, name=None))

    # Execute the insertion to the database's table
    cur.executemany(INSERT_TRIPS_SQL, rows)

    # Commit changes
    conn.commit()

    # Verify the processed work
    cur.execute("SELECT COUNT(*) FROM trips;")
    print("Loaded trips:", cur.fetchone()[0])

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
