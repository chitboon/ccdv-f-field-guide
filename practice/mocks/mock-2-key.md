# CCDV-F Mock Exam 2 — Key and Rationales

Grade in one pass after finishing all 53 items.

---

**1. A** — Effective context management keeps the system prompt and the most recent turns intact so the agent still follows its original instructions, while trimming or summarizing older tool_result payloads to reclaim space. Shortening the system prompt, dropping it, or replacing history with a placeholder all destroy the instructions or the working memory the loop needs. *(task 1.1; concept: context_window_trimming; item `mock2-01` (source: d1#3))*

---

**2. C** — `is_error: true` is a signal for the model to reason about, so the loop should let Claude choose a recovery step such as retrying, switching tools, or surfacing the failure to the user. Ignoring the flag, killing the session outright, or blindly resending the same request all fail to use the error content productively. *(task 1.1; concept: tool_result_is_error_recovery; item `mock2-02` (source: d1#4))*

---

**3. B** — Forcing `tool_choice` to name `extract_fields` guarantees that specific call instead of leaving the model free to reply with plain text. A longer description on other tools, a `stop_sequence`, and permanently removing tools are all indirect workarounds that don't reliably force the intended call. *(task 1.2; concept: tool_choice_forcing; item `mock2-03` (source: d1#8))*

---

**4. A** — Each turn's `tool_result` must be appended to the running conversation so the model can see everything it already tried; restarting history from a single result is why the loop keeps repeating earlier steps. Switching to the Batches API, duplicating tool calls, or resending the system prompt as a tool_result don't fix the missing accumulated history. *(task 1.2; concept: multiturn_loop_append_results; item `mock2-04` (source: d1#9))*

---

**5. C** — A single Claude turn can return multiple `tool_use` blocks, and the loop must execute each one and return a matching `tool_result` for every block before continuing. Rejecting the response, merging both calls into one result, or silently dropping the second block all mishandle a response that validly contains two requests. *(task 1.2; concept: parallel_tool_use_handling; item `mock2-05` (source: d1#10))*

---

**6. A** — A first call that emits only a category label, followed by dispatch to the subagent that owns that category, is the routing pattern. Evaluator-optimizer needs a critic looping on quality, orchestrator-workers decomposes a task into parallel pieces, and prompt chaining is a fixed sequence rather than a single classify-then-dispatch step. *(task 1.3; concept: routing_classification_pattern; item `mock2-06` (source: d1#14))*

---

**7. D** — Three Claude calls always run in the same fixed order with no step deciding to skip, repeat, or reorder is prompt chaining, precisely because nothing adapts based on what a prior step returned. Orchestrator-workers and evaluator-optimizer both involve a step making a decision about subsequent steps, and an autonomous agent loop is defined by exactly the adaptive behavior this pipeline lacks. *(task 1.3; concept: prompt_chaining_vs_agent; item `mock2-07` (source: d1#15))*

---

**8. B** — Three independent calls running at once on the same input, combined afterward by majority vote, is the parallelization (sectioning/voting) pattern. Routing sends input to exactly one subagent rather than three, orchestrator-workers would split the post into separate pieces instead of voting on the same one, and evaluator-optimizer requires a looped critique rather than a single simultaneous vote. *(task 1.3; concept: parallelization_sectioning_pattern; item `mock2-08` (source: d1#16))*

---

**9. A** — Without a prioritized, explicit criterion for which outcome wins when resolution speed and satisfaction trade off, two reasonable engineers built toward two different targets. More training data, single ownership, and a larger `max_tokens` don't resolve a disagreement about which outcome matters more. *(task 2.1; concept: prioritized_success_criteria; item `mock2-09` (source: d2#21))*

---

**10. C** — Explicitly scoping which data sources and access levels a vague requirement actually covers is what would have surfaced the read-only-wiki vs. read-write-database gap before implementation, not after. Code comments, a smarter model, or deferring security review don't address the requirement's own ambiguity. *(task 2.1; concept: scoping_data_access; item `mock2-10` (source: d2#22))*

---

**11. D** — Life-cycle rigor scaling with the cost of being wrong and the audience size is why a three-person, afternoon-rebuildable tool doesn't need the same process as a customer-facing system. Uniform rigor regardless of risk, skipping requirements unconditionally, and tying rigor to the exam's domain weighting are each the wrong variable to scale against. *(task 2.2; concept: lifecycle_rigor_scales_with_risk; item `mock2-11` (source: d2#23))*

---

**12. A, C** — `RateLimitError` and `InternalServerError` both describe transient conditions unrelated to whether the request itself was valid, so retrying with backoff can succeed. `PermissionDeniedError` and `NotFoundError` both describe a fixed problem with the request or its target that an identical retry cannot fix. *(concept: retryable_vs_nonretryable_exceptions; item `mock2-12`)*

---

**13. B** — Native PDF support lets Claude read a document block directly, including its visual layout, up to 100 pages — no manual text conversion needed. The Messages API isn't plain-text-only, PDFs don't need to be pre-split into page images, and there's no 5-page limit. *(task 2.3; concept: native_pdf_support; item `mock2-13` (source: d2#25))*

---

**14. C** — `max_tokens` is a required parameter on every Messages API request regardless of whether extended thinking is enabled; omitting it fails the request rather than being inferred from the thinking budget. The API doesn't auto-derive a cap, doesn't allow unlimited output, and doesn't silently disable thinking mode instead of erroring. *(task 2.3; concept: max_tokens_required_with_thinking; item `mock2-14` (source: d2#26))*

---

**15. D** — The Message Batches API is built specifically for large, non-urgent workloads like this one and discounts them accordingly. Shrinking `max_tokens` or adding more parallel synchronous requests reduces neither the fixed cost structure nor addresses urgency; switching to streaming doesn't change per-token pricing. *(task 2.3; concept: batch_api_for_bulk_workloads; item `mock2-15` (source: d2#27))*

---

**16. B** — Mocks that never touch the real API can't detect a genuine change in the API's response shape; the suite needs some coverage that exercises the real contract, whether live or via a fixture kept in sync with it. Mocking more of the system makes the blind spot worse, not better; removing integration tests or randomizing mock responses don't address the actual gap. *(task 2.4; concept: mocks_dont_catch_contract_drift; item `mock2-16` (source: d2#28))*

---

**17. A** — Redacting or excluding sensitive fields before they reach a shared log is the step that was skipped; without it, anyone with log access can see customer names, account numbers, and full conversations. Retention period, compression, and where the log server sits don't address who can read the sensitive content itself. *(task 2.4; concept: redact_before_shared_logging; item `mock2-17` (source: d2#29))*

---

**18. C** — The tool has no defensive handling for a caller omitting an optional field, so one bad call's unhandled exception takes down the entire session instead of failing just that call. Making every field mandatory just relocates the failure to a different input shape; a larger `max_tokens` and a different implementation language don't touch the missing error handling. *(task 2.4; concept: defensive_handling_optional_input; item `mock2-18` (source: d2#30))*

---

**19. D** — Two independent, subtly different implementations of the same rounding logic is exactly what Don't Repeat Yourself exists to prevent; one shared implementation would have kept results consistent everywhere it's called. Renaming the functions, moving the logic to the model, or adding more per-copy tests all leave the duplication itself in place. *(task 2.4; concept: dry_shared_codebase; item `mock2-19` (source: d2#31))*

---

**20. A** — Running the tool with the calling user's own credentials means the database's existing row-level access rules apply exactly as they would for any other client — no new access-control logic needed. A shared service account, no credentials at all, or an administrator credential each bypass or weaken the database's own controls instead of preserving them. *(task 2.5; concept: preserve_row_level_access; item `mock2-20` (source: d2#32))*

---

**21. B** — Running arbitrary user-submitted code inside an isolated, resource-limited sandbox is the essential safeguard before this tool reaches production; nothing else in the option list actually contains what the code can do. A system-prompt instruction, more `max_tokens`, or a linter pass are all trust-based or cosmetic and don't stop malicious code from executing on the host. *(task 2.5; concept: sandboxed_code_execution; item `mock2-21` (source: d2#33))*

---

**22. D** — A strict `input_schema` on a tool, with tool use forced, enforces the JSON shape structurally — Claude cannot return anything the schema doesn't allow. Repeating instructions in prose, asking users to phrase things differently, or manual sampling review are all requests or spot-checks, not guarantees. *(task 2.5; concept: structural_enforcement_over_prose; item `mock2-22` (source: d2#34))*

---

**23. C** — Retrieving the real source documents and passing their actual identifiers into context, then requiring citations to reference one of those identifiers, ties every citation to something genuinely present rather than merely requested. Lower temperature, asking twice, and more `max_tokens` don't connect the citation to an actual retrieved source. *(task 2.5; concept: grounded_citations_via_retrieval; item `mock2-23` (source: d2#35))*

---

**24. D** — Falling back to a simpler, non-Claude search path when the API is unavailable keeps the feature partially working instead of going completely blank during an outage the underlying database isn't even affected by. Retrying rapidly, pre-caching every possible answer, and raising `max_tokens` don't restore search during an actual API outage. *(task 2.5; concept: graceful_degradation_api_unavailable; item `mock2-24` (source: d2#50))*

---

**25. D** — One codebase with externalized per-environment config keeps behavior differences visible in config rather than duplicated across copies of the code, which is exactly what drifts out of sync over time. Separate codebases guarantee drift the moment one copy is edited and the others aren't; merging away the distinction removes a needed capability; deleting staging doesn't address the configuration question at all. *(task 2.6; concept: single_codebase_env_config; item `mock2-25` (source: d2#19))*

---

**26. A, B** — Per-environment keys injected via a secret store, plus immediate rotation the moment a key is found exposed anywhere, are both genuine security practices. Sharing one production key everywhere widens the blast radius of any single leak, and baking a key into a compiled binary just moves the exposure surface rather than removing it. *(concept: secrets_handling_practices; item `mock2-26`)*

---

**27. A, B** — Enterprise policy sits above both project and user settings in precedence, and CLAUDE.md files at different directory levels layer together instead of one replacing the other. Claude Code doesn't use file modification time to resolve conflicts, and subdirectory CLAUDE.md files load automatically, not only when explicitly referenced. *(concept: settings_and_memory_hierarchy; item `mock2-27`)*

---

**28. A** — A `PreToolUse` hook runs before the tool call executes and can block it outright when the allowlist script fails, matching the requirement to stop the command before it ever runs. A manual slash command depends on engineers remembering to run it, a `CLAUDE.md` instruction is only a request Claude might not follow, and a `PostToolUse` hook only observes the command after it has already executed. *(task 3.1; concept: hook_lifecycle_event; item `mock2-28` (source: d3#4))*

---

**29. A** — Pairing known-correct extractions with deliberately broken edge cases like the missing signature block is exactly what a golden eval set is for: it catches failures a single-client demo never would. Throughput, injection probing, and supervised fine-tuning are all different purposes that fifty labeled documents could serve, but none matches what's described here. *(task 4.1; concept: golden_eval_dataset_construction; item `mock2-29` (source: d4#2))*

---

**30. B** — Every cache hit resets the five-minute TTL, so the 4-minute gap since the last hit is well within the window and the segment is still cached. The TTL isn't fixed from the original write, it's measured in minutes rather than hours, and no miss occurred in this scenario to invalidate anything. *(task 5.1; concept: cache_ttl_reset_on_hit; item `mock2-30` (source: d5#4))*

---

**31. A, B** — This request fails both of extended thinking's independent numeric constraints at once: the 500-token budget doesn't clear the 1,024-token floor, and the 400-token `max_tokens` doesn't exceed it. `thinking` is correctly a top-level request parameter, not something nested in `messages`, and extended thinking works across Claude model snapshots, not just specific ones. *(concept: extended_thinking_dual_constraint; item `mock2-31`)*

---

**32. C** — When extended thinking is enabled, `temperature` must be 1.0 or left out entirely; a value like 0.2 fails validation. Lowering `budget_tokens` further doesn't fix a temperature conflict, `top_p` isn't a required companion parameter, and `max_tokens` still has to be set and simply must exceed `budget_tokens`. *(task 5.1; concept: thinking_requires_temperature_one; item `mock2-32` (source: d5#6))*

---

**33. C** — System prompt, conversation history, the new user turn, and the completion all draw from one shared, finite context-window token budget, so with only 6,000 tokens of headroom left, a 3,000-token turn plus a requested 5,000-token completion cannot all fit — the completion gets truncated or the call is rejected. Completions are not generated in a separate token space, the system prompt isn't auto-evicted to make room, and caching doesn't shrink what counts against the context window. *(task 5.2; concept: context_window_shared_token_budget; item `mock2-33` (source: d5#10))*

---

**34. A** — Claude processes text as subword tokens rather than individual characters, so a single token can bundle several letters together in a way the model never directly inspects letter-by-letter, which is why character-counting tasks can go wrong. The context window is large enough to hold a single word, temperature doesn't drop letters from the input, and extended thinking isn't a strict requirement for this class of task. *(task 5.2; concept: tokenization_limits_character_tasks; item `mock2-34` (source: d5#11))*

---

**35. B** — `max_tokens` only sets a ceiling on how many tokens the completion may contain; it has no bearing on the reasoning quality or factual accuracy of the tokens actually generated, which is why doubling it left summaries unchanged. Lowering it wouldn't have improved accuracy either, it governs output length rather than the context window available for input, and it isn't required to move in lockstep with `temperature`. *(task 5.2; concept: max_tokens_caps_length_not_quality; item `mock2-35` (source: d5#12))*

---

**36. C** — Sonnet is positioned as the balanced middle tier, offering faster responses and lower cost than Opus while handling moderate synthesis tasks better than the fastest tier alone — the fit this dashboard workload needs. Haiku isn't automatically correct whenever latency matters if the task needs more synthesis than it comfortably provides, Opus is more than this workload requires, and model tier does affect both latency and reasoning quality, not just cost. *(task 5.3; concept: sonnet_balanced_tier; item `mock2-36` (source: d5#15))*

---

**37. B** — Enabling extended thinking means spending extra tokens and added latency on visible step-by-step reasoning in exchange for better accuracy on multi-step problems — a deliberate cost/latency-for-quality tradeoff, not a tier switch. Extended thinking works with Opus and isn't restricted to the fastest tier, thinking tokens are billed as regular output rather than at a discount, and thinking does not guarantee a correct final answer. *(task 5.3; concept: extended_thinking_tradeoff_decision; item `mock2-37` (source: d5#16))*

---

**38. A, B** — The Batch API exists specifically for asynchronous, non-urgent volume, and results genuinely aren't retrievable — not even partially — until the batch reaches `ended`. There's no fixed 4,096-token `max_tokens` floor, and batch processing is explicitly not a real-time streaming mechanism. *(concept: batch_api_accuracy; item `mock2-38`)*

---

**39. A** — Reasoning through each factor step by step before stating a verdict gives the model room to work through the combination consistently, which is the point of chain-of-thought prompting for multi-step reasoning. Skipping explanation removes exactly the reasoning space that's missing; capping `max_tokens` at 1 would cut off any answer at all, not just improve consistency; and moving the combination outside the prompt sidesteps the reasoning task rather than improving it. *(task 6.1; concept: chain_of_thought_reasoning; item `mock2-39` (source: d6#4))*

---

**40. B** — A style described only in the abstract gives the model nothing concrete to match; a single worked example of the desired concise, formal tone would give it a pattern to follow. Style guidance can live in the system prompt just fine, so relocating it isn't the fix; "concise" being read as "one sentence" doesn't match the reported symptom of casual, wordy output; and nothing in the scenario suggests the instruction is being crowded out of context. *(task 6.1; concept: worked_example_over_description; item `mock2-40` (source: d6#5))*

---

**41. C** — Replacing a negative instruction with a positive description of the desired form gives the model something to aim for, rather than only something to avoid, which tends to hold up better against pull from the input material. Restating the same negative instruction more forcefully doesn't change what it's asking for; removing the instruction removes any guidance at all; and relocating an unchanged prohibition to a different part of the prompt doesn't change its phrasing. *(task 6.1; concept: positive_instruction_framing; item `mock2-41` (source: d6#6))*

---

**42. C** — A content block with `type: "image"` and a `source` object specifying `type: "base64"`, the correct `media_type`, and the base64 `data` is the structured way multimodal image input is represented in a request. Embedding the base64 string as plain text loses the structural markers the model relies on to treat it as image data; a `tool_result` block is for returning tool output, not for submitting user-supplied images; and there is no persistent system-prompt slot for image bytes. *(task 6.2; concept: multimodal_image_content_block; item `mock2-42` (source: d6#9))*

---

**43. D** — Wrapping each document in `<document>` tags and placing the marked question after the closing tags gives the model a clear boundary between reference text and the actual instruction to act on. Deleting sources doesn't fix the lack of a boundary, it just reduces how often the confusion can occur; moving the question into the system prompt doesn't establish where the documents end; and capitalizing the question is a cosmetic change with no structural effect. *(task 6.2; concept: reference_material_boundary_tags; item `mock2-43` (source: d6#10))*

---

**44. A, C** — Reading a structured, schema-validated field directly avoids the coincidental-substring problem that keyword matching over free text creates. Tool use enforces output shape, not the correctness of the underlying judgment, and it says nothing about preventing duplicate calls across turns. *(concept: tool_use_over_string_matching_benefits; item `mock2-44`)*

---

**45. A, C** — Both A and C describe adversarial instructions arriving through ingested content (a scraped review, a summarized email) that the model reads as data — the defining pattern of indirect injection. B is direct injection since the user is the one typing the attack, and D is a secrets-handling failure, not an injection attack at all. *(concept: classifying_indirect_injection; item `mock2-45`)*

---

**46. C** — Printing the secret into logs and then committing that line exposes the raw key to anyone with log or repository access, undermining whatever key-management controls exist elsewhere. The commit message's clarity, `print`'s performance, and the variable's naming are all real but unrelated to the actual exposure. *(task 7.1; concept: secrets_in_logs_and_commits; item `mock2-46` (source: d7#4))*

---

**47. A** — Uncapped volume and unscreened output are two separate failure modes needing two separate guardrails: per-user rate limiting bounds request volume, and output content filtering catches policy-violating responses. A bigger context window, a cheaper model, and more few-shot examples are all performance or cost tweaks that leave both original problems in place. *(task 7.2; concept: rate_limiting_and_content_filtering; item `mock2-47` (source: d7#6))*

---

**48. A** — Because the tool trusts whatever `customer_id` the model supplies instead of enforcing the logged-in session's identity, the agent can be manipulated into querying another customer's records under the same broad credential — exactly the identity-boundary failure the scenario sets up. A connection pool limit, query latency, and an inability to serve the logged-in customer are unrelated side effects, not the risk this gap creates. *(task 7.3; concept: identity_scoped_data_access; item `mock2-48` (source: d7#8))*

---

**49. A, D** — `input_schema` is the third required top-level key alongside `name` and `description`, and adding one with `type` and `properties` is exactly what fixes a definition missing it. `tool_choice` is a request-level parameter, never a key inside the tool object itself, so it isn't what the lint step is flagging — and the lint step is correctly catching a real gap, not a false positive. *(concept: tool_definition_required_keys; item `mock2-49`)*

---

**50. A** — When Claude issues multiple `tool_use` blocks in one assistant turn, the follow-up must be a single `user` message containing a `tool_result` for every `tool_use_id` — splitting them across two consecutive `user` messages is invalid. Matching `tool_use_id` values across two different calls would be wrong, not required; nothing about parallel calls dictates execution order; and MCP-style parallel results don't need a wrapping `system` message. *(task 8.1; concept: parallel_tool_result_batching; item `mock2-50` (source: d8#4))*

---

**51. B** — CLAUDE.md is loaded automatically at session start, which is exactly what makes standing rules like ticket references and a force-push ban apply every session without anyone invoking them by name. A slash command still requires typing it before each commit, a subagent invoked only for release branches wouldn't cover everyday commits, and a tool's `input_schema` only shapes that one tool's arguments. *(task 8.2; concept: claude_md_standing_rules; item `mock2-51` (source: d8#7))*

---

**52. C** — Neither mechanism alone covers both requirements: a slash command supplies the on-demand, typed-by-name trigger, but only a subagent supplies its own isolated context window and restricted tool access, so a slash command that dispatches to a dedicated subagent is what covers both. CLAUDE.md applies automatically rather than on demand, a bare slash command doesn't isolate context by itself, and a bare subagent isn't invoked by typing a name mid-conversation. *(task 8.2; concept: slash_command_plus_subagent; item `mock2-52` (source: d8#8))*

---

**53. D** — stdio is the transport for local integrations, where the client spawns the server as a child process and the two communicate over stdin/stdout with no network exposure. SSE is MCP's transport for remote, networked servers instead; WebSocket and gRPC are not among MCP's two defined transports at all. *(task 8.3; concept: mcp_transport_stdio; item `mock2-53` (source: d8#10))*
