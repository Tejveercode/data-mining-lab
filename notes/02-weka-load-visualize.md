# 02 — Experiment 2: Load a dataset in Weka and visualise it

> **Aim.** To load a dataset into Weka through the GUI and the command line, and to use the Explorer's statistics and visualisation to gain insights into the data.
>
> **Course outcomes.** CO1 (data mining process, preparing data for processing), CO2 (analysing data pre-processing techniques).
>
> **Dataset.** `iris.arff` (150 instances, 5 attributes) or `weather.nominal.arff` (14 instances, 5 attributes). Both ship with Weka in its `data` folder; copies of the weather file and a students file are in `weka/` in this pack.

## 1. Why we look before we model

A dataset is a claim about the world, and every claim has to be checked before it is used. In the first five minutes of looking at iris you learn three things that change every later decision:

- the **class is balanced** (50 / 50 / 50), so accuracy is a fair metric;
- the four measurements are **numeric and continuous**, so distance-based algorithms need scaling;
- `petal.width` separates the classes almost perfectly, so any classifier that uses only `sepal.width` will look weak by comparison.

None of that requires an algorithm. It requires opening the file and reading the summary panel. That is the entire aim of this experiment, and it is the first thing examiners ask you to do on the machine.

## 2. Anatomy of an ARFF file

```arff
% comment - anything after % on a line is ignored
@relation weather                      <- 1. name of the dataset

@attribute outlook {sunny,overcast,rainy}   <- 2. one line per column
@attribute temperature {hot,mild,cool}
@attribute humidity {high,normal}
@attribute windy {TRUE,FALSE}
@attribute play {yes,no}                    <- the CLASS is simply the last attribute

@data                                        <- 3. the rows, comma separated
sunny,hot,high,FALSE,no
sunny,hot,high,TRUE,no
...
```

The four rules that matter for the exam:

| Element | Meaning | Trap |
|---|---|---|
| `@relation` | dataset name, one word | must come before any `@attribute` |
| `{a,b,c}` after an attribute | **nominal** — closed list of allowed values | a value outside the braces makes the whole file fail to load |
| `numeric` / `real` / `integer` | continuous column | `integer` is only a hint; Weka stores it as numeric |
| `@data` | everything after this line is data, one row per line | no commas inside values unless quoted |
| `?` | missing value | an empty cell is **not** the same thing and can break parsing |

**Converting a CSV to ARFF by hand** is a standard exam question. Given a CSV header `movie,year,rating` you write:

```arff
@relation movies
@attribute movie string
@attribute year numeric
@attribute rating numeric
@data
Dangal,2016,8.4
PK,2014,8.1
```

Rule of thumb for choosing the type: numbers you will do arithmetic on → `numeric`; a fixed set of categories → `{...}`; free text used only as a label → `string`.

## 3. Load the data — the GUI route (your notebook, Step 1)

1. Start Weka → click **Explorer**.
2. In the **Preprocess** tab, click **Open file…**.
3. Navigate to the Weka `data` folder (Windows: `C:\Program Files\Weka-3-8-x\data`; Linux/macOS: the `data` folder beside `weka.jar`) and choose `iris.arff`. To use the files in this pack, navigate to `weka/` and pick `weather.nominal.arff`.
4. Weka reports in the log box: `--- Loading ---` and then `Relation: iris, Instances: 150, Attributes: 5`.
5. The **Current relation** box now shows the name, instance count and attribute count.

Other ways to load, which you should be able to name:

- **Open URL…** — load from a web address.
- **Open DB…** — load from a database through JDBC.
- **Generate…** — create a synthetic dataset (`weka.datagenerators`), useful for demos.

## 4. Read the statistics panel (your notebook, Step 3)

Click an attribute in the **Attributes** list on the left. The **Selected attribute** panel fills in:

| Field | What it tells you | iris example (`petalwidth`) |
|---|---|---|
| Name | the attribute | `petalwidth` |
| Missing | count of `?` values | 0 |
| Distinct | number of different values | 22 |
| Type | numeric / nominal | Numeric |
| Unique | count of values that occur once | 0 |

and below it, for a numeric attribute:

| Statistic | Meaning |
|---|---|
| Minimum | smallest value |
| Maximum | largest value |
| Mean | arithmetic average |
| StdDev | sample standard deviation (n−1 in the denominator) |

For a **nominal** attribute the same box lists every value with its count and a bar chart — that is how you check class balance. In `weather.nominal.arff`, `play` shows **yes 9 / no 5**: a mildly imbalanced class, worth mentioning in your conclusion.

Two questions the examiner will ask here, and the answers:

- *"Which attribute would you drop, and why?"* — an attribute with **Distinct = 1** (all values identical) carries no information; also one that is a unique ID (Distinct = number of instances, Unique = number of instances).
- *"How do you spot a data-quality problem in this panel?"* — Missing > 0 is the direct signal; a Mean far from the Median (visible in the Visualize tab as a long tail) is the indirect one.

## 5. Load the data — the command line (your notebook, Step 2)

