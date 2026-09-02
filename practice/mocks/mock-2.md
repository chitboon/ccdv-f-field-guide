# CCDV-F Mock Exam 2 — Blueprint-Exact (53 items, fresh content)

Same blueprint-proportional coverage as Mock 1 (D1=8, D2=18, D3=2, D4=1,
D5=9, D6=6, D7=4, D8=5 = 53), rebuilt from scratch against exam objectives
and Academy material — none of these 53 items are drawn from the
domain-drill pool. Every scenario here is distinct from Mock 1 — zero stem
overlap. 16 items (30.2%) are multi-response ("Select TWO"). Sealed key in
`mock-2-key.md`. Sit this one timed at 120 minutes as the closer rehearsal
to the real exam once Mock 1 is reviewed.

---

**1.** `[task 1.1 · loop_decides_from_output]` An inventory-reorder script always calls `check_stock`, then `calculate_reorder`, then `submit_po`, in that exact order, regardless of what any step returns. A teammate proposes replacing it with a Claude-driven loop that reads each tool's actual result and decides the next call itself. What single property would make the replacement agentic rather than a fixed pipeline?

A. The replacement would call more tools overall than the original three-step script did, on every run.
B. It reads each tool's output and picks its own next action instead of a fixed order.
C. The replacement would run at a lower `temperature` setting than the original fixed script used.
D. The replacement would submit purchase orders through the Batches API instead of the standard synchronous one used today.

---

**2.** `[task 1.1 · max_tokens_truncation_alert]` A translation service currently treats every Claude response the same way regardless of `stop_reason`, and has occasionally shipped a sentence cut off mid-word to end users. Which `stop_reason` value specifically signals output was cut short by a length limit, and should route to special handling instead of being shipped as-is?

A. `max_tokens`, since it means the response was truncated by the length limit rather than finishing naturally.
B. `end_turn`, since it means the model reached a natural stopping point on its own accord.
C. `tool_use`, since it means the model paused to invoke a tool rather than continue writing text.
D. A missing `stop_reason` field entirely, since Claude only omits that field when a response gets cut short.

---

**3.** `[task 1.2 · context_trim_preserve_brief]` A coding-assistant session has run 90 turns and accumulated dozens of full file-read tool outputs by turn 70, nearing the model's context ceiling. The team wants the loop to keep running without losing the original task brief given at the start.

A. Truncate the system prompt itself once the turn count passes a fixed threshold, since it's the largest fixed cost.
B. Keep the system prompt and recent turns, summarizing or dropping the oldest file-read outputs.
C. Restart the session from scratch with no prior history every time the turn count crosses the threshold.
D. Keep every file-read output in full and instead shorten the original task brief to make room.

---

**4.** `[task 1.2 · tool_result_is_error_recovery]` A `print_label` tool call fails inside a shipping-label agent's loop, coming back with `"is_error": true` and the content `"printer offline"`. On the next turn, what's the right way to handle that result?

A. Let the model see the error and choose a recovery step, such as retrying or switching printers.
B. Discard the `is_error` flag and treat the string as if a label had actually printed successfully.
C. End the session outright, since a printer failure means the task can never be completed at all.
D. Keep resending the identical `print_label` call every few seconds until the printer comes back online.

---

**5.** `[task 1.2 · tool_interface_needs_description]` A `lookup_customer` tool accepts an undocumented `id` string and either returns a customer record or silently returns `null`, with no explanation of why a given ID failed.

A. Rename the tool to something shorter, on the theory that shorter tool names get selected more reliably.
B. Increase `max_tokens` on the request, since more output room is assumed to fix silent lookup failures.
C. Document the expected `id` format and return a structured reason whenever the lookup comes back empty.
D. Remove the `id` parameter, since a tool with no parameters at all is assumed to be less error-prone.

---

**6.** `[task 1.2 · structured_error_per_failure_type]` A `book_flight` tool returns the same generic string `"error"` whether a fare expired, a card was declined, or the airline's API timed out, leaving the calling agent with no way to choose between retrying, asking for a new card, or giving up.

