#!/usr/bin/env python3
"""
Experiment 6 - Apply the Apriori algorithm to transaction data.

Prints every level (L1, L2, L3 ...), every count, and then the association
rules with support, confidence and lift, so each number can be reproduced on
paper. Plain Python, no libraries.

Run from inside the code/ folder:  python3 exp6_apriori.py
"""
import csv
from itertools import combinations

DATASETS = [
    # (csv file, min_support as a fraction, min_confidence, title)
    ("datasets/retail_transactions.csv", 0.20, 0.80,
     "RUN 1 - THE NOTEBOOK SETTINGS (4 transactions, support 0.20, confidence 0.80)"),
    ("datasets/retail_transactions.csv", 0.50, 0.60,
     "RUN 2 - THE SAME DATA WITH A STRICTER SUPPORT (0.50, confidence 0.60)"),
    ("datasets/market_basket.csv", 4 / 9, 0.60,
     "RUN 3 - MARKET BASKET (9 transactions, support 4/9 = 0.4444, confidence 0.60)"),
]


def load_transactions(path):
    """One row = one transaction; every cell holding 't' means the item is present."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    items = [c for c in rows[0].keys() if c != "tid"]
    transactions = []
    for r in rows:
        transactions.append(frozenset(i for i in items if r[i].strip().lower() == "t"))
    return items, transactions


def support_of(itemset, transactions):
    """Fraction of transactions that contain the whole itemset."""
    return sum(1 for t in transactions if itemset <= t) / len(transactions)


def count_of(itemset, transactions):
    return sum(1 for t in transactions if itemset <= t)


def apriori(transactions, min_support):
    """Level-wise search: generate, count, prune, repeat."""
    n = len(transactions)
    min_count = min_support * n
    levels = []
    items = sorted({i for t in transactions for i in t})

    # L1
    current = {}
    for item in items:
        s = frozenset([item])
        c = count_of(s, transactions)
        if c >= min_count:
            current[s] = c
    levels.append(current)

    k = 2
    while current:
        prev = list(current.keys())
        # JOIN step: only sets that share their first k-2 items are combined
        candidates = set()
        for a, b in combinations(sorted(prev, key=sorted), 2):
            union = a | b
            if len(union) == k:
                # PRUNE step: every (k-1)-subset must already be frequent
                if all(frozenset(sub) in current for sub in combinations(union, k - 1)):
                    candidates.add(union)
        # COUNT step
        nxt = {}
        for cand in sorted(candidates, key=lambda s: sorted(s)):
            c = count_of(cand, transactions)
            if c >= min_count:
                nxt[cand] = c
        if nxt:
            levels.append(nxt)
        current = nxt
        k += 1
    return levels, n


def show_levels(levels, n, min_support):
    print(f"  min_support = {min_support:.4f}  ->  an itemset must appear in at least "
          f"{min_support * n:.2f} of {n} transactions,")
    needed = int(min_support * n)
    if needed == min_support * n:
        print(f"  i.e. a count of at least {needed:.0f}.")
    else:
        print(f"  i.e. a count of at least {needed + 1} (counts are whole numbers).")
    print()
    for i, level in enumerate(levels, 1):
        named = ", ".join(
            "{" + ",".join(sorted(s)) + "}" + f":{c}" for s, c in
            sorted(level.items(), key=lambda kv: (-kv[1], sorted(kv[0])))
        )
        print(f"  L{i} ({len(level)} itemsets): {named}")
    print()


def rules_from(itemset, transactions, min_conf):
    """Every non-empty proper subset A of the itemset gives a rule A -> itemset-A."""
    out = []
    whole_support = support_of(itemset, transactions)
    body_items = sorted(itemset)
    for r in range(1, len(body_items)):
        for ant in combinations(body_items, r):
            ant = frozenset(ant)
            con = itemset - ant
            conf = whole_support / support_of(ant, transactions)
            if conf >= min_conf:
                out.append((ant, con, whole_support, conf))
    return out


def show_rules(levels, transactions, min_conf):
    print(f"  Rules with confidence >= {min_conf:.2f}")
    print(f"  {'rule':<32}{'support':>9}{'confidence':>12}{'lift':>9}   note")
    rows = []
    for level in levels:
        for itemset in level:
            rows.extend(rules_from(itemset, transactions, min_conf))
    rows.sort(key=lambda t: (-t[3], sorted(t[0])))
    for ant, con, sup, conf in rows:
        con_support = support_of(con, transactions)
        lift = conf / con_support
        note = "positive" if lift > 1 else ("negative" if lift < 1 else "independent")
        rule = "{" + ",".join(sorted(ant)) + "} -> {" + ",".join(sorted(con)) + "}"
        print(f"  {rule:<32}{sup:>9.4f}{conf:>12.4f}{lift:>9.4f}   {note} (lift)")
    if not rows:
        print("  (none - lower min_confidence to see rules)")
    print(f"  total rules: {len(rows)}")
    print()


def run(path, min_support, min_conf, title):
    print("=" * 78)
    print(title)
    print("=" * 78)
    items, transactions = load_transactions(path)
    print(f"  file   : {path}")
    print(f"  items  : {', '.join(items)}")
    print(f"  rows   : {len(transactions)}")
    for i, t in enumerate(transactions, 1):
        print(f"    T{i}: {{{','.join(sorted(t))}}}")
    print()
    levels, n = apriori(transactions, min_support)
    show_levels(levels, n, min_support)
    show_rules(levels, transactions, min_conf)
    return levels


def main():
    for path, sup, conf, title in DATASETS:
        levels = run(path, sup, conf, title)

    print("=" * 78)
    print("CONCLUSION")
    print("=" * 78)
    print("  Apriori found the frequent itemsets level by level, and every rule")
    print("  listed has support >= min_support and confidence >= min_confidence.")
    print("  Lift > 1 means the consequent is bought MORE often when the antecedent")
    print("  is present than when it is not - that is a real, useful pattern.")
    print()


if __name__ == "__main__":
    main()
