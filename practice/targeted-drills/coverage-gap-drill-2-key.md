# CCDV-F Coverage-Gap Drill 2 — Key and Rationales

**Answers:** 1 D · 2 B · 3 A+D · 4 D · 5 A · 6 C · 7 D · 8 B · 9 B+C · 10 C
· 11 A · 12 A · 13 B · 14 A+B · 15 D · 16 A · 17 C · 18 C+D · 19 B · 20 C

Items 3, 9, 14 and 18 need both letters to count.

## Administration protocol (for the agent running this sitting)

- **One item per question call.** `label` is the bare letter; the **full
  option text goes in the description**. No gist labels, no topic headers.
- **`header` is the item number** ("Item 12"), nothing more.
- **Immediate per-item feedback** — verdict, short rationale, running total.
- **Items 3, 9, 14, 18 are multi-response.** Lead the question text with
  *"Select TWO — tick both letters before submitting"*.
- Show the code block with the item where one is present.
- Untimed. This is a coverage sweep over previously untested objectives, so
  expect a lower first-pass score than the drilled domains — that is the
  point of it.

---

**1. D** — The SDK is a typed client over the same `POST /v1/messages`: typed exception classes per status, automatic retries (default `max_retries` 2, covering 408/409/429/5xx and connection errors), streaming event assembly with `.stream()` / `.get_final_message()`, and typed request/response objects. Those are ergonomics and correctness, not a different service. A is false — billing is per token, not per client. B is the most common wrong mental model and worth naming: the Messages API is **stateless**, and the full message history is resent on every request whether you use the SDK or curl. C inverts how pinning works — a pinned SDK protects you from *client* breaking changes, not from server-side removals. *(task 5.2; concept: sdk_wraps_rest_api; item `cg2-01`)*

---

**2. B** — Streaming is HTTP **server-sent events**: one-directional, server-to-client, and **not resumable**. A dropped connection cannot be rejoined — you resend the complete prompt and start over, which is why long generations need idempotent handling upstream. A describes a WebSocket contract the API does not offer; C invents an upgrade mechanism; D is the belief that causes teams to build reconnect logic that silently never works. *(task 5.2; concept: sse_not_websockets; item `cg2-02`)*

---

**3. A and D** — This is cache check-pointing: as the transcript grows, place a breakpoint at the end of the history *so far* on each turn, so the prefix that is already stable gets cached rather than re-billed as fresh input. **D is the constraint that makes it a rolling checkpoint** — four `cache_control` blocks per request is the ceiling, so you move it forward rather than accumulating one per turn. C is the misconception being corrected: a growing array does not invalidate a breakpoint placed *before* the growth, because matching is on the prefix — everything up to the breakpoint is unchanged, and only what follows is new. If C looked right, re-read prefix matching: appending is safe, editing is not. **B describes a single breakpoint doing the whole job** and misses that the system block and the transcript are cached against different stability profiles — collapsing to one gives up the frozen-prefix hit whenever the transcript changes. *(task 5.4; concept: cache_checkpointing; item `cg2-03`)*

---

**4. D** — Cached tokens are reported in their own counters and priced differently: `cache_creation_input_tokens` at **1.25×** the base input rate, `cache_read_input_tokens` at **0.10×**. Neither is included in `input_tokens`, so a model that sums only the two obvious fields under-reports every cached request — which is exactly the shape of a dashboard that reads low against the invoice. A invents a per-request surcharge. B is the trap for anyone who has just learned about thinking: thinking tokens are billed as **output** tokens and there is no separate `thinking_tokens` field. C describes tool-result accounting incorrectly — those tokens are ordinary input on the turn that carries them. *(task 5.4; concept: usage_fields_and_cache_pricing; item `cg2-04`)*

---

**5. A** — Context isolation through subagents is the named technique: each filing is read in a **separate context window**, and only a structured extract crosses back to the parent. The parent then reasons over 30 small extracts instead of 30 documents, so nothing is summarized twice. B raises the output ceiling, which does nothing about input pressure. C and D are both real context tools applied to the wrong cause — compaction *summarizes* the history (which is the very lossiness being complained about, applied automatically), and clearing tool results *discards* the filings, so later comparisons have nothing to draw on. The distinction to hold: compaction and tool-result clearing manage one agent's context; subagents give you more context windows. *(task 6.1; concept: context_isolation_via_subagents; item `cg2-05`)*

---

**6. C** — The description **is** the specification. The model has no other source of truth about when a tool applies, what its arguments mean, or what it returns — so `"Gets the balance."` invites exactly the misuse described. A good description states purpose, applicable and inapplicable situations, argument semantics, and the shape of the return, including error cases. A is the strongest distractor and confuses two layers: `strict: true` guarantees the *arguments validate against the schema*, not that the call was appropriate. B mixes a default value with a sampling parameter that current models reject anyway. D is half-true — system-prompt guidance helps — but it leaves the tool definition itself uninformative for every other caller and context, and tool selection is driven by the tool list. *(task 8.1; concept: tool_description_is_the_spec; item `cg2-06`)*

