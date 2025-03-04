from typing import cast

import numpy as np
import pandas as pd
import scipy.signal as signal
from xgboost.sklearn import XGBRegressor

df = pd.read_parquet('附件/附件2(Attachment 2)2023-51MCM-Problem B.parquet')
df.index = cast(pd.DatetimeIndex, df.index)

df['年份'] = df.index.year
df['季度'] = df.index.month // 3 + 1

df.insert(
    loc=0,
    column='发货-收货城市对',
    value=df['发货城市 (Delivering city)'] + '-' + df['收货城市 (Receiving city)'],
)
df.drop(
    columns=['发货城市 (Delivering city)', '收货城市 (Receiving city)'], inplace=True
)
df.set_index(['年份', '季度', '发货-收货城市对'], inplace=True)
df.columns = ['快递运输数量']


def apply_detrend(series: pd.DataFrame) -> float:
    group = series.to_numpy()
    assert group.ndim == 1
    trend = signal.detrend(group)
    trend = np.clip(trend, 0, group)
    return round(np.sum(trend))


grouped = df.groupby(['年份', '季度', '发货-收货城市对'])
df1 = grouped.aggregate(apply_detrend)
df2 = grouped.sum()
df1.columns = ['固定需求常数']
df2.columns = ['快递运输数量']
df1.sort_index(inplace=True)
df1.to_excel('问题5-固定需求常数.xlsx', float_format='%.0f')

X = df2.to_numpy().reshape(-1, 1)
y = df1.to_numpy()
assert X.size == y.size

Mdl = XGBRegressor()
Mdl.fit(X, y)
score = Mdl.score(X, y)
print(f'R2 score of this model is: {score:.4f}')
