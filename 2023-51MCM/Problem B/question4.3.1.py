import itertools
from collections import defaultdict

import matplotlib.pyplot as plt
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
sensitivity = list(range(195, 210, 5))
columns = ['Cargo-' + str(i) for i in sensitivity]

G: nx.DiGraph = nx.from_pandas_edgelist(
    df2,
    source='Start',
    target='End',
    edge_attr='Cost',
    create_using=nx.DiGraph,
)

df = pd.DataFrame(index=time_range, columns=columns)
df.index.name = 'Date'

for base in sensitivity:
    single = defaultdict(dict)

    for time in time_range:
        for s, t, cargo in df1.loc[time].itertuples(index=False):
            count = cargo // base
            if cargo % base == 0:
                count -= 1
            price = 0
            for path in k_shortest_paths(G, s, t, count + 1):
                for i, j in itertools.pairwise(path):
                    if cargo >= base:
                        price += G[i][j]['Cost'] * 2
                    else:
                        price += G[i][j]['Cost'] * (1 + (cargo / base) ** 3)
                cargo -= base
            single[time][f'{s}-{t}'] = price

    single = pd.DataFrame(single)
    single.fillna(0, inplace=True)
    single.sort_index(inplace=True)
    df[f'Cargo-{base}'] = single.sum()

with pd.ExcelWriter(
    'data/问题4-城市快递运输费用.xlsx',
    engine='openpyxl',
    mode='a',
    if_sheet_exists='replace',
) as writer:
    df.to_excel(writer, sheet_name='启发式算法敏感性检验', float_format='%.4f')

plt.rc('font', family='Source Han Serif SC', size=16)
plt.figure(1, figsize=(15, 8))
plt.plot(df, '-o')
plt.ylabel('总运费')
plt.legend(df.columns)
plt.subplots_adjust(left=0.08, bottom=0.05, right=0.95, top=0.95)
plt.savefig('data/问题4-启发式算法敏感性检验.svg', dpi=300)