A. Return a fixed apology message to the user instead of any structured detail about what failed.
B. Return distinct, structured error content per failure type so the agent can tell the cases apart.
C. Silently retry the exact same request up to five times before ever reporting anything back to the agent.
D. Remove the `book_flight` tool from the agent's tool list the first time any error occurs.

---

**7.** `[task 1.3 · orchestrator_workers_research]` A market-research briefing pulls data from five unrelated sources — weather, stock prices, social sentiment, traffic, and news — through one coordinator call that splits the job into five subtasks, dispatches one worker call per source, and combines every result into a single report. Which pattern does this describe?

A. Orchestrator-workers: a coordinator decomposes the briefing, delegates each source, and synthesizes results.
B. Prompt chaining, since each of the five data sources would be queried in one fixed, predetermined sequence every time.
C. A single linear agent, since one continuous loop could in principle query all five sources by itself.
D. Routing, since a classifier would read the request and send it to exactly one of the five specialized sources.

---

**8.** `[task 1.3 · evaluator_optimizer_patent_claim]` A patent-claim drafting workflow submits a claim to one Claude call for an initial version, then a second call flags any wording likely to be rejected as overly broad and explains exactly why, feeding those flags back into the first call for a narrower rewrite, continuing until the flagged-issue count hits zero. What does this describe?

A. A classifier deciding which patent office's rules apply before any drafting work starts at all.
B. A coordinator splitting the claim into independent clauses for separate, unrelated drafting passes.
C. A generator and a separate critic looping together until the claim clears every flagged objection.
D. Several claim drafts produced side by side, with whichever one looks strongest chosen afterward.

---

**9.** `[task 2.1 · ambiguous_requirement_wrong_scope]` Three weeks after a "flag risky submissions" feature ships, a newsroom's editorial lead is stunned to find it only catches typos — she'd assumed from the start it would screen for legal liability. Which of the following would have caught the mismatch earliest?

A. Assembling a bigger engineering team once the wrong feature has already begun shipping.
B. Raising `max_tokens` on every related request so responses come back more completely.
C. Holding a retrospective only after the mismatched feature has already been delivered.
D. A signed-off scope document naming the capability meant, before work starts.

---

**10.** `[task 2.1 · requirements_traceable_to_tests]` An onboarding-email generator has a written rule that it must never mention a discontinued product line, but that rule was never wired into any automated check. Two months after launch, a churned customer receives an email pitching the exact discontinued product. Which practice would have caught this before it reached a customer?

A. A more prominent mention of the requirement on the internal team wiki, in a larger font.
B. One engineer manually re-reading every generated email by hand before it ships.
C. Tracing the requirement to an automated test that fails whenever a discontinued product is mentioned.
D. A verbal mention of the requirement during a single standup meeting.

---

**11.** `[task 2.2 · iterative_vs_upfront_design_llm]` A vendor is scoping a research-assistant feature whose real question patterns can't be known until actual users start typing into it — something nobody can fully predict before launch. Which process best fits a feature with this kind of built-in uncertainty?

A. A fully upfront specification, since it removes uncertainty the same way it does for a traditional CRUD form.
B. An iterative approach that ships a narrow version early and refines it based on real usage data.
C. No process at all, since any structured process would only slow the team down here.
D. A fixed six-month timeline agreed in advance, regardless of what real usage data later shows.

---

**12.** `[task 2.3 · native_pdf_page_and_size_limit]` An HR team's résumé-screening tool accepts most candidate portfolios without issue, but rejects one candidate's 45MB scanned portfolio outright, even though it has fewer total pages than several other files the same pipeline already accepted that week.

A. Native PDF processing caps out at 100 pages and 32MB, and this file's 45MB size exceeds that limit.
B. PDFs must be converted to a sequence of images before Claude can process any of them at all.
C. The rejection means the account has exhausted its available request credits for the billing period.
D. The 100-page/32MB limit only applies to scanned reports specifically, not to other document categories.

---

**13.** `[task 2.3 · cloud_sdk_bedrock_vertex]` A hospital system's data-governance board will only approve a Claude integration if every API call passes through infrastructure the hospital already operates and audits — its existing Google Cloud project. Which SDK satisfies that requirement?

