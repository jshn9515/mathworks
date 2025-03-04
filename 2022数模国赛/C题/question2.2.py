import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as cluster
import seaborn as sns
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.svm import SVC

df = pd.read_excel('附件/附件-预处理后数据.xlsx', sheet_name='表单4', index_col=0)

df1 = df[df['类型'] == '铅钡']
df2 = df[df['类型'] == '高钾']
df1 = df1.select_dtypes(include='number')
df2 = df2.select_dtypes(include='number')
var1 = df1.var().sort_values(ascending=False)
var2 = df2.var().sort_values(ascending=False)
var1 = var1.index[:2].to_list()
var2 = var2.index[:2].to_list()
print(f'铅钡玻璃使用{var1[0]}，{var1[1]}作为分类依据')
print(f'高钾玻璃使用{var2[0]}，{var2[1]}作为分类依据')
df1 = df1[var1]
df2 = df2[var2]

sns.set_theme(
    context='paper',
    style='darkgrid',
    font='DengXian',
    font_scale=1.8,
    rc={'axes.unicode_minus': False},
)

L1 = cluster.linkage(df1, method='ward')
L2 = cluster.linkage(df2, method='ward')
fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
cluster.dendrogram(L1, labels=df1.index, ax=ax)
fig = plt.figure(2)
ax = fig.add_subplot(1, 1, 1)
cluster.dendrogram(L2, labels=df2.index, ax=ax)
T1 = cluster.fcluster(L1, 3, criterion='maxclust')
T2 = cluster.fcluster(L2, 3, criterion='maxclust')

df4 = pd.Series(T1, index=df1.index, name='类别')
df5 = pd.Series(T2, index=df2.index, name='类别')

with pd.ExcelWriter('问题2-铅钡高钾聚类数据.xlsx') as writer:
    df4.to_excel(writer, sheet_name='铅钡')
    df5.to_excel(writer, sheet_name='高钾')

Mdl1 = SVC(kernel='linear')
Mdl1.fit(df1, T1)
score = Mdl1.score(df1, T1)
print(f'铅钡模型准确率：{score:.2f}')
fig = plt.figure(3)
ax = fig.add_subplot(1, 1, 1)
DecisionBoundaryDisplay.from_estimator(
    Mdl1,
    df1,
    grid_resolution=1000,
    plot_method='contour',
    ax=ax,
    levels=[-1, 0, 1],
    colors='black',
)
scatter = ax.scatter(
    df1[var1[0]], df1[var1[1]], c=T1, s=30, cmap='viridis', edgecolors='black'
)
ax.scatter(
    Mdl1.support_vectors_[:, 0],
    Mdl1.support_vectors_[:, 1],
    s=150,
    facecolors='none',
    edgecolors='black',
)
ax.legend(*scatter.legend_elements(), loc='upper right', title='Classes')

Mdl2 = SVC(kernel='linear')
Mdl2.fit(df2, T2)
score = Mdl2.score(df2, T2)
print(f'高钾模型准确率：{score:.2f}')
fig = plt.figure(4)
ax = fig.add_subplot(1, 1, 1)
DecisionBoundaryDisplay.from_estimator(
    Mdl2,
    df2,
    grid_resolution=1000,
    plot_method='contour',
    ax=ax,
    levels=[-1, 0, 1],
    colors='black',
)
scatter = ax.scatter(
    df2[var2[0]], df2[var2[1]], c=T2, s=30, cmap='viridis', edgecolors='black'
)
ax.scatter(
    Mdl2.support_vectors_[:, 0],
    Mdl2.support_vectors_[:, 1],
    s=150,
    facecolors='none',
    edgecolors='black',
)
ax.legend(*scatter.legend_elements(), loc='upper right', title='Classes')

plt.show()
