# CCDV-F Mock Exam 2 — Blueprint-Exact (53 items)

Assembled from the same 131-item domain-drill pool as Mock 1, same
blueprint-proportional sampling (D1=8, D2=18, D3=2, D4=1, D5=9, D6=6, D7=4,
D8=5 = 53), but every item here is distinct from Mock 1 — zero stem overlap.
8 items (15.1%) are multi-response ("Select TWO"). Sealed key in
`mock-2-key.md`. Sit this one timed at 120 minutes as the closer rehearsal
to the real exam once Mock 1 is reviewed.

---

**1.** `[task 1.1 · context window trimming]` A research agent's loop has run 40 tool-call turns, and the growing transcript of full `tool_result` payloads is approaching the model's context window limit. The engineer wants the loop to keep running without losing its ability to follow the original instructions. What should the context-management strategy preserve?

A. Keep the system prompt and recent turns intact while summarizing or dropping older tool_result content to reclaim space.
B. Keep every full tool_result verbatim without ever trimming it, and instead shorten or simplify the system prompt itself once the loop has been running for many turns.
C. Discard the system prompt entirely after the very first turn, on the theory that the model no longer needs any instructions once its tools begin returning data.
D. Replace all prior turns with one hardcoded placeholder so transcript length never grows.

---

**2.** `[task 1.1 · tool_result is_error recovery]` An agent calls a `get_inventory` tool for SKU `X-771` and receives a `tool_result` block with `"is_error": true` and content `"warehouse service unreachable"`. The loop appends this tool_result to the conversation and calls the API again for the next turn. What should the model do with that turn?

A. Ignore the `is_error` flag entirely and treat the returned string as normal inventory data so the original plan continues unchanged.
B. Terminate the entire session immediately, since any `tool_result` carrying `is_error: true` means the conversation can no longer continue safely.
C. Read the error content and choose a recovery step: retry, switch tools, or report the failure to the user.
D. Resend the identical tool_use request in a loop until the `is_error` flag disappears, without changing any of its parameters.

---

**3.** `[task 1.2 · tool_choice forcing]` A form-filling agent has three tools available, and the developer wants the very first response to always call `extract_fields` rather than let Claude decide whether a tool is needed at all. Leaving `tool_choice` at its default sometimes produces a plain text reply instead of the desired call. What should the request specify instead?

A. A longer description written for every other tool, so the model avoids them by comparison rather than by direct instruction.
B. A `tool_choice` forcing `extract_fields` by name instead of leaving the model free to pick or skip tools.
C. A `stop_sequence` matching the tool's name, on the theory that stop sequences control which tool the model is permitted to call.
D. Removing the other two tools from the request permanently, so fewer tools force the intended one to be picked.

---

**4.** `[task 1.2 · multi-turn loop history]` A developer's agent loop sends a request, receives a `tool_use` block, executes the tool, and then starts an entirely new conversation containing only that single tool's result before asking the next question. The agent keeps repeating earlier steps because it never remembers what it already tried. What is the implementation error?

A. Each turn must append its own `tool_result` onto the growing conversation history, instead of restarting that history from just a single isolated result every time.
B. The loop should switch to the Batches API, since only batch requests can retain multi-turn memory.
C. The tool should be called twice per turn, since duplicate calls are what preserve memory across turns.
D. The system prompt must be resent as a `tool_result` block, since that is the only field read for memory.

---

**5.** `[task 1.2 · parallel tool_use blocks]` A trip-planning request returns a single Claude response containing two separate `tool_use` blocks: one for `check_flight_prices` and one for `check_hotel_prices`. The developer's loop executes only the first block and sends its `tool_result` back, dropping the second entirely. What must the loop do to handle this response correctly?

A. Reject the response outright, on the theory that a single Claude turn is only ever allowed to request one tool call at a time.
B. Merge both tool calls into one `tool_result` block, since the API accepts only a single result per turn.
C. Execute every `tool_use` block in the response and return a matching `tool_result` for each one before continuing.
D. Call only the first tool, since unused calls are dropped automatically by the runtime itself.

---