A. The standard Anthropic Python SDK, authenticating with a bare API key as usual.
B. `AnthropicBedrock`, since it is built specifically for AWS infrastructure.
C. `AnthropicVertex`, which authenticates through Google Cloud's application default credentials.
D. A custom-built wrapper, since no first-party SDK supports routing through a company's own GCP project.

---

**14.** `[task 2.3 · streaming_helper_choice]` A batch-summarization script needs the entire finished response as one plain string once generation completes, without manually concatenating individual stream chunks itself.

A. Continue concatenating each `text_stream` chunk by hand into one string.
B. Read `.usage` off `get_final_message()`, since usage data already contains the complete response text.
C. Re-request the same prompt without streaming enabled, discarding the streamed version entirely.
D. `stream.get_final_text()`, returning the complete response as one string once streaming finishes.

---

**15.** `[task 2.4 · canary_rollout_new_tool_integration]` Before letting a brand-new `auto_translate_ticket` tool touch every incoming support ticket, a team wants a way to cap how many customers would be affected if the integration turns out to have a hidden bug.

A. Require every user to manually opt in through account settings before the tool activates.
B. Test the integration only in local development before a single full release.
C. Gate the tool behind a flag for a small percentage of sessions, widening once proven stable.
D. Ship the new tool to all traffic immediately, monitoring closely afterward.

---

**16.** `[task 2.4 · tool_schema_versioning_compat]` Dozens of integration partners call a `schedule_appointment` tool with no `preferred_language` field at all, and none of them can be forced to redeploy on short notice — yet the field still needs to start rolling out.

A. Remove the field's optional status immediately, requiring every partner to send it starting today.
B. Replace the whole tool with a brand-new one under a different name.
C. Rename the existing tool so unmigrated partners naturally stop reaching it.
D. Accept the old shape as valid, ignoring the field until partners migrate.

---

**17.** `[task 2.4 · correlation_id_tracing_multitool]` A fraud-review dashboard shows three separate tool calls that appear to belong to the same customer interaction, but nothing in the logs actually ties them together, making a post-incident timeline impossible to reconstruct with confidence.

A. Reduce the number of tools available to the agent so fewer calls happen per session.
B. Log only the final tool call of each session, discarding the intermediate ones.
C. Extend log retention so events are kept around for a longer period of time.
D. Tag every tool call with that session's shared correlation ID, set at the start.

---

**18.** `[task 2.4 · mocked_api_for_ci_isolation]` A nightly regression suite calls the live Claude API for every one of its 200 test cases, and roughly one run a week fails for reasons that turn out to be a transient outage or rate limit rather than an actual regression in the code.

A. Blindly retry every failing CI run up to ten times without investigating why it failed.
B. Pad every request's timeout to several hours so slow responses never register as failures.
C. Replace the live API call in the pipeline with a mocked client, while a separate suite checks the real API.
D. Drop the automated check from CI entirely, relying on manual review instead.

---

**19.** `[task 2.5 · single_agent_vs_many_specialists]` One Claude agent is currently responsible for triaging incoming bug reports, drafting release notes, and answering customer billing questions, and its output quality has visibly dropped as all three responsibilities compete for the same system prompt's attention.

A. Split into role-scoped agents, giving triage, release notes, and billing questions each a narrower prompt.
B. Run three unmodified copies of the same combined prompt in parallel instead.
C. Lower the shared agent's `temperature` setting to reduce the confusion between domains.
D. Pile on more instructions to the same combined prompt, describing each responsibility in more detail.

---

**20.** `[task 2.5 · app_layer_rate_limiting_runaway_loop]` A team notices their `fetch_paper` tool was called on the identical DOI more than forty times within a single research-agent run, with no progress between calls — whatever caused it, they want a limit that holds regardless of what the model chooses to do next.

A. Ask the system prompt to politely request that the agent avoid repeating calls.
B. Raise the account's overall API rate limit so the loop can complete faster.
C. Enforce a per-session cap on tool-call count or rate at the application layer.
D. Switch to a slower model, hoping fewer calls happen per unit of time.

---

**21.** `[task 2.5 · fallback_ux_validation_failure]` Applicants using a résumé-parsing agent sometimes get stuck on an infinite spinning loader — no error, no message — whenever the agent's structured output happens to fail a downstream field-format check.

