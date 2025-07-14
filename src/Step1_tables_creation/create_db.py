from sqlite3 import Connection, Cursor
import sqlite3 as sql

def main():

    # Open gtfs.db file and prepare connection.
    connection : Connection = sql.connect("/workspaces/public-transport-analytics/gtfs.db")

    # create a cursor.
    cursor : Cursor = connection.cursor()
    
    # create a table in the dtfs.db via cursor.
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS stops ( 
    stop_id INTEGER PRIMARY KEY,
    stop_name TEXT, 
    stop_lat REAL, 
    stop_lon REAL);"""
    )
    connection.commit()
    
    # send the query to sqlite_master to list tables.
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type= 'table';"
    )
    # Retrive all matching rows
    tables = cursor.fetchall()
    print("Tables in the database: ", tables)

    # Need to get the column info and check it.
    # sending query with cursor.
    cursor.execute(
        "PRAGMA table_info('stops');"
    )
    # Retrive all matching tables.
    schema = cursor.fetchall()
    print("table's schema: ", schema)

    # Close connection.
    connection.close()

    

main()