**6.** `[task 1.3 · routing pattern]` A support system's first Claude call reads an incoming ticket and outputs only a category label — "billing," "technical," or "account" — and a second stage then sends the ticket to whichever specialized subagent handles that category. Which pattern does this two-stage design implement?

A. Routing: an initial classification step directs the input to the specialized subagent suited to that category.
B. Evaluator-optimizer: the category label is treated as though it were a quality score that the second stage optimizes against.
C. Orchestrator-workers: the first call splits the ticket into independent pieces for parallel handling.
D. Prompt chaining: each stage's entire output text is appended verbatim as the next stage's whole input prompt.

---

**7.** `[task 1.3 · prompt chaining vs autonomous agent]` A document pipeline always runs three fixed Claude calls in the same order — extract entities, then translate them, then format a summary — with no step ever deciding to skip, repeat, or reorder based on what a prior step returned. Which category best describes this design, as distinct from an autonomous agent loop?

A. Orchestrator-workers: a coordinator dynamically delegating subtasks to workers chosen based on the document's actual content.
B. Evaluator-optimizer: a critic stage rejecting outputs and looping the extraction step until quality noticeably improves.
C. An autonomous agent loop: each step deciding on its own whether to repeat itself or stop early.
D. Prompt chaining: a predetermined sequence of steps rather than a loop that adapts its own next action.

---

**8.** `[task 1.3 · parallelization / sectioning pattern]` A content-moderation task sends the same flagged post to three independent Claude calls at once, each voting "allow" or "remove," and a simple majority-vote rule decides the final outcome rather than any single call's answer. Which pattern does running these calls simultaneously and combining their outputs represent?

A. Routing: a classifier reads the post and dispatches it to exactly one subagent that owns all moderation decisions.
B. Parallelization: independent calls run at once and their outputs get aggregated, here by simple vote.
C. Orchestrator-workers: a coordinator splits the single post into three separate sub-documents for each worker to handle.
D. Evaluator-optimizer: one call drafts a decision while the other two critique it across several looped revisions.

---

**9.** `[task 2.1 · prioritized success criteria]` A team is asked to build an agent that "handles customer complaints well." Two engineers independently interpret this differently: one builds toward fastest possible resolution time, the other toward highest satisfaction survey scores, and the two goals trade off against each other in several concrete decisions during implementation. What was missing before implementation began?

A. A prioritized, explicit set of success criteria stating which outcome takes precedence when the two trade off.
B. A larger training dataset covering more categories of customer complaints than either engineer had considered.
C. A single engineer assigned ownership of the entire feature end to end, instead of splitting the work across two separate people.
D. A higher `max_tokens` setting so replies could cover both resolution speed and satisfaction at once.

---

**10.** `[task 2.1 · scoping data-access requirements]` A stakeholder wants an agent that can "access company data as needed." During implementation, the team discovers this could mean read-only access to a public wiki, or read-write access to a financial database, and the two options have wildly different security review timelines. Which requirements-gathering step should have caught this earlier?

A. Writing more detailed code comments describing what each tool call does internally.
B. Choosing a more capable model so it could infer the intended scope from context alone.
C. Explicitly scoping which specific data sources and access levels the requirement actually covers.
D. Deferring the security review entirely until after the agent has already been shipped into production.

---

**11.** `[task 2.2 · life cycle rigor scales with risk]` A team is deciding whether an internal agent needs a full requirements document or can go straight from a Slack conversation to a prototype, given that only three people will ever use it and it can be rebuilt in an afternoon if wrong. Which life-cycle principle applies?

A. Every application, regardless of scale or audience, requires the same formal requirements process to avoid scope creep.
B. Skipping requirements entirely is always safe as long as the code passes its unit tests before shipping.
C. Life-cycle rigor should scale with the exam blueprint's weighting for this domain, not the project's actual risk.
D. Life-cycle rigor should scale with the cost of being wrong and the audience size, not be applied uniformly everywhere.

---

**12.** `[task 2.3 · retryable vs non-retryable exceptions]` A team building a retry wrapper around the Python SDK wants to distinguish exceptions worth retrying from exceptions that will fail the exact same way no matter how many times the request is resent. Which TWO exceptions belong in the "safe to retry with backoff" category? (Select TWO)

