from itertools import islice

import networkx as nx
import pandas as pd


def k_shortest_paths(G: nx.DiGraph, source: str, target: str, k: int) -> list[float]:
    return list(
        islice(
            nx.shortest_simple_paths(G, source, target, weight='Cost'),
            k,
        )
    )


df1 = pd.read_parquet('附件/附件2(Attachment 2)2023-51MCM-Problem B.parquet')
df2 = pd.read_parquet('附件/附件3(Attachment 3)2023-51MCM-Problem B.parquet')
assert not df2.duplicated().all()

G = nx.from_pandas_edgelist(
    df2,
    source='Start',
    target='End',
    edge_attr='Cost',
    create_using=nx.DiGraph,
)

city1, city2 = 'G', 'V'
for path in k_shortest_paths(G, city1, city2, 5):
    print(path)
