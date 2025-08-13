import sqlite3 as sql3
from sqlite3 import Connection, Cursor
from typing import Final, List, Tuple

import pandas as pd
from pandas import DataFrame

STOP_TIME_CSV_PATH: Final[str] = (
    "/workspaces/public-transport-analytics/"
    "required_data/data/gtfs/stop_times.txt"
)
DB_PATH: Final[str] = "/workspaces/public-transport-analytics/gtfs.db"
INSERT_INTO_STOPS_TIME_SQL: Final[str] = """
INSERT OR IGNORE INTO stops_time (
    trip_id, 
    stop_id, 
    arrival_time, 
    departure_time, 
    stop_sequence
) VALUES(?, ?, ?, ?, ?);
"""


def main() -> None:
    """Populate the stop_times table from GTFS stop_times_file.txt"""

    # Read CSV file and store data in it
    stop_times_df: DataFrame = pd.read_csv(
        STOP_TIME_CSV_PATH,
        usecols=[
            "trip_id",
            "stop_id",
            "arrival_time",
            "departure_time",
            "stop_sequence",
        ],
    )

    # Verify the exact order of the dataframe
    stop_times_df = stop_times_df[
        [
            "trip_id",
            "stop_id",
            "arrival_time",
            "departure_time",
            "stop_sequence",
        ]
    ]

    # Connect to the GTFS database and create a cursor
    conn: Connection = sql3.connect(DB_PATH)
    cur: Cursor = conn.cursor()

    # Create a list with the rows
    rows: List[Tuple[str, str, str, str, int]] = list(
        stop_times_df.itertuples(index=False, name=None)
    )

    # Insert data from GTFS file to the table
    cur.executemany(INSERT_INTO_STOPS_TIME_SQL, rows)
    conn.commit()
    
    # Verify processed work
    cur.execute("SELECT COUNT(*) FROM stops_time;")
    loaded: int = cur.fetchone()[0]
    print("Loaded files:", loaded)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
