# Domain 5: Model Selection, Costs, and Optimization (16.8% Weight · 9 Items)

## Overview
Domain 5 evaluates model capabilities across the Claude family (Haiku, Sonnet, Opus), cost management, prompt caching, and batch processing.

---

## Model Selection Matrix

| Model | Primary Best Fit | Latency / Cost Tradeoff |
|---|---|---|
| **Claude 3.5 Haiku** | High-throughput classification, simple extraction, lightweight tools | Lowest cost, lowest latency |
| **Claude 3.5 Sonnet** | Complex reasoning, enterprise coding, multi-turn agent loops | Industry-leading benchmark performance |
| **Claude 3 Opus** | Deep analysis, multi-step nuanced reasoning | Highest intelligence tier for complex synthesis |

---

## Performance & Cost Optimization Invariants

### 1. Prompt Caching (`cache_control`)
- **Minimum Cache Thresholds:** 1,024 tokens for Claude 3.5 Sonnet / Opus; 2,048 tokens for Claude 3.5 Haiku.
- **Cache Writes & Reads:** `cache_creation_input_tokens` vs `cache_read_input_tokens`.
- **Structure:** Place static background documents, tools, and system prompts before dynamic user turns.

### 2. Message Batches API
- Asynchronous batch processing for non-realtime workloads.
- **Cost Reduction:** 50% discount on input and output tokens compared to standard synchronous endpoints.
- **Turnaround:** Completed within 24 hours.
