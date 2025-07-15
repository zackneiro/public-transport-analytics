import sqlite3 as sql
from sqlite3 import Connection, Cursor
from typing import List, Tuple

import pandas as pd
from pandas import DataFrame


def main() -> None:
    """
    This code fills the table "stop_times" in the database.
    """

    # create DataFrame to save the data from the file.
    stop_times_df: DataFrame = pd.read_csv(
        "/workspaces/public-transport-analytics/required_data/data/gtfs/stop_times.txt",
        usecols=[
            "trip_id",
            "stop_id",
            "arrival_time",
            "departure_time",
            "stop_sequence",
        ],
    )

    stop_times_df = stop_times_df[
        ["trip_id", "stop_id", "arrival_time", "departure_time", "stop_sequence"]
    ]

    # create connection to the database.
    connection_db: Connection = sql.connect(
        "/workspaces/public-transport-analytics/gtfs.db"
    )

    # create cursor.
    curosr_db: Cursor = connection_db.cursor()

    # create insert_sql; query-pattern which I use for insertion.
    insert_sql = """INSERT OR IGNORE INTO stops_time(
    trip_id, stop_id, arrival_time, departure_time, stop_sequence)
    VALUES(?, ?, ?, ?, ?);"""

    # create variable and save files rows in it.
    rows: List[Tuple[str, str, str, str, int]] = list(
        stop_times_df.itertuples(index=False, name=None)
    )

    # insert rows to the table of the database.
    connection_db.executemany(insert_sql, rows)
    # commit changes
    connection_db.commit()
    # check
    curosr_db.execute("SELECT COUNT(*) FROM stops_time;")
    print("Loaded files: ", curosr_db.fetchone()[0])

    connection_db.close()


if __name__ == "__main__":
    main()
