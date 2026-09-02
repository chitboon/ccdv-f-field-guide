# CCDV-F Mock Exam 2 — Key and Rationales (fresh content)

Grade in one pass after finishing all 53 items. For every miss, note
whether it was: didn't know it, misread the item, or picked the
plausible-but-soft option. Multi-response items require both correct
letters to count as a hit.

---

**1. B** — Reading each tool's actual output and choosing the next action from it, instead of running the same three calls in the same fixed order regardless of outcome, is exactly what makes a system agentic. Calling more tools, a different temperature, or the Batches API are all unrelated implementation details. *(task 1.1; concept: loop_decides_from_output; item `freshd1-09`)*

---

**2. A** — `max_tokens` is the value that specifically means the response was truncated by the length limit rather than completing naturally, which is exactly the signal that should route to special handling. `end_turn` and `tool_use` both describe non-truncated completions, and Claude doesn't omit `stop_reason` when output is cut short. *(task 1.1; concept: max_tokens_truncation_alert; item `freshd1-10`)*

---

**3. B** — Keeping the system prompt and the most recent turns intact while summarizing or dropping the oldest file-read outputs reclaims context space without losing the original task brief. Truncating the system prompt, restarting with no history, or shortening the brief itself all remove exactly what the team wants to keep. *(task 1.2; concept: context_trim_preserve_brief; item `freshd1-11`)*

---

**4. A** — Letting the model see the `is_error` content and choose a recovery step — retry, switch printers, notify a human — is what actually uses the structured failure signal productively. Discarding the flag, ending the session outright, or blindly resending the same call every few seconds all fail to reason over the failure. *(task 1.2; concept: tool_result_is_error_recovery; item `freshd1-12`)*

---

**5. C** — Documenting the expected `id` format and returning a structured reason for an empty result is what lets a caller actually diagnose a failed lookup, which a bare `null` never explains. Renaming the tool, raising `max_tokens`, or removing the parameter entirely don't address the missing diagnostic detail. *(task 1.2; concept: tool_interface_needs_description; item `freshd1-13`)*

---

**6. B** — Returning distinct, structured error content per failure type lets the agent tell an expired fare apart from a declined card or a timed-out API, and choose the right next step. A fixed apology message, blind silent retries, and removing the tool after one error all withhold or discard the very detail the agent needs. *(task 1.2; concept: structured_error_per_failure_type; item `freshd1-14`)*

---

**7. A** — A coordinator call that splits the briefing into five subtasks, delegates one worker call per data source, and combines the results is the orchestrator-workers pattern applied to independent parallel sources. Prompt chaining is a fixed sequence, a single linear agent wouldn't delegate to separate calls, and routing sends a request to exactly one destination, not five in parallel. *(task 1.3; concept: orchestrator_workers_research; item `freshd1-15`)*

---

**8. C** — A generator drafting the clause and a separate critic checking it against enforceability rules, looping until it passes, is the evaluator-optimizer pattern. Routing dispatches by classification rather than looping feedback, orchestrator-workers splits into independent parallel subtasks, and parallelization generates multiple drafts at once rather than iterating one draft against critique. *(task 1.3; concept: evaluator_optimizer_patent_claim; item `freshd1-16`)*

---

**9. D** — A signed-off scope document naming the specific capability meant — legal-liability review versus typo detection — is what would have caught the mismatch three weeks earlier, before the feature shipped in the wrong shape. A bigger team, more `max_tokens`, or a retrospective held only after shipping don't address the missing agreement on scope. *(task 2.1; concept: ambiguous_requirement_wrong_scope; item `freshd2-17`)*

---

**10. C** — Tracing the requirement to a concrete automated test that fails whenever a discontinued product is mentioned is what would have caught the bug before it ever reached a customer. A more prominent wiki font, one engineer manually re-reading every response, or a verbal mention in standup all create no actual enforcement. *(task 2.1; concept: requirements_traceable_to_tests; item `freshd2-18`)*

---

**11. B** — An iterative approach that ships a narrow version early and refines based on real usage data fits a feature whose behavior can't be fully predicted until users actually interact with it. A fully upfront spec assumes the same certainty traditional deterministic software has, no process at all overreacts to the uncertainty, and a fixed six-month timeline doesn't scale with the feature's actual needs. *(task 2.2; concept: iterative_vs_upfront_design_llm; item `freshd2-19`)*

