from typing import cast

import numpy as np
import pandas as pd
import scipy.signal as signal
from xgboost.sklearn import XGBRegressor

df = pd.read_parquet('附件/附件2(Attachment 2)2023-51MCM-Problem B.parquet')
df.index = cast(pd.DatetimeIndex, df.index)

df['Year'] = df.index.year
df['Season'] = df.index.month // 3 + 1

df.insert(
    loc=0,
    column='Pair',
    value=df.Deliver + '-' + df.Receiver,
)
df.drop(columns=['Deliver', 'Receiver'], inplace=True)
df.set_index(['Year', 'Season', 'Pair'], inplace=True)
df.columns = ['PCS']


def apply_detrend(series: pd.DataFrame) -> float:
    group = series.to_numpy()
    assert group.ndim == 1
    trend = signal.detrend(group)
    trend = np.clip(trend, 0, group)
    return round(np.sum(trend))


grouped = df.groupby(['Year', 'Season', 'Pair'])
df1 = grouped.aggregate(apply_detrend)
df2 = grouped.sum()
df1.columns = ['Constant']
df2.columns = ['PCS']
df1.sort_index(inplace=True)
df1.to_excel('问题5-固定需求常数.xlsx', float_format='%.0f')

X = df2.to_numpy().reshape(-1, 1)
y = df1.to_numpy()
assert X.size == y.size

Mdl = XGBRegressor()
Mdl.fit(X, y)
score = Mdl.score(X, y)
print(f'R2 score of this model is: {score:.4f}')
