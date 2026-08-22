#!/usr/bin/env python3
"""
check-item-quality.py — detect answer cues that let a reader score without knowing.

A practice set with an exploitable cue is worse than no practice set, because it
returns a score that feels like knowledge and is not. Every cue below was found
in a real draft of this material, and none was visible on inspection.

Checks
------
  position balance      chi-square of answer letters against uniform, so the
                        tolerance scales with the number of items
  longest run           consecutive items with the same answer letter
  correct-is-longest    how often the answer is the longest option
  length-rank spread    concentration of the answer at one length rank
  length ratio          mean answer length / mean distractor length
  punctuation tell      dash, colon or semicolon appearing mainly in answers
  answer is lowest      (ordering items) answer is the numerically lowest option
  constant positions    (ordering items) a slot identical across all options

Usage
-----
  python3 check-item-quality.py FILE [FILE ...]

Expected item format
--------------------
  **12.** `[tag]` Stem text ...

  A. option text · B. option text · C. option text        (inline, or one per line)

  <details><summary>Answer</summary>
  **C — ...**
  ...
  </details>

Ordering items whose options are bare number strings ("3, 2, 5, 4, 1") are
detected automatically; the length checks are skipped for them, because every
option is the same length by construction and the length metrics are meaningless.
The numeric-first check runs in their place.

Exit status
-----------
  0  all sets within target
  1  at least one cue outside target
"""
import collections
import re
import sys

TARGETS = """
Targets
  position balance      chi-square vs uniform below the 95% critical value,
                        and no letter above 50% of the items offering it
  longest run           <= 3
  correct-is-longest    within ~10 points of chance
  length-rank spread    no rank above ~40%
  length ratio          0.90 - 1.10
  punctuation tell      no mark in >60% of answers when <40% of distractors
  answer is lowest      ordering sets only: <= 40%
  constant positions    ordering sets only: none
"""

NUMERIC_OPTION = re.compile(r"^\d(?:\s*,\s*\d){2,}$")


def parse(path):
    """Return a list of items: {'n', 'options': {letter: text}, 'key': letter}.

    Keys are read from the same file when the answer is revealed inline. If the
    file is a sealed paper with its key elsewhere, pass --key FILE and the keys
    are matched to items by item number."""
    text = open(path, encoding="utf-8").read()
    blocks = re.split(r"\n---+\n", text)
    items = []
    for b in blocks:
        num = re.search(r"^\*\*(\d+)\.\*\*", b, re.M)
        if not num:
            continue
        options = {}
        inline = re.search(r"^A[.)]\s.*$", b, re.M)
        if inline and "·" in inline.group(0):
            for part in inline.group(0).split("·"):
                m = re.match(r"\s*([A-F])[.)]\s*(.+?)\s*$", part)
                if m:
                    options[m.group(1)] = m.group(2)
        else:
            for m in re.finditer(r"^([A-F])[.)]\s+(.+?)\s*$", b, re.M):
                options.setdefault(m.group(1), m.group(2))
        if not options:
            continue
        # Inline reveal, in any of the shapes this material uses:
        #   **C — 3, 2, 5, 4, 1.**      **B.** Description is ...
        #   **A, D** — both are ...      **B, D.** ...
        # Multi-response keys are captured in full: key is a string of every
        # keyed letter, e.g. "AD" — never just the first.
        key = None
        after = b[b.find("<details>"):] if "<details>" in b else b
        m = re.search(r"\*\*([A-F](?:\s*(?:,|&|and)\s*[A-F])*)\s*"
                      r"(?:[—\-–]|\.\*\*|\*\*)", after)
        if m:
            key = "".join(re.findall(r"[A-F]", m.group(1)))
        items.append({"n": int(num.group(1)), "options": options, "key": key})
    return items