---

**7. D** — Prompts are software: give each version an identifier, store it with the change, record it on every request alongside the model id, and benchmark against a golden set in CI before it ships. That is what makes "which wording produced that batch" answerable and rollback mechanical. A improves logging slightly but does not version anything. B misreads caching as an audit trail — the cache is an optimization with a short TTL, not a record. C changes the model's behaviour rather than the team's traceability, and leaves the same question unanswerable next quarter. *(task 2.6; concept: prompt_versioning; item `cg2-07`)*

---

**8. B** — Plugin dependencies are dependencies: pin the version in the project's checked-in configuration so every clone resolves the same revision, exactly as you would a package. Drift across forty machines is the predictable outcome of "whatever each engineer installed", and a withdrawn hook still firing is the tell. A treats a periodic manual reinstall as a control — it is a request, not a mechanism, and it leaves the fleet inconsistent between sprints. C moves the toolkit *further* from version control by putting it in per-machine user configuration, which is the opposite of the fix. D is a genuine confusion worth clearing: an MCP server is a different distribution shape, and choosing it does not by itself pin anything. *(task 2.5; concept: plugin_version_pinning; item `cg2-08`)*

---

**9. B and C** — Two structural controls. Delimit the untrusted block and tell the model, in the system prompt, that its contents are data to summarize rather than instructions to follow. Then place the operative instruction **after** the block, so the actionable request carries recency rather than being buried above 40K tokens of hostile text. **A is the one that sounds like sanitization and is not**: escaping markup protects a *parser*, and the model is not parsing — an instruction written in plain prose survives any amount of character escaping. D mistakes more reasoning for a boundary; deeper thinking on adversarial input is not a security control. Neither of these makes the summarizer safe on its own — indirect injection is mitigated in layers, and the output side is a separate control again. *(task 6.2; concept: input_sanitization_is_delimiting_not_escaping; item `cg2-09`)*

---

**10. C** — Two halves, and the item needs both. Constrain the output with structured outputs (`output_config={"format": {...}}`, or `messages.parse()`) so the response conforms to the schema rather than depending on the model's mood — **and** still parse behind a typed failure path, because defensive parsing means the pipeline degrades rather than crashing at 3 a.m. A retries a request that has no reason to differ and burns quota. B is the field expedient everyone writes, and it fails the moment a brace appears inside a string value; it also leaves the real problem — an unconstrained output contract — in place. D is a stale reflex twice over: `temperature` is removed on current models, and it was never a format guarantee. *(task 6.3; concept: constrain_then_parse_defensively; item `cg2-10`)*

---

**11. A** — Image input is its own content block: `{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": ...}}`, placed in the user message's content array, typically before the text block. B confuses images with PDFs — `document` is the PDF/text shape, and the block type must match the file's MIME type. C invents a URL source that would have the API reach into the caller's filesystem. D flattens the encoding fields; they nest under `source`. For repeated use of the same image, the Files API takes it once and you reference it as an `image` block by `file_id`. *(task 2.3; concept: image_block_shape; item `cg2-11`)*

---

**12. A** — Trace analysis isolates the layer by comparing the artifacts at the boundary. The name is present in the recorded `tool_use.input` and absent in the row, so the model produced it correctly and the integration layer lost it — no prompt change is warranted, and a week of prompt tuning would have found nothing. B is the expensive wrong move: it modifies the layer that is working and measures over a week what the trace answers in a minute. C changes a sampling parameter that current models do not accept and would not localise the fault anyway. D asserts a single cause for a symptom with several, and a schema constrains what the *model* sends, not what the writer does with it afterwards. *(task 4.1; concept: integration_layer_vs_model_output; item `cg2-12`)*

---

**13. B** — MCP servers expose three primitives and they are not interchangeable. **Tools** are actions the model invokes (run the runbook step). **Resources** are readable content the client can pull into context (the on-call roster). **Prompts** are reusable templates the client surfaces to the user (the post-incident review starter). A collapses all three into tools, which is the default assumption and loses the distinction the objective tests. C and D permute the mapping — worth checking which one you picked, since it says whether the gap is *resources* or *prompts*. Transport is separate: `stdio` for a local child process, HTTP/SSE for a remote server. *(task 8.2; concept: mcp_three_primitives; item `cg2-13`)*

---

**14. A and B** — The supervisor pattern works because each worker's transcript stays in the worker: the parent sees results, not reasoning, which is what keeps its context bounded as the fan-out grows. And durable progress belongs in a store the supervisor reads and writes — a supervisor holding 400 repo states in its own context is the original failure wearing a hierarchy. **C describes the anti-pattern**: sharing one conversation across workers puts every worker's transcript back into the parent's context and forfeits the entire benefit. D is the comfortable assumption that costs runs — a failed worker still needs its own error handling and a redispatch policy, including a cap, or a poison repo loops forever. *(task 1.1; concept: supervisor_context_and_state; item `cg2-14`)*

