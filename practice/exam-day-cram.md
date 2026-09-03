# CCDV-F Exam Day Cram Sheet

**53 items · 120 min · scaled 100–1000 · pass 720**
Sitting: **2026-09-04, 15:45 SGT**

Weights: **D2 33.1%** · D5 16.8% · **D1 14.7%** · D6 11.0% · D8 10.6% · D7 8.1% · D3 3.1% · D4 2.6%
Two thirds of the paper is D2 + D5 + D1. Budget your attention there.

---

## 1. Pacing protocol — no timed rehearsal was sat, so run the clock deliberately

| Checkpoint | Be at | If behind |
|---|---|---|
| 0:30 | item 13 | stop re-reading stems; first pass only |
| 1:00 | item 27 | start flagging aggressively |
| 1:30 | item 40 | guess-and-flag anything not cracked in 60s |
| 1:55 | item 53 | last 5 min for flagged items |

**The 90-second rule.** Any item you haven't cracked in 90 seconds gets your best guess, a flag, and a move-on. There is **no penalty for a wrong answer**, so never leave one blank.

**Triage by weight, not by stubbornness.** One D4 item is 2.6% of the paper; two D2 items you rushed past are worth more. If you're behind, sacrifice depth on the small domains.

**Read the response-count line on every item.** The format is mixed multiple-choice and multiple-response, and each item states how many to select. Your mocks ran 30% multi-response — higher than the real paper is likely to be — so don't pattern-match "this looks like a Select TWO."

---

## 2. Two test-craft warnings specific to how you prepared

**Your practice bank leaked answers through extreme language.** Measured across all 245 items: absolutes ("never", "at all", "regardless", "entirely") appear in **27.7% of distractors vs 7.3% of correct answers — a 3.8× tell**. You have been rewarded for eliminating the loud option. **Real exam distractors are plausible and measured.** Kill that reflex at the door: choose on the mechanism, not the register.

**Discount your 96.2%.** Mock 1 was authored by the same pipeline as the drills, against the same objective list, and sat untimed. It measured "no gaps in what I chose to test." It is not a predicted score.

---

## 3. UNLEARN — four facts your bank drilled that now return HTTP 400

The exam guide names *adaptive thinking*, *effort levels*, and *fast mode* (obj 5.1) and *"breaking behavior changes across model releases"* (obj 5.3). It is written against the current API. These four are the highest-risk items in your recall:

| You drilled | Current behaviour |
|---|---|
| `thinking: {"type":"enabled","budget_tokens":N}`, min 1024, `max_tokens > budget_tokens` | **`budget_tokens` → 400** on Opus 5 / 4.8 / 4.7 / Sonnet 5 / Fable. Use **`thinking: {"type":"adaptive"}`**; tune depth with `output_config.effort` |
| `temperature` must be 1.0 when thinking is on | **`temperature` / `top_p` removed → 400** on those models |
| Prefill `{"role":"assistant","content":"{"}` to force bare JSON | **Prefill → 400** on all current models. Use **`output_config: {format: {...}}`** (structured outputs), or a system instruction |
| Cache minimum 1,024 tokens (3.5 Sonnet) / 2,048 (3 Haiku) | Minimum cacheable prefix is **model-dependent, 512–4096**. Those model names are retired |

Also corrected: native PDF is **32 MB and 600 pages** (100 pages only on 200K-context models) — your bank teaches a flat 100.

---

## 4. Still correct, still worth a glance

**Exceptions → status.** `BadRequestError` 400 · `AuthenticationError` 401 · `PermissionDeniedError` 403 · `NotFoundError` 404 · `RateLimitError` 429 (read `retry-after`) · `InternalServerError` 500/529 (backoff + jitter) · `APIConnectionError`/`APITimeoutError` (resend whole prompt; SSE is not resumable).
Catch a **most-specific-first chain**, not one broad class — a single `except APIStatusError` loses retryable vs non-retryable. SDK defaults: timeout 10 min, `max_retries` 2 (408/409/429/5xx + connection).

**`stop_reason`.** `end_turn` · `max_tokens` (silent truncation — check for it) · `stop_sequence` · `tool_use` · `pause_turn` · `refusal`. `stop_details` is populated **only** on `refusal` — guard before reading.

**Tool results.** Parallel `tool_use` blocks → **one** `role:"user"` message containing **every** `tool_result`, each with its exact `tool_use_id`. Splitting them across messages trains Claude to stop calling in parallel. A failed tool returns `tool_result` with `is_error: true` — never drop it, never raise instead.

**Tool definition.** `name` + `description` + `input_schema` (required). `strict: true` goes **top-level on the tool**, needs `additionalProperties: false` and `required` — *not* on `tool_choice`. `bash` / text-editor tools are Anthropic-defined and take **no** `input_schema`.

**`tool_choice`.** `auto` (default) · `any` (must call something) · `{"type":"tool","name":...}` · `none`. Forced `any`/`tool` returns 400 on Fable 5.1 / Mythos 5.1.

**Caching.** Exact prefix match; render order **`tools` → `system` → `messages`**; max **4** breakpoints; put volatile content (timestamps, request IDs) *after* the last breakpoint. Verify with **`usage.cache_read_input_tokens`** — a persistent 0 means a silent invalidator. TTL refreshes on each read.

