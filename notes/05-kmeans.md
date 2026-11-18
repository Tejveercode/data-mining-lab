# 05 — Experiment 5: WAP for grouping similar data points together (K-means)

> **Aim.** To write a program that groups similar data points together using K-means clustering.
>
> **Course outcomes.** CO5 (categorise the different clustering approaches).
>
> **Programs.** `code/exp5_kmeans.py` (plain Python, traced iteration by iteration) and `code/pandas/exp5_sklearn.py` (scikit-learn version). Weka route: **Cluster** tab → `SimpleKMeans`.

## 1. What clustering is, and why K-means

**Clustering** is the grouping of objects so that objects in the same group (cluster) are more similar to each other than to objects in other groups. It is **unsupervised**: there is no class label, so nothing tells the algorithm the "right" answer. That single fact is the most examined one in this experiment — the measure of success is internal (compactness and separation), not accuracy.

**K-means** partitions the data into exactly `k` clusters by minimising the **within-cluster sum of squared errors**:

```
SSE = Σⱼ Σ_{x ∈ Cⱼ} ‖x − μⱼ‖²
```

where `μⱼ` is the centroid (mean) of cluster `Cⱼ`. It is a form of **partitional, hard, centroid-based** clustering: every point goes into exactly one cluster (hard), and each cluster is represented by its mean (centroid).

Where it sits in the taxonomy (a certain viva question):

| Type | Members | K-means belongs? |
|---|---|---|
| Partitional | K-means, K-medoids/PAM, CLARA | ✔ K-means |
| Hierarchical | AGNES (single/complete/average linkage), DIANA | ✘ |
| Density-based | DBSCAN, OPTICS | ✘ |
| Model-based | GMM/EM | ✘ |

## 2. The distance formula

```
d(p, q) = √( (p₁ − q₁)² + (p₂ − q₂)² + … + (pₙ − qₙ)² )
```

For two 2-D points this is Pythagoras. **Worked:** d((1,2), (1,0)) = √(0² + 2²) = **2.000**; d((2,1), (10,10)) = √(64 + 81) = √145 = **12.0416**.

Other distances you may be asked to name: Manhattan (Σ|xᵢ−yᵢ|), Minkowski (the generalisation with exponent p), cosine (for text), Jaccard (for sets).

**Why scaling matters:** if one attribute is in thousands (`votes`) and another in single digits (`rating`), the Euclidean distance is dominated entirely by the large attribute. Normalise first (min–max or z-score) — that is the connection back to Unit 2.

## 3. The algorithm (six steps, memorise this order)

```
1. Choose k, the number of clusters.
2. Choose k initial centroids (randomly, or by k-means++ / farthest-first).
3. Repeat:
   a. ASSIGN each point to the nearest centroid (minimum Euclidean distance).
   b. UPDATE each centroid to the mean of the points assigned to it.
   c. If no point changed cluster (or centroids stopped moving), STOP.
4. Output the clusters and the final centroids.
```

Two properties to state in the viva:

- **It always converges**, because each step can only decrease SSE and SSE is bounded below by 0 — but it can converge to a **local** minimum, so the result depends on the initial centroids.
- **It is not guaranteed to find the global optimum**, which is why real implementations restart several times (`n_init`) and keep the best SSE.

## 4. The notebook's data, traced by hand (verified output)

Your record uses:

```
points    = [[1,2], [2,1], [1,1], [8,9], [9,8], [8,8]]
centroids = [[1,0], [10,10]]
```

**Iteration 1** — distances to each centroid:

| point | to C1 (1,0) | to C2 (10,10) | nearer |
|---|---|---|---|
| (1,2) | 2.0000 | 12.0416 | C1 |
| (2,1) | 1.4142 | 12.0416 | C1 |
| (1,1) | 1.0000 | 12.7279 | C1 |
| (8,9) | 11.4018 | 2.2361 | C2 |
| (9,8) | 11.3137 | 2.2361 | C2 |
| (8,8) | 10.6301 | 2.8284 | C2 |

New centroids: C1 = ((1+2+1)/3, (2+1+1)/3) = **(1.3333, 1.3333)**; C2 = ((8+9+8)/3, (9+8+8)/3) = **(8.3333, 8.3333)**. SSE = 2.6667.

**Iteration 2** — distances to the new centroids: (1,2) → 0.7454, (2,1) → 0.7454, (1,1) → 0.4714 to C1; (8,9) → 0.7454, (9,8) → 0.7454, (8,8) → 0.4714 to C2. The assignment is unchanged, so the centroids do not move and the algorithm **stops after 2 iterations**.

**Final answer:** `C1 = {(1,2), (2,1), (1,1)}`, `C2 = {(8,9), (9,8), (8,8)}`, centroids (1.3333, 1.3333) and (8.3333, 8.3333), SSE = 2.6667.

