from typing import cast

import numpy as np
import pandas as pd
import scipy.integrate as integrate
import scipy.signal as signal
from sklearn.neighbors import KernelDensity

df1 = pd.read_excel(
    '附件/附件2(Attachment 2)2023-51MCM-Problem B.xlsx', index_col=0, parse_dates=True
)
df1.index = cast(pd.DatetimeIndex, df1.index)

df1['年份'] = df1.index.year
df1['季度'] = df1.index.month // 3 + 1

df1.insert(
    loc=0,
    column='发货-收货城市对',
    value=df1['发货城市 (Delivering city)'] + '-' + df1['收货城市 (Receiving city)'],
)
df1.drop(
    columns=['发货城市 (Delivering city)', '收货城市 (Receiving city)'], inplace=True
)
df1.set_index(['年份', '季度', '发货-收货城市对'], inplace=True)
df1.columns = ['快递运输数量']
df1.sort_index(inplace=True)


def apply_detrend(series: pd.Series) -> np.ndarray:
    group = series.to_numpy()
    trend = signal.detrend(group)
    trend = np.clip(trend, 0, group)
    trend = np.round(trend)
    return trend.astype(int)


grouped = df1.groupby(['年份', '季度', '发货-收货城市对'])
df2 = grouped.transform(apply_detrend)
df2.sort_index(inplace=True)
df2.columns = ['固定需求常数']

assert np.min(df1.values - df2.values) >= 0


def kernel_density_estimation(group: pd.DataFrame):
    X = group.to_numpy().reshape(-1, 1)
    Mdl = KernelDensity(kernel='gaussian', bandwidth=0.5)
    Mdl.fit(X)
    grid = np.linspace(np.min(X), np.max(X), 1000)
    pdf = np.exp(Mdl.score_samples(grid.reshape(-1, 1)))
    mean = integrate.simpson(grid * pdf, grid)
    var = integrate.simpson((grid - mean) ** 2 * pdf, grid)
    std = np.sqrt(var)
    df_mean.append(float(mean))
    df_std.append(float(std))


df_mean, df_std = [], []
df3 = grouped.aggregate(kernel_density_estimation)
df3 = pd.DataFrame(index=df3.index)
df3['均值'] = df_mean
df3['标准差'] = df_std
df3.to_excel('问题5-非固定需求均值和标准差.xlsx', float_format='%.2f')
