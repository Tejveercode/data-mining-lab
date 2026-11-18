# 00 — How this practical is marked, and how to prepare for it

## What the syllabus actually says

24CAP-308, **Data Mining Lab**, 0-0-4-2 (2 credits), 8 lab hours per week, coordinator Ms. Gurpreet.
Six experiments, two per unit, plus two projects and one project-based-learning case.

| Unit | Experiment | One-line aim |
|---|---|---|
| 1 | 1 | Download and install Weka |
| 1 | 2 | Load a dataset in Weka, visualise it, read insights |
| 2 | 3 | WAP to check for missing values and outliers |
| 2 | 4 | Identify potential patterns and correlations |
| 3 | 5 | WAP for grouping similar data points together (K-means) |
| 3 | 6 | Apply the Apriori algorithm to transaction data |

The internal marks are weighted like this (from the same syllabus page):

| Component | Weight | Frequency |
|---|---|---|
| Worksheet | 30 marks each | 6 experiments (2 per unit) → 43% of internal |
| Exam (MST) | 10 marks | once per semester → 10% |
| Experiential learning (mini project) | 5 marks | once → 5% |
| Attendance | — | — → 2% |

Two things follow from that table, and they should shape every hour you spend:

1. **The worksheet is 43% of your internal marks and it is written by hand during the lab.** The examiner is not checking whether your program is clever. They are checking whether the record has the required parts, in the required order, with your own output pasted in. A perfect program written in the wrong format scores less than a simple program recorded properly.
2. **Every experiment is examined in three phases** — the written theory/steps/formula questions, the viva, and running it on the machine. The same experiment has to be prepared three ways. That is what this pack gives you, experiment by experiment.

## The three phases, and what each one actually demands

### Phase 1 — the written part (theory, steps, formula)

Typical questions, all of which appear in `exam/question-bank.md`:

- "Write the aim and theory of Experiment 5." → you need the definition, the formula and two or three sentences on why the algorithm works.
- "Write the algorithm / procedure in steps." → numbered steps, no code.
- "State the formula for Euclidean distance / IQR / support / confidence / lift / Pearson correlation." → formula with every symbol defined.
- "Given this small table, compute Q1, Q3, IQR and the fences." → a numerical, marked line by line.
- "What will be the output of this program?" → code reading.

The written part is where students lose marks for a silly reason: they can run the program but cannot write the four-line formula from memory. Every note below has a **"Write this on paper"** section that is literally the text to reproduce.

### Phase 2 — the viva

Viva questions are short and go in this order almost every time:

1. What is the aim of your experiment? (one sentence, no hesitation)
2. Explain this line of your code. (the examiner points at a random line)
3. Why did you use this method and not the other one? (IQR vs z-score, K-means vs K-medoids, Apriori vs FP-Growth, correlation vs chi-square)
4. What does this number mean? (support 0.5, silhouette, SSE, r = −0.21)
5. What happens if the data changes? (missing values, different k, larger support)

Note 08 is a 120-question viva drill written in that exact order, including a line-by-line defence of each program.

### Phase 3 — the machine

You will be asked to *do* something, not to admire a finished file:

- open Weka, load a dataset, and show one statistic;
- write or modify a short program live — often "change the threshold and show me the new outliers" or "run it for k = 3";
- explain the output that appears.

That is why `code/` in this pack is plain Python with **no libraries**. It runs on any lab machine, it runs in IDLE, it runs if pandas is not installed, and every printed number can be checked by hand. The pandas and scikit-learn versions are shown in the notes as the "real world" version, not as the thing you depend on.

## Setup checklist before the lab

| Tool | Why | Check |
|---|---|---|
| Python 3 | Experiments 3, 5, 6 | `python3 --version` |
| pandas (optional) | the version in your notebook | `python3 -c "import pandas; print(pandas.__version__)"` |
| Java 8+ | Weka will not start without it | `java -version` |
| Weka 3.8.x | Experiments 1, 2, 4, 6 | Explorer opens with four tabs + Visualize |
| A folder for data | so paths in code match | keep `datasets/` next to your `.py` file |

If `java -version` prints nothing, install a JDK **before** the lab, not during it. On Windows, use the Weka installer whose name contains `zulu` — it carries its own Java, which removes the problem entirely.

## The record format (this is worth marks)

Every experiment in your notebook follows the same skeleton. Write these headings *before* the lab and fill them during it:

```
Experiment No.:      Date:
Aim:                 one sentence, copied from the syllabus wording
Course Outcomes:     CO1..CO5 as given (write the two or three that apply)
Theory:              8-15 lines - definition, formula, why the method works
Algorithm / Steps:   numbered, 6-12 steps, no code
Program / Procedure: the code, or the Weka menu path
Output:              a real screenshot or pasted text - never invented
Result / Conclusion: what the numbers mean, in one or two sentences
Viva questions:      the ones you were asked, with answers (examiners like this)
```

Three habits that separate a 28/30 worksheet from a 20/30 one:

1. **Never leave Output blank or invented.** If the program failed in the lab, write the error and the fix. That is a legitimate result and shows understanding.
2. **Number the steps even when the step is trivial.** "Step 5: compute IQR = Q3 − Q1" is a mark; a paragraph containing the same information is not.
3. **Put your name in the output or on the page** (your notebook already prints the name inside the program — keep that habit, it proves you ran it).

## A seven-day plan that actually fits around other subjects

| Day | Work | Time |
|---|---|---|
| 1 | Note 00 + 01 + 02, open Weka once at home | 60 min |
| 2 | Note 03, run `exp3_missing_outliers.py`, hand-compute Q1/Q3/IQR for one column | 75 min |
| 3 | Note 04, run `exp4_correlation.py`, do the Weka Select-attributes run | 60 min |
| 4 | Note 05, run `exp5_kmeans.py`, trace iteration 1 on paper without looking | 75 min |
| 5 | Note 06, run `exp6_apriori.py`, hand-build L1/L2 for the 4-transaction data | 75 min |
| 6 | Note 07 (projects) + note 09 (written answers) | 60 min |
| 7 | Note 08 viva drill out loud + cheat sheet, cover the answers | 45 min |

If you have only one evening: read the cheat sheet, run all four programs once, and answer the first 40 viva questions out loud. That is the minimum that prevents a disaster.

## What "hard to fail" means concretely

After this pack you should be able to do all of the following without notes. They are the exact things that get asked:

- write the Euclidean distance formula and compute one distance by hand
- state Q1, Q3, IQR and both fences for a list of ten numbers
- explain why `1.5` appears in the fence formula, and what a z-score of 3 means
- write support, confidence and lift, and compute all three from a 4×4 t/f table
- list Apriori's join and prune steps in order
- explain what K-means minimises and why the answer depends on the initial centroids
- name one advantage and one weakness of Weka's Explorer versus writing Python
- convert a CSV into ARFF by hand
