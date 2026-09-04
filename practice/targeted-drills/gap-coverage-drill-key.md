# CCDV-F Gap-Coverage Drill — Key and Rationales (11 items)

Grade in one pass after all 11 items. For each miss, mark which it was:
**didn't know it**, **misread the item**, or **knew the old behaviour**. That
third category matters most here — several items exist because the 245-item
bank drilled the pre-migration form of the same fact.

Item 8 needs both letters to count as a hit.

**Pruned 2026-09-04:** six items on untested API surface were removed after the
sitting. The `gap-NN` ids below are the original stable ids, so numbering here
jumps relative to them by design.

---

**1. C** — The tool runner (`client.beta.messages.tool_runner`) is harness-only: it drives the request/execute/loop cycle over tools you define, and you keep hosting. A is the closest wrong answer and worth understanding — the Claude Agent SDK is also harness-only and self-hosted, but it is a *separate product* that brings its own built-in Read/Write/Bash/Grep tool surface, so adopting it means changing the tool surface, not preserving it. B moves tool execution into an Anthropic-hosted per-session container, which is exactly the infrastructure change they ruled out. D keeps every line of loop code they wanted to stop maintaining. *(task 1.2; concept: harness_vs_deployment_split; item `gap-01`)*

---

**2. A** — Managed Agents has a mandatory two-step flow: create the Agent once, then reference its ID on every session. `model`, `system`, and `tools` are properties of the agent, and a session pins to an agent version. C inverts that and is the common first attempt — the session is the *run*, not the versioned config, and it does not accept those fields. B technically produces working sessions but discards the version-pinning the security review asked for, and `agents.create()` in the request path is the documented anti-pattern. D names the wrong product entirely. *(task 1.2; concept: agent_then_session_flow; item `gap-02`)*

---

**3. B** — A framework gives you graph/state/retry structure over the same `POST /v1/messages` contract; tool-use wire formats, token accounting, and context growth are unchanged underneath. C is the tempting one and the reason teams are disappointed: adopting a framework does not by itself solve context growth, and compaction/context-editing remain deliberate choices you make. A is false — these frameworks call the same API. D confuses the framework's declared structure with who decides the next step; an agent built on a graph is still model-directed at the decision points. *(task 1.3; concept: framework_changes_structure_not_contract; item `gap-03`)*

---

**4. C** — Caching is an exact prefix match, and the render order is `tools` -> `system` -> `messages`. A per-request timestamp inside the cached segment changes bytes on every call, so nothing matches. Moving volatile content after the last breakpoint fixes it. D is a genuine near-miss and worth being able to argue against: coarsening to the minute does produce hits for calls that happen to fall in the same minute, but it leaves a cache that silently misses at every boundary — a partial mitigation dressed as a fix. A misunderstands breakpoints: four of them do not create four independent chances to match, they mark cacheable segment ends within one prefix. B is backwards — a prefix below the model's minimum (512-4096 tokens, model-dependent) silently does not cache at all. *(task 5.4; concept: volatile_content_after_breakpoint; item `gap-08`)*

---

**5. A** — Two distinct features, and the exam-relevant discrimination is which one *removes* versus which one *summarizes*. Context editing (`context_management.edits` with `clear_tool_uses_*`) clears old tool results from what the model sees; compaction (beta, ~150K default trigger) summarizes earlier context into compaction blocks. B is the exact inversion, which is why it is the distractor — if you picked it, drill the pair as a matched set, not individually. Note the compaction gotcha too: you must append `response.content` back to `messages`, not just extracted text, or the compaction state is silently lost. *(task 6.1; concept: context_editing_clears_compaction_summarizes; item `gap-09`)*

---

**6. D** — `strict: true` is a top-level field on the *tool definition*, alongside `name`/`description`/`input_schema`, and it requires `additionalProperties: false` plus `required` in the schema. It guarantees `tool_use.input` validates exactly. C is the near-miss the API explicitly warns about: `strict` does not belong on `tool_choice`, and putting it there is a request the API will not honour as intended. A and B are both real, reasonable practices — a clear description does improve call quality, and returning `is_error: true` is the correct handling for a tool that *has* failed — but neither delivers the guarantee asked for; they reduce and repair violations rather than prevent them. *(task 8.1; concept: strict_goes_on_the_tool; item `gap-10`)*