A. `anthropic.RateLimitError` — the request itself was valid; the account has temporarily exceeded a rate quota.
B. `anthropic.PermissionDeniedError` — the workspace or API tier lacks permission for this request, a request-shape problem.
C. `anthropic.InternalServerError` — a transient failure on Anthropic's infrastructure side, not the request's fault.
D. `anthropic.NotFoundError` — the referenced resource ID doesn't exist and won't start existing on retry.

---

**13.** `[task 2.3 · native PDF support]` A team building a document-analysis feature sends a 15-page contract as a `document` content block with `media_type: "application/pdf"`, expecting Claude to read both the text and any embedded diagrams. A teammate insists this requires first converting the PDF to plain text themselves. Who is right, and why?

A. The teammate is right; the Messages API only accepts plain text, never binary document formats.
B. The team is right; native PDF support lets Claude read the document directly, including visual layout, up to 100 pages.
C. Neither is right; PDFs must be split into individual page images before they can be sent at all.
D. The teammate is right, but only because this specific contract exceeds Claude's undocumented 5-page PDF processing limit.

---

**14.** `[task 2.3 · max_tokens with extended thinking]` An application sends a request with `thinking: {"type": "enabled", "budget_tokens": 2000}` but omits `max_tokens` entirely, expecting the API to infer a reasonable output cap from the thinking budget alone. What actually happens?

A. The API infers `max_tokens` automatically as double the thinking budget.
B. The request succeeds with unlimited output tokens, since enabling thinking mode disables the max_tokens cap entirely.
C. The request fails, since `max_tokens` is required regardless of whether extended thinking is enabled.
D. The API silently disables extended thinking and falls back to standard generation.

---

**15.** `[task 2.3 · Batch API for non-urgent volume]` A cost-conscious team wants to reduce spend on a nightly job that processes 200,000 support transcripts, none of which need a same-day answer, currently sent one at a time through the standard synchronous Messages API. What single change cuts cost the most for this workload?

A. Reduce `max_tokens` on every request by half, accepting shorter summaries for lower output cost.
B. Switch every request over to streaming mode, on the theory that streamed responses are billed at a lower per-token rate than non-streamed ones.
C. Increase the number of parallel synchronous requests so the job finishes faster during off-peak hours.
D. Submit the whole batch through the Message Batches API, which discounts asynchronous, non-urgent workloads.

---

**16.** `[task 2.4 · mocks alone don't catch contract drift]` A team's integration tests mock every Claude API call with a hardcoded canned response, so the suite runs in milliseconds and never touches the network. After a real API change alters the shape of tool-use responses, the mocked tests keep passing while production breaks immediately. What testing gap does this reveal?

A. The team should mock even more of the system than it already does, including the database layer, to isolate tests further from the outside world.
B. Mocks alone can't catch a real contract change; the suite also needs a test hitting the real API.
C. Integration tests should be removed entirely in favor of manual QA before every release.
D. The mocked responses should be randomized on every test run to catch more edge cases.

---

**17.** `[task 2.4 · redact sensitive fields before logging]` A Claude-powered feature logs every prompt and response verbatim to a shared application log for debugging, including customer names, account numbers, and full conversation text, with no redaction step anywhere in the pipeline. What software-engineering practice was skipped?

A. Redacting sensitive fields before anything is written to the shared log.
B. Increasing the log retention period so past conversations remain searchable for longer than the current policy allows.
C. Compressing the log files to reduce their storage footprint on disk.
D. Moving the logs from a shared server onto each engineer's local machine instead.

---

**18.** `[task 2.4 · defensive handling of optional input]` A tool's implementation raises a raw, unhandled `KeyError` whenever a caller omits an optional field the tool doesn't strictly require. The exception propagates all the way up and crashes the entire agent loop, ending the user's session, instead of just that one call failing gracefully. What's the underlying issue?

A. The tool should require every field to be mandatory so optional fields can never be omitted.
B. The agent loop's `max_tokens` should be increased so Claude has more room to avoid producing this particular input shape.
C. The tool lacks defensive handling for missing optional input, letting one bad call take down the whole session.
D. The tool should be rewritten in a different programming language with stricter typing.

---

