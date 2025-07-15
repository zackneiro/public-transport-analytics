import sqlite3 as sql
from sqlite3 import Connection, Cursor

import pandas as pd
from pandas import DataFrame


def main() -> None:
    # read the file and check names of the rows I need.
    """table : DataFrame = pd.read_csv(
    "/workspaces/public-transport-analytics/required_data/data/gtfs/calendar.txt",
    nrows= 0
    )"""
    # check the types of the choosen rows.
    # print(table.dtypes)

    # create a schema.
    """
    service_id TEXT PRIMARY KEY,
    monday TEXT,
    tuesday TEXT,
    wednesday TEXT,
    thursday TEXT,
    friday TEXT,
    saturday TEXT,
    sunday TEXT,
    start_date TEXT,
    end_date TEXT
    """

    # create a connection to the db.
    connection: Connection = sql.connect(
        "/workspaces/public-transport-analytics/gtfs.db"
    )

    # create the cursos to interact with db.
    cursor: Cursor = connection.cursor()

    # create the table "calendar" with schema.
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS calendar(
                   service_id TEXT PRIMARY KEY,
                   monday TEXT,
                   tuesday TEXT,
                   wednesday TEXT,
                   thursday TEXT,
                   friday TEXT,
                   saturday TEXT,
                   sunday TEXT,
                   start_date TEXT,
                   end_date TEXT);"""
    )

    # commit changes.
    connection.commit()

    # check the existence of the table with query.
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

    # check the table's schema with PRAGMA.
    cursor.execute("PRAGMA table_info('calendar')")
    print(cursor.fetchall())

    # close connection.
    connection.close()


if __name__ == "__main__":
    main()
