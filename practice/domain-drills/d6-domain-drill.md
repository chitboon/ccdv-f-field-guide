# CCDV-F Domain Drill — Domain 6: Prompt and Context Engineering

12 items, one correct answer each. Untimed. Answer all 12 first, then grade
against the key in one pass — item by item, reading each rationale,
including the ones you got right. This is a scenario-based drill, not a
recall check: every stem carries a concrete situation you must reason about.
Suggested sittings: 1-6, 7-12 (two ~10-minute sessions), or all 12 in one
sitting.

---

**1.** `[task 6.1 · XML section delimiting]` A developer configures a customer support bot in Python. The system prompt currently concatenates reference documentation and behavioral guardrails in raw unformatted text:

```python
system_prompt = f"""
{return_policy_doc}
You are a support agent for RetailCorp.
Never issue refunds exceeding $100 without manager approval.
Always maintain a courteous tone.
"""
```

In production, Claude quotes policy clauses back to customers as if they were rigid operational commands the agent must follow. How should the developer refactor the `system_prompt` string to establish clear structural separation?

A. Shorten `return_policy_doc` to under 500 tokens so total system prompt token length decreases.
B. Wrap `return_policy_doc` in `<policy_docs>` and rules in `<guidelines>`, referencing them explicitly.
C. Move `return_policy_doc` into `messages[0]["content"]` alongside the customer's question unformatted.
D. Append a `stop_sequences=["Refund Policy"]` parameter inside the `client.messages.create()` payload.

---

**2.** `[task 6.1 · few-shot pattern demonstration]` A support-ticket tagging prompt describes the target format only in prose: "Reply with a comma-separated list of category tags, lowercase, no spaces after commas." Outputs still vary — sometimes capitalized, sometimes with spaces, sometimes as a bulleted list. What change is most likely to lock in the exact pattern?

A. Repeat the same prose formatting instruction three separate times in a row within the system prompt itself.
B. Move the same exact formatting instruction out of the system prompt and into the user turn on every request instead.
C. Add two or three input-ticket/output-tag-list example pairs showing the exact formatting live in the prompt.
D. Increase `max_tokens` so truncation can no longer plausibly be the cause of these malformed comma-separated tag lists.

---

**3.** `[task 6.1 · assistant message pre-fill]` A developer writes a Python script to extract structured security review findings from code diffs:

```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="Output only a raw JSON object with keys 'vulnerabilities' and 'severity'.",
    messages=[{"role": "user", "content": f"Review diff:\n{code_diff}"}],
)
findings = json.loads(response.content[0].text)
```

In production, `json.loads()` intermittently raises `json.decoder.JSONDecodeError` because Claude outputs conversational preamble (`"Here is the security assessment in JSON:"`) before the `{`. What modification to the `messages` payload natively forces Claude to output pure JSON starting at character 1?

A. Set `temperature=1.0` and append a `stop_sequences=["Here is the"]` parameter to the API request call.
B. Pass `{"role": "user", "content": "Return JSON only: {"}` at the beginning of the `messages` array.
C. Insert `{"role": "system", "content": "JSON_MODE=true"}` directly into the top of `messages` list.
D. Pre-fill `{"role": "assistant", "content": "{"}` in `messages`, then parse `"{" + response.content[0].text`.

---

**4.** `[task 6.1 · chain-of-thought for multi-step reasoning]` A prompt asks Claude to compute a multi-step loan eligibility decision (income ratio, credit history weight, and collateral value combined into one verdict) and return only the final approve/deny word. Reviewers notice the verdicts are inconsistent across near-identical applicants. What change is likely to improve reasoning consistency?

A. Instruct Claude to articulate intermediate reasoning inside `<thinking>` tags before outputting the verdict.
B. Instruct Claude to skip explanation entirely and output a single bare verdict token to minimize cost.
C. Set `max_tokens: 1` on the request so the model is physically constrained to emitting only one word.
D. Combine the financial metrics into a pre-computed external formula passed directly in the user prompt.

---

**5.** `[task 6.1 · role instructions vs. worked demonstration]` A drafting assistant's system prompt states "write concise, formal replies" but the outputs keep coming back casual and wordy despite the instruction being restated in every session. What is the most likely gap in the current approach?

