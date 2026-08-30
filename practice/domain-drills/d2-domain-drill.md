# CCDV-F Domain Drill — Domain 2: Applications and Integration

18 items, one correct answer each. Untimed. Answer all 18 first, then grade
against the key in one pass — item by item, reading each rationale,
including the ones you got right. This is a scenario-based drill, not a
recall check: every stem carries a concrete situation you must reason about.

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
