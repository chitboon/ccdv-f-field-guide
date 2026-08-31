# CCDV-F Domain Drill — Domain 2: Applications and Integration

36 items, one correct answer each. Untimed. Answer all 36 first, then grade
against the key in one pass — item by item, reading each rationale,
including the ones you got right. This is a scenario-based drill, not a
recall check: every stem carries a concrete situation you must reason about.
Suggested sittings: 1-9, 10-18, 19-27, 28-36 (four ~10-minute sessions), or
1-18 then 19-36 if you'd rather do two longer sessions.

---

**1.** `[task 2.1 · testable acceptance criteria]` A product manager asks for an agent that "summarizes customer emails accurately." Engineering builds it, but QA rejects the release because "accurately" was never defined — some summaries omit dollar amounts stakeholders consider critical, others correctly omit small talk. What should have prevented this rework?

A. Adding more few-shot examples to the existing prompt once QA had already flagged the release.
B. Switching to a model with a larger context window so more of each email gets read before summarizing.
C. Writing testable acceptance criteria for "accurate" before implementation began.
D. Lowering temperature so the summaries come out consistent across repeated runs on the same email.

---

**2.** `[task 2.1 · non-functional requirement trade-off]` A support-ticket triage agent must classify tickets within 500ms at p95, per a signed SLA with the frontend team, to avoid blocking the ticketing system's UI thread. During design review, an engineer proposes Claude Opus for its higher classification accuracy. What requirement does this proposal risk violating?

A. The non-functional latency requirement, since Opus trades speed for reasoning depth.
B. The functional requirement to classify tickets into the correct category.
C. The security requirement to redact PII before sending tickets to the API.
D. The requirement to support multilingual ticket text.

---

**3.** `[task 2.2 · life cycle: monitoring and maintenance]` A team has shipped an agent to production and is now tracking a rising rate of `tool_use` failures reported by real users, feeding those failures back into a backlog for the next sprint's prompt and tool-schema revisions. Which phase of the application life cycle does this activity belong to?

A. Requirements gathering, since the team is only now discovering what the agent's behavior actually needs to be.
B. Design, since the next sprint's tool-schema revisions haven't been drafted yet.
C. Testing, since the count of failures is what's driving the backlog entry.
D. Monitoring and maintenance — this is post-deployment feedback driving iteration.

---

**4.** `[task 2.3 · rate limit backoff]` A production integration receives a 429 response from the Messages API during a traffic spike. The response headers include `retry-after: 12`. The on-call engineer's retry logic instead waits a hardcoded 2 seconds before retrying, and the request fails again immediately with another 429. What is the fix?

A. Increase `max_tokens` so the whole request completes in a single call before any rate limit applies.
B. Read `retry-after` and wait that many seconds.
C. Switch to the async client, since asynchronous requests aren't subject to the same per-minute rate limits.
D. Set `temperature: 0`, since deterministic requests are less likely to trigger a rate limit.

---

**5.** `[task 2.3 · tool_choice selection]` An invoicing agent has three tools defined: `create_invoice`, `void_invoice`, and `send_reminder`. On a specific turn, the application needs Claude to definitely call one of these three tools — any of them is acceptable — but must not let Claude reply with plain text instead. Which `tool_choice` value achieves this?

A. `{"type": "any"}`
B. `{"type": "auto"}`
C. `{"type": "tool", "name": "create_invoice"}`
D. Omitting `tool_choice` and relying on the system prompt.

---

**6.** `[task 2.3 · Batch API lifecycle]` A data pipeline submits 40,000 document-classification requests through the Message Batches API at 9:00 AM. At 9:05 AM, the pipeline's status check calls the batch `ended` and attempts to download results from `results_url`, which returns a 404. What is the most likely cause?

A. The batch job failed permanently and must be resubmitted.
B. The Batch API does not support 40,000 requests in a single job.
C. `results_url` is only available once the batch has actually reached `ended`, not while it is still `in_progress` — the pipeline checked too early.
D. `results_url` requires a separate authentication token from the main API key.

---

**7.** `[task 2.3 · async streaming client]` A backend service needs to stream a Claude response to a browser over Server-Sent Events while continuing to serve other concurrent requests on the same event loop, without blocking on the full response. Which client/method combination fits this requirement?

