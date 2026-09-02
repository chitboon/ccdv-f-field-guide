# CCDV-F Mock Exam 1 — Key and Rationales (fresh content)

Grade in one pass after finishing all 53 items. For every miss, note
whether it was: didn't know it, misread the item, or picked the
plausible-but-soft option. Multi-response items require both correct
letters to count as a hit — partial credit isn't how the real exam scores
"select N" items either.

---

**1. D** — Deciding the next action from what a tool returned, rather than executing a preset order, is exactly what separates an agent loop from a fixed pipeline. A tool call alone, synchronicity, and temperature are all implementation details unrelated to that control-flow distinction. *(task 1.1; concept: loop_decides_from_output; item `freshd1-01`)*

---

**2. B** — `max_tokens` specifically means generation was cut off by the length limit before finishing naturally — exactly the case worth alerting on before truncated text reaches a user. `end_turn` is a normal successful completion, `tool_use` means the model paused to call a tool (not an error), and `stop_sequence` fires on a deliberate custom string, not a length cutoff. *(task 1.1; concept: max_tokens_truncation_alert; item `freshd1-02`)*

---

**3. D** — Keeping the system prompt and recent turns intact while summarizing or dropping the oldest tool dumps reclaims context space without losing the instructions the loop still needs to follow. Dropping the system prompt, restarting with no history, or replacing everything with a placeholder all destroy the working memory or instructions the loop actually needs. *(task 1.2; concept: context_trim_preserve_brief; item `freshd1-03`)*

---

**4. C** — `is_error: true` is a signal meant for the model to reason about, so the loop should let it choose a recovery step — retry, try an alternate warehouse, or escalate. Ignoring the flag, killing the session outright, or blindly resending the same call all fail to use the error content productively. *(task 1.2; concept: tool_result_is_error_recovery; item `freshd1-04`)*

---

**5. C** — A clear parameter description plus a structured, inspectable response is what lets Claude reason about correct usage and diagnose failures — neither exists in the current tool. Tool name length, a bigger `max_tokens`, and removing the parameter don't address the missing description or the silent failure at all. *(task 1.2; concept: tool_interface_needs_description; item `freshd1-05`)*

---

**6. D** — Returning distinct, structured content per failure type is what lets the model tell a decline apart from an invalid amount or a timeout, and choose the right recovery action. A single unlabeled boolean, server-only logging, and a hidden retry count all withhold exactly the detail the model needs to decide. *(task 1.2; concept: structured_error_per_failure_type; item `freshd1-06`)*

---

**7. B** — A coordinator call that identifies the subtasks, delegates each to a worker call, and synthesizes the results is the orchestrator-workers pattern. A fixed pipeline runs the same predetermined steps regardless of content, evaluator-optimizer needs a critic scoring a draft, and a single agent wouldn't delegate each unit to separate calls at all. *(task 1.3; concept: orchestrator_workers_quarterly_report; item `freshd1-07`)*

---

**8. D** — A drafting call and a separate checking call trading feedback until the draft clears every flagged issue is the evaluator-optimizer pattern by definition. Orchestrator-workers splits into independent parallel subtasks, routing dispatches by classification, and producing several drafts at once and picking the best is parallelization, not iterative feedback. *(task 1.3; concept: evaluator_optimizer_apology_email; item `freshd1-08`)*

---

**9. A** — A signed-off scope document naming the specific capability meant catches an ambiguous request like "handle vendor onboarding" before three weeks get spent building the wrong feature. A bigger team, more `max_tokens`, or a post-hoc retrospective don't address the missing agreement on scope itself. *(task 2.1; concept: ambiguous_requirement_wrong_scope; item `freshd2-01`)*

---

**10. B** — Tracing a requirement to a concrete, automated test is what actually catches a violation like PII leaking into output; restating it, assigning one person to remember it, or writing it in bold don't create any enforcement mechanism at all. *(task 2.1; concept: requirements_traceable_to_tests; item `freshd2-02`)*

---

