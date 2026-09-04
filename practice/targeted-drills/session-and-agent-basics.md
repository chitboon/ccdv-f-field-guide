# CCDV-F Session Lifecycle & Agent Basics — 14 items

**Why these 14:** an audit of all 409 items in this bank found two named
techniques with **zero** coverage — *session lifecycle* (objective 2.5, inside
the largest sub-objective on the paper at 8.6%) and *the workflow-versus-agent
decision* (objective 1.1, 4.5%). Both are examinable, and one candidate
reported session lifecycle appearing on their form. This set fills them, plus
thin coverage in 1.2 agent construction and 5.2 technical fundamentals.

**Register:** stems run 3–4 sentences and carry **no code**. These test
architectural decisions and API mechanics, not syntax recall. Items 2 and 8
are multiple-response — the published exam guide lists multiple-response
items in the format, so practise them even if a given form has none.

**Coverage:** 2.5 session lifecycle (×5) · 1.1 workflow vs agent (×3) ·
1.2 agent construction (×3) · 5.2 technical fundamentals (×3).

---

**1.** `[2.5 · session state and process lifetime]` A chat assistant holds each user's conversation in a dictionary keyed by user id inside the web process. After a routine deploy, every in-flight conversation starts over and users have to repeat themselves. What is the design fault?

A. The system prompt was not version-pinned, so the new release loaded different instructions and invalidated the running conversations.
B. The API discarded its server-side session when the client reconnected under a new process, which the application should have detected.
C. Conversation state lived in the web process's memory, so it did not survive the restart — session state belongs in a store outside the process.
D. The context window was exceeded at the moment of the deploy, so the accumulated histories were truncated rather than restored to the running conversations.

---

**2.** `[2.5 · resuming a long conversation]` A support product lets a customer return days later and continue where they left off. Conversations that reach 200 turns become slow and expensive to send. **(Select TWO)**

A. Persist the transcript in a datastore under a session id, and rehydrate it into the message array when the customer comes back.
B. Rely on the service to retain the conversation between calls, so that only the newest user message need be sent whenever the customer returns at all.
C. Raise the output token ceiling so the model has room to restate the earlier context once the conversation resumes.
D. Summarize or compact the older turns, so the resumed context carries the thread's substance without the full turn-by-turn transcript.

---

**3.** `[2.5 · session identity and authorization]` A multi-user assistant occasionally shows one customer's earlier answer inside another customer's reply. Sessions are looked up by an identifier the client sends in a request header. What is the most likely cause?

A. The prompt cache returned a prefix shared between the two users, carrying the earlier customer's answer across into the second conversation.
B. The client-supplied identifier is never checked against the authenticated caller, so two users can address one session.
C. Parallel tool calls resolved out of order and their results were written into the wrong conversation.
D. The context window filled, and the model substituted content it had seen in a concurrent request.

---

**4.** `[2.5 · session eviction]` A team stores every session indefinitely so any user can always resume. Storage grows without bound, and almost none of the retained sessions are ever read again. What should the design add?

A. A larger context window per request, so more of each session fits without needing long-term storage.
B. Compaction applied on every request, which summarizes the history and thereby removes any need to store the transcripts durably at all.
C. A second storage cluster partitioned by tenant, so the growth is distributed rather than concentrated.
D. An eviction policy — a time-to-live on inactive sessions, with an archive path for what must be retained.

---

**5.** `[2.5 · what a session is]` A developer new to the API asks why the application has to track a "session" at all, when every call already carries the whole conversation.

A. Because the application is what assembled that conversation in the first place — the service holds no session, so identity, storage, and lifetime are all the application's to define.
B. Because the service opens a session on the first call and expires it after a period of inactivity, which the application then has to mirror in its own store.
C. Because sessions exist only when streaming is in use, as the open connection is what carries continuity between turns.
D. Because the session is the cache entry for the conversation prefix; when that prefix expires, the session has ended.

---

**6.** `[1.1 · workflow versus agent]` Inbound tickets must be sorted into five fixed categories and routed to the matching queue. The categories are settled and the routing rules are written down. The team is debating an autonomous agent against a fixed pipeline.

