# check-item-quality.py

Checks a set of practice items for **cues that let a reader score well without
knowing anything** — the kind of defect that is invisible on inspection and
obvious the moment you measure it. See the root README's "How to use this"
section (or `HOW-TO-PRACTISE.md` in this repo) for why this matters and how it
fits into writing your own practice items.

## Usage

```
python3 tools/check-item-quality.py FILE [FILE ...]

# a sealed paper, keyed from a separate file
python3 tools/check-item-quality.py practice/mock-exam-60.md --key practice/mock-exam-60-key.md
```

Exits `0` if every set is within target, `1` if any check fails — including
when it cannot parse any items, or when it's handed a sealed paper with no key
(it refuses to report a false pass in either case).

## What each metric means

| Check | What it catches | Target |
|---|---|---|
| **Position balance** | The correct answer clustering on one letter — a chi-square test against a uniform distribution, so the tolerance scales with set size rather than using one fixed ratio that misreads small sets | below the 95% critical value, no letter above 50% of items offering it |
| **Longest run** | A stretch of consecutive items with the same answer letter — a reader who notices the streak can start guessing it | ≤ 3 |
| **Correct-is-longest** | The correct option being the longest, letting a reader skip the content entirely | within ~10 points of chance (~25% for 4 options) |
| **Length-rank spread** | The correct answer concentrating at one length rank (e.g. always 2nd-longest) even when it isn't always outright longest | no rank above ~40% |
| **Length ratio** | The correct answer's average length relative to the distractors' | 0.90–1.10 |
| **Punctuation tell** | A dash, colon or semicolon appearing mostly in correct answers (a common tic when an author writes the true statement more carefully than the distractors) | no mark in >60% of answers when it's in <40% of distractors |
| **Answer is lowest** *(ordering items only)* | The correct sequence being the numerically-lowest of the candidate orderings — a tell from authors who write the true order first and leave it looking tidiest | ≤ 40% |
| **Constant positions** *(ordering items only)* | A slot that holds the same value across every candidate ordering, which hands the reader a free position with no judgement required | none |

Ordering items (options that are bare number strings, e.g. `3, 2, 5, 4, 1`)
are detected automatically and exempted from the length-based checks, since
every option is the same length by construction — the two ordering-specific
checks run in their place.

## What a failing set looks like

Three real examples from this guide's own drafts, none of them visible until
measured:

- **The correct answer was the longest option in 94% of items** in an early
  draft of the mock exam — a reader with zero subject knowledge could have
  scored roughly 51/60 by picking the longest option every time.
- **A dash, colon or semicolon appeared in the correct answer in 89% of
  items** in the same draft — the author had, without noticing, written the
  true statement more carefully than the distractors.
- **A sequencing set was 16 of 18 answer "A", with a run of 13 in a row**,
  because the author habitually wrote the correct ordering first and
  generated distractors by shuffling it. A separate frameworks set had the
  opposite defect: **zero "A" answers at all**.

Every one of these passed a normal read-through. They only showed up once
someone ran the numbers.

## Expected item format

```
**12.** `[tag]` Stem text ...

A. option text · B. option text · C. option text        (inline, or one per line)

<details><summary>Answer</summary>
**C — ...**
...
</details>
```

If you write items in a different format, the script will report "no items
parsed" and exit non-zero rather than silently passing an empty set.
