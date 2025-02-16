import pandas as pd

df = pd.read_excel('附件/secondary_data.xlsx')
df.to_pickle('附件/secondary_data.pkl', compression='zip')
