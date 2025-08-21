import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

df1 = pd.read_parquet('attachment/附件1.parquet')

df1 = df1.groupby(['Deliver', 'Receiver']).sum().reset_index()

G = nx.from_pandas_edgelist(
    df1,
    source='Deliver',
    target='Receiver',
    edge_attr='PCS',
    create_using=nx.DiGraph,
)

plt.rc('font', family='Source Han Serif SC', size=16)
plt.rc('figure', figsize=(15, 8))

fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
pos = nx.kamada_kawai_layout(G)
nx.draw_networkx_nodes(
    G,
    pos=pos,
    node_size=30,
    node_color='#1171BE',
    ax=ax,
)
nx.draw_networkx_edges(
    G,
    pos=pos,
    node_size=30,
    edge_color='#88B8DE',
    width=0.6,
    connectionstyle='arc3,rad=0.15',
    ax=ax,
)
nx.draw_networkx_labels(
    G,
    pos={k: v + 0.024 for k, v in pos.items()},
    font_family=plt.rcParams['font.family'],
    font_weight='bold',
    font_size=plt.rcParams['font.size'] * 0.9,
    ax=ax,
)
fig.subplots_adjust(left=0.03, bottom=0.03, right=0.97, top=0.97)
plt.savefig('data/问题1-城市快递运输量网络图.svg')

# TODO: Consider time varying PageRank
# For now, we use a static PageRank based on the total PCS
rank = nx.pagerank(G, alpha=0.85, weight='PCS')

df2 = pd.DataFrame.from_dict(rank, orient='index', columns=['Score'])
df2['Rank'] = df2.rank(method='max', ascending=False).astype(int)
df2.reset_index(names='City', inplace=True)
df2.set_index(keys='Rank', verify_integrity=True, inplace=True)
df2['Income'] = [G.in_degree(city, weight='PCS') for city in df2.City]
df2['Outcome'] = [G.out_degree(city, weight='PCS') for city in df2.City]
df2['Pred'] = [G.in_degree(city) for city in df2.City]
df2['Succ'] = [G.out_degree(city) for city in df2.City]
df2.sort_index(inplace=True)
df2.to_excel('data/问题1-城市快递运输量得分.xlsx', float_format='%.4f')

TypstExport = True
if TypstExport:
    df3 = df2.head()
    columns = ['城市', 'PageRank值', '收货量', '发货量', '上游路径数', '下游路径数']
    df3.to_csv(
        'data/问题1-城市快递运输量得分.csv',
        float_format='%.4f',
        index_label='排名',
        header=columns,
    )
