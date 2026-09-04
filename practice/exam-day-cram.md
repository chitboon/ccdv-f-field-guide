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

**Your practice bank leaked answers through extreme language.** Measured across the 245 items in the bank at audit time: absolutes ("never", "at all", "regardless", "entirely") appear in **27.7% of distractors vs 7.3% of correct answers — a 3.8× tell**. You have been rewarded for eliminating the loud option. **Real exam distractors are plausible and measured.** Kill that reflex at the door: choose on the mechanism, not the register.

**Discount both mock scores.** Mock 1 (96.2%) and Mock 2 (98.1%) were authored by the same pipeline as the drills, against the same objective list, **before** the coverage audit — and both were sat **untimed, split across sittings, with immediate per-item feedback**. They measured "no gaps in what I chose to test." Neither is a predicted score. The honest first-pass number is **90.5% across the 168 non-mock items**, and the two clusters that cost marks (objectives 1.2 and 5.1) sit in §5 and §6, not in the drilled domains.

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

## 5b. Second-wave gaps — zero items in 405, found by the 2026-09-04 audit

Seven of these had **no** item anywhere in the bank; seven more had three or
fewer. Two sit inside the paper's largest sub-objectives. One line each.

**The SDK is a typed client over the same REST endpoint (5.2, 6.1%).** It adds typed exceptions per status, automatic retries (default `max_retries` 2 — 408/409/429/5xx + connection), streaming event assembly, and typed objects. It does **not** add server-side conversation state: the Messages API is **stateless** and you resend the full history every turn, SDK or curl.

**Streaming is HTTP SSE, not websockets (5.2).** One-directional, **not resumable** — a dropped connection means resending the whole prompt. There is no reconnect-to-message-id.

**Cache check-pointing (5.4).** In a growing conversation, move a breakpoint to the end of the transcript-so-far each turn so settled history is cached instead of re-billed. Four `cache_control` blocks is the ceiling, so it is a *rolling* checkpoint. Appending to a cached prefix is safe; **editing** inside it is what invalidates.

**What `usage` actually reports (5.4).** `cache_creation_input_tokens` (**1.25×** base input) and `cache_read_input_tokens` (**0.10×**) are separate counters — **not** inside `input_tokens`. Summing only input+output under-reports every cached request. Thinking tokens bill as **output**; there is no `thinking_tokens` field.

**Context isolation via subagents (6.1, 3.8%).** For fan-out reading, give each item its own subagent and context window and return a structured extract to the parent. Compaction *summarizes* one agent's history, clearing *removes* tool results — subagents give you **more windows**. Don't answer a fan-out question with compaction.

**Tool description writing (8.1).** The description **is** the specification — the model has no other source for when a tool applies, what arguments mean, or what comes back. `strict: true` guarantees arguments *validate*, not that the call was *appropriate*. Different layers.

**Plugin management and plugin dependencies (2.5 / 2.6).** Treat a shared toolkit as a dependency: pin its version in the project's checked-in config so every clone resolves the same revision. Per-machine installs drift; a periodic manual reinstall is a request, not a control.

**Prompt versioning (2.6).** Prompts are software — an id stored with each edit, recorded on every request beside the model id, benchmarked against a golden set in CI before shipping. A cache is not an audit trail.

**Input sanitization is delimiting, not escaping (6.2).** Wrap untrusted content in explicit tags, say in `system` that its contents are data and never instructions, and put the operative instruction **after** the block. Escaping markup protects a parser; the model is not parsing.

**Defensive parsing (6.3).** Constrain with `output_config={"format": {...}}` (or `messages.parse()`) **and** still parse behind a typed failure path. Brace-stripping breaks on a brace inside a string.

**Confidence is not accuracy (6.3).** Wrong output reads exactly like right output. A self-reported confidence score comes from the same process that produced the confident error — it filters nothing. Ground figures in retrieved text and cite them.

**Image blocks (2.3).** `{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": ...}}` in the user content array. `document` is the PDF/text shape — the block type must match the file's MIME type.

**MCP primitives (8.2).** **Tools** = actions the model invokes. **Resources** = readable content pulled into context. **Prompts** = reusable templates the client surfaces to the user. Not interchangeable. Transport: `stdio` local child process, HTTP/SSE remote.

