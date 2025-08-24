from itertools import islice

import networkx as nx
import pandas as pd


def k_shortest_paths(G: nx.DiGraph, source: str, target: str, k: int):
    it = nx.shortest_simple_paths(G, source, target, weight='Cost')
    return list(islice(it, k))


df1 = pd.read_parquet('attachment/附件3.parquet')

G = nx.from_pandas_edgelist(
    df1,
    source='Start',
    target='End',
    edge_attr='Cost',
    create_using=nx.DiGraph,
)

start, end = 'G', 'V'
for path in k_shortest_paths(G, start, end, 5):
    print(path)
