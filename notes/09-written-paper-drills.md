# 09 — The written paper: formulas, numericals and model answers

The written part is not a coding test. It asks four kinds of question, and each has a fixed shape of answer. This note gives the shape, then nine fully solved numericals — every number below was computed and checked, so you can trust it as the model answer.

---

## The four question types

| Type | Typical wording | Marks | What earns them |
|---|---|---|---|
| Aim + theory | "Write the aim and theory of Experiment X" | 5 | definition + formula + one line on why the method works |
| Algorithm/steps | "Write the algorithm/procedure" | 5 | numbered steps in the right order, no code |
| Formula + numerical | "Compute the outliers / support / r" | 5–10 | formula written first, substitution shown, boxed answer |
| Short answer | "Define…", "Differentiate…", "What happens if…" | 2 each | one precise sentence, no filler |

**The rule that decides most marks:** write the formula **before** substituting numbers. An examiner marking 60 scripts looks for the formula line; if it is there and the arithmetic slipped, you still get most of the marks. If it is missing, the whole answer looks guessed.

---

## Numerical 1 — IQR fences

**Question.** For the data `4, 8, 15, 16, 23, 42, 8, 4, 12, 20`, find Q1, Q3, IQR and both fences, and identify the outliers.

**Solution.**

```
Sorted: 4, 4, 8, 8, 12, 15, 16, 20, 23, 42      n = 10
Position of a percentile: p = (n − 1) × k/100

Q1: p = 9 × 0.25 = 2.25  ->  8 + 0.25 × (8 − 8) = 8
Q3: p = 9 × 0.75 = 6.75  -> 16 + 0.75 × (20 − 16) = 19

IQR = Q3 − Q1 = 19 − 8 = 11
lower fence = 8 − 1.5 × 11 = −8.5
upper fence = 19 + 1.5 × 11 = 35.5
```

**Answer: Q1 = 8, Q3 = 19, IQR = 11, fences = (−8.5, 35.5); 42 is an outlier.**

Note the two things a full-marks answer adds: (a) the position formula `p = (n−1)k/100`, so the quartile is not a guess; (b) the observation that the lower fence is negative, which simply means no low outliers are possible here (not an error).

---

## Numerical 2 — z-score on the same data

**Question.** For the same ten values, compute the z-score of 42 and decide whether it is an outlier at |z| > 2 and at |z| > 3.

**Solution.**

```
mean = (4+4+8+8+12+15+16+20+23+42)/10 = 152/10 = 15.2

deviations:  −11.2, −11.2, −7.2, −7.2, −3.2, −0.2, 0.8, 4.8, 7.8, 26.8
squared:      125.44, 125.44, 51.84, 51.84, 10.24, 0.04, 0.64, 23.04, 60.84, 718.24
Σ squares  = 1167.6
sample variance = 1167.6 / 9 = 129.7333
σ = √129.7333 = 11.3901

z(42) = (42 − 15.2) / 11.3901 = 26.8 / 11.3901 = +2.3529
```

**Answer: z = +2.35, so 42 is an outlier at the |z| > 2 threshold but not at |z| > 3.**

This is the exam's favourite contrast: **IQR catches 42, the strict z-score rule does not** — because σ is itself inflated by the very value being tested. Quote that sentence and the examiner knows you understand the method rather than the recipe.

---

## Numerical 3 — Pearson correlation

**Question.** For x = 2, 4, 6, 8, 10 and y = 5, 9, 12, 16, 18, compute the correlation coefficient and interpret it.

**Solution.**

```
x̄ = 30/5 = 6          ȳ = 60/5 = 12
x − x̄ :  −4, −2, 0, 2, 4
y − ȳ :  −7, −3, 0, 4, 6
products: 28, 6, 0, 8, 24   ->  Σ = 66
cov(x,y) = 66 / (5 − 1) = 16.5

σx = √(40/4) = √10     = 3.1623
σy = √(110/4) = √27.5  = 5.2440

r = 16.5 / (3.1623 × 5.2440) = 16.5 / 16.5834 = 0.9950
r² = 0.9900
```

**Answer: r = 0.9950 — a very strong positive linear relation; 99% of the variation in y is explained by the linear relation with x.**

---

## Numerical 4 — Support, confidence, lift

**Question.** Five transactions: T1 = {A,B,C}, T2 = {A,C}, T3 = {A,B}, T4 = {B,C}, T5 = {A,B,C}. With minimum support 0.4, find the frequent itemsets and the strong rules at minimum confidence 0.6, and comment on lift.

**Solution — itemset counts.**

```
support(A) = 4/5 = 0.8      support(B) = 0.8      support(C) = 0.8
support(A,B) = 3/5 = 0.6    support(A,C) = 0.6    support(B,C) = 0.6
support(A,B,C) = 2/5 = 0.4
```

All survive minsup 0.4: L1 = {A,B,C} (each 0.8), L2 = {AB, AC, BC} (each 0.6), L3 = {ABC} (0.4).

**Rules at minconf 0.6:**

| rule | support | confidence = sup(X∪Y)/sup(X) | lift = conf/sup(Y) |
|---|---|---|---|
| A → B | 0.6 | 0.6/0.8 = 0.75 | 0.75/0.8 = **0.9375** |
| A → C | 0.6 | 0.75 | 0.9375 |
| B → A | 0.6 | 0.75 | 0.9375 |
| B → C | 0.6 | 0.75 | 0.9375 |
| C → A | 0.6 | 0.75 | 0.9375 |
| C → B | 0.6 | 0.75 | 0.9375 |
| A,B → C | 0.4 | 0.4/0.6 = 0.6667 | 0.6667/0.8 = **0.8333** |
| A,C → B | 0.4 | 0.6667 | 0.8333 |
| B,C → A | 0.4 | 0.6667 | 0.8333 |