**11. B** — Locking in a detailed upfront spec before any real usage data exists risks building precisely to assumptions that user behavior will invalidate — exactly the risk an LLM feature's unpredictable real-world behavior creates. Upfront specification isn't inherently wrong for tool-calling features specifically, and neither "no risk" nor "too short a timeline" addresses the actual uncertainty problem. *(task 2.2; concept: iterative_vs_upfront_design_llm; item `freshd2-03`)*

---

**12. D** — Native PDF support caps out at 100 pages and 32MB; a 140-page file exceeding that specific ceiling is the actual cause, not a broken feature needing a custom workaround. PDFs don't need pre-conversion to text, and the failure isn't about a request quota. *(task 2.3; concept: native_pdf_page_and_size_limit; item `freshd2-04`)*

---

**13. C** — `AnthropicBedrock` authenticates through AWS SigV4 signing, matching a bank's requirement to route traffic through existing AWS infrastructure. The standard client uses a bare API key (not AWS-native signing), `AnthropicVertex` is built for GCP instead, and no first-party SDK requires a hand-rolled HTTP client for this. *(task 2.3; concept: cloud_sdk_bedrock_vertex; item `freshd2-05`)*

---

**14. A** — `stream.text_stream` is exactly the iterable meant for rendering each incremental delta as it arrives, unlike `get_final_message()` which blocks until the whole response completes. Looping `get_final_text()` doesn't simulate real incremental rendering, and polling with fresh non-streaming requests abandons streaming rather than using it. *(task 2.3; concept: streaming_helper_choice; item `freshd2-06`)*

---

**15. B** — Gating a new tool behind a flag for a small percentage of sessions first, expanding only once proven stable, is what limits the blast radius of an undiscovered bug. Shipping to everyone at once, testing only locally before a full release, or requiring manual opt-in through settings all skip the staged-rollout safety net. *(task 2.4; concept: canary_rollout_new_tool_integration; item `freshd2-07`)*

---

**16. D** — Making the new field optional with a default lets old callers keep working unmodified while new callers adopt it, only becoming required once every caller has actually migrated. Marking it required immediately breaks every caller still on the old shape, and deleting the schema or renaming the tool are far more disruptive than the situation calls for. *(task 2.4; concept: tool_schema_versioning_compat; item `freshd2-08`)*

---

**17. B** — A shared correlation ID set at the start of a session and attached to every one of that session's tool calls is exactly what lets a confusing multi-call session be reconstructed afterward. Longer retention, fewer tools, or logging only the last call don't create the missing link between related events at all. *(task 2.4; concept: correlation_id_tracing_multitool; item `freshd2-09`)*

---

**18. B** — Mocking the API call in CI removes exactly the network/rate-limit/outage noise causing intermittent failures unrelated to the code under test, while a separate non-blocking suite still exercises the real API. Skipping CI testing entirely, blindly retrying failures, or padding the timeout for hours don't address the actual flakiness source. *(task 2.4; concept: mocked_api_for_ci_isolation; item `freshd2-10`)*

---

**19. C** — Splitting one overloaded prompt into role-scoped agents (or a router plus specialists) gives each domain a narrower, better-suited prompt instead of one prompt straining to cover three unrelated domains at once. Lowering `temperature`, lengthening the same combined prompt further, or running three unmodified copies of it don't narrow the scope confusion at all. *(task 2.5; concept: single_agent_vs_many_specialists; item `freshd2-11`)*

---

**20. D** — A per-session cap on tool-call count or rate enforced at the application layer contains a runaway loop regardless of what the model itself decides to do next. Raising the account's rate limit lets the loop run faster, not less, and a system-prompt request or a slower model don't provide a hard structural limit either. *(task 2.5; concept: app_layer_rate_limiting_runaway_loop; item `freshd2-12`)*

---

**21. A** — Detecting the downstream validation failure and showing a clear fallback message (optionally with retry) replaces a blank, unexplained screen with something a user can actually act on. Infinite silent retries, disabling the whole feature, or logging without changing the UI all leave the user facing an unexplained dead end. *(task 2.5; concept: fallback_ux_validation_failure; item `freshd2-13`)*

---

**22. B** — Versioning the stored message schema lets old plain-text rows stay valid while new rows represent richer, typed content like images, without touching years of existing history. Deleting all history, storing everything as an unstructured blob, or stuffing image data into a text column all sidestep the actual schema-evolution problem. *(task 2.5; concept: versioned_conversation_schema_storage; item `freshd2-14`)*

