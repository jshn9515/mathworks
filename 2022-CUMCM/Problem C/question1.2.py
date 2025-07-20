import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import seaborn as sns
from matplotlib.ticker import FuncFormatter

df = pd.read_excel('attachment/附件-预处理后数据.xlsx', sheet_name='表单4', index_col=0)
df1 = df.query("类型 == '铅钡' and 表面风化 == '风化'")
df2 = df.query("类型 == '铅钡' and 表面风化 == '无风化'")
df3 = df.query("类型 == '高钾' and 表面风化 == '风化'")
df4 = df.query("类型 == '高钾' and 表面风化 == '无风化'")

df1 = df1.select_dtypes(include='number')
df2 = df2.select_dtypes(include='number')
df3 = df3.select_dtypes(include='number')
df4 = df4.select_dtypes(include='number')
columns = df1.columns.to_list()

sns.set_theme(
    context='paper',
    style='darkgrid',
    font='DengXian',
    font_scale=1.2,
    rc={'axes.unicode_minus': False},
)

plt.rc('figure', figsize=(15, 8))

fig = plt.figure(1)
for i, col in enumerate(columns):
    ax = fig.add_subplot(3, 5, i + 1)
    sns.boxplot(
        df,
        x='类型',
        y=col,
        hue='表面风化',
        order=['铅钡', '高钾'],
        hue_order=['无风化', '风化'],
        width=0.5,
        legend=False,
        ax=ax,
    )
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(col)
fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, hspace=0.3)
fig.savefig('data/问题1-风化前后化学成分含量箱线图.svg')

fig = plt.figure(2)
for i, col in enumerate(columns):
    ax = fig.add_subplot(4, 4, i + 1)
    sns.kdeplot(
        df[df['类型'] == '铅钡'],
        x=col,
        hue='表面风化',
        hue_order=['风化', '无风化'],
        palette=['#1F77B4', '#FF7E0D'],
        fill=True,
        ax=ax,
    )
    ax.set_xlabel('')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}'))
    ax.get_legend().set_loc('upper right')
    ax.set_title(col)
fig.subplots_adjust(
    left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.3, hspace=0.35
)
fig.savefig('data/问题1-风化前后铅钡化学成分含量核密度图.svg')

fig = plt.figure(3)
for i, col in enumerate(columns):
    ax = fig.add_subplot(4, 4, i + 1)
    sns.kdeplot(
        df[df['类型'] == '高钾'],
        x=col,
        hue='表面风化',
        hue_order=['风化', '无风化'],
        palette=['#1F77B4', '#FF7E0D'],
        fill=True,
        ax=ax,
    )
    ax.set_xlabel('')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}'))
    ax.get_legend().set_loc('upper right')
    ax.set_title(col)
fig.subplots_adjust(
    left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.3, hspace=0.35
)
fig.savefig('data/问题1-风化前后高钾化学成分含量核密度图.svg')

stat1 = []
alpha = 0.05
for name in columns:
    # MATLAB doc and Wiki clearly states that Mann-Whitney U test is equal to Wilcoxon rank-sum test.
    # But SciPy doc says Mann-Whitney U test provides better tie-handling and continuity correction.
    # So we use Mann-Whitney U test here.
    # ref: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
    stat1.append(stats.mannwhitneyu(df1[name], df2[name]))

stat2 = []
for name in columns:
    stat2.append(stats.mannwhitneyu(df3[name], df4[name]))

result1 = [
    [s.pvalue < alpha for s in stat1],
    [s.pvalue for s in stat1],
    [s.statistic for s in stat1],
]

result2 = [
    [s.pvalue < alpha for s in stat2],
    [s.pvalue for s in stat2],
    [s.statistic for s in stat2],
]

result1 = pd.DataFrame(result1, columns=columns, index=['h', 'pvalue', 'statistic'])
result2 = pd.DataFrame(result2, columns=columns, index=['h', 'pvalue', 'statistic'])

with pd.ExcelWriter(
    'data/问题1-假设检验.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace'
) as writer:
    result1.to_excel(writer, sheet_name='铅钡玻璃秩和检验', float_format='%.4f')
    result2.to_excel(writer, sheet_name='高钾玻璃秩和检验', float_format='%.4f')
