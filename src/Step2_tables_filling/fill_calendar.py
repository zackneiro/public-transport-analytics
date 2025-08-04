import sqlite3 as sql
from sqlite3 import Connection, Cursor
from typing import Final, List, Tuple

import pandas as pd
from pandas import DataFrame

DB_PATH: Final[str] = "/workspaces/public-transport-analytics/gtfs.db"
CALENDAR_CSV_PATH: Final[
    str
] = "/workspaces/public-transport-analytics/required_data/data/gtfs/calendar.txt"

INSERT_INTO_CALENDAR_SQL: Final[
    str
] = """
INSERT OR IGNORE INTO calendar (
    service_id,
    monday, tuesday, wednesday,
    thursday, friday, saturday,
    sunday, start_date, end_date
) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""


def main() -> None:
    """Populate the GTFS `calendar` table from calendar.txt."""

    # Connect to the SQLite database and create a cursor
    conn: Connection = sql.connect(DB_PATH)
    cur: Cursor = conn.cursor()

    # Load calendar.txt into a DataFrame with selected columns
    table_df: DataFrame = pd.read_csv(
        CALENDAR_CSV_PATH,
        usecols=[
            "service_id",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "start_date",
            "end_date",
        ],
    )

    # Create rows
    rows: List[Tuple[str, int, int, int, int, int, int, int, str]] = list(
        table_df.itertuples(index=False, name=None)
    )
    # Insert rows into the calendar table
    cur.executemany(INSERT_INTO_CALENDAR_SQL, rows)
    conn.commit()

    # Verify the number of inserted rows
    cur.execute("SELECT COUNT(*) FROM calendar;")
    print("Loaded files:", cur.fetchone()[0])

    # Close connection
    conn.close()


if __name__ == "__main__":
    main()
