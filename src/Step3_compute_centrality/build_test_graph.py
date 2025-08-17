import sqlite3 as sql3
from typing import Final

import networkx as nx
import pandas as pd
from pandas import DataFrame


DB_PATH: Final[str] = "gtfs.db"
EDGE_LIST_SQL: Final[str] = """
SELECT DISTINCT
    st1.stop_id AS source,
    st2.stop_id AS dest
    FROM
    stops_time AS st1
    JOIN
    stops_time AS st2
    ON st1.trip_id = st2.trip_id
    AND st2.stop_sequence = st1.stop_sequence + 1;
"""
TOP_N: Final[int] = 10

def main() -> None:
    """Compute the closeness centrality (undirected, unweighted)."""

    with sql3.connect(DB_PATH) as conn:
        # Create a DataFrame variable, which stores edges data
        edge_df: DataFrame = pd.read_sql_query(EDGE_LIST_SQL, conn)

        # Valid the dataframe
        print("Edges sample:\n", edge_df.head(5))
        # Check how many edges I loaded by how many rows (should be 2)
        print("Edges shape:", edge_df.shape)

        # Store all the nodes and the edges
        G: nx.Graph = nx.Graph()

        # Add edges to the dataframe
        for src, dst in edge_df.itertuples(index=False, name=None):
            G.add_edge(src, dst)

        # Confirm the graph size:
        print(
            "Graph has",
            G.number_of_nodes(),
            "nodes and",
            G.number_of_edges(),
            "edges",
        )

        # Call nx.closeness_centrality, which returns dict mapping each
        # node to its centrality score and store it
        centrality_dict: dict[int, float] = nx.closeness_centrality(G)

        # Convert computed centrality to the DataFrame
        centrality_df: DataFrame = (
            pd.DataFrame.from_dict(centrality_dict, orient="index", columns=["centrality"])
            .reset_index()
            .rename(columns={"index": "stop_id"})
        )

        # Attach human-readable stop names
        stops_df: DataFrame = pd.read_sql_query(
            "SELECT stop_id, stop_name FROM stops;", conn
        )
        stops_df["stop_id"] = stops_df["stop_id"].astype(int)
        centrality_df["stop_id"] = centrality_df["stop_id"].astype(int)

        merged = centrality_df.merge(stops_df, on="stop_id")

        # Order the rows by the highest centrality first and limit
        top10 = merged.sort_values("centrality", ascending=False).head(TOP_N)

        # Display result
        print(top10[["stop_id", "stop_name", "centrality"]])


if __name__ == "__main__":
    main()