def parse_keys(path):
    """Read an answer-key file. Supports '**26. A** — ...', '**26.** A — ...'
    and multi-response forms '**9. B,D**'; multi-response keys are captured in
    full ("BD"), never just the first letter."""
    text = open(path, encoding="utf-8").read()
    keys = {}
    for m in re.finditer(
            r"\*\*(\d+)\.?\s*((?:[A-F])(?:\s*(?:,|&|and)\s*[A-F])*)\s*\*\*",
            text):
        keys.setdefault(int(m.group(1)),
                        "".join(re.findall(r"[A-F]", m.group(2))))
    for m in re.finditer(r"\*\*(\d+)\.\*\*\s*([A-F](?:\s*,\s*[A-F])*)\b", text):
        keys.setdefault(int(m.group(1)),
                        "".join(re.findall(r"[A-F]", m.group(2))))
    return keys


def report(path, items):
    if not items:
        print(f"{path}: no items parsed — check the format section of this "
              f"script's docstring")
        print("FAIL-CLOSED: an audit that parsed nothing proves nothing. "
              "If this file contains no items, do not pass it to this check.")
        return False

    unkeyed = [it["n"] for it in items if not it["key"]]
    if unkeyed:
        print(f"\n=== {path}")
        print(f"items {len(items)} | {len(unkeyed)} with no answer revealed "
              f"in this file")
        print("FAIL-CLOSED: this looks like a sealed paper. Re-run with "
              "--key <key-file> to audit it:")
        print(f"  python3 {sys.argv[0]} {path} --key <key-file>")
        return False

    letters = sorted({l for it in items for l in it["options"]})
    keys = [it["key"] for it in items]
    counts = collections.Counter()
    for it in items:
        for l in it["key"]:           # multi-response: every keyed letter counts
            counts[l] += 1
    for l in letters:
        counts.setdefault(l, 0)
    # A letter can only be the answer in items that offer it. Multi-response
    # items carry extra options (E, F), so counting raw frequencies across a
    # mixed set makes the rare letters look suppressed when they are simply
    # rarely available. Compare rates, not counts.
    avail = collections.Counter()
    for it in items:
        for l in it["options"]:
            avail[l] += 1
    widths = collections.Counter(len(it["options"]) for it in items)

    run = mx = 1
    for a, b in zip(keys, keys[1:]):
        run = run + 1 if a == b else 1
        mx = max(mx, run)

    numeric = sum(1 for it in items
                  if all(NUMERIC_OPTION.match(v.strip())
                         for v in it["options"].values())) == len(items)

    ok = True
    print(f"\n=== {path}")
    wdesc = ", ".join(f"{w} options x{c}" for w, c in sorted(widths.items()))
    print(f"items {len(items)} | {wdesc}"
          f"{' | ORDERING SET (bare number options)' if numeric else ''}")

    # Only judge letters offered in at least a quarter of items; below that the
    # sample is too small to say anything.
    judged = [l for l in letters if avail[l] >= max(2, 0.25 * len(items))]
    dist = " ".join(
        f"{l}:{counts[l]}/{avail[l]}" for l in letters)
    rates = {l: counts[l] / avail[l] for l in judged}
    # Chi-square against uniform, so the tolerance scales with the number of
    # items. A fixed ratio rule flags ordinary sampling noise on a 60-item
    # paper and misses a real skew on an 18-item set.
    expected = sum(counts[l] for l in judged) / len(judged)
    chi2 = sum((counts[l] - expected) ** 2 / expected for l in judged) \
        if expected else 0.0
    crit = {1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49, 5: 11.07,
            6: 12.59}.get(len(judged) - 1, 12.59)
    hottest = max(rates, key=rates.get)
    balanced = chi2 <= crit and rates[hottest] <= 0.50
    print(f"positions (key/avail){dist}   {'ok' if balanced else 'OUTSIDE TARGET'}")
    print(f"                     chi2 {chi2:.2f} vs {crit} critical "
          f"(df {len(judged) - 1}); hottest letter {hottest} at "
          f"{rates[hottest]:.0%} of items offering it")
    if not balanced:
        print("                     this is a real skew, not sampling noise — "
              "rebalance before committing")
    ok &= balanced

    print(f"longest run          {mx}   {'ok' if mx <= 3 else 'OUTSIDE TARGET'}")
    ok &= mx <= 3

    if numeric:
        firsts = 0
        for it in items:
            seqs = sorted(v.strip() for v in it["options"].values())
            if seqs[0] == it["options"][it["key"][0]].strip():
                firsts += 1
        pct = 100 * firsts / len(items)
        good = pct <= 40
        print(f"answer is lowest     {firsts}/{len(items)} ({pct:.0f}%)   "
              f"{'ok' if good else 'OUTSIDE TARGET'}")
        ok &= good

        # A position that is identical across all five options is a free gift:
        # the reader gets that slot without knowing anything.
        gifts = []
        for it in items:
            seqs = [tuple(v.replace(",", " ").split())
                    for v in it["options"].values()]
            width = len(seqs[0])
            if any(len(s) != width for s in seqs):
                continue
            for pos in range(width):
                if len({s[pos] for s in seqs}) == 1:
                    gifts.append((it["n"], pos + 1))
        if gifts:
            detail = ", ".join(f"item {n} pos {p}" for n, p in gifts[:8])
            print(f"constant positions   {len(gifts)} ({detail})   OUTSIDE TARGET")
            ok = False
        else:
            print("constant positions   none   ok")

        print("length checks        skipped (all options equal length by design)")
    else:
        longest = 0
        rank_hist = collections.Counter()
        c_len = d_len = 0
        dash_c = dash_d = 0
        n_keyed = 0
        chance_sum = 0.0
        for it in items:
            lens = {l: len(v) for l, v in it["options"].items()}
            order = sorted(lens, key=lambda l: -lens[l])
            keyed = list(it["key"])
            distractors = [l for l in lens if l not in keyed]
            n_keyed += len(keyed)
            # Each keyed letter has the same chance of being longest as any
            # other offered letter; multi-response items contribute one
            # observation per keyed letter.
            chance_sum += sum(1 / len(lens) for _ in keyed)
            for kl in keyed:
                r = order.index(kl) + 1
                rank_hist[r] += 1
                if r == 1:
                    longest += 1
                c_len += lens[kl]
                if re.search(r"[—–;:]|\s-\s", it["options"][kl]):
                    dash_c += 1
            d_len += sum(lens[l] for l in distractors) / \
                max(1, len(distractors))
            if any(re.search(r"[—–;:]|\s-\s", it["options"][l])
                   for l in distractors):
                dash_d += 1

        n = len(items)
        chance = 100 * chance_sum / n_keyed
        pct = 100 * longest / n_keyed
        good = abs(pct - chance) <= 10
        print(f"correct is longest   {longest}/{n_keyed} ({pct:.0f}%, chance "
              f"{chance:.0f}%)   {'ok' if good else 'OUTSIDE TARGET'}")
        ok &= good

        spread = " ".join(f"{r}:{rank_hist[r]}" for r in sorted(rank_hist))
        top = 100 * max(rank_hist.values()) / n_keyed
        good = top <= 40
        print(f"length-rank spread   {spread}  (max {top:.0f}%)   "
              f"{'ok' if good else 'OUTSIDE TARGET'}")
        ok &= good

        ratio = (c_len / n_keyed) / max(1e-9, d_len / n)
        good = 0.90 <= ratio <= 1.10
        print(f"length ratio         {ratio:.2f}   "
              f"{'ok' if good else 'OUTSIDE TARGET'}")
        ok &= good

        pc, pd = 100 * dash_c / n_keyed, 100 * dash_d / n
        tell = pc > 60 and pd < 40
        print(f"punctuation tell     answers {pc:.0f}%, distractors {pd:.0f}%   "
              f"{'OUTSIDE TARGET' if tell else 'ok'}")
        ok &= not tell

    return ok


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    keyfile = None
    if "--key" in argv:
        i = argv.index("--key")
        keyfile = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    keys = parse_keys(keyfile) if keyfile else {}
    all_ok = True
    for path in argv:
        items = parse(path)
        if keys:
            for it in items:
                it["key"] = it["key"] or keys.get(it["n"])
        all_ok &= report(path, items)
    print(TARGETS)
    print("PASS: every set within target." if all_ok else
          "FAIL: at least one cue outside target. Fix before committing — a set "
          "with a cue returns a score that feels like knowledge and is not.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
