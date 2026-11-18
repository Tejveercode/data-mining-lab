# 03 — Experiment 3: WAP to check for missing values and outliers

> **Aim.** To write a program that checks a dataset for missing values and detects outliers.
>
> **Course outcomes.** CO2 (analyse data pre-processing techniques).
>
> **Programs.** `code/exp3_missing_outliers.py` (plain Python, no libraries — verified, runs on any lab machine) and the pandas version in `code/pandas/exp3_pandas.py` (the version in your notebook).

## 1. The theory in eight lines

Real datasets are incomplete. A **missing value** is a cell with no recorded value; in a CSV it appears as an empty field, and pandas reads it as `NaN` (not a number). A **noise value** is a recorded value that is wrong; in a CSV it appears as a normal number. An **outlier** is a value that lies far outside the pattern of the rest of the column — it may be noise (a data-entry error) or a genuine extreme case (a blockbuster film).

Missing values and outliers are different problems with different fixes, and this is the distinction the examiner probes:

| | Missing value | Outlier |
|---|---|---|
| Looks like | empty cell / `NaN` | a number, but an extreme one |
| Detected by | counting nulls | IQR fence, z-score, boxplot, distance |
| Fixed by | delete, mean/median/mode impute, regression, KNN impute, flag | delete, cap/winsorise, bin, transform, model separately, keep |
| Danger of the fix | imputation invents information | deleting a real extreme case destroys the signal |

## 2. The two detection methods (formulas you must be able to write)

### IQR method (Tukey's fences)

Order the column, then:

```
Q1 = 25th percentile      Q3 = 75th percentile      IQR = Q3 − Q1
lower fence = Q1 − 1.5 × IQR
upper fence = Q3 + 1.5 × IQR
```

Any value **below the lower fence or above the upper fence is an outlier**. `1.5` is Tukey's convention: for roughly normal data the fences sit about 2.7 standard deviations from the mean, so only about 0.7% of a normal sample is flagged. `3.0` gives "far out" fences for extreme outliers.

**Percentile by hand** (needed in the paper exam): with `n` sorted values, the k-th percentile sits at position `p = (n − 1) × k/100`. With `n = 10` and k = 25, `p = 2.25`, so Q1 = value at index 2 + 0.25 × (value at index 3 − value at index 2) — 0-based indices, which is what Python, pandas and Excel's `QUARTILE.INC` all do.

### Z-score method

```
z = (x − mean) / standard deviation        outlier if |z| > 3  (2 is "mild")
```

