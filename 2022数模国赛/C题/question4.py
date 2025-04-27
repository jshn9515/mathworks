import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import seaborn as sns

df = pd.read_excel('附件/附件-预处理后数据.xlsx', sheet_name='表单4', index_col=0)

df1 = df[df['类型'] == '铅钡']
df2 = df[df['类型'] == '高钾']
df1 = df1.select_dtypes(include='number')
df2 = df2.select_dtypes(include='number')

alpha = 0.05

stat1 = []
for col in df1.columns:
    stat1.append(stats.kstest(df1[col], 'norm'))

result1 = [
    [s.pvalue < alpha for s in stat1],
    [s.pvalue for s in stat1],
    [s.statistic for s in stat1],
]

stat2 = []
for col in df2.columns:
    stat2.append(stats.kstest(df2[col], 'norm'))

result2 = [
    [s.pvalue < alpha for s in stat2],
    [s.pvalue for s in stat2],
    [s.statistic for s in stat2],
]

result1 = pd.DataFrame(result1, columns=df1.columns, index=['h', 'pvalue', 'statistic'])
result2 = pd.DataFrame(result2, columns=df2.columns, index=['h', 'pvalue', 'statistic'])

with pd.ExcelWriter('问题4-K-S检验.xlsx') as writer:
    result1.to_excel(writer, sheet_name='铅钡', float_format='%.4f')
    result2.to_excel(writer, sheet_name='高钾', float_format='%.4f')

labels = df1.columns.str.replace(r'\(.*?\)', '', regex=True)
labels = labels.to_list()

plt.rc('font', family=['DejaVu Sans', 'DengXian'], size=12)
plt.rc('axes', unicode_minus=False)

plt.figure(1)
sns.heatmap(
    df1.corr(),
    annot=True,
    cmap='coolwarm',
    fmt='.2f',
    xticklabels=labels,
    yticklabels=labels,
    annot_kws=dict(fontsize=10),
)
plt.xticks(rotation=30)

plt.figure(2)
sns.heatmap(
    df2.corr(),
    annot=True,
    cmap='coolwarm',
    fmt='.2f',
    xticklabels=labels,
    yticklabels=labels,
    annot_kws=dict(fontsize=10),
)
plt.xticks(rotation=30)

plt.show()
