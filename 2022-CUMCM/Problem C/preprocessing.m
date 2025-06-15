clear; clc;

opts1 = detectImportOptions('attachment/附件.xlsx', Sheet='表单1', TextType='string', ...
    ReadRowNames=true, VariableNamingRule='preserve');
opts1 = setvartype(opts1, 'categorical');
opts1.VariableNames = ["Style", "Type", "Color", "Erode"];

tbl1 = readtable('attachment/附件.xlsx', opts1);
tbl1.Properties.DimensionNames = ["Sample", "Variables"];
groups = findgroups(tbl1.Style, tbl1.Type, tbl1.Erode);
lookup = groupsummary(tbl1, ["Style", "Type", "Erode"], 'mode');
lookup = renamevars(lookup, 'mode_Color', 'ModeColor');
idx = ismissing(tbl1.Color);
tbl1(idx, 'Color') = lookup(groups(idx), 'ModeColor');

opts2 = detectImportOptions('attachment/附件.xlsx', Sheet='表单2', TextType='string', ...
    ReadRowNames=true, VariableNamingRule='preserve');
opts2.VariableNames = extractBetween(opts2.VariableNames, '(', ')');

tbl2 = readtable('attachment/附件.xlsx', opts2);
tbl2.Properties.DimensionNames = ["Sample", "Variables"];
total = sum(tbl2, 2, 'omitnan');
idx = ~((85 <= total) & (total <= 105));
tbl2(table2array(idx), :) = [];
tbl2 = standardizeMissing(tbl2, 0);
tbl2 = fillmissing(tbl2, 'constant', 0.04);
data = table2array(tbl2);
data = log(data ./ geomean(data, 2));
tbl2(:, :) = array2table(data);

opts3 = detectImportOptions('attachment/附件.xlsx', Sheet='表单3', TextType='string', ...
    ReadRowNames=true, VariableNamingRule='preserve');
opts3 = setvartype(opts3, '表面风化', 'categorical');
opts3.VariableNames(1) = {'Erode'};
opts3.VariableNames(2:end) = extractBetween(opts3.VariableNames(2:end), '(', ')');

tbl3 = readtable('attachment/附件.xlsx', opts3);
tbl3.Properties.DimensionNames = ["Sample", "Variables"];
tbl3 = standardizeMissing(tbl3, 0);
tbl3(:, 2:end) = fillmissing(tbl3(:, 2:end), 'constant', 0.04);
data = table2array(tbl3(:, 2:end));
data = log(data ./ geomean(data, 2));
tbl3(:, 2:end) = array2table(data);

tbl1.ID = string(tbl1.Properties.RowNames);
tbl2.ID = string(tbl2.Properties.RowNames);
idx1 = contains(tbl2.ID, '严重风化点');
idx2 = contains(tbl2.ID, '未风化点');
pat = regexpPattern('^(\d+)');
tbl2.ID = double(extract(tbl2.ID, pat));
tbl4 = join(tbl2, tbl1);
tbl4{idx1, 'Erode'} = "风化";
tbl4{idx2, 'Erode'} = "无风化";
tbl1 = removevars(tbl1, 'ID');
tbl2 = removevars(tbl2, 'ID');
tbl4 = removevars(tbl4, 'ID');
tbl4 = movevars(tbl4, ["Style", "Type", "Color", "Erode"], After=0);

numeric = vartype('numeric');
tbl2(:, numeric) = round(tbl2(:, numeric), 2);
tbl3(:, numeric) = round(tbl3(:, numeric), 2);
tbl4(:, numeric) = round(tbl4(:, numeric), 2);

if exist('data', 'dir') ~= 7
    mkdir('data');
end

writetable(tbl1, 'attachment/附件-预处理后数据.xlsx', Sheet='表单1', ...
    WriteRowNames=true, WriteMode='overwritesheet');
writetable(tbl2, 'attachment/附件-预处理后数据.xlsx', Sheet='表单2', ...
    WriteRowNames=true, WriteMode='overwritesheet');
writetable(tbl3, 'attachment/附件-预处理后数据.xlsx', Sheet='表单3', ...
    WriteRowNames=true, WriteMode='overwritesheet');
writetable(tbl4, 'attachment/附件-预处理后数据.xlsx', Sheet='表单4', ...
    WriteRowNames=true, WriteMode='overwritesheet');