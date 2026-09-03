# CCDV-F Current-API Code Drill — Key and Rationales

**Answers:** 1 B · 2 C · 3 A+C · 4 D · 5 A · 6 B+C · 7 C · 8 B · 9 A+D · 10 D

Items 3, 6 and 9 need both letters to count as a hit.

## Administration protocol (for the agent running this sitting)

- **One item per question call.** Option `label` is the bare letter (`A`, `B`,
  `C`, `D`); the **full option text goes in the description**. No gist labels,
  no topic sub-headers — a summarizing label does the discriminating work the
  item is meant to test, and a topic header leaks the objective.
- **`header` is the item number** ("Item 4"), nothing more.
- **Immediate per-item feedback**: verdict, short rationale from the entry
  below, running total. Not batched to the end.
- **Items 3, 6, 9 are multi-response.** Put *"Select TWO — tick both letters
  before submitting"* at the head of the question text; the picker gives no
  signal that a second choice is expected, and both letters are required.
- **Show the code block with the item.** Every stem here is a diagnosis, not a
  definition — the snippet is the question.
- Untimed is fine. This set is a coverage check on newly corrected material,
  not a pacing rehearsal.

Mark every miss as one of three kinds: **didn't know it**, **misread the
snippet**, or **knew the previous behaviour**. That third category is why this
drill exists — four of these ten have a distractor that was the correct
answer one model generation ago and is still what the 274-item bank teaches.

---

**1. B** — On Opus 5 (and Fable 5/5.1, Sonnet 5, and the 4.6/4.7/4.8 family) an assistant prefill on the last turn is rejected with a 400, which is why the failure comes before generation rather than as bad output. The current mechanism is structured outputs: `output_config={"format": {...}}` on `messages.create()`, or `client.messages.parse()` to validate against a schema in one step. **A is the bank's answer wearing a disguise** — it keeps the assistant turn, so it keeps the 400. C misreads the symptom: `stop_sequences` shapes where generation *stops* and cannot rescue a request that never generated. D names a real-looking parameter, but `output_format` is the deprecated spelling; the current one nests under `output_config`. *(task 2.1; concept: structured_outputs_replace_prefill; item `api-01`)*

---

