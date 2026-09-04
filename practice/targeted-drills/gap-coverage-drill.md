# CCDV-F Gap-Coverage Drill — 11 items

**Purpose:** every item here tests a named technique from §6 of the official
exam guide that had **zero coverage** in the practice bank at the time it was
written.

**Authored:** 2026-09-03, by hand, against the current Claude API surface.
Not sampled from the drilled pool — no item here restates one you have sat.

**How to sit it:** untimed or ~40 min, one pass, no peeking. Key is sealed in
`gap-coverage-drill-key.md`. Item 8 is multi-response and needs both letters
to count.

**Pruned 2026-09-04, after the exam.** Six items were removed because the
sitting tested none of that surface: adaptive thinking vs `budget_tokens`,
`output_config.effort`, fast mode, the removal of assistant prefill, MCP
connector wiring, and Managed Agents vault credentials. The paper asked no
questions about new or changed API features and named no models. Stable item
ids (`gap-NN`) are unchanged in the key, so the six are still findable in git
history. What remains is the conceptual material the blueprint names.

**Register note:** distractors here are deliberately plausible. The existing
bank leaks answers through extreme language (absolutes appear in 27.7% of its
distractors vs 7.3% of its correct answers, a 3.8x tell). Nothing in this set
is eliminable that way — the real paper does not offer a loud wrong option,
so choosing on register rather than mechanism is a habit worth unlearning.

**Coverage map:** 1.2 (×2), 1.3, 2.5, 5.4, 6.1, 7.4, 8.1 (×2), 8.2, 8.3.

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

**4.** `[task 5.4 · why a cache never reads]` A 30,000-token system prompt carries one `cache_control` breakpoint, but `usage.cache_read_input_tokens` stays at 0 across repeated calls. The block ends with a rendered line reading `Generated at 2026-09-03T11:42:07Z`. Which change restores hits?

A. Add three further breakpoints, so that at least one of the four prefixes still matches between calls.
B. Shorten the block below the model's minimum cacheable prefix, which moves it to a cheaper matching path.
C. Move the timestamp after the last breakpoint, leaving the cached prefix byte-identical on every call.
D. Render the timestamp to the nearest minute, so calls landing in the same minute share a prefix.

---

**5.** `[task 6.1 · clearing tool output vs summarizing history]` A long-running agent's history is dominated by large file-read tool results. The team wants those specific results gone from what the model sees, while the original task brief and the recent turns stay intact. Which mechanism fits, and how does it differ from the alternative?

A. Context editing's `clear_tool_uses` removes old tool results outright; compaction summarizes earlier context.
B. Compaction removes the tool results once its token threshold trips; context editing is what summarizes them into a digest.
C. The two are the same operation behind different beta flags, so either one achieves the removal being asked for.
D. Neither applies to tool results; the supported route is rebuilding the messages array client-side each turn.

---

**6.** `[task 8.1 · guaranteeing argument validity]` A `create_ticket` tool intermittently receives a `priority` value outside the four strings its schema allows, and the team wants arguments that validate exactly against that schema rather than being repaired afterwards. What gets them there?

A. Restate the four permitted values in the tool's `description`, so the model reads them before composing a call.
B. Validate server-side and return `tool_result` with `is_error: true`, letting the model correct itself on the next turn.
C. Move the constraint onto the request as `tool_choice: {"type": "tool", "name": "create_ticket", "strict": true}`.
D. Set `strict: true` on the tool definition itself, with `additionalProperties: false` and `required` in the schema.

---

**7.** `[task 8.2 · MCP server primitives]` A team publishes internal runbooks through an MCP server. They want Claude to both invoke runbook actions and offer the runbooks as reusable, parameterized starting points a user can pick from. Which statement about MCP primitives fits?

A. A server publishes tools only; anything resource-like or template-like has to live in the host application.
B. A server can publish tools, resources, and prompts — prompts being reusable templates the client surfaces to the user.
C. Resources and prompts are one primitive under two names, told apart by the MIME type the server declares.
D. Runbooks must each become a tool definition, since a server has no mechanism for publishing read-only content.

---

**8.** `[task 8.3 · built-in vs custom vs Skills vs MCP]` A reporting feature needs two things: search the public web for recent filings, and hand back a formatted `.xlsx` workbook. The team wants whichever options carry the least code they have to own. Which TWO fit? (Select TWO)

A. Declare the server-side web search tool, which runs on Anthropic's infrastructure with no client loop.
B. Wrap a third-party search API as a custom tool, since retrieval has to be executed on the caller's side.
C. Use Agent Skills together with the code execution tool to generate the workbook inside the sandbox.
D. Stand up an MCP server exposing a spreadsheet tool, file generation being outside what the API itself reaches.

---

**9.** `[task 8.1 · why a server-tool failure never raises]` A pipeline wraps its web-search request in a try/except that logs nothing, yet users report silently empty results. The engineer confirms the handler never fires. Why?

A. The SDK retries server-tool failures to `max_retries` and then hands back an empty list without raising.
B. Failures of this kind report only through `usage`, leaving the content blocks structurally normal.
C. `APIConnectionError` is the one class raised for server tools, and the handler catches a different one.
D. The call returns HTTP 200 with an error object inside the result block, so nothing is ever raised.

---

**10.** `[task 7.4 · key rotation and access reporting]` A platform team must rotate API keys each quarter and produce a report of which service accounts have been calling the API. Which surface and credential does that work require?

A. Any workspace API key, provided the `admin` scope is requested on the call itself.
B. The Models API, which reports per-key call volume alongside model capability metadata.
C. The Admin API, reached with an Admin key or an `org:admin` OAuth token — ordinary API keys are refused.
D. The web Console alone; key and service-account lifecycle has no programmatic surface.

---

**11.** `[task 2.5 · instructions across interfaces]` A standing instruction that works in a `claude.ai` conversation is not honoured by the team's API integration, which sends the same wording inside a `messages` array and nothing else. What explains the difference?

A. A product surface adds its own system prompt and account settings; an API request applies only what it carries.
B. Style instructions reach the model through `output_config` when sent via the API, and are ignored anywhere else in the request.
C. An instruction has to sit in the final user message to bind through the API, rather than earlier in the array.
D. Account-level preferences apply to API traffic only when the request is authenticated with that same account's key.

---
