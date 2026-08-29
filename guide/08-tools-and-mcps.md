# Domain 8: Tools and MCPs (10.6% · 5 Items)

## Overview
Domain 8 covers tool definition schemas, tool call execution, Model Context Protocol (MCP) servers, resources, prompts, and tool registration.

---

## Core Technical Concepts

### 1. Tool Declaration & Schema Design
- Tools are declared in the `tools` array parameter of `messages.create()`.
- Each tool definition requires `name`, `description`, and `input_schema` (JSON Schema object).

### 2. Model Context Protocol (MCP)
- Open protocol connecting AI models to external tools, resources, and prompts.
- **MCP Server Capabilities:**
  - **Tools:** Actionable endpoints model can execute.
  - **Resources:** Readable context data (URIs).
  - **Prompts:** Reusable prompt templates.
- **FastMCP SDK:** High-level Python/TypeScript SDK for rapid MCP server development.
