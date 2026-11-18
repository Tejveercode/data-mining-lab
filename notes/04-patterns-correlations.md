# 04 — Experiment 4: Identify potential patterns and correlations

> **Aim.** To identify potential patterns and correlations in a dataset.
>
> **Course outcomes.** CO2 (data pre-processing techniques), CO4 (apply classification/prediction to real data).
>
> **Programs.** `code/exp4_correlation.py` (plain Python) and `code/pandas/exp4_pandas.py`. **Weka route** (your notebook): Select attributes tab with `CorrelationAttributeEval` + `Ranker`.

## 1. What the experiment is really asking

Two different questions hide behind the word "pattern":

- **Correlation** — do two numeric attributes move together, and how strongly? This is a number between −1 and +1.
- **Pattern** — is there a rule that holds for a subgroup? "Every student with marks ≥ 75 studied at least 7 hours" is a pattern; it is not a correlation coefficient.

A complete answer to this experiment gives both: the ranked correlations **and** at least one if-then pattern found by grouping. The note below does exactly that, and the program prints both.

## 2. Pearson correlation, derived

```
cov(x, y) = Σ (xᵢ − x̄)(yᵢ − ȳ) / (n − 1)          covariance: do they deviate together?
σx = √(Σ (xᵢ − x̄)² / (n − 1))                     standard deviation of x
r  = cov(x, y) / (σx · σy)                          Pearson correlation coefficient
```

Dividing by the two standard deviations is what makes `r` **scale-free**: it does not matter whether marks are out of 100 or out of 10, `r` is unchanged.

| r | Meaning |
|---|---|
| +1 | perfect positive linear relation |
| +0.9 … +0.7 | strong positive |
| +0.5 … +0.3 | moderate |
| +0.2 … 0 | weak / negligible |
| negative | one rises while the other falls |
| 0 | no **linear** relation (a curved relation can still exist!) |

`r²` is the **coefficient of determination**: the fraction of the variation in y explained by the linear relation with x. `r = 0.9979` gives `r² = 0.9958`, so 99.6% of the variation in marks is explained — that is the sentence to write in the conclusion, not just the r value.

**Three traps the examiner will set:**

1. **Correlation is not causation.** Ice-cream sales correlate with drowning deaths; neither causes the other (both follow temperature).
2. **r only measures linearity.** `y = x²` over a symmetric range gives `r ≈ 0`.
3. **r is sensitive to outliers** — one extreme point can move r from 0.2 to 0.9. Always look at the scatterplot in the Visualize tab before trusting r.

## 3. Verified output of the program

`code/exp4_correlation.py`, dataset `datasets/students.csv` (12 students; constructed for teaching, which is why the correlations are clean):

```
PART 1 - FULL CALCULATION (study_hours vs marks)
  n = 12   mean(x) = 6.4167   mean(y) = 65.6667
  cov(x,y) = 49.6061
  σx = 2.8749   σy = 17.2907
  r  = 49.6061 / (2.8749 × 17.2907) = 0.9979
  r² = 0.9958  ->  99.6% of the variation in marks

PART 2 - RANKED (what Weka's Ranker prints)
  rank  attribute          r        |r|    strength
  1     study_hours     0.9979    0.9979   very strong
  2     attendance_pct  0.9970    0.9970   very strong
  3     sleep_hours    -0.2120    0.2120   weak (negative)

PART 3 - CORRELATION MATRIX
                   study_hours  attendance_pct  sleep_hours   marks
  study_hours           1.0000          0.9935      -0.2016  0.9979
  attendance_pct        0.9935          1.0000      -0.2141  0.9970
  sleep_hours          -0.2016         -0.2141       1.0000 -0.2120
  marks                 0.9979          0.9970      -0.2120  1.0000

PART 4 - PATTERNS
  mean marks, study_hours >= 7 : 80.17 (n = 6)
  mean marks, study_hours <  7 : 51.17 (n = 6)
  students with marks >= 75    : 4 of 12 (33.3%)
  all of them studied >= 7 h   : yes
```

