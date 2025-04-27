import pandas as pd

df = pd.read_excel('附件/secondary_data.xlsx')
df.to_parquet('附件/secondary_data.parquet', compression='gzip')
