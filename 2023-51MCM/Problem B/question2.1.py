import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.graphics.gofplots as gofplots
import statsmodels.graphics.tsaplots as tsaplots
import statsmodels.tsa.api as tsa
from statsmodels.nonparametric.kde import KDEUnivariate
from statsmodels.tools.sm_exceptions import InterpolationWarning

df1 = pd.read_parquet('attachment/附件1.parquet')

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

# For demonstration purpose
df1 = df1['G-V'].copy()

# It seems like the time series doesn't have a trend.
plt.rc('font', family='Source Han Serif SC', size=16)
plt.rc('axes', unicode_minus=False)
plt.rc('figure', figsize=(15, 8))

plt.figure(1)
plt.plot(df1, linewidth=1.5)
plt.ylabel('快递运输量（件）')
plt.subplots_adjust(left=0.08, bottom=0.05, right=0.95, top=0.95)
plt.savefig('data/问题2-G-V城市对快递运输量图.svg')

x = np.fft.rfftfreq(len(df1))
y = np.fft.rfft(df1, norm='forward')
y = np.abs(y)
plt.figure(2)
plt.plot(x, y, linewidth=1.5)
plt.ylabel('Magnitude of FFT')
plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95)
plt.savefig('data/问题5-G-V城市对快递运输量FFT图.svg')

# Null hypothesis: The time series is non-stationary.
# Alternative hypothesis: The time series is stationary.
res1 = tsa.adfuller(df1, regression='c')
# Null hypothesis: The time series is level or trend stationary.
# Alternative hypothesis: The time series is non-stationary.
warnings.simplefilter('ignore', InterpolationWarning)
res2 = tsa.kpss(df1, regression='c')

# Both tests indicate that the time series is stationary.
print('ADF Test Statistic:', round(res1[0], 4))
print('ADF p-value:', round(res1[1], 4))
print('KPSS Test Statistic:', round(res2[0], 4))
print('KPSS p-value:', round(res2[1], 4))

# The ACF tails off, while the PACF cuts off
fig = plt.figure(3)
ax = fig.add_subplot(2, 1, 1)
tsaplots.plot_acf(df1, clip_on=False, ax=ax)
ax = fig.add_subplot(2, 1, 2)
tsaplots.plot_pacf(df1, clip_on=False, ax=ax)
fig.subplots_adjust(left=0.1, bottom=0.05, right=0.9, top=0.95, hspace=0.25)
fig.savefig('data/问题2-ACF与PACF图.svg')

Mdl = tsa.ARIMA(df1, order=(0, 0, 4), trend='c', missing='raise')
Mdl = Mdl.fit(method='statespace')
with open('data/问题2-ARIMA模型结果.html', 'w', encoding='utf-8') as fp:
    summary = Mdl.summary()
    fp.write(summary.as_html())
    print(summary)

plt.rc('font', family='Source Han Serif SC', size=14)

fig = plt.figure(4)
ax = fig.add_subplot(2, 2, 1)
ax.plot(Mdl.resid, linewidth=1.2, alpha=0.9)
ax.axhline(0, color='tab:blue', linewidth=1, alpha=0.5)
ax.set_title('Standardized Residuals for "G-V"')
ax = fig.add_subplot(2, 2, 2)
resid = (Mdl.resid - Mdl.resid.mean()) / Mdl.resid.std()
ax.hist(
    resid,
    bins=10,
    density=True,
    linewidth=1.5,
    color='cornflowerblue',
    edgecolor='white',
    alpha=0.6,
)
kde = KDEUnivariate(resid)
kde.fit(gridsize=1000)
ax.plot(kde.support, kde.density, color='orange', linewidth=1.5)
x = np.linspace(resid.min(), resid.max(), num=1000)
y = stats.norm.pdf(x)
ax.plot(x, y, color='forestgreen', linewidth=1.5)
ax.legend(['Hist', 'KDE', 'N(0,1)'])
ax.set_title('Histogram + Estimated Density')
ax = fig.add_subplot(2, 2, 3)
gofplots.qqplot(Mdl.resid, line='s', fit=True, marker='+', ax=ax)
ax.set_title('Normal Q-Q Plot')
ax = fig.add_subplot(2, 2, 4)
tsaplots.plot_acf(Mdl.resid, lags=10, clip_on=False, ax=ax)
ax.set_title('Correlogram')
fig.subplots_adjust(left=0.1, bottom=0.08, right=0.9, top=0.95, hspace=0.2)
fig.savefig('data/问题2-ARIMA模型诊断图.svg')

forecast = Mdl.forecast(steps=2)
df2 = pd.concat([df1, forecast], axis=0)

plt.rc('font', family='Source Han Serif SC', size=16)
plt.figure(5)
plt.plot(df2[: len(df1)], color='tab:blue', linewidth=1.2)
plt.plot(
    df2[len(df1) - 1 :],
    color='tab:orange',
    marker='o',
    markersize=5,
    linestyle='dashdot',
    linewidth=1.2,
)
for i in range(len(df1) - 1, len(df2)):
    plt.text(df2.index[i], df2.iloc[i], f'{df2.iloc[i]:.0f}')  # type: ignore
plt.ylabel('快递运输量（件）')
plt.legend(['Observed', 'Forecast'], title='G-V货运量', loc='upper left')
plt.subplots_adjust(left=0.08, bottom=0.05, right=0.95, top=0.95)
plt.savefig('data/问题2-ARIMA模型预测图.svg')
