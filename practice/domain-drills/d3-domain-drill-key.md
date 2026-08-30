# CCDV-F Domain Drill — Domain 3: key and rationales

Grade in one deferred pass. For every miss, note which it was: didn't know
it, misread the item, or picked the plausible-but-soft option.

---

**1. C** — Claude Code combines memory from multiple levels: the root `CLAUDE.md` supplies monorepo-wide context and the package-level file layers its own package-specific rules on top, rather than one file silently replacing the other. Reading only the local file, reading only the root file, or requiring explicit path references all describe a single-source model that isn't how the hierarchy actually combines context. *(task 3.1; concept: claude_md_hierarchy; item `d3d-01`)*

---

**2. B** — Piping a prompt in and running Claude Code in print mode returns the result straight to standard output with no interactive UI at all, which is exactly what a scriptable CI step needs. Scraping a `tmux` pane, saving a transcript from inside the REPL, and driving the interactive session with keyboard automation all still depend on an interactive terminal existing in the first place. *(task 3.1; concept: headless_print_mode; item `d3d-02`)*

---

**3. A** — A custom slash command packages the checklist prompt as a template invocable by a short name, which is exactly the reuse problem here. A `settings.json` permission entry, a subdirectory `CLAUDE.md`, and a session-start hook each store or trigger text in ways that don't give engineers a short, on-demand way to invoke the same prompt. *(task 3.1; concept: slash_command_reuse; item `d3d-03`)*

---

**4. A** — A `PreToolUse` hook runs before the tool call executes and can block it outright when the allowlist script fails, matching the requirement to stop the command before it ever runs. A manual slash command depends on engineers remembering to run it, a `CLAUDE.md` instruction is only a request Claude might not follow, and a `PostToolUse` hook only observes the command after it has already executed. *(task 3.1; concept: hook_lifecycle_event; item `d3d-04`)*

---

**5. C** — Enterprise-managed configuration sits above both project and user settings in the precedence order, so it wins regardless of what the repo or the developer's personal file tries to set. Project-level and user-level settings can override each other in narrower conflicts, but neither outranks an enterprise-managed policy, and Claude Code doesn't resolve conflicts by file modification time. *(task 3.1; concept: settings_precedence; item `d3d-05`)*

---

**6. A** — Registering the ticket-tracking MCP server's connection details in Claude Code's MCP configuration is what makes its tools available for Claude to call directly during the session. Pasting API docs into `CLAUDE.md` only gives Claude descriptive text to reason from, a slash command wrapping raw `curl` calls reimplements the integration by hand, and a hook that rewrites Bash calls addresses interception rather than exposing the server's own tools. *(task 3.1; concept: mcp_server_config; item `d3d-06`)*