A. The system prompt is treated as the wrong location for style guidance, which is assumed to belong only in the user turn.
B. The prompt describes the style abstractly but never shows a worked example of concise, formal writing to match.
C. The word "concise" is being interpreted overly literally, as a request for replies of a single short sentence.
D. The session has grown long enough to exceed the context window, pushing the original instruction out of view.

---

**6.** `[task 6.1 · negative instruction reframed positively]` A prompt tells Claude "do not use bullet points" for a narrative summary feature, yet outputs keep drifting back into bulleted lists whenever the input material itself contains lists. What phrasing adjustment is most likely to reduce this drift?

A. Restate the negative instruction in stronger language, written in all capital letters at the very end.
B. Remove the negative formatting rule entirely and rely on Claude's default paragraph formatting.
C. Replace the prohibition with a positive instruction describing the desired flowing prose paragraphs.
D. Move the negative constraint out of the system prompt and append it to every individual user turn.

---

**7.** `[task 6.2 · system prompt vs. user message placement]` A customer-support integration currently sends the company's refund policy, tone guidelines, and escalation rules inside every user message, right alongside that turn's customer question, for every single request. What placement change better matches how these two kinds of content are meant to be used?

A. Keep everything in the user message but move the customer's question to the very first line instead of the last one.
B. Split the policy content evenly between the system prompt and the user message so token usage balances out evenly.
C. Move the customer's question into the system prompt instead, so it persists across the whole ongoing conversation.
D. Move the stable policy and tone content into the system prompt, leaving only the question in the user message.

---

**8.** `[task 6.2 · long conversation context management]` A multi-hour support chat has grown to 80 turns. The team wants to keep the conversation running without hitting the context window limit, while making sure the original system instructions and the customer's opening problem statement stay available to the model. What approach fits both constraints?

A. Summarize or drop middle turns while keeping the system prompt and opening turn intact.
B. Truncate the system prompt itself once turn count passes 50 to reduce fixed token cost.
C. Restart a brand-new conversation with no history whenever turn counts cross a threshold.
D. Send the full 80-turn history on every request and rely on a larger context-window model.

---

**9.** `[task 6.2 · multimodal image content block]` An engineer needs Claude to inspect a screenshot the user just uploaded as a PNG file and describe any visible layout bugs. The image bytes are already base64-encoded in the client. How should this image be included in the request?

A. As a plain-text content block containing the base64 string, prefixed with a short note that it represents image data.
B. As a system prompt field named `image_data`, set once at the start of the conversation and never touched again.
C. As a content block with `type: "image"` and a `source` object carrying `type: "base64"`, the media type, and data.
D. As a `tool_result` block referencing a `tool_use_id` from an earlier turn, with the base64 string as its content.

---

**10.** `[task 6.2 · reference material inside XML with instruction after]` A research assistant prompt pastes three long PDFs' extracted text directly above the user's question, with no tags marking where the documents end and the question begins. Claude sometimes answers a question that was actually a sentence lifted from inside one of the documents. What structural fix addresses this?

A. Delete two of the three PDF documents entirely so fewer background sentences can cause prompt confusion.
B. Relocate the user's question into the system prompt string rather than inside the user message.
C. Format the user's question in all capital letters so the model prioritizes it visually across turns.
D. Wrap each source in `<document>` tags and place the user question after the closing tags.



---

**11.** `[task 6.3 · tool use for reliable parsing over string matching]` A financial compliance workflow needs Claude to evaluate a transaction and return whether it is approved, flagged for AML review, or denied. The current prompt asks for the word "APPROVED", "FLAGGED", or "DENIED" in the response, but downstream string parsing frequently breaks when Claude includes explanatory remarks or slight typos. What is the most reliable way to enforce this structured verdict?

A. Define a tool with a strict enum parameter for the decision and configure `tool_choice` to require its invocation.
B. Add a post-processing regex that searches for the first occurrence of the three keywords anywhere in the output string.
C. Set `max_tokens: 1` so Claude has only enough output budget to emit the first letter of the verdict word.
D. Wrap the request in a retry loop that resubmits the prompt whenever the returned string fails an exact equality match.

