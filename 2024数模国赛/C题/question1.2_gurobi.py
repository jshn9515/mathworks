import os
import numpy as np
import pandas as pd
import gurobipy as gp

df1 = pd.read_excel('附件/附件1.xlsx', sheet_name='乡村的现有耕地', index_col=0, usecols='A:C')
df1 = pd.concat([df1, df1.loc['D1':'F4']], axis=0)
df2 = pd.read_excel('问题1-农作物汇总表.xlsx', sheet_name='销售单价', index_col=0)
df2.fillna(0, inplace=True)
df3 = pd.read_excel('问题1-农作物汇总表.xlsx', sheet_name='种植成本', index_col=0)
df3.fillna(0, inplace=True)
df4 = pd.read_excel('问题1-农作物汇总表.xlsx', sheet_name='亩产量', index_col=[0, 1])
df4.fillna(0, inplace=True)
df5 = pd.read_excel('问题1-农作物汇总表.xlsx', sheet_name='种植面积', index_col=[0, 1])
df5.fillna(0, inplace=True)

# 2023年农作物总产量
max_crop = df4 * df5
max_crop_season1 = max_crop.loc['第一季'].sum(axis=0).to_numpy()
max_crop_season2 = max_crop.loc['第二季'].sum(axis=0).to_numpy()

lands = 82
crops = 41
years = 7
seasons = 2

model = gp.Model('crop')
# 农作物种植面积
x = model.addMVar((lands, crops, years), name='x')
# 农作物产量（与2023年相比较小值）
y_min = model.addMVar((seasons, crops, years), name='y_min')
# 农作物产量（与2023年相比较大值）
y_max = model.addMVar((seasons, crops, years), name='y_max')
# 农作物产量（原始产量）
z = model.addMVar((seasons, crops, years), name='z')
# 水浇地是否为单季种植
b = model.addMVar(8, vtype=gp.GRB.BINARY, name='b')

# 旱地不能种植某些作物
model.addConstr(x[:26, 15:, :] == 0, name='C1')

for k in range(years):
    for i in range(b.size):
        # 水浇地单季种植：只能种植水稻
        model.addGenConstrIndicator(b[i], True, x[26 + i, :15, k] == 0, name='B1')
        model.addGenConstrIndicator(b[i], True, x[26 + i, 16:, k] == 0, name='B2')
        # 水浇地双季种植：第一季
        model.addGenConstrIndicator(b[i], False, x[26 + i, :15, k] == 0, name='B3')
        model.addGenConstrIndicator(b[i], False, x[26 + i, 34:, k] == 0, name='B4')
        # 水浇地双季种植：第二季
        model.addGenConstrIndicator(b[i], False, x[54 + i, :33, k] == 0, name='B5')
        model.addGenConstrIndicator(b[i], False, x[54 + i, 37:, k] == 0, name='B6')
    # 普通大棚+智慧大棚：第一季
    model.addConstr(x[34: 54, :15, k] == 0, name='C2')
    model.addConstr(x[34: 54, 34:, k] == 0, name='C3')
    # 普通大棚：第二季
    model.addConstr(x[62: 78, :37, k] == 0, name='C4')
    # 智慧大棚：第二季
    model.addConstr(x[78:, :15, k] == 0, name='C5')
    model.addConstr(x[78:, 34:, k] == 0, name='C6')
    # 土地种植面积限制
    model.addConstr(x[:, :, k].sum(axis=1) <= df1['地块面积/亩'].to_numpy(), name='R1')

# 不能重茬种植
# 注意：此条件存在适当放宽，认为所有地块连续1年内不能种植相同作物
for k in range(years - 1):
    for i in range(lands):
        for j in range(crops):
            model.addSOS(gp.GRB.SOS_TYPE1, x[i, j, k: k + 2].tolist())

# 3年内必须种植豆类植物
# 假设3年内豆类植物种植面积大于等于地块面积即为满足该条件
beans1 = [0, 1, 2, 3, 4]
beans2 = [16, 17, 18]
areas = df1['地块面积/亩'].to_numpy()
for k in range(years - 3):
    # 平旱地梯田山坡地：单季种植
    model.addConstrs((x[i, beans1, k: k + 3].sum() >= areas[i] for i in range(26)), name='R2')
    # 普通大棚：第一季
    model.addConstrs((x[i, beans2, k: k + 3].sum() >= areas[i] for i in range(26, 50)), name='R3')
    # 智慧大棚：第一季 + 第二季
    idx1 = np.ix_(range(50, 54), beans2, range(k, k + 3))
    idx2 = np.ix_(range(78, 82), beans2, range(k, k + 3))
    total = x[idx1] + x[idx2]  # type: ignore
    model.addConstrs((total[i].sum() >= areas[-4 + i] for i in range(total.shape[0])), name='R4')

for k in range(years):
    for j in range(crops):
        # 第一季：总产量
        model.addConstr(z[0, j, k] == (x[:54, j, k] * df4.iloc[:54, j].to_numpy()).sum(), name='T1')
        # 第一季：总产量取较小值
        model.addGenConstrMin(y_min[0, j, k].item(), [z[0, j, k].item()], constant=max_crop_season1[j], name='MIN1')
        # 第一季：总产量取较大值
        model.addGenConstrMax(y_max[0, j, k].item(), [z[0, j, k].item()], constant=max_crop_season1[j], name='MAX1')
        # 第二季：总产量
        model.addConstr(z[1, j, k] == (x[54:, j, k] * df4.iloc[54:, j].to_numpy()).sum(), name='T2')
        # 第二季：总产量取较小值
        model.addGenConstrMin(y_min[1, j, k].item(), [z[1, j, k].item()], constant=max_crop_season2[j], name='MIN2')
        # 第二季：总产量取较大值
        model.addGenConstrMax(y_max[1, j, k].item(), [z[1, j, k].item()], constant=max_crop_season2[j], name='MAX2')

profit = gp.MLinExpr.zeros(crops)
for k in range(years):
    # 第一季利润
    profit += y_min[0, :, k] * df2.loc['第一季'].to_numpy()
    profit += (y_max[0, :, k] - y_min[0, :, k]) * 0.5 * df2.loc['第一季'].to_numpy()
    # 第二季利润
    profit += y_min[1, :, k] * df2.loc['第二季'].to_numpy()
    profit += (y_max[1, :, k] - y_min[1, :, k]) * 0.5 * df2.loc['第二季'].to_numpy()
    # 第一季成本
    profit -= (x[:54, :, k] * df3.loc['第一季'].to_numpy()).sum(axis=0)
    # 第二季成本
    profit -= (x[54:, :, k] * df3.loc['第二季'].to_numpy()).sum(axis=0)

model.setObjective(profit.sum(), sense=gp.GRB.MAXIMIZE)
model.setParam('MIPGap', 1e-6)
model.setParam('IgnoreNames', 1)
model.write('question1.2.mps')

if os.path.exists('question1.2.sol'):
    model.read('question1.2.sol')

model.optimize()
assert model.Status == gp.GRB.OPTIMAL
print(f'The profit is: {model.ObjVal:.4f}')
model.setParam('IgnoreNames', 0)
model.write('question1.2.json')

with pd.ExcelWriter('问题1.2-结果.xlsx') as writer:
    for k in range(years):
        file = pd.DataFrame(x[:, :, k].X, index=df5.index, columns=df5.columns)
        file.to_excel(writer, sheet_name=f'{2024 + k}', float_format='%.4f')
