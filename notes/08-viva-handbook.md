# 08 — The viva handbook: 120 questions in the order they are asked

How to use this: cover the answers, read the question aloud, answer aloud. If you hesitate for more than three seconds, mark it and come back. Viva marks are lost to hesitation, not to ignorance.

---

## Part A — Opening questions (asked in every viva)

**1. What is data mining?**
Extracting implicit, previously unknown and potentially useful patterns from large amounts of data. It is a step in the KDD process, not the whole of it.

**2. State the KDD process.**
Data → selection → pre-processing (cleaning, integration, reduction, transformation) → data mining → pattern evaluation → knowledge presentation.

**3. What is the difference between data mining and machine learning?**
Machine learning is the family of algorithms; data mining is the whole process of extracting knowledge from data, using ML algorithms on pre-processed data and then evaluating and presenting the result.

**4. Which experiment did you like most, and why?**
Pick one and give a reason that contains a technical fact — e.g. "K-means, because the elbow method shows the choice of k is evidence-based rather than arbitrary."

**5. What is Weka, and why did the lab use it?**
An open-source Java toolkit of ML algorithms with a GUI, CLI and API; it lets you run and inspect algorithms without writing code, and it ships the standard ARFF datasets.

**6. Name the four Weka GUI applications.**
Explorer, Experimenter, KnowledgeFlow, Workbench (+ Simple CLI).

**7. What is ARFF?**
Attribute-Relation File Format — relation, attributes with types, then data rows; `%` comments, `?` missing.

**8. What is the difference between supervised and unsupervised learning?**
Supervised has labelled targets (classification, regression); unsupervised has no labels (clustering, association rules).

**9. What is pre-processing, and why is it needed?**
The steps that make data trustworthy, unified, compact and usable: cleaning, integration, reduction, transformation. Real data is incomplete, noisy, inconsistent and redundant.

**10. Name the four pre-processing families and one technique from each.**
Cleaning (missing-value imputation), integration (redundancy removal by correlation), reduction (sampling, PCA), transformation (normalisation, discretisation).

---

## Part B — Experiment 1 and 2 (Weka)

**11. Why does Weka need Java?**
It is a `.jar` written in Java; it runs on the JVM, which is also why it is platform independent.

**12. What are the six tabs in Explorer?**
Preprocess, Classify, Cluster, Associate, Select attributes, Visualize.

**13. Which tab shows per-attribute statistics?**
Preprocess — the Selected attribute panel shows type, missing count, distinct count, and min/max/mean/std-dev for numeric attributes.

**14. How do you find missing values in Weka without coding?**
Preprocess → the Missing column for each attribute; the `?` values are also counted in the dataset summary.

**15. How many instances and attributes in iris?**
150 and 5 (four numeric measurements, one nominal class with 3 balanced values).

**16. What does the Visualize tab show?**
A scatterplot matrix of every pair of attributes; colouring by the class reveals separability.

**17. Why is the class attribute special in Weka?**
It is the target used by Classify and by attribute evaluators; it is set by the "class" dropdown at the bottom-right of the Preprocess panel.

**18. Convert `a,b,c` / `1,2,3` / `4,5,6` to ARFF.**
```
@relation t
@attribute a numeric
@attribute b numeric
@attribute c numeric
@data
1,2,3
4,5,6
```

**19. Can Weka read CSV?**
Yes — Open file with the CSV filter, or the `CSVLoader` converter; the first row becomes the attribute names.

**20. What is the Simple CLI for?**
Running Weka from the command line inside Weka's process, e.g. `java weka.core.Instances data/iris.arff`.

---

## Part C — Experiment 3 (missing values, outliers)

**21. Define a missing value and an outlier, and give one difference in treatment.**
Missing = no recorded value (impute or drop); outlier = an extreme value (cap, delete, or keep). Missing is absence, outlier is presence.

**22. Write the IQR fence formulas.**
`IQR = Q3 − Q1`, `lower = Q1 − 1.5·IQR`, `upper = Q3 + 1.5·IQR`.

**23. Why 1.5?**
Tukey's constant: on normal data the fences sit at ≈ ±2.7σ, flagging ≈0.7% of points.

**24. Write the z-score formula and its threshold.**
`z = (x − μ)/σ`, flag if `|z| > 3` (2 for "mild").

**25. Which is more robust, and why?**
IQR, because quartiles ignore the magnitude of extremes, while the mean and standard deviation are pulled by the outliers being tested.

**26. What does `df.isnull().sum()` return?**
The count of missing values per column.

