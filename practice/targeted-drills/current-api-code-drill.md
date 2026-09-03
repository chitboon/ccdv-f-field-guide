# CCDV-F Current-API Code Drill — 10 items

**Purpose:** every item here is a code-reading scenario built on the API
surface the 2026-09-04 STATUS review corrected — the shapes that replaced
`budget_tokens`, assistant prefill, the fixed cache minimums, and the flat
100-page PDF ceiling — plus the concepts named in §6 of the exam guide that
neither earlier targeted drill exercised.

**Authored:** 2026-09-04, by hand, against the `claude-api` reference (not
from the bank, not from recall — three of these facts changed under the bank).
No item restates one from the 17-item Gap-Coverage drill, the 12-item
Miss-Remediation drill, or either mock.

**Format:** each item shows a snippet and a symptom. You are diagnosing, not
recalling a definition. Items **3, 6 and 9 are multi-response** and need both
letters to count — for each option ask *"is this true of this stem, yes or
no?"* and take every yes. Do not rank four options and take the best pair.

**Register note:** distractors are plausible and measured. Several are the
*previous* correct answer for the same question — the bank's own teaching,
one model generation out of date. Others are half-right: they name the right
parameter and describe it wrongly. Neither is eliminable on tone.

**Coverage map:** 2.1, 2.2 (×2), 2.3, 2.4, 5.4, 6.1, 7.2, 8.1, 8.3.

---

**1.** `[task 2.1 · constraining response format on a current model]` An invoice-extraction service was migrated from Claude 3.5 Sonnet to `claude-opus-5`. Since the migration every call fails with a 400 before any tokens are generated.

```python
resp = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"Extract the invoice fields:\n{doc}"},
        {"role": "assistant", "content": "{"},
    ],
)
data = json.loads("{" + resp.content[0].text)
```

What is the correct repair?

A. Move the opening brace into the system prompt as a formatting instruction and keep the trailing assistant turn, which is what anchors the response to raw JSON.
B. Drop the trailing assistant turn and constrain the response shape with `output_config={"format": {...}}`, parsing the validated result directly.
C. Keep the messages as they are and add `stop_sequences=["}"]`, which bounds the response at the closing brace and restores parseable JSON.
D. Replace the assistant turn with `output_format="json"`, the request parameter that supersedes prefilling entirely on this model family.

---

**2.** `[task 2.3 · retry scope in an error handler]` A wrapper around the Messages API retries with exponential backoff and jitter. In production it burns its full retry budget on requests that were never going to succeed, and a malformed `tool_result` payload takes 45 seconds to surface as an error.

```python
for attempt in range(max_retries):
    try:
        return client.messages.create(**kwargs)
    except anthropic.APIStatusError as e:
        delay = base * (2 ** attempt) * random.uniform(0.5, 1.5)
        time.sleep(min(delay, max_delay))
raise
```

What is wrong with this handler?

A. `APIStatusError` does not cover quota responses, so 429s fall through uncaught while the loop retries everything else; a second `except anthropic.RateLimitError` branch is needed above it.
B. The jitter multiplier can exceed 1, so a computed delay can land above the intended exponential step; clamping the multiplier to the 0–1 range restores the backoff curve.
C. `APIStatusError` is the parent of retryable and non-retryable alike, so 400s and 404s get retried; the handler needs a most-specific-first chain.
D. The SDK already retries this class of failure internally, so the client loop multiplies every attempt; removing the wrapper and raising `max_retries` restores a single backoff curve.

---

**3.** `[task 2.2 · reading a response safely]` A moderation pipeline runs on `claude-opus-5` with adaptive thinking enabled. It works in staging and raises `AttributeError: 'NoneType' object has no attribute 'category'` on roughly the first production call. **(Select TWO — tick both letters before submitting)**

```python
msg = client.messages.create(
    model="claude-opus-5",
    thinking={"type": "adaptive"},
    max_tokens=4096,
    messages=[{"role": "user", "content": ticket}],
)
if msg.stop_details.category == "cyber":
    route_to_human(msg)
verdict = msg.content[0].text
```