---

**23. C** — Deduplicating on the event's unique ID before starting a new agent run turns a repeated webhook delivery into a no-op, which is the correct response to ordinary at-least-once delivery semantics. Asking the provider to change their delivery guarantee, more `max_tokens`, and disabling the integration outright don't address the duplicate-trigger problem itself. *(task 2.5; concept: idempotent_webhook_triggered_agent; item `freshd2-15`)*

---

**24. A** — Validating every required configuration value at startup and refusing to start when one is missing surfaces the real root cause immediately, instead of a confusing authentication error deep inside a later user request. Catching the eventual error, hardcoding a fallback key, or just logging a warning and continuing all let the actual problem hide until it resurfaces far from its cause. *(task 2.6; concept: fail_fast_startup_config_validation; item `freshd2-16`)*

---

**25. A, C** — `RateLimitError` and `InternalServerError` are both transient conditions that can resolve on their own, so a backoff retry makes sense. `BadRequestError` and `AuthenticationError` describe a malformed request or bad credential — retrying the exact same request changes nothing, so failing fast is correct instead. *(task 2.3; concept: retryable_vs_nonretryable_exceptions; item `mock1-12`)*

---

**26. A, B** — Loading the key from an environment variable or secrets manager keeps it out of source entirely, and a placeholder-only `.env.example` documents the required variables without exposing a real key. A committed config file still puts the real secret in the repository regardless of a read-only flag, and printing it to logs exposes it to anyone with log access. *(task 2.6; concept: secrets_handling_practices; item `mock1-25`)*

---

**27. A** — `--output-format json` returns a structured payload with the final message text, token usage, and cost that a CI pipeline can parse directly, unlike `--verbose` (human-formatted) or scraping plain-text output through a regex. *(task 3.1; concept: structured_session_output; item `freshd3d4-01`)*

---

**28. A, B** — Enterprise-managed policy sits above both project and user settings in precedence, and CLAUDE.md files at different directory levels combine rather than one silently overriding the other. User settings do not automatically outrank project settings, and Claude Code doesn't resolve conflicts by file modification time. *(task 3.1; concept: settings_and_memory_hierarchy; item `mock1-27`)*

---

**29. D** — An eval set that's never revisited against current product policy can silently reward outdated behavior instead of catching a real, current mistake, especially once policy has changed twice since the set was written. A stable pass rate doesn't prove the model hasn't drifted, and reference answers do need periodic review, not just the prompt. *(task 4.1; concept: eval_dataset_staleness; item `freshd3d4-02`)*

---

**30. C** — The Messages API caps ephemeral cache breakpoints at four per request, and this design tags six segments (system prompt, lint rules, style guide, three diffs, coverage summary, current diff), exceeding that limit outright. Breakpoints aren't confined to a token range near the start (A), aren't restricted to system-level content only (B), and the five-minute TTL isn't the constraint being violated here (D). *(task 5.1; concept: cache_max_breakpoints; item `freshd5-01`)*

---

**31. D** — Extended thinking requires `budget_tokens` of at least 1,024, and 600 falls short of that floor, which is why validation fails even though `max_tokens` at 4,000 is comfortably above the budget. A completion isn't bound to be at least as long as the thinking budget (A), thinking works fine on arithmetic-heavy tasks (B), and `budget_tokens` is expressed in tokens, not dollars (C). *(task 5.1; concept: thinking_budget_min_and_max_tokens; item `freshd5-02`)*

---

**32. A, C** — Extended thinking has two independent numeric requirements: `budget_tokens` must clear a 1,024-token floor (900 doesn't), and `max_tokens` must exceed `budget_tokens` (850 doesn't exceed 900) — this request fails both at once. Temperature must be 1.0 or omitted, never forced to 0.0, and there's no separate `model` field requirement for thinking. *(task 5.1; concept: extended_thinking_dual_constraint; item `mock1-31`)*

---