Write the iteration table in the record. It is the single most convincing piece of work in the whole lab file, because the examiner can check any row in two seconds.

## 5. Your notebook's program, and the bug in it

The program as written in the record:

```python
Points = [[1,2], [2,1], [1,1], [8,9], [9,8], [8,8]]
Centroids = [[1,0], [10,10]]
Clusters = [[], []]

for point in Points:
    d1 = ((point[0] - Centroids[0][0])**2 + (point[1] - Centroids[0][1])**2) ** 0.5
    if d1 < d2:                     # <-- d2 is used before it exists
        d2 = ((point[0] - Centroids[1][0])**2 + (point[1] - Centroids[1][1])**2) ** 0.5
    if d1 < d2:
        Clusters[0].append(point)
    else:
        Clusters[1].append(point)
...
```

**`d2` is referenced before it is assigned**, so the first pass raises `NameError: name 'd2' is not defined`. The stray `if d1 < d2:` on the line above the `d2` assignment is a copy error. If your record contains this version, an examiner who reads it will find it — and asking you to spot it is a very common viva question.

**Corrected, complete, single-pass version:**

```python
points = [[1, 2], [2, 1], [1, 1], [8, 9], [9, 8], [8, 8]]
centroids = [[1, 0], [10, 10]]
clusters = [[], []]

for point in points:
    d1 = ((point[0] - centroids[0][0])**2 + (point[1] - centroids[0][1])**2) ** 0.5
    d2 = ((point[0] - centroids[1][0])**2 + (point[1] - centroids[1][1])**2) ** 0.5
    if d1 < d2:
        clusters[0].append(point)
    else:
        clusters[1].append(point)

new_centroids = []
for cluster in clusters:
    x = sum(p[0] for p in cluster) / len(cluster)
    y = sum(p[1] for p in cluster) / len(cluster)
    new_centroids.append([round(x, 2), round(y, 2)])

print("Clusters:", clusters)
print("New centroids:", new_centroids)
```

Output:

```
Clusters: [[[1, 2], [2, 1], [1, 1]], [[8, 9], [9, 8], [8, 8]]]
New centroids: [[1.33, 1.33], [8.33, 8.33]]
```

This is **one iteration**. The record's version stops here; the honest caption is "after one iteration the centroids moved to …; repeating until the assignment stops changing converges in the second iteration to the same assignment". `code/exp5_kmeans.py` does the loop, which is the version to show if asked to demonstrate convergence live.

## 6. The general program (what to write if asked for the real thing)

The plain-Python general version in `code/exp5_kmeans.py` splits into four functions, and each is a viva question on its own:

| Function | Responsibility | The line that matters |
|---|---|---|
| `distance(p, c)` | Euclidean distance | `sum((pi-ci)**2 for ...) ** 0.5` |
| `assign(points, centroids)` | steps 3–4 | `dists.index(min(dists))` — the nearest centroid wins |
| `update(clusters)` | step 5 | mean of each coordinate over the cluster |
| `sse(clusters, centroids)` | compactness | sum of squared distances to the centroid |

It also runs the **elbow method** for k = 1…4 with deterministic farthest-first seeding. Verified output:

```
k      SSE        drop
1   149.6667
2     2.6667   147.0000
3     1.8333     0.8333
4     1.0000     0.8333
```

The drop from k = 1 to k = 2 is 147; each further cluster buys less than 1. That is the elbow at **k = 2** — which is the correct answer for six points in two obvious blocks. This is how you answer "how did you choose k?" with a number instead of an opinion.

## 7. The scikit-learn version (real-world form)

```python
import pandas as pd
from sklearn.cluster import KMeans

points = [[1,2], [2,1], [1,1], [8,9], [9,8], [8,8]]
X = pd.DataFrame(points, columns=["x", "y"])

model = KMeans(n_clusters=2, init="k-means++", n_init=10, random_state=0).fit(X)
print(model.labels_)              # cluster index of every point
print(model.cluster_centers_)     # final centroids
print(model.inertia_)             # SSE, sklearn's name for it
```

`init="k-means++"` chooses spread-out starting centroids, `n_init=10` restarts ten times and keeps the lowest SSE, and `inertia_` is exactly the SSE defined in section 1. Two arguments explain the whole of practice: random initialisation is a risk, and the fix is many restarts.

## 8. The Weka route

1. **Explorer → Preprocess** → load a numeric dataset (`iris.arff`).
2. Click the **Cluster** tab.
3. **Choose** → `weka.clusterers.SimpleKMeans`.
4. Click the parameter text to set `numClusters` (e.g. 3) and `seed`.
5. Make sure **Cluster mode** is set to "Use training set" for a quick demo.
6. Click **Start**; in the **Result list** (bottom left) right-click the new entry → **Visualize cluster assignments** to see the clusters coloured in a scatterplot.
7. The output reports the within-cluster SSE per cluster and the final centroids.