Open **Simple CLI** from the GUI Chooser (the button in the bottom-right of the chooser window; on some builds it is under **Tools**). The Simple CLI already has Weka's classpath configured, so the short form works:

```
java weka.core.Instances data/iris.arff
```

Output (abridged):

```
Relation: iris
Instances: 150
Attributes: 5
    sepalwidth
    sepallength
    petalwidth
    petallength
    class
```

From an ordinary terminal (outside Weka) you must supply the classpath yourself:

```bash
java -cp weka.jar weka.core.Instances data/iris.arff
```

Other command-line tools worth knowing for the viva:

```bash
java -cp weka.jar weka.filters.unsupervised.attribute.Remove -R 1 -i data/iris.arff -o iris_no_id.arff
java -cp weka.jar weka.clusterers.SimpleKMeans -N 3 -t data/iris.arff
java -cp weka.jar weka.associations.Apriori -t weka/retail_transaction.arff
```

The pattern is always: `java -cp weka.jar <package>.<Class> <options> -t <file>`.

## 6. Visualise (your notebook, Step 4)

1. Click the **Visualize** tab. Weka draws a **scatterplot matrix**: one small plot for every pair of attributes, arranged as a grid.
2. In the **Colour** dropdown (bottom right of the tab) choose the class attribute — for iris, `class`. Each class now has its own colour, and separation becomes visible at a glance.
3. Click any single plot to open it enlarged. The enlarged window has controls to change the axes (X, Y), **jitter** the points (useful when many values coincide), and **Save** the plot as an image for your record.
4. For iris you will see that one class is linearly separable from the other two in the petal plots, while the other two overlap — a conclusion you can write in one sentence without running a classifier.

**What "insight" means in the conclusion.** Not "the graph was plotted". Something like: *"In the petal-width vs petal-length scatter, the setosa points form an isolated cluster, while versicolor and virginica overlap; therefore a linear classifier will separate setosa easily but will confuse the other two classes. This is confirmed later by the confusion matrix."* That sentence is worth more than a screenshot with no comment.

## 7. Write this on paper

> **Aim.** To load the given dataset into Weka using the GUI and the command-line interface, and to visualise the data in order to gain insights.
>
> **Theory.** Weka is a Java-based machine-learning toolkit. Datasets are stored in ARFF (Attribute-Relation File Format), which has three parts: the relation name, the attribute declarations (with type: numeric, nominal or string) and the data rows. The Explorer's Preprocess tab reads the file, infers the type of each attribute and computes descriptive statistics — count, missing values, distinct values, minimum, maximum, mean and standard deviation for numeric attributes, and value frequencies for nominal attributes. The Visualize tab plots a scatterplot matrix of all attribute pairs, and colouring the points by the class attribute reveals how separable the classes are.
>
> **Procedure.**
> 1. Launch Weka and open the Explorer.
> 2. In the Preprocess tab click **Open file…** and select the dataset (`iris.arff`).
> 3. Note the relation name, number of instances and number of attributes reported.
> 4. Click each attribute and record its type, missing count, distinct count, and min/max/mean/std-dev.
> 5. Open Simple CLI and run `java weka.core.Instances data/iris.arff` to list the dataset structure from the command line.
> 6. Switch to the Visualize tab, choose the class attribute in the Colour menu, and inspect the scatterplot matrix.
> 7. Enlarge one informative plot and save it for the record.
>
> **Observation.** Iris contains 150 instances and 5 attributes; all attributes are numeric except the class, which is nominal with three balanced values. No missing values are reported. The petal measurements separate the classes far better than the sepal measurements.
>
> **Result.** The dataset was loaded successfully through both interfaces, its structure and statistics were verified, and the scatterplot matrix showed that petal width and petal length are the discriminating attributes.

## 8. Viva questions for Experiment 2

**Q: How many instances and attributes does iris have?**
150 instances, 5 attributes (4 numeric measurements + 1 nominal class).

**Q: Which section of an ARFF file must come first?**
`@relation`, then all `@attribute` lines, then `@data`.

**Q: What does Weka do with `?` in the data?**
It stores it as a missing value and, depending on the algorithm, either ignores that instance, distributes it proportionally, or uses the attribute mean/mode.

**Q: Difference between `numeric` and `nominal`?**
Numeric is continuous or ordered and supports arithmetic and distance; nominal is a closed set of unordered labels, stored internally as indices.

**Q: Why colour the scatterplot by the class?**
Because separation between classes is only visible when the points are labelled; it shows whether the problem is linearly separable before any model is trained.

**Q: What is the difference between Distinct and Unique in the panel?**
Distinct = number of different values present; Unique = number of values that occur exactly once.

**Q: Can you load Excel files directly?**
Not directly; export to CSV and load the CSV, or use `ExcelLoader` from the `weka.core.converters` package.

**Q: In the Simple CLI, why does `java weka.core.Instances ...` work without `-cp`?**
Because the Simple CLI runs inside the Weka process, which already has `weka.jar` on its classpath.
