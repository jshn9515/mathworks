import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.multiclass import OutputCodeClassifier
from sklearn.tree import DecisionTreeClassifier

plt.rc('font', family='DengXian', size=14)
plt.rc('axes', unicode_minus=False)

df1 = pd.read_parquet('附件/附件1-训练数据.parquet')
df2 = pd.read_parquet('附件/附件2-测试数据.parquet')

var = np.loadtxt('问题5-筛选变量名称.txt', dtype=str)
var = np.append(var, 'y')
df1 = df1[var]
df2 = df2[var]

train = df1.drop(columns='y')
label = df1.y

t1 = time.time()
Mdl = OutputCodeClassifier(DecisionTreeClassifier(), n_jobs=-1)
Mdl.fit(train, label)
t2 = time.time()
print(f'Training time: {t2 - t1:.2f}s')

test = df2.drop(columns='y')
label = df2.y
predict = Mdl.predict(test)
print('R2 score: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict)

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

plt.show()
