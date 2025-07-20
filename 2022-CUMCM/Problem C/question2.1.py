import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

df1 = pd.read_excel(
    'attachment/附件-预处理后数据.xlsx', sheet_name='表单1', index_col=0
)
df2 = pd.read_excel(
    'attachment/附件-预处理后数据.xlsx', sheet_name='表单4', index_col=0
)

P1 = pd.crosstab(
    index=df1['类型'], columns=df1['颜色'], margins=True, margins_name='总计'
)
P2 = pd.crosstab(
    index=df1['类型'], columns=df1['纹饰'], margins=True, margins_name='总计'
)
P3 = pd.crosstab(
    index=df1['类型'], columns=df1['表面风化'], margins=True, margins_name='总计'
)

encoder = LabelEncoder()
for col in df1.columns:
    df1[col] = encoder.fit_transform(df1[col])

X = df1.drop(columns='类型')
y = df1['类型']

Mdl1 = DecisionTreeClassifier()
Mdl1.fit(X, y)
score = Mdl1.score(X, y)
print(f'The accuracy of CART is: {score:.2f}')
imp = Mdl1.feature_importances_

sns.set_theme(context='paper', style='darkgrid', font='DengXian', font_scale=1.8)

plt.rc('figure', figsize=(15, 8))

fig = plt.figure(1)
ax = fig.add_axes((0.35, 0.05, 0.3, 0.92))
h = ax.bar(X.columns, imp, width=0.4, linewidth=0.8, edgecolor='black', alpha=0.8)
ax.bar_label(h, fmt='%.2f', padding=4)
fig.savefig('data/问题2-决策树重要性比较图.svg')

df_BaO2 = df2[df2['类型'] == '铅钡']
df_KMnO4 = df2[df2['类型'] == '高钾']
df_BaO2 = df_BaO2.select_dtypes(include='number')
df_KMnO4 = df_KMnO4.select_dtypes(include='number')
df_diff = (df_BaO2.mean() - df_KMnO4.mean()).abs()

df_diff = df_diff.to_frame('差异程度')
df_diff['排名'] = df_diff.rank(method='max', ascending=False).astype(int)
df_diff.sort_values('排名', inplace=True)
df_diff.index.rename('化学成分', inplace=True)

top3 = df_diff.index[:3].to_list()
X = df2[top3].select_dtypes(include='number')
y = df2['类型']
Mdl2 = SVC(kernel='linear')
Mdl2.fit(X, y)
score = Mdl2.score(X, y)
print(f'The accuracy of SVM is: {score:.2f}')
