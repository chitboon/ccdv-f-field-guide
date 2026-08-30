# CCDV-F Domain Drill — Domain 5: key and rationales

Grade in one deferred pass. For every miss, note which it was: didn't know
it, misread the item, or picked the plausible-but-soft option.

---

**1. C** — Claude tokenizes in subwords, so a 480-word description routinely produces more than 480 tokens as words, punctuation, and code get split into multiple chunks; there is never a 1:1 word-to-token mapping. Truncation would lower the count rather than raise it, a double-counted system prompt isn't described in the scenario, and caching doesn't inflate a token count at all. *(task 5.1; concept: subword_tokenization_ratio; item `d5d-01`)*

---

**2. D** — Claude 3.5 Haiku needs at least 2,048 tokens in a segment before it becomes cacheable, and 900 tokens falls short of that threshold regardless of how the `cache_control` block is placed. Haiku does support caching, placement isn't the issue described, and a TTL lapse would only explain occasional misses, not a cache that never hits at all. *(task 5.1; concept: cache_min_token_threshold; item `d5d-02`)*

---

**3. A** — The Messages API caps ephemeral cache breakpoints at four per request, and marking five separate segments exceeds that limit outright. The final user turn isn't specially forbidden from caching, the per-segment minimum-token rule is a separate constraint not at issue here, and breakpoints don't need to be contiguous from the start. *(task 5.1; concept: cache_max_breakpoints; item `d5d-03`)*

---

**4. B** — Every cache hit resets the five-minute TTL, so the 4-minute gap since the last hit is well within the window and the segment is still cached. The TTL isn't fixed from the original write, it's measured in minutes rather than hours, and no miss occurred in this scenario to invalidate anything. *(task 5.1; concept: cache_ttl_reset_on_hit; item `d5d-04`)*

---

**5. D** — Extended thinking requires `budget_tokens` of at least 1,024, so 800 is too low, and `max_tokens` must be strictly greater than `budget_tokens`, which 700 versus 800 fails as well — two separate violations in one request. Thinking works fine on arithmetic problems, no inline `model` field is required inside `thinking`, and `budget_tokens` is expressed in tokens, not characters. *(task 5.1; concept: thinking_budget_min_and_max_tokens; item `d5d-05`)*

---

**6. C** — When extended thinking is enabled, `temperature` must be 1.0 or left out entirely; a value like 0.2 fails validation. Lowering `budget_tokens` further doesn't fix a temperature conflict, `top_p` isn't a required companion parameter, and `max_tokens` still has to be set and simply must exceed `budget_tokens`. *(task 5.1; concept: thinking_requires_temperature_one; item `d5d-06`)*

---

**7. A** — `temperature: 0.0` makes token selection deterministic (greedy), which minimizes the run-to-run variability the compliance workflow needs. `temperature: 1.0` maximizes randomness rather than reducing it, a mid-range value still allows drift between runs, and temperature does directly govern wording variability regardless of `max_tokens`. *(task 5.2; concept: temperature_zero_deterministic; item `d5d-07`)*

---

**8. B** — Hallucination is an inherent property of next-token probabilistic generation without a built-in fact-verification step, so there is no setting that switches it off. `temperature: 0` only reduces variability, not factual grounding; extended thinking makes reasoning visible but doesn't add source verification; and a larger model reduces but does not eliminate the underlying risk. *(task 5.2; concept: hallucination_inherent_property; item `d5d-08`)*

---

**9. D** — As a conversation's history grows, earlier system instructions can lose relative weight compared to the volume of more recent turns, which is consistent with a redaction rule slipping by turn 35. The API doesn't drop system prompts at a turn-count threshold, extended thinking being off wouldn't cause this specific instruction-following lapse, and nothing in the scenario ties the card number to a cached segment. *(task 5.2; concept: context_degradation_long_conversation; item `d5d-09`)*

---