**27. What does `df.isnull().any(axis=1).sum()` return?**
The number of rows containing at least one missing value.

**28. Why did your `box_office_crore` count show 19 and not 21?**
Two cells are blank; pandas skips NaN in `count()` and `quantile()`.

**29. What is imputation? Name four methods.**
Replacing a missing value with an estimate: mean, median, mode, regression-predicted, KNN-based; plus a missing-indicator flag.

**30. Why median rather than mean for skewed data?**
The median is not moved by extreme values, so it represents the typical case better.

**31. How can you detect outliers graphically?**
Boxplot (points beyond the whiskers), histogram (long tail), scatterplot (isolated points).

**32. Worked: 10 values, n = 10, Q1 at what position?**
`(n−1)×0.25 = 2.25`, so Q1 = v[2] + 0.25·(v[3] − v[2]).

**33. What if a column has IQR = 0?**
More than half the values are identical, both fences collapse, and every different value is flagged — use another method.

**34. Difference between an outlier and noise?**
Noise is small random error everywhere (handled by smoothing/binning); an outlier is a large rare deviation (handled by detection and treatment).

**35. What did you do with the outlier you found?**
State the data, the method, the decision and the reason — e.g. "capped `votes` at the upper fence because the value is real but would dominate a distance-based model."

---

## Part D — Experiment 4 (patterns and correlations)

**36. Write the Pearson correlation formula.**
`r = cov(x,y)/(σx·σy)`, with `cov = Σ(xᵢ−x̄)(yᵢ−ȳ)/(n−1)`.

**37. What is the range and meaning of r?**
−1 to +1; sign is direction, magnitude is strength of the *linear* relation.

**38. What is r²?**
The coefficient of determination — the proportion of variance in y explained by x.

**39. r = 0.9 means what exactly?**
A strong positive linear relation; r² = 0.81, so 81% of the variation is explained linearly.

**40. Can r be 0 while the variables are related?**
Yes — a symmetric non-linear relation (e.g. y = x²) has r ≈ 0.

**41. Why is correlation not causation?**
A third variable can drive both (confounding), and the direction may be reversed.

**42. What is a correlation matrix and why is the diagonal 1?**
A table of all pairwise r values; each attribute correlates perfectly with itself.

**43. How do you detect redundant attributes?**
Off-diagonal |r| close to 1 between two predictors.

**44. What is multicollinearity?**
Highly correlated predictors making regression coefficients unstable and uninterpretable.

**45. Which Weka evaluator did you use and what does it do?**
`CorrelationAttributeEval` with `Ranker`: it computes the correlation of each attribute with the class, handling a nominal class by treating each value as an indicator and averaging.

**46. When do you use chi-square instead?**
When the class (or both attributes) are nominal: `χ² = Σ(O−E)²/E`, df = (r−1)(c−1), reject independence if p < 0.05.

**47. What is the difference between a pattern and a correlation?**
A correlation is a single number summarising a linear relation; a pattern is a rule holding for a subgroup, which can exist with r = 0.

**48. Give an example of a pattern you found.**
"Students studying ≥ 7 h averaged 80.17 marks against 51.17 below it, and all four students above 75 marks studied ≥ 7 h."

**49. Is that pattern causal?**
No — 12 observations, and study hours correlate 0.99 with attendance, so the two cannot be separated in this sample.

**50. What are the limitations of Pearson's r?**
Linear only, sensitive to outliers, no causal information, needs numeric data.

---

## Part E — Experiment 5 (K-means)

**51. What is clustering?**
Grouping objects so that members of a group are more similar to each other than to members of other groups; unsupervised.

**52. Why is K-means unsupervised?**
No labels are used; success is measured internally (SSE, silhouette), not by accuracy.

**53. Write the Euclidean distance formula.**
`d(p,q) = √(Σ(pᵢ − qᵢ)²)`.

**54. Compute d((1,2),(10,10)).**
√(81 + 64) = √145 = 12.0416.

**55. Write the K-means objective.**
`SSE = Σⱼ Σ_{x∈Cⱼ} ‖x − μⱼ‖²`.

**56. Give the algorithm in six steps.**
Choose k → initialise k centroids → assign each point to the nearest centroid → recompute centroids as cluster means → repeat until assignments stop changing → output clusters.

**57. Why does it converge?**
Each step monotonically decreases SSE, which is bounded below by zero; it stops at a local minimum.

**58. Why can two runs give different answers?**
Different initial centroids lead to different local minima; fixed by k-means++ seeding and multiple restarts (`n_init`).