A. Let the loader keep spinning indefinitely, since the failure is rare enough to ignore.
B. Silently loop the same request forever without ever informing the applicant anything went wrong.
C. Disable structured output for every applicant rather than handling this one failure case.
D. Detect the field-format failure and show a clear message with a retry option.

---

**22.** `[task 2.5 · versioned_conversation_schema_storage]` A helpdesk platform has years of ticket threads stored as flat plain-text fields, and product now wants new tickets to support inline file attachments with proper metadata, without corrupting or discarding any of the historical plain-text threads already on file.

A. Encode attachment data directly into the existing plain-text column without changing the schema.
B. Delete all existing ticket history to make room for the new schema.
C. Store every future ticket as one large unstructured blob regardless of content type.
D. Version the ticket schema, so old rows stay valid while new ones carry typed attachments.

---

**23.** `[task 2.5 · idempotent_webhook_triggered_agent]` A lead occasionally receives two nearly identical outreach emails back to back — the underlying cause is a CRM contact-form webhook firing twice under normal at-least-once delivery, with each firing spinning up its own fresh drafting-agent run.

A. Disable the webhook integration outright rather than handling duplicate deliveries.
B. Push the fix onto the provider by asking them to change their delivery guarantee.
C. Deduplicate on the event's unique ID before starting a new agent run, turning a repeat into a no-op.
D. Increase `max_tokens` on the agent run so it finishes before a second delivery can arrive.

---

**24.** `[task 2.6 · fail_fast_startup_config_validation]` A background worker occasionally crashes hours into processing a long queue with a cryptic connection error, and tracing it back reveals the real cause is a required configuration value that was simply never set in that environment.

A. Log a warning about the missing value and continue running as though nothing were wrong.
B. Hardcode a fallback value for the missing configuration so the service always starts.
C. Validate every required configuration value at startup, refusing to start when one is missing.
D. Catch the eventual error wherever it surfaces downstream and log it quietly there.

---

**25.** `[task 2.3 · retryable vs non-retryable exceptions]` A team building a retry wrapper around the Python SDK wants to distinguish exceptions worth retrying from exceptions that will fail the exact same way no matter how many times the request is resent. Which TWO exceptions belong in the "safe to retry with backoff" category? (Select TWO)

A. `anthropic.RateLimitError` — the request itself was valid; the account has temporarily exceeded a rate quota.
B. `anthropic.PermissionDeniedError` — the workspace or API tier lacks permission for this request, a request-shape problem.
C. `anthropic.InternalServerError` — a transient failure on Anthropic's infrastructure side, not the request's fault.
D. `anthropic.NotFoundError` — the referenced resource ID doesn't exist and won't start existing on retry.

---

**26.** `[task 2.6 · secrets handling guidelines]` A platform team is writing internal guidelines for how services should handle their Anthropic API keys across dev, staging, and production. Which TWO of the following guidelines should make it into the document? (Select TWO)

A. Each environment gets its own key, injected via the deployment platform's secret store, never checked into version control.
B. Rotate a key immediately if it's ever found in a commit history, git log, or log aggregator.
C. Reuse one shared production key across all environments to simplify credential management.
D. Store the key as a plain build-time constant baked into the compiled application binary.

---

**27.** `[task 3.1 · settings-based permission allowlisting]` A team wants Claude Code to run `git status` and `git diff` freely inside a repo, but require explicit approval before running any `git push` command, without writing a custom hook script. Where should this rule live?

A. In a `PreToolUse` hook script that pattern-matches the command string before every single Bash call made.
B. In `CLAUDE.md`, asking the agent politely to always confirm before pushing to a remote.
C. In `.claude/settings.json`'s permission rules, allow-listing the read-only subcommands.
D. In a custom slash command that wraps every git operation the team might ever run.

---

**28.** `[task 3.1 · settings and memory hierarchy]` Two engineers disagree over which of several claims about Claude Code's settings and memory hierarchy actually holds up, after a project rule seemed to get silently overridden last week. Which TWO of these claims are correct? (Select TWO)

