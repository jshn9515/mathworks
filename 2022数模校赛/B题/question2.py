import pandas as pd
from ydata_profiling import ProfileReport

df: pd.DataFrame = pd.read_pickle('附件/secondary_data.pkl', compression='zip')
df1 = df[df['class'] == 'p'].copy()
df2 = df[df['class'] == 'e'].copy()

profile1 = ProfileReport(df1, title='edibile')
profile2 = ProfileReport(df2, title='poisonous')

report = profile1.compare(profile2)
report.to_file('问题1-有无毒蘑菇对比分析.html')
