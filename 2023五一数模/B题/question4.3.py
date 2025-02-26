from collections import defaultdict
from collections.abc import Generator
from itertools import islice

import matplotlib.pyplot as plt
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


def calculate_price(base: int, cargo: int, cost: list[float]) -> float:
    count = cargo // base
    if cargo % base == 0:
        count -= 1
    price = (
        cost[count] * (1 + ((cargo - base * count) / base) ** 3) + sum(cost[:count]) * 2
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

sensitivity = list(range(195, 210, 5))
df = pd.DataFrame(
    index=time_range, columns=['额定装货量-' + str(i) for i in sensitivity]
)
for base in sensitivity:
    single = defaultdict(dict)
    for time in time_range:
        for city1, city2, cargo in df1.loc[time].itertuples(index=False):
            cost = []
            for weight in k_shortest_paths_length(G, city1, city2, 5):
                cost.append(weight)
            single[time][f'{city1}-{city2}'] = calculate_price(base, cargo, cost)
    single = pd.DataFrame(single)
    single.fillna(0, inplace=True)
    single.sort_index(inplace=True)
    df[f'额定装货量-{base}'] = single.sum()

with pd.ExcelWriter(
    '问题4-城市快递运输费用.xlsx',
    engine='openpyxl',
    mode='a',
    if_sheet_exists='replace',
) as writer:
    df.to_excel(
        writer, sheet_name='敏感性检验', index_label='日期', float_format='%.4f'
    )

plt.rc('font', family='DengXian', size=12)
plt.figure(1)
plt.plot(df.index, df.values, '-o')
plt.legend(df.columns)
plt.show()
