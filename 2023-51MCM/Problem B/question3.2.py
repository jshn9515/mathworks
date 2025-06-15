import pandas as pd
from sktime.forecasting.arima import StatsModelsARIMA
from sktime.forecasting.base import ForecastingHorizon

df1 = pd.read_parquet('attachment/附件2.parquet')

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

# NOTE: For simplicity, we ignore the steps of classification.
# That is, if the cargo is less than 42, we set it to 0,
# and mark it as False in the indicator.
# In this case, we don't distinguish "No demand" and "Can't deliver".
time_range = pd.date_range(start='2023-04-28', end='2023-04-29', freq='D')
horizon = ForecastingHorizon(time_range, freq='D')
Mdl = StatsModelsARIMA(order=(1, 0, 1), trend='c', missing='raise')
df1 = Mdl.fit_predict(df1, fh=horizon)
df1 = pd.DataFrame(df1)
df1.index = df1.index.strftime('%Y-%m-%d')  # type: ignore
df1[df1 < 42] = 0
df1 = df1.T.round(0)

time_range = time_range.strftime('%Y-%m-%d')
index = pd.MultiIndex.from_product([time_range.to_list(), df1.index.to_list()])
df2 = pd.DataFrame(index=index, columns=['Indicator', 'Cargo'])
df2.loc['2023-04-28', 'Indicator'] = df1['2023-04-28'] > 0
df2.loc['2023-04-28', 'Cargo'] = df1['2023-04-28']
df2.loc['2023-04-29', 'Indicator'] = df1['2023-04-29'] > 0
df2.loc['2023-04-29', 'Cargo'] = df1['2023-04-29']
df2.rename_axis(['Date', 'Pair'], inplace=True)
df2.to_excel('data/问题3-发货-收货站点城市间快递运输量.xlsx')
