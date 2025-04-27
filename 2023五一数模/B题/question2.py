from typing import cast

import pandas as pd
from sktime.forecasting.arima import StatsModelsARIMA
from sktime.forecasting.base import ForecastingHorizon

df = pd.read_parquet('附件/附件1(Attachment 1)2023-51MCM-Problem B.parquet')

df['Pair'] = df.Deliver + '-' + df.Receiver
df.drop(columns=['Deliver', 'Receiver'], inplace=True)
df = df.pivot_table(
    index='Date',
    columns='Pair',
    values='PCS',
    aggfunc='sum',
    fill_value=0,
)
df = df.asfreq('D', fill_value=0)

time_range = pd.date_range(start='2019-04-18', end='2019-04-19', freq='D')
horizon = ForecastingHorizon(time_range, freq='D')
Mdl = StatsModelsARIMA(order=(1, 0, 1), trend='ct', missing='raise')
df = Mdl.fit_predict(df, fh=horizon)
df = pd.DataFrame(df)
df.index = cast(pd.DatetimeIndex, df.index)
df.index = df.index.strftime('%Y-%m-%d')
df[df < 42] = 0
df = df.T.round(0)
df.loc['Total'] = df.sum()
df.index.name = 'Pair'
df.to_excel('问题2-发货-收货站点城市间快递运输量.xlsx')
