import numpy as np
import pandas as pd
import coptpy as cp

df1 = pd.read_excel('附件/附件1.xlsx', sheet_name='乡村的现有耕地', index_col=0, usecols='A:C')
df1 = pd.concat([df1, df1.loc['D1':'F4']], axis=0)
df2 = pd.read_excel('附件/附件-农作物汇总表.xlsx', sheet_name='销售单价', index_col=0)
df2.fillna(0, inplace=True)
df3 = pd.read_excel('附件/附件-农作物汇总表.xlsx', sheet_name='种植成本', index_col=0)
df3.fillna(0, inplace=True)
df4 = pd.read_excel('附件/附件-农作物汇总表.xlsx', sheet_name='亩产量', index_col=[0, 1])
df4.fillna(0, inplace=True)
df5 = pd.read_excel('附件/附件-农作物汇总表.xlsx', sheet_name='种植面积', index_col=[0, 1])
df5.fillna(0, inplace=True)

# 2023年农作物总产量
max_crop = df4 * df5
max_crop_season1 = max_crop.loc['第一季'].sum(axis=0).to_numpy()
max_crop_season2 = max_crop.loc['第二季'].sum(axis=0).to_numpy()

lands = 82
crops = 41
years = 7
seasons = 2

env = cp.Envr()
model = env.createModel('crop')
# 农作物种植面积
x = model.addMVar((lands, crops, years), nameprefix='x')
# 农作物产量（与2023年相比较小值）
y = model.addMVar((seasons, crops, years), nameprefix='y')
# 农作物产量（原始产量）
z = model.addMVar((seasons, crops, years), nameprefix='z')
# 水浇地是否为单季种植
b = model.addMVar(8, vtype=cp.COPT.BINARY, nameprefix='b')

# 旱地不能种植某些作物
model.addConstrs(x[:26, 15:, :] == 0, nameprefix='C1')
# 普通大棚+智慧大棚：第一季
model.addConstrs(x[34: 54, :15, :] == 0, nameprefix='C2')
model.addConstrs(x[34: 54, 34:, :] == 0, nameprefix='C3')
# 普通大棚：第二季
model.addConstrs(x[62: 78, :37, :] == 0, nameprefix='C4')
# 智慧大棚：第二季
model.addConstrs(x[78:, :15, :] == 0, nameprefix='C5')
model.addConstrs(x[78:, 34:, :] == 0, nameprefix='C6')
# 土地种植面积限制
block_areas = df1['地块面积/亩'].to_numpy().reshape(-1, 1).repeat(7, axis=1)
model.addConstrs(x.sum(axis=1) <= block_areas, nameprefix='R1')

for k in range(years):
    for i in range(b.size):
        # 水浇地单季种植：只能种植水稻
        for t in x[26 + i, :15, k].tolist():
            model.addGenConstrIndicator(b[i].item(), True, t == 0, name='B1')
        for t in x[26 + i, 16:, k].tolist():
            model.addGenConstrIndicator(b[i].item(), True, t == 0, name='B2')
        # 水浇地双季种植：第一季
        for t in x[26 + i, :15, k].tolist():
            model.addGenConstrIndicator(b[i].item(), False, t == 0, name='B3')
        for t in x[26 + i, 34:, k].tolist():
            model.addGenConstrIndicator(b[i].item(), False, t == 0, name='B4')
        # 水浇地双季种植：第二季
        for t in x[54 + i, :33, k].tolist():
            model.addGenConstrIndicator(b[i].item(), False, t == 0, name='B5')
        for t in x[54 + i, 37:, k].tolist():
            model.addGenConstrIndicator(b[i].item(), False, t == 0, name='B6')

# 不能重茬种植
# 注意：此条件存在适当放宽，认为所有地块连续1年内不能种植相同作物
for k in range(years - 1):
    for i in range(lands):
        for j in range(crops):
            model.addSOS(cp.COPT.SOS_TYPE1, x[i, j, k: k + 2].tolist())

# 3年内必须种植豆类植物
# 假设3年内豆类植物种植面积大于等于地块面积即为满足该条件
beans1 = slice(0, 5)
beans2 = slice(16, 19)
beans3 = [16, 17, 18]
areas = df1['地块面积/亩'].to_numpy()
for k in range(years - 3):
    # 平旱地梯田山坡地：单季种植
    model.addConstrs((x[i, beans1, k: k + 3].sum().item() >= areas[i] for i in range(26)), nameprefix='R2')
    # 普通大棚：第一季
    model.addConstrs((x[i, beans2, k: k + 3].sum().item() >= areas[i] for i in range(26, 50)), nameprefix='R3')
    # 智慧大棚：第一季 + 第二季
    idx1 = np.ix_(range(50, 54), beans3, range(k, k + 3))
    idx2 = np.ix_(range(78, 82), beans3, range(k, k + 3))
    total = x[idx1] + x[idx2]  # type: ignore
    model.addConstrs((total[i].sum().item() >= areas[-4 + i] for i in range(4)), nameprefix='R4')

for k in range(years):
    for j in range(crops):
        # 第一季：总产量取较小值
        model.addConstrs(z[0, j, k] == (x[:54, j, k] * df4.values[:54, j]).sum(), nameprefix='T1')
        model.addGenConstrMin(y[0, j, k].item(), [z[0, j, k].item()], constant=max_crop_season1[j], name='MIN1')
        # 第二季：总产量取较小值
        model.addConstrs(z[1, j, k] == (x[54:, j, k] * df4.values[54:, j]).sum(), nameprefix='T2')
        model.addGenConstrMin(y[1, j, k].item(), [z[1, j, k].item()], constant=max_crop_season2[j], name='MIN2')

profit = cp.MLinExpr.zeros(crops)
for k in range(years):
    # 第一季利润
    profit += y[0, :, k] * df2.loc['第一季'].to_numpy()
    # 第二季利润
    profit += y[1, :, k] * df2.loc['第二季'].to_numpy()
    # 第一季成本
    profit -= (x[:54, :, k] * df3.loc['第一季'].to_numpy()).sum(axis=0)
    # 第二季成本
    profit -= (x[54:, :, k] * df3.loc['第二季'].to_numpy()).sum(axis=0)

model.setObjective(profit.sum(), sense=cp.COPT.MAXIMIZE)
model.setParam('RelGap', 1e-6)
model.setParam('Presolve', 1)
model.setParam('HeurLevel', 3)

model.solve()
assert model.Status == cp.COPT.OPTIMAL
print(f'The profit is: {model.ObjVal:.4f}')