What to compare with Python: Weka's `SimpleKMeans` also uses k-means++ by default in recent versions and reports `Within cluster sum of squared errors` — the same quantity as `inertia_`.

## 9. Choosing k, and the honest limits

| Method | How it works | What it gives |
|---|---|---|
| Elbow | plot SSE against k, take the corner | a number, judgement needed |
| Silhouette | (b − a)/max(a,b), a = mean intra-cluster distance, b = mean distance to the nearest other cluster; range −1…+1 | higher is better; pick the k that maximises the mean |
| Domain knowledge | "we have three customer tiers" | the most reliable, when available |
| Gap statistic / BIC | compare against a null reference | statistical, heavier |

Limitations to name out loud:

- you must choose **k** in advance;
- it finds **spherical, similar-sized** clusters, and fails on elongated or nested shapes (DBSCAN handles those);
- it is **sensitive to feature scaling**;
- it is **sensitive to initial centroids** (local minima);
- it is **sensitive to outliers**, because a mean is dragged by extremes — which is exactly why **K-medoids (PAM)** exists: it uses a real point (the medoid) as the centre, so it is robust.

## 10. Write this on paper

> **Aim.** To write a program for grouping similar data points together using the K-means clustering algorithm.
>
> **Theory.** Clustering is an unsupervised learning technique that partitions a set of objects into groups such that objects within a group are more similar to each other than to objects in other groups. K-means is a partitional, centroid-based algorithm: it divides the data into k clusters and represents each cluster by the mean of its points. It minimises the within-cluster sum of squared errors, SSE = Σⱼ Σ_{x∈Cⱼ} ‖x − μⱼ‖². Similarity is measured by Euclidean distance, d(p,q) = √(Σ(pᵢ − qᵢ)²). Each iteration assigns every point to its nearest centroid and then recomputes each centroid as the mean of its cluster. The process repeats until the assignments stop changing. K-means always converges, but only to a local optimum, so the final result depends on the initial centroids; k-means++ seeding and multiple restarts are used to reduce this dependence.
>
> **Algorithm.**
> 1. Take the given data points and the number of clusters k.
> 2. Select k initial centroids.
> 3. Compute the Euclidean distance of every point from every centroid.
> 4. Assign each point to the nearest centroid.
> 5. Compute the new centroid of each cluster as the mean of its points.
> 6. Repeat steps 3–5 until the centroids no longer change.
> 7. Display the clusters and the final centroids.
>
> **Output.** Cluster 1 = {(1,2), (2,1), (1,1)} with centroid (1.33, 1.33); Cluster 2 = {(8,9), (9,8), (8,8)} with centroid (8.33, 8.33); converged after 2 iterations; SSE = 2.6667.
>
> **Result.** The six data points were grouped into two clusters of three points each. The elbow method confirmed k = 2 as the appropriate number of clusters.

## 11. Viva questions for Experiment 5

**Q: Why is K-means called unsupervised?**
Because no class label is used — the algorithm discovers groups from the data itself, so there is no accuracy to report, only internal measures such as SSE or silhouette.

**Q: What does K-means minimise?**
The within-cluster sum of squared Euclidean distances to the centroid (SSE / inertia).

**Q: Why does the algorithm always converge?**
Each assign step decreases SSE (or keeps it equal) and each update step decreases it further; SSE ≥ 0, so the sequence must stabilise. It can stop in a local minimum.

**Q: What happens if two initial centroids are placed on the same cluster?**
That cluster is split and the other may end up empty or merge improperly — a bad local optimum, one of two clusters containing one side. Re-running with different seeds or using k-means++ fixes it.

**Q: How do you choose k?**
Elbow method on SSE, silhouette score, or domain knowledge. Report the number, not the opinion.

**Q: What is a centroid?**
The mean vector of the points in a cluster; it need not be one of the data points.

**Q: K-means vs K-medoids (PAM)?**
K-medoids uses an actual data point (the medoid, minimising the sum of dissimilarities) as the centre, so it is robust to outliers and works with arbitrary distance measures; K-means is faster but sensitive to outliers.

**Q: What is the complexity of K-means?**
O(n · k · d · i): n points, k clusters, d dimensions, i iterations.

**Q: Why scale the data first?**
Because Euclidean distance is dominated by attributes with the largest numeric range; without scaling the clustering may effectively use only one attribute.

**Q: Which clustering algorithm would you use for arbitrary shapes with noise?**
DBSCAN — density-based, finds arbitrarily shaped clusters, and labels sparse points as noise.

**Q: What is hard vs soft clustering?**
Hard assigns each point to exactly one cluster (K-means); soft/fuzzy gives a membership degree per cluster (fuzzy c-means, GMM).

**Q: Can K-means handle categorical data?**
Not directly, because a mean of labels is meaningless; use K-modes or encode the categories first.
