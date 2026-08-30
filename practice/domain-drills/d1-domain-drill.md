# CCDV-F Domain Drill — Domain 1: Agents and Workflows

16 items, one correct answer each. Untimed. Answer all 16 first, then grade
against the key in one pass — item by item, reading each rationale,
including the ones you got right. This drill covers agent architecture,
agent construction with Claude, and agent patterns and frameworks; every
stem carries a concrete scenario you must reason about rather than a bare
recall question. Suggested sittings: 1-8 then 9-16, or 1-4 / 5-10 / 11-16
across three shorter sessions.

---

**1.** `[task 1.1 · autonomous loop vs fixed chain]` A travel-booking system either (a) always calls `search_flights`, then `book_flight`, then `send_confirmation` in that fixed order, or (b) calls Claude in a `tool_use` loop that decides after each response whether to search again, book, or stop. What single property distinguishes (b) as an agent rather than a fixed workflow?

A. It calls more tools per request, since agents are expected to invoke every available tool before finishing.
B. It reads each tool's output and picks its own next action, while the fixed sequence just runs the same three calls in order every time regardless of what came back.
C. It uses a lower temperature setting, since the fixed workflow needs a higher temperature to vary its output across runs.
D. It runs asynchronously, since agents must rely on the Batches API while the fixed workflow stays synchronous throughout.

---

**2.** `[task 1.1 · stop_reason interpretation]` An agent loop receives a Messages API response with `stop_reason: "tool_use"` and a `tool_use` block for `get_weather`; the following turn returns `stop_reason: "end_turn"` with only text content. How should the loop's control flow treat these two values?

A. Treat both values identically, since `stop_reason` only affects billing metadata and never changes what the loop does next.
B. Stop the loop on `tool_use` because the model is asking for permission, and keep looping only once `end_turn` appears.
C. Discard the response and resend the identical request whenever `stop_reason` is `tool_use`, treating it as a malformed reply.
D. Execute the tool on `tool_use` and return its `tool_result` to the model; once `end_turn` shows up instead, stop looping and hand the text back to the user.

---

**3.** `[task 1.1 · context window trimming]` A research agent's loop has run 40 tool-call turns, and the growing transcript of full `tool_result` payloads is approaching the model's context window limit. The engineer wants the loop to keep running without losing its ability to follow the original instructions. What should the context-management strategy preserve?

A. Keep the system prompt and recent turns intact while summarizing or dropping older tool_result content to reclaim space.
B. Keep every full tool_result verbatim without ever trimming it, and instead shorten or simplify the system prompt itself once the loop has been running for many turns.
C. Discard the system prompt entirely after the very first turn, on the theory that the model no longer needs any instructions once its tools begin returning data.
D. Replace all prior turns with one hardcoded placeholder so transcript length never grows.

---

**4.** `[task 1.1 · tool_result is_error recovery]` An agent calls a `get_inventory` tool for SKU `X-771` and receives a `tool_result` block with `"is_error": true` and content `"warehouse service unreachable"`. The loop appends this tool_result to the conversation and calls the API again for the next turn. What should the model do with that turn?

A. Ignore the `is_error` flag entirely and treat the returned string as normal inventory data so the original plan continues unchanged.
B. Terminate the entire session immediately, since any `tool_result` carrying `is_error: true` means the conversation can no longer continue safely.
C. Read the error content and choose a recovery step: retry, switch tools, or report the failure to the user.
D. Resend the identical tool_use request in a loop until the `is_error` flag disappears, without changing any of its parameters.

---

**5.** `[task 1.2 · tool interface design]` A developer defines a `cancel_order` tool whose only parameter is `id`, with no description, and whose implementation returns either a plain `"OK"` string or an unhandled exception. Agents calling it frequently pass the wrong ID format and can't tell why cancellations silently fail. What should the tool definition add so Claude can reason about correct usage?