**19.** `[task 2.4 · DRY across a shared codebase]` Two engineers each add a `format_currency` helper to a shared codebase, in two different files, with subtly different rounding — one rounds half up, the other rounds half to even. A tool calling one version returns totals that don't match a report generated with the other. What principle was violated?

A. Both functions should be renamed to make their different behavior more obvious to future readers.
B. The codebase should avoid handling currency formatting in code at all, and leave that decision entirely to the model on every call.
C. Each engineer should have written more unit tests for their own version of the function.
D. Don't Repeat Yourself — one shared implementation would have kept the rounding behavior consistent everywhere.

---

**20.** `[task 2.5 · preserve row-level access controls]` A customer-facing agent answers questions about a user's own order history, stored in a database with strict per-user row-level access controls. The team is deciding whether the agent's database-query tool should run with the calling user's own credentials or one shared service-account credential used for every user. Which design correctly preserves the database's access controls?

A. Running the tool with the calling user's own credentials, so the existing row-level rules apply unchanged.
B. Running the tool with a shared service-account credential, since it's simpler to configure once for every user.
C. Running the tool with no credentials at all, since Claude's tool-use layer already restricts access sufficiently.
D. Running the tool with an administrator credential, since it can always fetch every user's data if filtered later.

---

**21.** `[task 2.5 · sandboxed code execution]` A team is building a coding assistant that needs to run arbitrary user-submitted Python snippets as part of one of its tools, to check whether the code actually executes. What design choice is essential before this tool ever reaches production?

A. Trusting that the system prompt's instructions will prevent Claude from ever submitting genuinely malicious code.
B. Executing the submitted code inside an isolated, resource-limited sandbox, never directly on the host running the application.
C. Increasing `max_tokens` so the code has room to run to completion without truncation.
D. Requiring the code to pass a linter before execution, since linted code cannot be harmful.

---

**22.** `[task 2.5 · structural enforcement over prose instruction]` An application needs Claude to always respond in a fixed JSON shape so a downstream service can parse it without conditional logic, across every possible user query, including ones phrased in ways the model has never seen before. Which design most reliably guarantees this shape holds, request after request?

A. Repeating the desired JSON shape three times in the system prompt for emphasis.
B. Asking users to phrase their queries in a way that's easier for Claude to answer consistently.
C. Reviewing a sample of outputs manually before each release to catch shape drift early.
D. Defining the shape as a strict `input_schema` on a tool and forcing tool use, enforcing it structurally rather than requesting it in prose.

---

**23.** `[task 2.5 · grounded citations via retrieval]` A team building an internal knowledge-base assistant wants every answer to cite which specific document it came from, so a reader can verify the claim. Simply asking Claude in the system prompt to "always cite your sources" produces citations that are sometimes fabricated. What design change makes citations trustworthy instead of merely requested?

A. Lowering `temperature` to 0, since deterministic output is inherently more likely to be factually grounded.
B. Asking Claude twice and keeping whichever answer happens to include a citation.
C. Retrieving the actual source documents, passing their real identifiers into context, and requiring citations to reference one of those identifiers.
D. Increasing `max_tokens` so Claude has more room to write out a longer citation string.

---

**24.** `[task 2.5 · graceful degradation when the API is unavailable]` A retailer's product-search feature calls the Claude API to generate natural-language answers about inventory. During a regional Anthropic outage, every request fails, and the storefront's search bar goes completely blank with no results at all, even though the underlying inventory database is still fully operational. What design choice would have avoided a total feature outage?

A. Retrying the failed API call ten times in rapid, immediate succession before ever giving up on a single search.
B. Caching every possible natural-language answer in advance so no live API call is ever needed at all.
C. Increasing `max_tokens` on search requests so responses complete before any timeout is reached.
D. Falling back to a simpler, non-Claude search path when the API is unavailable.

---

**25.** `[task 2.6 · one codebase, per-environment config]` A team runs the exact same Claude application code against three environments — dev, staging, production — differing only in model tier and rate-limit budget. A developer proposes maintaining three separate copies of the codebase, one per environment, to keep each one's settings visible at a glance. What is the better configuration-management approach?

