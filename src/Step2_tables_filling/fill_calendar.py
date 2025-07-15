import sqlite3 as sql
from sqlite3 import Connection, Cursor
from typing import List, Tuple

import pandas as pd
from pandas import DataFrame


def main() -> None:
    """
    Function fills the "calendar" table in the SQL database.
    """
    # create connection.
    db_connection: Connection = sql.connect(
        "/workspaces/public-transport-analytics/gtfs.db"
    )
    # create cursor.
    db_cursor: Cursor = db_connection.cursor()
    # create dataframe and save the data to it.
    table_df: DataFrame = pd.read_csv(
        "/workspaces/public-transport-analytics/required_data/data/gtfs/calendar.txt",
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
    # create a query.
    insert_sql: str = """INSERT OR IGNORE INTO calendar(
                    service_id,
                    monday, tuesday, wednesday,
                    thursday, friday, saturday,
                    sunday, start_date, end_date)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    # create rows.
    rows: List[Tuple[str, int, int, int, int, int, int, int, str]] = list(
        table_df.itertuples(index=False, name=None)
    )
    # send query with rows (executemany).
    db_cursor.executemany(insert_sql, rows)
    # commit changes
    db_connection.commit()
    # check table for loadaed files.
    db_cursor.execute("SELECT COUNT(*) FROM calendar;")
    print("Loaded files: ", db_cursor.fetchone()[0])

    db_connection.close()


if __name__ == "__main__":
    main()