A. `Anthropic().messages.create()` with `stream=False`, buffering the entire response in memory before forwarding any of it downstream.
B. `Anthropic().messages.stream(...)`, called from inside a dedicated synchronous thread pool worker spun up per incoming request.
C. `AsyncAnthropic()` with `stream.get_final_message()` invoked right after the request is sent.
D. `AsyncAnthropic()` with `async with client.messages.stream(...) as stream: async for text in stream.text_stream:`.

---

**8.** `[task 2.4 · idempotency]` A payment agent's `charge_customer` tool has no idempotency key. During a network blip, the client times out waiting for a response and retries the same tool call. The customer is charged twice. What software-engineering principle, applied to the tool's design, would have prevented this?

A. Increasing the client's request timeout so retries happen less often after a network blip.
B. Making the tool idempotent via a deduplicated request ID.
C. Reducing the agent's `max_tokens` so tool calls are generated and sent faster than the network can time out.
D. Adding a confirmation step where the user has to re-type the exact charge amount before it's sent.

---

**9.** `[task 2.4 · statelessness across instances]` A team builds a Claude-powered chatbot where each backend server instance keeps the full conversation history for logged-in users in that instance's local memory. When the load balancer routes a user's next message to a different server instance, the bot has no memory of the prior turns. What design flaw caused this?

A. The system prompt was too short to hold enough of the earlier conversation's context.
B. The team used the wrong Claude model for a genuinely multi-turn conversation.
C. Conversation state was kept in-process, breaking statelessness across instances.
D. `temperature` was set too high, so each instance's replies came out inconsistent with the others.

---

**10.** `[task 2.4 · centralized configuration]` A team hardcodes `model="claude-3-5-sonnet-20241022"` directly in 40 different call sites across their codebase. When they need to test a newer model snapshot, they must find and edit all 40 locations, and two are missed, leaving the app running two different model versions in production. What practice would have prevented this?

A. Centralizing the model identifier in one configuration value that all call sites reference.
B. Increasing `max_tokens` at each call site to compensate for model differences.
C. Adding more unit tests for each of the 40 call sites.
D. Switching from the model name string to the model's numeric parameter count.

---

**11.** `[task 2.4 · structured output reliability]` An application asks Claude to output a JSON object it will `json.loads()` directly. In production, Claude occasionally wraps its answer in explanatory prose before the JSON, or adds a trailing sentence after it, causing the parser to throw on inputs that were correct 99% of the time in testing. What is the most robust engineering fix?

A. Lower `temperature` to 0, on the theory that a more deterministic model wraps its JSON less often.
B. Increase `max_tokens`, so Claude has enough room to finish whatever sentence follows the JSON block.
C. Ask the user to resubmit their request whenever the JSON parser throws.
D. Force the output through tool use, pulling the payload from the `tool_use` block.

---

**12.** `[task 2.5 · RAG for freshness]` A legal-tech company wants Claude to answer questions using their firm's 2,000 internal case memos, which are updated weekly as new cases close. Memos must never be answered from stale information. Which application design best fits this constraint?

A. Fine-tune a custom model on the memo corpus and retrain it nightly to absorb the week's closed cases.
B. Retrieve the relevant memos per query and inject them (RAG).
C. Paste all 2,000 memos into a single system prompt attached to every request the firm sends.
D. Rely on Claude's training data, on the assumption it may already contain similar legal reasoning.

---

**13.** `[task 2.5 · orchestrator-workers pattern]` A research assistant application must, for a single user query, search three unrelated external databases in parallel, each requiring different tool calls and result formats, then synthesize the combined findings into one answer. A single linear prompt-response loop keeps producing incomplete answers because it only queries one database before responding. What architectural pattern addresses this?

A. An orchestrator agent that delegates one subtask per database and synthesizes the results.
B. Reduce `max_tokens` so the single agent is forced to move on to the next database sooner.
C. Increase the system prompt's instruction to "search all databases" in noticeably stronger language.
D. Switch to a smaller, faster model so more turns fit in the same latency budget.

---

**14.** `[task 2.5 · application-layer guardrail]` A travel-booking agent can call a `book_flight` tool that charges a customer's card immediately upon invocation. The team wants to keep the agent fully autonomous for search and itinerary tools, but require a human-in-the-loop confirmation specifically before any charge is made. Where should this constraint be enforced?

A. In the system prompt, instructing Claude to always ask before booking.
B. By removing `book_flight` from the tool list entirely.
C. In the application layer, gating the `book_flight` tool's execution behind a required user confirmation step, independent of what Claude decides.
D. By lowering `temperature` so Claude is less likely to book by mistake.