A. Keep the three codebases separate, since each environment's settings are then easy to find without searching through config files.
B. Merge all three environments into one shared codebase with no per-environment distinction, since the application logic is identical everywhere.
C. Delete the staging environment entirely, since dev and production together already exercise the same code paths.
D. Keep one codebase and externalize the per-environment values into config, so behavior differs only by which config loads.

---

**26.** `[task 2.6 · secrets handling guidelines]` A platform team is writing internal guidelines for how services should handle their Anthropic API keys across dev, staging, and production. Which TWO of the following guidelines should make it into the document? (Select TWO)

A. Each environment gets its own key, injected via the deployment platform's secret store, never checked into version control.
B. Rotate a key immediately if it's ever found in a commit history, git log, or log aggregator.
C. Reuse one shared production key across all environments to simplify credential management.
D. Store the key as a plain build-time constant baked into the compiled application binary.

---

**27.** `[task 3.1 · settings and memory hierarchy]` A team lead is writing an onboarding note about how Claude Code's settings and memory files actually combine, and wants only accurate statements included. Which TWO of the following are correct? (Select TWO)

A. Project-level settings can override user-level settings, but neither can override an enterprise-managed policy.
B. Memory from a root `CLAUDE.md` and a nested package's `CLAUDE.md` combine rather than one silently replacing the other.
C. Settings conflicts are resolved by file modification timestamp, with the newest edit always winning.
D. A subdirectory `CLAUDE.md` is ignored entirely unless explicitly referenced by path in the prompt.

---

**28.** `[task 3.1 · hook lifecycle event]` A team wants every `Bash` tool call in a Claude Code session to first run through an internal command-allowlist script, blocking the call entirely if that script exits non-zero, before Claude's requested command ever executes. Which mechanism fits this requirement?

A. A `PreToolUse` hook that runs the script first and blocks the call on a non-zero exit.
B. A slash command that engineers run manually before asking Claude to execute any shell command.
C. A line in `CLAUDE.md` instructing Claude to always ask permission before running Bash commands.
D. A `PostToolUse` hook that logs the Bash command's output for later audit only after the command has already run.

---

**29.** `[task 4.1 · golden eval dataset construction]` A team building a contract-clause extractor has only tested it against contracts from one client, so every extraction the demo shows looks correct. Before wider rollout, an engineer proposes assembling 50 contracts with known-correct extracted fields, including three intentionally malformed contracts missing a signature block. What is this engineer building?

A. A golden eval dataset, since it pairs known-correct answers with edge cases the extractor must also handle correctly.
B. A load-testing harness, since 50 documents is enough volume to estimate the extractor's throughput under concurrent requests.
C. A prompt-injection test suite, since malformed contracts are the standard way to probe for injected instructions.
D. A fine-tuning corpus, since labeled examples like these are what gets fed into a supervised training run.

---

**30.** `[task 5.1 · cache TTL reset on hit]` A cached 1,024-token system prompt receives a cache hit at the 4-minute mark after being written, and the next request then arrives 4 more minutes after that hit. Does this second request still find the segment cached?

A. No, because the five-minute TTL is fixed from the original write and never resets on subsequent hits.
B. Yes, because each cache hit resets the five-minute TTL, and only four minutes had actually elapsed since the last hit occurred.
C. Yes, because prompt caching TTLs are measured in wall-clock hours, not minutes, regardless of hit pattern.
D. No, because a cache miss at any point permanently invalidates the segment until it is rewritten from scratch.

---

**31.** `[task 5.1 · extended thinking dual constraint]` This request fails validation before any generation begins:

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

**32.** `[task 5.1 · extended thinking temperature constraint]` A request enables extended thinking with `budget_tokens: 4000` while also setting `temperature: 0.2` to keep the final answer's wording consistent across retries. The call fails validation. What must change to keep extended thinking enabled on this request?

A. `budget_tokens` must be lowered below 1,024 whenever a non-default `temperature` is supplied.
B. `top_p` must be supplied alongside `temperature` any time extended thinking is requested.
C. `temperature` must be set to 1.0 or omitted entirely whenever extended thinking is enabled.
D. `max_tokens` must be removed from the request entirely so thinking can set its own output ceiling.

---

