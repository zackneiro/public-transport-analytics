import sqlite3 as sql3
from sqlite3 import Connection, Cursor
from typing import Final

DB_PATH: Final[str] = "/workspaces/public-transport-analytics/gtfs.db"
CREATE_CALENDAR_TABLE_SQL: Final[
    str
] = """
CREATE TABLE IF NOT EXISTS calendar (
    service_id TEXT PRIMARY KEY,
    monday TEXT,
    uesday TEXT,
    wednesday TEXT,
    thursday TEXT,
    friday TEXT,
    saturday TEXT,
    sunday TEXT,
    start_date TEXT,
    end_date TEXT
);
"""


def main() -> None:
    """Create the 'calendar' table in the GTFS SQLie database."""

    # Connect to the GTFS database and create a cursor
    conn: Connection = sql3.connect(DB_PATH)
    cur: Cursor = conn.cursor()

    # Create the table in GTFS database
    cur.execute(CREATE_CALENDAR_TABLE_SQL)
    conn.commit()

    # Verify the table's existence
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())

    # Verfiy the table's schema
    cur.execute("PRAGMA table_info('calendar')")
    print(cur.fetchall())

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
