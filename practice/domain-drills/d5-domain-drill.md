# CCDV-F Domain Drill — Domain 5: Model Selection and Optimization

18 items, one correct answer each. Untimed. Answer all 18 first, then grade
against the key in one pass — item by item, reading each rationale,
including the ones you got right. Every stem opens on a concrete artifact
(a model name, a token count, a dollar figure) you have to reason about,
not an abstract description.

---

**1.** `[task 5.1 · subword tokenization ratio]` A developer estimates that a 480-word product description will consume roughly 480 tokens when sent to the Messages API, budgeting `max_tokens` accordingly. The actual request comes back having consumed 640 input tokens for that same description. What most likely explains the gap between the word count and the token count?

A. Claude's context window silently truncated part of the description before tokenizing the remainder that was sent.
B. The request must have included a duplicate system prompt that got counted twice against the token budget by mistake.
C. Claude tokenizes in subwords, splitting words and punctuation into multiple tokens rather than one-to-one.
D. Prompt caching inflated the reported token count because the description was treated as a repeated prefix from an earlier call.

---

**2.** `[task 5.1 · cache minimum token threshold]` A team adds `cache_control: {"type": "ephemeral"}` to a 900-token system prompt sent with every Claude 3.5 Haiku request, expecting the standing cache discount on the second and later calls. The cache never registers a hit on any subsequent request. What is the most likely cause?

A. Ephemeral cache breakpoints only apply to Claude 3 Opus and Claude 3.5 Sonnet, not to any model in the Haiku family at all.
B. The system prompt was placed after the user turn instead of appearing first, so no prefix could be cached.
C. The five-minute cache TTL had already lapsed between the two calls, resetting the entire cached prefix back to nothing.
D. The 900-token block falls short of the 2,048-token minimum that Claude 3.5 Haiku requires for a cacheable segment.

---

**3.** `[task 5.1 · cache maximum breakpoints]` An engineer building a long RAG prompt wants to cache the system instructions, a shared knowledge-base excerpt, a per-customer document set, a conversation summary, and the latest user turn as five separate cacheable segments, placing a `cache_control` block after each one. The API rejects the request outright. What limit did this design exceed?

A. Anthropic's Messages API allows at most four ephemeral cache breakpoints per request, and this design defines five.
B. The request placed a `cache_control` breakpoint on the final user turn, which can never be marked ephemeral.
C. Each cached segment must individually exceed the per-model minimum token threshold, and one of the five segments fell short.
D. Cache breakpoints must be contiguous from the start of the prompt, and the conversation summary broke that contiguity.

---

**4.** `[task 5.1 · cache TTL reset on hit]` A cached 1,024-token system prompt receives a cache hit at the 4-minute mark after being written, and the next request then arrives 4 more minutes after that hit. Does this second request still find the segment cached?

A. No, because the five-minute TTL is fixed from the original write and never resets on subsequent hits.
B. Yes, because each cache hit resets the five-minute TTL, and only four minutes had actually elapsed since the last hit occurred.
C. Yes, because prompt caching TTLs are measured in wall-clock hours, not minutes, regardless of hit pattern.
D. No, because a cache miss at any point permanently invalidates the segment until it is rewritten from scratch.

---

**5.** `[task 5.1 · extended thinking parameter validation]` A request sets `thinking: {"type": "enabled", "budget_tokens": 800}` alongside `max_tokens: 700` for a multi-step arithmetic problem. The API returns a validation error before any generation begins. Which two configuration problems does this request actually have?

A. Extended thinking cannot ever be combined with arithmetic-style problems, and `max_tokens` was left below the model's absolute output ceiling.
B. The `thinking` parameter requires an explicit `model` field to be specified inline, and 700 tokens is far too small for any real completion at all.
C. `budget_tokens` must be expressed in characters rather than tokens, and 800 characters is too small a value to accept.
D. The budget falls below the 1,024-token minimum for extended thinking, and `max_tokens` is not strictly greater than `budget_tokens`.

---

**6.** `[task 5.1 · extended thinking temperature constraint]` A request enables extended thinking with `budget_tokens: 4000` while also setting `temperature: 0.2` to keep the final answer's wording consistent across retries. The call fails validation. What must change to keep extended thinking enabled on this request?