**Supervisor hierarchies (1.1, 4.5%).** Works because each worker returns a *result*, not its transcript — that is what keeps the parent's context bounded. Progress state lives in a store outside the model. Sharing one conversation across workers forfeits the whole benefit.

**Claude Code: `CLAUDE.md` + headless (3.1).** Standing conventions go in `CLAUDE.md` at the repo root (merging hierarchically with subdirectory files). Non-interactive runs use print mode `claude -p`, which streams to stdout and composes with pipelines. `settings.json` carries permissions, env, and hooks — not standing prose.

**Isolating a failure (4.1).** Compare artifacts at the boundary: value present in the recorded `tool_use.input` and absent in what was written puts the fault in the **integration layer**, not the model. Do that before touching the prompt.

**Per-tenant session hygiene (2.5, 8.6%).** Isolation is structural: a separate `messages` array per tenant, that tenant's policy in top-level `system`, each prefix cached independently. An instruction in a shared thread is not a boundary.

---

## 6. My confirmed misses — read these last

1. **Post-tool-use hook timing.** Secret redaction and PII masking run **after** tool execution (PostToolUse), on the output. Blocking a destructive call happens **before** (PreToolUse), on the arguments. *(Mock 1 Q48)*
2. **Tool definition keys.** A tool object needs `name`, `description`, `input_schema`. **`tool_choice` is a request-level parameter, never part of the tool object.** Missing `input_schema` → Claude has no argument shape and calls arrive malformed. *(Mock 1 Q50)*
3. **Tool Runner is not the Agent SDK.** This one was missed four times across two drills, so read it twice:
   - **Tool Runner** — `client.beta.messages.tool_runner`, part of the ordinary SDK. Loops over **only the tools you define**. **No built-in tools.** What it buys you over a hand-written loop is **per-turn hooks**: approval gates, logging, error interception, result modification, retries.
   - **Claude Agent SDK** — a *separate package*, Claude Code as a library. **Ships** Read/Write/Edit/Bash/Glob/Grep/WebSearch/WebFetch.
   - Both are **harness-only and self-hosted**. The tool surface is the difference.
   - **Managed Agents** is the only one of the four that supplies **both** harness and deployment. Its per-session container is **Anthropic-hosted** — that container *is* the deployment half.

4. **Multi-response technique.** Scored 1/6 on Select TWO items before correcting this. For each option ask **"is this statement true of this stem — yes or no?"** and take every yes. Do **not** rank the four and take the best-looking pair. If two options are direct negations of each other, one of them is almost certainly in the answer.

5. **Insecure output handling (OWASP LLM02) is not prompt injection.** Rendering a model's output straight into a page/DOM without escaping is an **output**-side flaw — the fix is escaping/sanitising at the render boundary, plus treating model text as untrusted data. Prompt injection is the **input** side (adversarial text arriving in the prompt or in retrieved data). If a stem describes model text ending up in HTML, a shell, or SQL, the answer is output escaping, not an input filter. *(Mock 2 Q45 — the only miss on the most recent 53 items)*

6. **Also missed on first pass, all in §5:** `effort` lives *inside* `output_config` (top-level is silently ignored, not rejected) · `thinking.display` now defaults to `omitted` · fast mode was **removed on Opus 4.7** and never ran on third-party platforms · toggling `speed` **invalidates the prompt cache** · **Priority Tier is not supported on Opus 5.**

7. **Mid-conversation system messages preserve prompt cache.** To inject an operator instruction mid-session without invalidating the cached top-level system prompt or prefix, append `{"role": "system", "content": ...}` directly into the `messages` array. Do **not** modify the top-level `system` parameter (breaks prefix matching) and do **not** inject `"SYSTEM:"` markers into user turns (untrusted user/doc channel). *(Current-API Drill Item 5)*

8. **Batch results are unordered & union-typed.** `client.messages.batches.results()` returns rows in **non-deterministic order** — never `zip(rows, results)`; always match using **`custom_id`**. Furthermore, only `result.type == "succeeded"` carries `.message`; checking `.message` on errored/canceled/expired entries raises `AttributeError`. *(Current-API Drill Item 10)*

---

**Last thing before you go in:** the mechanism, not the register. Your practice rewarded spotting the loud wrong answer; the real paper won't offer one.

