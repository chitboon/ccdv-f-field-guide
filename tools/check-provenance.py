#!/usr/bin/env python3
"""
check-provenance.py — detect reproduced Anthropic text in a learning guide.

Normalises both the guide and the captured Anthropic source material to a bare
word stream, then reports every run of N or more consecutive words that appears
in both. A long shared run means the guide is reproducing source text rather
than restating it.

Usage
-----
  python3 check-provenance.py <guide-path> [--source DIR] [--min-words 8]
  python3 check-provenance.py --internal certifications/ [--min-words 15]

  <guide-path>   file or directory to check (.md, .html, .txt, .json; JSON
                 contributes its string values)
  --source DIR   where the captured Anthropic material lives
                 (default: ../_anthropic-training and ../_exam-guides,
                  resolved relative to the working directory)
  --min-words    flag runs of this length or longer (default 8, or 15 with
                 --internal)
  --internal     different mode: compare the credential folders under the given
                 path against EACH OTHER, and report long passages shared
                 between two guides. Use this when several credentials cover
                 the same frameworks — Architect Foundations and Architect
                 Professional will overlap heavily in subject matter, and the
                 right response is a link between the two guides, not the same
                 six paragraphs in both. Threshold defaults to 15 words, because
                 short shared phrasing between sibling guides is expected.

Targets are normalised whole-file (fenced code blocks aside), so hard-wrapping
a reproduced passage across lines does not hide it; matches are mapped back to
the line where the run starts.

Exit status
-----------
  0  clean, or only allow-listed matches
  1  reproduced text found

What counts as acceptable
-------------------------
Course titles, tutorial titles and URLs are citations, not reproduction, and are
allow-listed below. Everything else at 8+ consecutive words should be rewritten.
Six- and seven-word overlaps are usually unavoidable when two texts discuss the
same named framework; they are reported at -v but do not fail the check.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

# Citations, not reproduction. Extend deliberately, never to silence a real hit.
ALLOWLIST = [
    "ai fluency framework foundations",
    "ai capabilities and limitations",
    "introduction to claude cowork",
    "claude 101",
    "ai fluency for builders",
    "academy claude com",
    "choosing the right claude model haiku sonnet opus or fable",
    "getting good at claude a research backed curriculum",
    "choosing between claude cowork or chat",
]

TEXT_EXT = {".md", ".html", ".htm", ".txt", ".json"}


def norm(s):
    """Collapse to a bare lowercase word stream, so punctuation and markup
    differences cannot hide a verbatim match."""
    s = unicodedata.normalize("NFKD", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'),
                 ("”", '"'), ("—", "-"), ("–", "-"),
                 ("…", "...")):
        s = s.replace(a, b)
    s = re.sub(r"&[a-z]+;", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)          # strip HTML tags
    s = re.sub(r"```.*?```", " ", s, flags=re.S)   # strip fenced code
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s.lower()).split())


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def read_target(path):
    """Read a target file for scanning. JSON files contribute their string
    values (recursively), so drill banks stored as JSON are checked rather
    than silently skipped; unparseable JSON falls back to the raw text."""
    raw = read(path)
    if not path.lower().endswith(".json"):
        return raw
    try:
        data = json.loads(raw)
    except ValueError:
        return raw
    parts = []

    def walk(x):
        if isinstance(x, str):
            parts.append(x)
        elif isinstance(x, (list, tuple)):
            for v in x:
                walk(v)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)

    walk(data)
    return "\n".join(parts)


def norm_with_lines(text):
    """Normalise a whole file to a word stream, tracking which source line
    each word came from. Fenced code blocks are masked BEFORE splitting into
    lines, so the stream matches whole-file norm() semantics — a verbatim
    passage cannot escape the check by being hard-wrapped across lines."""
    masked = re.sub(r"```.*?```", " ", text, flags=re.S)
    words, lines = [], []
    for lineno, line in enumerate(masked.split("\n"), 1):
        w = norm(line).split()
        words.extend(w)
        lines.extend([lineno] * len(w))
    return words, lines


def gather(paths):
    out = []
    for p in paths:
        if os.path.isfile(p):
            out.append(p)
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d != ".git"]
                for f in sorted(files):
                    if os.path.splitext(f)[1].lower() in TEXT_EXT:
                        out.append(os.path.join(root, f))
    return out


def allowed(run):
    return any(a in run for a in ALLOWLIST)


def internal_check(root, min_words=15):
    """Compare credential folders against each other and report shared prose."""
    subs = sorted(
        os.path.join(root, d) for d in os.listdir(root)
        if os.path.isdir(os.path.join(root, d)) and not d.startswith(("_", "."))
    ) if os.path.isdir(root) else []
    if len(subs) < 2:
        print(f"Only {len(subs)} credential folder(s) under {root} — nothing to "
              f"compare. This check becomes useful once a second guide exists.")
        return 0

    print(f"Comparing {len(subs)} credential folders for duplicated prose "
          f"(threshold {min_words} words):")
    for s in subs:
        print(f"  - {os.path.basename(s)}")

    texts = {}
    for s in subs:
        texts[s] = norm("\n".join(read_target(f) for f in gather([s])))

    findings = 0
    for i, a in enumerate(subs):
        for b in subs[i + 1:]:
            wa, corpus_b = texts[a].split(), texts[b]
            shared, k = [], 0
            while k < len(wa):
                best = 0
                for j in range(min(len(wa), k + 80), k + min_words - 1, -1):
                    if " ".join(wa[k:j]) in corpus_b:
                        best = j - k
                        break
                if best >= min_words:
                    shared.append((best, " ".join(wa[k:k + best])))
                    k += best
                else:
                    k += 1
            if shared:
                print(f"\n  {os.path.basename(a)} <-> {os.path.basename(b)}: "
                      f"{len(shared)} shared passage(s)")
                for n, s in sorted(shared, reverse=True)[:10]:
                    print(f"    [{n}w] {s[:120]}")
                findings += len(shared)

    print()
    if findings:
        print(f"{findings} passage(s) duplicated between credential guides.")
        print("Prefer one source of truth: keep the passage in the guide it "
              "belongs to, and link to it from the other. Duplication means two "
              "copies to keep correct, and they will diverge.")
        return 1
    print("PASS: no prose duplicated between credential guides.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--internal", action="store_true")
    ap.add_argument("--source", action="append", default=[])
    ap.add_argument("--min-words", type=int, default=None,
                    help="flag runs of this length or longer "
                         "(default 8; 15 in --internal mode)")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="also report 6- and 7-word overlaps (informational)")
    args = ap.parse_args()

    if args.internal:
        return internal_check(args.target, args.min_words or 15)

    min_words = args.min_words or 8

    sources = args.source or ["_anthropic-training", "_exam-guides",
                              "../_anthropic-training", "../_exam-guides"]
    sources = [s for s in sources if os.path.exists(s)]
    if not sources:
        sys.exit("No source material found. Pass --source DIR pointing at the "
                 "captured Anthropic material.\nWithout it this check cannot "
                 "run, and a guide must not be published unchecked.")

    corpus_files = gather(sources)
    corpus = norm("\n".join(read(f) for f in corpus_files))
    if len(corpus.split()) < 500:
        sys.exit(f"Source corpus is only {len(corpus.split())} words from "
                 f"{len(corpus_files)} files — too small to be a real check. "
                 "Is the captured material actually there?")

    print(f"Source corpus: {len(corpus_files)} files, "
          f"{len(corpus.split()):,} words")

    target_files = gather([args.target])
    if not target_files:
        sys.exit(f"No checkable files (.md/.html/.txt/.json) under "
                 f"{args.target} — refusing to report PASS over nothing.")
    print(f"Checking {len(target_files)} target file(s):")
    for f in target_files:
        print(f"  - {f}")

    floor = 6 if args.verbose else min_words
    failures = 0
    informational = 0

    for path in target_files:
        words, lines = norm_with_lines(read_target(path))
        i = 0
        while i < len(words):
            best = 0
            # longest run starting at i that appears in the corpus
            for j in range(min(len(words), i + 200), i + floor - 1, -1):
                if " ".join(words[i:j]) in corpus:
                    best = j - i
                    break
            if best >= floor:
                run = " ".join(words[i:i + best])
                if not allowed(run):
                    lineno = lines[i] if i < len(lines) else 0
                    if best >= min_words:
                        print(f"  FAIL {path}:{lineno} [{best}w] {run[:120]}")
                        failures += 1
                    else:
                        print(f"  note {path}:{lineno} [{best}w] {run[:120]}")
                        informational += 1
                i += best
            else:
                i += 1

    print()
    if failures:
        print(f"FAIL: {failures} run(s) of {min_words}+ consecutive words "
              f"reproduced from the source material.")
        print("Rewrite each in your own words. Keep the attribution; lose the "
              "sentence.")
        return 1
    print(f"PASS: no runs of {min_words}+ consecutive words reproduced.")
    if informational:
        print(f"({informational} shorter overlap(s) reported for information — "
              "usually unavoidable when naming the same framework.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
