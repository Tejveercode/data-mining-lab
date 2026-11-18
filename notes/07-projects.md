# 07 — The projects: churn, market basket, and the XYZ Mart case

The syllabus lists two projects and one project-based-learning case. They are examined as a **mini project (5 marks)** and they are the easiest marks in the course, because the questions are known in advance. This note gives the full answer for each, plus the exact sentences to say.

---

## Project 1 — Customer Churn Prediction

> **Goal:** predict which customers are likely to churn based on historical data.
> **Dataset:** customer data including purchase history, frequency of interaction and customer service history.

### What churn prediction is

**Churn** is a customer leaving (cancelling a subscription, closing an account, not renewing). Churn prediction is a **binary classification** problem: the target is `churn ∈ {Yes, No}`, the features are the customer's history, and the output is a probability per customer that is then turned into a retention action.

Why it is a classification problem and not a clustering problem: the label exists in the historical data. That one sentence answers the most likely viva question.

### The pipeline, in the order you should present it

| Step | What you do | Why |
|---|---|---|
| 1. Problem framing | target = churn, positive class = "will leave" | defines what accuracy means |
| 2. Data collection | tenure, monthly charges, support calls, contract type, payment method, usage | features must exist *before* the churn event |
| 3. Cleaning | missing values, duplicate customers, impossible values (negative tenure) | garbage in, garbage out |
| 4. Encoding | `contract` → one-hot; `Yes/No` → 0/1 | algorithms need numbers |
| 5. Scaling | z-score for numeric features | distance/gradient methods need comparable ranges |
| 6. Class imbalance | churn is usually 5–20% of customers | accuracy becomes misleading; use precision/recall/F1 |
| 7. Split | 70/30 or 80/20, **stratified** | keeps the churn rate in both parts |
| 8. Model | logistic regression (interpretable) or decision tree / random forest | baseline first |
| 9. Evaluate | confusion matrix, precision, recall, F1, ROC-AUC | recall matters most: missing a leaver costs revenue |
| 10. Act | rank customers by predicted probability, target the top decile | a model that is not used is not a project |

### The metric argument (this is what earns the marks)

With 10% churn, a model that predicts "nobody churns" is **90% accurate and completely useless**. So:

- **Recall** = of the customers who actually left, how many did we catch? This is the business-critical number, because a missed leaver is lost revenue.
- **Precision** = of the customers we flagged, how many really left? This controls the cost of the retention offer.
- **F1** balances the two; **ROC-AUC** measures ranking quality independent of the threshold.

Say: *"I optimise recall at an acceptable precision, because a retention campaign can afford some false alarms but not missed churners."*

### A worked example on the included data

`code/datasets/churn.csv` has 20 customers. Reading it directly:

- 9 of 20 churned → **base rate 45%** (deliberately high so the numbers are visible in a small file).
- Every churner has `contract = monthly`; no `two_year` customer churned.
- Churners average far more `support_calls` (4–8) than non-churners (0–2).
- Churners have short tenure (1–9 months); non-churners 12–60 months.

So the two strongest features are **contract type** and **support calls**, and a one-line rule already performs well:

```
IF contract = monthly AND support_calls >= 4 THEN churn = Yes
```

That rule is a decision tree of depth 2, and it is the honest baseline any fancier model must beat. Presenting it first, then a logistic regression, then comparing them, is exactly the structure a good project report has.

### The five sentences to say in the viva

1. "Churn prediction is binary classification because the historical data contains the label."
2. "The dataset is imbalanced, so accuracy is not the right metric; I report precision, recall, F1 and ROC-AUC."
3. "I use a stratified train/test split so the churn rate is the same in both parts."
4. "Recall is the priority, because a missed churner is lost revenue, while a false alarm only costs a discount."
5. "The output is a ranked list of customers by churn probability, which the retention team works down from the top."

---

## Project 2 — Market Basket Analysis

> **Goal:** identify products that are frequently bought together.
> **Dataset:** transaction data from a retail store.

### What it is

Market basket analysis is **association rule mining** on transactions: each row is a basket, each column an item, and the output is rules like `{bread, butter} → {milk}` with support, confidence and lift. It is the direct application of Experiment 6, which is why the two are examined together.

### The pipeline

| Step | What you do |
|---|---|
| 1. Collect transactions | one row per basket, one column per item, `t/f` or 0/1 |
| 2. Clean | remove returns, internal items, and items present in > 90% of baskets (they generate useless rules) |
| 3. Choose thresholds | support 0.01–0.05, confidence 0.5–0.6 for a real store |
| 4. Run Apriori (or FP-Growth) | get frequent itemsets, then rules |
| 5. Filter by lift | keep lift > 1; sort by lift, not by confidence |
| 6. Act | shelf placement, bundles, cross-sell recommendations, promotions |

### The three business actions, with the rule that justifies each

| Rule found | Action |
|---|---|
| `{diapers} → {beer}` (the classic) | place them near each other, or promote together |
| `{bread} → {butter}` high lift | bundle pricing; put butter at the end of the bread aisle |
| `{brand A} → {brand B}` lift < 1 | they are substitutes — do **not** promote together, they cannibalise |

