import pandas as pd

df1 = pd.read_csv('附件/X_train.csv', index_col=0)
df2 = pd.read_csv('附件/y_train.csv', index_col=0)
df = pd.concat([df1, df2], axis=1)
df.to_parquet('附件/附件1-训练数据.parquet', compression='gzip')

df1 = pd.read_csv('附件/X_test.csv', index_col=0)
df2 = pd.read_csv('附件/y_test.csv', index_col=0)
df = pd.concat([df1, df2], axis=1)
df.to_parquet('附件/附件2-测试数据.parquet', compression='gzip')