A. `budget_tokens` must be lowered below 1,024 whenever a non-default `temperature` is supplied.
B. `top_p` must be supplied alongside `temperature` any time extended thinking is requested.
C. `temperature` must be set to 1.0 or omitted entirely whenever extended thinking is enabled.
D. `max_tokens` must be removed from the request entirely so thinking can set its own output ceiling.

---

**7.** `[task 5.2 · temperature and determinism]` A compliance-summary endpoint must return identical wording every time it summarizes the same fixed document, since two summaries with different phrasing would trigger a manual reconciliation review. Which `temperature` setting best supports this requirement, and why?

A. `temperature: 0.0`, because it selects the highest-probability token at each step, minimizing run-to-run variability.
B. `temperature: 1.0`, because the maximum setting forces the model to converge on its single most probable output.
C. `temperature: 0.5`, because a mid-range value balances creativity against consistency for summarization tasks.
D. Temperature has no effect on wording consistency; only `max_tokens` governs repeatability.

---

**8.** `[task 5.2 · hallucination as inherent property]` A support bot confidently cites a refund-policy clause number that does not exist anywhere in the company's actual policy document, despite that document being included in context. An engineer asks whether some patch or setting exists to eliminate this kind of error entirely. What is the accurate answer?

A. Yes — setting `temperature: 0` eliminates hallucinated citations because the model becomes fully deterministic.
B. No — hallucination is an inherent consequence of generating plausible next tokens without a built-in fact-verification step.
C. Yes — enabling extended thinking guarantees that every cited clause number gets checked directly against the source document text.
D. Yes — switching to Claude Opus removes hallucination entirely, because larger models always verify facts before they respond.

---

**9.** `[task 5.2 · context degradation over long conversations]` A customer-service agent is given a system prompt instructing it to always redact card numbers, then carries on a 40-turn conversation with a customer. By turn 35, it responds to an unrelated question by repeating a customer's card number back in plain text. What phenomenon most plausibly explains this drift?

A. The Messages API silently drops system prompts entirely once a conversation exceeds roughly twenty turns in length.
B. Extended thinking was disabled partway through the conversation, removing the model's ability to follow instructions.
C. The card number was cached from an earlier turn via `cache_control`, which then bypassed the redaction instruction entirely.
D. The system prompt's instructions gradually lose relative weight as more and more recent conversation turns keep accumulating over a long history.

---

**10.** `[task 5.2 · context window as shared token budget]` A 190,000-token conversation history, together with a 4,000-token system prompt, is sent to a 200,000-token context window model, leaving only 6,000 tokens of headroom. The next user turn adds 3,000 tokens, and the developer still expects a 5,000-token completion to come back in full. What happens?

A. The request succeeds normally, because completions are generated in a token space entirely separate from the input context window.
B. The system prompt is automatically evicted first so that the full 5,000-token completion can still be produced without error.
C. The completion gets truncated or the request is rejected, since input and output share one finite context-window budget.
D. Prompt caching automatically compresses the history, since cached segments no longer count at all against the context window.

---

**11.** `[task 5.2 · tokenization limits on character-level tasks]` Asked to count how many times the letter "r" appears in a long word, Claude sometimes gives an incorrect count even though the task looks trivial to a person reading letter by letter. Which fact about how the model processes text best explains this class of error?

A. The model operates over subword tokens rather than individual characters, obscuring letter-level detail it can't directly see.
B. The model's context window is too small to hold a single long word, so part of it gets truncated before counting even begins.
C. Temperature above 0 randomly drops individual letters from the input text before the count is ever performed at all.
D. Extended thinking is strictly required for any character-counting task, and it was left disabled in this particular case.

---

**12.** `[task 5.2 · max_tokens does not govern quality]` A developer doubles `max_tokens` from 512 to 1,024 on a customer-summary endpoint, hoping the higher ceiling will make the summaries more accurate and less prone to factual slips. The output quality is unchanged afterward. What does this reveal about what `max_tokens` actually controls?

A. `max_tokens` was set too high, and lowering it back toward 512 would have improved factual accuracy.
B. `max_tokens` only caps how many tokens the completion may contain; it doesn't influence the model's reasoning or accuracy.
C. `max_tokens` controls the size of the context window available for reading the input, not just the output.
D. `max_tokens` and `temperature` must always be changed together, so accuracy regressed only because `temperature` stayed fixed.

