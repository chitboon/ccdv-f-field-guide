# Domain 1: Agents and Workflows (14.7% · 8 Items)

## Overview

Domain 1 tests how to design, construct, and orchestrate agentic systems using Claude. Developers must master the distinction between deterministic workflows and autonomous agents, understand core agent loop mechanics, manage `stop_reason` state transitions, isolate context using subagents, and implement resilient error recovery.

---

## 1. Architectural Patterns: Workflows vs. Autonomous Agents

Anthropic categorizes agentic architectures into two fundamental paradigms:

```
Deterministic Workflows (Code Controls Flow)
  ├── Prompt Chaining (Step A → Step B → Step C)
  ├── Routing (Classifier directs input to specialized prompt/model)
  ├── Parallelization (Sectioning / Voting across parallel LLM calls)
  ├── Orchestrator-Workers (Central coordinator assigns sub-tasks to workers)
  └── Evaluator-Optimizer (Generator creates output; Critic validates & loops)

Autonomous Agents (Model Controls Flow)
  └── While Loop: Model reasons, selects tools, inspects results, and decides termination.
```

### When to Use Which
* **Use Workflows** when tasks are well-scoped, steps are predictable, and high consistency / latency bounds are paramount. Programmatic code maintains control of the execution graph.
* **Use Autonomous Agents** when tasks are open-ended, the sequence of operations cannot be predetermined, and the model must dynamically explore, use tools, and react to unpredictable intermediate feedback.

---

## 2. The Core Agent Loop & Termination Contracts

An autonomous agent operates on a continuous feedback loop between the client application and Claude's Messages API:

```
               +---------------------------------------+
               |  Client initiates messages.create()   |
               +---------------------------------------+
                                  |
                                  v
                    +---------------------------+
                    | Model evaluates context   |
                    +---------------------------+
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
[stop_reason: "tool_use"]                    [stop_reason: "end_turn"]
Model emits tool_use blocks                  Model finishes natural response
            |                                           |
            v                                           v
Client executes tools locally                Client terminates loop &
            |                                returns output to user
            v                                           
Client constructs single "user" turn                    
with tool_result for EVERY tool_use_id                  
            |                                           
            +-------------------------------------------+
```

### `stop_reason` Invariants & Handling

| `stop_reason` | Meaning | Developer Action |
|---|---|---|
| **`"end_turn"`** | Model reached a natural stopping point. | Terminate loop; return response text or structured data to user. |
| **`"tool_use"`** | Model requested one or more tool calls. | Extract all `tool_use` blocks, execute each tool, and reply with bundled `tool_result` blocks. |
| **`"max_tokens"`** | Generation exceeded `max_tokens` (silent truncation). | **Detect as an error state.** Prompt model for continuation or raise `max_tokens`. Do not treat as normal completion. |
| **`"stop_sequence"`**| Generation encountered custom string delimiter. | Output bounded at delimiter. Process extracted content. |
| **`"pause_turn"`** | Long-running turn paused mid-flight. | Resend returned `response.content` unchanged as next assistant turn. |
| **`"refusal"`** | Model declined on safety grounds. | Only state where `stop_details` is populated. Guard before reading. Surface handled error; do not retry. |

> [!IMPORTANT]
> **Prose is Never a Stop Signal:** Claude may output explanatory text (*"Let me search the database..."*) in the exact same response as a `tool_use` block. Never exit a loop because text was generated; **only `stop_reason` dictates loop continuation or termination**.

---

## 3. Subagent Hierarchies & Context Isolation

As agent workflows scale, monolithic single-context conversations degrade due to context window saturation, tool confusion, and cost explosion.

### The Supervisor (Orchestrator-Workers) Pattern
* **Context Boundary:** The supervisor maintains a high-level plan. It invokes subagents to execute specific domain tasks (e.g., code analysis, web research, invoice parsing).
* **Return Value Contract:** Workers return **condensed results or structured summaries**, *not their entire internal execution transcripts*. This keeps the parent's context bounded and pristine.
* **External State Persistence:** Progress state, artifact IDs, and checkpoint data live in an external database or key-value store, not solely within LLM conversational memory.

### Context Isolation for Fan-Out Processing
* When processing large volumes of independent items (e.g., analyzing 40 distinct contracts), **spawn independent subagents with separate context windows**.
* **Anti-Pattern:** Attempting to feed all 40 contracts into a single context window or relying on compaction/summarization inside one thread. Compaction summarizes past history of *one* stream; subagents give you *multiple independent windows*.

---

## 4. Error Handling & Recovery Inside Agent Loops

When a tool fails (e.g., HTTP 500 from an external service, invalid database query, file not found):

```python
# CORRECT: Inform the model of tool execution failure
tool_result = {
    "type": "tool_result",
    "tool_use_id": block.id,
    "content": "DatabaseError: Table 'orders_2025' does not exist.",
    "is_error": True  # Instructs Claude that the action failed
}
```

* **Never Raise Unhandled App Exceptions:** Crashing the application terminates the agent loop prematurely and loses state.
* **Always Set `is_error: True`:** If you return error text without `is_error: True`, Claude interprets the error message as valid data and may hallucinate a successful outcome based on the error string.
* **Loop Circuit Breakers:** Always enforce an iteration counter (e.g., `max_iterations = 15`) and a token budget ceiling to guarantee that a looping agent never runs indefinitely.

---

## 5. Summary Checklist: Exam Invariants for Domain 1

- [ ] Autonomous loops branch strictly on `stop_reason`, never on the presence or absence of text.
- [ ] Multiple tool calls in parallel must be answered with **one single `user` message** containing all `tool_result` blocks.
- [ ] Failed tool operations return `is_error: true` in the `tool_result` block.
- [ ] Supervisor agents receive structured summaries from workers, keeping transcripts isolated.
- [ ] Subagents provide context isolation for fan-out tasks; compaction provides length reduction for a single long-running session.
- [ ] `stop_reason == "max_tokens"` indicates silent truncation that requires developer remediation.