A. An agent, because ticket wording varies enormously and only a model-directed loop can absorb that much variation regardless of phrasing.
B. An agent, so that additional tools can be introduced later without having to redesign the pipeline around them.
C. A workflow — the steps and their order are known in advance.
D. A workflow that dispatches an agent for each ticket, keeping the routing deterministic while leaving the classification step genuinely open-ended.

---

**7.** `[1.1 · when not to build an agent]` A team is applying the standard criteria to decide whether a task justifies an agent. Which consideration argues **against** building one?

A. Mistakes are caught by the test suite and are inexpensive to roll back when they happen.
B. The task runs over many steps and is difficult to specify completely before it starts.
C. The outcome carries enough value to justify the additional latency and cost that an agent inevitably brings with it.
D. The work can be written out in full as a fixed sequence of steps, decided in advance of the task beginning to run.

---

**8.** `[1.1 · patterns along the spectrum]` A team is weighing a prompt chain, a router, and an autonomous agent for a document-processing feature. **(Select TWO)**

A. An agent is the better choice whenever the input varies, since absorbing variation is the problem agents exist to solve.
B. A prompt chain suits steps that are known and fixed in order.
C. An agent is warranted when the number and order of steps depend on what earlier steps turn up.
D. A router is a species of agent, because the model is what selects the path taken at runtime.

---

**9.** `[1.2 · deployment models]` An organisation wants an agent where the vendor runs the reasoning loop *and* hosts the environment its tools execute in, with the configuration version-pinned so any run can be reproduced. Which arrangement is that?

A. A managed deployment — the vendor runs the loop and hosts the per-run workspace, with configuration stored as a versioned object.
B. A self-hosted harness running a version-pinned container image on infrastructure the organisation operates and maintains itself.
C. A framework-built agent deployed to the team's cluster behind a pinned dependency lockfile.
D. A hand-written loop that reads its configuration from checked-in files at process startup.

---

**10.** `[1.2 · deterministic guarantees]` A coding agent must never execute a destructive shell command, and the guarantee has to hold no matter what the model decides to do. Where does that guarantee belong?

A. In the system prompt, written as an explicit prohibition the model is directed to observe on every turn without exception.
B. In the tool description, which is where the model learns which commands fall outside the tool's intended scope.
C. In a deterministic pre-execution check that refuses the command before it runs.
D. In a post-execution check that recognises the destructive command afterwards and reverses what it did.

---

**11.** `[1.2 · what the agent loop is]` A developer is writing their first agent loop by hand and asks what governs whether it goes round again.

A. It continues for a fixed number of turns set at startup, which is what bounds an otherwise open-ended loop.
B. It continues while the response still contains text, and stops once the response contains only tool calls.
C. It continues until the model returns an empty content array, which is always the signal that it has nothing further to add.
D. It continues while the stop reason reports a tool call.

---

**12.** `[5.2 · what an SDK is]` A developer asks whether moving from hand-written HTTP calls to the official SDK will reduce the number of tokens their application sends per turn.

A. Yes — the SDK maintains the conversation on the service side, so only the newest turn actually travels on any given request.
B. No — it is a typed client over the same endpoint.
C. Yes — the SDK compresses the accumulated message history before transmitting it.
D. No, but it does lower the bill, because traffic sent through an official client is billed at a reduced rate.

---

**13.** `[5.2 · streaming transport]` An application streams a long response to a browser and the connection drops partway through. What does recovery require?

A. Resending the request in full; the stream is one-directional and cannot be rejoined partway through.
B. Reconnecting against the same response identifier, which resumes delivery from the last event received.
C. Switching to a bidirectional socket, which is the only transport that survives a drop once a response exceeds a certain length.
D. Polling a status endpoint until the finished response becomes available for retrieval.

---

**14.** `[5.2 · error handling scope]` A team wraps every API call in one broad exception handler that retries with exponential backoff. What is the consequence in production?

A. Rate-limit responses go uncaught and fail straight away, because they are signalled through a response header rather than raised as an error.
B. A request rejected for a client-side mistake is retried anyway, so one malformed call burns through the backoff schedule before its error surfaces.
C. Connection failures are retried while server errors are not, since only the former are treated as transient.
D. None — the policy is sound, though it duplicates retry behaviour the client library already performs.

---

*14 items · 2 multiple-response · key in `session-and-agent-basics-key.md`*
