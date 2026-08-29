# Domain 1: Agents and Workflows (14.7% · 8 Items)

## Overview
Agents combine LLMs with tool execution, loop control (`stop_reason`), state management, and multi-agent coordination. Developers building with Claude must master agent architectures, loop mechanics, subagent delegation, and control flows.

---

## Key Invariants & Architectural Patterns

### 1. The Core Agent Loop Mechanics
- **Turn Lifecycle:** Client sends `messages.create()` -> Claude responds -> If `stop_reason == "tool_use"`, client executes tool -> Client returns `type: "tool_result"` -> Client calls `messages.create()` again.
- **Termination Signals:**
  - `stop_reason: "end_turn"` — Generation finished, no further action required.
  - `stop_reason: "tool_use"` — Model requested one or more tool calls; client must execute and reply.
  - `stop_reason: "max_tokens"` — Generation hit max token threshold; handle context truncation or payload splitting.

### 2. Multi-Agent Delegation & Patterns
- **Orchestrator-Subagent Pattern:** A central coordinator agent breaks large problems into sub-tasks, assigns sub-tasks to specialized subagents, and synthesizes final outputs.
- **Subagent Error Reporting:** Subagents return `is_error: true` inside a `tool_result` block rather than throwing unhandled exceptions. This preserves coordinator context and enables recovery.
- **Reflection / Evaluator-Optimizer:** An agent generates candidate solutions (e.g., code), executes tests via tools, evaluates errors, and loops until tests pass.

### 3. State Management & Context Pruning
- **Stateless API:** Messages API retains zero server-side state. Each request must pass full valid message history.
- **Context Preservation:** Long-running loops must prune or summarize historical tool outputs while preserving system prompt instructions and recent conversation context.

---

## Anti-Patterns & Common Traps
- **Ignoring `is_error`:** Returning error text without `is_error: true` confuses Claude into treating error output as valid data.
- **Infinite Tool Loops:** Always implement a max iteration guard (e.g., `max_turns = 10`) to prevent unconstrained API cost burn.
- **Dropping System Instructions:** Resetting context history without re-injecting the system prompt breaks agent alignment and role behavior.
