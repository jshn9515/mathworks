import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sktime.forecasting.arima import StatsModelsARIMA
from sktime.forecasting.base import ForecastingHorizon

df = pd.read_parquet('attachment/附件2.parquet')

df['Pair'] = df.Deliver + '-' + df.Receiver
df.drop(columns=['Deliver', 'Receiver'], inplace=True)
df = df.pivot_table(index='Date', columns='Pair', values='PCS', aggfunc='sum')
df = df.asfreq('D')

# For demonstration purpose
df1 = df['G-V'].copy()

period = 7
size = len(df1) - period
X = np.zeros((size, period))
y = np.zeros(size, dtype=int)
for i in range(size):
    X[i] = df1.iloc[i : i + period].to_numpy()
    flag = df1.iat[i + period]
    if np.isnan(flag):
        y[i] = -1
    elif flag == 0:
        y[i] = 0
    else:
        y[i] = 1

Mdl1 = DecisionTreeClassifier()
Mdl1.fit(X, y)
score = Mdl1.score(X, y)
print(f'The accuracy of CART is: {score:.4f}')

imp = Mdl1.feature_importances_
imp = imp / np.sum(imp)

plt.rc('font', family='Source Han Serif SC', size=16)
plt.rc('figure', figsize=(15, 8))

plt.figure(1)
h = plt.bar(range(7, 0, -1), imp, width=0.5, edgecolor='black', alpha=0.6)
plt.bar_label(h, fmt='%.2f', padding=2)
plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.97)
plt.savefig('data/问题3-决策树变量重要性.svg')

df1.fillna(0, inplace=True)
time_range = pd.date_range(start='2023-04-28', end='2023-04-29', freq='D')
horizon = ForecastingHorizon(time_range, freq='D')
Mdl2 = StatsModelsARIMA(order=(1, 0, 1), trend='c', missing='raise')
df2 = Mdl2.fit_predict(df1, fh=horizon)
df2 = pd.DataFrame(df2)
df2 = df2.T.round(0)
df2 = pd.concat([df1, df2.T], axis=0)

predict = []
for i in range(len(time_range), 0, -1):
    X = df2.iloc[-i - period : -i].to_numpy()
    X = np.atleast_2d(X)
    y = Mdl1.predict(X.T)
    predict.append(y.item())
predict = np.array(predict, dtype=bool)
print('The classification result is:', predict)
