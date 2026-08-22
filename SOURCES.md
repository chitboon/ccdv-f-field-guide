# Sources — Claude Certified Developer – Foundations (CCDV-F)

Nothing has been written for this credential yet. This file exists so the
repository matches the structure used across all four Claude certification
field guides from the start; it will be filled in as the guide is written.

## Official exam guide
- Version: 1.0, effective July 2026
- Local path: `_exam-guides/ccdv-f/` — not committed, see the restructure plan §4
- What a future guide would take from it: the eight domain names and weights,
  and the objective inventory. Objective descriptions would be paraphrases,
  never the published wording. No sample item or answer from the exam guide
  may ever appear in this repository.

## Anthropic Academy courses
Not yet determined. The captured `_anthropic-training/ai-fluency-for-builders/`
material (in the author's private workspace) is currently unused by any guide
in this collection and is worth checking against this credential's objectives
before assuming it belongs elsewhere.

## Third-party material consulted
None yet. Any third-party repository or web guide read while building this
credential must be credited here by name, link and licence, copied from the
author's private manifest, per the same policy as
[ccar-f-field-guide/SOURCES.md](https://github.com/chitboon/ccar-f-field-guide/blob/main/SOURCES.md).

## Provenance
Not applicable — no guide prose exists yet. This is a note for the author,
not a reader: the checking tools are not shipped in this repository (see
`tools/README.md` for why) and are run from the private workspace this guide
is developed in. Once there is prose, the following must pass before any of
it is committed:

```
python3 _workspace/tools/check-provenance.py publish/ccdv-f-field-guide \
  --source _anthropic-training --source _exam-guides
python3 _workspace/tools/check-provenance.py --internal publish/
```