A. A shorter tool name, since Claude is believed to select tools by matching name length to the request.
B. A higher `max_tokens` setting on the request, under the mistaken assumption that tool-selection accuracy scales with the output budget.
C. Removal of the `id` parameter entirely, since tools with fewer parameters are assumed to always be easier to call.
D. A clear description of the `id` format and the values it accepts, together with structured success and error responses the model can actually inspect and act on.

---

**6.** `[task 1.2 · structured tool error signals]` A payments tool currently returns the same generic string, `"error"`, whether a card was declined, the amount was invalid, or the service timed out. An agent calling this tool cannot decide whether to retry, ask the customer for a new card, or escalate. What change to the tool's output would let the model choose correctly?

A. Distinct, structured error content per failure type so the model can distinguish declines from invalid input from timeouts.
B. A single boolean `is_error` field with no accompanying message at all, on the theory that the model only ever needs to know success or failure.
C. Logging failures server-side only, since surfacing error detail to the model risks leaking payment data.
D. A fixed retry count baked into the tool itself, so the model never sees failures to reason about.

---

**7.** `[task 1.2 · system prompt role scoping]` A customer-support agent's system prompt currently only says "You are a helpful assistant." In production it answers unrelated coding questions, invents refund policies, and never mentions the two tools it has access to. What should the system prompt add to keep the agent's behavior scoped to its intended role?

A. A longer greeting message, since users are believed to judge scope from the tone of the assistant's first sentence rather than any instructions.
B. A list of banned words, since restricting vocabulary alone is thought to be enough to stop an agent answering off-topic questions.
C. The agent's specific role, boundaries on what it should and shouldn't answer, and guidance on when to use its tools.
D. A higher `temperature` value, since more randomness is claimed to make topic selection more consistent.

---

**8.** `[task 1.2 · tool_choice forcing]` A form-filling agent has three tools available, and the developer wants the very first response to always call `extract_fields` rather than let Claude decide whether a tool is needed at all. Leaving `tool_choice` at its default sometimes produces a plain text reply instead of the desired call. What should the request specify instead?

A. A longer description written for every other tool, so the model avoids them by comparison rather than by direct instruction.
B. A `tool_choice` forcing `extract_fields` by name instead of leaving the model free to pick or skip tools.
C. A `stop_sequence` matching the tool's name, on the theory that stop sequences control which tool the model is permitted to call.
D. Removing the other two tools from the request permanently, so fewer tools force the intended one to be picked.

---

**9.** `[task 1.2 · multi-turn loop history]` A developer's agent loop sends a request, receives a `tool_use` block, executes the tool, and then starts an entirely new conversation containing only that single tool's result before asking the next question. The agent keeps repeating earlier steps because it never remembers what it already tried. What is the implementation error?

A. Each turn must append its own `tool_result` onto the growing conversation history, instead of restarting that history from just a single isolated result every time.
B. The loop should switch to the Batches API, since only batch requests can retain multi-turn memory.
C. The tool should be called twice per turn, since duplicate calls are what preserve memory across turns.
D. The system prompt must be resent as a `tool_result` block, since that is the only field read for memory.

---

**10.** `[task 1.2 · parallel tool_use blocks]` A trip-planning request returns a single Claude response containing two separate `tool_use` blocks: one for `check_flight_prices` and one for `check_hotel_prices`. The developer's loop executes only the first block and sends its `tool_result` back, dropping the second entirely. What must the loop do to handle this response correctly?

A. Reject the response outright, on the theory that a single Claude turn is only ever allowed to request one tool call at a time.
B. Merge both tool calls into one `tool_result` block, since the API accepts only a single result per turn.
C. Execute every `tool_use` block in the response and return a matching `tool_result` for each one before continuing.
D. Call only the first tool, since unused calls are dropped automatically by the runtime itself.

---

**11.** `[task 1.3 · orchestrator-workers pattern]` A code-migration project uses one Claude call to break a large repository into per-file migration subtasks, dispatches each subtask to a separate Claude call that handles just that file, and then combines the individual diffs into one pull request. Which multi-agent pattern does this describe?

