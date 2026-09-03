# CCDV-F Miss Remediation — 12 items

**Built from:** gap-coverage-drill misses on items **1, 4, 6** (2026-09-03).

**Diagnosis.** Items 4 and 6 are both objective 5.1 — the current request
surface for model options (what each model generation removed, and which
dial lives where). Item 1 is objective 1.2, the harness-vs-deployment axis
across the four ways to build an agent. Both are areas where the 245-item
bank has zero coverage, so a first-pass miss is expected; the risk is that
the *wrong* version is what's in recall.

**Two of the three misses were multi-response** (you took item 13, the third
Select TWO, correctly). Four items here are multi-response for that reason.
Technique: judge each option **independently as true/false** against the
stem, then pick the two that survive — do not rank the four against each
other and take the top pair.

**Deliberately not a re-ask.** None of these repeats items 1, 4 or 6. They
test the discriminations *next to* those facts — the boundaries where the
rule you just learned stops applying, which is where a recognition-only fix
falls over.

**Coverage:** 5.1 (x6), 5.4, 1.1, 1.2 (x4).
Key sealed in `miss-remediation-drill-key.md`.

---

**1.** `[task 5.1 · omitting the thinking parameter]` A service sends no `thinking` parameter at all. On its original model it reasons before answering; after the team repins to a different current model, the same request answers immediately and visibly shallower, with no error raised and no code changed. What accounts for that?

A. The second model needs `budget_tokens` supplied before any reasoning is performed.
B. The second model reasons only once `output_config.effort` is set to `high` or above.
C. Omitting `thinking` leaves some current models adaptive and others with none.
D. The second model returns reasoning in a separate block that the client is discarding.

---

**2.** `[task 5.1 · what current models removed]` A request written for an older model is repinned to `claude-opus-5` and now fails validation before generation. It sets `temperature: 0.2`, `top_p: 0.9`, `max_tokens: 4096`, and ends with an assistant message whose content is `{`. Which TWO of these are rejected on this model? (Select TWO)

A. The sampling parameters `temperature` and `top_p`.
B. `max_tokens: 4096`, which is capped lower once thinking is active.
C. The absence of a `thinking` block, which current models require to be explicit.
D. The trailing assistant message, prefill no longer being accepted.

---

**3.** `[task 5.1 · where effort lives]` An engineer adds `effort: "xhigh"` as a top-level request field and observes no behavioural change, then reads that the value they wanted is close to the default anyway. What is actually true about this dial?

A. It sits top-level but takes effect only alongside `thinking: {"type": "adaptive"}`.
B. It sits inside `output_config`, spans `low` through `max`, and defaults to `high`.
C. It sits inside `thinking`, having replaced the older `budget_tokens` field in place.
D. It sits inside `output_config` but accepts only `low`, `medium` and `high` here.

---

**4.** `[task 5.1 · thinking display]` A team streams responses to end users. After repinning to a current model they see a long pause followed by the answer, where a summary of the model's reasoning used to appear. Token billing is unchanged. What happened, and what restores the previous behaviour?

A. Reasoning now runs without being billed and cannot be surfaced to clients again.
B. The stream emits reasoning after the answer now, so the client must buffer and reorder.
C. Adaptive thinking suppresses summaries; reverting to a fixed budget brings them back.
D. The display default became omitted; set `thinking: {"display": "summarized"}` explicitly.

---

**5.** `[task 5.1 · fast mode eligibility]` A team wants fast mode for a latency-sensitive route. They currently run `claude-opus-4-7` on Amazon Bedrock. Which assessment of their options is accurate?

A. It is unavailable on both counts — removed on 4.7, and not offered on third-party platforms.
B. It works on 4.7, but must be requested through the Bedrock Mantle client rather than the beta endpoint.
C. It needs only a move to the beta messages endpoint; the hosting platform makes no difference here.
D. It is available on 4.7 via Bedrock, though the premium rate is billed at first-party prices.

---

**6.** `[task 5.1 · fast mode operational consequences]` A team puts fast mode on `claude-opus-5` behind a feature flag and wants to know what changes operationally, beyond the price per token. Which TWO consequences are real? (Select TWO)

A. Prompt-cache hits carry over unchanged when the flag flips, the model being identical.
B. Fast mode draws on a rate limit separate from standard requests to the same model.
C. Toggling `speed` invalidates the prompt cache, so the request after a flip pays a write.
D. Requests fall back to standard speed automatically once the fast-mode quota is spent.

---

**7.** `[task 5.4 · picking the right lever per route]` An overnight enrichment job processes 40,000 records, is not needed until morning, and is over budget. A separate live chat endpoint is within budget but users call it sluggish. Which pairing of levers fits the two routes?

A. Fast mode for the overnight job, and the Batch API for the chat endpoint.
B. The Batch API for both routes, it being the largest single discount available.
C. Higher effort on the overnight job, and Priority Tier for chat on `claude-opus-5`.
D. Batch for the overnight job; fast mode or lower effort for the chat endpoint.

---

**8.** `[task 1.2 · when managed deployment is the requirement]` A two-person team wants an agent that runs nightly without them operating a scheduler, keeps a workspace across the turns of a long session, and pins every run to a reviewed configuration. They have no infrastructure they want to maintain. Which surface fits?

A. The Claude Agent SDK, driven from a cron entry on a small always-on VM they provision.
B. Managed Agents — scheduled deployments fire sessions, and each session carries a container.
C. The SDK tool runner, with the nightly trigger supplied by their CI provider's scheduler.
D. A manual loop deployed as a serverless function, with workspace state kept in object storage.

---

**9.** `[task 1.2 · identifying the Agent SDK]` A developer wants a coding agent that reads and edits files, runs shell commands, and searches a repository, without writing any of those tools themselves. They intend to run it on hardware they already own. Which option matches?

A. The Messages API with the code execution tool, which gives file and shell access server-side.
B. Managed Agents, file and bash tools existing only inside an Anthropic-hosted container.
C. The Claude Agent SDK — a separate package shipping built-in file, bash and search tools.
D. The SDK tool runner, whose built-in tool set covers file and shell operations already.

---

**10.** `[task 1.2 · what the tool runner adds over a manual loop]` A team already owns a working manual `tool_use` loop and is unconvinced the SDK tool runner would buy them anything. Which capability is a genuine argument in its favour?

A. Per-turn hooks that gate execution, log calls, and intercept errors.
B. Built-in file and bash tools, removing the need for them to define their own.
C. Managed deployment, so that the loop stops running on their own infrastructure.
D. Server-side compaction, which the Messages API does not otherwise make available.

---

**11.** `[task 1.1 · whether to build an agent at all]` A team proposes an agent to extract a title and an ISO date from each of 200,000 uploaded PDFs. The output schema is fixed and the same two fields are wanted every time. What does the decision framework say?

A. Build the agent — the volume justifies the orchestration overhead it carries.
B. Build the agent, but give it one tool so that the loop terminates quickly.
C. Use a workflow, since an agent cannot be combined with batch processing.
D. Stay at a single call — the task is fully specifiable, nothing to explore.

---

**12.** `[task 1.2 · harness and deployment stated precisely]` A platform team is documenting the four ways to build an agent along two axes: who supplies the harness, and who supplies the deployment. Which TWO statements belong in that document? (Select TWO)

A. The Agent SDK and the tool runner both supply a harness while leaving hosting to the caller.
B. Managed Agents supplies the harness, and the caller supplies the container tools run in.
C. Managed Agents is the only one of the four that supplies both harness and deployment.
D. A manual loop supplies the deployment, and the Messages API supplies the harness.

---