Which TWO statements about this code are correct?

A. `stop_details` is populated only on `stop_reason: "refusal"` and is `None` for other stop reasons, so this access needs a guard ahead of it and a fallback path.
B. `stop_details` also carries a category when generation was cut off at `max_tokens`, so once guarded this branch doubles as the silent-truncation check.
C. With thinking on, `content[0]` may be a thinking block rather than the verdict, so indexing position 0 for text is unsafe either way.
D. A refusal is returned as a 4xx status by the Messages API, so the category check belongs inside an `except` branch rather than after a call that has already returned successfully.

---

**4.** `[task 2.4 · document input at scale]` A contract-review tool sends a 240-page, 18 MB PDF to `claude-opus-5` as an inline base64 `document` block, then re-sends the identical block on each of roughly 40 follow-up questions in the same review session. Latency and input cost are both climbing.

```python
doc_block = {
    "type": "document",
    "source": {"type": "base64", "media_type": "application/pdf",
               "data": b64_contract},
}
resp = client.messages.create(
    model="claude-opus-5", max_tokens=4096,
    messages=[{"role": "user", "content": [doc_block, {"type": "text", "text": q}]}],
)
```

Which assessment is correct?

A. At 240 pages the document is over the 100-page ceiling for PDF input; splitting it into three documents is required before any caching work is worthwhile.
B. Base64 document blocks are excluded from prompt caching, so the contract has to be extracted to plain text before any cache breakpoint placed after it will hold.
C. The 18 MB payload sits above the per-request document cap, and the Files API exists to carry documents past that cap, which makes it the required route for a contract this size.
D. The document sits within the limits for this model; upload it once through the Files API, reference it by `file_id`, and cache the prefix so it is read rather than re-billed.

---

**5.** `[task 5.4 · an operator instruction mid-session]` A support agent on `claude-opus-5` runs 60-turn sessions behind a cached system prompt and a stable tool list. When an incident starts, ops needs every in-flight session to begin refusing refund promises. The handler rewrites the top-level `system` string and continues the conversation; from that turn on, `usage.cache_read_input_tokens` reads 0 for the rest of every affected session.

```python
system = BASE_SYSTEM + "\n\nESCALATION FREEZE: do not promise refunds."
resp = client.messages.create(
    model="claude-opus-5", system=system, tools=TOOLS,
    messages=history, max_tokens=2048,
)
```

What change keeps the cached prefix intact?

A. Append the instruction as a `{"role": "system", ...}` entry in `messages` rather than editing the top-level `system` field, leaving the cached prefix unchanged.
B. Add a fifth `cache_control` breakpoint immediately after the appended instruction so the new suffix is cached alongside the original prefix.
C. Carry the instruction in the next user message behind a `SYSTEM:` marker, which keeps the system field byte-identical and costs nothing to cache.
D. Accept the loss — the cache is prefix-matched, so an operator instruction introduced mid-session invalidates it regardless of where it is placed.

---

**6.** `[task 6.1 · long-session state]` A research agent runs for hours on `claude-opus-5` with server-side compaction enabled. Past the four-hour mark it starts re-running searches it already ran and re-reading files it already summarized. **(Select TWO — tick both letters before submitting)**

```python
resp = client.beta.messages.create(
    model="claude-opus-5",
    betas=["compact-2026-01-12"],
    tools=TOOLS, messages=messages, max_tokens=8192,
)
messages.append({"role": "assistant", "content": resp.content[0].text})
```

Which TWO statements are correct?

A. Compaction clears earlier tool results out of the transcript, so the client is responsible for re-fetching and re-appending any result the agent still needs later.
B. Appending only `resp.content[0].text` drops the compaction blocks the API relies on to substitute for the compacted history on the next request.
C. Appending `resp.content` unchanged preserves every block the response carried, compaction blocks included, and is what keeps the summarized state alive.
D. The beta flag on its own is inert; compaction also has to be requested through `context_management={"edits": [{"type": "compact_20260112"}]}` on the same call.

