import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL
from xgboost.sklearn import XGBRegressor

df = pd.read_parquet('attachment/附件2.parquet')

df['Year'] = df.index.year  # type: ignore
df['Season'] = df.index.month // 3 + 1  # type: ignore

df.insert(
    loc=0,
    column='Pair',
    value=df.Deliver + '-' + df.Receiver,
)
df.drop(columns=['Deliver', 'Receiver'], inplace=True)
df.set_index(['Year', 'Season', 'Pair'], inplace=True)
df.columns = ['PCS']


def apply_decomp(series: pd.Series) -> float:
    assert series.ndim == 1
    result = STL(series, period=16).fit()
    result = np.mean(result.trend)
    return result.item()


grouped = df.groupby(['Year', 'Season', 'Pair'])
df1 = grouped.aggregate(apply_decomp)
df2 = grouped.sum()
df1.columns = ['Constant']
df2.columns = ['PCS']
df1.sort_index(inplace=True)
df1.to_excel('data/问题5-固定需求常数.xlsx', float_format='%.0f')

X = df2.to_numpy().reshape(-1, 1)
y = df1.to_numpy()
assert X.size == y.size

Mdl = XGBRegressor()
Mdl.fit(X, y)
score = Mdl.score(X, y)
print(f'R2 score of this model is: {score:.4f}')