**33.** `[task 5.2 · context window as shared token budget]` A 190,000-token conversation history, together with a 4,000-token system prompt, is sent to a 200,000-token context window model, leaving only 6,000 tokens of headroom. The next user turn adds 3,000 tokens, and the developer still expects a 5,000-token completion to come back in full. What happens?

A. The request succeeds normally, because completions are generated in a token space entirely separate from the input context window.
B. The system prompt is automatically evicted first so that the full 5,000-token completion can still be produced without error.
C. The completion gets truncated or the request is rejected, since input and output share one finite context-window budget.
D. Prompt caching automatically compresses the history, since cached segments no longer count at all against the context window.

---

**34.** `[task 5.2 · tokenization limits on character-level tasks]` Asked to count how many times the letter "r" appears in a long word, Claude sometimes gives an incorrect count even though the task looks trivial to a person reading letter by letter. Which fact about how the model processes text best explains this class of error?

A. The model operates over subword tokens rather than individual characters, obscuring letter-level detail it can't directly see.
B. The model's context window is too small to hold a single long word, so part of it gets truncated before counting even begins.
C. Temperature above 0 randomly drops individual letters from the input text before the count is ever performed at all.
D. Extended thinking is strictly required for any character-counting task, and it was left disabled in this particular case.

---

**35.** `[task 5.2 · max_tokens does not govern quality]` A developer doubles `max_tokens` from 512 to 1,024 on a customer-summary endpoint, hoping the higher ceiling will make the summaries more accurate and less prone to factual slips. The output quality is unchanged afterward. What does this reveal about what `max_tokens` actually controls?

A. `max_tokens` was set too high, and lowering it back toward 512 would have improved factual accuracy.
B. `max_tokens` only caps how many tokens the completion may contain; it doesn't influence the model's reasoning or accuracy.
C. `max_tokens` controls the size of the context window available for reading the input, not just the output.
D. `max_tokens` and `temperature` must always be changed together, so accuracy regressed only because `temperature` stayed fixed.

---

**36.** `[task 5.3 · Sonnet as balanced tier]` A product team is drafting internal weekly reports that require decent synthesis of multiple data sources but not the deepest possible reasoning, and they need response times fast enough for an interactive dashboard while keeping per-call cost well below Opus pricing. Which tier represents the intended middle-ground tradeoff for this workload?

A. Claude 3.5 Haiku, since its speed advantage makes it the correct default whenever latency matters at all.
B. Claude Opus, since any workload involving synthesis of multiple data sources requires the single most capable tier available today.
C. Claude Sonnet, since it is positioned as the balanced tier between Haiku's speed and Opus's reasoning depth and cost.
D. Any tier works identically here, since model choice only affects cost and never affects latency or reasoning quality.

---

**37.** `[task 5.3 · extended thinking as a selection tradeoff]` A team debates whether to enable extended thinking with an 8,000-token `budget_tokens` on a math-heavy tutoring endpoint that already runs on Claude Opus, knowing the thinking tokens are billed as output and add to response latency. What tradeoff does this decision actually represent?

A. Switching the underlying model tier from Opus to Haiku, since extended thinking is only compatible with the fastest tier.
B. Spending additional tokens and latency on visible step-by-step reasoning in exchange for better accuracy on multi-step problems.
C. Reducing the request's total cost, since thinking tokens are supposedly billed at a discounted rate compared to normal output tokens.
D. Guaranteeing a correct final answer, since extended thinking adds a deterministic verification pass after generation.

---

**38.** `[task 5.4 · Batch API accuracy check]` An engineer is writing documentation explaining when and how to use the Message Batches API correctly. Which TWO statements belong in that documentation as accurate? (Select TWO)

A. The Batch API is intended for non-urgent, asynchronous workloads, not requests needing an immediate response.
B. Attempting to download results while the batch is still `in_progress` returns a 404, not partial results.
C. Every batch request must set `max_tokens` to at least 4,096 tokens regardless of the task.
D. Batches API responses stream back to the client in real time via Server-Sent Events, like the standard API.

---

**39.** `[task 6.1 · chain-of-thought for multi-step reasoning]` A prompt asks Claude to compute a multi-step loan eligibility decision (income ratio, credit history weight, and collateral value combined into one verdict) and return only the final approve/deny word. Reviewers notice the verdicts are inconsistent across near-identical applicants. What change is likely to improve reasoning consistency?

