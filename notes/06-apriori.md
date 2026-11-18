# 06 — Experiment 6: Apply the Apriori algorithm to transaction data

> **Aim.** To identify patterns in transaction data by applying the Apriori algorithm.
>
> **Course outcomes.** CO3 (characterise the kinds of patterns discovered by association rule mining).
>
> **Programs.** `code/exp6_apriori.py` (plain Python, prints every level). **Weka route** (your notebook): Associate tab → Apriori, `minSupport = 0.2`, `metricType = Confidence`, `minMetric = 0.8`. **Data:** `weka/retail_transaction.arff`.

## 1. The one-paragraph theory

**Association rule mining** finds statements of the form *"customers who buy X also buy Y"* in a database of transactions. Each rule X → Y has two numbers: **support**, how often X and Y occur together in the whole database, and **confidence**, how often Y occurs among the transactions that contain X. A rule is called **strong** when both exceed thresholds chosen by the analyst. **Apriori** finds strong rules in two phases: first it finds all **frequent itemsets** (itemsets whose support ≥ minimum support), then it generates rules from those itemsets. Its efficiency comes from one property: *if an itemset is infrequent, every superset of it is also infrequent* (the **anti-monotone / downward-closure property**), so whole branches of the search space are pruned without counting them.

## 2. The three formulas (write these exactly)

```
support(X → Y)    = support(X ∪ Y) = (transactions containing both X and Y) / total transactions
confidence(X → Y) = support(X ∪ Y) / support(X)
lift(X → Y)       = confidence(X → Y) / support(Y)
```

And the reading of each:

| Measure | Question it answers | Range | Reading |
|---|---|---|---|
| Support | how common is the combination? | 0…1 | low support = rare, possibly noise |
| Confidence | how reliable is the rule? | 0…1 | 1.0 = Y always follows X in this data |
| Lift | is it better than chance? | 0…∞ | **> 1 useful, = 1 independent, < 1 negatively related** |

Two more worth naming: **leverage** = support(X∪Y) − support(X)·support(Y) (same idea as lift, absolute), and **conviction** = (1 − support(Y)) / (1 − confidence) (how much more often X would be wrong if the rule were perfect).

**The most important idea in this experiment:** high confidence alone is worthless. If 90% of all customers buy milk, then "bread → milk" with confidence 0.90 tells you nothing. Lift compares the rule against that baseline, which is why lift, not confidence, is the interestingness measure.

## 3. The Apriori procedure, step by step

```
1. Set minimum support (minsup) and minimum confidence (minconf).
2. Scan the database once, count every single item.
3. L1 = items with count ≥ minsup.
4. Repeat for k = 2, 3, 4, …:
   a. JOIN: combine pairs of (k−1)-itemsets that share their first k−2 items
      to form candidate k-itemsets.
   b. PRUNE: discard a candidate if any of its (k−1)-subsets is not frequent
      (this is the Apriori property doing the work).
   c. COUNT: scan the database and count the support of the surviving candidates.
   d. Lk = candidates with count ≥ minsup.
5. Stop when Lk is empty.
6. For every frequent itemset, generate all rules A → (itemset − A).
7. Keep the rules whose confidence ≥ minconf. Report support, confidence, lift.
```

Step 4b is what makes Apriori fast. Step 7 is where most students stop too early — the itemsets are not the answer, the **rules** are.

## 4. Your dataset, traced by hand (verified)

`weka/retail_transaction.arff`, 4 transactions, `t` = present:

| | bread | milk | butter | diapers |
|---|---|---|---|---|
| T1 | t | t | t | f |
| T2 | f | t | f | t |
| T3 | t | t | f | f |
| T4 | t | t | t | t |

**L1 (counts):** milk 4, bread 3, butter 2, diapers 2. With minsup = 0.5 (≥ 2 transactions) all four survive.

**L2 (candidates from L1, then counted):**

| pair | count | support | survive 0.5? |
|---|---|---|---|
| bread, milk | 3 | 0.75 | ✔ |
| bread, butter | 2 | 0.50 | ✔ |
| bread, diapers | 1 | 0.25 | ✘ |
| milk, butter | 2 | 0.50 | ✔ |
| milk, diapers | 2 | 0.50 | ✔ |
| butter, diapers | 1 | 0.25 | ✘ |

**L3:** only {bread, butter, milk} has support 0.50 (T1 and T4) and survives; {bread, butter, diapers} = 1, {bread, diapers, milk} = 1, {butter, diapers, milk} = 1 all fail. **L4** = {bread, butter, diapers, milk} = 1, fails. Stop.

**Rules at minconf = 0.6** (11 rules; a selection):

| rule | support | confidence | lift | reading |
|---|---|---|---|---|
| {bread} → {milk} | 0.75 | 1.0000 | 1.0000 | always true here, but milk is in 100% of baskets — no information |
| {butter} → {bread} | 0.50 | 1.0000 | 1.3333 | **useful: 33% more likely than chance** |
| {bread} → {butter} | 0.50 | 0.6667 | 1.3333 | the reverse rule has the same lift, lower confidence |
| {milk} → {bread} | 0.75 | 0.7500 | 1.0000 | no gain over chance |
| {bread, milk} → {butter} | 0.50 | 0.6667 | 1.3333 | same lift with a longer antecedent |

