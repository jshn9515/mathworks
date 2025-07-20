import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import seaborn as sns

df = pd.read_excel('attachment/附件-预处理后数据.xlsx', sheet_name='表单4', index_col=0)

df1 = df[df['类型'] == '铅钡']
df2 = df[df['类型'] == '高钾']
df1 = df1.select_dtypes(include='number')
df2 = df2.select_dtypes(include='number')

alpha = 0.05

stat = []
for col in df1.columns:
    stat.append(stats.kstest(df1[col], df2[col]))

result = [
    [s.pvalue < alpha for s in stat],
    [s.pvalue for s in stat],
    [s.statistic for s in stat],
]

index = ['h', 'pvalue', 'statistic']
result = pd.DataFrame(result, index=index, columns=df1.columns)
result.to_excel('data/问题4-K-S检验.xlsx', float_format='%.4f')

labels = df1.columns.str.replace(r'\(.*?\)', '', regex=True)
labels = labels.to_list()

plt.rc('font', family=['DejaVu Sans', 'DengXian'], size=12)
plt.rc('axes', unicode_minus=False)
plt.rc('figure', figsize=(15, 8))

fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
sns.heatmap(
    df1.corr(),
    annot=True,
    cmap='coolwarm',
    fmt='.2f',
    xticklabels=labels,
    yticklabels=labels,
    annot_kws=dict(fontsize=10),
    ax=ax,
)
ax.tick_params('x', rotation=30)
fig.subplots_adjust(left=0.1, bottom=0.08, right=0.9, top=0.97)
fig.savefig('data/问题4-铅钡相关系数矩阵.svg')

fig = plt.figure(2)
ax = fig.add_subplot(1, 1, 1)
sns.heatmap(
    df2.corr(),
    annot=True,
    cmap='coolwarm',
    fmt='.2f',
    xticklabels=labels,
    yticklabels=labels,
    annot_kws=dict(fontsize=10),
    ax=ax,
)
ax.tick_params('x', rotation=30)
fig.subplots_adjust(left=0.1, bottom=0.08, right=0.9, top=0.97)
fig.savefig('data/问题4-高钾相关系数矩阵.svg')
