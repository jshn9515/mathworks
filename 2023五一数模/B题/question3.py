from typing import cast

import pandas as pd
from sktime.forecasting.arima import StatsModelsARIMA
from sktime.forecasting.base import ForecastingHorizon

df1 = pd.read_parquet('附件/附件2(Attachment 2)2023-51MCM-Problem B.parquet')

df1['Pair'] = df1.Deliver + '-' + df1.Receiver
df1.drop(columns=['Deliver', 'Receiver'], inplace=True)
df1 = df1.pivot_table(
    index='Date',
    columns='Pair',
    values='PCS',
    aggfunc='sum',
    fill_value=0,
)
df1 = df1.asfreq('D', fill_value=0)

time_range = pd.date_range(start='2023-04-28', end='2023-04-29', freq='D')
horizon = ForecastingHorizon(time_range, freq='D')
Mdl = StatsModelsARIMA(order=(1, 0, 1), trend='ct', missing='raise')
df1 = Mdl.fit_predict(df1, fh=horizon)
df1 = pd.DataFrame(df1)
df1.index = cast(pd.DatetimeIndex, df1.index)
df1.index = df1.index.strftime('%Y-%m-%d')
df1[df1 < 42] = 0
df1 = df1.T.round(0)
index = pd.MultiIndex.from_product([time_range.strftime('%Y-%m-%d'), df1.index])
df2 = pd.DataFrame(index=index, columns=['Indicator', 'Cargo'])
df2.loc['2023-04-28', 'Cargo'] = df1['2023-04-28'].to_numpy()
df2.loc['2023-04-28', 'Indicator'] = (df1['2023-04-28'] > 0).to_numpy()
df2.loc['2023-04-29', 'Cargo'] = df1['2023-04-29'].to_numpy()
df2.loc['2023-04-29', 'Indicator'] = (df1['2023-04-29'] > 0).to_numpy()
df2.rename_axis(['Date', 'Pair'], inplace=True)
df2.to_excel('问题3-发货-收货站点城市间快递运输量.xlsx')
