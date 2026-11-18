#!/usr/bin/env python3
"""
Experiment 4, pandas version.

    pip install pandas
    python3 exp4_pandas.py
"""
import pandas as pd

CSV_PATH = "../datasets/students.csv"
TARGET = "marks"


def main():
    df = pd.read_csv(CSV_PATH)

    print("=" * 72)
    print("CORRELATION MATRIX  (df.corr())")
    print("=" * 72)
    print(df.drop(columns=["student"]).corr(numeric_only=True).round(4).to_string())

    print("\n" + "=" * 72)
    print("RANKED CORRELATION WITH THE CLASS  (what Weka's Ranker prints)")
    print("=" * 72)
    corr = df.drop(columns=["student"]).corr(numeric_only=True)[TARGET]
    corr = corr.drop(TARGET).sort_values(key=abs, ascending=False)
    for rank, (name, value) in enumerate(corr.items(), 1):
        print(f"  {rank}. {name:<18} r = {value:+.4f}   |r| = {abs(value):.4f}")

    print("\n" + "=" * 72)
    print("PAIRWISE REDUNDANCY CHECK (|r| > 0.9 between predictors)")
    print("=" * 72)
    matrix = df.drop(columns=["student", TARGET]).corr(numeric_only=True)
    found = False
    for i, a in enumerate(matrix.columns):
        for b in matrix.columns[i + 1:]:
            if abs(matrix.loc[a, b]) > 0.9:
                print(f"  {a} <-> {b}: r = {matrix.loc[a, b]:+.4f}  -> one is redundant")
                found = True
    if not found:
        print("  none")

    print("\n" + "=" * 72)
    print("A PATTERN, NOT JUST A COEFFICIENT")
    print("=" * 72)
    hi = df[df["study_hours"] >= 7]["marks"]
    lo = df[df["study_hours"] < 7]["marks"]
    print(f"  mean marks | study_hours >= 7 : {hi.mean():.2f}  (n = {len(hi)})")
    print(f"  mean marks | study_hours <  7 : {lo.mean():.2f}  (n = {len(lo)})")
    print(f"  gap: {hi.mean() - lo.mean():.2f} marks")
    good = df[df["marks"] >= 75]
    print(f"  students with marks >= 75: {len(good)}; "
          f"all studied >= 7 h? {'yes' if (good['study_hours'] >= 7).all() else 'no'}")


if __name__ == "__main__":
    main()