A. Project-level settings can override user-level settings, but neither can override an enterprise-managed policy.
B. Memory from a root `CLAUDE.md` and a nested package's `CLAUDE.md` combine rather than one silently replacing the other.
C. Settings conflicts are resolved by file modification timestamp, with the newest edit always winning.
D. A subdirectory `CLAUDE.md` is ignored entirely unless explicitly referenced by path in the prompt.

---

**29.** `[task 4.1 · sampling variance vs real regression]` A team's eval suite runs the same 30 prompts against Claude at `temperature: 1.0` and treats any run below a 90% pass threshold as a regression requiring investigation. Pass rates swing between 83% and 97% across otherwise-identical runs with no code or prompt changes in between. What change addresses the actual cause?

A. Lower the pass threshold to 80% so fewer runs trigger a false alarm each time.
B. Switch to a larger model, since larger models never exhibit run-to-run variance at all.
C. Increase `max_tokens` so each response has more room to reach the correct answer.
D. Run the eval at `temperature: 0`, or average multiple runs, so swings reflect real change.

---

**30.** `[task 5.1 · cache_min_token_threshold]` Every Claude 3 Opus request in a financial-disclosure assistant tags a 950-token system prompt with `cache_control: {"type": "ephemeral"}`, expecting a cheaper call from the second request onward — yet no request ever registers a cache hit. Why not?

A. Ephemeral breakpoints only apply to Claude 3.5 Haiku, not to any model in the Opus family at all.
B. The 950-token block falls short of the 1,024-token minimum that Claude 3 Opus requires for a cacheable segment.
C. The system prompt was placed after the user turn instead of first, so no prefix could be cached.
D. The five-minute cache TTL had already lapsed between the two calls, resetting the cached prefix to nothing.

---

**31.** `[task 5.1 · subword_tokenization_ratio]` Budgeting `max_tokens` for a 320-word indemnification clause, a paralegal assumes roughly one token per word — yet the actual request logs 470 input tokens for that same clause. What accounts for the gap?

A. The context window silently truncated part of the clause before tokenizing the remainder that was actually sent.
B. Prompt caching inflated the reported token count by treating the clause as a repeated prefix from an earlier call.
C. The request must have included a duplicated system prompt that got counted twice against the token budget.
D. Claude tokenizes in subwords, splitting words and punctuation into multiple tokens rather than one-to-one.

---

**32.** `[task 5.1 · extended thinking dual constraint]` This request fails validation before any generation begins:

```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=400,
    thinking={"type": "enabled", "budget_tokens": 500},
    messages=[{"role": "user", "content": "Solve this step by step: ..."}],
)
```

Which TWO separate problems does this specific request have? (Select TWO)

A. `budget_tokens` (500) is below the 1,024-token minimum extended thinking requires.
B. `max_tokens` (400) is not strictly greater than `budget_tokens` (500), which the API requires.
C. `thinking` must be nested inside the `messages` array, not passed as a top-level request parameter.
D. Extended thinking is not compatible with the `claude-3-5-sonnet-20241022` model snapshot at all.

---

**33.** `[task 5.2 · context_window_shared_token_budget]` After a long-running analysis session accumulates well over 175,000 combined tokens of history and instructions inside a 200,000-token window, a request for a lengthy summary comes back cut off partway through. An engineer wants to know why completions apparently "run out of room" the same way input does. What's the explanation?

A. The completion gets truncated or the request is rejected, since input and output share one finite context-window budget.
B. The request succeeds normally, because completions are generated in a token space entirely separate from the input history.
C. The system prompt is automatically dropped first so the full completion can still be produced without any error.
D. Prompt caching automatically compresses the history, since cached segments no longer count against the context window at all.

---

**34.** `[task 5.2 · tokenization_limits_character_tasks]` A person reversing an unfamiliar word letter by letter finds it trivial, yet Claude — asked to do the exact same thing — sometimes produces letters out of order. What about how the model processes text explains this gap?

A. The model's context window is too small to hold one long word, so part of it gets truncated first.
B. Temperature above zero randomly reorders individual letters within the input before any processing begins at all.
C. The model operates over subword tokens rather than individual characters, obscuring letter order.
D. Extended thinking is strictly required for any letter-reversal task, and it was left disabled in this particular test case entirely.

