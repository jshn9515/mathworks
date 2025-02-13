import networkx as nx
import pandas as pd

df1 = pd.read_excel('附件/附件1(Attachment 1)2023-51MCM-Problem B.xlsx', index_col=0, parse_dates=True)

G = nx.from_pandas_edgelist(
    df1,
    source='收货城市 (Receiving city)',
    target='发货城市 (Delivering city)',
    edge_attr='快递运输数量(件) (Express delivery quantity (PCS))',
    create_using=nx.DiGraph
)
rank = nx.pagerank(G, alpha=0.85, weight='快递运输数量(件) (Express delivery quantity (PCS))')

df2 = pd.DataFrame.from_dict(dict(rank), orient='index', columns=['得分'])
df2['排名'] = df2.rank(method='max', ascending=False)
df2.rename_axis('城市', inplace=True)
df2.sort_index(inplace=True)
df2.to_excel('问题1-城市快递运输量得分.xlsx', float_format='%.4f')
