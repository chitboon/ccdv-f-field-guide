# CCDV-F Domain Drill — Domain 1: key and rationales

Grade in one deferred pass. For every miss, note which it was: didn't know
it, misread the item, or picked the plausible-but-soft option.

---

**1. B** — Deciding the next action from what a tool returned, rather than executing a preset order, is exactly what separates an agent loop from a fixed workflow. Tool count, temperature, and the Batches API describe implementation details unrelated to that control-flow distinction. *(task 1.1; concept: autonomous_loop_vs_chain; item `d1d-01`)*

---

**2. D** — `tool_use` means Claude is asking the loop to run a tool and expects a `tool_result` back; `end_turn` means the model considers its response complete and the loop should stop and hand the text to the user. Treating them as equivalent, reversed, or as an error signal all misread what `stop_reason` communicates. *(task 1.1; concept: stop_reason_interpretation; item `d1d-02`)*

---

**3. A** — Effective context management keeps the system prompt and the most recent turns intact so the agent still follows its original instructions, while trimming or summarizing older tool_result payloads to reclaim space. Shortening the system prompt, dropping it, or replacing history with a placeholder all destroy the instructions or the working memory the loop needs. *(task 1.1; concept: context_window_trimming; item `d1d-03`)*

---

**4. C** — `is_error: true` is a signal for the model to reason about, so the loop should let Claude choose a recovery step such as retrying, switching tools, or surfacing the failure to the user. Ignoring the flag, killing the session outright, or blindly resending the same request all fail to use the error content productively. *(task 1.1; concept: tool_result_is_error_recovery; item `d1d-04`)*

---

**5. D** — A clear parameter description plus structured, inspectable success and error responses is what lets Claude reason about correct calls and diagnose failures. Tool name length, a higher `max_tokens`, and removing the parameter don't address the missing description or the unhandled-exception behavior at all. *(task 1.2; concept: tool_interface_design; item `d1d-05`)*

---

**6. A** — Returning distinct, structured content per failure type is what lets the model tell a decline apart from invalid input or a timeout and pick the right recovery action. A single unlabeled boolean, server-only logging, or a fixed retry count all withhold the very detail the model needs to decide. *(task 1.2; concept: structured_tool_error_signals; item `d1d-06`)*

---

**7. C** — Defining the agent's role, its boundaries, and when to invoke its tools is what keeps behavior scoped; a generic "helpful assistant" line gives the model no basis for staying on-topic. A longer greeting, a banned-word list, and a higher temperature don't constrain scope or mention the available tools. *(task 1.2; concept: system_prompt_role_scoping; item `d1d-07`)*

---

**8. B** — Forcing `tool_choice` to name `extract_fields` guarantees that specific call instead of leaving the model free to reply with plain text. A longer description on other tools, a `stop_sequence`, and permanently removing tools are all indirect workarounds that don't reliably force the intended call. *(task 1.2; concept: tool_choice_forcing; item `d1d-08`)*

---

**9. A** — Each turn's `tool_result` must be appended to the running conversation so the model can see everything it already tried; restarting history from a single result is why the loop keeps repeating earlier steps. Switching to the Batches API, duplicating tool calls, or resending the system prompt as a tool_result don't fix the missing accumulated history. *(task 1.2; concept: multiturn_loop_append_results; item `d1d-09`)*

---

**10. C** — A single Claude turn can return multiple `tool_use` blocks, and the loop must execute each one and return a matching `tool_result` for every block before continuing. Rejecting the response, merging both calls into one result, or silently dropping the second block all mishandle a response that validly contains two requests. *(task 1.2; concept: parallel_tool_use_handling; item `d1d-10`)*

---

**11. B** — A coordinator call that decomposes the repository into per-file subtasks, delegates each to a worker call, and synthesizes the diffs is the orchestrator-workers pattern. Prompt chaining is a fixed linear sequence, evaluator-optimizer relies on a critic scoring a draft, and a single linear agent wouldn't delegate subtasks to separate calls at all. *(task 1.3; concept: orchestrator_workers_pattern; item `d1d-11`)*

---

**12. D** — A generator drafting the headline and a separate critic scoring it, looping until a quality bar is cleared, is the evaluator-optimizer pattern by definition. Orchestrator-workers splits a task into parallel subtasks, routing dispatches by category, and parallelization runs independent drafts at once rather than looping generator feedback. *(task 1.3; concept: evaluator_optimizer_pattern; item `d1d-12`)*

---

**13. C** — A single system prompt with two tools handling one lookup and one draft is already within a linear agent's scope; orchestration earns its overhead once independent subtasks or genuine complexity appear, not preemptively. Treating multi-agent design as always superior, tying it to tool count, or claiming a single agent can't call more than one tool are all incorrect generalizations. *(task 1.3; concept: single_agent_vs_orchestration; item `d1d-13`)*

---

**14. A** — A first call that emits only a category label, followed by dispatch to the subagent that owns that category, is the routing pattern. Evaluator-optimizer needs a critic looping on quality, orchestrator-workers decomposes a task into parallel pieces, and prompt chaining is a fixed sequence rather than a single classify-then-dispatch step. *(task 1.3; concept: routing_classification_pattern; item `d1d-14`)*

---

**15. D** — Three Claude calls always run in the same fixed order with no step deciding to skip, repeat, or reorder is prompt chaining, precisely because nothing adapts based on what a prior step returned. Orchestrator-workers and evaluator-optimizer both involve a step making a decision about subsequent steps, and an autonomous agent loop is defined by exactly the adaptive behavior this pipeline lacks. *(task 1.3; concept: prompt_chaining_vs_agent; item `d1d-15`)*

---

**16. B** — Three independent calls running at once on the same input, combined afterward by majority vote, is the parallelization (sectioning/voting) pattern. Routing sends input to exactly one subagent rather than three, orchestrator-workers would split the post into separate pieces instead of voting on the same one, and evaluator-optimizer requires a looped critique rather than a single simultaneous vote. *(task 1.3; concept: parallelization_sectioning_pattern; item `d1d-16`)*