---

**35.** `[task 5.2 · max_tokens_caps_length_not_quality]` Hoping fewer missing details will show up in drafted replies, a developer doubles an email-drafting endpoint's `max_tokens` from 256 to 512 — and the output quality doesn't budge. What does that outcome reveal about what `max_tokens` actually governs?

A. `max_tokens` was set too high, and lowering it back toward 256 would have improved reply quality.
B. `max_tokens` only caps completion length; it doesn't influence reasoning or accuracy.
C. `max_tokens` governs the size of the context window available for reading the input, not just the output.
D. `max_tokens` and `temperature` must always change together, so quality regressed only because `temperature` stayed fixed the whole time.

---

**36.** `[task 5.3 · sonnet_balanced_tier]` Inside a live dashboard, a sales-enablement chatbot needs decent synthesis across several call transcripts at once, snappy enough responses for back-and-forth use, and a per-call cost nowhere near Opus pricing — but not the very deepest reasoning available. Which tier is built for exactly that middle ground?

A. Claude Sonnet, since it is positioned as the balanced tier between Haiku's speed and Opus's reasoning depth and cost.
B. Claude Opus, since summarizing several transcripts at once always requires the single most capable tier available today.
C. Claude 3.5 Haiku, since its speed advantage makes it the correct default whenever latency matters at all.
D. Any tier works identically here, since model choice only affects cost and never affects latency or reasoning quality.

---

**37.** `[task 5.3 · extended_thinking_tradeoff_decision]` Knowing full well that thinking tokens bill as ordinary output and add measurable latency, a team still debates turning on extended thinking with a 6,000-token `budget_tokens` for a spreadsheet-formula-debugging assistant already running on Claude Opus. What tradeoff are they actually weighing?

A. Switching the underlying model tier from Opus to Haiku, since extended thinking only works on the fastest tier.
B. Reducing the request's total cost, since thinking tokens are billed at a discounted rate versus normal output.
C. Guaranteeing a correct final formula, since extended thinking adds a deterministic verification pass after generation finishes.
D. Spending additional tokens and latency on visible step-by-step reasoning in exchange for better accuracy on multi-step problems.

---

**38.** `[task 5.4 · Batch API accuracy check]` Two engineers disagree over lunch about how the Message Batches API actually behaves in production, and decide to settle it by listing out claims and checking each one. Which TWO of these claims turn out to be true? (Select TWO)

A. The Batch API is intended for non-urgent, asynchronous workloads, not requests needing an immediate response.
B. Attempting to download results while the batch is still `in_progress` returns a 404, not partial results.
C. Every batch request must set `max_tokens` to at least 4,096 tokens regardless of the task.
D. Batches API responses stream back to the client in real time via Server-Sent Events, like the standard API.

---

**39.** `[task 6.1 · xml_section_delimiting]` A meal-kit bot's `system` string is built by joining `recipe_excerpt` with two hard-coded allergy rules, with no separators between them. A customer once received a reply that repeated a recipe-database ingredient line back verbatim, phrased as though it were a binding rule the bot had to follow for every future order. What fixes the underlying cause?

A. Wrap `recipe_excerpt` in one named tag and the two allergy rules in a second, separately named tag entirely.
B. Cap `recipe_excerpt` at a fixed token count so the joined string stays noticeably shorter overall, every single call.
C. Move `recipe_excerpt` into the customer's own message, leaving the two allergy rules in `system` by themselves.
D. Add `stop_sequences=["Ingredients:"]` to the request so generation halts at that heading every time it appears.

---

**40.** `[task 6.1 · few_shot_pattern_demonstration]` A changelog-entry tool is told only, in prose, to turn a raw commit list into one past-tense bullet per user-facing change with no ticket numbers. In practice, ticket numbers leak into bullets, tense stays mixed, and some commits still produce two bullets instead of one. Before changing the wording of the instruction again, what's the more effective fix?

A. Restate the same prose instruction a second time, back to back, inside the system prompt itself.
B. Relocate the unchanged instruction from the system prompt into every individual user turn instead.
C. Show worked commit-to-bullet pairs demonstrating the shape, not just restating the rule.
D. Raise `max_tokens` so the model has enough room to finish every bullet without ever truncating.

