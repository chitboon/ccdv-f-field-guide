# CCDV-F Gap-Coverage Drill — 17 items

**Purpose:** every item here tests a named technique from §6 of the official
exam guide that has **zero coverage** in the 245-item practice bank, or a fact
the bank teaches in a form that current models now reject with a 400.

**Authored:** 2026-09-03, by hand, against the current Claude API surface.
Not sampled from the drilled pool — no item here restates one you have sat.

**How to sit it:** untimed or ~40 min, one pass, no peeking. Key is sealed in
`gap-coverage-drill-key.md`. Items 4, 6 and 13 are multi-response and need
both letters to count.

**Register note:** distractors here are deliberately plausible. The existing
bank leaks answers through extreme language (absolutes appear in 27.7% of its
distractors vs 7.3% of its correct answers, a 3.8x tell). Nothing in this set
is eliminable that way — if you catch yourself hunting for the "measured
sounding" option, that reflex will not help you tomorrow.

**Coverage map:** 1.2 (x2), 1.3, 2.5, 5.1 (x3), 5.3, 5.4, 6.1, 7.4 (x2),
8.1 (x2), 8.2 (x2), 8.3.

---

**1.** `[task 1.2 · harness vs deployment when replacing a hand-written loop]` A team runs a working `while stop_reason == "tool_use"` loop over three tools they wrote themselves, deployed on their own ECS cluster. They want to stop maintaining the loop code, keep the same tool functions, and keep execution on their own infrastructure. Which surface fits with the least change?

A. The Claude Agent SDK, which supplies the full agent loop along with its own built-in file, bash, and search tools.
B. Managed Agents, which persists a versioned agent config and provisions a per-session container for tool execution.
C. The SDK tool runner (`client.beta.messages.tool_runner`), which loops over the tools they already define.
D. The same manual loop with `disable_parallel_tool_use` set, so the three tools resolve one per turn in a fixed order.

---

**2.** `[task 1.2 · Managed Agents object model]` A regulated insurer wants Anthropic to run the agent loop and host the workspace where bash and file operations execute, with the config version-pinned so any session runs a known revision. Which statement describes how that is set up?

A. Create the Agent once and reference its ID from every session; `model`, `system`, and `tools` live on the agent, not the session.
B. Create an Agent per session so each run carries its own model and tool list, then archive the agent when the run ends.
C. Skip the agent and pass `model`, `system`, and `tools` on `sessions.create`, since the session is the object that gets pinned.
D. Register the config through the SDK tool runner, which stores it server-side and hands back a session handle to reuse.

---

**3.** `[task 1.3 · what an agent framework does and does not change]` A team is weighing an agentic abstraction framework (Strands, LangGraph, PydanticAI) against orchestrating their own calls for a multi-step research agent. What is the honest accounting of what adopting one changes?

A. It replaces the Messages API with the framework's own inference endpoint, so tool-use wire formats no longer apply.
B. It supplies graph, state, and retry abstractions over the same Messages API, and leaves context growth still yours to manage.
C. It removes the need for context management, since frameworks compact history on the developer's behalf by default.
D. It converts the agent into a workflow, because a framework's declared graph is by definition not model-directed.

---

**4.** `[task 5.1 · adaptive thinking replaces a fixed budget]` A service pinned to `claude-opus-5` sends `thinking: {"type": "enabled", "budget_tokens": 8000}` after being migrated from an older model, and every request now fails before a single token is generated. Which TWO statements about this request are correct? (Select TWO)

A. `budget_tokens` is not part of this model's request surface, and the call is rejected with a 400.
B. Raising `max_tokens` above `budget_tokens` resolves it, since the budget must fit inside the response ceiling.
C. Sending `thinking: {"type": "adaptive"}` is the current form, letting the model decide how much to think per turn.
D. Adding `temperature: 1.0` next to the thinking block restores the behaviour the older model had.

---

**5.** `[task 5.1 · the request-level cost dial]` A coding agent on `claude-opus-5` produces good output but spends more tokens per task than its budget allows. The team wants one request-level dial to try before moving to a cheaper model. Which one, and what does it actually govern?

A. `max_tokens`, lowered to 4096 — the ceiling the model paces itself against for the whole task.
B. `speed: "fast"`, which cuts spend by completing the same work in fewer output tokens.
C. A `task_budget` of 20,000 tokens, a platform-enforced hard cap on what the loop may consume.
D. `output_config.effort`, stepped to `medium` — it trades thinking depth against token spend.

---

**6.** `[task 5.1 · fast mode constraints]` A latency-sensitive endpoint on `claude-opus-5` needs a higher output-token rate, and the team has signed off on premium pricing. Which TWO statements about enabling fast mode are correct? (Select TWO)

A. Per-token price is unchanged; the saving comes from shorter wall-clock time per request.
B. It requires the beta messages endpoint plus `speed: "fast"` sent as a top-level request parameter.
C. It is not available through the Batch API, on Priority Tier, or on third-party cloud platforms.
D. Fast and standard requests draw on one shared rate limit, so no separate quota planning is needed.

---

**7.** `[task 5.3 · a technique that a model release removed]` A prompt that reliably returned bare JSON on an older model now returns a 400 on `claude-opus-5`. The request's final entry is `{"role": "assistant", "content": "{"}`. What changed, and what replaces the technique?

A. Thinking blocks now precede the answer, so the parser must read `content[1]` rather than `content[0]`.
B. Assistant prefill is rejected on current models; constrain the shape with `output_config.format`.
C. `stop_sequences` must now carry the closing brace for the model to terminate the object cleanly.
D. The schema has to move into the top-level `system` field, the only instruction channel these models read.

---

