from pandas import DataFrame
from sqlite3 import Connection, Cursor
import pandas as pd
import sqlite3 as sql

def main() -> None:

    # read csv file to understand the base of schema.
    """
    table: DataFrame = pd.read_csv("/workspaces/public-transport-analytics/required_data/data/gtfs/stop_times.txt",
                        nrows=0)
    """
    # check the types of the rows and write a schema.
    # print(table.dtypes)
    """
    trip_id TEXT,
    stop_id TEXT,
    arrival_time TEXT,
    departure time TEXT,
    stop_sequence INTEGER,
    PRIMARY KEY (trip_id, stop_sequence)
    """

    # create connection with the data base.
    connection: Connection = sql.connect('/workspaces/public-transport-analytics/gtfs.db')

    # create cursor.
    cursor: Cursor = connection.cursor()

    # create the table.
    cursor.execute("""CREATE TABLE IF NOT EXISTS stops_time(
                   trip_id TEXT,
                   stop_id TEXT,
                   arrival_time TEXT,
                   departure_time TEXT,
                   stop_sequence INTEGER,
                   PRIMARY KEY(trip_id, stop_sequence));"""
    )

    # commit
    connection.commit()

    # check for existence
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    print(cursor.fetchall())

    # check the schema
    cursor.execute(
        "PRAGMA table_info(stops_time);"
    )
    print(cursor.fetchall())

    # close connection.
    connection.close()

if __name__ == "__main__":
    main()