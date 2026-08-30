# CCDV-F Domain Drill — Domain 3: Claude Code

6 items, one correct answer each. Untimed. Answer all 6 first, then grade
against the key in one pass — item by item, reading each rationale,
including the ones you got right. Domain 3 covers Claude Code operation and
the CLI — `CLAUDE.md` project memory, the settings hierarchy, headless
execution, slash commands, hooks, and MCP server configuration. Suggested
sitting: all 6 in one ~10-minute session.

---

**1.** `[task 3.1 · CLAUDE.md hierarchy]` A repo has a `CLAUDE.md` at the repo root documenting the monorepo's shared build commands, and a second `CLAUDE.md` inside `packages/billing/` documenting that package's currency-rounding rules. A developer opens Claude Code from within `packages/billing/`. How does Claude Code use these two files together?

A. Only the `packages/billing/CLAUDE.md` file loads, because Claude Code reads memory from the current working directory alone.
B. Only the repo root `CLAUDE.md` loads; child directories are never scanned for any additional memory files at all.
C. Both files load together: the root file supplies monorepo-wide context and the package file adds its own rules.
D. Neither file loads automatically; the developer must reference each path explicitly in the prompt for its contents to be read.

---

**2.** `[task 3.1 · headless print mode]` A CI pipeline needs a step that hands Claude Code a diff, gets back a written summary, and exits without ever showing an interactive terminal UI, so the summary can be redirected straight into a build artifact. Which invocation approach fits this requirement?

A. Run `claude` interactively inside a `tmux` session, then scrape the pane's output once the interactive session ends.
B. Pipe the prompt in and run Claude Code in print mode so output returns directly to standard output for the script to use.
C. Open the normal interactive REPL and use a slash command to save the transcript to a file at the end of the session.
D. Launch the interactive session with a keyboard-automation script that types the prompt and captures the screen buffer.

---

**3.** `[task 3.1 · slash command reuse]` A team's engineers keep manually retyping the same multi-paragraph prompt asking Claude Code to review a diff against the team's five-point security checklist. A lead wants that prompt packaged so anyone can invoke it by typing a short name instead of pasting the whole paragraph every time. What should the lead create?

A. A custom slash command that stores the checklist prompt as a reusable, invokable template.
B. A new entry in `settings.json` that stores the prompt text under a custom permission rule.
C. A second `CLAUDE.md` file placed only in the security team's subdirectory with the checklist written inline.
D. A hook that fires on session start and prints the checklist text to the terminal for reference.

---

**4.** `[task 3.1 · hook lifecycle event]` A team wants every `Bash` tool call in a Claude Code session to first run through an internal command-allowlist script, blocking the call entirely if that script exits non-zero, before Claude's requested command ever executes. Which mechanism fits this requirement?

A. A `PreToolUse` hook that runs the script first and blocks the call on a non-zero exit.
B. A slash command that engineers run manually before asking Claude to execute any shell command.
C. A line in `CLAUDE.md` instructing Claude to always ask permission before running Bash commands.
D. A `PostToolUse` hook that logs the Bash command's output for later audit only after the command has already run.

---

**5.** `[task 3.1 · settings.json precedence]` An enterprise-managed settings file disables a specific tool for every user in the org, but a project's `.claude/settings.json` in the repo attempts to re-enable that same tool, and a developer's personal user-level settings also re-enable it. When Claude Code starts inside that repo, which setting actually applies?

A. The project-level setting wins, since it's the most specific to the repository the developer is currently working in.
B. The user-level setting wins, since personal configuration always overrides any shared configuration file.
C. The enterprise-managed setting wins, since it sits above project and user configuration in the precedence order.
D. Whichever file was modified most recently wins, since Claude Code merges settings by last-write timestamp.

---

**6.** `[task 3.1 · MCP server config]` A developer wants Claude Code, during an interactive session, to be able to query a company's internal ticket-tracking system through its existing MCP server rather than reimplementing the same calls as ad hoc shell commands. What should the developer do to make that server's tools available in the session?

A. Add the server's connection details to Claude Code's MCP configuration so its tools register for the session.
B. Paste the ticket-tracking system's API documentation into `CLAUDE.md` so Claude infers the correct request format itself.
C. Write a slash command that shells out to `curl` against the ticket-tracking system's own REST endpoints directly.
D. Add a `PreToolUse` hook that intercepts every Bash call and rewrites it into a ticket-tracking API request.
