import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt

sheets = list(map(str, range(2024, 2031)))
df1 = pd.read_excel('问题2-结果.xlsx', sheet_name=sheets, index_col=[0, 1])
df2 = pd.read_excel('附件/附件-农作物汇总表.xlsx', sheet_name='销售单价', index_col=0)
df2.fillna(0, inplace=True)
df3 = pd.read_excel('附件/附件-农作物汇总表.xlsx', sheet_name='种植成本', index_col=0)
df3.fillna(0, inplace=True)
df4 = pd.read_excel('附件/附件-农作物汇总表.xlsx', sheet_name='亩产量', index_col=[0, 1])
df4.fillna(0, inplace=True)
df5 = pd.read_excel('附件/附件-农作物汇总表.xlsx', sheet_name='种植面积', index_col=[0, 1])
df5.fillna(0, inplace=True)

lands = 82
crops = 41
years = 7
seasons = 2

data = np.zeros((lands, crops, years))
for k in range(years):
    data[:, :, k] = df1[sheets[k]].to_numpy()
data = np.sum(data, axis=0)
# to avoid zero division
data += 0.0001 * np.random.rand(crops, years)
corr = np.corrcoef(data)
fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
sns.heatmap(corr, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)

price = df2.sum().to_numpy().reshape(-1, 1)
cost = df3.sum().to_numpy().reshape(-1, 1)
y = (df4 * df5).sum().to_numpy()
X = np.hstack((price, cost))
X = sm.add_constant(X)
Mdl = sm.OLS(y, X)
Mdl = Mdl.fit()
with open('问题3-指标回归结果.html', 'w') as fp:
    summary = Mdl.summary()
    fp.write(summary.as_html())

plt.show()
