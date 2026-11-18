# Question bank — Data Mining Lab (24CAP-308)

Everything that can be asked in the written part, the viva and the on-machine part, organised by experiment. Marks are indicative: **2** = one short paragraph, **5** = half a page with a formula or steps, **10** = a full answer with a numerical or a table.

Model answers are given as outlines — expand each bullet to a sentence in the exam, because the examiner is marking sentences.

---

## Section A — General (Unit 1: what the lab is about)

**A1 (2). Define data mining.**
Extraction of implicit, previously unknown, potentially useful patterns from large data; one step of the KDD process.

**A2 (5). Explain the KDD process with a diagram.**
Selection → pre-processing (cleaning, integration, reduction, transformation) → data mining → pattern evaluation → knowledge presentation. One line per stage.

**A3 (2). What is Weka?**
Open-source Java toolkit (Waikato, NZ) of ML algorithms with GUI, CLI and API.

**A4 (5). Compare Weka and Python for data mining.**

| | Weka | Python (pandas/scikit-learn) |
|---|---|---|
| Setup | installer | pip + code |
| Ease | GUI, no code | code required |
| Reproducibility | clicks, saved config | script |
| Extensibility | fixed algorithms | any library |
| Best for | demonstrating, comparing | real pipelines |

**A5 (2). What is ARFF?**
Weka's text data format: `@relation`, `@attribute` declarations with types, `@data` rows; `%` comment, `?` missing.

**A6 (5). Write an ARFF file for a dataset with attributes age (numeric), city (nominal: Delhi, Mumbai) and bought (nominal: yes, no) with two rows.**
```arff
@relation customer
@attribute age numeric
@attribute city {Delhi,Mumbai}
@attribute bought {yes,no}
@data
25,Delhi,yes
40,Mumbai,no
```

**A7 (2). Why is ARFF preferred in Weka over CSV?**
It declares types and nominal value sets explicitly, so no inference is needed and invalid values are rejected at load time.

**A8 (5). List the four pre-processing families and give one technique and one effect of each.**
Cleaning (imputation → completeness), integration (redundancy removal → consistency), reduction (sampling/PCA → compactness), transformation (normalisation → usability).

**A9 (2). Difference between supervised and unsupervised learning.**
Labels present vs absent; prediction vs structure discovery.

**A10 (2). What is the difference between a training set and a test set?**
Training fits the model; test estimates generalisation on unseen data. Splitting prevents overfitting from being hidden.

---

## Section B — Experiment 1: Install Weka

**B1 (5). Write the steps to install Weka on Windows.**
Visit the official download page → choose 3.8.x and the Windows `zulu` installer (bundles Java) → run → accept licence → default path → Next/Install/Finish → launch from Start menu → verify the GUI Chooser and Explorer's six tabs.

**B2 (2). Why does Weka need Java?**
It is a `.jar` executed by the JVM; that is also why it is platform independent.

**B3 (5). Name the four Weka applications and one use of each.**
Explorer (main workbench), Experimenter (compare algorithms statistically), KnowledgeFlow (visual pipelines), Workbench (all-in-one) + Simple CLI (commands).

**B4 (2). What are the six tabs of the Explorer?**
Preprocess, Classify, Cluster, Associate, Select attributes, Visualize.

**B5 (5). How do you verify a correct installation?**
GUI Chooser opens with the version; Explorer shows six tabs; the `data` folder exists beside `weka.jar` with `iris.arff`; Simple CLI prints the structure of `iris.arff` (150 instances).

**B6 (5). List four installation failures and their fixes.**
No Java (install a JRE / use the zulu build); wrong working directory (`cd` first); path with spaces (quote it); partial extraction (extract the whole archive).

**B7 (2). Difference between Weka 3.8 and 3.9.**
3.8 = stable branch; 3.9 = development branch with newer, occasionally unstable algorithms.

---

## Section C — Experiment 2: Load and visualise

**C1 (5). Write the procedure to load a dataset in Weka and read its statistics.**
Explorer → Preprocess → Open file… → select file → note Relation/Instances/Attributes → click each attribute → record Missing, Distinct, Type, Unique and Min/Max/Mean/StdDev.

**C2 (2). How many instances and attributes does iris have, and what are their types?**
150 instances, 5 attributes; four numeric measurements and one nominal 3-value class.

**C3 (5). How do you visualise the data in Weka and what do you conclude?**
Visualize tab → scatterplot matrix → set Colour = class → click a plot to enlarge → conclusion: petal measurements separate the classes; sepal width does not.

