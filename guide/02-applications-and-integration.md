# Domain 2: Applications and Integration (33.1% · 18 Items)

## Overview

Domain 2 is the primary domain of the CCDV-F exam, representing one-third of the total score (33.1% / 18 items). It evaluates foundational software engineering, REST API mechanics, streaming protocols, SDK client behaviors, multimodal data handling, and production session lifecycle management.

---

## 1. REST API Mechanics & Statelessness

Anthropic’s Messages API is an HTTP REST service:

* **Endpoint:** `POST https://api.anthropic.com/v1/messages`
* **Mandatory Headers:**
  * `x-api-key: <ANTHROPIC_API_KEY>`
  * `anthropic-version: 2023-06-01`
  * `content-type: application/json`
* **Required Body Fields:** `model`, `max_tokens`, `messages`.
* **Message Array Structure:**
  * Strictly alternating `user` and `assistant` turns.
  * Must begin with a `user` turn (unless using beta mid-conversation system roles).
  * System instructions live in the top-level **`system`** parameter (string or array of text blocks), *never* as a `role: "system"` item in legacy endpoints.
* **Statelessness Invariant:** The Messages API maintains **zero server-side conversational state**. The application is entirely responsible for persisting conversational history and resending the full array of prior turns on every request.

---

## 2. The SDK Client vs. Raw REST

The official Anthropic Python/TypeScript SDK wraps the REST API:

```
+-------------------------------------------------------------------+
| Anthropic Client SDK (Client-Side Wrapper)                        |
|   ├── Typed Response Models (Message, ContentBlock, Usage)        |
|   ├── Exception Mapping (HTTP 4xx/5xx → Specific Exception)       |
|   ├── Automatic Retries (default max_retries=2 with backoff)       |
|   └── SSE Event Assembly (stream.text_stream, get_final_message)  |
+-------------------------------------------------------------------+
                                  │  HTTPS POST
                                  ▼
+-------------------------------------------------------------------+
| Anthropic Messages API (Stateless Server-Side Endpoint)           |
|   ├── Evaluates full submitted messages array                    |
|   ├── Enforces token limits, prompt caching, tool validation      |
|   └── Emits token generation stream                               |
+-------------------------------------------------------------------+
```

### SDK Invariants & Common Misconceptions
* **SDK Version Pinning:** Pinning your SDK package version in `requirements.txt` guarantees client-side code stability, typed signatures, and client retry behavior. However, **version pinning cannot force Anthropic’s servers to accept retired request parameters or deprecated API shapes**.
* **Statelessness is Unchanged:** Using the SDK does not automatically create server-side sessions. You still send full conversation history on each turn.

---

## 3. Server-Sent Events (SSE) Streaming Protocol

Setting `stream=True` returns a chunked Server-Sent Events (SSE) stream. Understanding event order is vital for real-time applications:

| SSE Event Name | Data Emitted | Purpose / Handling |
|---|---|---|
| **`message_start`** | `Message` object with empty content | Contains message `id`, `model`, `role`, and initial **`usage.input_tokens`**. |
| **`content_block_start`** | `ContentBlock` metadata | Emits index and type (`text` or `tool_use`). For tools, emits `id` and `name`. |
| **`content_block_delta`** | `Delta` object | Emits incremental payload: `text_delta` (partial prose) or `input_json_delta` (partial JSON string). |
| **`content_block_stop`** | Index | Confirms current content block is complete. |
| **`message_delta`** | Final metadata & usage | Delivers final **`usage.output_tokens`** and terminal **`stop_reason`**. |
| **`message_stop`** | None | Closes the SSE connection. |

> [!WARNING]
> **SSE Connections are NOT Resumable:** If a network blip or timeout disconnects an active stream mid-generation, there is no "reconnect to stream" or resume-from-offset API. The client must handle the connection failure and **replay the complete request prompt from scratch**.

---

## 4. SDK Exception Hierarchy & Resiliency Architecture

To build resilient applications, handle exceptions specifically rather than catching generic errors:

