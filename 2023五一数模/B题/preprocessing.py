import pandas as pd

df1 = pd.read_excel('附件/附件2(Attachment 2)2023-51MCM-Problem B.xlsx', index_col=0, parse_dates=True)
df1.to_parquet('附件/附件2(Attachment 2)2023-51MCM-Problem B.parquet', compression='gzip')
