import gurobipy as gp
import networkx as nx
import pandas as pd

df1 = pd.read_parquet('attachment/附件3.parquet')

G: nx.DiGraph = nx.from_pandas_edgelist(
    df1,
    source='Start',
    target='End',
    edge_attr='Cost',
    create_using=nx.DiGraph,
)

num_paths = 5
start = 'G'
end = 'V'
cargo = 75

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
    model.addConstr(temp[k] == 1 + (q[k] / 200) ** 3)

cost = gp.quicksum(
    G.edges[i, j]['Cost'] * temp[k] * f[i, j, k]
    for i, j in G.edges
    for k in range(num_paths)
)
model.setObjective(cost, sense=gp.GRB.MINIMIZE)

model.optimize()

if model.Status == gp.GRB.OPTIMAL:
    path = 0
    for k in range(num_paths):
        if y[k].X > 0.5:
            path += 1
            print(f'Path {path}:')
            route = {}
            for i, j in G.edges:
                if f[i, j, k].X > 0.5:
                    route[i] = j
            i, j = start, route[start]
            while j != end:
                print(f'  {i} -> {j}')
                i, j = j, route[j]
            print(f'  {i} -> {j}')
            print(f'  Cargo: {q[k].X:.0f}, Cost: {model.ObjVal:.4f}')