**What the conclusion should say.** The only genuine association in this data is **butter ↔ bread** (lift 1.33 both ways). Everything involving milk has lift exactly 1.0, because milk appears in every single transaction — the honest observation is that *this dataset is too small (4 rows) for milk to be informative*, and that is a data problem, not an algorithm problem. Saying that out loud is worth more than any rule table.

## 5. The settings in your notebook, and what they really mean

Your record used `minSupport = 0.20` and `minMetric = 0.80` with 4 transactions. **Support 0.20 of 4 rows is 0.8 transactions**, and because counts are whole numbers, the effective requirement becomes **"appears in at least 1 transaction"** — that is, no pruning at all. Verified consequence: every itemset appears in L1…L4, and 16 rules are generated, most of them from single-transaction coincidences.

That is a perfect exam answer to *"what does support 0.20 mean?"*:

> Support 0.20 means the itemset must occur in 20% of transactions. In a 4-transaction dataset that is 0.8 transactions, so in practice any itemset occurring once qualifies; the threshold is meaningless at this scale. With 100 transactions the same 0.20 would require 20 occurrences.

**Choosing sensible thresholds:** as a rule of thumb in a real basket dataset, start with support 0.01–0.05 (transactions are many) and confidence 0.5–0.6, then raise support until the output is readable. State your thresholds and the transaction count together — one without the other is uninterpretable.

## 6. The Weka route, exactly as in your notebook

1. **Create the ARFF file** `retail_transaction.arff` with the four nominal attributes `{t,f}` and the four data rows (copy `weka/retail_transaction.arff`).
2. **Explorer → Preprocess → Open file…** and load it. Weka shows 4 instances, 4 attributes, all nominal.
3. Click the **Associate** tab.
4. **Choose** → `weka.associations.Apriori`.
5. Click the options text and set: `minSupport = 0.2`, `metricType = Confidence`, `minMetric = 0.8` (or set them through the property sheet / `-S 0.2 -C 0.8` on the command line).
6. Click **Start**.
7. Read the output in three blocks: the **scheme and options**, the **frequent itemsets** it found with support, and the **best rules** (`rule (confidence, support)`), followed by the run statistics (time, number of itemsets, number of rules).

What Weka prints, and how to read it:

```
Apriori
=======
Minimum support: 0.2 (0 instances)
...
Frequent itemsets (itemsets with support >= 0.2):
  milk 4
  bread 3
  ...
Best rules found:
  1. bread= t 3 ==> milk= t 3    conf:(1)
  ...
```

`conf:(1)` means confidence 1.0. Weka prints the values of the nominal attribute (`bread=t`), which is why the file must be `{t,f}` and not numeric.

**Common failures in Weka's Associate tab, with the fix:**

| Message | Cause | Fix |
|---|---|---|
| `Apriori: Cannot handle numeric attributes!` | the item columns are numeric 0/1 | declare them `{0,1}` nominal, or use the `NumericToNominal` filter |
| `Apriori: No attributes!` | the class index is set to an item, or no attributes selected | set "Ignore class" / clear the class, or select attributes |
| output has thousands of rules | support too low | raise `minSupport` |
| no rules at all | support or confidence too high | lower them and re-read the itemset block to see where it stops |
| `Nominal value not declared in header` | a value in `@data` is not in the `{...}` list | make the braces match the data exactly |

## 7. The program, and why it is worth writing by hand

`code/exp6_apriori.py` implements all seven steps with no libraries. The parts to be able to point at:

```python
def support_of(itemset, transactions):
    return sum(1 for t in transactions if itemset <= t) / len(transactions)
```

`itemset <= t` is **set inclusion** — frozenset `<=` means "is a subset of". That one expression is the whole of support counting.

```python
for a, b in combinations(sorted(prev, key=sorted), 2):
    union = a | b
    if len(union) == k:
        if all(frozenset(sub) in current for sub in combinations(union, k - 1)):
            candidates.add(union)
```

That is the **join** (`a | b`) and the **prune** (`all(... in current)`) in five lines. If the examiner asks you to explain Apriori's pruning, this is the code to point at: a candidate survives only if *every* (k−1)-subset is already known to be frequent.

Verified output (Run 1 = notebook settings 0.20/0.80):

```
L1 (4 itemsets): {milk}:4, {bread}:3, {butter}:2, {diapers}:2
L2 (6 itemsets): {bread,milk}:3, {bread,butter}:2, {butter,milk}:2,
                 {diapers,milk}:2, {bread,diapers}:1, {butter,diapers}:1
L3 (4 itemsets): {bread,butter,milk}:2, {bread,butter,diapers}:1,
                 {bread,diapers,milk}:1, {butter,diapers,milk}:1
L4 (1 itemset):  {bread,butter,diapers,milk}:1
total rules: 16
```

