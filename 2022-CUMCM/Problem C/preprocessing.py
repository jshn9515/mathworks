import os
import statistics as stat

import numpy as np
import pandas as pd
import skbio.stats.composition as comp

df1 = pd.read_excel('attachment/附件.xlsx', sheet_name='表单1', index_col=0)
# fill the missing rows of table in column 'Color'
groups = df1.groupby(['纹饰', '类型', '表面风化'])
ngroup = groups.ngroup()
lookup = groups.aggregate(stat.mode)
lookup.reset_index(inplace=True)
idx = df1['颜色'].isna()
df1.loc[idx, '颜色'] = lookup.loc[ngroup[idx], '颜色'].values

df2 = pd.read_excel('attachment/附件.xlsx', sheet_name='表单2', index_col=0)
# drop out the total range exceed 85% ~ 105%
total = df2.sum(axis=1)
idx = ~((85 <= total) & (total <= 105))
df2.drop(df2.index[idx], inplace=True)
df2.fillna(0.04, inplace=True)
# calculate the CLR transform
df2[df2 == 0] += 0.04
df2[:] = comp.clr(df2.to_numpy())

df3 = pd.read_excel('attachment/附件.xlsx', sheet_name='表单3', index_col=[0, 1])
df3.fillna(0.04, inplace=True)
# calculate the CLR transform
df3[df3 == 0] += 0.04
df3.iloc[:] = np.asarray(comp.clr(df3))

# combine df1 and df2 together
df2['文物编号'] = df2.index
idx1 = df2.index.str.contains('严重风化点', na=False)
idx2 = df2.index.str.contains('未风化点', na=False)
df2.index = df2.index.astype(str)
df2.index = df2.index.str.extract(r'^(\d+)', expand=False)
df2.index = df2.index.astype(int)
df4 = df1.join(df2, how='right')
df4.loc[idx1, '表面风化'] = '风化'
df4.loc[idx2, '表面风化'] = '无风化'
df2.set_index('文物编号', inplace=True)
df4.set_index('文物编号', inplace=True)

if not os.path.exists('data'):
    os.mkdir('data')

with pd.ExcelWriter('attachment/附件-预处理后数据.xlsx') as writer:
    df1.to_excel(writer, sheet_name='表单1', float_format='%.2f')
    df2.to_excel(writer, sheet_name='表单2', float_format='%.2f')
    df3.to_excel(writer, sheet_name='表单3', float_format='%.2f')
    df4.to_excel(writer, sheet_name='表单4', float_format='%.2f')
