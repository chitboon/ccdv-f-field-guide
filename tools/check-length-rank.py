#!/usr/bin/env python3
"""
check-length-rank.py — per-item option length/rank diagnostic for authoring.

check-item-quality.py's "correct is longest" and "length-rank spread" checks
only report aggregate percentages, which don't tell you WHICH items to fix.
This prints, per item, the correct answer's rank among its options by
character length (1 = longest, 4 = shortest) — run it after a first draft
and while iterating, not only after check-item-quality.py already failed.

Usage
-----
  python3 check-length-rank.py FILE --key KEYFILE

Read the printed rank distribution: if most items show rank 1, the correct
answer is consistently the longest (a real cue) — trim the over-explained
correct answers and add genuine reasoning to the thinnest distractors until
ranks spread out. Aim for no single rank at more than ~35% of items before
running check-item-quality.py, which is the real gate.
"""
import collections
import re
import sys


def main(argv):
    if len(argv) < 3 or argv[1] != "--key":
        print(__doc__)
        return 2
    path, _, keypath = argv
    text = open(path, encoding="utf-8").read()
    keytext = open(keypath, encoding="utf-8").read()
    keys = {}
    for m in re.finditer(r"\*\*(\d+)\.\s*([A-F](?:\s*(?:,|&|and)\s*[A-F])*)\s*\*\*", keytext):
        keys[int(m.group(1))] = "".join(re.findall(r"[A-F]", m.group(2)))

    ranks = []
    for block in re.split(r"\n---+\n", text):
        num = re.search(r"^\*\*(\d+)\.\*\*", block, re.M)
        if not num:
            continue
        n = int(num.group(1))
        opts = dict(re.findall(r"^([A-F])[.)]\s+(.+?)\s*$", block, re.M))
        if not opts or n not in keys:
            continue
        lens = {l: len(v) for l, v in opts.items()}
        order = sorted(lens, key=lambda l: -lens[l])
        for k in keys[n]:
            if k not in lens:
                continue
            rank = order.index(k) + 1
            ranks.append(rank)
            print(f"item {n:2d} key={k} rank={rank} lens={lens}")

    if not ranks:
        sys.exit(f"{path}: no items matched against {keypath} — check both files parse")

    dist = collections.Counter(ranks)
    n = len(ranks)
    print(f"\nrank distribution over {n} keyed answers: "
          + " ".join(f"{r}:{dist[r]} ({100*dist[r]/n:.0f}%)" for r in sorted(dist)))
    worst = max(dist, key=dist.get)
    if dist[worst] / n > 0.35:
        print(f"rank {worst} is {100*dist[worst]/n:.0f}% of items — likely to fail "
              f"check-item-quality.py's correct-is-longest/length-rank-spread checks. "
              f"Rebalance before running that gate.")
    else:
        print("rank distribution looks spread out — check-item-quality.py is the real gate, run it next.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
