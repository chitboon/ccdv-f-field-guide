# CCDV-F Domain Drill — Domain 2: key and rationales

Grade in one deferred pass. For every miss, note which it was: didn't know
it, misread the item, or picked the plausible-but-soft option.

---

**1. C** — Acceptance criteria have to be testable before implementation starts; "accurately" is not falsifiable, so QA had no way to check the build against the requirement until after the fact. More examples, a bigger context window, or lower temperature all patch symptoms of an undefined requirement, not the requirement itself. *(task 2.1; concept: testable_acceptance_criteria; item `d2d-01`)*

---

**2. A** — Opus's stronger reasoning comes at higher latency, which directly threatens the signed 500ms p95 SLA — a non-functional requirement independent of whether the classification itself is correct. The other three options describe requirements the proposal doesn't touch. *(task 2.1; concept: nonfunctional_latency_requirement; item `d2d-02`)*

---

**3. D** — Tracking production failures and feeding them into a revision backlog is exactly the monitoring-and-maintenance phase of the life cycle. The agent has already shipped, so this isn't first-time requirements gathering; counting failures isn't itself testing, and revising schemas next sprint isn't the design phase happening now. *(task 2.2; concept: lifecycle_maintenance_phase; item `d2d-03`)*

---

**4. B** — `retry-after` tells the client exactly how long to wait; ignoring it in favor of a fixed 2-second retry is why the second attempt failed immediately. `max_tokens`, the async client, and `temperature` have no bearing on whether a 429 is returned. *(task 2.3; concept: retry_after_header; item `d2d-04`)*

---

**5. A** — `{"type": "any"}` forces a tool call but leaves the model free to choose which of the three; `auto` also permits a plain-text reply, `{"type": "tool", "name": ...}` pins one specific tool, and omitting `tool_choice` gives no guarantee at all. *(task 2.3; concept: tool_choice_any; item `d2d-05`)*

---

**6. C** — `results_url` only populates once the batch has actually reached `ended`; checking 5 minutes in for a 40,000-item job almost certainly caught it still `in_progress`. Nothing in the scenario indicates permanent failure, an item-count limit, or a separate auth requirement. *(task 2.3; concept: batch_lifecycle_results_url; item `d2d-06`)*

---

**7. D** — `AsyncAnthropic` with the async streaming context manager is the only option that streams incrementally without blocking the event loop. Buffering the full response (A), running a sync stream inside a thread pool per request (B), and calling `get_final_message()` immediately (C) all either block or defeat the point of streaming. *(task 2.3; concept: async_streaming_client; item `d2d-07`)*

---

**8. B** — A unique, deduplicated request ID makes the retried call a no-op instead of a second charge — that's what idempotency means here. A longer timeout just delays the same failure mode; `max_tokens` and a user-facing confirmation don't address the retry itself. *(task 2.4; concept: tool_idempotency; item `d2d-08`)*

---

**9. C** — Keeping history in one instance's local memory breaks the moment the load balancer routes elsewhere; the fix is a shared store the whole fleet can read, not anything about the system prompt, the model choice, or `temperature`. *(task 2.4; concept: statelessness_across_instances; item `d2d-09`)*

---

**10. A** — One centralized configuration value means updating the model version is a one-line change instead of a 40-site hunt where two get missed. Unit tests wouldn't have caught the missed edits any faster, and `max_tokens` or the model identifier's format aren't the actual problem. *(task 2.4; concept: centralized_model_config; item `d2d-10`)*

---

**11. D** — Routing the response through `tool_use` with a strict `input_schema` gets structured output straight from a typed block instead of parsing free text that can be preceded or followed by prose. `temperature: 0` reduces variance but doesn't guarantee format; more `max_tokens` doesn't stop Claude from adding prose; asking users to resubmit doesn't fix the underlying reliability problem. *(task 2.4; concept: structured_output_via_tool_use; item `d2d-11`)*

---

**12. B** — RAG retrieves against a freshly updated index at query time, so answers never lag behind the latest closed cases. Fine-tuning nightly is expensive and still stale within the day; pasting all 2,000 memos into every prompt doesn't scale and still requires an update mechanism; relying on training data guarantees staleness. *(task 2.5; concept: rag_for_freshness; item `d2d-12`)*

---

**13. A** — An orchestrator that delegates one worker call per database and synthesizes the results is the standard fix for "one linear loop can't cover independent parallel subtasks." Shrinking `max_tokens`, rephrasing the instruction, or using a smaller model don't give the single agent any new way to actually query three databases per turn. *(task 2.5; concept: orchestrator_workers_pattern; item `d2d-13`)*

---

**14. C** — Enforcing the confirmation in the application layer, ahead of the tool's execution, guarantees the charge can't happen without it regardless of what Claude decides to do. A system-prompt instruction is not a hard guarantee; removing the tool would also block the desired autonomous booking flow; `temperature` doesn't create a control gate. *(task 2.5; concept: app_layer_guardrail; item `d2d-14`)*

---

**15. B** — The Messages API holds no server-side conversation state; every call is independent, and the calling application must resend the full history each time. None of the other options describe how the API actually behaves. *(task 2.5; concept: stateless_messages_api; item `d2d-15`)*

---

**16. D** — Prompt caching bills the repeated 50-page prefix at a fraction of cost after the first call and skips reprocessing it, cutting both latency and cost without touching the manual's content. A smaller context window, more `max_tokens`, or base64 encoding don't reduce the cost of resending the same large block every time. *(task 2.5; concept: prompt_caching_for_repeated_context; item `d2d-16`)*

---

**17. C** — Loading the key from an environment variable or secrets manager means it's never present in source to begin with, so staging and production differ only in deployment configuration. Rotation on a schedule doesn't prevent this specific exposure path; renaming a variable or committing a "read-only" file still leaves the secret in the repository. *(task 2.6; concept: secrets_not_hardcoded; item `d2d-17`)*

---

**18. A** — An externalized feature flag lets the team route a percentage of traffic and flip back instantly, with no redeploy. Deploying the new prompt to everyone at once removes the safety net the team explicitly wants; manual opt-in via support tickets doesn't give controlled percentage rollout; maintaining two codebases is exactly the redeploy-to-roll-back problem the team is trying to avoid. *(task 2.6; concept: feature_flag_rollout; item `d2d-18`)*