---

**15.** `[task 2.5 · stateless Messages API]` A developer new to the Messages API is confused that a second API call to Claude doesn't "remember" the first call unless the full message history is resent. They ask whether the API stores conversation state server-side. What is the correct application design implication?

A. The API stores the last 10 turns of every conversation automatically, keyed off the caller's API key.
B. The API is stateless; the calling application must resend the full message history on every call.
C. Conversation state is only stored when `stream: true` is set on the request.
D. State is preserved automatically as long as every single request happens to reuse the same `model` string.

---

**16.** `[task 2.5 · prompt caching for repeated context]` An application repeatedly sends the same 50-page product manual as part of every user query's system prompt, because answers must be grounded in that manual. Latency and per-request cost are both growing as usage scales. Which design change directly targets both, without changing what the manual actually contains?

A. Switch to a model with a smaller context window, forcing much more concise handling of the manual on every single request.
B. Increase `max_tokens` so full responses complete in fewer follow-up turns.
C. Compress the manual into a base64-encoded string before attaching it to each request.
D. Mark the manual's block with `cache_control: {"type": "ephemeral"}` so the repeated prefix is billed at a fraction of cost.

---

**17.** `[task 2.6 · secrets not hardcoded]` A team's staging and production environments use different Anthropic API keys and different rate-limit tiers, but a developer accidentally commits the production API key directly into the application's source code while testing a fix. What configuration-management practice would have prevented this exposure?

A. Rotating the production API key on a fixed monthly schedule regardless of whether it was ever exposed.
B. Renaming the variable that holds the key to something less recognizable to a casual reader.
C. Loading the key from an environment variable or secrets manager instead of hardcoding it.
D. Storing the key in a config file that gets committed to the repository but is marked read-only.

---

**18.** `[task 2.6 · feature-flagged rollout]` A team wants to roll out a new system-prompt version to 5% of production traffic before committing to it fully, and needs to roll back instantly if error rates spike, without redeploying code. What configuration approach supports this?

A. A feature flag or externalized prompt-version config that can route a percentage of traffic and be flipped back without a code deploy.
B. Hardcode the new prompt and deploy it to all traffic, monitoring closely.
C. Ask a subset of users to manually opt in via a support ticket.
D. Maintain two separate codebases, one per prompt version.

---

**19.** `[task 2.6 · one codebase, per-environment config]` A team runs the exact same Claude application code against three environments — dev, staging, production — differing only in model tier and rate-limit budget. A developer proposes maintaining three separate copies of the codebase, one per environment, to keep each one's settings visible at a glance. What is the better configuration-management approach?

A. Keep the three codebases separate, since each environment's settings are then easy to find without searching through config files.
B. Merge all three environments into one shared codebase with no per-environment distinction, since the application logic is identical everywhere.
C. Delete the staging environment entirely, since dev and production together already exercise the same code paths.
D. Keep one codebase and externalize the per-environment values into config, so behavior differs only by which config loads.

---

**20.** `[task 2.6 · single source of configuration truth]` An application reads its Claude model identifier, max token budget, and retry count from three separate places — a `.env` file, a hardcoded constant in `client.py`, and a command-line flag that silently overrides the other two whenever it's present. A new engineer edits the `.env` file and can't figure out why nothing changes. What configuration practice caused this confusion?

A. The `.env` file format itself is unreliable for a production application and should be replaced with a database-backed settings table instead.
B. Configuration is scattered across multiple sources with an undocumented precedence order, instead of one clear source of truth.
C. The retry count specifically should never be configurable, since it's an internal implementation detail.
D. The command-line flag should be removed so only environment variables can ever set these values.

---

**21.** `[task 2.1 · prioritized success criteria]` A team is asked to build an agent that "handles customer complaints well." Two engineers independently interpret this differently: one builds toward fastest possible resolution time, the other toward highest satisfaction survey scores, and the two goals trade off against each other in several concrete decisions during implementation. What was missing before implementation began?

A. A prioritized, explicit set of success criteria stating which outcome takes precedence when the two trade off.
B. A larger training dataset covering more categories of customer complaints than either engineer had considered.
C. A single engineer assigned ownership of the entire feature end to end, instead of splitting the work across two separate people.
D. A higher `max_tokens` setting so replies could cover both resolution speed and satisfaction at once.

---

