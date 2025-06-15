%% Question 1.1
clear; clc;

tbl = readtable('attachment/附件-预处理后数据.xlsx', Sheet='表单1', ...
    TextType='string', ReadRowNames=true);

alpha = 0.05;
[P1, chi1, pval1] = crosstab(tbl.Style, tbl.Erode, OutputFormat='table');
[P2, chi2, pval2] = crosstab(tbl.Type, tbl.Erode, OutputFormat='table');
[P3, chi3, pval3] = crosstab(tbl.Color, tbl.Erode, OutputFormat='table');
[h, pval, stats] = fishertest(P2, Alpha=alpha);

result = [
    pval1 < 0.05, pval2 < 0.05, pval3 < 0.05;
    pval1, pval2, pval3;
    chi1, chi2, chi3;
    ];

index = ["h", "pvalue", "statistic"];
column = ["Style", "Type", "Color"];
dim = ["Test", "Variables"];
result = array2table(result, RowNames=index, VariableNames=column, DimensionNames=dim);
result = round(result, 4);

writetable(result, 'data/问题1-假设检验.xlsx', Sheet='卡方检验', ...
    WriteRowName=true, WriteMode='overwritesheet');

%% Question 1.2
clear; clc;

opts = detectImportOptions('attachment/附件-预处理后数据.xlsx', Sheet='表单4', ...
    TextType='string', ReadRowNames=true);
opts = setvartype(opts, opts.VariableNames(1:4), 'categorical');
tbl = readtable('attachment/附件-预处理后数据.xlsx', opts);

numeric = vartype('numeric');
tbl1 = tbl((tbl.Erode == '风化') & (tbl.Type == '铅钡'), numeric);
tbl2 = tbl((tbl.Erode == '无风化') & (tbl.Type == '铅钡'), numeric);
tbl3 = tbl((tbl.Erode == '风化') & (tbl.Type == '高钾'), numeric);
tbl4 = tbl((tbl.Erode == '无风化') & (tbl.Type == '高钾'), numeric);

figure(1);
fig = tiledlayout(3, 5, TileSpacing='loose', Padding='compact');
for col = tbl1.Properties.VariableNames
    nexttile;
    boxchart(tbl.Type, tbl{:, col}, GroupByColor=tbl.Erode);
    title(col);
    set(gca, FontName='Microsoft YaHei', FontSize=12, TitleFontWeight='normal');
end
exportgraphics(fig, 'data/问题1-风化前后化学成分含量箱线图.svg', ...
    Width=15, Height=8, Units='inches');

figure(2);
fig = tiledlayout(3, 5, TileSpacing='loose', Padding='compact');
for col = tbl1.Properties.VariableNames
    nexttile;
    [f, xf] = kde(tbl1{:, col}, Bandwidth=0.5);
    hold on
    area(xf, f, EdgeColor='#1F77B4', LineWidth=1, FaceColor='#1F77B4', FaceAlpha=0.6);
    [f, xf] = kde(tbl2{:, col}, Bandwidth=0.5);
    area(xf, f, EdgeColor='#FF7E1D', LineWidth=1, FaceColor='#FF7E1D', FaceAlpha=0.6);
    title(col);
    set(gca, FontName='Microsoft YaHei', FontSize=12, TitleFontWeight='normal');
    hold off
end
exportgraphics(fig, 'data/问题1-风化前后铅钡化学成分含量核密度图.svg', ...
    Width=15, Height=8, Units='inches');

figure(3);
fig = tiledlayout(3, 5, TileSpacing='loose', Padding='compact');
for col = tbl3.Properties.VariableNames
    nexttile;
    [f, xf] = kde(tbl3{:, col}, Bandwidth=0.5);
    hold on
    area(xf, f, EdgeColor='#1F77B4', LineWidth=1, FaceColor='#1F77B4', FaceAlpha=0.6);
    [f, xf] = kde(tbl4{:, col}, Bandwidth=0.5);
    area(xf, f, EdgeColor='#FF7E1D', LineWidth=1, FaceColor='#FF7E1D', FaceAlpha=0.6);
    title(col);
    hold off
    set(gca, FontName='Microsoft YaHei', FontSize=12, TitleFontWeight='normal');
end
exportgraphics(fig, 'data/问题1-风化前后高钾化学成分含量核密度图.svg', ...
    Width=15, Height=8, Units='inches');

alpha = 0.05;
index = ["h", "pvalue", "statistic"];
column = string(tbl1.Properties.VariableNames);
dim = ["Test", "Variables"];