**59. What did your program output?**
Clusters {(1,2),(2,1),(1,1)} and {(8,9),(9,8),(8,8)}, centroids (1.3333,1.3333) and (8.3333,8.3333), SSE 2.6667, converged in 2 iterations.

**60. Show the first iteration's distances.**
2.0000, 1.4142, 1.0000 → C1; 2.2361, 2.2361, 2.8284 → C2.

**61. Why did your notebook's program fail?**
`d2` was referenced before it was assigned — a `NameError`; the assignment must come before the comparison.

**62. How do you choose k?**
Elbow (SSE corner), silhouette (maximise), gap statistic, or domain knowledge; state the number.

**63. What did the elbow show for your data?**
k = 1 → 149.6667; k = 2 → 2.6667 (drop 147); k = 3 → 1.8333; k = 4 → 1.0000. The elbow is at k = 2.

**64. Write the silhouette formula.**
`s = (b − a)/max(a,b)`, a = mean intra-cluster distance, b = mean distance to the nearest other cluster; range −1 to +1.

**65. What is a centroid? Is it a data point?**
The mean vector of the cluster; it need not be an actual observation.

**66. K-means vs K-medoids?**
K-medoids uses an actual point (the one minimising the sum of dissimilarities), so it is robust to outliers and works with any distance; K-means is faster but outlier-sensitive.

**67. Which algorithm for non-convex clusters with noise?**
DBSCAN — density-based, arbitrary shapes, marks sparse points as noise.

**68. Why must you scale before clustering?**
Distance is dominated by the largest-range attribute.

**69. Complexity of K-means?**
O(n·k·d·i).

**70. What is hard vs soft clustering?**
Hard: one cluster per point (K-means). Soft: membership degrees (fuzzy c-means, GMM).

---

## Part F — Experiment 6 (Apriori)

**71. Write the support, confidence and lift formulas.**
`support(X→Y) = |X∪Y|/N`; `confidence = support(X∪Y)/support(X)`; `lift = confidence/support(Y)`.

**72. State the Apriori property.**
If an itemset is infrequent, all its supersets are infrequent (downward closure).

**73. Why is lift needed?**
High confidence can come from a frequent consequent alone; lift measures the gain over the base rate.

**74. What does lift = 1.33 mean?**
Y is 33% more likely when X is present than in general — a positive association.

**75. What does lift < 1 mean?**
Negative association: Y is less likely when X is present (substitutes).

**76. Give the two phases of Apriori.**
Frequent-itemset generation level by level, then rule generation with a confidence threshold.

**77. Explain join and prune.**
Join: combine (k−1)-itemsets sharing k−2 items into candidate k-itemsets. Prune: discard a candidate if any (k−1)-subset is not frequent.

**78. Your L1 and L2 for the 4-transaction data?**
L1: milk 4, bread 3, butter 2, diapers 2. L2: {bread,milk} 3, {bread,butter} 2, {butter,milk} 2, {diapers,milk} 2 (at minsup 0.5).

**79. What does minSupport 0.2 mean on 4 transactions?**
0.2 × 4 = 0.8 → an itemset appearing in ≥ 1 transaction qualifies; effectively no pruning.

**80. Which rule was genuinely interesting in your data?**
`{butter} → {bread}`, support 0.5, confidence 1.0, lift 1.3333; rules with milk have lift 1.0 because milk is in every basket.

**81. Why is a 1.0-lift rule useless?**
It says nothing beyond the base rate — the consequent was already certain.

**82. Apriori vs FP-Growth?**
Same results; Apriori scans once per level and generates candidates, FP-Growth builds a compressed tree in two scans with no candidates — much faster on dense data.

**83. What is a maximal frequent itemset?**
A frequent itemset with no frequent superset. Closed = frequent and no superset with the same support.

**84. Why must item columns be nominal in Weka?**
Apriori treats items as categories; numeric 0/1 columns are rejected or must be discretised.

**85. Name three applications.**
Market basket analysis, cross-selling/recommendation, web clickstream analysis (also medical and fraud rules).

**86. What is the worst-case complexity?**
Exponential, 2^d candidate itemsets for d items; pruning makes it practical.

**87. How would you handle a numeric attribute like age?**
Discretise it into intervals (young/middle/old) and then mine.

---

## Part G — Code-reading questions (they point at a line)

**88. `out.append(float(v) if v != "" else None)` — what does this do?**
Converts a present cell to a number and records a blank cell as `None`, i.e. a missing value, without turning it into 0.

**89. Why `len(sorted_vals) - 1` in the quantile function?**
Because it is the position index over n−1 gaps, which is the same convention pandas/numpy use for linear interpolation.

