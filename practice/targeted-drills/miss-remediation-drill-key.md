# CCDV-F Miss Remediation — Key and Rationales

Items 2, 6 and 12 need both letters. For each miss, mark whether it was the
**fact** or the **format** (multi-response items judged as a ranking rather
than four independent true/false calls).

---

**1. C** — This is the trap sitting immediately next to gap item 4. Adaptive thinking is the current form, but the *default when you omit `thinking` entirely* is not uniform: Opus 5 and Sonnet 5 run adaptive if the parameter is absent, while **Opus 4.8 and 4.7 run with no thinking at all** unless you set `{"type": "adaptive"}` explicitly. Same request, same absence of a parameter, different behaviour — and no error either way, which is what makes it a production bug rather than a 400. D is the strongest distractor and describes a real adjacent feature (see item 4), but a discarded thinking block would not make the *answer* shallower. A is the removed parameter. B inverts effort: it modulates depth, it does not switch reasoning on. *(task 5.1; concept: omitting_thinking_is_not_uniform; item `rem-01`)*

---

**2. A and D** — Two separate removals land on the same request. Sampling parameters (`temperature`, `top_p`, `top_k`) are removed on Opus 5 / 4.8 / 4.7, Sonnet 5 and Fable, and return a 400. Assistant prefill is likewise rejected across current models — use `output_config: {format: {...}}` instead. **B and C are the plausible pair, and both are wrong in an instructive way:** `max_tokens: 4096` is entirely valid (these models accept up to 128K, streaming required at the top of that range), and no current model requires an explicit `thinking` block — omitting it is legal, it just means different things per model, which is item 1. If you picked B or C, that is the ranking instinct: they *look* like the two most technical-sounding options. Judged independently against the stem, each is simply false. *(task 5.1; concept: sampling_and_prefill_both_removed; item `rem-02`)*

---

**3. B** — `effort` lives **inside `output_config`**, not top-level, which is why the engineer's field was ignored rather than rejected. Range is `low` / `medium` / `high` / `xhigh` / `max`, default `high` — so their reading was right that `xhigh` is close to the default, but only one step above it, and `xhigh` is the recommended setting for coding and agentic work on current models. C is the highest-value wrong answer to understand: effort *conceptually* replaces the fixed thinking budget, so it feels like it should live where `budget_tokens` lived, inside `thinking`. It does not. D describes the older Opus 4.6 / Sonnet 4.6 range, before `xhigh` arrived with Opus 4.7. *(task 5.1; concept: effort_lives_in_output_config; item `rem-03`)*

---

**4. D** — `thinking.display` defaulted to `"summarized"` on Opus 4.6 / Sonnet 4.6 and defaults to **`"omitted"`** on Opus 5 / 4.8 / 4.7, Sonnet 5 and Fable — a silent change that presents exactly as described: a long quiet pause, then output. `display` governs visibility only; thinking still happens and is still billed, which the stem's "billing is unchanged" is there to tell you. Set `display: "summarized"` explicitly if you stream reasoning to users. A is contradicted by that same clue. C is worth rejecting firmly — reverting to a fixed budget is not available on these models at all (gap item 4). *(task 5.1; concept: thinking_display_default_changed; item `rem-04`)*

---

**5. A** — Both halves of their setup rule it out, and each is a separate fact worth holding. Fast mode is **Opus 5 and Opus 4.8 only** — it was *removed* on Opus 4.7, where `speed: "fast"` now errors — and it runs on the Claude API and Managed Agents only, not on Bedrock, Vertex, Foundry, or Claude Platform on AWS. B is the most tempting because the Mantle client genuinely is the right Bedrock client for everything else; the platform restriction is not a client-selection problem. D invents cross-platform billing parity. *(task 5.1; concept: fast_mode_model_and_platform_limits; item `rem-05`)*

---

**6. B and C** — A and C are direct opposites, so the item forces a decision rather than allowing a ranking: **switching `speed` invalidates the prompt cache**, so A is false and C is true. And fast mode carries its **own rate limit**, separate from standard requests to the same model, so capacity planning does not carry over either. D is the operationally important false one: there is no automatic fallback. On a fast-mode 429 you either honour `retry-after` or drop `speed` and reissue at standard — and that reissue pays a cache write, which is C again from the other direction. Fast mode is also excluded from Batch and Priority Tier. *(task 5.1; concept: fast_mode_cache_and_rate_limit; item `rem-06`)*

---