---

**15. D** — Two things carry disproportionate risk in a generated diff: tests written alongside the implementation tend to assert what the code does rather than what was required, and generated changes tend to include work nobody asked for. So the review asks whether the tests exercise the *claimed behaviour*, and whether the diff exceeds the task. A discards the work and is not review. B is worth doing and is not where the risk is. C sounds rigorous and is the failure mode of large-diff review — uniform attention across 900 lines means uniform shallowness; the signal about where risk sits comes from the requirement, not from the diff's provenance. *(task 2.4; concept: reviewing_generated_code; item `cg2-15`)*

---

**16. A** — Twelve thousand independent requests with results needed by morning is the Message Batches API's exact shape: asynchronous, **50% discount**, 24-hour window, poll `processing_status` to `"ended"`, then read results keyed by `custom_id`. B is the strongest distractor because it is not wrong, only insufficient — caching the shared instruction prefix does cut cost, and combines with batching rather than substituting for it. C picks a smaller model, which may well be right on the merits but answers a cost question the stem did not ask and trades quality without evidence. D fixes wall-clock with concurrency and pays full price for latency the job does not need. *(task 2.4; concept: batch_for_non_interactive_volume; item `cg2-16`)*

---

**17. C** — Two mechanisms, two places. Standing conventions live in `CLAUDE.md` at the repository root, loaded automatically for every session in that repo and merged hierarchically with any subdirectory `CLAUDE.md`. Non-interactive execution is headless print mode — `claude -p` — which streams to stdout and composes with shell pipelines and CI steps. B re-states conventions manually every session, which is the thing `CLAUDE.md` exists to stop. A invents a `memory` key in `settings.json`; settings carry permissions, env, and hooks, not standing prose. D routes a CI invocation through MCP, which is a server-integration surface, not a runner. *(task 3.1; concept: claude_md_plus_headless_mode; item `cg2-17`)*

---

**18. C and D** — Fluency is a property of the generator, not of the facts, so "it sounded certain" carries no information — the review process has to assume that wrong output looks exactly like right output, which is what the stem observed. The structural answer is grounding: retrieve the source text, cite it, and make each figure checkable against the passage it came from. **A is the seductive one** — a self-reported confidence score is generated by the same process that produced the confident wrong figure, so thresholding on it filters nothing and adds the appearance of a control. B is worth doing and does not change the kind of problem: a lower error rate on unverifiable figures is still unverifiable figures, and spot checks remain the only thing standing between you and the one in twenty. *(task 6.3; concept: confidence_is_not_accuracy; item `cg2-18`)*

---

**19. B** — Web fetch is a **server-side** tool: declare it and it runs on Anthropic's infrastructure with no client execution loop, and it fetches URLs already present in the conversation — precisely the stated requirement. The 8.3 ordering is built-in/server tools first, then Skills, then MCP, then a custom tool; "build it yourself" is usually the wrong answer to a least-code question. A is that wrong answer with a plausible justification attached. C is reasonable engineering for a capability used across several applications, but it is more to build and operate than declaring a tool. D reaches for the sandbox to do something a declared tool already does. *(task 8.3; concept: server_tools_before_custom; item `cg2-19`)*

---

**20. C** — Isolation has to be structural: a separate `messages` array per tenant session, that tenant's policy in the top-level `system` field, and each tenant's prefix cached independently. Nothing from tenant A is ever in the array sent for tenant B, so there is no cross-reference to prevent. A and B both leave a single shared conversation carrying every tenant's content and rely on the model to partition it — an instruction is not a boundary, and the failure mode is exactly the leak reported. D clears tool results but leaves the assistant turns that already restated the other tenant's policy, so the leak survives. Session hygiene means the isolation is in the data structure, not in the prompt. *(task 2.5; concept: per_tenant_session_isolation; item `cg2-20`)*

---

## After grading

| Cluster | Items | Objective weight on the paper |
|---|---|---|
| SDK / transport fundamentals | 1, 2 | 5.2 — 6.1% |
| Caching and cost accounting | 3, 4 | 5.4 — 2.8% |
| Context strategy (isolate vs compact vs clear) | 5 | 6.1 — 3.8% |
| Tool and MCP authoring | 6, 13, 19 | 8.1/8.2/8.3 — 10.6% |
| Config and lifecycle discipline | 7, 8, 17 | 2.6/2.5/3.1 |
| Untrusted input and untrusted output | 9, 10, 18 | 6.2/6.3 — 7.2% |
| Application design | 11, 16, 20 | 2.3/2.4/2.5 |
| Isolating a failure | 12, 15 | 4.1/2.4 |
| Multi-agent structure | 14 | 1.1 — 4.5% |