---

**12. A** — Native PDF processing caps out at 100 pages and 32MB, and this file's 45MB size — not a broken feature — is the actual cause of the rejection. PDFs don't require conversion to images first, the rejection isn't about credit exhaustion, and the limit isn't specific to any one document category. *(task 2.3; concept: native_pdf_page_and_size_limit; item `freshd2-20`)*

---

**13. C** — `AnthropicVertex` authenticates through Google Cloud's application default credentials, matching a mandate to route through an existing GCP project. `AnthropicBedrock` is built for AWS instead, a bare API key doesn't satisfy GCP-specific infrastructure requirements, and no first-party SDK requires a hand-rolled HTTP client here. *(task 2.3; concept: cloud_sdk_bedrock_vertex; item `freshd2-21`)*

---

**14. D** — `stream.get_final_text()` already returns the complete response as a single string once the stream finishes, replacing manual chunk concatenation entirely. Continuing to concatenate by hand, reading `.usage` off `get_final_message()`, or re-requesting the prompt without streaming are all unnecessary or don't actually solve the problem. *(task 2.3; concept: streaming_helper_choice; item `freshd2-22`)*

---

**15. C** — Gating the new tool behind a flag for a small percentage of sessions first, widening only once proven stable, limits how many users an undiscovered bug can reach. Requiring manual opt-in, shipping to everyone immediately, or testing only locally before a full release all skip the staged rollout that actually contains the risk. *(task 2.4; concept: canary_rollout_new_tool_integration; item `freshd2-23`)*

---

**16. D** — Continuing to accept the old shape while ignoring the missing field keeps older, not-yet-updated partners working, until every partner has actually migrated to send it. Removing the field's optional status immediately breaks those old partners, and replacing the whole tool or renaming it are far more disruptive than the situation requires. *(task 2.4; concept: tool_schema_versioning_compat; item `freshd2-24`)*

---

**17. D** — Tagging every tool call from a session with that session's shared correlation ID, set at the very start, is exactly what lets an incident review reconstruct which calls belonged together. Fewer tools, longer retention, or logging only the last call don't create the missing link between related events. *(task 2.4; concept: correlation_id_tracing_multitool; item `freshd2-25`)*

---

**18. C** — Replacing the live API call in the PR pipeline with a mocked client removes exactly the network/rate-limit/outage noise causing intermittent failures unrelated to the code being tested, while a separate suite still checks the real API. Padding the timeout for hours, blindly retrying failures, or dropping the check entirely don't address the actual flakiness source. *(task 2.4; concept: mocked_api_for_ci_isolation; item `freshd2-26`)*

---

**19. A** — Splitting into role-scoped agents (or a router plus specialists) gives triage, release notes, and billing questions each a prompt narrowed to its own responsibility, instead of one prompt straining to cover all three. Running three unmodified copies of the same prompt, lowering `temperature`, or piling on more instructions to the same combined prompt don't narrow anything. *(task 2.5; concept: single_agent_vs_many_specialists; item `freshd2-27`)*

---

**20. C** — A per-session cap on tool-call count or rate enforced at the application layer contains a runaway loop regardless of what the model itself chooses to do. A polite system-prompt request, raising the account's rate limit, or switching to a slower model don't provide any hard structural limit on the behavior. *(task 2.5; concept: app_layer_rate_limiting_runaway_loop; item `freshd2-28`)*

---

**21. D** — Detecting the field-format failure and showing a clear message with a retry option replaces a silent spinning loader with something the applicant can actually act on. Letting the loader keep spinning, silently looping the same request forever, or disabling structured output for every applicant entirely all leave the underlying failure unaddressed or overcorrect. *(task 2.5; concept: fallback_ux_validation_failure; item `freshd2-29`)*

---

**22. D** — Versioning the ticket schema lets old plain-text rows stay valid while new rows represent richer, typed attachments, without disturbing years of existing history. Encoding attachment data into the text column, deleting all history, or storing everything as an unstructured blob all sidestep the actual versioning problem. *(task 2.5; concept: versioned_conversation_schema_storage; item `freshd2-30`)*

---