**The redundancy finding is the exam-worthy one.** `study_hours` and `attendance_pct` correlate **0.9935 with each other** — they carry almost the same information. Keeping both adds no predictive power and makes any linear model's coefficients unstable (multicollinearity). The correct action is: keep the one with the higher correlation to the class (`study_hours`, 0.9979), remove the other. That is precisely Step 4 of your notebook (Remove button in Preprocess).

## 4. The Weka route, exactly as in your notebook

1. **Explorer → Preprocess → Open file…** → a numeric dataset (your notebook used `cpu.arff` or `diabetes.arff`; `weka/students.arff` in this pack works the same way).
2. Click the **Select attributes** tab (next to Visualize).
3. In **Attribute Evaluator** click **Choose** → `weka.attributeSelection.CorrelationAttributeEval`.
4. In **Search Method** click **Choose** → `weka.attributeSelection.Ranker`. Weka may ask to confirm switching to a ranking method — click **Yes**.
5. Set the **class** dropdown (bottom right) if it is not already set; `CorrelationAttributeEval` measures each attribute against that class.
6. Click **Start**.

The output lists attributes from most to least correlated with the class, plus a "Merit" per attribute — this is the same ranking the Python program printed in Part 2.

> **What `CorrelationAttributeEval` does, in one line (this is a favourite viva question):** it computes Pearson's correlation between each attribute and the class; a nominal class is handled by treating each of its values as a 0/1 indicator and combining the correlations as a weighted average.

### When the class is categorical: chi-square instead

Pearson's r needs a numeric class. For a nominal class (`churn = Yes/No`) use a **χ² test of independence**:

```
χ² = Σ (observed − expected)² / expected
expected(cell) = (row total × column total) / grand total
degrees of freedom = (rows − 1)(cols − 1)
```

Interpretation: a large χ² (relative to its critical value at 5% significance) means the two attributes are **not** independent, i.e. the attribute is informative for the class. `p < 0.05` is the usual threshold. In Weka this is `ChiSquaredAttributeEval` in the same Select-attributes tab.

Which evaluator to choose — a table worth memorising:

| Evaluator | Data | Measures |
|---|---|---|
| `CorrelationAttributeEval` | numeric class | Pearson correlation with the class |
| `ChiSquaredAttributeEval` | nominal class | χ² independence from the class |
| `InfoGainAttributeEval` | nominal class | reduction in entropy |
| `GainRatioAttributeEval` | nominal class | information gain corrected for many-valued attributes |
| `OneRAttributeEval` | nominal class | accuracy of the 1-rule classifier per attribute |
| `ReliefFAttributeEval` | any | instance-based, handles interaction between attributes |

## 5. The pandas version

```python
import pandas as pd

df = pd.read_csv("datasets/students.csv")

print(df.corr(numeric_only=True).round(4))          # full correlation matrix

target = "marks"
scores = (df.corr(numeric_only=True)[target]
            .drop(target)                             # remove the self-correlation
            .sort_values(key=abs, ascending=False))   # rank by strength
print(scores.round(4))
```

`df.corr()` returns a square matrix of Pearson coefficients; selecting the target column gives exactly the ranked list Weka's Ranker prints, and `sort_values(key=abs)` puts the strongest relation first regardless of sign.

For Spearman's rank correlation (which survives outliers and reads monotonic non-linear relations): `df.corr(method="spearman")`.

## 6. From correlation to a pattern you can act on

The program's Part 4 is the "pattern" half of the aim, and this is the format to copy in the record:

> Students studying ≥ 7 h average **80.17** marks; students below 7 h average **51.17** — a gap of 29 marks (n = 6 in each group). All four students scoring ≥ 75 studied ≥ 7 h.
>
> **Pattern:** `IF study_hours ≥ 7 THEN marks ≥ 75` holds for 4 of the 6 students in that group (67%), and for 0 of the 6 students below the threshold.
>
> **Caveat:** n = 12, so this is a hypothesis, not a law; the relation is also confounded with attendance (r = 0.99 with study hours).

