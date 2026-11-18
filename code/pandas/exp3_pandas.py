#!/usr/bin/env python3
"""
Experiment 3, pandas version - the program as it appears in the lab notebook,
cleaned up and made runnable from anywhere.

    pip install pandas
    python3 exp3_pandas.py
"""
import pandas as pd

CSV_PATH = "../datasets/movies.csv"


def main():
    df = pd.read_csv(CSV_PATH)

    print("=" * 70)
    print("STEP 1-2: dataset loaded, first five records")
    print("=" * 70)
    print(df.head().to_string(index=False))

    print("\n" + "=" * 70)
    print("STEP 4: dataset information (dtypes and non-null counts)")
    print("=" * 70)
    df.info()

    print("\n" + "=" * 70)
    print("STEP 5: statistical summary (data.describe())")
    print("=" * 70)
    print(df.describe().round(2).to_string())

    print("\n" + "=" * 70)
    print("STEPS 6-12: outliers in every numerical column (IQR method)")
    print("=" * 70)
    # 'year' is a time index, not a measurement, so it is excluded from the scan.
    num_cols = [c for c in df.select_dtypes(include="number").columns if c != "year"]
    for col in num_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower) | (df[col] > upper)][col]
        print(f"\n  Column: {col}")
        print(f"    Q1 = {q1:.2f}   Q3 = {q3:.2f}   IQR = {iqr:.2f}")
        print(f"    lower = {lower:.2f}   upper = {upper:.2f}")
        print(f"    outliers found: {len(outliers)}")
        if len(outliers):
            for idx, val in outliers.items():
                print(f"      row {idx:>2}  {df.loc[idx, 'movie']:<24} {val:.2f}")

    print("\n" + "=" * 70)
    print("STEP 13: missing values (data.isnull().sum())")
    print("=" * 70)
    print(df.isnull().sum().to_string())
    print(f"\n  total missing cells : {df.isnull().sum().sum()} of {df.size}")
    print(f"  rows with any blank : {df.isnull().any(axis=1).sum()}")

    print("\n" + "=" * 70)
    print("STEP 14: conclusion")
    print("=" * 70)
    print("  Missing values were found in votes (1) and box_office_crore (2).")
    print("  Outliers were detected with the IQR rule; the extreme votes value")
    print("  belongs to a genuine blockbuster, so it is retained and noted.")


if __name__ == "__main__":
    main()
