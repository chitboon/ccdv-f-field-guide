# Domain 7: Security and Safety (8.1% · 4 Items)

## Overview
Domain 7 focuses on application security, prompt injection defense, sandboxing, Human-in-the-Loop (HITL) gates, and identity/secrets management.

---

## Core Security Invariants

### 1. Indirect Prompt Injection Defense
- User-supplied inputs or retrieved external documents must be treated as untrusted data.
- Wrap external data in distinct XML tags and enforce strict validation hooks before executing tool calls derived from retrieved context.

### 2. Human-in-the-Loop (HITL) Confirmation
- High-impact or destructive operations (e.g. database deletes, financial transactions, outbound emails) MUST require human confirmation before calling the tool.

### 3. Least Privilege & Tool Scope
- Restrict tool permissions to the minimal set of resources required for the task.
- Sandbox code execution environments (e.g., Docker container or WASM sandbox) when running LLM-generated code.
