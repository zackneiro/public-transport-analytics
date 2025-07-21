import sqlite3 as sql
from sqlite3 import Connection, Cursor

DB_PATH = "/workspaces/public-transport-analytics/gtfs.db"
TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS calendar(
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
    """
    This code creates the 'calendar table' in the GTFS database
    if it doesn't exist.

    This function connects to the SQLite database at gtfs.db, then
    executes a CREATE TABLE IF NOT EXISTS for the 'calendar', table
    with coloumns mathcing the GTFS schema.
    """

    # Table's schema:
    # service_id TEXT PRIMARY KEY,
    # monday     TEXT,
    # tuesday    TEXT,
    # wednesday  TEXT,
    # thursday   TEXT,
    # friday     TEXT,
    # saturday   TEXT,
    # sunday     TEXT,
    # start_date TEXT,
    # end_date   TEXT

    # Connect to the GTFS SQLite database
    connection_db: Connection = sql.connect(DB_PATH)
    cursor: Cursor = connection_db.cursor()

    # Create 'calendar' table if missing
    cursor.execute(TABLE_SCHEMA)

    connection_db.commit()

    # Verify the table's exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

    # Inspect the 'calendar' schema
    cursor.execute("PRAGMA table_info('calendar')")
    print(cursor.fetchall())

    connection_db.close()


if __name__ == "__main__":
    main()
