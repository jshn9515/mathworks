from collections import defaultdict
from collections.abc import Generator
from itertools import islice

import networkx as nx
import pandas as pd


def k_shortest_paths_length(
    G: nx.DiGraph, source: str, target: str, k: int
) -> Generator[float]:
    paths = islice(
        nx.shortest_simple_paths(G, source, target, weight='固定成本 (Fixed cost)'), k
    )
    for path in paths:
        weight = 0
        for i in range(len(path) - 1):
            weight += G[path[i]][path[i + 1]]['固定成本 (Fixed cost)']
        yield weight


def calculate_price(cargo: int, cost: list[float]) -> float:
    count = cargo // 200
    if cargo % 200 == 0:
        count -= 1
    price = (
        cost[count] * (1 + ((cargo - 200 * count) / 200) ** 3) + sum(cost[:count]) * 2
    )
    return price


df1 = pd.read_excel(
    '附件/附件2(Attachment 2)2023-51MCM-Problem B.xlsx', index_col=0, parse_dates=True
)
df2 = pd.read_excel('附件/附件3(Attachment 3)2023-51MCM-Problem B.xlsx')

time_range = pd.date_range('2023-04-23', '2023-04-27', freq='D')
time_range = time_range.strftime('%Y-%m-%d')

G = nx.from_pandas_edgelist(
    df2,
    source='起点 (Start)',
    target='终点 (End)',
    edge_attr='固定成本 (Fixed cost)',
    create_using=nx.DiGraph,
)

result = defaultdict(dict)
for time in time_range:
    for city1, city2, cargo in df1.loc[time].itertuples(index=False):
        cost = []
        for weight in k_shortest_paths_length(G, city1, city2, 5):
            cost.append(weight)
        result[time][f'{city1}-{city2}'] = calculate_price(cargo, cost)

result = pd.DataFrame(result)
result.fillna(0, inplace=True)
result.sort_index(inplace=True)
result.loc['总运费'] = result.sum()
result.to_excel(
    '问题4-城市快递运输费用.xlsx',
    sheet_name='运费',
    index_label='快递运输路线',
    float_format='%.4f',
)
