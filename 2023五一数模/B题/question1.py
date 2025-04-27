import networkx as nx
import pandas as pd

df1 = pd.read_parquet('附件/附件1(Attachment 1)2023-51MCM-Problem B.parquet')

df1 = df1.groupby(['Deliver', 'Receiver']).sum().reset_index()

G = nx.from_pandas_edgelist(
    df1,
    source='Deliver',
    target='Receiver',
    edge_attr='PCS',
    create_using=nx.DiGraph,
)
rank = nx.pagerank(G, alpha=0.85, weight='PCS')

df2 = pd.DataFrame.from_dict(dict(rank), orient='index', columns=['Score'])
df2['Rank'] = df2.rank(method='max', ascending=False)
df2.index.name = 'City'
df2.sort_index(inplace=True)
df2.to_excel('问题1-城市快递运输量得分.xlsx', float_format='%.4f')