---

**12.** `[task 6.3 · validating structured output before use]` A billing agent calls a tool that returns a JSON object with an `amount_cents` integer field, but a malformed response once contained `amount_cents` as the string `"null"`, and the downstream charge code accepted it silently before failing later in a payment processor with an opaque error. What handling would have caught this earlier and more clearly?

A. Retry the same tool call automatically up to five times whenever any returned field value looks even slightly unusual or malformed.
B. Validate the tool's returned arguments against the schema, checking type and required fields, right after the call returns.
C. Log the raw JSON response to a file so a human can review it manually once a week during a routine check.
D. Increase the model's `max_tokens` so the tool call has more room to fully complete its output.

---

**13.** `[task 6.2 · system prompt separation with prompt caching in SDK]` A developer builds a multi-turn support assistant with 15,000 tokens of static policy documentation:

```python
system_policy = load_company_policies()  # ~15,000 tokens of static rules

def handle_user_message(history: list[dict], user_input: str) -> str:
    messages = history + [{"role": "user", "content": f"{system_policy}\n\nUser Question: {user_input}"}]
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=messages,
    )
    return response.content[0].text
```

As dialogue turns accumulate, latency and token costs explode because `system_policy` is re-sent in every `user` turn. Which refactoring achieves maximum token efficiency and latency reduction?

A. Pass `system_policy` into top-level system parameter and duplicate it in every user turn as an explicit fallback.
B. Compress `system_policy` using zlib and instruct Claude to decode it dynamically within a custom tool execution.
C. Set `system=[{"type": "text", "text": system_policy, "cache_control": {"type": "ephemeral"}}]` and clean `messages`.
D. Retain `system_policy` inside the user turn but set `cache_control: {"type": "ephemeral"}` on volatile message turns.

---

**14.** `[task 6.3 · structured output extraction via tool_choice forcing in SDK]` A developer builds an automated triage pipeline that must extract entities from support emails into a typed schema:

```python
tools = [
    {
        "name": "record_triage_decision",
        "description": "Record triage category and urgency rating.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["billing", "technical", "security"]},
                "urgency": {"type": "integer", "minimum": 1, "maximum": 5}
            },
            "required": ["category", "urgency"]
        }
    }
]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=512,
    tools=tools,
    messages=[{"role": "user", "content": email_text}],
    tool_choice={"type": "auto"}
)
```

In production, Claude occasionally outputs conversational analysis in prose instead of calling `record_triage_decision`. Which configuration change deterministically guarantees that Claude executes the extraction tool?

A. Set `tool_choice={"type": "tool", "name": "record_triage_decision"}` to enforce calling that exact tool signature.
B. Set `tool_choice={"type": "any"}` to require a tool call, and define a secondary regex parser for free-form prose.
C. Append `"Invoke record_triage_decision exclusively"` to the user message while leaving `tool_choice` set to `"auto"`.
D. Set `temperature=0.0` on the API call and remove parameter descriptions from `input_schema` to reduce token spread.

---

**15.** `[task 6.3 · defensive validation of structured tool inputs in Python]` An agent executes bank wire transfers via a tool call. The application defines a Pydantic schema for validation:

```python
from pydantic import BaseModel, Field, ValidationError

class WireTransferSchema(BaseModel):
    recipient_iban: str = Field(min_length=15, max_length=34)
    amount_cents: int = Field(gt=0)
    currency: str = Field(pattern="^[A-Z]{3}$")

def process_agent_turn(messages: list[dict]) -> dict:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=[wire_tool_def],
        messages=messages
    )
    for block in response.content:
        if block.type == "tool_use":
            # Validation logic
```

When `block.type == "tool_use"` arrives, how should the application validate arguments and handle schema violations defensively?

A. Execute transfer queries directly and catch database driver constraint exceptions inside backend persistence code.
B. Validate `block.input` via `WireTransferSchema` and return a `tool_result` with `is_error=True` if `ValidationError` is raised.
C. Catch `ValidationError` and immediately raise an unhandled exception to terminate the Python application runtime.
D. Silently coerce invalid argument values to hardcoded fallback defaults before invoking the financial transaction.


