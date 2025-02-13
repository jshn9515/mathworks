import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import seaborn as sns
from matplotlib.ticker import FuncFormatter

df = pd.read_excel('附件/附件-预处理后数据.xlsx', sheet_name='表单4', index_col=0)
df1 = df[df['表面风化'] == '风化']
df2 = df[df['表面风化'] == '无风化']
df1 = df1.select_dtypes(include='number')
df2 = df2.select_dtypes(include='number')
columns = df1.columns.to_list()

sns.set_theme(context='paper', style='darkgrid', font='DengXian', font_scale=1.2,
              rc={'axes.unicode_minus': False})

fig = plt.figure(1)
for i, col in enumerate(columns):
    ax = fig.add_subplot(3, 5, i + 1)
    sns.boxplot(df, x='表面风化', y=col, hue='表面风化', order=['风化', '无风化'], width=0.5, legend=False, ax=ax)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(col, fontsize=12)
plt.subplots_adjust(hspace=0.3)

fig = plt.figure(2)
for i, col in enumerate(columns):
    ax = fig.add_subplot(3, 5, i + 1)
    sns.kdeplot(df, x=col, hue='表面风化', hue_order=['风化', '无风化'], fill=True, ax=ax)
    ax.set_xlabel('')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}'))
    ax.get_legend().set_loc('upper right')
    ax.set_title(col, fontsize=12)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.3)

stat = []
alpha = 0.05
for name in columns:
    stat.append(stats.ranksums(df1[name], df2[name]))

result = [
    [s.pvalue < alpha for s in stat],
    [s.pvalue for s in stat],
    [s.statistic for s in stat]
]

result = pd.DataFrame(result, columns=columns, index=['h', 'pvalue', 'statistic'])
with pd.ExcelWriter('问题1-假设检验.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    result.to_excel(writer, sheet_name='秩和检验', float_format='%.4f')

plt.show()
