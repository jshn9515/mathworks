import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_parquet('附件/secondary_data.parquet')

profile = ProfileReport(df, title='问题1-蘑菇总表分析')
profile.to_file('问题1-蘑菇总表分析.html')