```
AnthropicError (Base SDK exception)
  ├── APIError
  │     ├── APIConnectionError (Network down, DNS drop, connection refused)
  │     ├── APITimeoutError (Request exceeded client timeout)
  │     └── APIStatusError (HTTP error returned by server)
  │           ├── BadRequestError (HTTP 400 - Invalid params, schema mismatch)
  │           ├── AuthenticationError (HTTP 401 - Bad API key)
  │           ├── PermissionDeniedError (HTTP 403 - Tier/feature forbidden)
  │           ├── NotFoundError (HTTP 404 - Resource/Batch ID not found)
  │           ├── RateLimitError (HTTP 429 - Quota exceeded; read retry-after)
  │           └── InternalServerError (HTTP 500 / 529 - Server error or overloaded)
```

### Specific-First Catch Hierarchy
```python
import anthropic

try:
    response = client.messages.create(...)
except anthropic.RateLimitError as e:
    # Read the integer retry-after header (in seconds)
    retry_after = int(e.response.headers.get("retry-after", 5))
    time.sleep(retry_after)
    # Retry request...
except (anthropic.InternalServerError, anthropic.APIConnectionError):
    # Retryable transient failures: exponential backoff + jitter
    time.sleep(backoff_with_jitter())
    # Retry request...
except anthropic.BadRequestError as e:
    # Non-retryable: fix client payload/schema bug; do NOT retry blindly
    logger.error(f"Malformed request parameters: {e}")
    raise
```

---

## 5. Multimodal Documents (PDFs) and Images

Claude accepts multimodal inputs structured as content blocks in user messages:

### PDF Document Invariants
* **Format:** Pass as `type: "document"` with `source: {"type": "base64", "media_type": "application/pdf", "data": "..."}`.
* **Size & Page Limits:** Standard models support up to **32 MB and 600 pages** per request.
* **Prompt Caching:** Large PDF documents can be marked with `cache_control: {"type": "ephemeral"}` to avoid re-upload and re-processing costs across multiple queries.

### Image Block Invariants
* **Format:** Pass as `type: "image"` with `source: {"type": "base64", "media_type": "image/jpeg"|"image/png"|"image/gif"|"image/webp", "data": "..."}`.
* **MIME Matching:** The content block `type` must strictly match the data type (`image` vs `document`).

---

## 6. Session Lifecycle & Multi-Tenant Architecture

Session lifecycle was explicitly tested on the CCDV-F exam. Developers must manage concurrent user conversations systematically:

### Session Lifecycle States
1. **Creation & Initialization:** Client generates a cryptographically unique `session_id`. It loads the baseline `system` prompt, configures tool definitions, and initializes an empty `messages` store.
2. **Active Turn Exchange:**
   * Client receives incoming user turn.
   * Client appends user turn to stored history.
   * Client invokes Messages API with complete accumulated history.
   * Client appends assistant response and executed tool results.
3. **Rolling State Checkpointing:**
   * For long-running conversations, the application moves an ephemeral prompt cache breakpoint to the settled history, maintaining cached prefixes.
   * When history reaches context bounds, the application performs compaction (summarizing historical turns while preserving core context).
4. **Eviction & Expiration:** Sessions inactive beyond a designated TTL (e.g. 24 hours) are evicted from memory/Redis and archived to durable storage.

### Multi-Tenant Isolation: Structural vs. Prompt-Level
When serving multiple corporate tenants or user accounts:

* **CORRECT (Structural Isolation):**
  * Maintain isolated, dedicated `messages[]` arrays per tenant in the data store.
  * Inject tenant-specific business logic into the top-level `system` parameter.
  * Maintain separate prompt cache keys so one tenant's traffic never hits or shares another tenant's cached memory.
* **FLAWED ANTI-PATTERN (Prompt-Level Prefixes):**
  * Reusing a shared conversation thread and attempting to separate tenants using in-band prefixes (e.g., `[Tenant 42] Process order #1234`).
  * In-band prompt prefixes fail under prompt injection, risk severe cross-tenant data leakage, and break prompt caching efficiency.

---

## 7. Summary Checklist: Exam Invariants for Domain 2

- [ ] Messages API is stateless; full conversational history must be passed each turn.
- [ ] SDK version pinning protects client-side dependencies, not server-side API shape support.
- [ ] SSE streams are not resumable; connection drops require full request resubmission.
- [ ] Rate limit backoff (429) should read the integer `retry-after` header in seconds.
- [ ] PDF document limits: 32 MB and 600 pages using `type: "document"`.
- [ ] Multi-tenant isolation must be structural in data architecture, never prompted via in-band tags.