**C4 (5). What does the Selected attribute panel show, and why is it useful?**
Name, Missing, Distinct, Type, Unique, plus Min/Max/Mean/StdDev (or value counts for nominal). It is the fastest data-quality check: Missing > 0 flags gaps, Distinct = 1 flags a useless attribute, Unique = instance count flags an ID.

**C5 (2). What is the difference between Distinct and Unique?**
Distinct = number of different values; Unique = how many occur exactly once.

**C6 (5). Load the dataset by command line and explain the command.**
`java weka.core.Instances data/iris.arff` in Simple CLI (classpath already set); from a terminal `java -cp weka.jar weka.core.Instances data/iris.arff`. `weka.core.Instances` is the class that loads data and prints a summary.

**C7 (5). Can Weka read CSV/Excel?**
CSV: yes (Open file with the CSV filter, or `CSVLoader`). Excel: convert to CSV first, or use `ExcelLoader`. The first row becomes the attribute names.

**C8 (2). What does `?` mean in an ARFF file?**
A missing value.

---

## Section D — Experiment 3: Missing values and outliers

**D1 (5). Write the algorithm to detect missing values and outliers.**
1 import/load → 2 head() → 3 info() → 4 describe() → 5 select numeric columns → 6 Q1, Q3 → 7 IQR = Q3−Q1 → 8 lower/upper fences → 9 select values outside → 10 display → 11 `isnull().sum()` → 12 conclude with the treatment.

**D2 (2). Define a missing value.**
An attribute value not recorded for an instance; represented as NaN, not as zero.

**D3 (2). Define an outlier.**
An observation deviating so much from the rest that it appears to be generated by a different mechanism.

**D4 (5). Write the IQR method with formulas and explain the 1.5 constant.**
IQR = Q3−Q1; lower = Q1−1.5·IQR; upper = Q3+1.5·IQR. 1.5 is Tukey's constant: on normal data the fences correspond to ≈ ±2.7σ, flagging ≈0.7% of points.

**D5 (5). Numerically: 4,8,15,16,23,42,8,4,12,20 → Q1, Q3, IQR, fences, outliers.**
Sorted 4,4,8,8,12,15,16,20,23,42 (n=10). Q1 at p=2.25 → 8; Q3 at p=6.75 → 19; IQR 11; fences −8.5 and 35.5; **42 is the outlier**.

**D6 (5). Write the z-score method and compute z for 42 in the same data.**
z = (x−μ)/σ; μ = 15.2, σ = 11.3901; z = 26.8/11.3901 = **+2.3529** → outlier at |z|>2, not at |z|>3.

**D7 (5). Compare the IQR and z-score methods.**
Table: rank-based/robust vs mean-based/normal assumption; gives a flag vs a distance; fails when IQR=0 vs fails with skewed data (σ inflated by the outlier); preference: IQR for skewed/small samples.

**D8 (5). Why does the z-score method miss an outlier that IQR finds?**
The outlier inflates both μ and σ, which are exactly the quantities used to judge it; with a large σ the standardised distance falls below the threshold. This is the masking effect.

**D9 (5). List six treatments for missing values.**
Delete rows; mean impute; median impute; mode impute; regression/KNN impute; add a missing-indicator flag.

**D10 (5). List five treatments for outliers.**
Delete (proven error); cap/winsorise at the fence; log/sqrt transform; bin/discretise; keep and model separately; robust model (median, K-medoids).

**D11 (2). What does `df.isnull().sum()` return, and how do you count affected rows?**
Missing count per column; `df.isnull().any(axis=1).sum()` counts rows with at least one missing value.

**D12 (5). Why did a column's `count` show 19 instead of 21?**
Two cells were blank and pandas excludes NaN from `count`, `quantile` and `mean`.

**D13 (2). Why is the median preferred for skewed data?**
It is not moved by extreme values, so it represents the typical observation.

**D14 (5). Detect outliers in Weka without code.**
Preprocess → click attribute → read Min/Max/Mean/StdDev and Missing; Visualize → plot / boxplot-style view; or apply the `InterquartileRange` filter with `--filter` to remove instances outside the fences.

---

## Section E — Experiment 4: Patterns and correlations

**E1 (5). Write the procedure to find correlations in Weka.**
Explorer → Preprocess → load numeric dataset → **Select attributes** tab → AttributeEvaluator = `CorrelationAttributeEval` → Search = `Ranker` → confirm → set class → Start → read ranked merits → return to Preprocess and Remove the negligible attributes.

