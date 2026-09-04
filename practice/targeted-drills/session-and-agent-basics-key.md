# CCDV-F Session Lifecycle & Agent Basics — Key and Rationales

**Answers:** 1 C · 2 A+D · 3 B · 4 D · 5 A · 6 C · 7 D · 8 B+C · 9 A · 10 C
· 11 D · 12 B · 13 A · 14 B

Items 2 and 8 need both letters to count.

---

**1. C** — Session state held in process memory is lost on every restart, deploy, or scale-in event, and nothing about the API restores it. Session storage belongs outside the process — a datastore keyed by session id — so any instance can serve any turn. **B is the misconception this whole set exists to correct: the API holds no session.** Each request carries the entire conversation because the caller assembled it; there is nothing server-side to reconnect to. A and D describe real failures that would look different — a prompt change alters behaviour rather than erasing history, and truncation degrades the tail rather than resetting everything at once. *(2.5; concept: session_state_outside_the_process)*

---

**2. A and D** — Two independent problems, two mechanisms. Resumability needs the transcript persisted under a session id and rehydrated into the message array on return. Cost and latency at 200 turns need the older history summarized or compacted, so the resumed context carries the substance without every turn. **B is the stateless misconception again** — sending only the newest message loses the thread entirely, because nothing retained it. C confuses the output ceiling with input context: a larger output allowance neither restores history nor reduces what you send. *(2.5; concept: persist_then_compact)*

---

**3. B** — A session identifier supplied by the client and used without checking it against the authenticated user is an authorization defect: any caller who supplies another's identifier is handed that session. Session lookup must be scoped to the authenticated identity, never to a value the caller controls. A is worth ruling out on mechanism — cache reads return the caller's own prefix and never move content between conversations. C and D describe failures that do not cross user boundaries: misordered tool results corrupt one conversation, and a full context window truncates rather than importing another request's content. *(2.5; concept: session_lookup_scoped_to_identity)*

---

**4. D** — Unbounded retention with no read pattern is a storage leak. The mechanism is an eviction policy: a time-to-live on inactive sessions, plus a deliberate archive path for anything with a retention obligation. A addresses the wrong resource — the context window governs a single request, not stored history. B misreads compaction, which manages what goes into a request and is not a substitute for durable storage. C is the plausible operational answer that postpones the problem: sharding unbounded growth still grows without bound. *(2.5; concept: session_eviction_policy)*

---

**5. A** — The service is stateless: every request carries the full conversation because the application built it that way. "Session" is therefore an application-level construct — the application decides what identifies one, where it is stored, when it expires, and who may address it. B invents a server-side session with a server-side expiry. C ties continuity to the streaming connection, which lasts one response. D conflates a session with a cache entry — caching is a cost optimization over the prefix you send, and its expiry says nothing about whether the conversation is over. *(2.5; concept: sessions_are_an_application_concern)*

---

**6. C** — Fixed categories and written-down routing rules mean the steps and their order are known before the work starts, which is the definition of a workflow. A fixed pipeline is cheaper, lower-latency, easier to test, and easier to reason about when it goes wrong. A is the most common wrong instinct: **variation in the input is not the criterion — variation in the required control flow is.** Classifying varied text is a single well-specified step. B builds for a hypothetical requirement at real present cost. D adds an autonomous loop inside a step that does not need one. *(1.1; concept: workflow_when_control_flow_is_known)*

---

**7. D** — Work expressible as a fixed sequence decided up front does not need a model to choose the next step, so an agent adds latency, cost, and nondeterminism for nothing. A, B, and C are the criteria that argue *for* an agent: recoverable errors, a task that resists full specification, and an outcome worth the overhead. The trap is reading A as an objection — cheap, catchable errors make an agent *more* viable, not less, because the cost of a wrong step is bounded. *(1.1; concept: criteria_against_an_agent)*

---

**8. B and C** — These name the ends of the spectrum correctly. A prompt chain fits fixed, known, ordered steps; an agent is warranted when the number and order of steps depend on what earlier steps discover. **D is the item's real discrimination:** routing uses the model to *classify*, but the set of destinations and the control flow around them are fixed by the developer, which makes it a workflow pattern, not an agent. A repeats item 6's error — input variation is not the test. *(1.1; concept: chain_router_agent_spectrum)*

---

**9. A** — Two things are being asked for together: the vendor runs the loop (the harness) *and* hosts where tools execute (the deployment). Only a managed deployment supplies both, and storing the configuration as a versioned object is what makes a run reproducible. B, C, and D all keep execution on the organisation's own infrastructure and differ only in how the harness is obtained — a container image, a framework, or hand-written code. **The axis being tested is harness versus deployment**, and it is easy to answer on the harness half alone and miss that hosting was also specified. *(1.2; concept: harness_and_deployment_together)*

---

**10. C** — A guarantee that must hold regardless of what the model decides cannot live anywhere the model can influence. A deterministic pre-execution check inspects the proposed command and refuses it before anything runs — code, not persuasion. A and B both place the control inside the model's input: a system instruction and a tool description are requests, and a sufficiently unusual turn can work around either. D acts too late; some destructive operations have no reverse, and "detect and undo" is not a guarantee. *(1.2; concept: deterministic_control_before_execution)*

---

**11. D** — The loop is driven by the stop reason: while it reports that the model called a tool, execute the calls, return the results, and go round again; when the model reaches a natural stop, the loop ends. A fixed turn cap (A) is a sensible *safety bound* but is not what governs continuation — mistaking the guard for the condition is the error. B inverts the signal, since a turn can carry both text and tool calls. C waits for a state the API does not produce as a completion signal. *(1.2; concept: stop_reason_drives_the_loop)*

---

**12. B** — The SDK is a typed client over the same endpoint. It gives you typed exceptions, retry policy, streaming assembly, and typed objects; it does not change what travels on the wire. **A is the stateless misconception in its most tempting form** — and the reason it matters is that a developer who believes it will build a client that silently drops history. C invents compression. D invents a billing distinction; pricing is per token regardless of the client. *(5.2; concept: sdk_is_a_typed_client)*

---

**13. A** — Streaming is one-directional server-to-client and is not resumable: a dropped connection means resending the request in full, which is why long generations need idempotent handling upstream. B is the answer most people expect and the reason teams build reconnect logic that never fires. C describes a transport the API does not use for this. D describes a batch or polling interface, not a stream. *(5.2; concept: streams_are_not_resumable)*

---

**14. B** — One broad handler cannot distinguish a request that failed because it was malformed from one that failed because the service was busy, so it retries both. The client-side failure was never going to succeed, and the caller waits out the entire backoff before seeing an error that was available immediately. The fix is a most-specific-first chain: re-raise client errors at once, honour the retry hint on rate limits, back off on server errors and connection failures. A is false — rate-limit responses are raised like any other error status. C has the transience backwards. D treats duplicated retries as harmless when they multiply the delay on exactly the failures that deserve none. *(5.2; concept: retry_scope_must_distinguish_failure_classes)*