**23. C** — Deduplicating on the event's unique ID before starting a new agent run turns a repeated delivery into a no-op, which is the correct response to ordinary at-least-once webhook delivery. Disabling the integration outright, pushing the fix onto the provider, or increasing `max_tokens` don't address the duplicate-trigger problem itself. *(task 2.5; concept: idempotent_webhook_triggered_agent; item `freshd2-31`)*

---

**24. C** — Validating every required configuration value at startup and refusing to start when one is missing surfaces the real root cause immediately, instead of an error far removed from the missing config deep inside a later request. Catching the eventual error, logging a warning and continuing, or hardcoding a fallback value all let the actual problem hide until it resurfaces elsewhere. *(task 2.6; concept: fail_fast_startup_config_validation; item `freshd2-32`)*

---

**25. A, C** — `RateLimitError` and `InternalServerError` both describe transient conditions unrelated to whether the request itself was valid, so retrying with backoff can succeed. `PermissionDeniedError` and `NotFoundError` both describe a fixed problem with the request or its target that an identical retry cannot fix. *(task 2.3; concept: retryable_vs_nonretryable_exceptions; item `mock2-12`)*

---

**26. A, B** — Per-environment keys injected via a secret store, plus immediate rotation the moment a key is found exposed anywhere, are both genuine security practices. Sharing one production key everywhere widens the blast radius of any single leak, and baking a key into a compiled binary just moves the exposure surface rather than removing it. *(task 2.6; concept: secrets_handling_practices; item `mock2-26`)*

---

**27. C** — Read-only subcommands like `git status`/`git diff` can be allow-listed directly in `.claude/settings.json`'s permission rules, letting `git push` still require approval without any custom hook script. A `PreToolUse` hook works but isn't needed when settings-based allowlisting already covers it, a `CLAUDE.md` request is only a polite suggestion the model can ignore, and a slash command wrapper adds friction the requirement doesn't ask for. *(task 3.1; concept: settings_based_permission_allowlisting; item `freshd3d4-03`)*

---

**28. A, B** — Enterprise policy sits above both project and user settings in precedence, and CLAUDE.md files at different directory levels layer together instead of one replacing the other. Claude Code doesn't use file modification time to resolve conflicts, and subdirectory CLAUDE.md files load automatically, not only when explicitly referenced. *(task 3.1; concept: settings_and_memory_hierarchy; item `mock2-27`)*

---

**29. D** — Running the eval at `temperature: 0`, or averaging multiple runs, removes the sampling noise that's producing 83%-97% swings with no actual code or prompt change behind them. Lowering the threshold papers over the noise instead of fixing it, a larger model doesn't eliminate run-to-run variance at temperature 1.0, and more `max_tokens` doesn't address variance at all. *(task 4.1; concept: sampling_variance_vs_real_regression; item `freshd3d4-04`)*

---

**30. B** — Claude 3 Opus needs at least 1,024 tokens in a segment before it becomes cacheable, and 950 tokens falls just short of that threshold regardless of how the block is otherwise configured. Opus does support ephemeral caching (A), placement relative to the user turn isn't the issue described (C), and a TTL lapse would only explain occasional misses, not a cache that never hits at all (D). *(task 5.1; concept: cache_min_token_threshold; item `freshd5-08`)*

---

**31. D** — Claude tokenizes in subwords, so a 320-word clause routinely produces more than 320 tokens as words and punctuation get split into multiple chunks; there is never a 1:1 word-to-token mapping. Truncation would lower the reported count rather than raise it (A), a double-counted system prompt isn't described in the scenario (C), and caching doesn't inflate a token count at all (B). *(task 5.1; concept: subword_tokenization_ratio; item `freshd5-09`)*

---

**32. A, B** — This request fails both of extended thinking's independent numeric constraints at once: the 500-token budget doesn't clear the 1,024-token floor, and the 400-token `max_tokens` doesn't exceed it. `thinking` is correctly a top-level request parameter, not something nested in `messages`, and extended thinking works across Claude model snapshots, not just specific ones. *(task 5.1; concept: extended_thinking_dual_constraint; item `mock2-31`)*

---