A. Prompt chaining: a fixed sequence of steps where each step's output feeds directly into the very next step's input stage.
B. Orchestrator-workers: a coordinator decomposes the task, delegates subtasks, and synthesizes the workers' results.
C. Evaluator-optimizer: one agent produces a draft while a second, entirely separate agent scores it against a quality bar.
D. Single linear agent: one continuous tool_use loop handling the whole repository without any subtask delegation.

---

**12.** `[task 1.3 · evaluator-optimizer pattern]` A marketing-copy pipeline has one Claude call draft an ad headline, a second Claude call score that headline against a rubric and return specific feedback, and the first call revise the headline using that feedback — repeating until the score clears a set threshold. Which pattern is this?

A. Orchestrator-workers: a coordinator splits the headline task into independent subtasks for parallel workers to draft separately.
B. Routing: a classifier reads the headline first and dispatches it to whichever specialized model best fits its topic.
C. Parallelization: several independent drafts of the headline are generated at once and the best one is chosen afterward by vote.
D. Evaluator-optimizer: a generator and a separate critic loop together until the output clears a quality bar.

---

**13.** `[task 1.3 · single agent vs orchestration]` A team is building a tool that looks up one customer record and drafts one reply email, using a single system prompt and two tools. A colleague proposes splitting this into an orchestrator plus three specialized subagents before any performance problem has appeared. What should guide the decision here?

A. Multi-agent orchestration should always be the default, on the theory that more agents can only ever improve quality.
B. Subagents are required whenever more than one tool is defined, no matter how simple the overall task is.
C. A single linear agent already covers this task's full scope; orchestration is worth adding only once real complexity or genuinely independent subtasks appear.
D. The orchestrator pattern must be used because a single agent is assumed incapable of calling multiple tools within one session.

---

**14.** `[task 1.3 · routing pattern]` A support system's first Claude call reads an incoming ticket and outputs only a category label — "billing," "technical," or "account" — and a second stage then sends the ticket to whichever specialized subagent handles that category. Which pattern does this two-stage design implement?

A. Routing: an initial classification step directs the input to the specialized subagent suited to that category.
B. Evaluator-optimizer: the category label is treated as though it were a quality score that the second stage optimizes against.
C. Orchestrator-workers: the first call splits the ticket into independent pieces for parallel handling.
D. Prompt chaining: each stage's entire output text is appended verbatim as the next stage's whole input prompt.

---

**15.** `[task 1.3 · prompt chaining vs autonomous agent]` A document pipeline always runs three fixed Claude calls in the same order — extract entities, then translate them, then format a summary — with no step ever deciding to skip, repeat, or reorder based on what a prior step returned. Which category best describes this design, as distinct from an autonomous agent loop?

A. Orchestrator-workers: a coordinator dynamically delegating subtasks to workers chosen based on the document's actual content.
B. Evaluator-optimizer: a critic stage rejecting outputs and looping the extraction step until quality noticeably improves.
C. An autonomous agent loop: each step deciding on its own whether to repeat itself or stop early.
D. Prompt chaining: a predetermined sequence of steps rather than a loop that adapts its own next action.

---

**16.** `[task 1.3 · parallelization / sectioning pattern]` A content-moderation task sends the same flagged post to three independent Claude calls at once, each voting "allow" or "remove," and a simple majority-vote rule decides the final outcome rather than any single call's answer. Which pattern does running these calls simultaneously and combining their outputs represent?

A. Routing: a classifier reads the post and dispatches it to exactly one subagent that owns all moderation decisions.
B. Parallelization: independent calls run at once and their outputs get aggregated, here by simple vote.
C. Orchestrator-workers: a coordinator splits the single post into three separate sub-documents for each worker to handle.
D. Evaluator-optimizer: one call drafts a decision while the other two critique it across several looped revisions.