**E2 (5). Write the Pearson formula and explain each term.**
r = cov(x,y)/(σx·σy), cov = Σ(xᵢ−x̄)(yᵢ−ȳ)/(n−1). Numerator: joint deviation; denominator: normalisation so r is scale-free; range −1…+1.

**E3 (5). Numerically: x = 2,4,6,8,10; y = 5,9,12,16,18.**
x̄=6, ȳ=12, Σproducts=66, cov=16.5, σx=3.1623, σy=5.2440, **r = 0.9950**, r² = 0.9900.

**E4 (2). Interpret r = −0.85.**
Strong negative linear relation: as one increases, the other decreases, close to a falling line.

**E5 (2). What is r²?**
The proportion of variance in one attribute explained by the linear relation with the other.

**E6 (5). What is a correlation matrix and how do you use it for redundancy?**
Square table of all pairwise r values; the diagonal is 1; off-diagonal |r| ≈ 1 between two predictors means one is redundant and can be removed.

**E7 (2). What is multicollinearity?**
High correlation among predictors, making regression coefficients unstable and hard to interpret.

**E8 (5). When do you use chi-square instead of correlation? Give the formula.**
When attributes/class are nominal: χ² = Σ(O−E)²/E, E = (row total × column total)/grand total, df = (r−1)(c−1); large χ² (p<0.05) = dependent.

**E9 (5). What does CorrelationAttributeEval compute?**
Pearson correlation of each attribute with the class; a nominal class is handled by treating each value as an indicator and combining the correlations as a weighted average.

**E10 (5). Difference between a pattern and a correlation, with an example.**
Correlation is one number summarising a linear relation; a pattern is a rule holding for a subgroup. Example: r = 0.9979 between study hours and marks; pattern = "all students scoring ≥75 studied ≥7 h".

**E11 (2). Why is correlation not causation?**
A third variable can drive both, and the direction can be reversed; only a controlled experiment establishes causation.

---

## Section F — Experiment 5: K-means

**F1 (5). Write the K-means algorithm.**
Choose k → initialise k centroids → assign each point to the nearest centroid by Euclidean distance → recompute each centroid as the cluster mean → repeat until assignments stop changing → output clusters and centroids.

**F2 (5). Write the Euclidean distance formula and compute d((1,2),(10,10)).**
√(Σ(pᵢ−qᵢ)²); √(81+64) = √145 = **12.0416**.

**F3 (10). Perform one iteration for points (1,2),(2,1),(1,1),(8,9),(9,8),(8,8) with centroids (1,0) and (10,10).**
Distances: 2.0000, 1.4142, 1.0000 / 11.4018, 11.3137, 10.6301 to C1; 12.0416, 12.0416, 12.7279 / 2.2361, 2.2361, 2.8284 to C2. Clusters: first three to C1, last three to C2. New centroids **(1.3333,1.3333)** and **(8.3333,8.3333)**. Repeat: assignment unchanged → converged in 2 iterations, SSE 2.6667.

**F4 (5). Write the K-means objective function and explain each symbol.**
SSE = Σⱼ Σ_{x∈Cⱼ}‖x−μⱼ‖²; Cⱼ is cluster j, μⱼ its centroid, the inner sum is over points, the outer over clusters.

**F5 (2). Why is K-means unsupervised?**
No labels are used; groups are inferred from distances, and quality is measured internally (SSE/silhouette).

**F6 (5). Why does K-means always converge, and why is that not enough?**
Each step decreases SSE and SSE ≥ 0, so the process stabilises; but it stabilises at a **local** minimum, so the result depends on the initial centroids.

**F7 (5). How do you choose k?**
Elbow (SSE vs k), silhouette (maximise mean s), gap statistic, or domain knowledge; always report the number and the evidence.

**F8 (5). Silhouette: formula and interpretation.**
s = (b−a)/max(a,b); a = mean distance to points in the same cluster, b = mean distance to the nearest other cluster; range −1…+1; near 1 = well inside its cluster, near 0 = boundary, negative = probably misassigned.

**F9 (5). K-means vs K-medoids.**
Centroid (mean, may not be a data point, outlier-sensitive) vs medoid (actual point minimising sum of dissimilarities, robust, any distance); K-means faster; PAM = the K-medoids algorithm.