Run 2 (0.50 / 0.60) gives L1 4, L2 4, L3 1 and **11 rules** — the same numbers as the hand trace in section 4. Run 3 uses the 9-transaction market basket file: L1 = {milk:7, bread:6, butter:4}, L2 = {bread,milk:5}, and only two rules ({bread}→{milk}, conf 0.8333, lift 1.0714; {milk}→{bread}, conf 0.7143, lift 1.0714). The extra transactions immediately make the output meaningful — a point worth making in the conclusion.

## 8. Apriori versus FP-Growth (guaranteed comparison question)

| | Apriori | FP-Growth |
|---|---|---|
| Database scans | one per level (k+1 scans) | **two** |
| Data structure | candidate itemsets | compressed FP-tree |
| Candidate generation | yes (join + prune) | **none** |
| Memory | low | higher (tree in memory) |
| Speed on dense/long data | slow | much faster |
| Rule quality | identical results | identical results |
| Implementation difficulty | easy | harder |

Both find exactly the same frequent itemsets; they differ only in cost. Say that — it is the sentence that shows you understand rather than memorised.

## 9. Write this on paper

> **Aim.** To identify patterns in transaction data by applying the Apriori algorithm.
>
> **Theory.** Association rule mining discovers rules of the form X → Y, where X and Y are disjoint itemsets, in a database of transactions. The support of a rule is the fraction of transactions containing X ∪ Y; the confidence is support(X ∪ Y)/support(X); the lift is confidence/support(Y), and a lift greater than 1 shows that the consequent occurs more often than it would by chance. A rule is strong if both its support and confidence meet user-defined thresholds. Apriori finds frequent itemsets level by level, using the anti-monotone property: if an itemset is not frequent, none of its supersets can be frequent, so candidates containing an infrequent subset are pruned before counting. Rules are then generated from each frequent itemset by splitting it into antecedent and consequent.
>
> **Procedure.**
> 1. Create an ARFF file whose attributes are the items, declared nominal as `{t,f}`.
> 2. Enter one row per transaction, `t` for present and `f` for absent.
> 3. Launch Weka and open the Explorer.
> 4. Load the ARFF file in the Preprocess tab.
> 5. Switch to the Associate tab and choose the Apriori algorithm.
> 6. Set minimum support (0.2), metric type (Confidence) and minimum metric (0.8).
> 7. Click Start and observe the frequent itemsets printed with their support.
> 8. Read the association rules with their confidence and support, and the execution statistics.
>
> **Observation.** With 4 transactions, milk occurs in all 4, bread in 3, butter and diapers in 2. {bread, butter, milk} is the only 3-itemset meeting support 0.5. The rule {butter} → {bread} has support 0.5, confidence 1.0 and lift 1.3333, indicating a positive association.
>
> **Result.** Frequent itemsets and association rules were generated successfully from the transaction data using Apriori. The lift values show that butter and bread are positively associated, while rules involving milk carry no information because milk occurs in every transaction.

## 10. Viva questions for Experiment 6

**Q: State the Apriori property.**
If an itemset is infrequent, all of its supersets are infrequent; equivalently, every subset of a frequent itemset is frequent. It is the downward-closure property and it is what allows pruning.

**Q: Difference between support and confidence?**
Support is a property of the itemset (how common the combination is); confidence is a property of the rule (how reliable the implication is). Confidence = support(X∪Y)/support(X).

**Q: Why is lift needed if confidence is already high?**
Because a frequent consequent makes confidence high for every rule pointing at it. Lift divides by the consequent's base rate, so it measures the actual gain over chance.

**Q: What does lift < 1 mean?**
Negative association — the consequent is *less* likely when the antecedent is present (substitutes, e.g. two competing brands).

**Q: What are the two phases of Apriori?**
Frequent-itemset generation (join → prune → count, level by level), then rule generation from those itemsets with a confidence threshold.

**Q: Why does Apriori need many database scans?**
It must count candidates for each level k, and candidates depend on the counts of level k−1, so one scan per level. FP-Growth avoids this by compressing the database into a tree in two scans.

**Q: What is a maximal frequent itemset? What is a closed itemset?**
Maximal: frequent and no superset is frequent. Closed: frequent and no superset has the same support. Both are compressions of the itemset lattice; closed sets preserve all support information.

**Q: What happens if minimum support is 0?**
Every itemset is frequent, including the full set — the lattice explodes and the runtime is exponential.

**Q: In your file, what do `t` and `f` mean, and why nominal?**
`t` = item present, `f` = absent. Nominal because Apriori treats items as categories; a numeric 0/1 column would be rejected or binned.

**Q: What is the complexity of Apriori?**
Exponential in the worst case (2^d candidate itemsets for d items), though pruning makes it practical; cost per level ≈ number of candidates × transactions.

**Q: Give three real applications.**
Market basket analysis, cross-selling/product placement, web clickstream and page recommendation, medical symptom–diagnosis rules, fraud pattern detection.

**Q: Can Apriori handle quantitative attributes?**
Not directly; they must be discretised into intervals (e.g. age → young/middle/old), after which the same algorithm applies.
