# CCDV-F Domain Drill — Domain 8: Tools and MCPs

10 items, one correct answer each. Untimed. Answer all 10 first, then grade
against the key in one pass.

---

**1.** `[task 8.1 · tool definition structure]` A developer defines a `get_weather` tool for the Messages API but only includes `name` and `description` in the tool object, leaving out the third required top-level key. Claude's subsequent tool-use calls arrive with malformed or guessed arguments. Which key is missing from the definition?

A. `tool_choice`, the request-level parameter controlling when tools fire at all.
B. `input_schema`, the JSON Schema object describing the expected arguments.
C. `tool_use_id`, the identifier that links a call back to its eventual result.
D. `max_tokens`, the parameter that caps how long the tool's own response can run.

---

**2.** `[task 8.1 · tool_choice forced-tool form]` An order-processing agent has three tools available: `charge_card`, `issue_refund`, and `send_receipt`. On this turn the application needs Claude to call exactly `charge_card` — not `issue_refund`, not `send_receipt`, and not a plain-text reply. Which `tool_choice` value produces that guarantee?

A. `{"type": "auto"}`, which still leaves Claude free to reply with plain text.
B. `{"type": "any"}`, which forces some tool call but lets Claude pick among the three.
C. `{"type": "tool", "name": "charge_card"}`, which pins the call to that one tool.
D. Leaving `tool_choice` unset, since Claude defaults to the first tool in the array.

---

**3.** `[task 8.1 · tool_result error signaling]` Claude calls a `lookup_order` tool, and the model's request carries `tool_use_id` `toolu_9f3`. The order number turns out not to exist. The application sends back a `tool_result` block referencing `toolu_9f3` with the error text in its content, but the block is missing one field the model needs to read this as a failed call rather than a valid, merely-empty result. What's missing?

A. A `cache_control` field marking the block as ephemeral for caching purposes.
B. A second `tool_use_id` value covering an eventual retry attempt.
C. `is_error: true`, flagging the block as the result of a failed call.
D. A `stop_reason` field explaining why the assistant turn ended.

---

**4.** `[task 8.1 · parallel tool_result batching]` On one turn, Claude's assistant message contains two `tool_use` blocks: one calling `check_inventory`, one calling `get_shipping_rate`. The application runs both, then replies with the `check_inventory` result in one `user` message and, immediately after, the `get_shipping_rate` result in a second, separate `user` message. What is wrong with this sequence?

A. Both `tool_result` blocks belong in one `user` message, not split into two.
B. The two blocks must carry an identical `tool_use_id` value to match the same turn.
C. The `check_inventory` result must be sent before `get_shipping_rate` is ever invoked.
D. Parallel tool calls require a wrapping `system`-role message around both results.

---

**5.** `[task 8.2 · custom slash command]` A team wants a repeatable action — typing `/deploy-staging` mid-conversation to run their deployment checklist on demand — rather than something that fires automatically on every turn regardless of whether deployment is even relevant. Which customization mechanism fits this need?

A. A CLAUDE.md rule instructing the agent to deploy after every code change.
B. A custom slash command, defined as a file the agent runs when invoked by name.
C. A project-specific subagent that launches automatically in its own isolated context.
D. A system prompt override applied globally across every project the user opens.

---

**6.** `[task 8.2 · project-specific subagent]` A codebase has a recurring need: running a full security review of a diff without filling the main conversation's context with every file the review inspects, and restricting which tools that review is allowed to call while it runs. Which customization mechanism best fits this need?

A. A CLAUDE.md instruction reminding the agent to review diffs carefully before merging.
B. A slash command that simply prints out a static security checklist as plain text.
C. A project-specific subagent with its own context window and restricted tools.
D. Raising the `max_tokens` limit so the review's output is never truncated mid-response.

---

**7.** `[task 8.2 · CLAUDE.md standing behavior]` A repository's engineers are tired of reminding the agent every session that commits must reference a Jira ticket and that `git push --force` is never allowed on `main`. They want these rules to apply automatically in every session, without being invoked by name each time. Where should these standing rules live?

A. In a slash command that engineers must type before every single commit.
B. In the project's CLAUDE.md file, loaded automatically each session start.
C. In a subagent definition invoked only when working on release branches.
D. In the `input_schema` of a custom commit-validation tool the agent calls.

---

**8.** `[task 8.2 · combining customization mechanisms]` A team wants `/incident-review` typed by name mid-conversation, and once triggered, wants the review to run in its own context window with access to only a read-only log-search tool, so the main conversation's history stays uncluttered. Which single approach satisfies both the on-demand trigger and the isolated, tool-restricted execution?

A. A CLAUDE.md rule alone, since standing instructions can restrict tool access at session start.
B. A slash command alone, since typing its name already isolates the conversation's context.
C. A slash command that invokes a dedicated subagent, pairing on-demand triggering with isolation.
D. A subagent alone, since subagents already trigger by name without needing a slash command.

---

**9.** `[task 8.3 · MCP Resources vs Tools]` An MCP server exposes two capabilities to a connected client: one lets the client read the current contents of a `config.yaml` file without changing anything on the server, and the other lets the client trigger a `restart_service` action that mutates the server's running state. How should these two capabilities be classified under MCP's model?

A. Both as Tools, since MCP does not distinguish between passive reads and mutations.
B. Both as Resources, since neither operation depends on a live network round trip.
C. `restart_service` behaves like a Resource, while reading `config.yaml` functions as a Tool.
D. `config.yaml` reads back as a Resource; `restart_service` executes as a Tool.

---

**10.** `[task 8.3 · MCP transport choice]` A developer is building an MCP server meant to run as a local child process on the same machine as the client, communicating over standard input and output with no network exposure at all. Which transport should this server implement?

A. SSE, since it streams responses back to the client over an HTTP connection.
B. gRPC, since it offers strongly typed contracts suited to local process communication.
C. WebSocket, since it keeps a persistent bidirectional connection open for local use.
D. stdio, since the client spawns the server and pipes messages over standard streams.
