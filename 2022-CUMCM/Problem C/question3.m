clear; clc;

tbl1 = readtable('attachment/附件-预处理后数据.xlsx', Sheet='表单4', ...
    ReadRowNames=true, TextType='string');
tbl2 = readtable('attachment/附件-预处理后数据.xlsx', Sheet='表单3', ...
    ReadRowNames=true, TextType='string');

numeric = vartype('numeric');
tbl2 = tbl2(:, numeric);
tbl_BaO2 = tbl1(tbl1.Type == '铅钡', numeric);
tbl_KMnO4 = tbl1(tbl1.Type == '高钾', numeric);

tbl_diff = abs(mean(tbl_BaO2) - mean(tbl_KMnO4));
index = string(tbl_diff.Properties.VariableNames);
[~, idx] = sort(tbl_diff.Variables);
rank = 1 : length(idx);
tbl_diff = table(tbl_diff.Variables.', RowNames=index, VariableNames="Diff");
tbl_diff.Rank = rank(idx).';
tbl_diff.Properties.DimensionNames = ["Component", "Variables"];
tbl_diff = sortrows(tbl_diff, 'Rank');

top3 = tbl_diff.Properties.RowNames(1:3);
X = tbl1(:, top3);
y = tbl1.Type;
Mdl1 = fitcsvm(X, y, KernelFunction='linear');
score1 = resubLoss(Mdl1);
predict1 = predict(Mdl1, tbl2(:, top3));
disp("Phrase 1: The accuracy of SVM model is: " + round(1 - score1, 4));

predict1 = string(predict1);
tbl_pred_BaO2 = tbl2(predict1 == '铅钡', :);
tbl_pred_KMnO4 = tbl2(predict1 == '高钾', :);

index = string(tbl_BaO2.Properties.VariableNames);
dim = ["Component", "Variables"];

var_BaO2 = var(tbl_BaO2);
var_BaO2 = array2table(var_BaO2.Variables.', RowNames=index, ...
    VariableNames="Var", DimensionNames=dim);
var_BaO2 = sortrows(var_BaO2, 'Var', 'descend');
var_BaO2 = var_BaO2.Component(1:2);

var_KMnO4 = var(tbl_KMnO4);
var_KMnO4 = array2table(var_KMnO4.Variables.', RowNames=index, ...
    VariableNames="Var", DimensionNames=dim);
var_KMnO4 = sortrows(var_KMnO4, 'Var', 'descend');
var_KMnO4 = var_KMnO4.Component(1:2);

disp("The BaO2 glasses use " + var_BaO2(1) + " and " + var_BaO2(2) + " as classification criteria...");
disp("The KMnO4 glasses use " + var_KMnO4(1) + " and " + var_KMnO4(2) + " as classification criteria...");

tbl_BaO2 = tbl_BaO2(:, var_BaO2);
tbl_KMnO4 = tbl_KMnO4(:, var_KMnO4);

T_BaO2 = clusterdata(tbl_BaO2.Variables, Maxclust=3, Linkage='ward');
T_KMnO4 = clusterdata(tbl_KMnO4.Variables, Maxclust=3, Linkage='ward');

template = templateSVM(KernelFunction='linear');
Mdl21 = fitcecoc(tbl_BaO2, T_BaO2, Learners=template);
score21 = resubLoss(Mdl21);
predict21 = predict(Mdl21, tbl_pred_BaO2(:, var_BaO2));
disp("Phrase 2: The accuray of BaO2 is: " + round(1 - score21, 4));

Mdl22 = fitcecoc(tbl_KMnO4, T_KMnO4, Learners=template);
score22 = resubLoss(Mdl22);
predict22 = predict(Mdl22, tbl_pred_KMnO4(:, var_KMnO4));
disp("Phrase 2: The accuray of KMnO4 is: " + round(1 - score22, 4));

disp("The classification result of BaO2 is: " + sprintf('%d, ', predict21));
disp("The classification result of KMnO4 is: " + sprintf('%d, ', predict22));