**7. D** — Two routes, two different problems, two different levers. The overnight job is latency-insensitive and over budget: that is the Batch API's exact case — asynchronous, 50% discount, 24-hour window. The chat endpoint is latency-bound and within budget: fast mode buys throughput at premium price, and lower effort buys latency by reducing thinking depth. A is the inversion and the one to be able to reject instantly — Batch's 24-hour window is disqualifying for live chat, and paying fast mode's premium on an overnight job spends money to solve a problem that does not exist. C is wrong twice: raising effort increases spend on a route that is already over budget, and **Priority Tier is not supported on `claude-opus-5`** (it is on Fable 5 and Opus 4.8), so that half fails validation. *(task 5.4; concept: match_lever_to_route_constraint; item `rem-07`)*

---

**8. B** — Read the requirements as a set: a scheduler they do not run, a workspace persisting across turns, and per-run config pinning. Managed Agents supplies all three — scheduled deployments fire sessions on a cron cadence with per-firing run records, each session provisions a container, and a session pins to an agent version. What makes this item harder than gap item 1 is that **A, C and D are all workable engineering**; they are rejected by the last sentence, not by being wrong. Each puts infrastructure back on a two-person team: a VM to keep alive, a CI scheduler to own, or a serverless function plus an object-storage state layer they now maintain. *(task 1.2; concept: managed_agents_supplies_scheduler_and_workspace; item `rem-08`)*

---

**9. C** — The Claude Agent SDK (`claude-agent-sdk` / `@anthropic-ai/claude-agent-sdk`) is Claude Code packaged as a library: built-in Read/Write/Edit/Bash/Glob/Grep/WebSearch/WebFetch, the loop, context management, subagents and permissions, running on infrastructure you own. That matches every clause of the stem. **D is the misconception this whole cluster turns on, and it is the mirror image of your item 1 miss:** the tool runner has *no* built-in tools — it loops over tools you define. Conflating the two is easy because both are harness-only and both are self-hosted; the difference is whether a tool surface comes with it. A gets file access wrong (code execution runs in Anthropic's sandbox, not their repo). B is false on its face given C exists. *(task 1.2; concept: agent_sdk_ships_builtin_tools; item `rem-09`)*

---

**10. A** — The tool runner's real argument over a hand-written loop is the per-turn hooks: approval gates before execution, logging, error interception, result modification (attaching `cache_control`, for instance), retries, streaming and compaction — the things teams end up hand-rolling badly inside a manual loop. B and C are precisely what it does **not** provide, and naming them is how you check your own model of it: no built-in tools (that is the Agent SDK) and no managed deployment (that is Managed Agents). D names a real feature that is available on the Messages API independently, so it is no argument for the runner. *(task 1.2; concept: tool_runner_per_turn_hooks; item `rem-10`)*

---

**11. D** — Run the four criteria: complexity (the task is fully specifiable — two named fields, fixed schema), value, viability, cost of error. Nothing here is open-ended or model-directed, so there is no exploration for an agent loop to do; this is a single call per document, and at 200,000 documents it is a single call per document *submitted through Batch*. A is the seductive one — volume feels like a reason to add machinery, when it is actually a reason to keep the per-unit path as cheap and simple as possible. B still pays the loop's overhead to reach the same answer. C has a false premise: agents and batch processing are not mutually exclusive, they are simply both unnecessary complexity here. *(task 1.1; concept: specifiable_task_needs_no_agent; item `rem-11`)*

---

**12. A and C** — This states the axis your item 1 miss turned on, so treat it as the summary card. **Harness** is the loop plus context management; **deployment** is the infrastructure it runs on. The manual loop supplies neither. The tool runner and the Agent SDK both supply a harness and leave hosting to you — which is exactly why they are easy to confuse with each other, and why the tool surface (item 9) is the thing that separates them. Managed Agents is the only one of the four supplying both. B is the inversion worth rejecting explicitly: the container is Anthropic-hosted, and that *is* the deployment half. D reverses both axes. *(task 1.2; concept: harness_vs_deployment_summary; item `rem-12`)*

---

## If you missed these

| Missed | Read |
|---|---|
| 1, 2, 3, 4 | You have the current model-options surface roughly right but not the per-model boundaries. The cram sheet §3 and §5 lines on thinking, effort and display are the ones to re-read. |
| 5, 6, 7 | Fast mode's constraints, not its concept, are the gap — model eligibility, platform exclusions, separate rate limit, cache invalidation on toggle. |
| 8, 9, 10, 12 | The harness/deployment axis has not settled. Item 12's rationale is the summary card; read it last. |
| 2, 6, or 12 while getting the single-answer items right | Format, not knowledge. On the paper, take each option in a Select TWO and ask "is this statement true of this stem" before comparing any two options to each other. |
