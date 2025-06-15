%% Question 2.1
clear; clc;

tbl1 = readtable('attachment/附件-预处理后数据.xlsx', Sheet='表单1', ...
    TextType='string', ReadRowNames=true);
tbl2 = readtable('attachment/附件-预处理后数据.xlsx', Sheet='表单4', ...
    TextType='string', ReadRowNames=true);

P1 = crosstab(tbl1.Type, tbl1.Color, OutputFormat='table');
P2 = crosstab(tbl1.Type, tbl1.Style, OutputFormat='table');
P3 = crosstab(tbl1.Type, tbl1.Erode, OutputFormat='table');

Mdl1 = fitctree(tbl1, 'Type');
score1 = resubLoss(Mdl1);
disp("The accuracy of CART is: " + round(1 - score1, 4));
imp = predictorImportance(Mdl1);
imp = imp ./ sum(imp);

fig = figure(1);
x = ["Style", "Color", "Erode"];
h = bar(x, imp, 0.5, EdgeColor='black', LineWidth=1, FaceAlpha=0.6);
set(h, Labels=round(imp, 2), FontSize=12);
set(gca, FontName='Microsoft YaHei', FontSize=12);
exportgraphics(fig, 'data/问题2-决策树重要性比较图.svg', Width=15, Height=8, Units='inches');

numeric = vartype('numeric');
tbl_BaO2 = tbl2(tbl2.Type == '铅钡', numeric);
tbl_KMnO4 = tbl2(tbl2.Type == '高钾', numeric);
tbl_diff = abs(mean(tbl_BaO2) - mean(tbl_KMnO4));

index = string(tbl_diff.Properties.VariableNames);
[~, idx] = sort(tbl_diff.Variables);
rank = 1 : length(idx);
tbl_diff = table(tbl_diff.Variables.', RowNames=index, VariableNames="Diff");
tbl_diff.Rank = rank(idx).';
tbl_diff.Properties.DimensionNames = ["Component", "Variables"];
tbl_diff = sortrows(tbl_diff, 'Rank');

top3 = tbl_diff.Component(1:3);
X = tbl2(:, top3);
y = tbl2.Type;
Mdl2 = fitcsvm(X, y, KernelFunction='linear');
score2 = resubLoss(Mdl2);
disp("The accuracy of SVM is: " + round(1 - score2, 4));

%% Question 2.2
clear; clc;

tbl = readtable('attachment/附件-预处理后数据.xlsx', Sheet='表单4', TextType='string', ReadRowNames=true);

numeric = vartype('numeric');
tbl1 = tbl(tbl.Type == '铅钡', numeric);
tbl2 = tbl(tbl.Type == '高钾', numeric);

index = string(tbl1.Properties.VariableNames);
dim = ["Component", "Variables"];

var1 = var(tbl1);
var1 = array2table(var1.Variables.', RowNames=index, VariableNames="Var", DimensionNames=dim);
var1 = sortrows(var1, 'Var', 'descend');
var1 = var1.Component(1:2);

var2 = var(tbl2);
var2 = array2table(var2.Variables.', RowNames=index, VariableNames="Var", DimensionNames=dim);
var2 = sortrows(var2, 'Var', 'descend');
var2 = var2.Component(1:2);

disp("The BaO2 glasses use " + var1(1) + " and " + var1(2) + " as classification criteria...");
disp("The KMnO4 glasses use " + var2(1) + " and " + var2(2) + " as classification criteria...");

tbl1 = tbl1(:, var1);
tbl2 = tbl2(:, var2);

L1 = linkage(tbl1.Variables, 'ward');
L2 = linkage(tbl2.Variables, 'ward');
T1 = cluster(L1, Maxclust=3);
T2 = cluster(L2, Maxclust=3);

fig = figure(1);
h = dendrogram(L1, 0, Labels=tbl1.Sample, ClusterIndices=T1, ShowCut=true);
set(h, LineWidth=1);
exportgraphics(fig, 'data/问题2-铅钡聚类图.svg', Width=15, Height=8, Units='inches');

fig = figure(2);
h = dendrogram(L2, 0, Labels=tbl2.Sample, ClusterIndices=T2, ShowCut=true);
set(h, LineWidth=1);
exportgraphics(fig, 'data/问题2-高钾聚类图.svg', Width=15, Height=8, Units='inches');

dim = ["文物编号", "Variables"];
tbl4 = table(T1, RowNames=tbl1.Sample, VariableNames="类别", DimensionNames=dim);
tbl5 = table(T2, RowNames=tbl2.Sample, VariableNames="类别", DimensionNames=dim);

writetable(tbl4, 'data/问题2-铅钡高钾聚类数据.xlsx', Sheet='铅钡', ...
    WriteRowNames=true, WriteMode='overwritesheet');
writetable(tbl5, 'data/问题2-铅钡高钾聚类数据.xlsx', Sheet='高钾', ...
    WriteRowNames=true, WriteMode='overwritesheet');

template = templateSVM(KernelFunction='linear');
Mdl1 = fitcecoc(tbl1, T1, Learners=template);
score1 = resubLoss(Mdl1);
disp("The accuracy of BaO2 is: " + round(1 - score1, 4));

fig = figure(3);
for idx = 1 : length(Mdl1.BinaryLearners)
    learner = Mdl1.BinaryLearners{idx};
    fun = @(x1, x2) ([x1; x2].' * learner.Beta + learner.Bias).';
    fimplicit(fun, Color='black', LineStyle='-.', LineWidth=1.2);
    hold on
    x1 = tbl1{:, var1(1)};
    x2 = tbl1{:, var1(2)};
    h = gscatter(x1, x2, T1, [], 'o', 8, 'on', var1(1), var1(2), 'filled');
end
grid on
hold off
lgd = legend(Location='northeast');
title(lgd, 'Classes', FontSize=12);
set(gca, FontName='Microsoft YaHei', FontSize=12);
exportgraphics(fig, 'data/问题2-铅钡SVM分类图.svg', Width=15, Height=8, Units='inches');

Mdl2 = fitcecoc(tbl2, T2, Learners=template);
score2 = resubLoss(Mdl2);
disp("The accuracy of KMnO4 is: " + round(1 - score2, 4));

fig = figure(4);
for idx = 1 : length(Mdl2.BinaryLearners)
    learner = Mdl2.BinaryLearners{idx};
    fun = @(x1, x2) ([x1; x2].' * learner.Beta + learner.Bias).';
    fimplicit(fun, Color='black', LineStyle='-.', LineWidth=1.2);
    hold on
    x1 = tbl2{:, var2(1)};
    x2 = tbl2{:, var2(2)};
    h = gscatter(x1, x2, T2, [], 'o', 8, 'on', var2(1), var2(2), 'filled');
end
grid on
hold off
lgd = legend(Location='northeast');
title(lgd, 'Classes', FontSize=12);
set(gca, FontName='Microsoft YaHei', FontSize=12);
exportgraphics(fig, 'data/问题2-高钾SVM分类图.svg', Width=15, Height=8, Units='inches');