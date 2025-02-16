import time

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import RocCurveDisplay, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

df: pd.DataFrame = pd.read_pickle('附件/secondary_data.pkl', compression='zip')
columns = df.select_dtypes(include='object').columns

encoder = LabelEncoder()
for col in columns:
    df[col] = encoder.fit_transform(df[col])

X = df.drop(columns='class')
y = df['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

t1 = time.time()
Mdl1 = KNeighborsClassifier()
Mdl1.fit(X_train, y_train)
t2 = time.time()
score = Mdl1.score(X_test, y_test)
print(f'The score of KNeighborsClassifier is {score:.4f}, time: {t2 - t1:.4f}s')

t1 = time.time()
Mdl2 = DecisionTreeClassifier()
Mdl2.fit(X_train, y_train)
t2 = time.time()
score = Mdl2.score(X_test, y_test)
print(f'The score of DecisionTreeClassifier is {score:.4f}, time: {t2 - t1:.4f}s')

plt.rc('font', size=12)
fig = plt.figure(1)
ax = fig.add_subplot(1, 2, 1)
ConfusionMatrixDisplay.from_estimator(Mdl1, X_test, y_test, cmap='Blues', ax=ax)
ax = fig.add_subplot(1, 2, 2)
RocCurveDisplay.from_estimator(Mdl1, X_test, y_test, plot_chance_level=True, despine=True, color='darkorange', ax=ax)

fig = plt.figure(2)
ax = fig.add_subplot(1, 2, 1)
ConfusionMatrixDisplay.from_estimator(Mdl2, X_test, y_test, cmap='Blues', ax=ax)
ax = fig.add_subplot(1, 2, 2)
RocCurveDisplay.from_estimator(Mdl2, X_test, y_test, plot_chance_level=True, despine=True, color='darkorange', ax=ax)
plt.show()