---

**41.** `[task 6.1 · chain_of_thought_reasoning]` An insurance-triage prompt hands Claude the incident severity score, coverage limit, and prior-claims count, then asks for one bare word: `approve` or `escalate`. Two claims with nearly identical inputs, submitted minutes apart, come back with opposite verdicts. Before touching the input data, what prompt change is most likely to make the verdict logic more repeatable?

A. Cap `max_tokens` at 1 so Claude has no room to output anything at all but the bare verdict itself.
B. Tell Claude to skip any explanation and answer with only the bare verdict word.
C. Fold the three inputs into a single external score and hand Claude only that number, nothing else.
D. Have Claude reason through each factor inside `<thinking>` tags first.

---

**42.** `[task 6.2 · system_prompt_vs_user_message]` A documentation-generation service reconstructs its prompt from scratch on each call: the docstring format spec and naming-convention rules are read from a config file and appended directly before the function source in that single user turn, request after request, with the `system` field left at its default empty string. What should change about where the spec and rules live?

A. Leave the `system` field empty as it is, but move the function source above the spec and rules in `content`.
B. Move the two stable pieces into `system`, leaving the function source alone in the user turn.
C. Read the function source from the same config file too, so every piece of context loads from one place.
D. Alternate which call in the rotation carries the spec and naming rules so average token usage evens out.

---

**43.** `[task 6.2 · reference_material_boundary_tags]` A meeting-notes assistant concatenates three full transcripts into the same message as the user's follow-up question, with no marker distinguishing recorded dialogue from the actual instruction. Because one transcript happens to end on a line that reads like a request, Claude sometimes responds to that line instead of the real question that follows it. What change resolves this?

A. Enclose each transcript in its own document tag, with the follow-up question placed after them.
B. Trim the transcripts down to only the most recent meeting to shorten the combined message overall.
C. Move the follow-up question into the system prompt instead of the user message.
D. Write the follow-up question in all capital letters to increase its visual priority.

---

**44.** `[task 6.3 · why tool use beats string matching]` A team debating whether to keep their keyword-matching output parser or switch to tool-based extraction lists out the claimed benefits of switching. Which TWO claims are actually true benefits of the tool-use approach? (Select TWO)

A. Downstream code reads a structured field directly, instead of searching free text for a substring that might appear by coincidence.
B. Tool-based extraction automatically improves the accuracy of the underlying decision being extracted.
C. It removes false positives caused by Claude's prose explanation happening to mention a different category's keyword.
D. It guarantees the tool call will never be duplicated across parallel turns.

---

**45.** `[task 7.1 · insecure output handling]` An internal wiki bot lets a coding agent post model-generated summaries as raw HTML on a shared team page, with no escaping or sanitization applied. An attacker submits a support ticket whose text includes a `<script>` tag; the agent's summary of that ticket is rendered directly into the wiki page, and the script executes for every visitor who opens it. What security failure does this illustrate?

A. Insecure output handling, because the model's generated content was rendered as executable HTML without ever being sanitized.
B. Indirect prompt injection, because the attacker's ticket text caused the model to abandon its stated summarization instructions entirely.
C. A least-privilege violation, because the coding agent's account had permission to post directly to the shared wiki page.
D. A rate-limiting gap, because the ticket-summarization tool processed the malicious ticket without throttling how often it could be called.

---

**46.** `[task 7.1 · classifying indirect injection]` A team is documenting the difference between direct and indirect prompt injection for a security training session, using four candidate examples. Which TWO of these examples are indirect prompt injection specifically? (Select TWO)

A. A scraped customer review contains hidden text instructing the model to leak other customers' data, and the model reads it during a summarization task.
B. A user pastes a jailbreak prompt directly into the chat box, attempting to override the system prompt.
C. An email a support agent is asked to summarize contains an embedded instruction telling the model to forward internal notes to an external address.
D. A developer accidentally logs an API key in plaintext to a shared log stream.

---

**47.** `[task 7.2 · anomaly monitoring and circuit breaker]` An autonomous purchasing agent can call a `place_order` tool to buy inventory from suppliers, with no spending cap and no anomaly monitoring in place. A bug causes it to reorder the same item every few minutes for two days before anyone notices, running up a bill far beyond the normal budget. Which guardrail would most directly have caught this early?

