# CCDV-F Exam Day Cram Sheet

**Claude Certified Developer – Foundations (CCDV-F)**
53 items · 120 min · Pass 720/1000
Weights: **D2 33.1% · D5 16.8% · D6 11.0% · D8 10.6% · D1 14.7% · D7 8.1% · D3 3.1% · D4 2.6%**

---

## My Drill Misses (read twice)

1. **Prompt caching: max 4 ephemeral breakpoints per request — full stop.** Not "must be contiguous from the start" (that's the *prefix-matching* rule for whether a hit registers, a different constraint entirely). Five `cache_control` blocks in one request → rejected outright, regardless of placement.
2. **A tool *definition* needs exactly 3 top-level keys: `name`, `description`, `input_schema`.** `tool_choice` is a *request-level* parameter (`auto`/`any`/`{"type": "tool", "name": ...}`) controlling whether/which tool fires — it is never part of the tool object itself. Missing `input_schema` → Claude has no argument shape to fill in, calls arrive malformed.

---