**Answer: 9 strong rules.** All of them have **lift < 1**, which is the point of the question: confidence 0.75 looks respectable, but every item already appears in 80% of transactions, so a rule pointing at one is *less* likely than the base rate. The complete remark: *"lift < 1 means negative association; the items substitute for one another in this dataset, so these rules should not be used for cross-selling."*

If you want an example where lift exceeds 1, use the retail 4-transaction data: `{butter} → {bread}` has support 0.5, confidence 1.0, lift 1.3333.

---

## Numerical 5 — One K-means iteration

**Question.** Points (2,2), (3,2), (6,6), (7,7) with initial centroids C1 = (2,2), C2 = (8,8). Perform one iteration and give the new centroids.

**Solution.**

| point | d to C1 | d to C2 | cluster |
|---|---|---|---|
| (2,2) | √(0+0) = 0.0000 | √(36+36) = 8.4853 | C1 |
| (3,2) | √(1+0) = 1.0000 | √(25+36) = 7.8102 | C1 |
| (6,6) | √(16+16) = 5.6569 | √(4+4) = 2.8284 | C2 |
| (7,7) | √(25+25) = 7.0711 | √(1+1) = 1.4142 | C2 |

```
C1 = ((2+3)/2, (2+2)/2) = (2.5, 2.0)
C2 = ((6+7)/2, (6+7)/2) = (6.5, 6.5)
```

**Answer: C1 = {(2,2), (3,2)} with centroid (2.5, 2.0); C2 = {(6,6), (7,7)} with centroid (6.5, 6.5).** In the next iteration both points of each cluster stay nearest to their new centroid, so the algorithm terminates.

Show the distance column — that is the mark scheme.

---

## Numerical 6 — Euclidean distance

**Question.** Compute the Euclidean distance between (1,2) and (10,10), and between (1,2) and (1,0).

```
d((1,2),(10,10)) = √((1−10)² + (2−10)²) = √(81 + 64) = √145 = 12.0416
d((1,2),(1,0))   = √(0 + 4) = 2.0000
```

**Answer: 12.0416 and 2.0000.** State the formula before substituting, and keep four decimals — the examiner is checking the arithmetic, so inconsistent rounding looks careless.

---

## Numerical 7 — Writing an ARFF file

**Question.** Convert the CSV `age,income,bought` / `25,30000,yes` / `40,55000,no` into ARFF, declaring the types you choose and justifying them.

```arff
@relation customer
@attribute age numeric
@attribute income numeric
@attribute bought {yes,no}
@data
25,30000,yes
40,55000,no
```

A full-marks justification: *"age and income are numeric because arithmetic and distance are meaningful on them; bought is nominal because it is a two-value label with no order, and declaring it `{yes,no}` lets Weka treat it as a class."*

---

## Numerical 8 — Steps of an experiment (5-mark template)

**Question.** Write the procedure to check a CSV file for missing values and outliers.

```
1. Import pandas and load the dataset with pd.read_csv().
2. Inspect the first rows with head() and the structure with info()
   (info() shows the non-null count of every column).
3. Obtain the statistical summary with describe().
4. Select the numerical columns with select_dtypes().
5. For each numerical column compute Q1 = quantile(0.25) and Q3 = quantile(0.75).
6. Compute IQR = Q3 − Q1.
7. Compute lower = Q1 − 1.5·IQR and upper = Q3 + 1.5·IQR.
8. Select the values outside [lower, upper] — these are the outliers.
9. Display the outliers column by column.
10. Count the missing values with isnull().sum().
11. State the treatment (impute or drop; cap, delete or keep) and conclude.
```

Steps 5–8 are the ones that must be in this order. A "procedure" answer that says "find the outliers" without the four arithmetic steps earns half.

---

## Numerical 9 — Two-mark short answers (memorise these exact sentences)

**Define data pre-processing.** The set of techniques that transform raw data into a clean, consistent, compact and usable form before mining: cleaning, integration, reduction and transformation.

**Define an outlier.** An observation that deviates so much from other observations as to arouse suspicion that it was generated by a different mechanism.

**Define support.** The fraction of all transactions that contain the itemset X ∪ Y.

**Define confidence.** The fraction of transactions containing X that also contain Y; support(X∪Y)/support(X).

**Define lift.** Confidence(X→Y) divided by support(Y); the factor by which the rule improves on the base rate.

**Define clustering.** The unsupervised partitioning of objects into groups whose members are more similar to each other than to members of other groups.

**Define a centroid.** The mean vector of the points assigned to a cluster.

**What is the Apriori property?** If an itemset is infrequent, every superset of it is also infrequent, so supersets can be pruned without counting.

**What is ARFF?** Weka's Attribute-Relation File Format: a relation declaration, attribute declarations with types, and comma-separated data rows.

**What is the elbow method?** Plotting the within-cluster SSE against k and choosing the k at which the decrease flattens.

**Difference between classification and clustering.** Classification is supervised and predicts a known label; clustering is unsupervised and discovers groups with no label.

**Difference between noise and an outlier.** Noise is a random error present in all measurements; an outlier is an extreme deviation, present in few.

---

## How to spend the last 20 minutes before the paper

1. Read the cheat sheet's formula block once.
2. Re-do Numerical 1 and Numerical 4 from memory on blank paper. Those two types appear most often and carry the most marks.
3. Write the six-step K-means algorithm and the seven-step Apriori procedure from memory.
4. Stop. Cramming new material in the last ten minutes replaces things you already know.