**8.** `[task 5.4 · why a cache never reads]` A 30,000-token system prompt carries one `cache_control` breakpoint, but `usage.cache_read_input_tokens` stays at 0 across repeated calls. The block ends with a rendered line reading `Generated at 2026-09-03T11:42:07Z`. Which change restores hits?

A. Add three further breakpoints, so that at least one of the four prefixes still matches between calls.
B. Shorten the block below the model's minimum cacheable prefix, which moves it to a cheaper matching path.
C. Move the timestamp after the last breakpoint, leaving the cached prefix byte-identical on every call.
D. Render the timestamp to the nearest minute, so calls landing in the same minute share a prefix.

---

**9.** `[task 6.1 · clearing tool output vs summarizing history]` A long-running agent's history is dominated by large file-read tool results. The team wants those specific results gone from what the model sees, while the original task brief and the recent turns stay intact. Which mechanism fits, and how does it differ from the alternative?

A. Context editing's `clear_tool_uses` removes old tool results outright; compaction summarizes earlier context.
B. Compaction removes the tool results once its token threshold trips; context editing is what summarizes them into a digest.
C. The two are the same operation behind different beta flags, so either one achieves the removal being asked for.
D. Neither applies to tool results; the supported route is rebuilding the messages array client-side each turn.

---

**10.** `[task 8.1 · guaranteeing argument validity]` A `create_ticket` tool intermittently receives a `priority` value outside the four strings its schema allows, and the team wants arguments that validate exactly against that schema rather than being repaired afterwards. What gets them there?

A. Restate the four permitted values in the tool's `description`, so the model reads them before composing a call.
B. Validate server-side and return `tool_result` with `is_error: true`, letting the model correct itself on the next turn.
C. Move the constraint onto the request as `tool_choice: {"type": "tool", "name": "create_ticket", "strict": true}`.
D. Set `strict: true` on the tool definition itself, with `additionalProperties: false` and `required` in the schema.

---

**11.** `[task 8.2 · MCP server primitives]` A team publishes internal runbooks through an MCP server. They want Claude to both invoke runbook actions and offer the runbooks as reusable, parameterized starting points a user can pick from. Which statement about MCP primitives fits?

A. A server publishes tools only; anything resource-like or template-like has to live in the host application.
B. A server can publish tools, resources, and prompts — prompts being reusable templates the client surfaces to the user.
C. Resources and prompts are one primitive under two names, told apart by the MIME type the server declares.
D. Runbooks must each become a tool definition, since a server has no mechanism for publishing read-only content.

---

**12.** `[task 8.2 · wiring a remote MCP server to a request]` A request that sets `mcp_servers=[{"type": "url", "url": "...", "name": "runbooks"}]` and nothing else is rejected as a validation error before reaching the model. What is missing?

A. A matching `tools` entry of type `mcp_toolset` naming the same server.
B. Each remote tool restated locally as an ordinary definition with its own `input_schema`.
C. `tool_choice: {"type": "any"}`, without which the model is not permitted to reach a remote server.
D. The remote tool list written into the top-level `system` field so the model knows the tools exist.

---

**13.** `[task 8.3 · built-in vs custom vs Skills vs MCP]` A reporting feature needs two things: search the public web for recent filings, and hand back a formatted `.xlsx` workbook. The team wants whichever options carry the least code they have to own. Which TWO fit? (Select TWO)

A. Declare the server-side web search tool, which runs on Anthropic's infrastructure with no client loop.
B. Wrap a third-party search API as a custom tool, since retrieval has to be executed on the caller's side.
C. Use Agent Skills together with the code execution tool to generate the workbook inside the sandbox.
D. Stand up an MCP server exposing a spreadsheet tool, file generation being outside what the API itself reaches.

---

**14.** `[task 8.1 · why a server-tool failure never raises]` A pipeline wraps its web-search request in a try/except that logs nothing, yet users report silently empty results. The engineer confirms the handler never fires. Why?

A. The SDK retries server-tool failures to `max_retries` and then hands back an empty list without raising.
B. Failures of this kind report only through `usage`, leaving the content blocks structurally normal.
C. `APIConnectionError` is the one class raised for server tools, and the handler catches a different one.
D. The call returns HTTP 200 with an error object inside the result block, so nothing is ever raised.

---

**15.** `[task 7.4 · keeping a credential out of the sandbox]` A Managed Agents deployment must call a partner API with a long-lived key. Security review requires that the key not be readable from inside the agent's container, including by the model. Which approach satisfies that?

A. Export the key in the environment's setup script, so it exists only for the lifetime of that session's container.
B. Configure a vault `environment_variable` credential, stored by Anthropic and substituted at egress.
C. Place the key in the agent's `system` field, where it is available at the moment the outbound call is composed.
D. Commit it to the repository the container mounts, with file permissions restricted to the agent's user.

---

**16.** `[task 7.4 · key rotation and access reporting]` A platform team must rotate API keys each quarter and produce a report of which service accounts have been calling the API. Which surface and credential does that work require?

A. Any workspace API key, provided the `admin` scope is requested on the call itself.
B. The Models API, which reports per-key call volume alongside model capability metadata.
C. The Admin API, reached with an Admin key or an `org:admin` OAuth token — ordinary API keys are refused.
D. The web Console alone; key and service-account lifecycle has no programmatic surface.

---

**17.** `[task 2.5 · instructions across interfaces]` A standing instruction that works in a `claude.ai` conversation is not honoured by the team's API integration, which sends the same wording inside a `messages` array and nothing else. What explains the difference?

A. A product surface adds its own system prompt and account settings; an API request applies only what it carries.
B. Style instructions reach the model through `output_config` when sent via the API, and are ignored anywhere else in the request.
C. An instruction has to sit in the final user message to bind through the API, rather than earlier in the array.
D. Account-level preferences apply to API traffic only when the request is authenticated with that same account's key.

---
