import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

plt.rc('font', family='DengXian', size=12)
plt.rc('axes', unicode_minus=False)

df1: pd.DataFrame = pd.read_pickle('附件/附件1-训练数据.pkl', compression='zip')
df2: pd.DataFrame = pd.read_pickle('附件/附件2-测试数据.pkl', compression='zip')

train = df1.drop(columns='y')
label = df1.y
var = df1.columns.values

# entire dataset
t1 = time.time()
Mdl = RandomForestClassifier(
    n_estimators=50, n_jobs=-1, max_features='sqrt', verbose=True
)
Mdl.fit(train, label)
t2 = time.time()
print(f'Training time: {t2 - t1:.2f}s')

importance = Mdl.feature_importances_
idx = np.argsort(-importance)
var = var[idx[:10]]
np.savetxt('问题1-筛选变量名称.txt', var, fmt='%s')

test = df2.drop(columns='y')
label = df2.y

predict = Mdl.predict(test)
matrix = confusion_matrix(label, predict)
print('R2 score: %.4f' % Mdl.score(test, label))

fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
ticks = list(map(str, range(1, 13)))
mask = np.bitwise_or(matrix == 0, np.eye(matrix.shape[0], dtype=bool))
sns.heatmap(
    matrix,
    mask=mask,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    xticklabels=ticks,
    yticklabels=ticks,
    cbar=True,
    ax=ax,
)
mask = np.bitwise_not(np.eye(matrix.shape[0], dtype=bool))
sns.heatmap(
    matrix,
    mask=mask,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    xticklabels=ticks,
    yticklabels=ticks,
    cbar=False,
    ax=ax,
)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

# select dataset
var = np.append(var, 'y')
df1 = df1[var]
df2 = df2[var]

train = df1.drop(columns='y')
label = df1.y

t1 = time.time()
Mdl = RandomForestClassifier(
    n_estimators=50, n_jobs=-1, max_features='sqrt', verbose=False
)
Mdl.fit(train, label)
t2 = time.time()
print(f'Training time: {t2 - t1:.2f}s')

test = df2.drop(columns='y')
label = df2.y
predict = Mdl.predict(test)
print('R2 score: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict)

fig = plt.figure(2)
ax = fig.add_subplot(1, 1, 1)
ticks = list(map(str, range(1, 13)))
mask = np.bitwise_or(matrix == 0, np.eye(matrix.shape[0], dtype=bool))
sns.heatmap(
    matrix,
    mask=mask,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    xticklabels=ticks,
    yticklabels=ticks,
    cbar=True,
    ax=ax,
)
mask = np.bitwise_not(np.eye(matrix.shape[0], dtype=bool))
sns.heatmap(
    matrix,
    mask=mask,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    xticklabels=ticks,
    yticklabels=ticks,
    cbar=False,
    ax=ax,
)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

fig = plt.figure(3)
for i in range(len(var) - 1):
    ax = fig.add_subplot(3, 4, i + 1)
    idx = np.zeros(df1.shape[0], dtype=int)
    idx[(1 <= df1.y) & (df1.y <= 3)] = 1
    idx[(4 <= df1.y) & (df1.y <= 6)] = 2
    idx[(7 <= df1.y) & (df1.y <= 12)] = 3
    sns.kdeplot(
        df1,
        x=var[i],
        hue=idx,
        hue_order=[1, 2, 3],
        palette='tab10',
        fill=True,
    )
    ax.set_title(ax.get_xlabel())
    ax.set_xlabel('')
plt.subplots_adjust(wspace=0.3, hspace=0.5)

plt.show()
