from typing import List, Tuple
from pandas import DataFrame
from sqlite3 import Connection, Cursor
import pandas as pd
import sqlite3 as sql

def main() -> None:
    
    # Create a variable and save data of the columns I need.
    table_db: DataFrame = pd.read_csv(
        "/workspaces/public-transport-analytics/required_data/data/gtfs/stops.txt",
        usecols= ["stop_id", "stop_name", "stop_lat", "stop_lon"]
    )

    connection: Connection = sql.connect("/workspaces/public-transport-analytics/gtfs.db")
    cursor : Cursor = connection.cursor()

    # Now I insert data from variable to the data base.
    # I create a variable that will hold a query.
    insert_sql = """
    INSERT OR IGNORE INTO stops (
    stop_id,
    stop_name,
    stop_lat,
    stop_lon
    ) VALUES (?, ?, ?, ?);
    """
    # Preparing the data as the plain tuples,
    # which will give me memory efficiency and cleanliness
    # So I dropp the namedtuples and set index to False,
    # So I will work exactly with my four colunmns in the query.

    rows :  List[Tuple[str, str, float, float]] = list(
        table_db.itertuples(index=False, name=None)
    ) 

    # Execute the bulk insert.
    cursor.executemany(insert_sql, rows)
    
    # commit transaction.
    connection.commit()

    # close connection.
    connection.close()



if __name__ == "__main__":
    main()