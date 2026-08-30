# CCDV-F Domain Drill — Domain 6: Prompt and Context Engineering

12 items, one correct answer each. Untimed. Answer all 12 first, then grade
against the key in one pass — item by item, reading each rationale,
including the ones you got right. This is a scenario-based drill, not a
recall check: every stem carries a concrete situation you must reason about.
Suggested sittings: 1-6, 7-12 (two ~10-minute sessions), or all 12 in one
sitting.

---

**1.** `[task 6.1 · XML section delimiting]` A 4,000-word system prompt mixes a product return-policy reference document and behavioral instructions in one undifferentiated block of prose. Claude has started quoting return-policy line items back to customers as if they were rules the agent itself must obey. What restructuring most directly fixes this?

A. Shorten the reference document by roughly half so the combined system prompt consumes noticeably fewer tokens on every request.
B. Wrap the reference document in `<context>` tags and the behavioral rules in `<instructions>` tags for clarity.
C. Move the entire block, unchanged, from the system prompt into the first user turn of every single new conversation.
D. Ask Claude in a later follow-up turn to disregard the return-policy wording it already quoted, going forward.

---

**2.** `[task 6.1 · few-shot pattern demonstration]` A support-ticket tagging prompt describes the target format only in prose: "Reply with a comma-separated list of category tags, lowercase, no spaces after commas." Outputs still vary — sometimes capitalized, sometimes with spaces, sometimes as a bulleted list. What change is most likely to lock in the exact pattern?

A. Repeat the same prose formatting instruction three separate times in a row within the system prompt itself.
B. Move the same exact formatting instruction out of the system prompt and into the user turn on every request instead.
C. Add two or three input-ticket/output-tag-list example pairs showing the exact formatting live in the prompt.
D. Increase `max_tokens` so truncation can no longer plausibly be the cause of these malformed comma-separated tag lists.

---

**3.** `[task 6.1 · assistant message pre-fill]` A code-review bot must always reply with a raw JSON object and nothing else, but Claude keeps prefacing replies with "Here's the review:" before the JSON starts, breaking a downstream parser that expects the very first character to be `{`. Which technique addresses this directly?

A. Add a stop sequence on the exact string "Here's the review:" so generation halts right before it gets written.
B. Raise the sampling temperature so the model varies its phrasing and, with luck, eventually drops the preface.
C. Ask the user to strip everything before the first `{` character in their own client-side parsing code, ticket by ticket.
D. Start the assistant turn with the pre-filled text `{`, so the reply continues on as JSON.

---

**4.** `[task 6.1 · chain-of-thought for multi-step reasoning]` A prompt asks Claude to compute a multi-step loan eligibility decision (income ratio, credit history weight, and collateral value combined into one verdict) and return only the final approve/deny word. Reviewers notice the verdicts are inconsistent across near-identical applicants. What change is likely to improve reasoning consistency?

A. Instruct Claude to reason through each factor step by step before stating the final verdict, rather than jumping straight to the word.
B. Instruct Claude to skip explanation entirely and answer in a single token to save output cost.
C. Lower `max_tokens` to 1 so the model is physically limited to just the verdict word.
D. Replace the loan factors with a single combined numeric score computed outside the prompt.

---

**5.** `[task 6.1 · role instructions vs. worked demonstration]` A drafting assistant's system prompt states "write concise, formal replies" but the outputs keep coming back casual and wordy despite the instruction being restated in every session. What is the most likely gap in the current approach?

A. The system prompt is treated as the wrong location for style guidance, which is assumed to belong only in the user turn.
B. The prompt describes the style abstractly but never shows a worked example of concise, formal writing to match.
C. The word "concise" is being interpreted overly literally, as a request for replies of a single short sentence.
D. The session has grown long enough to exceed the context window, pushing the original instruction out of view.

---

**6.** `[task 6.1 · negative instruction reframed positively]` A prompt tells Claude "do not use bullet points" for a narrative summary feature, yet outputs keep drifting back into bulleted lists whenever the input material itself contains lists. What phrasing adjustment is most likely to reduce this drift?

