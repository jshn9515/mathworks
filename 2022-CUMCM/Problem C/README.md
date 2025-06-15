# Problem C: Composition Analysis and Identification of Ancient Glass Artifacts

## Background

The study of ancient glass artifacts holds significant value across various fields such as culture, history, and art. Analyzing and identifying their composition aids in the protection and academic study of cultural relics. This paper analyzes the chemical composition of glass artifacts to achieve two main objectives: (1) to predict the pre-weathering chemical composition of weathered high-potassium glass and lead-barium glass, thereby achieving _composition restoration_; and (2) to construct a subclassification model for glass artifacts, enabling reasonably accurate identification of glass type and subcategory based on known chemical composition—even for weathered samples. This has practical significance for archaeologists studying glass artifacts.

## Data Preprocessing

The dataset provided is **compositional data**, which requires focus on the **relative proportions** of each component rather than their absolute values. The data is also characterized by high dimensionality, sparsity, and right-skewness. To address these issues, we applied the **Centered Log-Ratio (CLR) transformation**, which highlights the relative importance of each chemical component in a glass artifact and partially corrects for the undesirable properties of compositional data.

## Problem 1

For Problem 1, chi-squared and Fisher’s exact tests revealed no significant relationship between decorative patterns, color, and surface weathering, but a strong correlation between glass type and weathering status. Both qualitative and quantitative analyses were performed to examine compositional differences between weathered and unweathered lead-barium and high-potassium glass artifacts. We found that eight components (e.g., K2O, CaO) showed significant differences in lead-barium glass, and seven components (e.g., SiO2, Na2O) in high-potassium glass. Since existing data do not allow precise mapping of a weathered composition to its original state, we used **descriptive statistical methods** to estimate the original relative composition of weathered samples, achieving a form of composition restoration.

## Problem 2

We explored classification patterns from both categorical and numerical perspectives. For categorical data, we used decision trees to assess feature importance. For numerical data, we performed dimensionality reduction followed by **Support Vector Machine (SVM)** classification to derive explicit formulas separating lead-barium and high-potassium glass. For subclassification, we selected chemical components based on variance and applied **hierarchical clustering**, identifying three subtypes within each main category:

- Lead-barium glass: high-sodium/low-phosphorus, low-sodium/low-phosphorus, and low-sodium/high-phosphorus.
- High-potassium glass: low-sodium/high-potassium, high-sodium/potassium-rich, and low-sodium/potassium-rich.

SVM was again used to derive explicit classification expressions. Finally, we added noise to verify the **robustness** of our model.

## Problem 3

For Problem 3, building on the previous conclusions, we first provided a rough qualitative classification method with practical significance. Then, using the trained SVM classifier, we quantitatively categorized the unknown samples into major and subtypes:

- A2, A3, A4, A5, A8 belong to the lead-barium category.
- A1, A6, A7 belong to the high-potassium category.

Among the lead-barium glass samples, A5 falls into the "high-sodium/low-phosphorus" subtype, and the rest into "low-sodium/high-phosphorus". Among the high-potassium samples, A1 belongs to the "low-sodium/high-potassium" subtype, and the others to "low-sodium/potassium-rich". A robustness test was performed to further validate the classifier's performance.

## Problem 4

For Problem 4, we used correlation heatmaps to evaluate differences in chemical composition proportions between the two glass categories. The non-parametric Kolmogorov–Smirnov (K-S) test was employed to assess statistical differences in component relationships across categories. The results showed significant differences in the relational structure of K2O and BaO between subcategories.

## Conclusion

In summary, after applying an appropriate CLR transformation, we effectively extracted meaningful features from the compositional data by focusing on **relative importance**. This enabled successful classification and subclassification of ancient glass artifacts. Given the limited sample size, we employed methods suitable for small datasets, avoiding overly complex or low-interpretability models.
