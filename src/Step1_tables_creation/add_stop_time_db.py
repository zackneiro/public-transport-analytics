import sqlite3 as sql3
from sqlite3 import Connection, Cursor
from typing import Final

DB_PATH: Final[str] = "/workspaces/public-transport-analytics/gtfs.db"
CREATE_STOPS_TIME_TABLE_SQL: Final[
    str
] = """
CREATE TABLE IF NOT EXISTS stops_time (
    trip_id TEXT,
    stop_id TEXT,
    arrival_time TEXT,
    departure_time TEXT,
    stop_sequence INTEGER,
    PRIMARY KEY(trip_id, stop_sequence
));
"""


def main() -> None:
    """Create the 'stops_time' table in the GTFS SQLite database."""

    # Connect to the GTFS database and create a cursor
    conn: Connection = sql3.connect(DB_PATH)
    cur: Cursor = conn.cursor()

    # Excucte the table creation
    cur.execute(CREATE_STOPS_TIME_TABLE_SQL)
    conn.commit()

    # Verfiy that the tables exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())

    # Check the correctness of schema
    cur.execute("PRAGMA table_info(stops_time);")
    print(cur.fetchall())

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
