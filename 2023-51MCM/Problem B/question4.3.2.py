from collections import defaultdict

import gurobipy as gp
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import tqdm

df1 = pd.read_parquet('attachment/附件2.parquet')
df2 = pd.read_parquet('attachment/附件3.parquet')

num_paths = 5
time_range = pd.date_range('2023-04-23', '2023-04-27', freq='D')
time_range = time_range.strftime('%Y-%m-%d')
sensitivity = list(range(195, 210, 5))
columns = ['Cargo-' + str(i) for i in sensitivity]

G: nx.DiGraph = nx.from_pandas_edgelist(
    df2,
    source='Start',
    target='End',
    edge_attr='Cost',
    create_using=nx.DiGraph,
)

df = pd.DataFrame(index=time_range, columns=columns)
df.index.name = 'Date'

gp.setParam('OutputFlag', 0)  # Suppress Gurobi output

for base in tqdm.tqdm(sensitivity, desc='Processing sensitivity', unit='it'):
    single = defaultdict(dict)

    for time in time_range:
        for start, end, cargo in df1.loc[time].itertuples(index=False):
            model = gp.Model('Transportation')
            f = model.addVars(G.edges, range(num_paths), vtype=gp.GRB.BINARY, name='f')
            y = model.addVars(num_paths, vtype=gp.GRB.BINARY, name='y')
            q = model.addVars(num_paths, vtype=gp.GRB.INTEGER, name='q')
            temp = model.addVars(num_paths, name='temp')

            model.addConstr(q.sum() == cargo)

            for k in range(num_paths):
                expr = gp.quicksum(f[start, j, k] for j in G.successors(start))
                model.addGenConstrIndicator(y[k], True, expr == 1)
                expr = gp.quicksum(f[i, start, k] for i in G.predecessors(start))
                model.addGenConstrIndicator(y[k], True, expr == 0)

                expr = gp.quicksum(f[i, end, k] for i in G.predecessors(end))
                model.addGenConstrIndicator(y[k], True, expr == 1)
                expr = gp.quicksum(f[end, j, k] for j in G.successors(end))
                model.addGenConstrIndicator(y[k], True, expr == 0)

                for n in G.nodes:
                    if n != start and n != end:
                        expr1 = gp.quicksum(f[n, j, k] for j in G.successors(n))
                        expr2 = gp.quicksum(f[i, n, k] for i in G.predecessors(n))
                        model.addConstr(expr1 == expr2)

                for i, j in G.edges:
                    model.addConstr(f[i, j, k] <= y[k])

                model.addGenConstrIndicator(y[k], False, q[k] == 0)
                model.addConstr(temp[k] == 1 + (q[k] / base) ** 3)

            cost = gp.quicksum(
                G.edges[i, j]['Cost'] * temp[k] * f[i, j, k]
                for i, j in G.edges
                for k in range(num_paths)
            )
            model.setObjective(cost, sense=gp.GRB.MINIMIZE)

            model.optimize()

            if model.Status == gp.GRB.OPTIMAL:
                single[time][f'{start}-{end}'] = model.ObjVal
            else:
                raise RuntimeError(
                    f'No optimal solution found for {start} to {end} on {time}'
                )

    single = pd.DataFrame(single)
    single.fillna(0, inplace=True)
    single.sort_index(inplace=True)
    df[f'Cargo-{base}'] = single.sum()

with pd.ExcelWriter(
    'data/问题4-城市快递运输费用.xlsx',
    engine='openpyxl',
    mode='a',
    if_sheet_exists='replace',
) as writer:
    df.to_excel(writer, sheet_name='精确算法敏感性检验', float_format='%.4f')

plt.rc('font', family='Source Han Serif SC', size=16)
plt.figure(1, figsize=(15, 8))
plt.plot(df, '-o')
plt.ylabel('总运费')
plt.legend(df.columns)
plt.subplots_adjust(left=0.08, bottom=0.05, right=0.95, top=0.95)
plt.savefig('data/问题4-精确算法敏感性检验.svg', dpi=300)
