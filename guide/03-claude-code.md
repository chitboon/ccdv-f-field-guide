# Domain 3: Claude Code (3.1% · 2 Items)

## Overview
Claude Code is Anthropic's CLI-first agentic coding environment. This domain covers repository configuration, non-interactive execution, tool scopes, and project context (`CLAUDE.md`).

---

## Core Technical Concepts

### 1. `CLAUDE.md` Conventions
- Project-level context file read automatically by Claude Code.
- Contains build commands, test suite execution instructions, code style rules, and repository invariants.

### 2. CLI Execution Modes
- **Interactive:** Terminal session with real-time prompt / tool permissions.
- **Headless / Non-Interactive:** Run in CI/CD pipelines using `-p` / `--print` or pipe flags.

### 3. Tool Permissions & Security Scopes
- Bash tool execution, file editing (`Edit`, `Write`), file viewing (`View`), directory listing (`LS`).
- Security boundaries prevent arbitrary shell commands without user confirmation in interactive mode.
