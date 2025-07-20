import numpy as np
import pandas as pd
import skbio.stats.composition as comp

df = pd.read_excel('attachment/附件-预处理后数据.xlsx', sheet_name='表单4', index_col=0)

df1 = df.query("类型 == '铅钡' and 表面风化 == '风化'")
df2 = df.query("类型 == '铅钡' and 表面风化 == '无风化'")
df3 = df.query("类型 == '高钾' and 表面风化 == '风化'")
df4 = df.query("类型 == '高钾' and 表面风化 == '无风化'")
df1 = df1.select_dtypes(include='number')
df2 = df2.select_dtypes(include='number')
df3 = df3.select_dtypes(include='number')
df4 = df4.select_dtypes(include='number')

TypstExport = True
if TypstExport:
    # Typst support, export as CSV table.
    df5 = pd.DataFrame(index=df1.columns)
    df5['铅钡风化后'] = df1.mean()
    df5['铅钡风化前'] = df2.mean()
    df5['铅钡均值差'] = df2.mean() - df1.mean()
    df5['高钾风化后'] = df3.mean()
    df5['高钾风化前'] = df4.mean()
    df5['高钾均值差'] = df4.mean() - df3.mean()
    df5.index = df5.index.str.extract(r'(.*?)\(', expand=False)
    df5.index.name = '化学元素'
    df5.to_csv(
        'data/问题1-各化学成分的均值差.csv', float_format='%.2f', encoding='utf_8_sig'
    )

df1 = df1 + (df2.mean() - df1.mean())
df3 = df3 + (df4.mean() - df3.mean())

df1[:] = np.asarray(comp.clr_inv(df1)) * 100
df3[:] = np.asarray(comp.clr_inv(df3)) * 100

with pd.ExcelWriter('data/问题1-铅钡高钾还原数据.xlsx') as writer:
    df1.to_excel(writer, sheet_name='铅钡-还原', float_format='%.2f')
    df3.to_excel(writer, sheet_name='高钾-还原', float_format='%.2f')

if TypstExport:
    # Typst support, export as CSV table.
    df1.columns = df1.columns.str.extract(r'(.*?)\(', expand=False)
    df3.columns = df3.columns.str.extract(r'(.*?)\(', expand=False)
    df1.to_csv('data/问题1-铅钡还原数据.csv', float_format='%.2f', encoding='utf_8_sig')
    df3.to_csv('data/问题1-高钾还原数据.csv', float_format='%.2f', encoding='utf_8_sig')
