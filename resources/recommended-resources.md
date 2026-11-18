# Recommended resources — the minimum set, and what to ignore

You do not need many resources for a practical exam. You need the syllabus, one book chapter per topic, the official tool documentation, and datasets you can actually open. This is the smallest set that covers everything.

## 1. The one document to keep open

**Your own lab record.** The examiner has seen the syllabus a hundred times and your notebook once. Every aim, every procedure and every output in your record is a potential question, so the highest-value revision is reading your own file, not a new book.

## 2. Textbooks — the exact chapters

| Book | Chapter | Covers |
|---|---|---|
| Han, Kamber & Pei — *Data Mining: Concepts and Techniques*, 3rd ed. | Ch. 3 (3.2, 3.3, 3.5) | pre-processing: cleaning, integration, reduction, discretisation |
| same | Ch. 6 (6.1–6.3) | association rules, Apriori, FP-Growth |
| same | Ch. 8 (8.1–8.5) | classification: decision trees, Bayes, kNN, evaluation |
| same | Ch. 10 (10.1–10.6) | clustering: partitioning, hierarchy, density |
| Tan, Steinbach & Kumar — *Introduction to Data Mining*, 2nd ed. | Ch. 2, 4, 5, 7, 8 | pre-processing, classification, association, cluster analysis |
| Witten, Frank, Hall & Pal — *Data Mining: Practical ML Tools*, 4th ed. | Ch. 1, 2, 17 | the Weka book: how the tool works, how to read its output |

Read the chapter section that matches the experiment **after** doing the experiment, not before. The practical makes the chapter obvious; the chapter then gives you the vocabulary the examiner expects.

## 3. Official tool documentation (free, and the examiner's own source)

- **Weka manual** — *The WEKA Workbench* (Witten et al., free PDF from the Weka site) and the online **Weka Wiki**. The wiki's "Primer" page is the fastest way to learn the Explorer's panels.
- **Weka Javadoc / package list** — search `weka.associations.Apriori` or `weka.clusterers.SimpleKMeans` to see the exact option list; the option letters are what the command-line questions ask about.
- **pandas documentation** — `read_csv`, `describe`, `quantile`, `isnull`, `select_dtypes`, `corr`. The "10 minutes to pandas" page is enough.
- **scikit-learn user guide** — sections "Clustering" (`KMeans`, silhouette) and "Preprocessing" (`StandardScaler`), plus the "metrics" page for precision/recall.

## 4. Datasets you can use if the lab machine has none

| Dataset | Where | Why |
|---|---|---|
| `iris.arff`, `weather.nominal.arff` | inside Weka's `data` folder | ship with the tool; no download needed |
| the ARFF files in `weka/` of this pack | this repository | exactly the ones the experiments use |
| UCI Machine Learning Repository | archive.ics.uci.edu | iris, wine, adult, wholesale customers |
| Kaggle "Market Basket Optimisation" | kaggle.com | real grocery transactions for Project 2 |
| Kaggle "Telco Customer Churn" | kaggle.com | the standard churn dataset for Project 1 |

Download at home and keep them on a pen drive: a lab machine with no internet is the most common cause of a wasted session.

## 5. What to skip

- Long video playlists covering the whole subject — 40 hours to answer a 5-mark question.
- "Data mining project" repositories that dump a notebook with no explanation; you will be asked *why*, and the notebook does not say.
- Anything that teaches the algorithm without the formula. In this exam the formula is the answer.

## 6. A single reading plan if you have one day

1. Han Ch. 3.2–3.3, then run `exp3_missing_outliers.py`. (90 min)
2. Tan Ch. 4 (or Han 8.3 for Bayes) — but for the lab, only the evaluation metrics matter; read the confusion-matrix section. (45 min)
3. Han Ch. 10.2 (K-means) and 6.2 (Apriori), then run `exp5_kmeans.py` and `exp6_apriori.py`. (90 min)
4. Weka Primer, sections on Preprocess and Associate. (45 min)
5. Cheat sheet + viva handbook out loud. (60 min)

That is about six hours and covers every question in the bank.
