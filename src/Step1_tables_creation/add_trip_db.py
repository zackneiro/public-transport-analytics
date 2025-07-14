from pandas import DataFrame
from sqlite3 import Connection, Cursor
import pandas as pd
import sqlite3 as sql

def main() -> None:
    
    # At first, I read a file and preview rows to check their types.
    """trips_db : DataFrame = pd.read_csv(
        "/workspaces/public-transport-analytics/required_data/data/gtfs/trips.txt",
        usecols=["route_id", "service_id", "trip_id"]
        )"""
    
    """trips_db_2 = pd.read_csv(
        "/workspaces/public-transport-analytics/required_data/data/gtfs/trips2.txt",
        usecols=["route_id", "service_id", "trip_id"]
    )"""
    
    # check the types.
    """print(f"{trips_db.dtypes} \n{trips_db_2.dtypes}")"""

    
    # After I got the types of objects I create schema of the database.
    """
    route_id TEXT
    service_id TEXT
    trip_id TEXT
    """

    # Now I create connection to the database.
    connection: Connection = sql.connect("/workspaces/public-transport-analytics/gtfs.db")

    # Next I create a cursor to interact with db.
    cursor: Cursor= connection.cursor()

    # Now I will create a table with the upper schema.
    cursor.execute(""" CREATE TABLE IF NOT EXISTS trips (
                   trip_id TEXT PRIMARY KEY,
                   route_id TEXT,
                   service_id TEXT);"""
    )
    connection.commit()

    # Next step is to check the existence of the table.
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type= 'table';"
    )
    table = cursor.fetchall()
    print("This is a table: ", table)

    # Check the "trip" table's schema.
    cursor.execute(
        "PRAGMA table_info('trips')"
    )

    table_info = cursor.fetchall()
    print("This is a table's schema: ", table_info)

    # Close connection.
    connection.close()

if __name__ == "__main__":
    main()
