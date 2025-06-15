import itertools
from collections import defaultdict

import networkx as nx
import pandas as pd


def k_shortest_paths(G: nx.DiGraph, source: str, target: str, k: int):
    it = nx.shortest_simple_paths(G, source, target, weight='Cost')
    paths = itertools.islice(it, k)
    for path in paths:
        yield path


df1 = pd.read_parquet('attachment/附件2.parquet')
df2 = pd.read_parquet('attachment/附件3.parquet')

time_range = pd.date_range('2023-04-23', '2023-04-27', freq='D')
time_range = time_range.strftime('%Y-%m-%d')

G: nx.DiGraph = nx.from_pandas_edgelist(
    df2,
    source='Start',
    target='End',
    edge_attr='Cost',
    create_using=nx.DiGraph,
)

result = defaultdict(dict)
for time in time_range:
    for start, end, cargo in df1.loc[time].itertuples(index=False):
        count = cargo // 200
        if cargo % 200 == 0:
            count -= 1
        price = 0
        for path in k_shortest_paths(G, start, end, count + 1):
            for i, j in itertools.pairwise(path):
                if cargo >= 200:
                    price += G[i][j]['Cost'] * 2
                else:
                    price += G[i][j]['Cost'] * (1 + (cargo / 200) ** 3)
            cargo -= 200
        result[time][f'{start}-{end}'] = price

result = pd.DataFrame(result)
result.fillna(0, inplace=True)
result.sort_index(inplace=True)
result.loc['Total'] = result.sum()
result.index.name = 'Route'
result.to_excel(
    'data/问题4-城市快递运输费用.xlsx', sheet_name='启发式算法', float_format='%.4f'
)
