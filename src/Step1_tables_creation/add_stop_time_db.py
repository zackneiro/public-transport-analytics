import sqlite3 as sql
from sqlite3 import Connection, Cursor

DB_PATH = "/workspaces/public-transport-analytics/gtfs.db"
TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS stops_time(
    trip_id TEXT,
    stop_id TEXT,
    arrival_time TEXT,
    departure_time TEXT,
    stop_sequence INTEGER,
    PRIMARY KEY(trip_id, stop_sequence));
"""


def main() -> None:
    """Create the stops_time table in the GTFS SQLite3 database."""

    # Connect to the GTFS database
    connection: Connection = sql.connect(DB_PATH)
    cursor: Cursor = connection.cursor()

    # Excucte table creation
    cursor.execute(TABLE_SCHEMA)
    connection.commit()

    # Verfiy that the tables exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

    # Check the correctness of schema
    cursor.execute("PRAGMA table_info(stops_time);")
    print(cursor.fetchall())

    # Close the connection.
    connection.close()


if __name__ == "__main__":
    main()
