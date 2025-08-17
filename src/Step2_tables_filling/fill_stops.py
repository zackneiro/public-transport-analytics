import sqlite3 as sql3
from sqlite3 import Connection, Cursor
from typing import Final, List, Tuple

import pandas as pd
from pandas import DataFrame

DB_PATH: Final[str] = "gtfs.db"
STOPS_CSV_PATH: Final[str] = ("required_data/data/gtfs/stops.txt")
SQL_INSERT_QUERY: Final[str] = """
INSERT OR IGNORE INTO stops (
    stop_id,
    stop_name,
    stop_lat,
    stop_lon
) VALUES (?, ?, ?, ?);
"""


def main() -> None:
    """Fills the 'stops' table with the data from CSV table of stops.txt."""

    table_df: DataFrame = pd.read_csv(
        STOPS_CSV_PATH,
        usecols=["stop_id", "stop_name", "stop_lat", "stop_lon"],
    )

    # Connect to the GTFS database and create a cursor
    conn: Connection = sql3.connect(DB_PATH)
    cur: Cursor = conn.cursor()

    # Create a list of rows
    rows: List[Tuple[str, str, float, float]] = list(
        table_df.itertuples(index=False, name=None)
    )

    # Execute the bulk insert
    cur.executemany(SQL_INSERT_QUERY, rows)
    conn.commit()

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
