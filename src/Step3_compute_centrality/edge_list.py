import sqlite3 as sql
from sqlite3 import Connection

import pandas as pd
from pandas import DataFrame


def main() -> None:
    """
    Creates and saves the edges of the centrality to the dataframe.
    """

    # Creates connections to the database.
    conn: Connection = sql.connect("/workspaces/public-transport-analytics/gtfs.db")

    # creating the variable, which stores edges of the network.
    edge_df: DataFrame = pd.read_sql_query(
        """SELECT DISTINCT
        st1.stop_id AS source,
        st2.stop_id AS dest
        FROM
        stops_time AS st1
        JOIN
        stops_time AS st2
        ON st1.trip_id = st2.trip_id
        AND st2.stop_sequence = st1.stop_sequence + 1;""",
        conn,
    )

    # preview for the verification.
    print(edge_df.head())

    # close connection.
    conn.close()


if __name__ == "__main__":
    main()
