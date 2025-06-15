clear; clc;

tbl = readtable('attachment\附件-预处理后数据.xlsx', Sheet='表单4', ...
    TextType='string', ReadRowNames=true);

numeric = vartype('numeric');
tbl1 = tbl(tbl.Type == '铅钡', numeric);
tbl2 = tbl(tbl.Type == '高钾', numeric);

alpha = 0.05;
result = zeros(3, length(tbl1.Properties.VariableNames));
num = 1;
for col = tbl1.Properties.VariableNames
    [h, p, stat] = kstest2(tbl1{:, col}, tbl2{:, col}, Alpha=alpha);
    result(:, num) = [h, p, stat].';
    num = num + 1;
end
index = ["h", "pvalue", "statistic"];
column = string(tbl1.Properties.VariableNames);
dim = ["Test", "Variables"];
result = array2table(result, RowNames=index, VariableNames=column, DimensionNames=dim);
result = round(result, 4);

writetable(result, 'data/问题4-K-S检验.xlsx', WriteRowNames=true, WriteMode='overwritesheet');

fig = figure(1);
R1 = corrcoef(tbl1.Variables);
heatmap(R1, XDisplayLabels=column, YDisplayLabels=column, CellLabelFormat='%0.2f');
set(gca, FontSize=12);
exportgraphics(fig, 'data/问题4-铅钡相关系数矩阵.svg', Width=15, Height=8, Units='inches');

fig = figure(2);
R2 = corrcoef(tbl2.Variables);
heatmap(R2, XDisplayLabels=column, YDisplayLabels=column, CellLabelFormat='%0.2f');
set(gca, FontSize=12);
exportgraphics(fig, 'data/问题4-高钾相关系数矩阵.svg', Width=15, Height=8, Units='inches');