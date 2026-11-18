# Cheat sheet — Data Mining Lab (24CAP-308)

Print this. One page per experiment, formulas first.

---

## THE FORMULA BLOCK (learn this cold)

```
IQR:            IQR = Q3 − Q1
                lower = Q1 − 1.5·IQR        upper = Q3 + 1.5·IQR
                percentile position p = (n − 1) × k/100

Z-score:        z = (x − μ) / σ              outlier if |z| > 3 (2 = mild)

Pearson:        cov(x,y) = Σ(xᵢ−x̄)(yᵢ−ȳ)/(n−1)
                r = cov(x,y) / (σx · σy)     r² = coefficient of determination

Chi-square:     χ² = Σ(O − E)² / E           df = (rows−1)(cols−1)

Euclidean:      d(p,q) = √( Σ(pᵢ − qᵢ)² )

K-means SSE:    SSE = Σⱼ Σ_{x∈Cⱼ} ‖x − μⱼ‖²

Silhouette:     s = (b − a) / max(a, b)      a = intra, b = nearest other cluster

Support:        support(X→Y) = |X ∪ Y| / N
Confidence:     confidence(X→Y) = support(X ∪ Y) / support(X)
Lift:           lift(X→Y) = confidence(X→Y) / support(Y)
Leverage:       support(X∪Y) − support(X)·support(Y)
Conviction:     (1 − support(Y)) / (1 − confidence)

Accuracy  = (TP+TN)/(TP+TN+FP+FN)
Precision = TP/(TP+FP)      Recall = TP/(TP+FN)
F1        = 2PR/(P+R)       MSE = Σ(y−ŷ)²/n    RMSE = √MSE
```

---

## EXPERIMENT 1 — Install Weka

- Weka = **W**aikato **E**nvironment for **K**nowledge **A**nalysis; Java, GPL, University of Waikato.
- Official page: `cs.waikato.ac.nz/ml/weka/downloading.html`; stable **3.8.x**, dev 3.9.x.
- Windows: take the **zulu** build (bundles Java). macOS: `.dmg`. Linux: `.tar.gz` → `java -jar weka.jar`.
- GUI Chooser → **Explorer, Experimenter, KnowledgeFlow, Workbench, Simple CLI**.
- Verify: Explorer opens with 6 tabs and a `data` folder containing `iris.arff`.
- Failure with no message = **no Java**.

---

## EXPERIMENT 2 — Load and visualise

- ARFF = `@relation` → `@attribute` lines → `@data` rows. `%` comment, `?` missing.
- Explorer → **Preprocess → Open file…** → load; panel shows Relation/Instances/Attributes.
- Attribute click → **Missing, Distinct, Type, Unique** + Min/Max/Mean/StdDev.
- CLI: `java weka.core.Instances data/iris.arff` (Simple CLI) or `java -cp weka.jar …` (terminal).
- **Visualize** tab = scatterplot matrix; set **Colour** = class to see separability.
- iris = 150 instances, 5 attributes; weather.nominal = 14 instances, play 9 yes / 5 no.

---

## EXPERIMENT 3 — Missing values and outliers

- Missing = absent (impute/drop). Outlier = extreme (cap/delete/keep). **Different problems.**
- IQR **robust**; z-score **mean-based, assumes normal, weakened by the outlier itself**.
- pandas: `read_csv` → `info` → `describe` → `select_dtypes("number")` → `quantile(.25/.75)` → fences → mask → `isnull().sum()`.
- 1.5 in the fence rule = Tukey's constant ≈ ±2.7σ on normal data (≈0.7% flagged).
- Negative lower fence is normal when the column cannot be negative.
- Blank cells reduce `count()` — so missing values change Q1/Q3.

---

## EXPERIMENT 4 — Patterns and correlations

- `r = cov/(σx·σy)`, range −1…+1, **linear only**, sensitive to outliers, **not causation**.
- 0.9–1.0 very strong · 0.7–0.9 strong · 0.4–0.7 moderate · <0.2 negligible.
- Redundancy: two predictors with |r| ≈ 1 → drop one (multicollinearity).
- Weka: **Select attributes** → `CorrelationAttributeEval` + `Ranker` → Start.
- Nominal class → **χ²** (`ChiSquaredAttributeEval`), p < 0.05 = dependent.
- Verified: study_hours 0.9979, attendance 0.9970, sleep −0.2120; study↔attendance 0.9935 (redundant).

---

## EXPERIMENT 5 — K-means

```
1 choose k  2 initial centroids  3 assign to nearest  4 recompute means
5 repeat until no change        6 output clusters
```
- Notebook data: {(1,2),(2,1),(1,1)} + {(8,9),(9,8),(8,8)}; centroids (1.3333,1.3333)/(8.3333,8.3333); **SSE 2.6667**, converged in **2 iterations**.
- Elbow: k=1 → 149.6667, k=2 → 2.6667, k=3 → 1.8333, k=4 → 1.0000 → **k = 2**.
- Always converges, but to a **local** minimum → depends on initial centroids (k-means++ / n_init).
- K-medoids (PAM) = robust to outliers because the centre is a real point.
- Must scale first; fails on non-convex shapes (use DBSCAN).
- Your notebook bug: **`d2` used before assignment → `NameError`**.

---

## EXPERIMENT 6 — Apriori

```
1 minsup/minconf  2 count items  3 L1  4 join → prune → count → Lk  5 repeat
6 generate rules from itemsets  7 keep conf ≥ minconf
```
- Apriori property: infrequent itemset ⇒ all supersets infrequent.
- 4-transaction data at minsup 0.5: L1 milk 4, bread 3, butter 2, diapers 2; L2 {bread,milk} 3, {bread,butter} 2, {butter,milk} 2, {diapers,milk} 2; L3 {bread,butter,milk} 2 → **11 rules**.
- Best rule: `{butter} → {bread}` support 0.5, confidence 1.0, **lift 1.3333**.
- milk rules have **lift 1.0** (milk is in 100% of baskets) → useless.
- minsup 0.2 on 4 rows = **0.8 transactions = count 1** → no pruning, 16 rules.
- Weka: Associate tab → Apriori → `minSupport 0.2`, `metricType Confidence`, `minMetric 0.8`.
- Apriori = k+1 scans + candidates; FP-Growth = 2 scans, no candidates, same results.

---

## NUMBERS TO REMEMBER

| Fact | Value |
|---|---|
| iris | 150 instances, 5 attributes |
| weather.nominal | 14 instances, 5 attributes |
| K-means notebook SSE | 2.6667, 2 iterations |
| K-means elbow drop k1→k2 | 147.0000 |
| retail L1 at minsup 0.5 | milk 4, bread 3, butter 2, diapers 2 |
| best retail rule lift | 1.3333 |
| rules at 0.5/0.6 | 11 |
| rules at 0.2/0.8 | 16 |
| correlation demo | r = 0.9979, r² = 0.9958 |
| IQR drill | Q1 8, Q3 19, IQR 11, fences −8.5 / 35.5 |

---

## THE SIX SENTENCES THAT SAVE ANY ANSWER

1. "The formula is …, substituting the values gives …"
2. "I used IQR rather than the z-score because the column is skewed."
3. "This threshold is meaningless without the number of rows — 0.2 of 4 is one transaction."
4. "Correlation is not causation; this sample is too small to conclude."
5. "K-means finds a local optimum, which is why the initial centroids matter."
6. "Detection is only half the task; the treatment is …"
