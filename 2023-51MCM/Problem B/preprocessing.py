import os

import pandas as pd

names = ['Date', 'Deliver', 'Receiver', 'PCS']
df1 = pd.read_excel(
    'attachment/附件1(Attachment 1)2023-51MCM-Problem B.xlsx',
    index_col=0,
    names=names,
    parse_dates=True,
)
df2 = pd.read_excel(
    'attachment/附件2(Attachment 2)2023-51MCM-Problem B.xlsx',
    index_col=0,
    names=names,
    parse_dates=True,
)
names = ['Start', 'End', 'Cost', 'Cargo']
df3 = pd.read_excel('附件/附件3(Attachment 3)2023-51MCM-Problem B.xlsx', names=names)

if not os.path.exists('data'):
    os.mkdir('data')

df1.to_parquet('attachment/附件1.parquet', compression='gzip')
df2.to_parquet('attachment/附件2.parquet', compression='gzip')
df3.to_parquet('attachment/附件3.parquet', compression='gzip')