**22.** `[task 2.1 · scoping data-access requirements]` A stakeholder wants an agent that can "access company data as needed." During implementation, the team discovers this could mean read-only access to a public wiki, or read-write access to a financial database, and the two options have wildly different security review timelines. Which requirements-gathering step should have caught this earlier?

A. Writing more detailed code comments describing what each tool call does internally.
B. Choosing a more capable model so it could infer the intended scope from context alone.
C. Explicitly scoping which specific data sources and access levels the requirement actually covers.
D. Deferring the security review entirely until after the agent has already been shipped into production.

---

**23.** `[task 2.2 · life cycle rigor scales with risk]` A team is deciding whether an internal agent needs a full requirements document or can go straight from a Slack conversation to a prototype, given that only three people will ever use it and it can be rebuilt in an afternoon if wrong. Which life-cycle principle applies?

A. Every application, regardless of scale or audience, requires the same formal requirements process to avoid scope creep.
B. Skipping requirements entirely is always safe as long as the code passes its unit tests before shipping.
C. Life-cycle rigor should scale with the exam blueprint's weighting for this domain, not the project's actual risk.
D. Life-cycle rigor should scale with the cost of being wrong and the audience size, not be applied uniformly everywhere.

---

**24.** `[task 2.3 · message role alternation]` A developer sends a Messages API request with two consecutive `user`-role messages and no `assistant` turn between them: `[{"role": "user", "content": "Hi"}, {"role": "user", "content": "Are you there?"}]`. What happens?

A. The API returns a 400 error, since same-role messages without an intervening turn violate the required alternation.
B. The API silently merges both user messages into a single turn before generating a response to the combined content.
C. The API responds twice, once to each user message, inside a single response payload.
D. The API treats the second message as a system-prompt override for that turn only.

---

**25.** `[task 2.3 · native PDF support]` A team building a document-analysis feature sends a 15-page contract as a `document` content block with `media_type: "application/pdf"`, expecting Claude to read both the text and any embedded diagrams. A teammate insists this requires first converting the PDF to plain text themselves. Who is right, and why?

A. The teammate is right; the Messages API only accepts plain text, never binary document formats.
B. The team is right; native PDF support lets Claude read the document directly, including visual layout, up to 100 pages.
C. Neither is right; PDFs must be split into individual page images before they can be sent at all.
D. The teammate is right, but only because this specific contract exceeds Claude's undocumented 5-page PDF processing limit.

---

**26.** `[task 2.3 · max_tokens with extended thinking]` An application sends a request with `thinking: {"type": "enabled", "budget_tokens": 2000}` but omits `max_tokens` entirely, expecting the API to infer a reasonable output cap from the thinking budget alone. What actually happens?

A. The API infers `max_tokens` automatically as double the thinking budget.
B. The request succeeds with unlimited output tokens, since enabling thinking mode disables the max_tokens cap entirely.
C. The request fails, since `max_tokens` is required regardless of whether extended thinking is enabled.
D. The API silently disables extended thinking and falls back to standard generation.

---

**27.** `[task 2.3 · Batch API for non-urgent volume]` A cost-conscious team wants to reduce spend on a nightly job that processes 200,000 support transcripts, none of which need a same-day answer, currently sent one at a time through the standard synchronous Messages API. What single change cuts cost the most for this workload?

A. Reduce `max_tokens` on every request by half, accepting shorter summaries for lower output cost.
B. Switch every request over to streaming mode, on the theory that streamed responses are billed at a lower per-token rate than non-streamed ones.
C. Increase the number of parallel synchronous requests so the job finishes faster during off-peak hours.
D. Submit the whole batch through the Message Batches API, which discounts asynchronous, non-urgent workloads.

---

**28.** `[task 2.4 · mocks alone don't catch contract drift]` A team's integration tests mock every Claude API call with a hardcoded canned response, so the suite runs in milliseconds and never touches the network. After a real API change alters the shape of tool-use responses, the mocked tests keep passing while production breaks immediately. What testing gap does this reveal?

A. The team should mock even more of the system than it already does, including the database layer, to isolate tests further from the outside world.
B. Mocks alone can't catch a real contract change; the suite also needs a test hitting the real API.
C. Integration tests should be removed entirely in favor of manual QA before every release.
D. The mocked responses should be randomized on every test run to catch more edge cases.

---

