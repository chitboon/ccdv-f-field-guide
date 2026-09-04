# Domain 4: Evaluation, Testing, and Debugging (2.6% · 1 Item)

## Overview

Domain 4 covers evaluation methodologies, LLM testing architectures, Model-as-a-Judge calibration, systematic failure isolation, and production observability.

---

## 1. The Evaluation Hierarchy: Deterministic vs. LLM Judge

Testing LLM applications requires a layered evaluation strategy:

| Evaluation Tier | Implementation Technique | Best Applied To | Characteristics |
|---|---|---|---|
| **Deterministic Code Assertions** | JSON Schema validation, Pydantic models, exact string matching, regex patterns, unit tests | Structured outputs, enum validation, required keys, numerical bounds, formatting | Zero marginal cost, deterministic, instant feedback, 100% reproducible. |
| **Model-as-a-Judge** | High-capability model prompted with explicit scoring rubrics (e.g., 1–5 scale) | Open-ended text, summary quality, tone adherence, qualitative nuance | Evaluates semantic meaning; subject to model biases; requires calibration. |

### Mitigating Model-as-a-Judge Biases
* **Verbosity Bias:** Evaluator models systematically assign higher ratings to longer, verbose responses regardless of factual accuracy.
  * **Remediation:** Anchor judge prompts with explicit rubrics that explicitly penalize extraneous fluff and reward concise, factually dense explanations.
* **Position Bias:** In pairwise comparisons, models often favor the first candidate shown.
  * **Remediation:** Evaluate candidates in both orderings (`[A, B]` and `[B, A]`) and aggregate scores.

---

## 2. Systematic Failure Isolation & Boundary Tracing

When an LLM-powered application fails in production, do not immediately mutate the system prompt. Perform boundary tracing across system layers:

```
[User Input] ──► [Prompt Layer] ──► [Claude API] ──► [Tool Input Schema] ──► [Backend Driver] ──► [Database]
                                          │                      │
                                          ▼                      ▼
                                    Boundary 1             Boundary 2
```

### Boundary Tracing Diagnostic Method
1. **Inspect Boundary 1 (Model Output):** Examine the recorded `tool_use.input` payload.
   * *Case A:* If the model emitted a valid, correctly typed argument matching the schema (e.g., `{"customer_id": "C-109"}`), the model succeeded.
2. **Inspect Boundary 2 (Integration / Backend Persistence):** Examine what the backend driver passed to the database.
   * *Symptom:* If the database row has `NULL` for `customer_id`, the bug exists in the **application integration / ORM code**, *not* in Claude's prompt or reasoning.
3. **Inspect API Status:**
   * *Symptom:* HTTP 400 with `BadRequestError` indicates malformed API request syntax (e.g. invalid message role structure), not a downstream backend crash.

---

## 3. Golden Datasets & Prompt Regression Testing

* **Prompts are Software:** Any change to system instructions, few-shot exemplars, or model tiers must be treated like code changes.
* **Golden Datasets:** Maintain a curated suite of input/output pairs representing typical production requests, difficult edge cases, adversarial injections, and historical customer bugs.
* **Continuous Integration (CI):** Run automated evaluation suites against golden datasets on every prompt commit before deploying to production.

---

## 4. Production Observability & Silent Truncation

* **Silent Truncation:** If `response.stop_reason == "max_tokens"`, the model was cut off mid-thought because it reached the token ceiling.
  * Always monitor and alert on `stop_reason == "max_tokens"` in production.
  * Resolve by increasing `max_tokens`, instructing more concise outputs, or chunking generation tasks.
* **Transaction Telemetry:** Capture request correlation IDs, full input/output token counts (`cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens`), latency, and `stop_reason` for every API invocation.

---

## 5. Summary Checklist: Exam Invariants for Domain 4

- [ ] Use deterministic code assertions for structured schemas; reserve LLM judges for open-ended text.
- [ ] Mitigate verbosity bias by scoring with concise-rewarding rubrics.
- [ ] Isolate failures at architectural boundaries before editing prompts.
- [ ] If `tool_use.input` is valid but database record is empty, fix the backend integration layer.
- [ ] `stop_reason: "max_tokens"` represents silent truncation, not normal completion.
