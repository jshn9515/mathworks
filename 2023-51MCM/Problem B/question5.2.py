from functools import partial
from typing import Literal

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

df = pd.read_parquet('attachment/附件2.parquet')

df['Year'] = df.index.year  # type: ignore
df['Season'] = df.index.month // 3 + 1  # type: ignore

df.insert(
    loc=0,
    column='Pair',
    value=df.Deliver + '-' + df.Receiver,
)
df.drop(columns=['Deliver', 'Receiver'], inplace=True)
df.set_index(['Year', 'Season', 'Pair'], inplace=True)
df.columns = ['PCS']


def apply_decomp(series: pd.Series[float], flag: Literal['mean', 'std']) -> float:
    data = np.asarray_chkfinite(series)
    assert data.ndim == 1
    Mdl = STL(data, period=16).fit()
    mean = np.mean(Mdl.seasonal)
    std = np.std(Mdl.seasonal, ddof=1 if Mdl.nobs[0] > 1 else 0, mean=mean)
    return mean.item() if flag == 'mean' else std.item()


df = df.groupby(['Year', 'Season', 'Pair']).aggregate(
    Mean=pd.NamedAgg('PCS', partial(apply_decomp, flag='mean')),
    Std=pd.NamedAgg('PCS', partial(apply_decomp, flag='std')),
)
df.to_excel('data/问题5-非固定需求均值和标准差.xlsx', float_format='%.2f')