**33. A** — System prompt, conversation history, the new user turn, and the completion all draw from one shared, finite context-window budget, so with only 40,000 tokens of headroom left, a 25,000-token turn plus a requested 20,000-token completion cannot both fit — the completion gets truncated or the call is rejected. Completions are not generated in a separate token space (B), the system prompt isn't auto-evicted to make room (C), and caching doesn't shrink what counts against the context window (D). *(task 5.2; concept: context_window_shared_token_budget; item `freshd5-10`)*

---

**34. C** — Claude processes text as subword tokens rather than individual characters, so a token can bundle several letters together in a way the model never directly inspects one at a time, which is why letter-order tasks like spelling a word backwards can go wrong. The context window is large enough to hold a single word (A), temperature doesn't reorder letters in the input (B), and extended thinking isn't a strict requirement for this class of task (D). *(task 5.2; concept: tokenization_limits_character_tasks; item `freshd5-11`)*

---

**35. B** — `max_tokens` only sets a ceiling on how many tokens the completion may contain; it has no bearing on the reasoning quality or accuracy of the tokens actually generated, which is why doubling it left the drafted emails unchanged in quality. Lowering it wouldn't have improved quality either (A), it governs output length rather than the context window available for input (C), and it isn't required to move in lockstep with `temperature` (D). *(task 5.2; concept: max_tokens_caps_length_not_quality; item `freshd5-12`)*

---

**36. A** — Sonnet is positioned as the balanced middle tier, offering faster responses and lower cost than Opus while handling moderate multi-transcript synthesis better than the fastest tier alone — the fit this live dashboard workload needs. Opus is more capability than a moderate-synthesis task requires (B), Haiku isn't automatically correct whenever latency matters if the task needs more synthesis than it comfortably provides (C), and model tier does affect both latency and reasoning quality, not just cost (D). *(task 5.3; concept: sonnet_balanced_tier; item `freshd5-13`)*

---

**37. D** — Enabling extended thinking means spending extra tokens and added latency on visible step-by-step reasoning in exchange for better accuracy on multi-step formula debugging — a deliberate cost/latency-for-quality tradeoff, not a tier switch. Extended thinking works with Opus and isn't restricted to the fastest tier (A), thinking tokens are billed as regular output rather than at a discount (B), and thinking does not guarantee a correct final answer (C). *(task 5.3; concept: extended_thinking_tradeoff_decision; item `freshd5-14`)*

---

**38. A, B** — The Batch API exists specifically for asynchronous, non-urgent volume, and results genuinely aren't retrievable — not even partially — until the batch reaches `ended`. There's no fixed 4,096-token `max_tokens` floor, and batch processing is explicitly not a real-time streaming mechanism. *(task 5.4; concept: batch_api_accuracy; item `mock2-38`)*

---

**39. A** — Naming each block (`<recipe_data>`, `<safety_rules>`) gives the model a structural cue distinguishing reference content from a behavioral rule, which is what's missing when a plain ingredient line gets echoed back as if binding. Capping length, moving the excerpt to the customer's message, or a stop sequence tied to one heading don't address the underlying lack of a boundary. *(task 6.1; concept: xml_section_delimiting; item `freshd6-06`)*

---

**40. C** — Showing a couple of worked commit-list-to-bullet examples demonstrates the exact pattern (tense, ticket-number omission, one bullet per change) rather than just describing it in prose, which is what prose alone has already failed to lock in. Repeating the same instruction, relocating it unchanged, or raising `max_tokens` don't add a demonstration of the pattern. *(task 6.1; concept: few_shot_pattern_demonstration; item `freshd6-07`)*

---

**41. D** — Reasoning through each input inside `<thinking>` tags before committing to a verdict gives the model room to weigh near-identical claims the same way, addressing the inconsistency directly. Capping `max_tokens` at 1, asking for a bare word, or pre-combining the inputs into one external score all remove reasoning room rather than add it. *(task 6.1; concept: chain_of_thought_reasoning; item `freshd6-08`)*

---

**42. B** — The docstring spec and naming rules are stable across every call, which is what `system` is for; the function source is what's actually turn-specific and belongs in the user message. Leaving `system` empty, moving the source into the same config file, or rotating which call carries the rules all leave the stable/volatile content in the wrong place. *(task 6.2; concept: system_prompt_vs_user_message; item `freshd6-09`)*

---