That last row is the answer to "what if lift is less than 1?" and it is the one students forget.

### On the included data

`code/datasets/market_basket.csv` (9 transactions, 6 items) with support 4/9 and confidence 0.6 gives exactly two rules: `{bread} → {milk}` (support 0.5556, confidence 0.8333, lift 1.0714) and `{milk} → {bread}` (support 0.5556, confidence 0.7143, lift 1.0714). The lift of 1.07 is barely above chance — the honest conclusion is that 9 transactions are too few to support a business decision, and that a real analysis needs thousands. Saying that is a strength, not a weakness.

---

## The project-based-learning case: XYZ Mart customer segmentation

> **Background.** A retail company, XYZ Mart, wanted to segment its customers into distinct groups based on purchasing behaviour and demographic characteristics, in order to improve its marketing strategy.

The syllabus asks two questions about it. Both are answered below in the form you would write.

### Question 3 — How did XYZ Mart preprocess the transactional data, and why does preprocessing matter?

**Answer.** Preprocessing is the step that turns raw transactional records into a matrix a clustering algorithm can use. For XYZ Mart it has six parts:

1. **Data cleaning.** Remove duplicate transactions, cancelled and returned orders, and test entries. Handle missing demographic fields (age, income) by median/mode imputation or by excluding those customers, and treat extreme basket values (a ₹5 lakh purchase) as outliers to be capped or examined.
2. **Aggregation to the customer level.** Transactions are not customers. Each customer is reduced to features: **recency** (days since last purchase), **frequency** (number of purchases), **monetary value** (total spend), average basket size, category share (how much of the spend is groceries vs apparel), and tenure. This is the RFM transformation, and it is the single most important preprocessing decision in the case.
3. **Data transformation.** Monetary values are heavily right-skewed, so a log transform is applied; then all features are **standardised** (z-score) or min–max normalised, because K-means uses Euclidean distance and a spend column in thousands would otherwise dominate a frequency column in single digits.
4. **Encoding.** Categorical demographics (gender, city tier, marital status) are one-hot encoded, or handled with K-modes if the analyst prefers to keep them categorical.
5. **Reduction.** Highly correlated features (total spend and average basket value, for instance) are pruned, and PCA may be applied to compress the feature space before clustering.
6. **Outlier treatment.** A few wholesale buyers can pull an entire centroid; they are either capped or clustered separately.

**Why it matters.** Clustering has no labels to correct it, so it can only be as good as the distance it is given. Unscaled data makes the algorithm cluster on spend alone; unaggregated data clusters transactions instead of customers; uncleaned data creates a "cluster" that is nothing but data-entry errors. Preprocessing is what makes the resulting segments *interpretable and actionable* — and interpretability is the entire business purpose of segmentation.

### Question 4 — Explain the clustering algorithm used, and the factors considered in choosing the number of clusters

**Answer.** XYZ Mart used **K-means**, a partitional, centroid-based, unsupervised algorithm:

1. Choose k, the number of segments.
2. Place k initial centroids (k-means++ seeding).
3. Assign each customer to the nearest centroid by Euclidean distance in the standardised feature space.
4. Recompute each centroid as the mean of its customers.
5. Repeat 3–4 until assignments stop changing.
6. Report the segments and their centroids, which are then profiled (e.g. "high-value loyal", "discount-driven occasional", "dormant").

It minimises the within-cluster sum of squared errors, `SSE = Σⱼ Σ_{x∈Cⱼ} ‖x − μⱼ‖²`.

**Factors considered in choosing k:**

1. **The elbow method** — plot SSE against k and take the point where the fall flattens; beyond it, extra clusters buy almost nothing.
2. **Silhouette score** — measures how much closer a customer is to their own cluster than to the nearest other cluster; the k with the highest mean silhouette is preferred.
3. **Business usability** — a marketing team can act on 3–6 segments; 15 segments are statistically fine and operationally useless. This is a real constraint, not an excuse.
4. **Segment size** — a segment of 12 customers out of 50 000 cannot justify a campaign; minimum viable size is a criterion.
5. **Stability** — re-run with different seeds; if the segments change completely, k is wrong or the features are.
6. **Interpretability of the profile** — each segment must be describable in one sentence ("young, high-frequency, low-basket grocery shoppers"). If it is not, the segmentation has failed regardless of the metric.

**The closing sentence for the case:** *"K-means with k = 4 was chosen because the elbow flattened at 4, the silhouette peaked there, and the four resulting segments were each large enough and distinct enough to support a separate marketing campaign."*

---

## How to present any of these in 5 minutes

1. **One sentence of problem framing** (classification or association or clustering, and why).
2. **The data** — rows, columns, target, and one data-quality problem you found.
3. **The method** — the algorithm's name, its objective, and one parameter you chose and why.
4. **The result** — one table or one rule, with the numbers.
5. **The action** — what the business does differently because of it.
6. **The limitation** — sample size, imbalance, or correlation-not-causation.

Six sentences, in that order, is a complete project presentation. Practise it out loud once; it is the difference between "I did a project" and a mark.
