import sqlite3 as sql3
from sqlite3 import Connection, Cursor
from typing import Final

DB_PATH: Final[str] = "gtfs.db"
CREATE_STOPS_TABLE_SQL: Final[
    str
] = """
CREATE TABLE IF NOT EXISTS stops (
    stop_id INTEGER PRIMARY KEY,
    stop_name TEXT,
    stop_lat REAL,
    stop_lon REAL
);
"""


def main() -> None:
    """Create the 'stops' table in the GTFS SQLite database."""

    # Create connection to the GTFS table and a cursor
    conn: Connection = sql3.connect(DB_PATH)
    cur: Cursor = conn.cursor()

    # Create the table in the GTFS database
    cur.execute(CREATE_STOPS_TABLE_SQL)
    conn.commit()

    # Verfiy that the table exists
    conn.execute("SELECT name FROM sqlite_master WHERE type= 'table';")
    tables = cur.fetchall()
    print("Tables in the database:", tables)

    # Verify the table schema
    cur.execute("PRAGMA table_info('stops');")
    schema = cur.fetchall()
    print("table's schema:", schema)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
