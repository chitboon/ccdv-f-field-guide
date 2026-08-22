# Contributing

Corrections and additions are welcome. This guide already had several errors caught and fixed during its own construction — including two definitions I had backwards and a setup sequence I had in the wrong order — so the assumption is that more remain.

## The one hard rule

**No exam content. Ever.**

Do not open an issue or a pull request containing, paraphrasing, or reconstructing questions from the live exam. Candidates agree to keep exam content confidential; contributing it here would breach that and put both your credential and this project at risk.

You can describe your experience usefully without disclosing anything. Compare:

> ❌ "Question 34 asked about a marketing manager choosing between an artifact and a spreadsheet, and the options were…"

> ✅ "The output-format items tested sequencing information *within* a document, not just choosing between artifact and inline. That distinction isn't covered here."

The second tells a guide author everything they need. The first breaches your agreement and adds nothing the second didn't.

## What's especially useful

- **Objective-level score data.** The single biggest limitation of this guide is that its objective-level analysis rests on one report. If you have your own breakdown and are willing to share which objectives came back weak or perfect — no item content needed — that materially improves the calibration.
- **Frameworks I've missed.** Anthropic's course material is organised into named, enumerable frameworks, and they are highly testable. If you find one this guide doesn't cover, that's a real gap.
- **Corrections to sourced claims.** If a quotation is inaccurate, an attribution wrong, or a definition drifted from its source, say so and point at the lesson.
- **Objectives that drew items on your form.** Knowing which objectives appear on other forms sharpens the sampling picture.
- **Practice item subjects.** Not the items — the *task domains*. "There was an ordering question about setting up a connector" is enough to build practice from.

## Standards for new practice items

- Written from the **published objectives**, never from recall of a live form.
- Correct answer **not** systematically the longest option. This guide's first draft could be beaten by picking the longest answer, which is worth knowing as a failure mode in your own item writing.
- No punctuation tells. Dashes, colons and semicolons distributed evenly across correct answers and distractors, or absent from all of them.
- Every distractor should be **wrong for a nameable reason**, and the explanation should name it.
- Tag the **trap family** the item teaches, not just the answer.
- Run `tools/check-item-quality.py` on anything you add — see `tools/README.md`.

## Distinguishing sourced from inferred

Where the guide states something Anthropic's material actually says, quote it and link the lesson. Where it synthesises, extrapolates, or reasons from a pattern, **say so inline**. The existing text uses explicit flags for this — please keep that convention. A guide that is candid about the boundary is more useful than one that sounds uniformly authoritative.

## How to submit

Issues for corrections and discussion. Pull requests for text changes — mention which section or file you touched so the diff is easy to review.
