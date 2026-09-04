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

## 2. What the Exam is Actually Like (The Real Register)

Preparation materials frequently over-index on low-level syntax drills or lengthy code debugging. In reality, the live CCDV-F examination has distinct characteristics:

1. **Format:** Every scored question is **single-response (four options, one correct, no multi-select)**. There are no "Select TWO" questions on the live paper.
2. **Stem Length:** Question stems are **concise scenarios (typically 3–4 sentences, ~35–60 words)** describing a production requirement, architectural symptom, or boundary failure.
3. **No Code Snippets:** You will not be asked to debug raw Python code lines or find missing colons in stems. Questions test **architectural decisions, API mechanics, error classifications, and protocol lifecycles**.
4. **No Proprietary Model Names:** Model selection questions are framed in terms of **abstract capability tiers and tradeoffs**—quality, latency, cost per task, context requirements, and throughput—rather than ephemeral model version strings.
5. **Session Lifecycle is Tested:** Managing multiple user sessions, persistence boundaries, conversational state isolation across tenants, and session eviction are core questions.
6. **Generous Pacing:** Because stems are 3–4 sentences without code blocks, reading load is moderate. Candidates commonly finish their first pass in 50–60 minutes, leaving ample time to review flagged items.

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