---

**7. B** — An MCP server exposes three primitive kinds: **tools** (callable actions), **resources** (readable content the client can fetch), and **prompts** (reusable, parameterized templates the client surfaces). The runbook case wants tools and prompts together, which is exactly why the third primitive exists. D is the most tempting wrong answer, because a tools-only mental model is workable and common — you *can* force everything into tool definitions, which is precisely the design mistake the prompts primitive avoids. Your bank covers MCP transports and has six items mentioning MCP at all; the prompts primitive appears in none of them. *(task 8.2; concept: mcp_three_primitives; item `gap-11`)*

---

**8. A and C** — Both legs of this request are already covered by things you do not have to build: web search is a server-side tool that runs on Anthropic's infrastructure with no client execution loop, and Agent Skills plus the code execution tool generate formatted documents inside the sandbox (the sandbox ships `python-docx`, `python-pptx`, `matplotlib`, `pillow`, `pypdf`). B and D are the build-it-yourself reflex, and both rest on a false premise — retrieval does not have to be client-side, and file generation is not outside the API's reach. This four-way tradeoff (built-in / custom / Skills / MCP) is objective 8.3 at 4.1% of the exam, and *both* the built-in-tools leg and the Skills leg are absent from your bank. *(task 8.3; concept: prefer_built_in_and_skills_over_custom; item `gap-13`)*

---

**9. D** — Server-tool failures come back as HTTP 200 with an error object inside the `web_search_tool_result` block (e.g. `{"error_code": "max_uses_exceeded"}`), so no exception is raised and a try/except sees nothing. The consequence to internalize: on success `content` is a **list** of results, on error it is a single **object** — branch on that before indexing, or the failure surfaces later as a type error far from its cause. A is wrong because SDK retries cover transport-level failures (408/409/429/5xx), not a 200 carrying an error payload. C is the right instinct in the wrong place — the specific-first exception chain matters, but no class is raised here at all. *(task 8.1; concept: server_tool_errors_return_200; item `gap-14`)*

---

**10. C** — Organization administration — API keys, service accounts, workspaces, members, rate-limit reports — sits behind the Admin API and requires an admin credential: an Admin key (`sk-ant-admin...`) or an `org:admin` OAuth token. Ordinary API keys are rejected outright, which is the fact worth carrying. A is the intuitive guess and wrong in a specific way: scope is a property of the credential, not something a request elevates itself with. B misattributes the capability to the Models API, which reports capability metadata and context windows, not usage per key. D understates it — there is a programmatic surface, though note that *usage and cost* reports specifically remain raw-HTTP only rather than in the SDKs. Objective 7.4 has **zero items** in your existing bank. *(task 7.4; concept: admin_api_needs_admin_credential; item `gap-16`)*

---

**11. A** — Product surfaces (claude.ai, Desktop, Claude Code) wrap the conversation in their own system prompt, tools, and account settings; an API request is exactly what you send and nothing more. This is the substance of objective 2.5's "how Claude interprets instructions across interfaces" — 8.6% of the exam, the single largest sub-objective, and the interface-comparison leg of it appears nowhere in your bank (`claude.ai` and Desktop are mentioned zero times across all 245 items). C is the closest wrong answer and contains a real effect worn as a rule: recency does influence attention, and putting the actionable instruction last is good practice, but it is not what makes an instruction bind. B invents a role for `output_config`, which governs output format and effort, not style. *(task 2.5; concept: surfaces_add_context_api_does_not; item `gap-17`)*

---

## Score interpretation

This set is deliberately harder than the bank you have been scoring 95%+ on,
and it tests material you have not seen. Read the result as a gap check, not
as a score.

| Result | Reading |
|---|---|
| 14-17 | Gaps were mostly knowledge you had but had not been tested on. Nothing further needed tonight. |
| 10-13 | Normal for a first pass on unseen material. Re-read the rationales for the misses; that is your tomorrow-morning list. |
| under 10 | The platform-surface half of the blueprint is genuinely thin. Prioritize items 1-2, 4, 7, 13 — they carry the most exam weight between them. |

Any miss on **4** or **7** specifically means a stale fact from the bank is
still live in your recall. Those two are the ones to re-read last thing.
