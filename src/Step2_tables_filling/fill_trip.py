import sqlite3 as sql
from sqlite3 import Connection, Cursor
from typing import List, Tuple

import pandas as pd
from pandas import DataFrame


def main() -> None:
    """
    This code fills the table "trips" in the database
    with the data from the file.
    """

    # At first, I prepare DataFrame, connection, cursor, sql query.
    # DataFrame.
    trip1_df: DataFrame = pd.read_csv(
        """/workspaces/public-transport-analytics/
        required_data/data/gtfs/trips.txt""",
        usecols=["trip_id", "route_id", "service_id"],
    )
    trip2_df: DataFrame = pd.read_csv(
        """/workspaces/public-transport-analytics/
        required_data/data/gtfs/trips2.txt""",
        usecols=["trip_id", "route_id", "service_id"],
    )

    # concatenate them.
    df_trips = pd.concat([trip1_df, trip2_df], ignore_index=True)

    # Drop duplicates by trip_id if needed:
    df_trips = df_trips.drop_duplicates(subset=["trip_id"])

    # Connection.
    connection: Connection = sql.connect(
        "/workspaces/public-transport-analytics/gtfs.db"
    )

    # Cursor.
    cursor: Cursor = connection.cursor()

    # SQL query.
    query_insert = """
    INSERT OR IGNORE INTO trips (trip_id, route_id, service_id)
    VALUES(?, ?, ?);
    """
    # Prepare the data for insertion.
    rows: List[Tuple[str, str, str]] = list(df_trips.itertuples(index=False, name=None))

    # Now execute the insertion to the database's table.
    cursor.executemany(query_insert, rows)

    # Commit changes.
    connection.commit()

    # Check.
    cursor.execute("SELECT COUNT(*) FROM trips;")
    print("Loaded trips:", cursor.fetchone()[0])

    # Close connection.
    connection.close()


if __name__ == "__main__":
    main()