result1 = zeros(3, length(column));
num = 1;
for col = tbl1.Properties.VariableNames
    [p, h, stats] = ranksum(tbl1{:, col}, tbl2{:, col}, Alpha=alpha);
    result1(:, num) = [h; p; stats.ranksum];
    num = num + 1;
end
result1 = array2table(result1, RowNames=index, VariableNames=column, DimensionNames=dim);
result1 = round(result1, 4);

result2 = zeros(3, length(column));
num = 1;
for col = tbl3.Properties.VariableNames
    [p, h, stats] = ranksum(tbl3{:, col}, tbl4{:, col}, Alpha=alpha);
    result2(:, num) = [h; p; stats.ranksum];
    num = num + 1;
end
result2 = array2table(result2, RowNames=index, VariableNames=column, DimensionNames=dim);
result2 = round(result2, 4);

writetable(result1, 'data/问题1-假设检验.xlsx', Sheet='铅钡玻璃秩和检验', ...
    WriteRowNames=true, WriteMode='overwritesheet');
writetable(result2, 'data/问题1-假设检验.xlsx', Sheet='高钾玻璃秩和检验', ...
    WriteRowNames=true, WriteMode='overwritesheet');

%% Question 1.3
clear; clc;

opts = detectImportOptions('attachment/附件-预处理后数据.xlsx', Sheet='表单4', ...
    TextType='string', ReadRowNames=true);
opts = setvartype(opts, opts.VariableNames(1:4), 'categorical');
tbl = readtable('attachment/附件-预处理后数据.xlsx', opts);

numeric = vartype('numeric');
tbl1 = tbl((tbl.Erode == '风化') & (tbl.Type == '铅钡'), numeric);
tbl2 = tbl((tbl.Erode == '无风化') & (tbl.Type == '铅钡'), numeric);
tbl3 = tbl((tbl.Erode == '风化') & (tbl.Type == '高钾'), numeric);
tbl4 = tbl((tbl.Erode == '无风化') & (tbl.Type == '高钾'), numeric);

TypstExport = true;
index = string(tbl1.Properties.VariableNames);
if TypstExport
    % Typst support, export as CSV table.
    tbl5 = table(RowNames=index);
    tbl5 = addvars(tbl5, mean(tbl1.Variables).', NewVariableNames='铅钡风化后');
    tbl5 = addvars(tbl5, mean(tbl2.Variables).', NewVariableNames='铅钡风化前');
    data = mean(tbl2) - mean(tbl1);
    tbl5 = addvars(tbl5, data.Variables.', NewVariableNames='铅钡均值差');
    tbl5 = addvars(tbl5, mean(tbl1.Variables).', NewVariableNames='高钾风化后');
    tbl5 = addvars(tbl5, mean(tbl2.Variables).', NewVariableNames='高钾风化前');
    data = mean(tbl2) - mean(tbl1);
    tbl5 = addvars(tbl5, data.Variables.', NewVariableNames='高钾均值差');
    tbl5.Properties.DimensionNames = ["化学元素", "Variables"];
    tbl5 = round(tbl5, 2);
    writetable(tbl5, 'data/问题1-各化学成分的均值差.csv', WriteRowNames=true, Encoding='GBK');
end

tbl1 = tbl1 + (mean(tbl2) - mean(tbl1));
tbl3 = tbl3 + (mean(tbl4) - mean(tbl3));

function y = softmax(x)
x = table2array(x);
s = exp(x - max(x, [], 2));
y = s ./ sum(s, 2);
y = array2table(y * 100);
end

tbl1(:, :) = softmax(tbl1);
tbl3(:, :) = softmax(tbl3);
tbl1 = round(tbl1, 2);
tbl3 = round(tbl3, 2);

writetable(tbl1, 'data/问题1-铅钡高钾还原数据.xlsx', Sheet='铅钡-还原', ...
    WriteRowNames=true, WriteMode='overwritesheet');
writetable(tbl3, 'data/问题1-高钾高钾还原数据.xlsx', Sheet='铅钡-还原', ...
    WriteRowNames=true, WriteMode='overwritesheet');

if TypstExport
    writetable(tbl1, 'data/问题1-铅钡还原数据.csv', WriteRowNames=true, Encoding='GBK');
    writetable(tbl3, 'data/问题1-高钾还原数据.csv', WriteRowNames=true, Encoding='GBK');
end