---

**7.** `[task 8.1 · Anthropic-defined tools]` A developer wants Claude's built-in bash tool on a build agent and writes this definition. Claude calls the tool, but its arguments and behaviour are nothing like the built-in tool the team saw demoed.

```python
tools = [{
    "name": "bash",
    "description": "Run a shell command on the build server",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]
```

What is actually happening?

A. The name `bash` is reserved for the Anthropic-defined tool, so a custom definition claiming it is rejected at validation until the tool is given a different name.
B. The definition is missing `strict: true`, which is the flag that promotes a schema-bearing custom definition to the Anthropic-defined equivalent of the same name.
C. This is an ordinary custom tool that happens to be named `bash`; the Anthropic-defined one is selected by a versioned `type` and carries no `input_schema` of its own.
D. The definition is nearly right and needs `type` added alongside the existing keys, since Anthropic-defined tools take the same `input_schema` as custom ones plus a versioned `type`.

---

**8.** `[task 8.3 · picking a surface for file generation]` A nightly reconciliation job must return a formatted `.xlsx` workbook, not a table in the response text. The team wants the least code they own. Which call shape does that?

A. Create a Managed Agent with `client.beta.agents.create(...)`, then open a session per run and collect the workbook from the session's container.
B. Call `client.beta.messages.create(...)` with `container={"skills": [...]}` and the `code_execution_20260521` tool, letting the skill build the workbook in the sandbox.
C. Define a custom `write_xlsx` tool, execute it client-side with `openpyxl` on every run of the loop, and return the written path in the `tool_result`.
D. Attach the skill with `client.beta.skills.attach(...)` under the `skills-2025-10-02` beta header, which registers it for subsequent message calls.

---

**9.** `[task 7.2 · where a model's output lands]` An internal dashboard summarizes inbound customer emails with Claude and renders each summary into the page. An analyst opens a ticket and their browser executes a script that originated in the body of one of those emails. **(Select TWO — tick both letters before submitting)**

```javascript
const summary = await summarize(email.body);   // Claude's text
document.getElementById("summary").innerHTML = summary;
```

Which TWO statements are correct?

A. This is insecure output handling: model text reached a rendering sink without escaping, and the sink is where the vulnerability lives.
B. The payload arrived inside retrieved content, so this is indirect prompt injection and the correct fix is a filter on the email body before it reaches the prompt.
C. Instructing Claude in the system prompt never to emit HTML or script tags addresses the root cause, since the model is what produces the rendered string.
D. Model output is untrusted data at the boundary — render it with `textContent`, or sanitize the HTML — whatever is done to the inbound email.

---

**10.** `[task 2.2 · reading batch results]` A weekly job summarizes 4,000 support threads through the Message Batches API. It polls until `processing_status` is `"ended"` before reading. Summaries land on the wrong threads, and a handful of rows raise `AttributeError` on `.message`.

```python
batch = client.messages.batches.create(requests=reqs)
# ... poll until batch.processing_status == "ended" ...
results = list(client.messages.batches.results(batch.id))
for row, res in zip(rows, results):
    row.summary = res.result.message.content[0].text
```

What explains both symptoms?

A. `results()` streams as the batch drains, so a list built the moment the status flips to `"ended"` can be short; re-reading it once the results URL is fully written restores order and completeness.
B. The results call needs its ordering pinned explicitly — passing the `custom_id` sort option returns the rows in submission order and omits the entries that carry no message at all.
C. Thinking blocks sit at `content[0]` for the threads that needed reasoning, which both shifts the text and breaks the attribute access on those rows.
D. Batch results come back in any order, so zipping by position misaligns them; key by `custom_id`, and branch on `result.type` before reading `.message`, which succeeded entries carry.

---

*10 items · 3 multi-response · key in `current-api-code-drill-key.md`*
