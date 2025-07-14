import sqlite3 as sql, pandas as pd, networkx as nx
import matplotlib.pyplot as plt
from sqlite3 import Connection, Cursor
from pandas import DataFrame

def main() -> None:
    """
    This functions creates edge graph.
    The condtions of what are:
        1. Undirected graph.
            - Treats every connection as two - way.
            - Simple and fine for centrality.
        2. Unweighted.
            - Every edge counts the same (weight = 1)
            - Closeness measures "fewest hops".
    """

    # Create connection:
    conn: Connection = sql.connect(
        "/workspaces/public-transport-analytics/gtfs.db"
        )
    
    # Create cursor.
    cursor: Cursor = conn.cursor()

    # Create a DataFrame variable, which stores edges data.
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
        conn
    )

    # Check the DataFrame before moving to the next steps.
    # Print the first 5 row.
    print(edge_df.head(5))
    # Tells how many edges I loaded by how many rows (should be 2)
    print(edge_df.shape)

    # Create variable that stores all nodes and edges.
    G: nx.Graph = nx.Graph()

    # Adding edges to the data frame I've created eariler.
    for src, dst in edge_df.itertuples(index=False, name=None):
        G.add_edge(src,dst)
    
    # Confirm the graph size:
    print("Graph has", G.number_of_nodes(), "nodes and", G.number_of_edges(), "egdes")
    
    # Start to compute closeness centrality.
    # Create a variable to compute closeness centrality and store it.
    # I call nx.closeness_centrality, which returns dict mapping each
    # node to its centrality score.
    centrality: nx.closeness_centrality = nx.closeness_centrality(G)

    # Converting computed centrality to the pandas DataFrame.
    # .from_dict treats dict keys as row tables.
    # columns name the single data column. 
    # .reset_index() turns the row labels into a regular column.
    # .rename() renames that column to 'stop_id'.
    centrality_df: DataFrame = pd.DataFrame.from_dict(
        centrality,
        orient= 'index',
        columns=['centrality']
    ).reset_index().rename(columns={'index':'stop_id'})

    # Now I attach human-readable stop names.
    # Converting 'stop_id' to the int type, since I can't merge
    # 'object' type and 'int64'.

    stops_df: DataFrame = pd.read_sql_query(
        "SELECT stop_id, stop_name FROM stops;",
        conn
    )
    stops_df['stop_id'] = stops_df['stop_id'].astype(int)
    centrality_df['stop_id'] = centrality_df['stop_id'].astype(int)

    merged = centrality_df.merge(stops_df, on='stop_id')

    # ordering the rows by the highest centrality first and limitng.
    top10 = merged.sort_values('centrality', ascending=False).head(10)

    # Display result.
    print(top10[['stop_id', 'stop_name', 'centrality']])


main()