A. Instruct Claude to articulate intermediate reasoning inside `<thinking>` tags before outputting the verdict.
B. Instruct Claude to skip explanation entirely and output a single bare verdict token to minimize cost.
C. Set `max_tokens: 1` on the request so the model is physically constrained to emitting only one word.
D. Combine the financial metrics into a pre-computed external formula passed directly in the user prompt.

---

**40.** `[task 6.1 · role instructions vs. worked demonstration]` A drafting assistant's system prompt states "write concise, formal replies" but the outputs keep coming back casual and wordy despite the instruction being restated in every session. What is the most likely gap in the current approach?

A. The system prompt is treated as the wrong location for style guidance, which is assumed to belong only in the user turn.
B. The prompt describes the style abstractly but never shows a worked example of concise, formal writing to match.
C. The word "concise" is being interpreted overly literally, as a request for replies of a single short sentence.
D. The session has grown long enough to exceed the context window, pushing the original instruction out of view.

---

**41.** `[task 6.1 · negative instruction reframed positively]` A prompt tells Claude "do not use bullet points" for a narrative summary feature, yet outputs keep drifting back into bulleted lists whenever the input material itself contains lists. What phrasing adjustment is most likely to reduce this drift?

A. Restate the negative instruction in stronger language, written in all capital letters at the very end.
B. Remove the negative formatting rule entirely and rely on Claude's default paragraph formatting.
C. Replace the prohibition with a positive instruction describing the desired flowing prose paragraphs.
D. Move the negative constraint out of the system prompt and append it to every individual user turn.

---

**42.** `[task 6.2 · multimodal image content block]` An engineer needs Claude to inspect a screenshot the user just uploaded as a PNG file and describe any visible layout bugs. The image bytes are already base64-encoded in the client. How should this image be included in the request?

A. As a plain-text content block containing the base64 string, prefixed with a short note that it represents image data.
B. As a system prompt field named `image_data`, set once at the start of the conversation and never touched again.
C. As a content block with `type: "image"` and a `source` object carrying `type: "base64"`, the media type, and data.
D. As a `tool_result` block referencing a `tool_use_id` from an earlier turn, with the base64 string as its content.

---

**43.** `[task 6.2 · reference material inside XML with instruction after]` A research assistant prompt pastes three long PDFs' extracted text directly above the user's question, with no tags marking where the documents end and the question begins. Claude sometimes answers a question that was actually a sentence lifted from inside one of the documents. What structural fix addresses this?

A. Delete two of the three PDF documents entirely so fewer background sentences can cause prompt confusion.
B. Relocate the user's question into the system prompt string rather than inside the user message.
C. Format the user's question in all capital letters so the model prioritizes it visually across turns.
D. Wrap each source in `<document>` tags and place the user question after the closing tags.

---

**44.** `[task 6.3 · why tool use beats string matching]` A team debating whether to keep their keyword-matching output parser or switch to tool-based extraction lists out the claimed benefits of switching. Which TWO claims are actually true benefits of the tool-use approach? (Select TWO)

A. Downstream code reads a structured field directly, instead of searching free text for a substring that might appear by coincidence.
B. Tool-based extraction automatically improves the accuracy of the underlying decision being extracted.
C. It removes false positives caused by Claude's prose explanation happening to mention a different category's keyword.
D. It guarantees the tool call will never be duplicated across parallel turns.

---

**45.** `[task 7.1 · classifying indirect injection]` A team is documenting the difference between direct and indirect prompt injection for a security training session, using four candidate examples. Which TWO of these examples are indirect prompt injection specifically? (Select TWO)

A. A scraped customer review contains hidden text instructing the model to leak other customers' data, and the model reads it during a summarization task.
B. A user pastes a jailbreak prompt directly into the chat box, attempting to override the system prompt.
C. An email a support agent is asked to summarize contains an embedded instruction telling the model to forward internal notes to an external address.
D. A developer accidentally logs an API key in plaintext to a shared log stream.

---

