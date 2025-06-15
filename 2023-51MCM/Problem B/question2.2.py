import pandas as pd
from sktime.forecasting.arima import StatsModelsARIMA
from sktime.forecasting.base import ForecastingHorizon

df = pd.read_parquet('attachment/附件1.parquet')

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

# TODO: Consider entire graph, not just a single route
time_range = pd.date_range(start='2019-04-18', end='2019-04-19', freq='D')
horizon = ForecastingHorizon(time_range, freq='D')
# You can estimate the order of the ARIMA model using ACF and PACF plots,
# or use a method like auto_arima to find the best parameters.
# Here, we assume an ARIMA(1, 0, 1) model with a constant trend.
# Adjust the order as necessary based on your data.
Mdl = StatsModelsARIMA(order=(1, 0, 1), trend='c', missing='raise')
df = Mdl.fit_predict(df, fh=horizon)
df = pd.DataFrame(df)
df.index = df.index.strftime('%Y-%m-%d')  # type: ignore

# According to data, set values below 42 to 0.
df[df < 42] = 0
df = df.T.round(0)
df.loc['Total'] = df.sum()
df.index.name = 'Pair'
df.to_excel('data/问题2-发货-收货站点城市间快递运输量.xlsx')
