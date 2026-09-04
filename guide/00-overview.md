# CCDV-F Overview — Blueprint, Register, and Architectural Invariants

**Claude Certified Developer – Foundations (CCDV-F)** · 53 items · 120 minutes · 720/1000 to pass · proctored (online or test centre) · $125 · 12-month validity.

---

## 1. The Blueprint Allocation

The exam tests 8 domains weighted heavily toward application engineering and foundational integration:

| Domain | Weight | Items | Core Focus |
|---|:---:|:---:|---|
| **Domain 2 · Applications and Integration** | **33.1%** | **18** | REST mechanics, streaming, SDK client error handling, PDF/images, session lifecycle |
| **Domain 5 · Model Selection and Optimization** | **16.8%** | **9** | Quality-first tiering, latency/cost tradeoffs, prompt caching invariants, Batch API |
| **Domain 1 · Agents and Workflows** | **14.7%** | **8** | Autonomous loops, `stop_reason` control, evaluator-optimizer, subagent context isolation |
| **Domain 6 · Prompt and Context Engineering** | **11.0%** | **6** | XML delimiting, few-shot patterns, CoT reasoning, affirmative bounds, structured JSON |
| **Domain 8 · Tools and MCPs** | **10.6%** | **5** | Tool schemas, description as specification, `tool_choice`, MCP primitives & transports |
| **Domain 7 · Security and Safety** | **8.1%** | **4** | Direct/indirect injection, insecure output handling (OWASP LLM02), hooks, least privilege |
| **Domain 3 · Claude Code** | **3.1%** | **2** | `CLAUDE.md` hierarchy, settings precedence, headless `-p` mode, slash commands |
| **Domain 4 · Eval, Testing, and Debugging** | **2.6%** | **1** | Deterministic assertions vs LLM judge, failure boundary tracing, golden test sets |
| **Total** | **100%** | **53** | **Two-thirds of the paper is Domain 2 + Domain 5 + Domain 1** |

---

## 2. One Sitting's Observations — and What They Are Worth

**Read this section as a single data point, not as the specification.** The notes below come from **one candidate's sitting on 2026-09-04** (scored 926/1000). Exam forms rotate and item pools differ between candidates, so treat these as *likely* characteristics to calibrate against — never as guarantees to prepare around.

**Where this conflicts with the official guide, the official guide wins.** Anthropic's published exam guide states the item format is *"Multiple-choice and multiple-response items; each item states how many"* — so multiple-response items are part of the specification even though none appeared on this particular form. **Prepare for them.**

| Observed on this form | Confidence | How to use it |
|---|---|---|
| All items single-response; no "Select TWO" appeared | **Low** — contradicts the official spec | Still practise multi-response. Read the response-count line on every item. |
| Stems ran 3–4 sentences (~35–60 words) | Medium | Expect concise scenarios, not long code-bearing vignettes. |
| No code snippets in any stem | Medium | Study mechanisms and architecture over syntax recall — but know the shapes. |
| No model version strings; selection framed as quality / latency / cost | Medium | Learn the tradeoff reasoning, not a model lineup that will be stale by your sitting. |
| Session lifecycle was tested | Medium | Multi-session state, persistence boundaries, isolation, eviction. See Domain 2. |
| First pass finished in ~60 of 120 minutes | Low — one person, one form | Do not plan on slack. Rehearse against the clock and you lose nothing if it is generous. |

**What generalises and what does not.** The blueprint weights in §1 are published by Anthropic and are stable — build your study time on those. Everything in the table above is one observation; the further a claim goes beyond "this is what one form looked like", the less weight it deserves.

---

## 3. The Core Mental Habit: Structural Over Prompt-Level Solutions

When evaluating options on the CCDV-F exam, apply this golden invariant:

> **Prefer structural and deterministic mechanisms over prompt-level or probabilistic requests.**

| Goal | Flawed Prompt-Level Approach | Correct Structural / Architectural Mechanism |
|---|---|---|
| **JSON Output** | *"Please respond in valid JSON without markdown"* | JSON Schema in `tools` or `output_config: {format: ...}` with defensive parser |
| **Multi-Tenant Safety** | In-prompt prefix: `[Tenant 42] Process this invoice` | Separate `messages[]` array per tenant, isolated cache prefix, tenant policy in `system` |
| **Destructive Actions** | In-prompt rule: *"Do not delete tables without asking"* | Deterministic `PreToolUse` hook enforcing human approval or schema permission gates |
| **Model Selection** | Optimize for cheapest model first and hope it succeeds | **Quality-first**: verify task feasibility on highest capability tier, then trade down on cost/latency |
| **Tool Applicability** | Relying on parameter `strict: true` | Writing clear, unambiguous natural language **`description`** strings (the model's specification) |
| **Data Leakage / PII** | Instructing the model: *"Never print SSNs"* | Deterministic `PostToolUse` redaction hook scrubbing outputs before returning to the model |
| **API Error Recovery** | Retrying immediately on any exception | Catch specific SDK exceptions; backoff + jitter on 429/5xx; read `retry-after` header |

---

## 4. How to Navigate This Guide

* **[Domain Guides (01–08)](./)**: Deep technical notes detailing exact invariants, SDK mechanics, and failure modes per domain.
* **[Trap Patterns (trap-patterns.md)](./trap-patterns.md)**: The 12 core cognitive traps and discriminators tested across the blueprint.
* **[Practice Suite (../practice/)](../practice/)**: Blueprint-aligned practice sets, scenario drills, and full mock exams.
