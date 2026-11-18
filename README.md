# Data Mining Lab (24CAP-308) — complete practical study pack

Everything needed to pass **all three phases** of the Data Mining Lab practical: the written theory/steps/formula questions, the viva, and the on-machine implementation. Built from the CU-LMS lab syllabus and from the six experiments as they are actually written in the lab record.

Course: **24CAP-308 Data Mining Lab**, 0-0-4-2 (2 credits), 8 lab hours per week.
Course outcomes served: **CO1–CO5** (data mining process · pre-processing · association rules · classification/prediction · clustering).

---

## The six experiments, and where each is covered

| # | Experiment (syllabus wording) | Note | Program |
|---|---|---|---|
| 1 | Download Weka and install it | [notes/01](notes/01-weka-install.md) | — |
| 2 | Load the dataset in Weka (GUI + CLI) and visualise it | [notes/02](notes/02-weka-load-visualize.md) | — |
| 3 | WAP to check for missing values and outliers | [notes/03](notes/03-missing-values-outliers.md) | `code/exp3_missing_outliers.py` |
| 4 | Identify potential patterns and correlations | [notes/04](notes/04-patterns-correlations.md) | `code/exp4_correlation.py` |
| 5 | WAP for grouping similar data points (K-means) | [notes/05](notes/05-kmeans.md) | `code/exp5_kmeans.py` |
| 6 | Apply the Apriori algorithm to transaction data | [notes/06](notes/06-apriori.md) | `code/exp6_apriori.py` |
| — | Projects: churn · market basket · XYZ Mart case | [notes/07](notes/07-projects.md) | `code/datasets/` |

Plus:

| File | What it is |
|---|---|
| [notes/00-lab-orientation.md](notes/00-lab-orientation.md) | how the lab is marked, the record format, a 7-day plan, the checklist |
| [notes/08-viva-handbook.md](notes/08-viva-handbook.md) | **120 viva questions** in the order they are asked, with answers |
| [notes/09-written-paper-drills.md](notes/09-written-paper-drills.md) | the written paper: **9 fully solved numericals** + 2-mark answer set |
| [exam/cheat-sheet.md](exam/cheat-sheet.md) | one card per experiment: formulas, Weka menu paths, numbers |
| [exam/question-bank.md](exam/question-bank.md) | every question type with marks and model-answer outlines |
| [resources/recommended-resources.md](resources/recommended-resources.md) | the exact book chapters, official docs, datasets |
| [weka/](weka/) | ready-made ARFF files, including the exact one from the record |
| [code/](code/) | dependency-free Python for every program, plus pandas/sklearn versions |
| [pdf/](pdf/) | five printable PDFs (built by `build_pdf.py`) |

---

## Run the programs (no installation needed)

```bash
cd code
python3 exp3_missing_outliers.py     # missing values, IQR and z-score outliers
python3 exp4_correlation.py          # Pearson r, ranking, matrix, patterns
python3 exp5_kmeans.py               # K-means traced iteration by iteration + elbow
python3 exp6_apriori.py              # Apriori: every level, then every rule
```

These use **only the Python standard library**, so they run in IDLE, in the lab, on any machine. Every number they print appears in the notes, so you can check the note against the program.

The *pandas / scikit-learn* versions are in `code/pandas/` and need libraries — use them when the examiner asks for "the real way", not as your fallback:

```bash
pip install pandas scikit-learn
cd code/pandas
python3 exp3_pandas.py               # the version written in the lab record
python3 exp4_pandas.py
python3 exp5_sklearn.py
```

Verified outputs (all four plain-Python programs exit 0):

| Program | Key verified result |
|---|---|
| `exp3` | `votes` 1 missing, `box_office_crore` 2; votes fences [−95000, 225000]; Baahubali 2 z = +3.988 |
| `exp4` | r = 0.9979 (study hours), 0.9970 (attendance), −0.2120 (sleep); study↔attendance 0.9935 → redundant |
| `exp5` | centroids (1.3333, 1.3333) / (8.3333, 8.3333), SSE 2.6667, converged in 2 iterations; elbow k=2 |
| `exp6` | L1/L2/L3 counts; `{butter}→{bread}` support 0.5, confidence 1.0, lift 1.3333; 11 rules at 0.5/0.6 |

---

## The 30-second version of each experiment

1. **Weka install** — Java toolkit; take the `zulu` Windows build (bundles Java); verify the GUI Chooser and Explorer's six tabs.
2. **Load & visualise** — ARFF = relation, attributes, data; Preprocess shows Missing/Distinct/Min/Max/Mean/StdDev; Visualize colours points by class.
3. **Missing values & outliers** — count nulls; IQR fences (Q1−1.5·IQR, Q3+1.5·IQR) and z-score (|z|>3); IQR is robust, z-score assumes normal.
4. **Patterns & correlations** — r = cov/(σx·σy), 0.9+ is strong; near-1 pairs are redundant (drop one); Weka: `CorrelationAttributeEval` + `Ranker`.
5. **K-means** — nearest centroid, recompute means, repeat; minimises SSE; local optimum → initialisation matters; choose k by the elbow.
6. **Apriori** — support, confidence, lift; anti-monotone property; join → prune → count per level; then rules from the frequent itemsets.

---

## What the record must contain (marks live here)

```
Aim · Course Outcomes · Theory · Algorithm/Steps · Program or Weka path
Output (real, pasted) · Result · Viva questions asked
```

Never invent output. If the program failed, write the error and the fix — that is a correct result and it demonstrates understanding. Your record's own programs print a name inside the output; keep that, it proves the run is yours.

---

## Honest notes about the material

- The two data files in the lab record (`Indian-Movie-Theatre.csv`, and the four-transaction retail table) are reproduced as `code/datasets/movies.csv` and `code/datasets/retail_transactions.csv` / `weka/retail_transaction.arff`. The movies file is a **stand-in of the same shape** (21 films, same columns, deliberate blanks and extremes), because the original Kaggle file was not supplied. The code works identically on the original — change the path.
- The retail ARFF is **exactly** the one in the record (4 transactions, `{t,f}`), so the Weka numbers you get will match the note.
- `iris.arff` and `weather.nominal.arff` ship inside Weka's own `data` folder. A copy of the weather file is in `weka/` so the experiment works even if that folder is missing.
- Two numbers in the notes were produced by running the programs in this pack, not copied from a book. Every formula was checked against at least one worked numerical.

---

## Rebuild the PDFs

```bash
pip install reportlab
python3 build_pdf.py        # from this folder
```

Writes five PDFs into `pdf/`: the manual (experiments 1–6), projects + written paper, viva handbook, question bank, cheat sheet.

---

## References

1. Han, Kamber & Pei — *Data Mining: Concepts and Techniques*, 3rd ed., 2011 — Ch. 3 (pre-processing), 6 (association), 10 (clustering).
2. Tan, Steinbach & Kumar — *Introduction to Data Mining*, 2nd ed., 2018 — Ch. 2, 4, 5, 7, 8.
3. Witten, Frank, Hall & Pal — *Data Mining: Practical ML Tools*, 4th ed., 2016 — the Weka book.
4. Weka documentation: <https://www.cs.waikato.ac.nz/ml/weka/>
5. pandas and scikit-learn user guides.
