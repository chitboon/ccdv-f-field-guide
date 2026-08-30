# CCDV-F Domain Drill — Domain 8: key and rationales

Grade in one deferred pass. For every miss, note which it was: didn't know
it, misread the item, or picked the plausible-but-soft option.

---

**1. B** — A tool definition requires exactly three top-level keys: `name`, `description`, and `input_schema`; the JSON Schema in `input_schema` is what tells the model the shape of valid arguments, and without it the model has nothing structured to fill in. `tool_choice` is a separate request-level parameter, not part of the tool object; `tool_use_id` belongs to a call's result, not its definition; `max_tokens` governs the assistant's overall response length. *(task 8.1; concept: tool_definition_input_schema; item `d8d-01`)*

---

**2. C** — `{"type": "tool", "name": "charge_card"}` is the only form that pins the call to one specific tool. `auto` still permits a text-only reply, `any` forces a call but leaves the choice among all three tools open, and an unset `tool_choice` gives no such guarantee — there's no "first tool in the array" default. *(task 8.2; concept: tool_choice_pinned_tool; item `d8d-02`)*

---

**3. C** — `is_error: true` is what marks the `tool_result` block as a failed call, letting the model reason about the failure structurally instead of treating the error text as ordinary output. `cache_control` governs prompt caching, a second `tool_use_id` is unrelated to signaling failure, and `stop_reason` describes why an assistant turn ended, not the status of one tool call. *(task 8.1; concept: tool_result_is_error; item `d8d-03`)*

---

**4. A** — When Claude issues multiple `tool_use` blocks in one assistant turn, the follow-up must be a single `user` message containing a `tool_result` for every `tool_use_id` — splitting them across two consecutive `user` messages is invalid. Matching `tool_use_id` values across two different calls would be wrong, not required; nothing about parallel calls dictates execution order; and MCP-style parallel results don't need a wrapping `system` message. *(task 8.1; concept: parallel_tool_result_batching; item `d8d-04`)*

---

**5. B** — A custom slash command is exactly the mechanism for an on-demand, invoked-by-name action like `/deploy-staging`. A CLAUDE.md rule would instead apply automatically on every turn regardless of relevance, a subagent launches for isolated sub-tasks rather than being typed by name mid-conversation, and a global system prompt override reaches far beyond one team's one project. *(task 8.2; concept: custom_slash_command; item `d8d-05`)*

---

**6. C** — A project-specific subagent runs in its own context window and can be restricted to a specific tool set, which keeps the main conversation's context clean while limiting what the review is allowed to touch. A CLAUDE.md reminder doesn't isolate context or restrict tools, a slash command that prints a static checklist performs no actual review, and raising `max_tokens` addresses response length, not context isolation. *(task 8.2; concept: project_subagent_isolation; item `d8d-06`)*

---

**7. B** — CLAUDE.md is loaded automatically at session start, which is exactly what makes standing rules like ticket references and a force-push ban apply every session without anyone invoking them by name. A slash command still requires typing it before each commit, a subagent invoked only for release branches wouldn't cover everyday commits, and a tool's `input_schema` only shapes that one tool's arguments. *(task 8.2; concept: claude_md_standing_rules; item `d8d-07`)*

---

**8. C** — Neither mechanism alone covers both requirements: a slash command supplies the on-demand, typed-by-name trigger, but only a subagent supplies its own isolated context window and restricted tool access, so a slash command that dispatches to a dedicated subagent is what covers both. CLAUDE.md applies automatically rather than on demand, a bare slash command doesn't isolate context by itself, and a bare subagent isn't invoked by typing a name mid-conversation. *(task 8.2; concept: slash_command_plus_subagent; item `d8d-08`)*

---

**9. D** — MCP treats a passive, read-only data stream like the `config.yaml` contents as a Resource, comparable to an HTTP GET, while an action that mutates server state like `restart_service` is a Tool, comparable to an HTTP POST. Classifying both as Tools or both as Resources erases that distinction, and reversing which one is which mislabels the mutation as passive. *(task 8.3; concept: mcp_resources_vs_tools; item `d8d-09`)*

---

**10. D** — stdio is the transport for local integrations, where the client spawns the server as a child process and the two communicate over stdin/stdout with no network exposure. SSE is MCP's transport for remote, networked servers instead; WebSocket and gRPC are not among MCP's two defined transports at all. *(task 8.3; concept: mcp_transport_stdio; item `d8d-10`)*