**46.** `[task 7.1 · secrets in logs and commits]` A developer debugging a failing API integration adds `print(f"Using key: {api_key}")` so the key's value shows up in the deployment logs, then commits the change alongside the fix. What is the security problem with this approach?

A. The commit message doesn't explain why the debug line was added, making the change hard to audit later.
B. `print` statements are slower than a proper logging framework, which will degrade the integration's response latency.
C. Logging and committing the raw secret exposes it to anyone with log or repository access, defeating key management.
D. The `api_key` variable name is not descriptive enough for other engineers to understand its purpose.

---

**47.** `[task 7.2 · rate limiting and content filtering]` A public-facing chatbot built on the Messages API has no cap on requests per user and no output-content screening; within an hour a single anonymous user sends thousands of requests generating disallowed content, running up a large API bill in the process. Which guardrails would address this deployment as a pair?

A. Per-user rate limiting to cap request volume, paired with output content filtering to catch policy-violating responses.
B. A larger context window and a higher `max_tokens` limit so each response is more complete.
C. Switching to a cheaper model and caching the system prompt to reduce per-request cost.
D. Adding more few-shot examples to the prompt so refusals become more consistent across requests.

---

**48.** `[task 7.3 · identity-scoped data access]` A support agent authenticates as a specific logged-in customer, then calls a `query_orders` tool that runs under a single database credential with read access to every customer's order history. The tool passes along whatever `customer_id` the model puts in its query, with no check against the logged-in session. What risk does this create?

A. The agent could be prompted to supply another customer's `customer_id` and retrieve that person's order data.
B. The broad database credential will eventually hit its connection pool limit under normal traffic.
C. The model's response latency will increase because the `query_orders` tool has too many columns to scan.
D. The support agent will be unable to answer questions about the logged-in customer's own orders.

---

**49.** `[task 8.1 · tool definition required keys]` A CI lint step flags this tool definition as incomplete before it ever reaches the Messages API:

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

**50.** `[task 8.1 · parallel tool_result batching]` On one turn, Claude's assistant message contains two `tool_use` blocks: one calling `check_inventory`, one calling `get_shipping_rate`. The application runs both, then replies with the `check_inventory` result in one `user` message and, immediately after, the `get_shipping_rate` result in a second, separate `user` message. What is wrong with this sequence?

A. Both `tool_result` blocks belong in one `user` message, not split into two.
B. The two blocks must carry an identical `tool_use_id` value to match the same turn.
C. The `check_inventory` result must be sent before `get_shipping_rate` is ever invoked.
D. Parallel tool calls require a wrapping `system`-role message around both results.

---

**51.** `[task 8.2 · CLAUDE.md standing behavior]` A repository's engineers are tired of reminding the agent every session that commits must reference a Jira ticket and that `git push --force` is never allowed on `main`. They want these rules to apply automatically in every session, without being invoked by name each time. Where should these standing rules live?

A. In a slash command that engineers must type before every single commit.
B. In the project's CLAUDE.md file, loaded automatically each session start.
C. In a subagent definition invoked only when working on release branches.
D. In the `input_schema` of a custom commit-validation tool the agent calls.

---

**52.** `[task 8.2 · combining customization mechanisms]` A team wants `/incident-review` typed by name mid-conversation, and once triggered, wants the review to run in its own context window with access to only a read-only log-search tool, so the main conversation's history stays uncluttered. Which single approach satisfies both the on-demand trigger and the isolated, tool-restricted execution?

A. A CLAUDE.md rule alone, since standing instructions can restrict tool access at session start.
B. A slash command alone, since typing its name already isolates the conversation's context.
C. A slash command that invokes a dedicated subagent, pairing on-demand triggering with isolation.
D. A subagent alone, since subagents already trigger by name without needing a slash command.

---

**53.** `[task 8.3 · MCP transport choice]` A developer is building an MCP server meant to run as a local child process on the same machine as the client, communicating over standard input and output with no network exposure at all. Which transport should this server implement?

A. SSE, since it streams responses back to the client over an HTTP connection.
B. gRPC, since it offers strongly typed contracts suited to local process communication.
C. WebSocket, since it keeps a persistent bidirectional connection open for local use.
D. stdio, since the client spawns the server and pipes messages over standard streams.