**F10 (5). Which algorithms handle non-convex clusters and noise?**
DBSCAN (density-based: eps and minPts, core/border/noise points), OPTICS, spectral clustering; K-means fails because it partitions by distance to a centroid.

**F11 (2). Why must features be scaled before K-means?**
Distance is dominated by the largest-range attribute; unscaled clustering effectively uses one column.

**F12 (5). What is the elbow method, and what did it show on your data?**
Plot SSE against k and take the corner; verified: k=1 149.6667, k=2 2.6667, k=3 1.8333, k=4 1.0000 → drop of 147 from k=1 to 2, then <1 each → **elbow at k=2**.

**F13 (2). Name the bug in the notebook program and its fix.**
`d2` is used in `if d1 < d2` before being assigned → `NameError`; move the `d2` computation above the comparison.

**F14 (2). Complexity of K-means.**
O(n·k·d·i) — n points, k clusters, d dimensions, i iterations.

**F15 (5). What are the limitations of K-means?**
k must be chosen; spherical similar-sized clusters only; sensitive to scaling, initialisation and outliers; every point is forced into a cluster (no noise label).

---

## Section G — Experiment 6: Apriori

**G1 (5). Write the Apriori algorithm.**
Set minsup/minconf → count items → L1 → repeat: join (k−1)-itemsets sharing k−2 items, prune those with an infrequent (k−1)-subset, count survivors, keep those ≥ minsup → stop when empty → generate rules from itemsets → keep conf ≥ minconf.

**G2 (5). State and explain the Apriori property.**
If an itemset is infrequent, all its supersets are infrequent (downward closure). It allows pruning entire candidate branches before counting, which is what makes the level-wise search practical.

**G3 (5). Write support, confidence and lift with one line of interpretation each.**
support(X∪Y)/N = how common; confidence = sup(X∪Y)/sup(X) = how reliable; lift = conf/sup(Y) = how much better than chance (>1 useful, =1 independent, <1 negative).

**G4 (10). For T1={A,B,C}, T2={A,C}, T3={A,B}, T4={B,C}, T5={A,B,C} with minsup 0.4 and minconf 0.6, find all frequent itemsets and strong rules.**
L1: A 0.8, B 0.8, C 0.8. L2: AB 0.6, AC 0.6, BC 0.6. L3: ABC 0.4. Rules: nine, e.g. A→B support 0.6, confidence 0.75, **lift 0.9375**; AB→C support 0.4, confidence 0.6667, lift 0.8333. All lifts < 1 → negative association, do not cross-sell.

**G5 (10). For the retail 4-transaction data at minsup 0.5, show L1, L2, L3 and the best rule.**
L1: milk 4, bread 3, butter 2, diapers 2. L2: {bread,milk} 3, {bread,butter} 2, {butter,milk} 2, {diapers,milk} 2 (pairs with count 1 pruned). L3: {bread,butter,milk} 2. Best rule {butter}→{bread}: support 0.5, confidence 1.0, lift 1.3333.

**G6 (5). What does minimum support 0.2 mean on a 4-row dataset, and what happens?**
0.2 × 4 = 0.8, and counts are whole numbers, so an itemset appearing once qualifies → no pruning, every itemset including the 4-item one is frequent, and 16 rules are produced. Thresholds are meaningless without the row count.

**G7 (5). Write the Weka procedure for Apriori.**
Create ARFF with nominal `{t,f}` item attributes → Explorer → Preprocess → Open file → Associate tab → choose Apriori → set minSupport 0.2, metricType Confidence, minMetric 0.8 → Start → read frequent itemsets, then best rules with confidence and support.

**G8 (2). Why must the item attributes be nominal?**
Apriori treats items as categories; numeric columns are rejected ("Cannot handle numeric attributes") unless discretised.

**G9 (5). Apriori vs FP-Growth.**
Table: scans (k+1 vs 2), candidates (yes vs none), structure (itemset lists vs FP-tree), memory (low vs higher), speed on dense data (slow vs fast), results (identical).

**G10 (2). What is lift < 1, and what business action follows?**
Negative association — the items substitute for each other; do not promote them together.

**G11 (5). What are closed and maximal frequent itemsets?**
Maximal: frequent with no frequent superset. Closed: frequent with no superset of equal support. Both compress the lattice; closed sets preserve all support information.

**G12 (2). Give three applications of association rule mining.**
Market basket analysis, cross-selling/recommendation, web clickstream analysis (also medical rules, fraud detection).

**G13 (2). What is the worst-case complexity of Apriori?**
Exponential — up to 2^d candidate itemsets for d items; pruning makes it practical.

