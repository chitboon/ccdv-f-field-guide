# CCDV-F Domain Drill — Domain 7: key and rationales

Grade in one deferred pass. For every miss, note which it was: didn't know
it, misread the item, or picked the plausible-but-soft option.

---

**1. B** — The user is typing the malicious instruction directly into the live conversation, attempting to override the system prompt in that same input channel — that's direct injection. It didn't arrive through a tool result (A), and the scenario is about the attempted override itself, not the refund tool's invocation or the agent's permission grants (C, D). *(task 7.1; concept: direct_prompt_injection; item `d7d-01`)*

---

**2. B** — The instructions were planted inside retrieved page content and the model followed them as commands, which is the defining pattern of indirect injection; the attacker never spoke to the model directly (A), and neither `tool_choice` configuration nor request throttling describes what happened (C, D). *(task 7.1; concept: indirect_prompt_injection; item `d7d-02`)*

---

**3. C** — Granting owner-level access to the entire Drive when the task only ever touches one folder is exactly what least privilege forbids: access should match the narrowest scope the task needs. Defense in depth is about layering controls, data minimization is about how much retrieved content gets used, and separation of duties is about who configures what — none of those is the issue named here. *(task 7.1; concept: least_privilege_scoping; item `d7d-03`)*

---

**4. C** — Printing the secret into logs and then committing that line exposes the raw key to anyone with log or repository access, undermining whatever key-management controls exist elsewhere. The commit message's clarity, `print`'s performance, and the variable's naming are all real but unrelated to the actual exposure. *(task 7.1; concept: secrets_in_logs_and_commits; item `d7d-04`)*

---

**5. D** — A destructive action against a production resource is the case guardrails exist for: routing it through required human approval would have caught the target mismatch before deletion. Rate limiting only throttles frequency, an audit log only helps after the fact, and content filtering addresses generated text, not tool actions. *(task 7.2; concept: human_review_high_risk_action; item `d7d-05`)*

---

**6. A** — Uncapped volume and unscreened output are two separate failure modes needing two separate guardrails: per-user rate limiting bounds request volume, and output content filtering catches policy-violating responses. A bigger context window, a cheaper model, and more few-shot examples are all performance or cost tweaks that leave both original problems in place. *(task 7.2; concept: rate_limiting_and_content_filtering; item `d7d-06`)*

---

**7. D** — Validating a proposed tool call and rejecting it before it ever runs is the definition of a pre-tool-use hook; this is what stops the destructive command from executing at all. A post-tool-use hook would only see the output after the shell already ran, and neither prompt caching nor subagent routing describes inspecting a command for danger. *(task 7.3; concept: pre_tool_use_hook; item `d7d-07`)*

---

**8. A** — Because the tool trusts whatever `customer_id` the model supplies instead of enforcing the logged-in session's identity, the agent can be manipulated into querying another customer's records under the same broad credential — exactly the identity-boundary failure the scenario sets up. A connection pool limit, query latency, and an inability to serve the logged-in customer are unrelated side effects, not the risk this gap creates. *(task 7.3; concept: identity_scoped_data_access; item `d7d-08`)*