---

**13.** `[task 5.3 · Haiku for high-volume simple tasks]` A pipeline classifies 2 million incoming support tickets per day into one of six fixed categories, a task with no need for multi-step reasoning, and the team is choosing between Claude 3.5 Haiku and Claude 3 Opus purely on the merits of this workload. Which model best fits the requirement, and why?

A. Claude 3 Opus, because its considerably larger context window would let it read much more of each ticket before classifying it correctly.
B. Claude 3 Opus, because only the most capable tier can reliably choose among six fixed categories.
C. Neither model fits, since fixed-category classification requires extended thinking to be enabled.
D. Claude 3.5 Haiku, because it is the fastest and cheapest tier, well suited to high-volume simple classification at this scale.

---

**14.** `[task 5.3 · Opus for complex reasoning tradeoff]` A legal team needs an assistant to reason through multi-step contract clause interactions across a 50-page agreement, where a wrong inference could mean a missed liability, and cost per request is a secondary concern compared to correctness. Which tradeoff should guide the model choice here?

A. Choosing Claude Opus, accepting higher cost and latency in exchange for its stronger complex-reasoning capability.
B. Choosing Claude 3.5 Haiku, since its speed advantage outweighs reasoning depth when documents are long.
C. Choosing the cheapest available tier and compensating for weaker reasoning with a larger `max_tokens` value.
D. Choosing based on `temperature` alone, since a lower `temperature` value equalizes reasoning quality across model tiers.

---

**15.** `[task 5.3 · Sonnet as balanced tier]` A product team is drafting internal weekly reports that require decent synthesis of multiple data sources but not the deepest possible reasoning, and they need response times fast enough for an interactive dashboard while keeping per-call cost well below Opus pricing. Which tier represents the intended middle-ground tradeoff for this workload?

A. Claude 3.5 Haiku, since its speed advantage makes it the correct default whenever latency matters at all.
B. Claude Opus, since any workload involving synthesis of multiple data sources requires the single most capable tier available today.
C. Claude Sonnet, since it is positioned as the balanced tier between Haiku's speed and Opus's reasoning depth and cost.
D. Any tier works identically here, since model choice only affects cost and never affects latency or reasoning quality.

---

**16.** `[task 5.3 · extended thinking as a selection tradeoff]` A team debates whether to enable extended thinking with an 8,000-token `budget_tokens` on a math-heavy tutoring endpoint that already runs on Claude Opus, knowing the thinking tokens are billed as output and add to response latency. What tradeoff does this decision actually represent?

A. Switching the underlying model tier from Opus to Haiku, since extended thinking is only compatible with the fastest tier.
B. Spending additional tokens and latency on visible step-by-step reasoning in exchange for better accuracy on multi-step problems.
C. Reducing the request's total cost, since thinking tokens are supposedly billed at a discounted rate compared to normal output tokens.
D. Guaranteeing a correct final answer, since extended thinking adds a deterministic verification pass after generation.

---

**17.** `[task 5.4 · prompt caching cost multipliers]` A 5,000-token system prompt is cached and reused across 100 requests per hour: the first request in each hour writes the cache, and the following 99 all hit it. At a base input price of $3 per million tokens, roughly what does this caching strategy cost compared to sending all 100 requests fully uncached?

A. Roughly the same overall, since cache writes and cache reads are both billed at the same standard base input token price.
B. More overall, since every one of the 100 requests must pay the 1.25x write premium independently.
C. Free, since Anthropic waives all token charges for any request that references a cached prefix.
D. Far less overall, since writes cost 1.25x base price but hits cost only 0.10x.

---

**18.** `[task 5.4 · Message Batches API cost discount]` A data-labeling job submits 200,000 non-urgent classification prompts and can tolerate results arriving up to 24 hours later, so an engineer is deciding between the standard Messages API and the Message Batches API purely on cost grounds. What should drive that choice?

A. The Message Batches API, roughly 50% cheaper for async, non-urgent work.
B. The standard Messages API, since batch requests are billed at a premium in exchange for their guaranteed faster turnaround time.
C. Either API costs the same, since Anthropic's per-token pricing does not vary by request mode.
D. The Message Batches API, but only because it removes the need for `max_tokens` on each individual request.
