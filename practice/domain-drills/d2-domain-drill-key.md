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

---

**19. D** — One codebase with externalized per-environment config keeps behavior differences visible in config rather than duplicated across copies of the code, which is exactly what drifts out of sync over time. Separate codebases guarantee drift the moment one copy is edited and the others aren't; merging away the distinction removes a needed capability; deleting staging doesn't address the configuration question at all. *(task 2.6; concept: single_codebase_env_config; item `d2d-19`)*

---

**20. B** — Three sources with an undocumented precedence order is why editing one of them (the `.env` file) had no visible effect — the command line was silently winning. Replacing `.env` with a database doesn't fix an ordering problem; making the retry count non-configurable and removing the CLI flag each address only one of the three sources, not the missing precedence documentation itself. *(task 2.6; concept: single_source_of_truth; item `d2d-20`)*

---

**21. A** — Without a prioritized, explicit criterion for which outcome wins when resolution speed and satisfaction trade off, two reasonable engineers built toward two different targets. More training data, single ownership, and a larger `max_tokens` don't resolve a disagreement about which outcome matters more. *(task 2.1; concept: prioritized_success_criteria; item `d2d-21`)*

---

**22. C** — Explicitly scoping which data sources and access levels a vague requirement actually covers is what would have surfaced the read-only-wiki vs. read-write-database gap before implementation, not after. Code comments, a smarter model, or deferring security review don't address the requirement's own ambiguity. *(task 2.1; concept: scoping_data_access; item `d2d-22`)*

---

**23. D** — Life-cycle rigor scaling with the cost of being wrong and the audience size is why a three-person, afternoon-rebuildable tool doesn't need the same process as a customer-facing system. Uniform rigor regardless of risk, skipping requirements unconditionally, and tying rigor to the exam's domain weighting are each the wrong variable to scale against. *(task 2.2; concept: lifecycle_rigor_scales_with_risk; item `d2d-23`)*

---

**24. A** — The Messages API requires alternating roles; two consecutive `user` messages with no `assistant` turn between them violates that and returns a 400. The API doesn't merge, double-respond to, or reinterpret the second message as a system override — it simply rejects the malformed sequence. *(task 2.3; concept: message_role_alternation; item `d2d-24`)*

---

**25. B** — Native PDF support lets Claude read a document block directly, including its visual layout, up to 100 pages — no manual text conversion needed. The Messages API isn't plain-text-only, PDFs don't need to be pre-split into page images, and there's no 5-page limit. *(task 2.3; concept: native_pdf_support; item `d2d-25`)*

---

**26. C** — `max_tokens` is a required parameter on every Messages API request regardless of whether extended thinking is enabled; omitting it fails the request rather than being inferred from the thinking budget. The API doesn't auto-derive a cap, doesn't allow unlimited output, and doesn't silently disable thinking mode instead of erroring. *(task 2.3; concept: max_tokens_required_with_thinking; item `d2d-26`)*

---

**27. D** — The Message Batches API is built specifically for large, non-urgent workloads like this one and discounts them accordingly. Shrinking `max_tokens` or adding more parallel synchronous requests reduces neither the fixed cost structure nor addresses urgency; switching to streaming doesn't change per-token pricing. *(task 2.3; concept: batch_api_for_bulk_workloads; item `d2d-27`)*

---

**28. B** — Mocks that never touch the real API can't detect a genuine change in the API's response shape; the suite needs some coverage that exercises the real contract, whether live or via a fixture kept in sync with it. Mocking more of the system makes the blind spot worse, not better; removing integration tests or randomizing mock responses don't address the actual gap. *(task 2.4; concept: mocks_dont_catch_contract_drift; item `d2d-28`)*

---

**29. A** — Redacting or excluding sensitive fields before they reach a shared log is the step that was skipped; without it, anyone with log access can see customer names, account numbers, and full conversations. Retention period, compression, and where the log server sits don't address who can read the sensitive content itself. *(task 2.4; concept: redact_before_shared_logging; item `d2d-29`)*

---

**30. C** — The tool has no defensive handling for a caller omitting an optional field, so one bad call's unhandled exception takes down the entire session instead of failing just that call. Making every field mandatory just relocates the failure to a different input shape; a larger `max_tokens` and a different implementation language don't touch the missing error handling. *(task 2.4; concept: defensive_handling_optional_input; item `d2d-30`)*

---

**31. D** — Two independent, subtly different implementations of the same rounding logic is exactly what Don't Repeat Yourself exists to prevent; one shared implementation would have kept results consistent everywhere it's called. Renaming the functions, moving the logic to the model, or adding more per-copy tests all leave the duplication itself in place. *(task 2.4; concept: dry_shared_codebase; item `d2d-31`)*

---

**32. A** — Running the tool with the calling user's own credentials means the database's existing row-level access rules apply exactly as they would for any other client — no new access-control logic needed. A shared service account, no credentials at all, or an administrator credential each bypass or weaken the database's own controls instead of preserving them. *(task 2.5; concept: preserve_row_level_access; item `d2d-32`)*

---

**33. B** — Running arbitrary user-submitted code inside an isolated, resource-limited sandbox is the essential safeguard before this tool reaches production; nothing else in the option list actually contains what the code can do. A system-prompt instruction, more `max_tokens`, or a linter pass are all trust-based or cosmetic and don't stop malicious code from executing on the host. *(task 2.5; concept: sandboxed_code_execution; item `d2d-33`)*

---

**34. D** — A strict `input_schema` on a tool, with tool use forced, enforces the JSON shape structurally — Claude cannot return anything the schema doesn't allow. Repeating instructions in prose, asking users to phrase things differently, or manual sampling review are all requests or spot-checks, not guarantees. *(task 2.5; concept: structural_enforcement_over_prose; item `d2d-34`)*

---

**35. C** — Retrieving the real source documents and passing their actual identifiers into context, then requiring citations to reference one of those identifiers, ties every citation to something genuinely present rather than merely requested. Lower temperature, asking twice, and more `max_tokens` don't connect the citation to an actual retrieved source. *(task 2.5; concept: grounded_citations_via_retrieval; item `d2d-35`)*

---

**36. A** — Externalizing the system prompt into its own versioned config artifact the application loads at startup decouples a wording change from a full code deploy. Keeping multiple copies of `agent.py`, freezing the prompt after release, or slowing the deploy pipeline all leave the actual coupling between prompt and code deploy in place. *(task 2.6; concept: externalize_system_prompt; item `d2d-36`)*
