import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

df = pd.read_parquet('附件/secondary_data.parquet')
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
imp = Mdl2.feature_importances_
print(f'The score of DecisionTreeClassifier is {score:.4f}, time: {t2 - t1:.4f}s')

sns.set_theme(context='paper', style='darkgrid', font_scale=1.5)
fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
sns.barplot(x=Mdl2.feature_importances_, y=Mdl2.feature_names_in_, ax=ax)
plt.show()
