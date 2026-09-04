# Domain 3: Claude Code (3.1% · 2 Items)

## Overview

Domain 3 tests Claude Code, Anthropic’s agentic coding tool for the command line. Developers are evaluated on repository configuration files (`CLAUDE.md`), settings precedence, non-interactive execution modes, custom commands, hooks, and tool security scopes.

---

## 1. `CLAUDE.md` Conventions & Hierarchical Inheritance

`CLAUDE.md` files provide persistent repository memory and standing instructions across developer sessions:

* **Location:** Placed in the project root and/or subdirectories.
* **Inheritance Rules:**
  * Root `CLAUDE.md` defines organization-wide or repository-wide invariants (code style, testing frameworks, primary build commands).
  * Subdirectory `packages/api/CLAUDE.md` adds localized instructions for that specific service.
  * When working in a subdirectory, Claude Code reads and **merges both files hierarchically**.
* **What Belongs in `CLAUDE.md`:** Standard build commands (`npm test`, `pytest`), architectural style guides, linting rules, and directory conventions.
* **What Does NOT Belong in `CLAUDE.md`:** API keys, passwords, environment-specific secrets, or individual developer tool preferences.

---

## 2. Settings Precedence Hierarchy

Configuration files are resolved across three distinct tiers with strict precedence:

$$\textbf{Enterprise Policy} \;\;\;>\;\;\; \textbf{Project Config} \;(\text{.claude/settings.json}) \;\;\;>\;\;\; \textbf{User Config} \;(\sim\text{/.claude/settings.json})$$

1. **Enterprise Policy:** Highest priority. Enforced by corporate administrators. Cannot be overridden, bypassed, or weakened by project or user settings.
2. **Project Config (`.claude/settings.json`):** Committed to version control. Governs project-specific tool allowlists, MCP servers, and hooks for the entire team.
3. **User Config (`~/.claude/settings.json`):** Local to the developer’s workstation. Stores personal UI preferences, themes, and personal paths.

---

## 3. Interactive vs. Headless Print Mode (`-p`)

Claude Code supports two primary execution workflows:

| Execution Mode | Command Flag | Primary Use Case | Output Behavior |
|---|---|---|---|
| **Interactive REPL** | `claude` | Daily pair programming, multi-step debugging, exploratory authoring | Full terminal UI, interactive permission prompts for bash/file edits. |
| **Headless Print Mode** | `claude -p "..."` / `--print` | CI/CD automation, pull request reviews, git hook linting, Unix pipelines | Non-interactive. Streams output directly to `stdout` and exits cleanly. |

### Composing with Headless Mode
```bash
# Evaluate git diff in a CI pipeline
git diff main...feature | claude -p "Review this diff for security vulnerabilities and output findings"
```

---

## 4. Custom Slash Commands & Argument Substitution

Custom commands standardize recurring development workflows:

* **Directory:** Stored as Markdown files under `.claude/commands/` (e.g., `.claude/commands/review-pr.md`).
* **Invocation:** Called within the REPL via `/review-pr`.
* **Dynamic Variables:**
  * `$ARGUMENTS` — Injects all text passed after the command name.
  * `$1`, `$2` — Positional parameter substitution.

---

## 5. Security Gates, Tool Permissions & Hooks

### Tool Permission Allowlists
Configure pattern-based approvals in `.claude/settings.json` to reduce interactive friction while maintaining safety:

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(pytest *)"
    ]
  }
}
```

### PreToolUse vs. PostToolUse Hooks
* **`PreToolUse` Hook:** Executes *before* a tool runs. Inspects the proposed command line or file path. If the hook exits with a non-zero code, execution is **blocked** before the shell runs.
* **`PostToolUse` Hook:** Executes *after* tool execution to validate, log, or sanitize results.

### MCP Configuration & Secrets Expansion
Register Model Context Protocol (MCP) servers in `.claude/mcp.json`. Always use environment variable expansion to avoid committing secrets:

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "PGPASSWORD": "${DB_PASSWORD}"
      }
    }
  }
}
```

---

## 6. Summary Checklist: Exam Invariants for Domain 3

- [ ] Root and subdirectory `CLAUDE.md` files merge hierarchically.
- [ ] Enterprise policy strictly overrides Project and User settings.
- [ ] Non-interactive CI/CD pipelines use `claude -p` / `--print` to stream to `stdout`.
- [ ] Custom slash commands support dynamic arguments via `$ARGUMENTS` or `$1`.
- [ ] Destructive commands are blocked before execution using `PreToolUse` hooks.
- [ ] MCP credentials use `${ENV_VAR}` expansion in `.claude/mcp.json`.