That is a complete, honest answer, and it demonstrates the two skills being marked: computing the coefficient and interpreting it.

## 7. Write this on paper

> **Aim.** To identify potential patterns and correlations among the attributes of a dataset.
>
> **Theory.** Correlation measures the strength and direction of the linear relationship between two numeric attributes. The Pearson correlation coefficient is r = cov(x,y)/(σx·σy), where cov(x,y) = Σ(xᵢ−x̄)(yᵢ−ȳ)/(n−1). It ranges from −1 (perfect negative) through 0 (no linear relation) to +1 (perfect positive), and is scale-free because the covariance is divided by the product of the standard deviations. The square of r, the coefficient of determination r², is the proportion of variance in one variable explained by the other. Correlation must not be confused with causation, and it detects only linear relations. When the target attribute is nominal, the chi-square test of independence is used instead: χ² = Σ(O−E)²/E with (r−1)(c−1) degrees of freedom. Highly correlated pairs of predictor attributes are redundant and one of them may be removed without loss of information.
>
> **Procedure (Weka).**
> 1. Launch Weka and open the Explorer.
> 2. Load a numeric dataset in the Preprocess tab.
> 3. Switch to the **Select attributes** tab.
> 4. Choose the attribute evaluator `CorrelationAttributeEval`.
> 5. Choose the search method `Ranker` and confirm the switch.
> 6. Select the class attribute.
> 7. Click **Start** and read the ranked list of attributes by merit.
> 8. Return to Preprocess, select the attributes with negligible merit, and click **Remove**.
> 9. Note the reduction in the number of attributes.
>
> **Observation.** `study_hours` (r = 0.9979) and `attendance_pct` (r = 0.9970) are both very strongly correlated with marks, while `sleep_hours` (r = −0.2120) is weak and negative. The two strong attributes correlate 0.9935 with each other, so one of them is redundant.
>
> **Result.** Correlations were identified and ranked; the redundant attribute was removed, reducing the feature space without losing predictive information.

**Numerical drill.** For x = 1, 2, 3 and y = 2, 4, 7: x̄ = 2, ȳ = 13/3 = 4.333; cov = [(1−2)(2−4.333) + 0 + (3−2)(7−4.333)]/2 = (2.333 + 0 + 2.667)/2 = 2.5; σx = 1; σy = √(14.333/2) = 2.677; **r = 2.5/(1×2.677) = 0.934**. Very strong positive.

## 8. Viva questions for Experiment 4

**Q: What does a correlation of −0.85 mean?**
A strong negative linear relation: as one attribute increases the other decreases, and the points lie close to a falling straight line.

**Q: Difference between covariance and correlation?**
Covariance depends on the units of both variables; correlation divides by the standard deviations, so it is unit-free and bounded in [−1, 1].

**Q: What is r²?**
The coefficient of determination: the proportion of the variance in the dependent attribute explained by the linear model.

**Q: Why is the diagonal of a correlation matrix always 1?**
Every attribute correlates perfectly with itself.

**Q: How do you detect redundant attributes?**
Look for off-diagonal values close to ±1; those pairs carry overlapping information. Keep the one with the stronger relation to the class.

**Q: What are the limitations of Pearson's r?**
It captures only linear relations, is not robust to outliers, and says nothing about causation.

**Q: What is multicollinearity and why does it matter?**
When two or more predictors are highly correlated, their individual coefficients in a regression become unstable and hard to interpret, even though predictions may stay accurate. Removing one predictor is the usual fix.

**Q: When would you use chi-square instead of correlation?**
When both attributes (or the class) are nominal — for example, `contract_type` versus `churn`.

**Q: What does the Ranker search method do?**
It ranks attributes individually by their evaluated merit instead of searching for a subset, so it is fast but ignores interaction between attributes.

**Q: What is the difference between a pattern and a correlation?**
A correlation is a numeric summary of a linear relation; a pattern is a rule or structure that holds for a subgroup of instances ("if study hours ≥ 7 then marks ≥ 75"), which can exist even when the correlation is zero.
