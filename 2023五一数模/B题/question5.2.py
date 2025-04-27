from functools import partial
from typing import Literal, cast

import numpy as np
import pandas as pd
import scipy.integrate as integrate
import scipy.signal as signal
import scipy.stats as stats

df1 = pd.read_parquet('附件/附件2(Attachment 2)2023-51MCM-Problem B.parquet')
df1.index = cast(pd.DatetimeIndex, df1.index)

df1['Year'] = df1.index.year
df1['Season'] = df1.index.month // 3 + 1

df1.insert(
    loc=0,
    column='Pair',
    value=df1.Deliver + '-' + df1.Receiver,
)
df1.drop(columns=['Deliver', 'Receiver'], inplace=True)
df1.set_index(['Year', 'Season', 'Pair'], inplace=True)
df1.columns = ['Cargo']
df1.sort_index(inplace=True)


def apply_detrend(series: pd.Series) -> np.ndarray:
    group = series.to_numpy()
    trend = signal.detrend(group)
    trend = np.clip(trend, 0, group)
    trend = np.round(trend)
    return trend.astype(int)


df2 = df1.groupby(['Year', 'Season', 'Pair']).transform(apply_detrend)
df2.sort_index(inplace=True)
df2.columns = ['Constant']

df3 = df1.values - df2.values
df3 = pd.DataFrame(df3, index=df2.index, columns=['Variation'])
assert np.min(df3) >= 0


def kernel_density_estimation(
    group: pd.DataFrame, flag: Literal['mean', 'std']
) -> float:
    X = group.to_numpy()
    if X.size == 1:
        mean = float(np.squeeze(X))
        std = 0
        return mean if flag == 'mean' else std
    try:
        Mdl = stats.gaussian_kde(X, bw_method='silverman')
    except np.linalg.LinAlgError:
        mean = float(np.mean(X))
        std = float(np.std(X))
        return mean if flag == 'mean' else std
    else:
        grid = np.linspace(np.min(X), np.max(X), 1000)
        pdf = Mdl.evaluate(grid)
        mean = integrate.simpson(grid * pdf, grid)
        if flag == 'mean':
            return float(mean)
        else:
            var = integrate.simpson((grid - mean) ** 2 * pdf, grid)
            std = np.sqrt(var)
            return float(std)


df4 = df3.groupby(['Year', 'Season', 'Pair']).aggregate(
    Mean=('Variation', partial(kernel_density_estimation, flag='mean')),
    Std=('Variation', partial(kernel_density_estimation, flag='std')),
)
df4.to_excel('问题5-非固定需求均值和标准差.xlsx', float_format='%.2f')
