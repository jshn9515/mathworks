from itertools import islice

import networkx as nx
import pandas as pd


def k_shortest_paths(G: nx.DiGraph, source: str, target: str, k: int) -> list[float]:
    return list(
        islice(
            nx.shortest_simple_paths(G, source, target, weight='固定成本 (Fixed cost)'),
            k,
        )
    )


df1 = pd.read_parquet('附件/附件2(Attachment 2)2023-51MCM-Problem B.parquet')
df2 = pd.read_excel('附件/附件3(Attachment 3)2023-51MCM-Problem B.xlsx')

G = nx.from_pandas_edgelist(
    df2,
    source='起点 (Start)',
    target='终点 (End)',
    edge_attr='固定成本 (Fixed cost)',
    create_using=nx.DiGraph,
)

city1, city2 = 'G', 'V'
for path in k_shortest_paths(G, city1, city2, 5):
    print(path)
