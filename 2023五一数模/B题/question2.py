from typing import cast

import pandas as pd
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.arima import StatsModelsARIMA

df = pd.read_excel('附件/附件1(Attachment 1)2023-51MCM-Problem B.xlsx', parse_dates=True)

df['发货-收货城市对'] = df['发货城市 (Delivering city)'] + '-' + df['收货城市 (Receiving city)']
df.drop(columns=['发货城市 (Delivering city)', '收货城市 (Receiving city)'], inplace=True)
df = df.pivot_table(
    index='日期(年/月/日) (Date Y/M/D)',
    columns='发货-收货城市对',
    values='快递运输数量(件) (Express delivery quantity (PCS))',
    aggfunc='sum',
    fill_value=0
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
df.loc['合计运输量'] = df.sum()
df.rename_axis('发货-收货城市对', inplace=True)
df.to_excel('问题2-发货-收货站点城市间快递运输量.xlsx')