**Batch API.** Async, **50% discount**, 24-hour window. Poll `processing_status` until `"ended"`. **Results come back in any order — key by `custom_id`, never by position.**

**D7 security.** Direct injection = user types it; **indirect** = adversarial text arrives inside retrieved data (scraped page, ingested PDF, customer email). **PreToolUse** hook inspects arguments and can **block** a destructive call; **PostToolUse** runs after and sanitizes/redacts output. Least privilege, HITL on irreversible mutations, validate model-supplied IDs against the authenticated session rather than a global admin credential.

---

## 5. The gap topics — untested in your bank, named in the blueprint

One line each. If an item mentions one of these, this is your only prep on it.

- **Four ways to build an agent.** Manual loop (you own everything) · **Tool Runner** (`client.beta.messages.tool_runner`, loops over *your* tools, you host) · **Managed Agents** (Anthropic runs the loop **and** hosts a per-session container) · **Claude Agent SDK** (a *separate product* — Claude Code as a library, brings built-in Read/Write/Bash/Grep, you host). Key axis: **harness vs deployment** — only Managed Agents supplies both.
- **Managed Agents shape.** Create the **Agent once**, reference its ID from **every session**. `model` / `system` / `tools` live on the agent, never the session. Scheduled deployments fire sessions on cron.
- **Effort.** `output_config: {effort: "low"|"medium"|"high"|"xhigh"|"max"}` — *inside* `output_config`. Default `high`. `xhigh` is the sweet spot for coding/agentic work. This is the cost dial, not `max_tokens` (which the model cannot see and which truncates).
- **Task budget vs `max_tokens`.** Task budget is **advisory**, token-denominated, and the model *is* aware of it so it paces itself. `max_tokens` is an enforced per-response ceiling the model cannot see.
- **Fast mode.** Opus 5 / 4.8 only; beta messages endpoint + `speed: "fast"` top-level; ~2.5× output token rate at **premium** price; separate rate limit; excluded from Batch, Priority Tier, and third-party clouds.
- **Context editing vs compaction.** Context editing **clears** old tool results (`clear_tool_uses_*`). Compaction **summarizes** earlier context (~150K trigger) — and you must append `response.content` back, not just the text, or state is lost. Don't invert these.
- **Server / built-in tools.** Web search, web fetch, code execution run on Anthropic's infrastructure — no client loop. **Failures return HTTP 200 with an error object inside the result block; nothing is raised.** On success `content` is a *list*; on error it's an *object*. Web fetch only fetches URLs already in the conversation.
- **Agent Skills.** Invoked via `container={"skills":[...]}` with the code execution tool. Skills ≠ Managed Agents. The sandbox has `python-docx`, `python-pptx`, `matplotlib`, `pillow`, `pypdf` — so "generate a .xlsx/.pptx/PDF" is a Skills + code-execution job, not a custom tool you build.
- **MCP.** Three server primitives: **tools** (actions), **resources** (readable content), **prompts** (reusable templates the client surfaces). Transports: **stdio** for a local child process, HTTP/SSE for remote. The API connector needs **both** halves: `mcp_servers=[...]` **and** a `tools` entry `{type:"mcp_toolset", mcp_server_name:<same name>}`.
- **8.3 tradeoff.** Reach for built-in/server tools first, then Skills, then MCP, then a custom tool. "Build it yourself" is usually the wrong answer to a least-code question.
- **Secrets (obj 7.4 — zero items in your bank).** Vault `environment_variable` credentials are stored by Anthropic and **substituted at egress**, so the value never enters the sandbox or model context. Scoping a secret to an ephemeral container still leaves it readable inside that container.
- **Admin API.** Key rotation, service accounts, workspaces, rate-limit reports — needs an **Admin key or `org:admin` OAuth token**; ordinary API keys are refused. Usage/cost reports are raw HTTP, not in the SDKs.
- **Interfaces (obj 2.5, 8.6% — largest sub-objective).** claude.ai / Desktop / Claude Code wrap the conversation in their own system prompt, tools, and account settings. An **API request applies only what that request carries** — nothing is inherited.
- **Structured outputs.** `output_config: {format: {...}}`; the old `output_format` parameter is deprecated. `messages.parse()` validates against your schema.
- **Models API.** Fields are `max_input_tokens` (context window), `max_tokens` (output cap), `capabilities`. There is **no** `context_window` field.

---

## 6. My confirmed misses — read these last

1. **Post-tool-use hook timing.** Secret redaction and PII masking run **after** tool execution (PostToolUse), on the output. Blocking a destructive call happens **before** (PreToolUse), on the arguments. *(Mock 1 Q48)*
2. **Tool definition keys.** A tool object needs `name`, `description`, `input_schema`. **`tool_choice` is a request-level parameter, never part of the tool object.** Missing `input_schema` → Claude has no argument shape and calls arrive malformed. *(Mock 1 Q50)*
3. _[add any gap-coverage-drill misses here — especially items 4 and 7, which test the stale facts in §3]_

---

**Last thing before you go in:** the mechanism, not the register. Your practice rewarded spotting the loud wrong answer; the real paper won't offer one.
