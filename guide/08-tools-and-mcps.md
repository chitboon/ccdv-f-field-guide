# Domain 8: Tools and Model Context Protocol (MCP) (10.6% · 5 Items)

## Overview

Domain 8 covers tool declaration schemas, the semantic role of tool descriptions, tool execution lifecycles, parallel tool calling mechanics, request-level `tool_choice` controls, and Model Context Protocol (MCP) architecture.

---

## 1. Tool Declaration & Schema Design

Tools are passed to the Messages API via the top-level `tools` array:

```python
tools = [
    {
        "name": "get_weather",
        "description": "Retrieve current temperature, humidity, and conditions for a given city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name, e.g. San Francisco"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
]
```

### The Three Required Keys
1. **`name`:** A unique identifier string matching `^[a-zA-Z0-9_-]{1,64}$`.
2. **`description`:** Detailed natural language explanation of what the tool does, when to call it, and what constraints apply.
3. **`input_schema`:** Standard JSON Schema object defining arguments and required properties.

---

## 2. Invariant: Tool Description is the Specification

A frequent exam discriminator:

> [!IMPORTANT]
> **The `description` IS the Specification:**
> Claude has no access to your backend source code. The natural language `description` is the *only* source of truth Claude has to determine whether invoking the tool is appropriate.

* **`strict: true` vs. `description`:**
  * `strict: true` validates JSON schema syntax adherence (types, enum values, required fields).
  * `strict: true` **cannot** teach the model *when* to invoke the tool or *what* the tool semantically accomplishes.
  * Clear, unambiguous descriptions prevent tool misfires, invalid invocations, and hallucinated arguments.

---

## 3. Request-Level `tool_choice` Parameter

`tool_choice` dictates how Claude selects tools. It is configured at the **request level**, *never* inside the tool definition:

| `tool_choice` Value | Behavior | Common Production Use Case |
|---|---|---|
| **`{"type": "auto"}`** (Default) | Claude autonomously decides whether to invoke tools or respond in natural language. | Open-ended customer support, general agent workflows. |
| **`{"type": "any"}`** | Claude **must invoke at least one tool** from the `tools` array, but decides which one. | Routing routers, intent classification agents. |
| **`{"type": "tool", "name": "..."}`** | Claude **must invoke the exact named tool**. | Data extraction pipelines, structured JSON enforcement. |

---

## 4. Parallel Tool Calling & Single-Turn Response Protocol

When Claude identifies that multiple tools can run concurrently (or one tool multiple times), it emits multiple `tool_use` blocks within a single assistant response:

```
[Claude Assistant Turn]
  ├── tool_use block (id: "call_1", name: "fetch_stock_price", input: {"ticker": "AAPL"})
  └── tool_use block (id: "call_2", name: "fetch_stock_price", input: {"ticker": "MSFT"})
```

### The Single-Turn Bundling Rule
Your application must execute the tools and reply with a **single message with `role: "user"`** containing an array of `tool_result` blocks for **every** `tool_use_id`:

```python
# CORRECT: One single user turn bundling ALL tool results
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        ...,
        assistant_turn,
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "call_1",
                    "content": "AAPL: $224.50"
                },
                {
                    "type": "tool_result",
                    "tool_use_id": "call_2",
                    "content": "MSFT: $448.20"
                }
            ]
        }
    ]
)
```

> [!CAUTION]
> **Anti-Pattern:** Never send consecutive `user` turns for parallel tool calls (e.g. sending `call_1` in one message, then `call_2` in another). Consecutive same-role turns violate the alternating role API invariant.

---

## 5. Built-in vs. Custom vs. MCP Tools

| Tool Type | Definition Style | `input_schema` Required? | Execution Location |
|---|---|:---:|---|
| **Custom Client Tools** | Defined in `tools` array | **Yes** | Client application executes locally. |
| **Anthropic Built-in Tools** | Defined by versioned `type` (e.g. `bash_20241022`) | **No** | Client sandbox or Anthropic container. |
| **Model Context Protocol (MCP)** | Discovered dynamically via MCP client | Handled by MCP server | MCP Server process (local or remote). |

---

## 6. Model Context Protocol (MCP) Architecture

The Model Context Protocol (MCP) standardizes how models connect to external data sources and tools:

### MCP Server Primitives
* **Tools:** Callable executable functions (e.g., query database, send Slack message, run terminal command).
* **Resources:** Readable, passive content URIs (e.g., `file:///var/log/app.log`, database schemas, documentation).
* **Prompts:** Standardized prompt templates surfaced directly to end-users in UI dropdowns.

### MCP Communication Transports

| Transport | Communication Mechanism | Ideal Environment |
|---|---|---|
| **`stdio`** | Local child process communication via standard input/output (`stdin` / `stdout`). | Local desktop tools, CLI utilities, developer environments. |
| **HTTP with SSE** | Networked transport: client sends HTTP POST requests; server streams responses via Server-Sent Events (SSE). | Remote microservices, cloud deployments, multi-tenant enterprise architectures. |

---

## 7. Summary Checklist: Exam Invariants for Domain 8

- [ ] Tool declarations require `name`, `description`, and `input_schema`.
- [ ] The `description` is the semantic specification that governs when Claude calls the tool.
- [ ] `tool_choice` is configured at the request level, never inside the tool definition.
- [ ] Parallel tool calls must be answered with **one single `user` message** containing all `tool_result` blocks.
- [ ] Built-in tools have versioned types and require no `input_schema`.
- [ ] Failed tool calls must return `is_error: true` inside the `tool_result` content block.
- [ ] MCP primitives are Tools (actions), Resources (readable data), and Prompts (templates).
- [ ] MCP transports are `stdio` (local subprocess) and HTTP/SSE (remote networked services).
