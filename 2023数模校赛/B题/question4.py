import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import RocCurveDisplay, confusion_matrix

plt.rc('font', family='DengXian', size=14)
plt.rc('axes', unicode_minus=False)

df1 = pd.read_parquet('附件/附件1-训练数据.parquet')
df2 = pd.read_parquet('附件/附件2-测试数据.parquet')

ticks = [8, 9]

tbl1 = df1[np.isin(df1.y, ticks)]
tbl2 = df2[np.isin(df2.y, ticks)]

train = tbl1.drop(columns='y')
label = tbl1.y

Mdl = RandomForestClassifier(
    n_estimators=50, n_jobs=-1, max_features='sqrt', verbose=False
)
Mdl.fit(train, label)

test = tbl2.drop(columns='y')
label = tbl2.y
predict = Mdl.predict(test)
print('Training accuracy: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict, labels=ticks)

fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
ticks = ['坐着转换为站着', '坐着转换为躺着']
sns.heatmap(
    matrix,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    cbar=True,
    xticklabels=ticks,
    yticklabels=ticks,
    ax=ax,
)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

fig = plt.figure(2)
ax = fig.add_subplot(1, 1, 1)
RocCurveDisplay.from_estimator(
    Mdl,
    test,
    label,
    plot_chance_level=True,
    color='darkorange',
    despine=True,
    ax=ax,
)

ticks = [7, 11]

tbl1 = df1[np.isin(df1.y, ticks)]
tbl2 = df2[np.isin(df2.y, ticks)]

train = tbl1.drop(columns='y')
label = tbl1.y

Mdl = RandomForestClassifier(
    n_estimators=50, n_jobs=-1, max_features='sqrt', verbose=False
)
Mdl.fit(train, label)

test = tbl2.drop(columns='y')
label = tbl2.y
predict = Mdl.predict(test)
print('Training accuracy: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict, labels=ticks)

fig = plt.figure(3)
ax = fig.add_subplot(1, 1, 1)
ticks = ['站着转换为坐着', '站着转换为躺着']
sns.heatmap(
    matrix,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    cbar=True,
    xticklabels=ticks,
    yticklabels=ticks,
    ax=ax,
)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

fig = plt.figure(4)
ax = fig.add_subplot(1, 1, 1)
RocCurveDisplay.from_estimator(
    Mdl,
    test,
    label,
    plot_chance_level=True,
    color='darkorange',
    despine=True,
    ax=ax,
)

ticks = [10, 12]

tbl1 = df1[np.isin(df1.y, ticks)]
tbl2 = df2[np.isin(df2.y, ticks)]

train = tbl1.drop(columns='y')
label = tbl1.y

Mdl = RandomForestClassifier(
    n_estimators=50, n_jobs=-1, max_features='sqrt', verbose=False
)
Mdl.fit(train, label)

test = tbl2.drop(columns='y')
label = tbl2.y
predict = Mdl.predict(test)
print('Training accuracy: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict, labels=ticks)

fig = plt.figure(5)
ax = fig.add_subplot(1, 1, 1)
ticks = ['躺着转换为坐着', '躺着转换为站着']
sns.heatmap(
    matrix,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    cbar=True,
    xticklabels=ticks,
    yticklabels=ticks,
    ax=ax,
)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

fig = plt.figure(6)
ax = fig.add_subplot(1, 1, 1)
RocCurveDisplay.from_estimator(
    estimator=Mdl,
    X=test,
    y=label,
    plot_chance_level=True,
    color='darkorange',
    despine=True,
    ax=ax,
)

plt.show()
