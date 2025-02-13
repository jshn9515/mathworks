from typing import cast

import pandas as pd
from sktime.forecasting.arima import StatsModelsARIMA
from sktime.forecasting.base import ForecastingHorizon

df1 = pd.read_excel('附件/附件2(Attachment 2)2023-51MCM-Problem B.xlsx', index_col=0)

df1['发货-收货城市对'] = df1['发货城市 (Delivering city)'] + '-' + df1['收货城市 (Receiving city)']
df1.drop(columns=['发货城市 (Delivering city)', '收货城市 (Receiving city)'], inplace=True)
df1 = df1.pivot_table(
    index='日期(年/月/日) (Date Y/M/D)',
    columns='发货-收货城市对',
    values='快递运输数量(件) (Express delivery quantity (PCS))',
    aggfunc='sum',
    fill_value=0
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
df2 = pd.DataFrame(index=index, columns=['是否能正常发货', '发货数量'])
df2.loc['2023-04-28', '发货数量'] = df1['2023-04-28'].to_numpy()
df2.loc['2023-04-28', '是否能正常发货'] = (df1['2023-04-28'] > 0).to_numpy()
df2.loc['2023-04-29', '发货数量'] = df1['2023-04-29'].to_numpy()
df2.loc['2023-04-29', '是否能正常发货'] = (df1['2023-04-29'] > 0).to_numpy()
df2.rename_axis(['日期', '发货-收货城市对'], inplace=True)
df2.to_excel('问题3-发货-收货站点城市间快递运输量.xlsx')
