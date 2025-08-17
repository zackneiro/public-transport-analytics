import sqlite3 as sql3
from sqlite3 import Connection, Cursor
from typing import Final

DB_PATH: Final[str] = "gtfs.db"
CREATE_TRIPS_TABLE_SQL: Final[
    str
] = """
CREATE TABLE IF NOT EXISTS trips (
    trip_id TEXT PRIMARY KEY,
    route_id TEXT,
    service_id TEXT
);
"""


def main() -> None:
    """Create the 'trips' table in the GTFS SQLite database."""

    # Connect to the GTFS database and create a cursor
    conn: Connection = sql3.connect(DB_PATH)
    cur: Cursor = conn.cursor()

    # Execute table creation
    cur.execute(CREATE_TRIPS_TABLE_SQL)
    conn.commit()

    # Verify that the table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type= 'table';")
    table = cur.fetchall()
    print("This is a table:", table)

    # Verify the table's schema
    cur.execute("PRAGMA table_info('trips')")
    table_info = cur.fetchall()
    print("This is a table's schema:", table_info)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