**G14 (5). How would you mine rules from a table with numeric attributes like age and income?**
Discretise them into intervals (equal-width, equal-frequency, or entropy-based) so each becomes nominal, then apply Apriori; report the binning because it changes the rules.

---

## Section H — Projects

**H1 (5). Frame the churn problem.**
Binary classification, target churn ∈ {Yes,No}, features from history before the event; imbalanced classes → report precision/recall/F1/ROC-AUC, not accuracy.

**H2 (5). Why is accuracy misleading for churn, and which metric do you optimise?**
If 10% churn, "nobody churns" is 90% accurate; optimise **recall** at acceptable precision, because a missed churner is lost revenue while a false alarm costs a discount.

**H3 (10). Describe the full churn pipeline.**
Framing → collection → cleaning → encoding → scaling → imbalance handling (class weights/resampling) → stratified split → model (logistic regression baseline, then tree/forest) → evaluation (confusion matrix, P/R/F1, ROC) → ranking and retention action.

**H4 (10). How did XYZ Mart preprocess its data, and why does it matter?**
Cleaning (duplicates, returns, missing demographics); aggregation to customer level (RFM, basket size, category share); transformation (log for skewed spend, then standardisation); encoding demographics; reduction (drop correlated features, optional PCA); outlier treatment (cap wholesale buyers). It matters because clustering has no labels to correct it — the distance it is given *is* the model, so unscaled or unaggregated data produces meaningless segments.

**H5 (10). Explain XYZ Mart's clustering and how k was chosen.**
K-means: k centroids, assign by Euclidean distance, recompute means, repeat to convergence, profile the segments. k chosen by elbow (SSE corner), silhouette (maximum), business usability (3–6 actionable segments), minimum segment size, stability across seeds, and interpretability of each profile.

**H6 (5). Market basket: state the pipeline and two business actions.**
Transactions as t/f → clean (remove returns, near-universal items) → thresholds → Apriori/FP-Growth → filter by lift → actions: place associated items together / bundle; avoid promoting substitutes (lift < 1).

**H7 (5). Your market basket has 9 transactions and lift 1.07 — what do you conclude?**
The association is barely above chance and the sample is far too small to justify a business decision; a real analysis needs thousands of baskets and a support threshold reported alongside its count.

---

## Section I — Code reading (2–5 marks each)

**I1.** What does `df.select_dtypes(include="number")` return, and why is it used? → Only numeric columns, because IQR cannot be computed on text.

**I2.** What does `df[col].quantile(0.25)` compute, and how does it treat NaN? → Q1; NaNs are skipped by default (`skipna=True`).

**I3.** Explain `df[(df[col] < lower) | (df[col] > upper)][col]`. → Boolean mask for values outside the fences, filtered frame, single column kept.

**I4.** Explain `(sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5`. → Sample standard deviation with Bessel's correction.

**I5.** Explain `sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)`. → Linear interpolation between the two neighbouring order statistics — the percentile definition pandas/numpy use.

**I6.** Explain `if itemset <= t` for frozensets. → Subset test: every element of `itemset` appears in transaction `t`.

**I7.** Explain `dists.index(min(dists))`. → Index of the nearest centroid = the cluster assignment.

**I8.** Explain `model.inertia_`. → Within-cluster sum of squared distances (SSE).

**I9.** Explain `combinations(sorted(prev, key=sorted), 2)` in Apriori. → Enumerates pairs of frequent (k−1)-itemsets for the join step.

**I10.** Explain `all(frozenset(sub) in current for sub in combinations(union, k-1))`. → The prune step: the candidate survives only if all its (k−1)-subsets are frequent.

**I11.** Explain `df.corr(numeric_only=True)[TARGET].drop(TARGET)`. → Correlations with the target, with the self-correlation removed so the ranking is meaningful.

**I12.** Why `n_init=10` in scikit-learn's KMeans? → It runs the algorithm ten times from different seeds and keeps the lowest-SSE result, reducing the chance of a bad local optimum.

**I13.** Why `random_state=0`? → Reproducibility: the same seed gives the same initialisation and therefore the same result.

**I14.** Why is `init="k-means++"` better than random initialisation? → It spreads the initial centroids out, which empirically gives lower SSE and fewer bad local minima.

**I15.** Explain `round(x, 2)` in the notebook's centroid update. → Display rounding only; applying it between iterations would introduce a small error and can change convergence.