**2. C** — `APIStatusError` is the parent class covering every non-2xx response, so this handler treats a 400 from a malformed payload exactly like a 429: it sleeps through the whole backoff curve before surfacing an error that was never going to change. The fix is a most-specific-first chain — `NotFoundError` / `BadRequestError` re-raised immediately, `RateLimitError` honouring `retry-after`, `APIStatusError` for 5xx, `APIConnectionError` for network drops. **A is the strongest distractor and is backwards**: `RateLimitError` is a *subclass* of `APIStatusError`, so 429s are already caught here — the problem is over-catching, not under-catching. B is a real-looking numerical quibble that changes nothing about which failures get retried; full jitter deliberately spans above and below the step. D is wrong on the facts (the SDK's own `max_retries` defaults to 2 and covers 408/409/429/5xx) but more importantly leaves the same non-retryable requests being retried. *(task 2.3; concept: retryable_vs_nonretryable_chain; item `api-02`)*

---

**3. A and C** — `stop_details` is populated **only** when `stop_reason == "refusal"`; on `end_turn`, `max_tokens`, `tool_use`, or `pause_turn` it is `None`, so the unguarded `.category` raises on the first ordinary response. Guard on `stop_reason` before reading it. C is the second defect in the same three lines and the one most people walk past: with adaptive thinking on, `content` can lead with a thinking block, so `content[0].text` is not reliably the verdict — iterate and match on block type. B is the near-miss worth naming: truncation is detected by `stop_reason == "max_tokens"` alone, and `stop_details` stays `None` there. D inverts the transport — a refusal is an HTTP **200** with `stop_reason: "refusal"`, which is exactly why it has to be checked after a successful call rather than caught. *(task 2.2; concept: stop_details_guard_and_block_order; item `api-03`)*

---

**4. D** — Inline base64 PDF limits are **32 MB and 600 pages** (the 100-page figure applies to 200K-context models; Opus 5 is 1M). At 240 pages and 18 MB this contract is comfortably inside both, so nothing needs splitting — the waste is re-sending it 40 times. Upload once through the Files API, reference it as `{"type": "document", "source": {"type": "file", "file_id": ...}}`, and set a cache breakpoint after it so the prefix is read rather than re-billed. **A is the stale fact this drill was built to catch** — a flat 100-page ceiling is what the bank teaches, and it turns a caching problem into an imaginary chunking problem. B is false: PDF document blocks support prompt caching, and converting to text throws away the layout the model reads. C invents a cap; the Files API is a convenience for reuse here, not a size escape hatch. *(task 2.4; concept: pdf_limits_and_file_reuse; item `api-04`)*

---

**5. A** — Mid-conversation system messages exist for exactly this: append `{"role": "system", "content": ...}` to `messages[]` and the top-level `system` field stays byte-identical, so the cached prefix survives (Opus 5, Opus 4.8, Fable 5/5.1, Mythos 5/5.1 — not Sonnet 5; no beta header). It is also the injection-safe operator channel, which is the second reason to prefer it. B misreads what a breakpoint does — caching is prefix-matched, so editing `system` invalidates everything downstream no matter where a later breakpoint sits, and four is the ceiling anyway. C is the workaround teams reach for and it puts operator policy into the user channel, where retrieved or user-supplied content can imitate it. D is the plausible-sounding surrender: prefix matching is real, but it is the *reason* the message-array channel works, not a reason nothing does. *(task 5.4; concept: mid_conversation_system_message; item `api-05`)*

---

**6. B and C** — Compaction returns blocks that stand in for the history it summarized. Appending only `resp.content[0].text` throws them away, so the next request arrives without the summarized state and the agent rediscovers work it had already done — a silent failure with no error to trace. Appending `resp.content` unchanged is the fix, and it is the single most common compaction bug. **A and D are both the other feature**: clearing old tool results is *context editing* (`context_management={"edits": [{"type": "clear_tool_uses_20250919"}]}`, beta `context-management-2025-06-27`), which clears rather than summarizes and does not ask the client to re-fetch anything; and `compact_20260112` is not a context-editing strategy to be paired with the compaction beta. If you picked either, the distinction to hold is *clears* versus *summarizes*, and that they are configured through different parameters. *(task 6.1; concept: compaction_requires_appending_content_blocks; item `api-06`)*

---

**7. C** — Anthropic-defined tools are selected by their versioned `type`, and they carry **no** `input_schema`: `{"type": "bash_20250124", "name": "bash"}`, likewise `{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}`. A definition with a `name` and an `input_schema` and no `type` is an ordinary custom tool, and naming it `bash` does not make it the built-in one — which is precisely why the behaviour looked unfamiliar rather than erroring. **D is the half-right distractor**: it correctly spots that `type` is missing and then keeps `input_schema`, which is the part that has to go. A invents a reservation — the name is not protected, and that is the trap. B describes `strict: true` doing something it does not; `strict` constrains argument validity on a custom tool's own schema and goes top-level on the tool, never on `tool_choice`. *(task 8.1; concept: anthropic_defined_tools_are_schemaless; item `api-07`)*

---

**8. B** — Agent Skills run in the code-execution sandbox: `client.beta.messages.create(...)` with `container={"skills": [...]}`, the `code_execution_20260521` tool, and the `code-execution-2025-08-25` beta. The sandbox ships `python-docx`, `python-pptx`, `matplotlib`, `pillow` and `pypdf`, so document generation is a Skills job rather than something you build. **A is the Skills-versus-Managed-Agents confusion** — `client.beta.agents` / `sessions` / `environments` are a different surface entirely, and standing up an agent, an environment and a session is far more code than this job needs. C is the "build it yourself" answer to a least-code question, which is usually wrong once server-side tools and Skills are on the table. D uses the retired beta header — the Skills and Files APIs are out of beta and live at `client.skills.*` / `client.files.*`. *(task 8.3; concept: agent_skills_call_shape; item `api-08`)*

---

**9. A and D** — The vulnerability is at the sink. Claude's text was written into `innerHTML`, so a script that rode in on the email body executes in the analyst's session. The fix belongs at the render boundary — `textContent`, or an HTML sanitizer if formatted output is genuinely needed — and rests on treating model output as untrusted data by default, exactly as you would treat a database field. **B is the discrimination this item exists for, and it is the miss from the most recent mock**: indirect prompt injection is the *input* side, and hardening it is worth doing, but a filter on inbound email does not make an unescaped rendering sink safe — model output can carry markup for reasons that have nothing to do with an attacker. C mistakes a prompt for a security control: a system instruction is a probabilistic request, not an enforced boundary, and it leaves the sink exactly as exposed. *(task 7.2; concept: insecure_output_handling_vs_injection; item `api-09`)*

---

**10. D** — Batch results are returned in **any order**, so `zip(rows, results)` pairs unrelated records — the misalignment is silent and survives any amount of polling. Key by `custom_id`, which is the field the API exists to give you for this. The `AttributeError` is the second half: each entry has a `result.type` of `succeeded`, `errored`, `canceled` or `expired`, and only `succeeded` carries `.message`. A sounds procedurally careful but the stem already states the job polls to `"ended"`; completeness was never the issue. B invents a sort option and would not explain the missing `.message` either. **C is a deliberate trap for anyone pattern-matching item 3** — leading thinking blocks are a real hazard in general, but they would produce wrong *text*, not a `NoneType`-style failure on `.message`, and they do not shuffle rows. *(task 2.2; concept: batch_results_keyed_by_custom_id; item `api-10`)*

---

## After grading

| Cluster | Items | What a miss means |
|---|---|---|
| Retired shapes the bank still teaches | 1, 4 | Re-read cram §3 before the sitting — these are the 400s |
| Clears vs summarizes | 6 | Context editing and compaction are different parameters |
| Response-object discipline | 3, 10 | Guard `stop_details`; never index `content[0]` blindly; never zip batch results |
| Surface selection | 7, 8 | `type` vs `name`; Skills vs Managed Agents |
| Security boundary | 9 | Input filtering and output escaping are separate controls |
| Error scope | 2 | Over-catching costs latency and retry budget on dead requests |
