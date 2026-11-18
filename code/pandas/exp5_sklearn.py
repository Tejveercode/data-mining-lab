#!/usr/bin/env python3
"""
Experiment 5, scikit-learn version - the form used in practice.

    pip install scikit-learn pandas
    python3 exp5_sklearn.py
"""
import pandas as pd
from sklearn.cluster import KMeans

POINTS = [[1, 2], [2, 1], [1, 1], [8, 9], [9, 8], [8, 8]]


def main():
    X = pd.DataFrame(POINTS, columns=["x", "y"])

    print("=" * 72)
    print("K-MEANS, k = 2 (same data as the lab record)")
    print("=" * 72)
    model = KMeans(n_clusters=2, init="k-means++", n_init=10, random_state=0).fit(X)
    for i, point in enumerate(POINTS):
        print(f"  point {point}  ->  cluster {model.labels_[i]}")
    centroids = [[round(float(v), 4) for v in c] for c in model.cluster_centers_]
    print(f"  centroids : {centroids}")
    print(f"  SSE (inertia_) : {model.inertia_:.4f}")

    print("\n" + "=" * 72)
    print("ELBOW METHOD, k = 1 to 4")
    print("=" * 72)
    print(f"  {'k':<4}{'SSE':>12}{'drop':>12}")
    previous = None
    for k in range(1, 5):
        m = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=0).fit(X)
        drop = "" if previous is None else f"{previous - m.inertia_:.4f}"
        print(f"  {k:<4}{m.inertia_:>12.4f}{drop:>12}")
        previous = m.inertia_
    print("\n  The large drop is from k = 1 to k = 2; afterwards the gains are tiny,")
    print("  so the elbow says k = 2.")


if __name__ == "__main__":
    main()
