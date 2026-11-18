#!/usr/bin/env python3
"""
Experiment 5 - WAP for grouping similar data points together (K-means).

Two demos:
  PART 1  the exact dataset and initial centroids from the lab notebook,
          traced iteration by iteration so every number can be checked.
  PART 2  the same algorithm for k = 1..4 to show the elbow method, with a
          deterministic "farthest first" seeding so the result is repeatable.

Run from inside the code/ folder:  python3 exp5_kmeans.py
"""

POINTS = [[1, 2], [2, 1], [1, 1], [8, 9], [9, 8], [8, 8]]
CENTROIDS = [[1, 0], [10, 10]]          # the two starting centroids from the notebook


def distance(p, c):
    """Euclidean distance between two points."""
    return sum((pi - ci) ** 2 for pi, ci in zip(p, c)) ** 0.5


def assign(points, centroids):
    """Steps 3-4: distance to every centroid, then the nearest one wins."""
    clusters = [[] for _ in centroids]
    for p in points:
        dists = [distance(p, c) for c in centroids]
        clusters[dists.index(min(dists))].append(p)
    return clusters


def update(clusters):
    """Step 5: the new centroid of a cluster is the mean of its points."""
    new = []
    for cl in clusters:
        if not cl:                      # an empty cluster keeps its old centre
            new.append(None)
            continue
        k = len(cl[0])
        new.append([sum(p[i] for p in cl) / len(cl) for i in range(k)])
    return new


def sse(clusters, centroids):
    """Sum of squared errors - the number the elbow plot shows."""
    total = 0.0
    for cl, c in zip(clusters, centroids):
        for p in cl:
            total += sum((pi - ci) ** 2 for pi, ci in zip(p, c))
    return total


def show_points(pts):
    return " ".join(f"({p[0]:g},{p[1]:g})" for p in pts) if pts else "-"


def show_centroid(c):
    return "(" + ", ".join(f"{v:.4f}" for v in c) + ")"


def run_kmeans(points, k, seed_centroids, max_iter=50):
    centroids = [list(c) for c in seed_centroids[:k]]
    for _ in range(max_iter):
        clusters = assign(points, centroids)
        new = update(clusters)
        moved = any(nc is not None and any(abs(a - b) > 1e-9 for a, b in zip(nc, c))
                    for nc, c in zip(new, centroids))
        centroids = [nc if nc is not None else c for nc, c in zip(new, centroids)]
        if not moved:
            break
    return assign(points, centroids), centroids


# ---------------------------------------------------------------- part 1
def part1():
    print("=" * 78)
    print("PART 1 - THE NOTEBOOK DATASET, TRACED BY HAND")
    print("=" * 78)
    print(f"  points    : {POINTS}")
    print(f"  centroids : {CENTROIDS}")
    print()

    centroids = [list(c) for c in CENTROIDS]
    for it in range(1, 11):
        clusters = assign(POINTS, centroids)
        print(f"  --- iteration {it} ---")
        for i, c in enumerate(centroids):
            dists = ", ".join(f"{distance(p, c):.4f}" for p in POINTS)
            print(f"    distances to C{i + 1}{show_centroid(c)}: {dists}")
        for i, cl in enumerate(clusters):
            print(f"    cluster {i + 1}: {show_points(cl)}   (size {len(cl)})")
        new_centroids = update(clusters)
        moved = any(nc is not None and any(abs(a - b) > 1e-9 for a, b in zip(nc, c))
                    for nc, c in zip(new_centroids, centroids))
        centroids = [nc if nc is not None else c
                     for nc, c in zip(new_centroids, centroids)]
        print("    new centroids: " + "   ".join(
            f"C{i + 1}{show_centroid(c)}" for i, c in enumerate(centroids)))
        print(f"    SSE = {sse(clusters, centroids):.4f}")
        print()
        if not moved:
            print(f"  Converged after {it} iteration(s): the centroids stopped moving.")
            break

    print(f"  FINAL clusters  : C1 = {show_points(clusters[0])}    "
          f"C2 = {show_points(clusters[1])}")
    print(f"  FINAL centroids : {show_centroid(centroids[0])}   {show_centroid(centroids[1])}")
    print(f"  FINAL SSE       : {sse(clusters, centroids):.4f}")
    print()


# ---------------------------------------------------------------- part 2
def farthest_first(points, k):
    """Deterministic seeding: start at the first point, then always take the point
    farthest from everything chosen so far. Same idea as k-means++, no randomness."""
    seeds = [list(points[0])]
    while len(seeds) < k:
        best = max(points, key=lambda p: min(distance(p, s) for s in seeds))
        seeds.append(list(best))
    return seeds


def part2():
    print("=" * 78)
    print("PART 2 - ELBOW METHOD (k = 1 to 4, farthest-first seeding)")
    print("=" * 78)
    print(f"  {'k':<4}{'SSE':>12}   {'drop':>10}")
    values = []
    for k in range(1, 5):
        clusters, centroids = run_kmeans(POINTS, k, farthest_first(POINTS, k))
        val = sse(clusters, centroids)
        values.append((k, val))
        drop = "" if k == 1 else f"{values[-2][1] - val:.4f}"
        print(f"  {k:<4}{val:>12.4f}   {drop:>10}")
        print(f"      clusters: " + " | ".join(show_points(c) for c in clusters))
    print()
    print("  Read the 'drop' column: the big fall happens going from k = 1 to")
    print("  k = 2, and after that each extra cluster buys a much smaller fall.")
    print("  That corner is the elbow, and it points at k = 2 clusters.")
    print("  The dataset has two clear groups, so this is the correct answer -")
    print("  the elbow method is not decoration, it recovers the truth.")
    print()


def main():
    part1()
    part2()
    print("=" * 78)
    print("CONCLUSION")
    print("=" * 78)
    print("  K-means put (1,2) (2,1) (1,1) in one cluster and (8,9) (9,8) (8,8) in")
    print("  the other, with final centroids (1.3333,1.3333) and (8.3333,8.3333).")
    print("  It is unsupervised: no label was ever used, only distances.")
    print("  The result depends on the starting centroids - which is why the lab")
    print("  asks you to state them, and why real tools use k-means++ seeding.")
    print()


if __name__ == "__main__":
    main()
