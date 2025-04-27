import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

try:
    import matlab.engine as engine
except ImportError:
    use_matlab = False
    from sklearn.cluster import KMeans
else:
    use_matlab = True
    eng = engine.start_matlab()
    assert isinstance(eng, engine.MatlabEngine)

df = pd.read_parquet('附件/secondary_data.parquet')
df = df[df['class'] == 'p']
df.drop(columns='class', inplace=True)
columns = df.select_dtypes(include='object').columns

encoder = LabelEncoder()
for col in columns:
    df[col] = encoder.fit_transform(df[col])

if use_matlab:
    X = eng.double(df.to_numpy())
    T = eng.kmedoids(X, 4)
else:
    Mdl = KMeans(n_clusters=4)
    T = Mdl.fit_predict(df)

T = np.asarray(T).flatten()
df.insert(0, 'label', T)
df.index = pd.Index(range(1, len(df) + 1))
df.to_excel('问题5-毒蘑菇聚类结果.xlsx', index_label='id')