**43. A** — Wrapping each transcript in `<document>` tags and placing the follow-up question after the closing tags gives the model an explicit boundary, which is exactly what's missing when a transcript line that reads like a request gets treated as the actual instruction. Trimming transcripts, moving the question into `system`, or capitalizing it don't establish where the recorded dialogue ends. *(task 6.2; concept: reference_material_boundary_tags; item `freshd6-10`)*

---

**44. A, C** — Reading a structured, schema-validated field directly avoids the coincidental-substring problem that keyword matching over free text creates. Tool use enforces output shape, not the correctness of the underlying judgment, and it says nothing about preventing duplicate calls across turns. *(task 6.3; concept: tool_use_over_string_matching_benefits; item `mock2-44`)*

---

**45. A** — Rendering model-generated content as raw, unescaped HTML is what let the injected `<script>` tag execute for every visitor — that is insecure output handling, independent of what the model was told to do. The model did complete its summarization task rather than abandon it (B), and the scenario turns on missing sanitization, not on posting permissions or request throttling (C, D). *(task 7.1; concept: insecure_output_handling; item `freshd7-04`)*

---

**46. A, C** — Both A and C describe adversarial instructions arriving through ingested content (a scraped review, a summarized email) that the model reads as data — the defining pattern of indirect injection. B is direct injection since the user is the one typing the attack, and D is a secrets-handling failure, not an injection attack at all. *(task 7.1; concept: classifying_indirect_injection; item `mock2-45`)*

---

**47. D** — Real-time monitoring for unusual ordering activity, paired with an automatic halt, is what would have stopped the runaway reorder loop within minutes instead of two days. A quarterly audit trail only surfaces the problem long after the fact, and neither profanity filtering nor extra few-shot examples touches the missing spend controls. *(task 7.2; concept: anomaly_monitoring_circuit_breaker; item `freshd7-05`)*

---

**48. B** — Baking one long-lived key into every tenant's container means a single compromised container hands an attacker access to every other tenant's data through the same integration; scoped, tenant-specific, rotatable credentials are what key management calls for instead. The failure here is the shared credential itself, not a missing hook, a request-volume issue, or injected instructions in a config file (A, C, D). *(task 7.3; concept: shared_credential_across_tenants; item `freshd7-06`)*

---

**49. C** — Setting `content` to an array of content blocks lets one `tool_result` carry a text block and an image block together under the same `tool_use_id`. A separate `tool_use` block would be Claude's action, not the application's reply; flattening everything into one JSON string discards the structure Claude reads content blocks with; and splitting the result across two `tool_result` blocks would need two distinct `tool_use_id` values that don't exist for a single call. *(task 8.1; concept: tool_result_content_array; item `freshd8-05`)*

---

**50. A, D** — `input_schema` is the third required top-level key alongside `name` and `description`, and adding one with `type` and `properties` is exactly what fixes a definition missing it. `tool_choice` is a request-level parameter, never a key inside the tool object itself, so it isn't what the lint step is flagging — and the lint step is correctly catching a real gap, not a false positive. *(task 8.1; concept: tool_definition_required_keys; item `mock2-49`)*

---

**51. B** — A custom slash command is exactly the mechanism for an on-demand, invoked-by-name action like `/run-smoke-tests`. A CLAUDE.md rule would instead fire automatically after every code change regardless of relevance, a subagent launches for isolated sub-tasks rather than being typed by name mid-conversation, and a global system prompt override reaches every project the QA team opens, not just this one. *(task 8.2; concept: custom_slash_command_ondemand; item `freshd8-06`)*

---

**52. D** — CLAUDE.md is loaded automatically at the start of each session, which is exactly what makes standing rules like a license-header requirement and a `vendor/` edit ban apply every session without anyone invoking them by name. A slash command still requires typing it before each edit, a subagent scoped to release branches wouldn't cover everyday file creation, and a tool's `input_schema` only shapes that one tool's arguments. *(task 8.2; concept: claude_md_standing_rules_license; item `freshd8-07`)*

---

**53. A** — SSE is MCP's transport for remote, networked servers, streaming server-initiated messages back to clients over an HTTP connection, which fits a server deployed on a shared remote host and reached by several clients. stdio is the transport for a local child process communicating over standard streams, not a network deployment; and WebSocket and gRPC are not among MCP's two defined transports at all. *(task 8.3; concept: mcp_transport_sse; item `freshd8-08`)*
