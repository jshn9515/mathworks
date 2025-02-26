import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.multiclass import OutputCodeClassifier
from sklearn.svm import SVC

plt.rc('font', family='DengXian', size=14)
plt.rc('axes', unicode_minus=False)

df1: pd.DataFrame = pd.read_pickle('附件/附件1-训练数据.pkl', compression='zip')
df2: pd.DataFrame = pd.read_pickle('附件/附件2-测试数据.pkl', compression='zip')

var = np.loadtxt('问题1-筛选变量名称.txt', dtype=str)
var = np.append(var, 'y')
df1 = df1[var]
df2 = df2[var]

tbl1 = df1[(1 <= df1.y) & (df1.y <= 6)]
tbl2 = df2[(1 <= df2.y) & (df2.y <= 6)]

train = tbl1.drop(columns='y')
label = (1 <= tbl1.y) & (tbl1.y <= 3)

Mdl = SVC(C=1, kernel='linear', verbose=False)
Mdl.fit(train, label)

test = tbl2.drop(columns='y')
label = (1 <= tbl2.y) & (tbl2.y <= 3)

predict = Mdl.predict(test)
print('Training accuracy: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict, labels=[0, 1])

fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
sns.heatmap(
    matrix,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    xticklabels=['静态', '动态'],
    yticklabels=['静态', '动态'],
    cbar=True,
    ax=ax,
)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

tbl1 = df1[(1 <= df1.y) & (df1.y <= 3)]
tbl2 = df2[(1 <= df2.y) & (df2.y <= 3)]

train = tbl1.drop(columns='y')
label = tbl1.y

Mdl = OutputCodeClassifier(SVC(C=1, kernel='linear', verbose=False), n_jobs=-1)
Mdl.fit(train, label)

test = tbl2.drop(columns='y')
label = tbl2.y

predict = Mdl.predict(test)
print('Training accuracy: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict, labels=[1, 2, 3])

fig = plt.figure(2)
ax = fig.add_subplot(1, 1, 1)
sns.heatmap(
    matrix,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    xticklabels=['步行', '上楼', '下楼'],
    yticklabels=['步行', '上楼', '下楼'],
    cbar=True,
    ax=ax,
)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

tbl1 = df1[(4 <= df1.y) & (df1.y <= 6)]
tbl2 = df2[(4 <= df2.y) & (df2.y <= 6)]

train = tbl1.drop(columns='y')
label = tbl1.y

Mdl = OutputCodeClassifier(SVC(C=1, kernel='linear', verbose=False), n_jobs=-1)
Mdl.fit(train, label)

test = tbl2.drop(columns='y')
label = tbl2.y

predict = Mdl.predict(test)
print('Training accuracy: %.4f' % Mdl.score(test, label))
matrix = confusion_matrix(label, predict, labels=[4, 5, 6])

fig = plt.figure(3)
ax = fig.add_subplot(1, 1, 1)
sns.heatmap(
    matrix,
    annot=True,
    fmt='d',
    cmap='coolwarm',
    linewidths=0.5,
    linecolor='gray',
    xticklabels=['坐着', '站着', '躺着'],
    yticklabels=['坐着', '站着', '躺着'],
    cbar=True,
    ax=ax,
)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

plt.show()
