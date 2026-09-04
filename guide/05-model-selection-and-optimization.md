# Domain 5: Model Selection, Costs, and Optimization (16.8% · 9 Items)

## Overview

Domain 5 is the second-heaviest domain of the CCDV-F exam (16.8% / 9 items). It tests model selection strategies across capability tiers, cost estimation, prompt caching invariants, token usage accounting, and asynchronous batch processing.

---

## 1. Model Selection Strategy: The "Quality First" Invariant

On the CCDV-F exam, model selection questions are framed in terms of **abstract capability tiers, quality thresholds, and latency/cost trade-offs** rather than fixed model names.

### The Optimization Sequence
1. **Meet the Quality Bar First:** Always validate task feasibility using the highest-capability tier first. Establish an accurate ground-truth baseline to verify that Claude can perform the reasoning and tool use reliably.
2. **Filter by Hard Constraints:** Latency budgets (e.g., `< 500ms` for real-time auto-complete) and cost ceilings act as **strict exclusion filters** on the candidate model pool, *not* as the initial optimization target.
3. **Trade Down Systematically:** Benchmark balanced and fast model tiers against the golden evaluation baseline. Choose the lowest-cost tier that meets your defined quality threshold.
4. **Evaluate Cost Per Completed Task:** Always compute cost per *successful business transaction* rather than raw token price. A cheaper model that fails 30% of the time and triggers retries, error loops, or human intervention is significantly more expensive than a reliable flagship model.

### Abstract Capability Tiers

| Capability Tier | Best-Fit Architectural Workloads | Trade-off Characteristics |
|---|---|---|
| **Flagship / High Intelligence** | Multi-turn agent loops, complex coding refactors, ambiguous reasoning, multi-document synthesis | Highest accuracy; higher token cost; higher latency. |
| **Balanced / Workhorse** | Enterprise search & RAG, customer support dialog, structured JSON extraction, routine coding | Optimal balance of high reasoning, moderate cost, and low latency. |
| **High-Throughput / Fast** | High-volume classification, intent routing, content moderation, simple data tagging | Lowest cost (90%+ cheaper); sub-second latency; lightweight reasoning. |

---

## 2. Prompt Caching (`cache_control`) Architectural Invariants

Prompt caching eliminates redundant computation across multi-turn conversations and repeated reference documents:

```
[tools (cached)] ──► [system prompt (cached)] ──► [document context (cached)] ──► [user message]
      ▲                        ▲                              ▲
      │                        │                              │
breakpoint 1              breakpoint 2                   breakpoint 3
```

### Core Caching Rules
* **Minimum Cacheable Prefix:** Model-dependent, typically **~512 to 4,096 tokens**. Prompts below the threshold will not cache.
* **Prefix Render Order:** Caching evaluates tokens strictly in order: `tools` $\rightarrow$ `system` $\rightarrow$ `messages`. A cache match requires an exact 100% character-by-character match from the very beginning of the prompt.
* **Ephemeral Breakpoint Limit:** You can define a maximum of **4** `cache_control: {"type": "ephemeral"}` blocks per request.
* **Time-To-Live (TTL):** The cache maintains a **5-minute TTL**. Crucially, **every cache read (hit) automatically refreshes the 5-minute TTL window**.
* **Pricing Multipliers:**
  * **Cache Creation (Write):** **1.25×** base input token cost (+25% surcharge for caching).
  * **Cache Read (Hit):** **0.10×** base input token cost (**90% discount**).

---

## 3. Usage Accounting & Billing Counter Truths

When calculating spend from API responses, inspect the `usage` block carefully:

```json
{
  "usage": {
    "input_tokens": 150,
    "cache_creation_input_tokens": 2048,
    "cache_read_input_tokens": 4096,
    "output_tokens": 320
  }
}
```

> [!CAUTION]
> **Common Billing Mistake:** `cache_creation_input_tokens` and `cache_read_input_tokens` are reported as **separate, dedicated counters outside `input_tokens`**!
>
> If your billing system computes cost as `input_tokens + output_tokens`, you will **severely under-report actual API spend** on all cached requests.
>
> Furthermore, thinking tokens are billed as output tokens under `output_tokens` (there is **no** separate `thinking_tokens` field).

### Cache Prefix Stability & Mid-Conversation Injections
* A cached block must be completely immutable. If you place dynamic timestamps, session IDs, or random UUIDs *inside* a cached prefix, the entire cache match is destroyed.
* **Mid-Conversation System Instructions:** To inject runtime operator instructions into an ongoing conversation without invalidating the top-level cached system prompt, append `{"role": "system", "content": "..."}` directly to the end of the `messages` array.

---

## 4. Message Batches API

For non-realtime, asynchronous workloads (e.g. nightly document indexing, offline evaluations):

* **Cost Discount:** **50% discount** on all input and output tokens compared to standard on-demand pricing.
* **Turnaround SLA:** Batches complete within **24 hours** (typically much faster).
* **Asynchronous Lifecycle:**
  $$\text{Submission} \;\longrightarrow\; \text{Status: } \texttt{"in\_progress"} \;\longrightarrow\; \text{Status: } \texttt{"ended"} \;\longrightarrow\; \text{Download Results}$$
* **Non-Deterministic Ordering:** Results returned from `client.messages.batches.results()` are **not guaranteed to match submission order**. Never correlate by array index (`zip(requests, results)`). Always correlate by **`custom_id`**.
* **Union Result Types:** Check `result.type == "succeeded"` before attempting to read `result.message`. Errored or canceled batch entries do not possess a `.message` property.

---

## 5. Summary Checklist: Exam Invariants for Domain 5

- [ ] Select models using a **quality-first** approach; treat latency and cost as filters.
- [ ] Measure cost per *completed business task*, not per single request.
- [ ] Minimum cacheable prefix is model-dependent (~512–4,096 tokens).
- [ ] Up to 4 ephemeral cache breakpoints per request; TTL is 5 minutes (refreshes on hit).
- [ ] Cache creation is 1.25× base input; cache read is 0.10× base input (90% discount).
- [ ] `cache_creation_input_tokens` and `cache_read_input_tokens` report outside `input_tokens`.
- [ ] Batch API yields a 50% discount; results return unordered and must be keyed by `custom_id`.
