#!/usr/bin/env python3
"""
Experiment 4 - Identify potential patterns and correlations.

Pearson correlation from the formula, then the same thing ranked the way Weka's
CorrelationAttributeEval + Ranker shows it. Plain Python, no libraries.

Run from inside the code/ folder:  python3 exp4_correlation.py
"""
import csv

CSV_PATH = "datasets/students.csv"
TARGET = "marks"
FEATURES = ["study_hours", "attendance_pct", "sleep_hours"]


def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def column(rows, name):
    return [float(r[name]) for r in rows]


def mean(v):
    return sum(v) / len(v)


def pearson(x, y):
    """r = cov(x,y) / (sigma_x * sigma_y), written out so it can be shown on paper."""
    n = len(x)
    mx, my = mean(x), mean(y)
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (n - 1)
    sx = (sum((xi - mx) ** 2 for xi in x) / (n - 1)) ** 0.5
    sy = (sum((yi - my) ** 2 for yi in y) / (n - 1)) ** 0.5
    return cov / (sx * sy), cov, sx, sy


def strength(r):
    a = abs(r)
    if a >= 0.9:
        return "very strong"
    if a >= 0.7:
        return "strong"
    if a >= 0.4:
        return "moderate"
    if a >= 0.2:
        return "weak"
    return "negligible"


def show_full_calculation(rows):
    print("=" * 72)
    print("PART 1 - PEARSON CORRELATION, FULL CALCULATION (attributes: study_hours)")
    print("=" * 72)
    x = column(rows, "study_hours")
    y = column(rows, TARGET)
    r, cov, sx, sy = pearson(x, y)
    print(f"  n            = {len(x)}")
    print(f"  mean(x)      = {mean(x):.4f}     mean(y) = {mean(y):.4f}")
    print(f"  cov(x,y)     = {cov:.4f}")
    print(f"  sigma_x      = {sx:.4f}     sigma_y = {sy:.4f}")
    print(f"  r            = {cov:.4f} / ({sx:.4f} x {sy:.4f}) = {r:.4f}")
    print(f"  r^2          = {r * r:.4f}  -> {100 * r * r:.1f}% of the variation in marks")
    print(f"  interpretation: {strength(r)} positive linear relation")
    print()


def show_ranked(rows):
    print("=" * 72)
    print("PART 2 - CORRELATION OF EVERY FEATURE WITH THE CLASS, RANKED")
    print("     (this is exactly the ranking Weka's Ranker prints)")
    print("=" * 72)
    y = column(rows, TARGET)
    scores = []
    for f in FEATURES:
        r, _, _, _ = pearson(column(rows, f), y)
        scores.append((f, r))
    scores.sort(key=lambda t: -abs(t[1]))
    print(f"  {'rank':<6}{'attribute':<20}{'r':>10}   {'|r|':>8}   strength")
    for i, (f, r) in enumerate(scores, 1):
        print(f"  {i:<6}{f:<20}{r:>10.4f}   {abs(r):>8.4f}   {strength(r)}")
    print()
    return scores


def show_matrix(rows):
    print("=" * 72)
    print("PART 3 - CORRELATION MATRIX (attribute vs attribute)")
    print("=" * 72)
    cols = FEATURES + [TARGET]
    print("  " + " " * 16 + "".join(f"{c[:14]:>16}" for c in cols))
    for a in cols:
        line = f"  {a[:14]:<16}"
        for b in cols:
            r, _, _, _ = pearson(column(rows, a), column(rows, b))
            line += f"{r:>16.4f}"
        print(line)
    print()
    print("  Reading it: the diagonal is always 1.0000 (an attribute with itself).")
    print("  A pair with |r| close to 1 away from the diagonal is REDUNDANT -")
    print("  one of the two can be dropped without losing information.")
    print()


def show_patterns(rows):
    print("=" * 72)
    print("PART 4 - PATTERNS BEYOND THE CORRELATION COEFFICIENT")
    print("=" * 72)
    hi = [r for r in rows if float(r["study_hours"]) >= 7]
    lo = [r for r in rows if float(r["study_hours"]) < 7]
    print(f"  average marks, study_hours >= 7 : {mean([float(r[TARGET]) for r in hi]):.2f} "
          f"(n = {len(hi)})")
    print(f"  average marks, study_hours <  7 : {mean([float(r[TARGET]) for r in lo]):.2f} "
          f"(n = {len(lo)})")
    good = [r for r in rows if float(r[TARGET]) >= 75]
    print(f"  students with marks >= 75       : {len(good)} of {len(rows)} "
          f"({100 * len(good) / len(rows):.1f}%)")
    print(f"  all of them study >= 7 h?       : "
          f"{'yes' if all(float(r['study_hours']) >= 7 for r in good) else 'no'}")
    print(f"  all of them sleep >= 6 h?       : "
          f"{'yes' if all(float(r['sleep_hours']) >= 6 for r in good) else 'no'}")
    print()


def main():
    rows = load(CSV_PATH)
    print(f"\nDataset: {CSV_PATH}   rows = {len(rows)}\n")
    show_full_calculation(rows)
    scores = show_ranked(rows)
    show_matrix(rows)
    show_patterns(rows)
    print("=" * 72)
    print("CONCLUSION")
    print("=" * 72)
    best = scores[0]
    print(f"  '{best[0]}' is the strongest predictor of marks (r = {best[1]:.4f}),")
    print("  so it is the attribute to keep first in any model.")
    print("  Correlation is not causation: these numbers describe THIS sample of")
    print("  12 students, they do not prove that studying longer causes marks.")
    print()


if __name__ == "__main__":
    main()
