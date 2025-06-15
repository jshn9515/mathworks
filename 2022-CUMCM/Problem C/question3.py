import pandas as pd
import scipy.cluster.hierarchy as cluster
from sklearn.svm import SVC

df1 = pd.read_excel(
    'attachment/附件-预处理后数据.xlsx', sheet_name='表单4', index_col=0
)
df2 = pd.read_excel(
    'attachment/附件-预处理后数据.xlsx', sheet_name='表单3', index_col=0
)
df2 = df2.select_dtypes(include='number')

df_BaO2 = df1[df1['类型'] == '铅钡']
df_KMnO4 = df1[df1['类型'] == '高钾']
df_BaO2 = df_BaO2.select_dtypes(include='number')
df_KMnO4 = df_KMnO4.select_dtypes(include='number')

df_diff = (df_BaO2.mean() - df_KMnO4.mean()).abs()
df_diff = df_diff.to_frame('差异程度')
df_diff['排名'] = df_diff.rank(method='max', ascending=False).astype(int)
df_diff.sort_values('排名', inplace=True)
df_diff.index.rename('化学成分', inplace=True)

top3 = df_diff.index[:3].to_list()
X = df1[top3].select_dtypes(include='number')
y = df1['类型']
Mdl1 = SVC(kernel='linear')
Mdl1.fit(X, y)
score1 = Mdl1.score(X, y)
predict1 = Mdl1.predict(df2[top3])
print(f'Phrase 1: The accuracy of SVM model is: {score1:.2f}')

df_pred_BaO2 = df2[predict1 == '铅钡']
df_pred_KMnO4 = df2[predict1 == '高钾']

var_BaO2 = df_BaO2.var().sort_values(ascending=False)
var_KMnO4 = df_KMnO4.var().sort_values(ascending=False)
var_BaO2 = var_BaO2.index[:2].to_list()
var_KMnO4 = var_KMnO4.index[:2].to_list()
print(
    f'The BaO2 glasses use {var_BaO2[0]} and {var_BaO2[1]} as classification criteria...'
)
print(
    f'The KMnO4 glasses use {var_KMnO4[0]} and {var_KMnO4[1]} as classification criteria...'
)
df_BaO2 = df_BaO2[var_BaO2]
df_KMnO4 = df_KMnO4[var_KMnO4]

T_BaO2 = cluster.fclusterdata(df_BaO2, 3, criterion='maxclust', method='ward')
T_KMnO4 = cluster.fclusterdata(df_KMnO4, 3, criterion='maxclust', method='ward')

Mdl21 = SVC(kernel='linear')
Mdl21.fit(df_BaO2, T_BaO2)
score21 = Mdl21.score(df_BaO2, T_BaO2)
predict21 = Mdl21.predict(df_pred_BaO2[var_BaO2])
print(f'Phrase 2: the accuray of BaO2 is: {score21:.2f}')

Mdl22 = SVC(kernel='linear')
Mdl22.fit(df_KMnO4, T_KMnO4)
score22 = Mdl22.score(df_KMnO4, T_KMnO4)
predict22 = Mdl22.predict(df_pred_KMnO4[var_KMnO4])
print(f'Phrase 2: the accuray of KMnO4 is: {score22:.2f}')

print(f'The classification result of BaO2 is: {predict21}')
print(f'The classification result of KMnO4 is: {predict22}')