**90. `(sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5` — what is this?**
The sample standard deviation, with n−1 in the denominator (Bessel's correction).

**91. `df[(df[col] < lower) | (df[col] > upper)][col]` — step by step?**
Builds a boolean mask for rows outside the fences, filters the frame, and keeps only that column.

**92. `select_dtypes(include="number")` — why?**
To keep only numeric columns, because IQR cannot be computed on text.

**93. `itertools.combinations(items, 2)` in the rule generator — why?**
To enumerate every 2-element subset as an antecedent.

**94. `if itemset <= t` — what does `<=` mean for frozensets?**
Subset test: every element of `itemset` is in `t`.

**95. `dists.index(min(dists))` — what does it return?**
The index of the nearest centroid, which is the cluster assignment.

**96. `model.inertia_` — what is it?**
The within-cluster sum of squared distances, i.e. the SSE that K-means minimises.

**97. `sorted(level.items(), key=lambda kv: (-kv[1], sorted(kv[0])))` — why?**
Sort by descending count, then alphabetically, so output is deterministic.

**98. `df.corr(numeric_only=True)[TARGET].drop(TARGET)` — why drop?**
To remove the attribute's correlation with itself (always 1.0), which would top the ranking.

**99. In the Weka output `{bread=t}` — why is `=t` printed?**
Because ARFF nominal attributes are printed as `attribute=value`; the rule is on the value, not the column.

**100. `round(x, 2)` after the mean — does it change the clustering?**
No, it only affects display; rounding before the next iteration would introduce a small error.

---

## Part H — Comparison questions (the "why this and not that" set)

**101. Mean vs median imputation?**
Mean preserves the average but is pulled by outliers and shrinks variance; median is robust for skewed data.

**102. Deletion vs imputation for missing values?**
Deletion is safe only if missingness is MCAR and the loss is small; otherwise imputation avoids bias but invents information.

**103. Normalisation vs standardisation?**
Min–max maps to [0,1] (sensitive to outliers, keeps no distribution shape); z-score gives mean 0, std 1 (assumes no heavy tail).

**104. IQR vs z-score for outliers?**
IQR is rank-based and robust; z-score is mean-based and assumes normality.

**105. K-means vs hierarchical clustering?**
K-means needs k and gives a flat partition, fast on large n; hierarchical gives a dendrogram, no k needed, O(n²) or worse.

**106. K-means vs DBSCAN?**
K-means: spherical, k required, all points assigned. DBSCAN: arbitrary shapes, k not needed, noise identified, but sensitive to eps/minPts.

**107. Apriori vs FP-Growth?** (see 82)

**108. Correlation vs chi-square?**
Correlation: two numeric attributes. Chi-square: categorical attributes or a categorical class.

**109. Weka vs writing Python?**
Weka: no code, standard visualisations, good for demonstrating and comparing algorithms. Python: reproducible, scriptable, integrates with real pipelines and custom metrics.

**110. Classification vs clustering?**
Labels present vs absent; predictive accuracy vs internal cohesion.

---

## Part I — Traps, and the honest answers

**111. Your result is 100% accurate — is that good?**
Ask about leakage, sample size and class balance. With 4 transactions, 100% confidence is a coincidence, not a finding.

**112. Your model has 90% accuracy on imbalanced data — good?**
Only if the base rate is not 90%; report precision, recall and F1 alongside.

**113. Your correlation is 0.99 — is the relationship proven?**
No: 12 observations, possible confounding, and correlation is not causation.

**114. Why is your outlier still in the data?**
Because it is a genuine extreme (a blockbuster film), not an error; deleting it would remove the phenomenon being studied. I capped/flagged it instead.

**115. Why only 2 clusters?**
The elbow and silhouette both indicate 2, and the data has two visible groups.

**116. What would you do with 1 million rows and 500 attributes?**
Sample and reduce first (feature selection/PCA), use mini-batch K-means, and FP-Growth instead of Apriori.

**117. What is the biggest limitation of your work?**
The datasets are tiny; thresholds and cluster counts are therefore indicative rather than conclusive.

**118. If your program crashed in the lab, what would you say?**
State the error, its cause and the fix — e.g. "NameError because d2 was used before assignment; I reordered the lines." That is a correct answer, not a failure.

**119. Why did you print your name inside the program?**
To make the output verifiably my own run.

**120. What did you learn from this lab that you will actually use?**
Pick one honest item, e.g. "that a threshold is meaningless without knowing the number of transactions, which is why I now always report support as a count as well as a fraction."