**29.** `[task 2.4 · redact sensitive fields before logging]` A Claude-powered feature logs every prompt and response verbatim to a shared application log for debugging, including customer names, account numbers, and full conversation text, with no redaction step anywhere in the pipeline. What software-engineering practice was skipped?

A. Redacting sensitive fields before anything is written to the shared log.
B. Increasing the log retention period so past conversations remain searchable for longer than the current policy allows.
C. Compressing the log files to reduce their storage footprint on disk.
D. Moving the logs from a shared server onto each engineer's local machine instead.

---

**30.** `[task 2.4 · defensive handling of optional input]` A tool's implementation raises a raw, unhandled `KeyError` whenever a caller omits an optional field the tool doesn't strictly require. The exception propagates all the way up and crashes the entire agent loop, ending the user's session, instead of just that one call failing gracefully. What's the underlying issue?

A. The tool should require every field to be mandatory so optional fields can never be omitted.
B. The agent loop's `max_tokens` should be increased so Claude has more room to avoid producing this particular input shape.
C. The tool lacks defensive handling for missing optional input, letting one bad call take down the whole session.
D. The tool should be rewritten in a different programming language with stricter typing.

---

**31.** `[task 2.4 · DRY across a shared codebase]` Two engineers each add a `format_currency` helper to a shared codebase, in two different files, with subtly different rounding — one rounds half up, the other rounds half to even. A tool calling one version returns totals that don't match a report generated with the other. What principle was violated?

A. Both functions should be renamed to make their different behavior more obvious to future readers.
B. The codebase should avoid handling currency formatting in code at all, and leave that decision entirely to the model on every call.
C. Each engineer should have written more unit tests for their own version of the function.
D. Don't Repeat Yourself — one shared implementation would have kept the rounding behavior consistent everywhere.

---

**32.** `[task 2.5 · preserve row-level access controls]` A customer-facing agent answers questions about a user's own order history, stored in a database with strict per-user row-level access controls. The team is deciding whether the agent's database-query tool should run with the calling user's own credentials or one shared service-account credential used for every user. Which design correctly preserves the database's access controls?

A. Running the tool with the calling user's own credentials, so the existing row-level rules apply unchanged.
B. Running the tool with a shared service-account credential, since it's simpler to configure once for every user.
C. Running the tool with no credentials at all, since Claude's tool-use layer already restricts access sufficiently.
D. Running the tool with an administrator credential, since it can always fetch every user's data if filtered later.

---

**33.** `[task 2.5 · sandboxed code execution]` A team is building a coding assistant that needs to run arbitrary user-submitted Python snippets as part of one of its tools, to check whether the code actually executes. What design choice is essential before this tool ever reaches production?

A. Trusting that the system prompt's instructions will prevent Claude from ever submitting genuinely malicious code.
B. Executing the submitted code inside an isolated, resource-limited sandbox, never directly on the host running the application.
C. Increasing `max_tokens` so the code has room to run to completion without truncation.
D. Requiring the code to pass a linter before execution, since linted code cannot be harmful.

---

**34.** `[task 2.5 · structural enforcement over prose instruction]` An application needs Claude to always respond in a fixed JSON shape so a downstream service can parse it without conditional logic, across every possible user query, including ones phrased in ways the model has never seen before. Which design most reliably guarantees this shape holds, request after request?

A. Repeating the desired JSON shape three times in the system prompt for emphasis.
B. Asking users to phrase their queries in a way that's easier for Claude to answer consistently.
C. Reviewing a sample of outputs manually before each release to catch shape drift early.
D. Defining the shape as a strict `input_schema` on a tool and forcing tool use, enforcing it structurally rather than requesting it in prose.

---

**35.** `[task 2.5 · grounded citations via retrieval]` A team building an internal knowledge-base assistant wants every answer to cite which specific document it came from, so a reader can verify the claim. Simply asking Claude in the system prompt to "always cite your sources" produces citations that are sometimes fabricated. What design change makes citations trustworthy instead of merely requested?

A. Lowering `temperature` to 0, since deterministic output is inherently more likely to be factually grounded.
B. Asking Claude twice and keeping whichever answer happens to include a citation.
C. Retrieving the actual source documents, passing their real identifiers into context, and requiring citations to reference one of those identifiers.
D. Increasing `max_tokens` so Claude has more room to write out a longer citation string.

---

**36.** `[task 2.6 · externalize the system prompt from code]` A team's production system prompt lives as a string literal inside `agent.py`. To test a small wording change, an engineer must edit the file, redeploy the whole service, and wait out the deploy pipeline, even though nothing else in the code changed. What configuration-management gap does this expose?

