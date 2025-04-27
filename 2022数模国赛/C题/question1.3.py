import pandas as pd
import skbio.stats.composition as comp

df = pd.read_excel('附件/附件-预处理后数据.xlsx', sheet_name='表单4', index_col=0)

df1 = df[(df['表面风化'] == '风化') & (df['类型'] == '铅钡')]
df2 = df[(df['表面风化'] == '无风化') & (df['类型'] == '铅钡')]
df3 = df[(df['表面风化'] == '风化') & (df['类型'] == '高钾')]
df4 = df[(df['表面风化'] == '无风化') & (df['类型'] == '高钾')]
df1 = df1.select_dtypes(include='number')
df2 = df2.select_dtypes(include='number')
df3 = df3.select_dtypes(include='number')
df4 = df4.select_dtypes(include='number')

df1 = df1 + (df2.mean() - df1.mean())
df3 = df3 + (df4.mean() - df3.mean())

df1[:] = comp.clr_inv(df1.to_numpy()) * 100
df3[:] = comp.clr_inv(df3.to_numpy()) * 100

with pd.ExcelWriter('问题1-铅钡高钾还原数据.xlsx') as writer:
    df1.to_excel(writer, sheet_name='铅钡-还原', float_format='%.2f')
    df3.to_excel(writer, sheet_name='高钾-还原', float_format='%.2f')