**33. B** — `temperature: 0.0` makes token selection deterministic (greedy), minimizing the run-to-run variability that a billing-audit-sensitive coding tool needs. `temperature: 1.0` maximizes randomness rather than forcing convergence (A), a mid-range value still allows drift between runs (C), and temperature does directly govern output consistency regardless of `max_tokens` (D). *(task 5.2; concept: temperature_zero_deterministic; item `freshd5-03`)*

---

**34. A** — Hallucination is an inherent property of next-token probabilistic generation without a built-in fact-verification step, so no configuration switches it off, including a fabricated statute citation like this one. `temperature: 0` only reduces variability, not factual grounding (C); extended thinking makes reasoning visible but doesn't add source verification (D); and a larger model reduces but does not eliminate the underlying risk (B). *(task 5.2; concept: hallucination_inherent_property; item `freshd5-04`)*

---

**35. D** — As a conversation's history grows across dozens of turns, earlier system instructions can lose relative weight compared to the volume of more recent turns, consistent with the license-header rule slipping by turn 48. The API doesn't strip system prompts at a fixed turn count (A), extended thinking being disabled wouldn't specifically explain this instruction-following lapse (B), and nothing in the scenario ties the header text to a cached, TTL-expired segment (C). *(task 5.2; concept: context_degradation_long_conversation; item `freshd5-05`)*

---

**36. C** — Claude 3.5 Haiku is the fastest, cheapest tier, purpose-built for high-volume, low-complexity work like sorting 3 million forum posts a day into two fixed categories. Opus's larger reasoning capacity and context window aren't needed for a task this simple (A, D), and binary spam classification doesn't require extended thinking to be enabled at all (B). *(task 5.3; concept: haiku_high_volume_classification; item `freshd5-06`)*

---

**37. A** — For multi-step reasoning across a 200-page data room where a wrong inference risks missing a material liability and cost is secondary, choosing Opus trades higher cost and latency for its stronger reasoning capability — exactly the intended tradeoff. Haiku's speed advantage doesn't compensate for the reasoning depth this task needs (B), a larger `max_tokens` value doesn't substitute for reasoning quality (C), and `temperature` doesn't equalize capability differences between tiers (D). *(task 5.3; concept: opus_complex_reasoning_tradeoff; item `freshd5-07`)*

---

**38. A, B** — The Batch API's whole value proposition is the ~50% discount for asynchronous, non-urgent work, and results genuinely aren't available until the batch reaches `ended` — checking earlier returns a 404. It's a discount, not a premium, and `in_progress` is a real intermediate lifecycle state, not skipped. *(task 5.4; concept: batch_api_accuracy; item `mock1-38`)*

---

**39. B** — Naming each block (`<kb_article>`, `<moderation_rules>`) gives Claude a structural signal for which content is reference material to relay versus a rule to obey, stopping the walkthrough from being read back as a behavioral instruction. Shortening the text, moving it to the user turn unchanged, or a stop sequence tied to its first step don't address the missing boundary. *(task 6.1; concept: xml_section_delimiting; item `freshd6-01`)*

---

**40. C** — Concrete diff-to-message pairs show the exact target pattern (mood, length, punctuation) directly, which holds up better against drift than a prose restatement of the same rule. It isn't about prompt length or temperature — examples work because they demonstrate the pattern rather than describe it. *(task 6.1; concept: few_shot_pattern_demonstration; item `freshd6-02`)*

---

**41. D** — Reasoning through each factor's contribution before naming the verdict gives Claude room to weigh a borderline case consistently, which is exactly what's missing when a one-unit forecast shift flips the answer. It isn't about token count, temperature is unrelated to wording consistency, and writing text first doesn't change the context window's size. *(task 6.1; concept: chain_of_thought_reasoning; item `freshd6-03`)*

---

**42. D** — The style guide, checklist, and rubric are stable across every call, which is exactly what `system` is for; only the diff itself is turn-specific and belongs in `content`. Leaving `system` empty, splitting stable content across both fields, or putting the volatile diff in `system` all misplace what's stable versus what's per-turn. *(task 6.2; concept: system_prompt_vs_user_message; item `freshd6-04`)*

---

