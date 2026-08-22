# CCDV-F Field Guide

An unofficial study guide for the **Claude Certified Developer – Foundations** (CCDV-F) exam.

**Nothing has been written for this credential yet.** This repo exists as a
placeholder recording the exam facts and the tooling this collection's guides
are built with, so it's ready to fill in.

One of four Claude certification field guides, each in its own repository and
built to the same standard: [ccao-f-field-guide](https://github.com/chitboon/ccao-f-field-guide) (Associate – Foundations, **complete** — start there if you want to see the finished shape of these guides), [ccar-f-field-guide](https://github.com/chitboon/ccar-f-field-guide) (Architect – Foundations, in progress), [ccar-p-field-guide](https://github.com/chitboon/ccar-p-field-guide) (Architect – Professional, not started).

---

## No exam content. Ever.

Whatever gets written here will contain **no questions, answers, or content
from the live exam**, and it never will. Candidates agree to keep exam
content confidential, so anything advertising itself as "real exam
questions" or a "dump" is either fabricated or a breach — and using it puts
your credential at risk. Any practice item eventually added here will be
written from the published exam objectives.

## The exam

- 53 items
- 720 on a 100–1000 scale to pass
- $125, 12 months' validity
- Proctored, online or at a test centre

Eight domains and their weights, from the published exam guide:

| Domain | Weight |
|---|---|
| Agents and Workflows | 14.7% |
| Applications and Integration | 33.1% |
| Claude Code | 3.1% |
| Eval, Testing, and Debugging | 2.6% |
| Model Selection and Optimization | 16.8% |
| Prompt and Context Engineering | 11.0% |
| Security and Safety | 8.1% |
| Tools and MCPs | 10.6% |

This is a notably lopsided blueprint compared with the other three
credentials: **Applications and Integration alone is a third of the paper**,
while Claude Code and Eval/Testing/Debugging together are under 6% — roughly
three items between them on a 53-item form. Any guide for this credential
should allocate effort to match, not spread evenly across domains.

## What's here

Nothing yet — this file, `SOURCES.md`, and `tools/check-item-quality.py`
(copied in ahead of any content it would check, so it's ready the moment
there's a practice set to audit — see `tools/README.md`).

## How to use this

There's nothing to practise yet. Once there is, the same approach as the
other guides in this collection applies: point Claude or Kimi at this cloned
repo, write new items from the published objectives (never from a live
exam), and run `python3 tools/check-item-quality.py <file>` before trusting
any set. See
[ccao-f-field-guide/HOW-TO-PRACTISE.md](https://github.com/chitboon/ccao-f-field-guide/blob/main/HOW-TO-PRACTISE.md)
for the full method, including the paste-ready prompts, and the real
cue-defect numbers that make the audit step non-optional.

## Sources

See [SOURCES.md](SOURCES.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The one hard rule: **no exam content, ever.**

## Licence

[CC BY 4.0](LICENSE) for the original writing, once there is any. Quoted Academy material remains Anthropic's.

---

Compiled by **Chit Boon Lee** and **Claude**.
Unofficial. Not affiliated with, endorsed by, or sponsored by Anthropic.
