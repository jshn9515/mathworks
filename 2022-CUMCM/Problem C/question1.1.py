import pandas as pd
import scipy.stats as stats

df = pd.read_excel('attachment/附件-预处理后数据.xlsx', sheet_name='表单1', index_col=0)

P1 = pd.crosstab(index=df['纹饰'], columns=df['表面风化'])
P2 = pd.crosstab(index=df['类型'], columns=df['表面风化'])
P3 = pd.crosstab(index=df['颜色'], columns=df['表面风化'])

alpha = 0.05

# An often quoted guideline for the validity of this calculation is that
# the test should be used only if the observed and expected frequencies
# in each cell are at least 5.
stat1 = stats.chi2_contingency(P1.values)
stat2 = stats.chi2_contingency(P2.values)
stat3 = stats.chi2_contingency(P3.values)

result1 = [
    [stat1.pvalue < alpha, stat2.pvalue < alpha, stat3.pvalue < alpha],
    [stat1.pvalue, stat2.pvalue, stat3.pvalue],
    [stat1.statistic, stat2.statistic, stat3.statistic],
]

# MATLAB's fishertest only applies to 2x2 contingency table.
# But SciPy v1.15.0 added support for tables of any size.
# ref: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html
stat4 = stats.fisher_exact(P1.values)
stat5 = stats.fisher_exact(P2.values)
stat6 = stats.fisher_exact(P3.values)

result2 = [
    [stat4.pvalue < alpha, stat5.pvalue < alpha, stat6.pvalue < alpha],
    [stat4.pvalue, stat5.pvalue, stat6.pvalue],
    [stat4.statistic, stat5.statistic, stat6.statistic],
]

index = ['h', 'pvalue', 'statistic']
columns = ['纹饰', '类型', '颜色']
result1 = pd.DataFrame(result1, index=index, columns=columns)
result2 = pd.DataFrame(result2, index=index, columns=columns)

with pd.ExcelWriter('data/问题1-假设检验.xlsx') as writer:
    result1.to_excel(writer, sheet_name='卡方检验', float_format='%.4f')
    result2.to_excel(writer, sheet_name='Fisher检验', float_format='%.4f')