A. Logging every `place_order` call to an audit trail that finance only reviews at the end of each quarter.
B. Filtering the agent's order confirmation messages for profanity before they are shown to the purchasing team.
C. Adding more few-shot examples of correct ordering behavior so the system prompt discourages duplicate purchase orders.
D. Real-time spend and anomaly monitoring that automatically halts the agent once unusual ordering activity is detected.

---

**48.** `[task 7.3 · shared credential across tenants]` A multi-tenant support platform bakes one long-lived API key into the container image deployed for every customer's agent instance, rather than issuing each tenant its own scoped credential. When one customer's container is compromised, the attacker extracts the key and uses it to reach every other tenant's data through the same integration. What key-management failure does this illustrate?

A. A pre-tool-use hook that failed to block the compromised container from calling any tools at all, at any point.
B. A single shared credential granting cross-tenant access, instead of issuing each tenant its own scoped, rotatable key.
C. A rate-limiting gap that let the attacker call the shared integration's API far more often than normal traffic.
D. An indirect prompt injection reaching the agent through text stored in the compromised container's configuration file.

---

**49.** `[task 8.1 · tool_result_content_array]` A `parse_invoice` tool call finishes, and the application needs to send back both the extracted line-item text and a small warning-icon image in the same `tool_result` block, referencing `tool_use_id` `toolu_77a`. Which structure lets that single `tool_result` block carry both pieces of content back to Claude?

A. Store the image as a separate `tool_use` block appended right after the `tool_result`.
B. JSON-stringify the text and the image bytes together into one plain `content` string field.
C. Set `content` to an array of content blocks, pairing one text block with one image block in the same result.
D. Send two consecutive `tool_result` blocks, each with its own fresh `tool_use_id`.

---

**50.** `[task 8.1 · tool definition required keys]` A CI lint step flags this tool definition as incomplete before it ever reaches the Messages API:

```python
tool_def = {
    "name": "cancel_subscription",
    "description": "Cancel a customer's active subscription.",
}
```

Which TWO statements about this specific definition are correct? (Select TWO)

A. It's missing `input_schema`, the JSON Schema describing the tool's expected arguments.
B. It's missing `tool_choice`, since every tool object must declare its own default choice mode.
C. `name` and `description` alone are sufficient; the lint step is a false positive.
D. Adding `input_schema` with at least a `type` and `properties` key would resolve the lint failure.

---

**51.** `[task 8.2 · custom_slash_command_ondemand]` A QA team wants to type `/run-smoke-tests` mid-conversation whenever they want the smoke suite executed against staging, rather than having the agent run those tests automatically after every code change regardless of relevance. Which customization mechanism fits this need?

A. A CLAUDE.md rule instructing the agent to run the smoke suite after every code change.
B. A custom slash command, defined as a file the agent runs on demand whenever a user types its name.
C. A project-specific subagent that launches automatically in its own isolated context window.
D. A system prompt override applied globally across every project the QA team opens.

---

**52.** `[task 8.2 · claude_md_standing_rules_license]` Maintainers are done reminding the agent, session after session, that new source files need a license header and that `vendor/` is off-limits for edits — they want both rules enforced automatically, never invoked by name. Where do standing rules like these belong?

A. In a slash command that maintainers must remember to type before every single file edit they make.
B. In a subagent definition invoked only when working on release branches specifically.
C. In the `input_schema` of a custom file-creation tool the agent calls.
D. In the project's CLAUDE.md, loaded each session.

---

**53.** `[task 8.3 · mcp_transport_sse]` A developer is building an MCP server that will be deployed on a shared remote host, reached over the network by several different clients at once, and needs to stream server-initiated messages back to each client over an existing HTTP connection. Which transport should this server implement?

A. SSE, since it streams responses back to each connected client over an HTTP connection.
B. stdio, since the client spawns the server and pipes messages over standard streams.
C. gRPC, since it offers strongly typed contracts suited to remote service calls.
D. WebSocket, since it keeps a persistent bidirectional connection open between remote peers.
