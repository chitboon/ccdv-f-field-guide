#!/usr/bin/env python3
"""
check-nearclone.py — the gate the mock handover requires and had no command for.

Compares every stem in a new item bank or key against every stem in papers that
have already been sat, token-wise. Two authors writing to the same task statement
can land on the same situation without either copying, and a paper that repeats an
item already answered correctly returns a score that is partly memory.

Usage
-----
  python3 check-nearclone.py NEW [NEW ...] --against OLD [OLD ...] [--threshold 0.6]

NEW accepts a bank *.json (objects with "stem"), a key.json (objects with "exp"
is ignored; keys carry no stems, so pass the bank or the rendered paper), or a
rendered paper .md with '## Q<n>' headings and '**A)**' options.
OLD accepts the same forms.

Exit status 1 if anything is at or above the threshold. Rewrite those stems.
"""
import argparse, collections, difflib, json, re, sys


def stems(path):
    if path.endswith(".json"):
        rows = json.load(open(path, encoding="utf-8"))
        out = [(r.get("id") or r.get("n"), r["stem"]) for r in rows if r.get("stem")]
        if not out:
            sys.exit(f"{path}: no 'stem' fields — pass the item bank or the rendered paper, "
                     f"not the key (keys carry no stems)")
        return out
    text = open(path, encoding="utf-8").read()
    out = []
    for block in re.split(r"\n(?=## Q\d+\n)", text):
        m = re.match(r"## Q(\d+)\n", block)
        if not m:
            continue
        body = block[m.end():]
        stem = re.split(r"^\*\*[A-F]\)\*\*", body, maxsplit=1, flags=re.M)[0]
        out.append((f"Q{m.group(1)}", stem.replace("---", "").strip()))
    if not out:
        sys.exit(f"{path}: parsed no items — expected '## Q<n>' headings with '**A)**' options")
    return out


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("new", nargs="+")
    ap.add_argument("--against", nargs="+", required=True)
    ap.add_argument("--threshold", type=float, default=0.6)
    a = ap.parse_args()
    new = [(f, i, s) for f in a.new for i, s in stems(f)]
    old = [(f, i, norm(s)) for f in a.against for i, s in stems(f)]
    print(f"{len(new)} new stems against {len(old)} already sat, threshold {a.threshold}")
    if not new or not old:
        sys.exit("nothing to compare — refusing to report a pass")
    rows = []
    for f, i, s in new:
        toks = norm(s)
        best = max(((difflib.SequenceMatcher(None, toks, o).ratio(), of, oi)
                    for of, oi, o in old), default=(0, "", ""))
        rows.append((best[0], i, f"{best[2]} in {best[1].split('/')[-1]}"))
    rows.sort(reverse=True)
    print("\nhighest similarities")
    for r, i, m in rows[:10]:
        print(f"  {r:.3f}  {i}  vs  {m}")
    # Guard against the obvious mistake: comparing a bank against the paper that
    # was rendered from it. Every stem matches at 1.000 and the gate looks broken.
    perfect = [r for r in rows if r[0] >= 0.99]
    if len(perfect) > 0.5 * len(rows):
        src = collections.Counter(r[2].split(" in ")[-1] for r in perfect).most_common(1)[0][0]
        print(f"\nSELF-COMPARISON: {len(perfect)} of {len(rows)} stems match {src} exactly.")
        print("That file was almost certainly rendered from the bank you are checking. "
              "Compare a NEW bank against PREVIOUS papers, never against its own.")
        return 1

    over = [r for r in rows if r[0] >= a.threshold]
    if over:
        print(f"\nFAIL: {len(over)} item(s) at or above {a.threshold} — rewrite these stems:")
        for r, i, m in over:
            print(f"  {r:.3f}  {i}  vs  {m}")
        return 1
    print(f"\nPASS: nothing at or above {a.threshold}; maximum is {rows[0][0]:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
