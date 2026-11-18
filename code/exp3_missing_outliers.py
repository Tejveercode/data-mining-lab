#!/usr/bin/env python3
"""
Experiment 3 - WAP to check for missing values and outliers.

Runs with plain Python 3 (no pandas needed), so it works on any lab machine.
The four sections mirror the four things the examiner asks for:
  1. how much data is missing, and where
  2. a five-number summary (min, Q1, median, Q3, max)
  3. IQR fencing  -> outliers
  4. z-score     -> outliers (the second, independent method)

Run from inside the code/ folder:  python3 exp3_missing_outliers.py
"""
import csv

CSV_PATH = "datasets/movies.csv"
# 'year' is deliberately left out of the outlier sections: it is a time index,
# not a measurement, so a film from 2009 is not an "outlier".
NUMERIC = ["rating", "votes", "box_office_crore", "screens"]


# ---------------------------------------------------------------- helpers
def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def column(rows, name):
    """Return the column as a list of floats, with None wherever the cell is blank."""
    out = []
    for r in rows:
        v = r[name].strip()
        out.append(float(v) if v != "" else None)
    return out


def quantile(sorted_vals, q):
    """Linear-interpolation percentile, the same convention pandas and numpy use."""
    n = len(sorted_vals)
    pos = (n - 1) * q
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def mean(vals):
    return sum(vals) / len(vals)


def stdev(vals):
    """Sample standard deviation (n-1), same as pandas .std()."""
    m = mean(vals)
    return (sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5


def fmt(x):
    return f"{x:.4f}"


# ---------------------------------------------------------------- section 1
def report_missing(rows):
    print("=" * 70)
    print("SECTION 1 - MISSING VALUES (data.isnull().sum())")
    print("=" * 70)
    total_cells = 0
    total_missing = 0
    for col in NUMERIC:
        blanks = sum(1 for r in rows if r[col].strip() == "")
        total_cells += len(rows)
        total_missing += blanks
        pct = 100 * blanks / len(rows)
        print(f"  {col:<20} {blanks:>3} missing   ({pct:5.1f}% of {len(rows)} rows)")
    print(f"  {'TOTAL':<20} {total_missing:>3} missing   "
          f"({100 * total_missing / total_cells:5.1f}% of all cells)")
    print()
    print("  Rows that have at least one blank cell:")
    for i, r in enumerate(rows):
        gaps = [c for c in NUMERIC if r[c].strip() == ""]
        if gaps:
            print(f"    row {i:>2} ({r['movie']:<22}) -> {', '.join(gaps)}")
    print()


# ---------------------------------------------------------------- section 2
def five_number_summary(rows):
    print("=" * 70)
    print("SECTION 2 - FIVE-NUMBER SUMMARY  (data.describe())")
    print("=" * 70)
    print(f"  {'column':<18}{'count':>6}{'min':>12}{'Q1':>12}{'median':>12}"
          f"{'Q3':>12}{'max':>12}{'mean':>12}")
    for col in NUMERIC:
        vals = sorted(v for v in column(rows, col) if v is not None)
        print(f"  {col:<18}{len(vals):>6}{vals[0]:>12.2f}{quantile(vals, 0.25):>12.2f}"
              f"{quantile(vals, 0.50):>12.2f}{quantile(vals, 0.75):>12.2f}"
              f"{vals[-1]:>12.2f}{mean(vals):>12.2f}")
    print()


# ---------------------------------------------------------------- section 3
def iqr_outliers(rows, k=1.5):
    print("=" * 70)
    print(f"SECTION 3 - IQR METHOD  (lower = Q1 - {k}*IQR, upper = Q3 + {k}*IQR)")
    print("=" * 70)
    for col in NUMERIC:
        pairs = [(r["movie"], v) for r, v in zip(rows, column(rows, col)) if v is not None]
        vals = sorted(v for _, v in pairs)
        q1 = quantile(vals, 0.25)
        q3 = quantile(vals, 0.75)
        iqr = q3 - q1
        lower = q1 - k * iqr
        upper = q3 + k * iqr
        found = [(name, v) for name, v in pairs if v < lower or v > upper]
        print(f"  {col}")
        print(f"    Q1 = {fmt(q1)}   Q3 = {fmt(q3)}   IQR = {fmt(iqr)}")
        print(f"    lower fence = {fmt(lower)}   upper fence = {fmt(upper)}")
        if found:
            for name, v in found:
                side = "HIGH" if v > upper else "LOW "
                print(f"    OUTLIER ({side}) {name:<22} = {fmt(v)}")
        else:
            print("    no outliers")
    print()


# ---------------------------------------------------------------- section 4
def zscore_outliers(rows, threshold=2.0):
    print("=" * 70)
    print(f"SECTION 4 - Z-SCORE METHOD  (|z| > {threshold})")
    print("=" * 70)
    for col in NUMERIC:
        pairs = [(r["movie"], v) for r, v in zip(rows, column(rows, col)) if v is not None]
        vals = [v for _, v in pairs]
        m, s = mean(vals), stdev(vals)
        found = [(name, v, (v - m) / s) for name, v in pairs if abs((v - m) / s) > threshold]
        print(f"  {col:<20} mean = {fmt(m):>10}   std = {fmt(s):>10}")
        if found:
            for name, v, z in found:
                print(f"    OUTLIER {name:<22} = {fmt(v):>10}   z = {z:+.3f}")
        else:
            print("    no outliers")
    print()


# ---------------------------------------------------------------- main
def main():
    rows = load_rows(CSV_PATH)
    print(f"\nDataset: {CSV_PATH}   rows = {len(rows)}\n")
    report_missing(rows)
    five_number_summary(rows)
    iqr_outliers(rows)
    zscore_outliers(rows)
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("  1. box_office_crore and votes both contain blank cells -> impute or drop.")
    print("  2. IQR and z-score agree on the extreme 'votes' value (Baahubali 2),")
    print("     which is a genuine blockbuster, not an error: cap it, keep it, or")
    print("     model it separately - but never delete it silently.")
    print("  3. Report which method you used; the two methods do not have to agree.")
    print()


if __name__ == "__main__":
    main()