**43. B** — Wrapping each contract and the amendment in `<document>` tags and placing the question after them gives Claude an explicit boundary between source material and the actual request. Deleting a document doesn't fix the missing boundary, moving the question into `system` doesn't establish where the documents end, and bold markdown has no structural effect. *(task 6.2; concept: reference_material_boundary_tags; item `freshd6-05`)*

---

**44. A, C** — Structured tool arguments are read directly instead of being fished out of prose, and that directly removes the false-positive risk of a rival keyword showing up in an explanatory sentence. Tool use enforces format, not correctness of reasoning, and it doesn't prevent the model from choosing the wrong tool in the first place. *(task 6.3; concept: tool_use_over_string_matching_benefits; item `mock1-44`)*

---

**45. C** — A crafted request that talks the model into reciting its own system prompt discloses confidential fee-schedule and escalation content verbatim — that's system prompt leakage. The extraction text came from the live user turn, not a retrieved document (A); there is no service-account or request-volume detail in the scenario for the other two to attach to (B, D). *(task 7.1; concept: system_prompt_leakage; item `freshd7-01`)*

---

**46. A, C** — Indirect injection is defined by the attack arriving through retrieved or ingested content the model treats as data — a fetched web page or a parsed PDF both fit. A user typing directly into chat is direct injection, and over-broad tool permissions is a least-privilege problem, not an injection vector at all. *(task 7.1; concept: classifying_indirect_injection; item `mock1-45`)*

---

**47. D** — Promoting a changed prompt to a small monitored slice of traffic before full rollout is exactly what would have caught the time-zone bug before it hit every user; that is what staged, canary-style rollout buys you. Per-call human approval, a higher rate limit, and profanity filtering none address the missing monitoring window that let the bug reach 100% of traffic at once. *(task 7.2; concept: staged_rollout_before_full_deployment; item `freshd7-02`)*

---

**48. D** — Inspecting and modifying a tool's return value after `run_diagnostics` has already executed, before the model ever sees it, is the defining behavior of a post-tool-use hook. A pre-tool-use hook would act before execution (A), and neither subagent routing nor prompt caching describes scanning output for credential patterns (B, C). *(task 7.3; concept: post_tool_use_hook_secret_redaction; item `freshd7-03`)*

---

**49. B** — An `enum` array on the `format` property is what constrains the model to exactly the accepted lowercase values; without it, `"string"` alone permits any casing or spelling Claude happens to generate. `tool_choice` controls which tool fires, not the shape of one tool's arguments; moving `format` into `required` only makes the field mandatory, it doesn't restrict its values; and renaming the key to `Format` changes nothing about what values are accepted. *(task 8.1; concept: tool_schema_enum_constraint; item `freshd8-01`)*

---

**50. A, C** — `name` and `input_schema` are two of the three required top-level keys on a tool object (`description` is the third, not listed here as a distractor). `tool_choice` and `max_tokens` are both real API parameters, but neither lives inside a tool's own definition — they're request-level settings. *(task 8.1; concept: tool_definition_required_keys; item `mock1-49`)*

---

**51. C** — A project-specific subagent runs in its own context window, which keeps draft translations out of the main conversation, and can be restricted to a single tool, which covers all three stated needs at once. A CLAUDE.md instruction is a standing reminder, not an isolated workspace; a slash command that only prints a checklist does no translating; and a global system prompt override reaches far beyond one team's project. *(task 8.2; concept: subagent_isolated_review; item `freshd8-02`)*

---

**52. D** — A slash command supplies the on-demand, typed-by-name trigger, and dispatching it to a dedicated subagent supplies the isolated context and the single restricted tool, so the pairing is what satisfies both requirements together. A CLAUDE.md rule applies automatically rather than on demand; a subagent by itself isn't invoked by typing a command name; and a slash command by itself doesn't isolate context or restrict tools. *(task 8.2; concept: slash_command_subagent_combo; item `freshd8-03`)*

---

**53. D** — MCP classifies a passive, read-only capability like reading `contact_list` as a Resource, comparable to an HTTP GET, and an action that mutates server state like `create_deal` as a Tool, comparable to an HTTP POST. Calling both Tools or both Resources erases that distinction, and swapping which one is which mislabels the mutation as passive. *(task 8.3; concept: mcp_resources_vs_tools_crm; item `freshd8-04`)*