A. Restate the identical negative instruction in stronger language, written in all capital letters, at the very end.
B. Remove the instruction entirely and rely on the model's own default formatting choices for the summary.
C. Replace the prohibition with a positive instruction describing the desired form, such as flowing prose paragraphs.
D. Move the same instruction out of the system prompt and repeat it at the end of every single user message.

---

**7.** `[task 6.2 · system prompt vs. user message placement]` A customer-support integration currently sends the company's refund policy, tone guidelines, and escalation rules inside every user message, right alongside that turn's customer question, for every single request. What placement change better matches how these two kinds of content are meant to be used?

A. Keep everything in the user message but move the customer's question to the very first line instead of the last one.
B. Split the policy content evenly between the system prompt and the user message so token usage balances out evenly.
C. Move the customer's question into the system prompt instead, so it persists across the whole ongoing conversation.
D. Move the stable policy and tone content into the system prompt, leaving only the question in the user message.

---

**8.** `[task 6.2 · long conversation context management]` A multi-hour support chat has grown to 80 turns. The team wants to keep the conversation running without hitting the context window limit, while making sure the original system instructions and the customer's opening problem statement stay available to the model. What approach fits both constraints?

A. Summarize or drop the oldest middle turns, while retaining the system prompt and the conversation's opening turn fully intact.
B. Truncate the system prompt itself once the turn count passes 50, since it is the largest fixed line-item cost.
C. Start a brand-new conversation with no prior context every time the turn count crosses a fixed threshold.
D. Send the full 80-turn history on every request and rely on a larger context-window model to absorb the growth.

---

**9.** `[task 6.2 · multimodal image content block]` An engineer needs Claude to inspect a screenshot the user just uploaded as a PNG file and describe any visible layout bugs. The image bytes are already base64-encoded in the client. How should this image be included in the request?

A. As a plain-text content block containing the base64 string, prefixed with a short note that it represents image data.
B. As a system prompt field named `image_data`, set once at the start of the conversation and never touched again.
C. As a content block with `type: "image"` and a `source` object carrying `type: "base64"`, the media type, and data.
D. As a `tool_result` block referencing a `tool_use_id` from an earlier turn, with the base64 string as its content.

---

**10.** `[task 6.2 · reference material inside XML with instruction after]` A research assistant prompt pastes three long PDFs' extracted text directly above the user's question, with no tags marking where the documents end and the question begins. Claude sometimes answers a question that was actually a sentence lifted from inside one of the documents. What structural fix addresses this?

A. Delete two of the three source documents entirely so only one remains available to get confused with the question.
B. Move the question up into the system prompt so it gets processed before any of the document text.
C. Ask the user to retype their question in all capital letters so that it visually stands out from the rest.
D. Wrap each document in `<document>` tags and place the actual user question, clearly marked, after the closing tags.

---

**11.** `[task 6.3 · tool use for reliable parsing over string matching]` A pipeline currently asks Claude to answer with the word "APPROVED" or "REJECTED" as free text, then a downstream script does `if "APPROVED" in response`. This misfires when Claude writes an explanation that happens to contain the word "REJECTED" while ultimately approving the request. What is the more robust fix?

A. Define a tool with a strict schema, such as a boolean `approved` field, so the verdict is parsed from call arguments.
B. Tell Claude to only ever write the single word "APPROVED" or "REJECTED" with absolutely nothing else in the reply.
C. Switch the string match to check `response.startswith("APPROVED")` instead of a substring search anywhere in the text.
D. Ask Claude to wrap its verdict word in double asterisks so the script can search for `**APPROVED**` instead of plain text.

---

**12.** `[task 6.3 · validating structured output before use]` A billing agent calls a tool that returns a JSON object with an `amount_cents` integer field, but a malformed response once contained `amount_cents` as the string `"null"`, and the downstream charge code accepted it silently before failing later in a payment processor with an opaque error. What handling would have caught this earlier and more clearly?

A. Retry the same tool call automatically up to five times whenever any returned field value looks even slightly unusual or malformed.
B. Validate the tool's returned arguments against the schema, checking type and required fields, right after the call returns.
C. Log the raw JSON response to a file so a human can review it manually once a week during a routine check.
D. Increase the model's `max_tokens` so the tool call has more room to fully complete its output.
