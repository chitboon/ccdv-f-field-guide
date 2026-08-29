# Domain 2: Applications and Integration (33.1% · 18 Items)

## Overview
Applications & Integration is the single heaviest domain of the CCDV-F exam (33.1% / 18 items). It tests software engineering foundations, REST API integration, streaming, SDK client usage, configuration management, and structured data handling.

---

## Core Technical Foundations

### 1. Claude Messages API Mechanics
- **Endpoint & Auth:** `POST https://api.anthropic.com/v1/messages` with `x-api-key` header and `anthropic-version: 2023-06-01`.
- **Required Fields:** `model`, `max_tokens`, `messages` array.
- **Message Roles:** Strictly alternating `user` and `assistant` messages. Top-level `system` parameter for system prompts.

### 2. Streaming Responses & Event Buffering
- `stream=True` returns Server-Sent Events (SSE):
  - `message_start`: Initial message metadata & input token count.
  - `content_block_start`: Start of text or tool call block.
  - `content_block_delta`: Text chunks (`text_delta`) or JSON tool arguments (`input_json_delta`).
  - `content_block_stop`: Block completion.
  - `message_delta`: Output token count & `stop_reason`.
  - `message_stop`: Final event.

### 3. Error Handling & Resiliency
- **429 (Rate Limit) & 5xx (Server Error):** Implement exponential backoff with full jitter.
- **400 (Invalid Request):** Client parameter error (e.g. invalid message role or missing required field) — do not retry blindly.
- **401 / 403:** Authentication/permission failure.

### 4. Configuration & Decoupling
- Keep system prompts and model hyperparameters outside hardcoded source code (use environment variables or external prompt management repositories).
- Secure secret key management: Never check API keys into source control.

---

## Code Example: SDK Client Integration
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a precise data processing subagent.",
    messages=[{"role": "user", "content": "Parse customer ID 4819."}]
)

print(response.content[0].text)
```