A. The system prompt should be externalized into its own versioned config artifact the application loads at startup, decoupling prompt changes from code deploys.
B. The engineer should keep multiple copies of `agent.py`, one per prompt variant, and swap which file gets deployed.
C. System prompts should never be changed after the initial release, to avoid needing this process at all.
D. The deploy pipeline should be made slower and more thorough specifically to compensate for frequent prompt edits.

---

**37.** `[task 2.3 · claude api mechanics: http 400 invalid role sequence]` A developer migrates an automated bot to the Messages API and submits the following payload:
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "user", "content": "Here is my order number: 10482"}
  ]
}
```
What error does the Messages API return, and why?

A. HTTP `429 RateLimitError` because submitting two user prompts within one second triggers account throttling.
B. HTTP `400 InvalidRequestError` because the Messages API strictly requires alternating `user` and `assistant` turns.
C. HTTP `529 OverloadedError` because the Anthropic routing gateway cannot resolve back-to-back user messages.
D. HTTP `200 OK` because the API automatically concatenates adjacent messages into a single conversational turn.

---

**38.** `[task 2.3 · claude api mechanics: http 400 parameter conflict]` A team configures Claude 3.7 Sonnet for code refactoring with the following API request:
```python
client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=2048,
    thinking={"type": "enabled", "budget_tokens": 4096},
    temperature=0.2,
    messages=[{"role": "user", "content": "Optimize this binary tree search..."}]
)
```
What error does the API return upon receiving this request?

A. HTTP `400 InvalidRequestError` because `budget_tokens` exceeds `max_tokens` and `temperature` is not 1.0.
B. HTTP `529 OverloadedError` because extended reasoning models reject low-temperature sampling during peak usage.
C. HTTP `429 RateLimitError` because reasoning tokens require an active enterprise quota allocation tier.
D. HTTP `200 OK` with `stop_reason: "thinking_complete"` because the API automatically clamps parameters to valid values.

---

**39.** `[task 2.3 · claude api mechanics: http 429 quota exhaustion]` A document parsing service submits 500 concurrent PDF extraction requests to Claude 3.5 Sonnet. The API responds with an HTTP status code accompanied by these response headers:
```http
HTTP/1.1 429 Too Many Requests
anthropic-ratelimit-tokens-remaining: 0
retry-after: 25
```
How should the client application handle this response?

A. Immediately resend the request to an alternate AWS Bedrock endpoint without waiting for rate limits.
B. Sleep for 25 seconds as dictated by the `retry-after` header before attempting a retry.
C. Treat the service as permanently down and alert the infrastructure on-call engineer for quota fixes.
D. Reduce `max_tokens` to zero and resend immediately to bypass the token rate limit accounting window.

---

**40.** `[task 2.3 · claude api mechanics: http 529 infrastructure capacity]` During a global peak traffic period, an enterprise integration receives the following JSON error body:
```json
{
  "type": "error",
  "error": {
    "type": "overloaded_error",
    "message": "Anthropic's API is temporarily overloaded"
  }
}
```
Inspection confirms the client organization has consumed only 10% of its monthly quota. What is the root cause and correct recovery strategy?

A. The client account's payment method failed, requiring an immediate billing update in the management console.
B. The client payload contained corrupt UTF-8 bytes, requiring payload serialization fixes in client code.
C. Anthropic's hosting infrastructure is saturated; retry using exponential backoff with jitter.
D. The API key was revoked by an administrator and must be regenerated from the enterprise security portal.

---

**41.** `[task 2.3 · claude api mechanics: http 400 tool_result schema mismatch]` Claude invokes an external database query tool with ID `toolu_01A99Z`. The client application executes the SQL query and responds with the following message payload:
```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "content": "{\"status\": \"active\", \"balance\": 450.00}"
    }
  ]
}
```
What error does the Messages API return, and what is the fix?

A. HTTP `429 RateLimitError`; the client must increase its tool execution rate limit allocation in the console.
B. HTTP `529 OverloadedError`; the client must retry after a random jitter delay interval across endpoints.
C. HTTP `400 InvalidRequestError` because `tool_use_id` is missing; the client must supply `"tool_use_id": "toolu_01A99Z"`.
D. HTTP `200 OK`; the API automatically matches the result to the most recent assistant tool call in history.