It answers a different question: *how many standard deviations from the mean is this value?* `z = +3.99` (Baahubali 2's votes in our data) means "four standard deviations above average".

**The trade-off the viva wants:**

| | IQR | Z-score |
|---|---|---|
| Assumes a distribution | no — it is rank-based | yes — roughly normal |
| Robust to existing outliers | yes, because Q1/Q3 are not pulled by extremes | **no** — the outlier inflates the std-dev that is supposed to catch it |
| Best for | skewed data, small samples | symmetric, roughly normal data |
| Gives | a yes/no flag | a distance, so it can rank |

Saying "I used IQR because the `votes` column is heavily right-skewed, and a mean-based method would be dragged by the very films I am trying to detect" is a complete viva answer.

## 3. The program, line by line

`code/exp3_missing_outliers.py` is written without pandas so it cannot fail on a machine that lacks it. The parts:

```python
def column(rows, name):
    out = []
    for r in rows:
        v = r[name].strip()
        out.append(float(v) if v != "" else None)   # blank -> None (the missing value)
    return out
```

```python
def quantile(sorted_vals, q):
    n = len(sorted_vals)
    pos = (n - 1) * q            # position of the percentile
    lo = int(pos)                # index below
    hi = min(lo + 1, n - 1)      # index above (clamped at the end)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)
```

That is **linear interpolation**, exactly what `pandas.quantile()` and `numpy.percentile()` do by default. Being able to write these five lines is the difference between "I used a library" and "I understand the method".

```python
q1 = quantile(vals, 0.25); q3 = quantile(vals, 0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr; upper = q3 + 1.5 * iqr
found = [v for v in pairs if v < lower or v > upper]
```

and for the z-score:

```python
z = (v - mean(vals)) / stdev(vals)     # sample std-dev: divide by (n-1)
```

## 4. Verified output (run it yourself)

Dataset: `code/datasets/movies.csv`, 21 films, with three blank cells planted on purpose.

```
SECTION 1 - MISSING VALUES
  rating                 0 missing   ( 0.0% of 21 rows)
  votes                  1 missing   ( 4.8% of 21 rows)
  box_office_crore       2 missing   ( 9.5% of 21 rows)
  screens                0 missing   ( 0.0% of 21 rows)
  TOTAL                  3 missing   ( 3.6% of all cells)
  rows with a blank: Sultan -> box_office_crore
                     Chhichhore -> votes
                     Dream Girl -> box_office_crore

SECTION 2 - FIVE-NUMBER SUMMARY
  column             count      min       Q1   median        Q3       max     mean
  rating                21     2.50     5.00     7.00      8.00      8.40     6.52
  votes                 20 12000.00 25000.00 42500.00 105000.00 1000000.00
  box_office_crore      19    98.00   290.00   379.00    586.50   2020.00  565.11
  screens               21  2200.00  3000.00  3900.00   4200.00   6500.00 3804.76

SECTION 3 - IQR
  votes     Q1 = 25000   Q3 = 105000   IQR = 80000
            fences = [-95000, 225000]
            OUTLIER (HIGH) 3 Idiots       = 300000
            OUTLIER (HIGH) Baahubali 2    = 1000000
  rating    no outliers
  screens   OUTLIER (HIGH) Baahubali 2    = 6500   fences = [1200, 6000]

SECTION 4 - Z-SCORE (|z| > 2)
  votes     mean = 119600   std = 220778
            OUTLIER Baahubali 2 = 1000000   z = +3.988
  rating    OUTLIER Student of the Year 2 = 2.5   z = -2.123
  screens   OUTLIER Baahubali 2 = 6500      z = +2.988
```

Four things to notice, because each is an exam question:

1. **The two methods disagree on `votes` at count level.** IQR flags both 3 Idiots (300 000) and Baahubali 2 (1 000 000); the z-score only flags Baahubali 2, because the huge standard deviation (220 778, itself inflated by Baahubali) pulls 3 Idiots inside the ±3 band. This is the classic argument for IQR on skewed data.
2. **`rating` is flagged by z-score but not by IQR.** `Student of the Year 2` at 2.5 is a genuinely low but plausible rating; the IQR fences (0.5 → 12.5) correctly refuse to call it an outlier.
3. **A negative lower fence is fine.** `votes` cannot be negative, so the lower fence of −95 000 simply means "no low outliers possible". Say that out loud in the viva; students often think a negative fence is an error.
4. **`box_office_crore` has count 19, not 21**, because two cells are blank — the missing values change the count, and therefore Q1/Q3. Missing values and outliers interact, and the record should mention it.

## 5. The pandas version (your notebook, corrected)

Your notebook's program, tidied. Functionally identical; the corrections are noted underneath.

```python
import pandas as pd

df = pd.read_csv("datasets/movies.csv")
df.info()                                   # column types + non-null counts

print("\nOutliers in numerical columns:")
num_f = df.select_dtypes(include=["float64", "int64"]).columns
for col in num_f:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)][col]
    print(f"\nColumn: {col}   Q1={Q1:.2f} Q3={Q3:.2f} IQR={IQR:.2f} "
          f"fences=[{lower:.2f}, {upper:.2f}]  outliers={len(outliers)}")
    print(outliers.to_string())

print("\nMissing values per column:")
print(df.isnull().sum())
print(f"\nTotal missing: {df.isnull().sum().sum()} of {df.size} cells")
print(f"Rows with any missing value: {df.isnull().any(axis=1).sum()}")
```

What each line does, in the words you would use in the viva:

| Line | Meaning |
|---|---|
| `pd.read_csv(...)` | reads the CSV; empty cells and the strings `NA`, `NaN`, `null` become `NaN` |
| `df.info()` | prints each column's dtype and non-null count — the fastest missing-value check |
| `select_dtypes([...])` | keeps numeric columns only; you cannot compute an IQR on a text column |
| `.quantile(0.25)` | Q1; pandas **skips NaN** by default (`skipna=True`) |
| `df[(df[col] < lower) \| (df[col] > upper)]` | boolean mask: keeps rows outside either fence |
| `[col]` at the end | keeps only that column, so the printout is one number per outlier |
| `df.isnull().sum()` | counts NaN per column |
| `df.isnull().any(axis=1)` | `True` for a row that has at least one NaN |

**Three corrections to the notebook version, and why they matter:**

1. **`select_dtypes(include=['float64','int64'])` can miss a column.** If an integer column contains one `NaN`, pandas converts it to `float64` — which is included, so this is fine here — but a column of large integers with no NaN stays `int64`, and a column of whole numbers read as `object` (because of a stray space) is skipped silently. Safer: `df.select_dtypes(include="number")`.
2. **`print("Tejveer Singh")` inside the loop** prints your name once per column. Keep it — it is proof the output is yours — but move it to the end, or the output is unreadable.
3. **The file path.** `pd.read_csv("Downloads/...")` fails on any machine but yours. Put the CSV in `datasets/` next to the script and use a relative path; this is the single most common reason a program that "worked at home" fails in the lab.

## 6. What to do after detection (the part students skip)

Detection without a decision is half an answer. In the conclusion, name the treatment:

| Situation | Treatment | pandas one-liner |
|---|---|---|
| Few missing values, random | drop the rows | `df.dropna()` |
| Numeric, symmetric | mean impute | `df[col].fillna(df[col].mean())` |
| Numeric, skewed (our `votes`) | **median** impute | `df[col].fillna(df[col].median())` |
| Categorical | mode impute | `df[col].fillna(df[col].mode()[0])` |
| Meaningful absence | new flag column | `df[col].isnull().astype(int)` |
| Outlier is a data error | correct or delete | `df = df[df[col] <= upper]` |
| Outlier is genuine | cap at the fence (winsorise) | `df[col].clip(lower, upper)` |
| Outlier is the phenomenon | keep it, model separately | — |

For our data: `box_office_crore` and `votes` are right-skewed, so median imputation is defensible; Baahubali 2 is a real blockbuster, so capping its votes at 225 000 or keeping it with a note are both correct — deleting it silently is not.

## 7. Write this on paper

> **Aim.** To write a program to check a dataset for missing values and to detect outliers using the IQR and z-score methods.
>
> **Theory.** A dataset is said to be incomplete when some attribute values are absent; such values are represented as NaN and must be handled before mining, because most algorithms cannot process them. An outlier is an observation that deviates so much from the other observations as to arouse suspicion that it was generated by a different mechanism (Hawkins). Two standard detection methods are used. The IQR method orders the values, computes Q1 (25th percentile), Q3 (75th percentile) and IQR = Q3 − Q1, and flags any value outside [Q1 − 1.5·IQR, Q3 + 1.5·IQR]; it is robust because quartiles are not affected by extreme values. The z-score method standardises each value as z = (x − μ)/σ and flags values with |z| > 3; it assumes an approximately normal distribution, and σ itself is inflated by the outlier it is meant to detect, which makes it weaker on skewed data.
>
> **Algorithm.**
> 1. Import the required library (pandas) or open the CSV file.
> 2. Load the dataset.
> 3. Display the first few records and the dataset information to see types and non-null counts.
> 4. Display the statistical summary (count, mean, std, min, quartiles, max).
> 5. Select the numerical columns.
> 6. For each numerical column compute Q1 and Q3.
> 7. Compute IQR = Q3 − Q1.
> 8. Compute lower = Q1 − 1.5·IQR and upper = Q3 + 1.5·IQR.
> 9. Select the values below lower or above upper; these are the outliers.
> 10. Display the detected outliers.
> 11. Compute the missing-value count for every column.
> 12. Analyse the results and state the treatment to be applied.
>
> **Output.** (paste the real run) `votes` has 1 missing value, `box_office_crore` 2; IQR flags 3 Idiots and Baahubali 2 in `votes`, z-score flags Baahubali 2 with z = 3.99.
>
> **Result.** Missing values and outliers were detected successfully. The skewness of the `votes` column makes the IQR method more reliable than the z-score method for this dataset.

**Numerical drill** (this exact style appears in the paper exam). For the ten values
`12, 15, 14, 10, 18, 22, 13, 16, 90, 15`:

- sorted: `10, 12, 13, 14, 15, 15, 16, 18, 22, 90`, n = 10
- Q1 at position (10−1)×0.25 = 2.25 → 13 + 0.25×(14−13) = **13.25**
- Q3 at position (10−1)×0.75 = 6.75 → 16 + 0.75×(18−16) = **17.5**
- IQR = 17.5 − 13.25 = **4.25**
- lower = 13.25 − 6.375 = **6.875**, upper = 17.5 + 6.375 = **23.875**
- **90 is an outlier** (greater than 23.875); every other value lies inside the fences.
- mean = 22.5, sample std = 23.36, z(90) = (90 − 22.5)/23.36 = **+2.89** — just under the |z| > 3 rule, which is exactly the point: the IQR catches it, the z-score at threshold 3 does not.

## 8. Viva questions for Experiment 3

**Q: What is a missing value?**
An attribute value that is not recorded for an instance. It is not zero and not an empty string — it is unknown, and treating it as zero changes the mean.

**Q: Why is `NaN` a float in pandas and not a string?**
Because pandas uses IEEE-754 floating-point NaN, which propagates correctly through arithmetic, and every numeric column can hold it without changing dtype to object.

**Q: What is an outlier?**
A value that deviates so much from the rest of the data that it is suspected of coming from a different mechanism. It can be an error or a genuine extreme.

**Q: Why 1.5 in the IQR rule?**
It is Tukey's convention: on normal data the fences correspond to about ±2.7σ, flagging ≈0.7% of points as outliers — a balance between missing real extremes and flagging noise.

**Q: What if IQR = 0?**
Q1 = Q3, which happens when more than half the values are identical. Both fences collapse onto that value, and every different value is flagged. Correct response: fall back to the z-score or a domain rule.

**Q: Which method did you use and why?**
IQR, because the `votes` column is strongly right-skewed; the mean and standard deviation are pulled upward by the very extreme values I want to find, so a z-score test is biased against them.

**Q: What does a z-score of 3.99 mean?**
The value lies 3.99 standard deviations above the mean — far outside the expected range of a normal distribution (99.99% of a normal sample lies within ±4σ).

**Q: Why does `box_office_crore` show count 19 while `rating` shows 21?**
Two cells are blank and pandas excludes NaN from `count()`, `quantile()` and `mean()`.

**Q: How do you handle an outlier?**
Delete it if it is a proven error; cap (winsorise) it at the fence; transform the column (log); bin it; or keep it and model it separately. The choice depends on whether it is error or signal, and must be stated.

**Q: Difference between noise and an outlier?**
Noise is a random error in a measured value (small, everywhere); an outlier is an extreme deviation (rare, large). Smoothing handles noise; detection and treatment handle outliers.

**Q: What is the difference between `isnull().sum()` and `isnull().any(axis=1).sum()`?**
The first counts missing cells per column; the second counts **rows** that contain at least one missing cell.

**Q: Can I delete all rows with a missing value?**
Only if the missingness is MCAR (missing completely at random) and the loss is small. Otherwise deletion biases the sample, which is why imputation exists.