**10. C** — System prompt, conversation history, the new user turn, and the completion all draw from one shared, finite context-window token budget, so with only 6,000 tokens of headroom left, a 3,000-token turn plus a requested 5,000-token completion cannot all fit — the completion gets truncated or the call is rejected. Completions are not generated in a separate token space, the system prompt isn't auto-evicted to make room, and caching doesn't shrink what counts against the context window. *(task 5.2; concept: context_window_shared_token_budget; item `d5d-10`)*

---

**11. A** — Claude processes text as subword tokens rather than individual characters, so a single token can bundle several letters together in a way the model never directly inspects letter-by-letter, which is why character-counting tasks can go wrong. The context window is large enough to hold a single word, temperature doesn't drop letters from the input, and extended thinking isn't a strict requirement for this class of task. *(task 5.2; concept: tokenization_limits_character_tasks; item `d5d-11`)*

---

**12. B** — `max_tokens` only sets a ceiling on how many tokens the completion may contain; it has no bearing on the reasoning quality or factual accuracy of the tokens actually generated, which is why doubling it left summaries unchanged. Lowering it wouldn't have improved accuracy either, it governs output length rather than the context window available for input, and it isn't required to move in lockstep with `temperature`. *(task 5.2; concept: max_tokens_caps_length_not_quality; item `d5d-12`)*

---

**13. D** — Claude 3.5 Haiku is the fastest and cheapest tier, purpose-built for high-volume, low-complexity work like sorting 2 million tickets a day into six fixed categories. Opus's larger reasoning capacity and context window aren't needed for a task this simple, and fixed-category classification doesn't require extended thinking to be enabled at all. *(task 5.3; concept: haiku_high_volume_classification; item `d5d-13`)*

---

**14. A** — For multi-step reasoning where an incorrect inference carries real liability risk and cost is secondary, choosing Opus trades higher cost and latency for its stronger reasoning capability — exactly the intended tradeoff. Haiku's speed advantage doesn't compensate for the reasoning depth this task needs, a larger `max_tokens` value doesn't substitute for reasoning quality, and `temperature` doesn't equalize capability differences between tiers. *(task 5.3; concept: opus_complex_reasoning_tradeoff; item `d5d-14`)*

---

**15. C** — Sonnet is positioned as the balanced middle tier, offering faster responses and lower cost than Opus while handling moderate synthesis tasks better than the fastest tier alone — the fit this dashboard workload needs. Haiku isn't automatically correct whenever latency matters if the task needs more synthesis than it comfortably provides, Opus is more than this workload requires, and model tier does affect both latency and reasoning quality, not just cost. *(task 5.3; concept: sonnet_balanced_tier; item `d5d-15`)*

---

**16. B** — Enabling extended thinking means spending extra tokens and added latency on visible step-by-step reasoning in exchange for better accuracy on multi-step problems — a deliberate cost/latency-for-quality tradeoff, not a tier switch. Extended thinking works with Opus and isn't restricted to the fastest tier, thinking tokens are billed as regular output rather than at a discount, and thinking does not guarantee a correct final answer. *(task 5.3; concept: extended_thinking_tradeoff_decision; item `d5d-16`)*

---

**17. D** — The one cache write costs 1.25x the base input price while each of the 99 subsequent hits costs only 0.10x base price, a 90% discount per hit, making the hourly total far cheaper than sending all 100 requests uncached. Writes and reads are not billed at the same base rate, the write premium applies once rather than to every request, and caching is discounted, not free. *(task 5.4; concept: cache_write_read_cost_multipliers; item `d5d-17`)*

---

**18. A** — The Message Batches API carries a standing discount of roughly 50% for asynchronous, non-urgent workloads exactly like this 24-hour-tolerant labeling job, making it the cost-driven choice. The standard API isn't the discounted option here, per-token pricing does differ meaningfully between the two modes, and the batch discount has nothing to do with whether `max_tokens` is set on individual requests. *(task 5.4; concept: batch_api_cost_discount; item `d5d-18`)*
