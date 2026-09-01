# CCDV-F Mock Exam 1 — Key and Rationales

Grade in one pass after finishing all 53 items. For every miss, note
whether it was: didn't know it, misread the item, or picked the
plausible-but-soft option. Multi-response items require both correct
letters to count as a hit — partial credit isn't how the real exam scores
"select N" items either.

---

**1. B** — Deciding the next action from what a tool returned, rather than executing a preset order, is exactly what separates an agent loop from a fixed workflow. Tool count, temperature, and the Batches API describe implementation details unrelated to that control-flow distinction. *(task 1.1; concept: autonomous_loop_vs_chain; item `mock1-01` (source: d1#1))*

---

**2. D** — `tool_use` means Claude is asking the loop to run a tool and expects a `tool_result` back; `end_turn` means the model considers its response complete and the loop should stop and hand the text to the user. Treating them as equivalent, reversed, or as an error signal all misread what `stop_reason` communicates. *(task 1.1; concept: stop_reason_interpretation; item `mock1-02` (source: d1#2))*

---

**3. D** — A clear parameter description plus structured, inspectable success and error responses is what lets Claude reason about correct calls and diagnose failures. Tool name length, a higher `max_tokens`, and removing the parameter don't address the missing description or the unhandled-exception behavior at all. *(task 1.2; concept: tool_interface_design; item `mock1-03` (source: d1#5))*

---

**4. A** — Returning distinct, structured content per failure type is what lets the model tell a decline apart from invalid input or a timeout and pick the right recovery action. A single unlabeled boolean, server-only logging, or a fixed retry count all withhold the very detail the model needs to decide. *(task 1.2; concept: structured_tool_error_signals; item `mock1-04` (source: d1#6))*

---

**5. C** — Defining the agent's role, its boundaries, and when to invoke its tools is what keeps behavior scoped; a generic "helpful assistant" line gives the model no basis for staying on-topic. A longer greeting, a banned-word list, and a higher temperature don't constrain scope or mention the available tools. *(task 1.2; concept: system_prompt_role_scoping; item `mock1-05` (source: d1#7))*

---

**6. B** — A coordinator call that decomposes the repository into per-file subtasks, delegates each to a worker call, and synthesizes the diffs is the orchestrator-workers pattern. Prompt chaining is a fixed linear sequence, evaluator-optimizer relies on a critic scoring a draft, and a single linear agent wouldn't delegate subtasks to separate calls at all. *(task 1.3; concept: orchestrator_workers_pattern; item `mock1-06` (source: d1#11))*

---

**7. D** — A generator drafting the headline and a separate critic scoring it, looping until a quality bar is cleared, is the evaluator-optimizer pattern by definition. Orchestrator-workers splits a task into parallel subtasks, routing dispatches by category, and parallelization runs independent drafts at once rather than looping generator feedback. *(task 1.3; concept: evaluator_optimizer_pattern; item `mock1-07` (source: d1#12))*

---

**8. C** — A single system prompt with two tools handling one lookup and one draft is already within a linear agent's scope; orchestration earns its overhead once independent subtasks or genuine complexity appear, not preemptively. Treating multi-agent design as always superior, tying it to tool count, or claiming a single agent can't call more than one tool are all incorrect generalizations. *(task 1.3; concept: single_agent_vs_orchestration; item `mock1-08` (source: d1#13))*

---

**9. C** — Acceptance criteria have to be testable before implementation starts; "accurately" is not falsifiable, so QA had no way to check the build against the requirement until after the fact. More examples, a bigger context window, or lower temperature all patch symptoms of an undefined requirement, not the requirement itself. *(task 2.1; concept: testable_acceptance_criteria; item `mock1-09` (source: d2#1))*

---

**10. A** — Opus's stronger reasoning comes at higher latency, which directly threatens the signed 500ms p95 SLA — a non-functional requirement independent of whether the classification itself is correct. The other three options describe requirements the proposal doesn't touch. *(task 2.1; concept: nonfunctional_latency_requirement; item `mock1-10` (source: d2#2))*

---

**11. D** — Tracking production failures and feeding them into a revision backlog is exactly the monitoring-and-maintenance phase of the life cycle. The agent has already shipped, so this isn't first-time requirements gathering; counting failures isn't itself testing, and revising schemas next sprint isn't the design phase happening now. *(task 2.2; concept: lifecycle_maintenance_phase; item `mock1-11` (source: d2#3))*

---

**12. A, C** — `RateLimitError` and `InternalServerError` are both transient conditions that can resolve on their own, so a backoff retry makes sense. `BadRequestError` and `AuthenticationError` describe a malformed request or bad credential — retrying the exact same request changes nothing, so failing fast is correct instead. *(concept: retryable_vs_nonretryable_exceptions; item `mock1-12`)*

---

**13. A** — `{"type": "any"}` forces a tool call but leaves the model free to choose which of the three; `auto` also permits a plain-text reply, `{"type": "tool", "name": ...}` pins one specific tool, and omitting `tool_choice` gives no guarantee at all. *(task 2.3; concept: tool_choice_any; item `mock1-13` (source: d2#5))*

---

**14. C** — Result files are only provisioned on Anthropic's storage backend once `processing_status` transitions to `ended`; querying 5 minutes in while the batch is still `in_progress` causes result download requests to return a 404. *(task 2.3; concept: batch_lifecycle_results_url; item `mock1-14` (source: d2#6))*

---

**15. D** — `AsyncAnthropic` with the async streaming context manager is the only option that streams incrementally without blocking the event loop. Buffering the full response (A), running a sync stream inside a thread pool per request (B), and calling `get_final_message()` immediately (C) all either block or defeat the point of streaming. *(task 2.3; concept: async_streaming_client; item `mock1-15` (source: d2#7))*

---

**16. A** — In mutation tools (such as fund transfers), validating client-supplied deduplication/idempotency keys ensures duplicate retry calls return the existing transaction record rather than executing a second debit. Socket timeouts and backoff retry delays do not eliminate the root cause of duplicate executions. *(task 2.4; concept: tool_idempotency_keys; item `mock1-16` (source: d2#8))*

---

**17. B** — In horizontally scaled cloud fleets, dialogue history must be externalized to a shared state store (e.g. Redis, DynamoDB) so any container instance can retrieve and re-hydrate the full message context on incoming requests. Sticky sessions are fragile to container crashes and scaling events. *(task 2.4; concept: externalized_state_across_instances; item `mock1-17` (source: d2#9))*

---

**18. A** — Defining model strings in a centralized configuration module or registry guarantees that updating the model version is an atomic, single-line change referenced uniformly across all call sites, eliminating multi-site drift. *(task 2.4; concept: centralized_model_configuration; item `mock1-18` (source: d2#10))*

---

**19. D** — Routing the response through `tool_use` with a strict `input_schema` gets structured output straight from a typed block instead of parsing free text that can be preceded or followed by prose. `temperature: 0` reduces variance but doesn't guarantee format; more `max_tokens` doesn't stop Claude from adding prose; asking users to resubmit doesn't fix the underlying reliability problem. *(task 2.4; concept: structured_output_via_tool_use; item `mock1-19` (source: d2#11))*

---

**20. B** — RAG retrieves against a freshly updated index at query time, so answers never lag behind the latest closed cases. Fine-tuning nightly is expensive and still stale within the day; pasting all 2,000 memos into every prompt doesn't scale and still requires an update mechanism; relying on training data guarantees staleness. *(task 2.5; concept: rag_for_freshness; item `mock1-20` (source: d2#12))*

---

**21. A** — An orchestrator that delegates one worker call per database and synthesizes the results is the standard fix for "one linear loop can't cover independent parallel subtasks." Shrinking `max_tokens`, rephrasing the instruction, or using a smaller model don't give the single agent any new way to actually query three databases per turn. *(task 2.5; concept: orchestrator_workers_pattern; item `mock1-21` (source: d2#13))*

---

**22. C** — Enforcing the confirmation in the application layer, ahead of the tool's execution, guarantees the charge can't happen without it regardless of what Claude decides to do. A system-prompt instruction is not a hard guarantee; removing the tool would also block the desired autonomous booking flow; `temperature` doesn't create a control gate. *(task 2.5; concept: app_layer_guardrail; item `mock1-22` (source: d2#14))*

---

**23. B** — The Messages API holds no server-side conversation state; every call is independent, and the calling application must resend the full history each time. None of the other options describe how the API actually behaves. *(task 2.5; concept: stateless_messages_api; item `mock1-23` (source: d2#15))*

---

**24. D** — Prompt caching bills the repeated 50-page prefix at a fraction of cost after the first call and skips reprocessing it, cutting both latency and cost without touching the manual's content. A smaller context window, more `max_tokens`, or base64 encoding don't reduce the cost of resending the same large block every time. *(task 2.5; concept: prompt_caching_for_repeated_context; item `mock1-24` (source: d2#16))*

---

**25. A, B** — Loading the key from an environment variable or secrets manager keeps it out of source entirely, and a placeholder-only `.env.example` documents the required variables without exposing a real key. A committed config file still puts the real secret in the repository regardless of a read-only flag, and printing it to logs exposes it to anyone with log access. *(concept: secrets_handling_practices; item `mock1-25`)*

---

**26. A** — An externalized feature flag lets the team route a percentage of traffic and flip back instantly, with no redeploy. Deploying the new prompt to everyone at once removes the safety net the team explicitly wants; manual opt-in via support tickets doesn't give controlled percentage rollout; maintaining two codebases is exactly the redeploy-to-roll-back problem the team is trying to avoid. *(task 2.6; concept: feature_flag_rollout; item `mock1-26` (source: d2#18))*

---

**27. A, B** — Enterprise-managed policy sits above both project and user settings in precedence, and CLAUDE.md files at different directory levels combine rather than one silently overriding the other. User settings do not automatically outrank project settings, and Claude Code doesn't resolve conflicts by file modification time. *(concept: settings_and_memory_hierarchy; item `mock1-27`)*

---

**28. B** — Piping a prompt in and running Claude Code in print mode returns the result straight to standard output with no interactive UI at all, which is exactly what a scriptable CI step needs. Scraping a `tmux` pane, saving a transcript from inside the REPL, and driving the interactive session with keyboard automation all still depend on an interactive terminal existing in the first place. *(task 3.1; concept: headless_print_mode; item `mock1-28` (source: d3#2))*

---

**29. C** — Code-based assertions work when there's one shape of right answer, like an enum; open-ended text needs a second LLM call scoring it against a rubric instead. Extending the schema can't judge free-text quality, dropping the field loses coverage entirely, and using a judge for the enum too throws away a cheaper, deterministic check that already works. *(task 4.1; concept: code_assertion_vs_judge; item `mock1-29` (source: d4#1))*

---

**30. C** — Claude tokenizes in subwords, so a 480-word description routinely produces more than 480 tokens as words, punctuation, and code get split into multiple chunks; there is never a 1:1 word-to-token mapping. Truncation would lower the count rather than raise it, a double-counted system prompt isn't described in the scenario, and caching doesn't inflate a token count at all. *(task 5.1; concept: subword_tokenization_ratio; item `mock1-30` (source: d5#1))*

---

**31. A, C** — Extended thinking has two independent numeric requirements: `budget_tokens` must clear a 1,024-token floor (900 doesn't), and `max_tokens` must exceed `budget_tokens` (850 doesn't exceed 900) — this request fails both at once. Temperature must be 1.0 or omitted, never forced to 0.0, and there's no separate `model` field requirement for thinking. *(concept: extended_thinking_dual_constraint; item `mock1-31`)*

---

**32. A** — The Messages API caps ephemeral cache breakpoints at four per request, and marking five separate segments exceeds that limit outright. The final user turn isn't specially forbidden from caching, the per-segment minimum-token rule is a separate constraint not at issue here, and breakpoints don't need to be contiguous from the start. *(task 5.1; concept: cache_max_breakpoints; item `mock1-32` (source: d5#3))*

---

**33. A** — `temperature: 0.0` makes token selection deterministic (greedy), which minimizes the run-to-run variability the compliance workflow needs. `temperature: 1.0` maximizes randomness rather than reducing it, a mid-range value still allows drift between runs, and temperature does directly govern wording variability regardless of `max_tokens`. *(task 5.2; concept: temperature_zero_deterministic; item `mock1-33` (source: d5#7))*

---

**34. B** — Hallucination is an inherent property of next-token probabilistic generation without a built-in fact-verification step, so there is no setting that switches it off. `temperature: 0` only reduces variability, not factual grounding; extended thinking makes reasoning visible but doesn't add source verification; and a larger model reduces but does not eliminate the underlying risk. *(task 5.2; concept: hallucination_inherent_property; item `mock1-34` (source: d5#8))*

---

**35. D** — As a conversation's history grows, earlier system instructions can lose relative weight compared to the volume of more recent turns, which is consistent with a redaction rule slipping by turn 35. The API doesn't drop system prompts at a turn-count threshold, extended thinking being off wouldn't cause this specific instruction-following lapse, and nothing in the scenario ties the card number to a cached segment. *(task 5.2; concept: context_degradation_long_conversation; item `mock1-35` (source: d5#9))*

---

**36. D** — Claude 3.5 Haiku is the fastest and cheapest tier, purpose-built for high-volume, low-complexity work like sorting 2 million tickets a day into six fixed categories. Opus's larger reasoning capacity and context window aren't needed for a task this simple, and fixed-category classification doesn't require extended thinking to be enabled at all. *(task 5.3; concept: haiku_high_volume_classification; item `mock1-36` (source: d5#13))*

---

**37. A** — For multi-step reasoning where an incorrect inference carries real liability risk and cost is secondary, choosing Opus trades higher cost and latency for its stronger reasoning capability — exactly the intended tradeoff. Haiku's speed advantage doesn't compensate for the reasoning depth this task needs, a larger `max_tokens` value doesn't substitute for reasoning quality, and `temperature` doesn't equalize capability differences between tiers. *(task 5.3; concept: opus_complex_reasoning_tradeoff; item `mock1-37` (source: d5#14))*

---

**38. A, B** — The Batch API's whole value proposition is the ~50% discount for asynchronous, non-urgent work, and results genuinely aren't available until the batch reaches `ended` — checking earlier returns a 404. It's a discount, not a premium, and `in_progress` is a real intermediate lifecycle state, not skipped. *(concept: batch_api_accuracy; item `mock1-38`)*

---

**39. B** — Wrapping `return_policy_doc` in `<policy_docs>` and behavioral constraints in `<guidelines>` provides unambiguous structural demarcation in the prompt string, preventing context contamination. Shortening the document or appending stop sequences does not resolve the lack of structural demarcation. *(task 6.1; concept: xml_section_delimiting; item `mock1-39` (source: d6#1))*

---

**40. C** — Live input/output example pairs show the exact formatting rather than describing it, which is what few-shot prompting is for and is far more reliable than prose alone. Repeating the same prose instruction three times doesn't add new information; a larger `max_tokens` addresses truncation, not formatting drift; and moving the instruction to the user turn changes where it lives, not whether it's demonstrated. *(task 6.1; concept: few_shot_pattern_demonstration; item `mock1-40` (source: d6#2))*

---

**41. D** — Appending `{"role": "assistant", "content": "{"}` as the final element of `messages` natively forces Claude to continue emitting JSON tokens from that opening character, bypassing any preamble. The application then parses `"{" + response.content[0].text`. Stop sequences, user prompt tricks, or invalid `"role": "system"` inside `messages` do not provide native assistant continuation. *(task 6.1; concept: assistant_prefill; item `mock1-41` (source: d6#3))*

---

**42. D** — Policy, tone, and escalation rules are stable across turns, which is exactly what the system prompt is for, leaving the user message to carry only what's specific to that turn's question. Reordering content within the user message doesn't change where the stable material lives; splitting it evenly doesn't address the underlying mismatch; and moving the turn-specific question into the system prompt puts the wrong content in the persistent slot. *(task 6.2; concept: system_prompt_vs_user_message; item `mock1-42` (source: d6#7))*

---

**43. A** — Summarizing or dropping the oldest middle turns while keeping the system prompt and the opening turn intact controls context growth without losing the instructions or the original problem statement. Truncating the system prompt removes the very instructions the team wants preserved; starting over with no context loses the opening problem statement entirely; and sending the full history unmodified is exactly the growth the team is trying to avoid. *(task 6.2; concept: long_conversation_context_management; item `mock1-43` (source: d6#8))*

---

**44. A, C** — Structured tool arguments are read directly instead of being fished out of prose, and that directly removes the false-positive risk of a rival keyword showing up in an explanatory sentence. Tool use enforces format, not correctness of reasoning, and it doesn't prevent the model from choosing the wrong tool in the first place. *(concept: tool_use_over_string_matching_benefits; item `mock1-44`)*

---

**45. A, C** — Indirect injection is defined by the attack arriving through retrieved or ingested content the model treats as data — a fetched web page or a parsed PDF both fit. A user typing directly into chat is direct injection, and over-broad tool permissions is a least-privilege problem, not an injection vector at all. *(concept: classifying_indirect_injection; item `mock1-45`)*

---

**46. B** — The instructions were planted inside retrieved page content and the model followed them as commands, which is the defining pattern of indirect injection; the attacker never spoke to the model directly (A), and neither `tool_choice` configuration nor request throttling describes what happened (C, D). *(task 7.1; concept: indirect_prompt_injection; item `mock1-46` (source: d7#2))*

---

**47. D** — A destructive action against a production resource is the case guardrails exist for: routing it through required human approval would have caught the target mismatch before deletion. Rate limiting only throttles frequency, an audit log only helps after the fact, and content filtering addresses generated text, not tool actions. *(task 7.2; concept: human_review_high_risk_action; item `mock1-47` (source: d7#5))*

---

**48. D** — Validating a proposed tool call and rejecting it before it ever runs is the definition of a pre-tool-use hook; this is what stops the destructive command from executing at all. A post-tool-use hook would only see the output after the shell already ran, and neither prompt caching nor subagent routing describes inspecting a command for danger. *(task 7.3; concept: pre_tool_use_hook; item `mock1-48` (source: d7#7))*

---

**49. A, C** — `name` and `input_schema` are two of the three required top-level keys on a tool object (`description` is the third, not listed here as a distractor). `tool_choice` and `max_tokens` are both real API parameters, but neither lives inside a tool's own definition — they're request-level settings. *(concept: tool_definition_required_keys; item `mock1-49`)*

---

**50. C** — `{"type": "tool", "name": "charge_card"}` is the only form that pins the call to one specific tool. `auto` still permits a text-only reply, `any` forces a call but leaves the choice among all three tools open, and an unset `tool_choice` gives no such guarantee — there's no "first tool in the array" default. *(task 8.2; concept: tool_choice_pinned_tool; item `mock1-50` (source: d8#2))*

---

**51. B** — A custom slash command is exactly the mechanism for an on-demand, invoked-by-name action like `/deploy-staging`. A CLAUDE.md rule would instead apply automatically on every turn regardless of relevance, a subagent launches for isolated sub-tasks rather than being typed by name mid-conversation, and a global system prompt override reaches far beyond one team's one project. *(task 8.2; concept: custom_slash_command; item `mock1-51` (source: d8#5))*

---

**52. C** — A project-specific subagent runs in its own context window and can be restricted to a specific tool set, which keeps the main conversation's context clean while limiting what the review is allowed to touch. A CLAUDE.md reminder doesn't isolate context or restrict tools, a slash command that prints a static checklist performs no actual review, and raising `max_tokens` addresses response length, not context isolation. *(task 8.2; concept: project_subagent_isolation; item `mock1-52` (source: d8#6))*

---

**53. D** — MCP treats a passive, read-only data stream like the `config.yaml` contents as a Resource, comparable to an HTTP GET, while an action that mutates server state like `restart_service` is a Tool, comparable to an HTTP POST. Classifying both as Tools or both as Resources erases that distinction, and reversing which one is which mislabels the mutation as passive. *(task 8.3; concept: mcp_resources_vs_tools; item `mock1-53` (source: d8#9))*
