# CCDV-F Concept Drills (53 Blueprint-Exact Items)







---

**1.** In an agentic architecture, what distinguishes an autonomous agent loop from a standard sequential chain?

A. Sequential chains execute in parallel, while agent loops execute serially across standard client implementation workflows within standard production deployment environments.  
B. Sequential chains use system prompts, while agent loops do not across standard client implementation workflows in enterprise system configurations.  
C. Agent loops inspect output dynamically to decide next steps, while sequential chains follow fixed steps in enterprise system configurations.  
D. Agent loops require fine-tuned custom model weights across standard client implementation workflows in enterprise system configurations.  

<details><summary>Answer</summary>
**C — Agent loops inspect output dynamically to decide next ste...**
Agent loops inspect `stop_reason` and intermediate tool outputs dynamically to determine the next action, whereas sequential chains follow fixed, predetermined paths.
</details>

---

**2.** In a coordinator-subagent pattern, what is the primary role of the coordinator agent?

A. Execute all low-level API calls directly without delegating work under default system configuration within standard production deployment environments.  
B. Store user authentication tokens in browser storage under default system configuration in enterprise system configurations.  
C. Format final responses as HTML web pages under default system configuration in enterprise system configurations.  
D. Decompose complex user goals, delegate subtasks to subagents, and synthesize results in enterprise system configurations.  

<details><summary>Answer</summary>
**D — Decompose complex user goals, delegate subtasks to subage...**
Coordinator agents manage overall workflow orchestration, splitting large tasks into targeted subagent tasks and aggregating their outputs.
</details>

---

**3.** How should an application agent loop handle a response with `stop_reason: "end_turn"`?

A. Immediately invoke a tool call during standard production API invocation in enterprise system configurations.  
B. Raise an exception and terminate execution during standard production API invocation.  
C. Re-send the prompt with double the max token limit during standard production API invocation.  
D. Treat the message as complete and return the final output to the user within standard production deployment environments.  

<details><summary>Answer</summary>
**D — Treat the message as complete and return the final output...**
`stop_reason: "end_turn"` signals that Claude has completed its response generation and does not require further tool calls or processing.
</details>

---

**4.** What is the most effective context management strategy during a long-running multi-turn agent loop?

A. Keep all historical tool call responses in full without trimming across standard client implementation workflows within standard production deployment environments.  
B. Truncate or summarize historical tool outputs while preserving instructions and system context in enterprise system configurations.  
C. Clear the entire conversation history after every turn across standard client implementation workflows in enterprise system configurations.  
D. Move system prompt instructions into every user message across standard client implementation workflows in enterprise system configurations.  

<details><summary>Answer</summary>
**B — Truncate or summarize historical tool outputs while prese...**
Trimming large tool outputs prevents context crowding and degradation while keeping core system instructions intact.
</details>

---

**5.** When an agent tool call fails due to a temporary external service error, how should the agent loop recover?

A. Crash the script immediately under default system configuration within standard production deployment environments.  
B. Delete the system prompt and resend under default system configuration in enterprise system configurations.  
C. Pass `is_error: true` in the `tool_result` block so Claude can observe failure and attempt self-correction.  
D. Hardcode a dummy string into response under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**C — Pass `is_error: true` in the `tool_result` block so Claud...**
Returning `is_error: true` provides Claude with structural feedback on the failure, allowing it to retry or adjust parameters.
</details>

---

**6.** Which workflow execution pattern allows independent tool execution steps to run concurrently?

A. Parallel tool execution within standard production deployment environments.  
B. Serial chaining in enterprise system configurations.  
C. Evaluator-optimizer loop.  
D. Human-in-the-loop gate  

<details><summary>Answer</summary>
**A — Parallel tool execution within standard production deploy...**
Parallel tool execution enables non-dependent tool operations to run simultaneously, reducing total wall-clock latency.
</details>

---

**7.** What defines the Reflection / Self-Correction agent pattern?

A. The agent generates an output, evaluates it against quality criteria, and refines it before returning in enterprise system configurations.  
B. The agent delegates work to a human supervisor across standard client implementation workflows in enterprise system configurations.  
C. The agent runs multiple models simultaneously and averages their outputs across standard client implementation workflows within standard production deployment environments.  
D. The agent caches responses in Redis across standard client implementation workflows in enterprise system configurations.  

<details><summary>Answer</summary>
**A — The agent generates an output, evaluates it against quali...**
Reflection loops incorporate an evaluation step where intermediate results are checked against rubrics before finalizing output.
</details>

---

**8.** Situations where a human-in-the-loop (HITL) gate should be integrated into an agentic workflow:

A. Executing high-impact financial transactions or database mutations in enterprise system configurations.  
B. Performing low-risk, read-only search operations under default system configuration within standard production deployment environments.  
C. Formatting text into JSON arrays under default system configuration in enterprise system configurations.  
D. Escalating operations when model confidence or tool safety checks fail in enterprise system configurations.  

<details><summary>Answer</summary>
**A, D — Executing high-impact financial transactions or database ...**
HITL gates prevent unauthorized state mutations and handle edge-case escalations when automated checks trigger warnings.
</details>

---

**9.** What is the core design principle of stateless LLM API integration?

A. The client application must send the complete required conversation history with every API call within standard production deployment environments.  
B. The API server automatically saves all past user messages on Anthropic servers during standard production API invocation.  
C. Prompts must never exceed 100 tokens during standard production API invocation in enterprise system configurations.  
D. All API calls must use HTTP GET requests during standard production API invocation in enterprise system configurations.  

<details><summary>Answer</summary>
**A — The client application must send the complete required co...**
Anthropic APIs are stateless; all context and message history required for generation must be supplied by the client application.
</details>

---

**10.** Why should system prompt templates be decoupled from application source code?

A. To speed up Python execution time across standard client implementation workflows within standard production deployment environments.  
B. To enable independent prompt iteration, versioning, and testing without redeployments in enterprise system configurations.  
C. To allow client browsers to edit system prompts directly across standard client implementation workflows.  
D. To avoid using environment variables across standard client implementation workflows in enterprise system configurations.  

<details><summary>Answer</summary>
**B — To enable independent prompt iteration, versioning, and t...**
Decoupling prompts from application code allows rapid prompt refinement without requiring full software build and release cycles.
</details>

---

**11.** In a Retrieval-Augmented Generation (RAG) architecture, when is context injection preferred over model fine-tuning?

A. When domain knowledge is static and never changes under default system configuration.  
B. When knowledge updates frequently and responses require strict source citation.  
C. When latency must be under 5 milliseconds under default system configuration within standard production deployment environments.  
D. When the application operates completely offline under default system configuration.  

<details><summary>Answer</summary>
**B — When knowledge updates frequently and responses require s...**
RAG allows dynamic knowledge insertion and verifiable attribution without expensive model retraining.
</details>

---

**12.** How should long-running, asynchronous LLM processing tasks be structured in cloud applications?

A. Block the HTTP request thread until LLM completes generation during standard production API invocation.  
B. Use task queues and return a job ID to the client for status polling or webhooks within standard production deployment environments.  
C. Increase client HTTP request timeout to 24 hours during standard production API invocation in enterprise system configurations.  
D. Run LLM inference directly inside a database trigger during standard production API invocation.  

<details><summary>Answer</summary>
**B — Use task queues and return a job ID to the client for sta...**
Asynchronous queues decouple user HTTP requests from variable LLM generation times, preventing web server worker exhaustion.
</details>

---

**13.** What is the primary security risk when building multi-tenant LLM applications?

A. Low GPU memory usage across standard client implementation workflows in enterprise system configurations.  
B. High network bandwidth consumption across standard client implementation workflows.  
C. Exceeding maximum JSON payload size across standard client implementation workflows within standard production deployment environments.  
D. Cross-tenant context leakage when prompt history or embeddings are not tenant-isolated.  

<details><summary>Answer</summary>
**D — Cross-tenant context leakage when prompt history or embed...**
Multi-tenant applications must strictly filter vector queries and prompt context to prevent unauthorized access across tenants.
</details>

---

**14.** Which Anthropic SDK client instantiation is recommended for TypeScript production applications?

A. `const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });` in enterprise system configurations.  
B. `const client = Anthropic.connectWithoutKey();` under default system configuration within standard production deployment environments.  
C. `const client = new Anthropic({ rawHttp: true });` under default system configuration.  
D. `const client = new Anthropic({ hardcodedKey: "sk-ant-12345" });` in enterprise system configurations.  

<details><summary>Answer</summary>
**A — `const client = new Anthropic({ apiKey: process.env.ANTHR...**
Passing `apiKey` from `process.env` keeps sensitive authentication secrets out of source code and client bundles.
</details>

---

**15.** What is the recommended recovery action for HTTP status codes 429 (Rate Limit) and 529 (Overloaded)?

A. Fail permanently and inform user to delete their account during standard production API invocation.  
B. Switch from Python to JavaScript immediately during standard production API invocation in enterprise system configurations.  
C. Implement client-side exponential backoff with randomized jitter and retry within standard production deployment environments.  
D. Remove system parameter and retry during standard production API invocation in enterprise system configurations.  

<details><summary>Answer</summary>
**C — Implement client-side exponential backoff with randomized...**
Exponential backoff with jitter handles temporary rate limiting and server congestion gracefully without thundering herd retries.
</details>

---

**16.** Why is random jitter added to exponential backoff algorithms during API retries?

A. To increase overall payload size across standard client implementation workflows within standard production deployment environments.  
B. To randomise model temperature across standard client implementation workflows.  
C. To prevent thundering herd problems where simultaneous retries re-overload the server.  
D. To bypass authentication checks across standard client implementation workflows.  

<details><summary>Answer</summary>
**C — To prevent thundering herd problems where simultaneous re...**
Jitter desynchronizes concurrent client retries, smoothing out traffic spikes to the API endpoints.
</details>

---

**17.** Which telemetry metrics should be captured when tracing Claude API requests in production?

A. Input token count and output token count in enterprise system configurations.  
B. Time-to-first-token (TTFT) and total request latency.  
C. User OS password under default system configuration within standard production deployment environments.  
D. Database table row count under default system configuration.  

<details><summary>Answer</summary>
**A, B — Input token count and output token count in enterprise sy...**
Tracking token consumption and latency metrics is vital for cost management, SLA monitoring, and performance optimization.
</details>

---

**18.** In the Anthropic Python SDK streaming interface, how are text tokens consumed from the stream?

A. `for chunk in response:` during standard production API invocation in enterprise system configurations.  
B. `stream.fetch_all_at_once()` during standard production API invocation.  
C. `client.get_stream_array()` during standard production API invocation.  
D. `with client.messages.stream(...) as stream: for text in stream.text_stream:` within standard production deployment environments.  

<details><summary>Answer</summary>
**D — `with client.messages.stream(...) as stream: for text in ...**
The helper context manager `stream.text_stream` yields incremental text tokens safely and handles stream closure automatically.
</details>

---

**19.** How does the top-level `system` parameter in the Messages API differ from placing instructions inside a `user` message?

A. `system` parameter is ignored by Claude 3.5 Sonnet across standard client implementation workflows.  
B. `system` parameter sets global framing and constraints with higher adherence and steerability in enterprise system configurations.  
C. `system` parameter can only contain 10 words across standard client implementation workflows within standard production deployment environments.  
D. `system` parameter is only supported in legacy v1 APIs across standard client implementation workflows.  

<details><summary>Answer</summary>
**B — `system` parameter sets global framing and constraints wi...**
The dedicated `system` parameter receives higher structural weight in model attention mechanisms compared to user message text.
</details>

---

**20.** Which message array payload violates the Messages API specification?

A. `[{"role": "user", "content": "Question 1"}, {"role": "user", "content": "Question 2"}]` in enterprise system configurations.  
B. `[{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]` within standard production deployment environments.  
C. `[{"role": "user", "content": "Analyze this image", "content": [...]}]` under default system configuration.  
D. `[{"role": "user", "content": "Hello"}]` under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**A — `[{"role": "user", "content": "Question 1"}, {"role": "us...**
The API requires strict alternation between `user` and `assistant` roles in the `messages` array payload.
</details>

---

**21.** How are image files passed to Claude in a multi-modal Messages API call?

A. As a raw binary URL string in system prompt during standard production API invocation in enterprise system configurations.  
B. Inside a `content` block specifying `type: "image"`, source `type: "base64"`, `media_type`, and base64 `data` within standard production deployment environments.  
C. Attached as an email file zip archive during standard production API invocation in enterprise system configurations.  
D. Converted into an ASCII art string during standard production API invocation in enterprise system configurations.  

<details><summary>Answer</summary>
**B — Inside a `content` block specifying `type: "image"`, sour...**
Multi-modal requests pass structured image blocks containing valid base64 payload strings and mime types (`image/jpeg`, `image/png`).
</details>

---

**22.** What is the security standard for managing `ANTHROPIC_API_KEY` in server applications?

A. Hardcode API key in public client JavaScript files across standard client implementation workflows within standard production deployment environments.  
B. Commit `.env` files with keys to public GitHub repositories across standard client implementation workflows.  
C. Pass key in URL query parameters across standard client implementation workflows in enterprise system configurations.  
D. Store in server environment variables or key vaults, never exposing keys to client-side code in enterprise system configurations.  

<details><summary>Answer</summary>
**D — Store in server environment variables or key vaults, neve...**
API keys grant full account billing access and must never be shipped in frontend bundles or committed to version control.
</details>

---

**23.** What client SDK parameters should be configured to prevent indefinite request hangs during network disruptions?

A. `temperature` and `top_k` within standard production deployment environments.  
B. `model` and `system`.  
C. `timeout` and `maxRetries`  
D. `stream` and `tools`.  

<details><summary>Answer</summary>
**C — `timeout` and `maxRetries`**
Setting explicit request timeouts and retry counts ensures application threads recover when underlying network sockets stall.
</details>

---

**24.** If an application requires subsecond response visibility for user chat interfaces, which API feature must be implemented?

A. Streaming API (`stream=True`) within standard production deployment environments.  
B. Batch API during standard production API invocation.  
C. Prompt Caching only in enterprise system configurations.  
D. Offline JSON export in enterprise system configurations.  

<details><summary>Answer</summary>
**A — Streaming API (`stream=True`) within standard production ...**
Streaming returns partial token deltas immediately, reducing perceived user latency from seconds to milliseconds.
</details>

---

**25.** How can developers enforce deterministic outputs from probabilistic LLM responses?

A. Set `temperature: 1.0` across standard client implementation workflows in enterprise system configurations.  
B. Use longer system prompts without schemas across standard client implementation workflows in enterprise system configurations.  
C. Disable system prompts completely across standard client implementation workflows within standard production deployment environments.  
D. Combine strict JSON schema enforcement via tool choice (`tool_choice`) with client-side schema validation.  

<details><summary>Answer</summary>
**D — Combine strict JSON schema enforcement via tool choice (`...**
Forcing schema validation via `tool_choice` constrains generation to valid structural properties programmatically.
</details>

---

**26.** Why should production applications pin exact model version identifiers (e.g. `claude-3-5-sonnet-20241022`) instead of aliases?

A. Aliases are 50% more expensive under default system configuration within standard production deployment environments.  
B. Model version strings speed up DNS lookup under default system configuration in enterprise system configurations.  
C. Aliases do not support tool calling under default system configuration in enterprise system configurations.  
D. Model aliases may update automatically, causing unexpected behavior or output regression in production workflows.  

<details><summary>Answer</summary>
**D — Model aliases may update automatically, causing unexpecte...**
Pinning exact date-versioned model strings protects production applications from behavioral drifts when aliases change targets.
</details>

---

**27.** What is the priority hierarchy for `CLAUDE.md` files in a project workspace?

A. Subdirectory `CLAUDE.md` rules override or augment parent/project-root `CLAUDE.md` rules for files in that subdirectory within standard production deployment environments.  
B. Global settings override project root, which overrides subdirectories during standard production API invocation.  
C. System environment variables ignore `CLAUDE.md` completely during standard production API invocation in enterprise system configurations.  
D. Only one `CLAUDE.md` file is allowed per operating system during standard production API invocation in enterprise system configurations.  

<details><summary>Answer</summary>
**A — Subdirectory `CLAUDE.md` rules override or augment parent...**
Claude Code merges configuration hierarchy, allowing localized subdirectory instructions to take precedence over root defaults.
</details>

---

**28.** Which flag allows Claude Code to run non-interactively in CI/CD automation scripts without prompting for confirmation?

A. `--interactive` across standard client implementation workflows within standard production deployment environments.  
B. `--print` (or `--dangerously-skip-permissions` for headless execution).  
C. `--gui-mode` across standard client implementation workflows in enterprise system configurations.  
D. `--debug-pause` across standard client implementation workflows.  

<details><summary>Answer</summary>
**B — `--print` (or `--dangerously-skip-permissions` for headle...**
Headless CLI execution mode bypasses interactive terminal prompts, enabling automated execution in CI/CD runners.
</details>

---

**29.** In automated LLM output testing, what is the "LLM-as-a-Judge" pattern?

A. Human developers manually grade every single API output under default system configuration in enterprise system configurations.  
B. An independent, highly capable LLM evaluates candidate responses against predefined grading rubrics.  
C. Unit tests verify Python syntax errors only under default system configuration within standard production deployment environments.  
D. Database triggers check SQL query execution speeds under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**B — An independent, highly capable LLM evaluates candidate re...**
Using a strong evaluator model automates quality scoring across subjective output criteria efficiently.
</details>

---

**30.** Why can LLMs output false information with high confidence (hallucination)?

A. The model database is corrupted during standard production API invocation in enterprise system configurations.  
B. System prompts disable factual checks by default during standard production API invocation in enterprise system configurations.  
C. API keys expire during generation during standard production API invocation in enterprise system configurations.  
D. Token generation is driven by conditional probability distributions, not factual verification logic within standard production deployment environments.  

<details><summary>Answer</summary>
**D — Token generation is driven by conditional probability dis...**
Language models produce plausible continuations based on probabilistic patterns; factual correctness is not natively guaranteed.
</details>

---

**31.** What is "context degradation" in long LLM conversations?

A. The model forgets its token pricing tier across standard client implementation workflows within standard production deployment environments.  
B. The API server shuts down automatically across standard client implementation workflows in enterprise system configurations.  
C. As context window fills up, earlier system instructions and constraints can be crowded out by historical dialogue.  
D. Output generation switches to Spanish across standard client implementation workflows in enterprise system configurations.  

<details><summary>Answer</summary>
**C — As context window fills up, earlier system instructions a...**
Model attention mechanisms dilute over long context windows, causing older prompt constraints to lose relative weight.
</details>

---

**32.** What capability does Extended Thinking (Claude 3.7 Sonnet thinking mode) introduce?

A. Generates image assets alongside text under default system configuration within standard production deployment environments.  
B. Runs client-side Python scripts offline under default system configuration in enterprise system configurations.  
C. Produces visible reasoning tokens before generating final response to solve complex logic problems.  
D. Reduces token costs to zero under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**C — Produces visible reasoning tokens before generating final...**
Thinking mode exposes internal reasoning tokens prior to output generation, significantly boosting accuracy on complex tasks.
</details>

---

**33.** Which Claude 3.5 model selection is optimized for high-volume, cost-sensitive, low-latency tasks like fast classification?

A. Claude 3.5 Haiku within standard production deployment environments.  
B. Claude 3.5 Opus.  
C. Claude 3.5 Sonnet  
D. Claude 3.0 Light  

<details><summary>Answer</summary>
**A — Claude 3.5 Haiku within standard production deployment en...**
Claude 3.5 Haiku offers rapid generation speed and low token costs, ideal for high-volume text classification and filtering.
</details>

---

**34.** What is the effect of setting `temperature: 0.0` in a Messages API request?

A. Disables API key authentication across standard client implementation workflows within standard production deployment environments.  
B. Maximizes output randomness and creativity across standard client implementation workflows.  
C. Produces greedy, deterministic output selection (lowest variability) in enterprise system configurations.  
D. Truncates response to 0 tokens across standard client implementation workflows in enterprise system configurations.  

<details><summary>Answer</summary>
**C — Produces greedy, deterministic output selection (lowest v...**
Setting temperature to 0 selects top-probability tokens, minimizing variation across repeated calls.
</details>

---

**35.** How does subword tokenization (byte-pair encoding) impact token counting?

A. 1 word always equals exactly 1 token under default system configuration in enterprise system configurations.  
B. Words, code snippets, and special characters are split into subword chunks; ~100 tokens equals roughly 75 English words.  
C. Tokens are calculated based on file disk megabytes under default system configuration within standard production deployment environments.  
D. Images do not consume tokens under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**B — Words, code snippets, and special characters are split in...**
BPE tokenization tokenizes common subwords and code constructs, resulting in token counts exceeding raw word counts.
</details>

---

**36.** You need to classify 100,000 incoming customer support tickets into 5 categories overnight. Cost is the main constraint. Which model choice is best?

A. Claude 3.5 Haiku via Message Batches API within standard production deployment environments.  
B. Claude 3.5 Opus via real-time streaming API.  
C. Claude 3.5 Sonnet real-time API in enterprise system configurations.  
D. Claude 3.0 Opus real-time API in enterprise system configurations.  

<details><summary>Answer</summary>
**A — Claude 3.5 Haiku via Message Batches API within standard ...**
Combining Haiku's low base cost with the Message Batches API provides a 50% cost discount for asynchronous workloads.
</details>

---

**37.** What trade-off is made when selecting Claude 3.5 Sonnet over Claude 3.5 Haiku for a complex code refactoring task?

A. Higher cost and slightly higher latency for superior reasoning and code accuracy in enterprise system configurations.  
B. Lower cost and faster speed for lower accuracy across standard client implementation workflows.  
C. Zero token usage for lower security across standard client implementation workflows within standard production deployment environments.  
D. Offline availability for higher memory consumption across standard client implementation workflows.  

<details><summary>Answer</summary>
**A — Higher cost and slightly higher latency for superior reas...**
Sonnet trades higher per-token cost for advanced architectural reasoning and code generation quality.
</details>

---

**38.** What are the requirement conditions for a prompt segment to benefit from Prompt Caching?

A. Segment must be at the prefix (start) of the request payload in enterprise system configurations.  
B. Segment must change on every API call under default system configuration within standard production deployment environments.  
C. Segment must meet minimum token length (e.g. 1,024 tokens for Sonnet/Opus, 2,048 for Haiku).  
D. Payload must use HTTP GET requests under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**A, C — Segment must be at the prefix (start) of the request payl...**
Prompt caching applies to fixed prompt prefixes meeting minimum token counts (1k/2k tokens depending on model).
</details>

---

**39.** Why are XML tags (e.g. `<instructions>`, `<context>`) recommended in Claude prompts?

A. XML tags are required for JSON parsing during standard production API invocation in enterprise system configurations.  
B. XML tags reduce token count by 50% during standard production API invocation in enterprise system configurations.  
C. XML tags bypass safety guardrails during standard production API invocation in enterprise system configurations.  
D. Claude is explicitly trained to parse XML structure, improving instruction compliance and boundary enforcement within standard production deployment environments.  

<details><summary>Answer</summary>
**D — Claude is explicitly trained to parse XML structure, impr...**
XML tagging separates context, examples, and instructions cleanly, allowing Claude's attention to parse intent accurately.
</details>

---

**40.** What is "few-shot prompting"?

A. Providing zero examples and asking Claude to guess across standard client implementation workflows within standard production deployment environments.  
B. Retraining model weights using gradient descent across standard client implementation workflows in enterprise system configurations.  
C. Sending 100 requests simultaneously across standard client implementation workflows in enterprise system configurations.  
D. Providing 1 to 5 concrete input/output examples within the prompt to demonstrate formatting and reasoning.  

<details><summary>Answer</summary>
**D — Providing 1 to 5 concrete input/output examples within th...**
Few-shot examples clarify target formatting, edge cases, and output style in-context without weight updates.
</details>

---

**41.** In prompt iteration, what is the Description-Discernment loop?

A. Observing output defects (Discernment), naming the specific gap, and updating prompt constraints (Description).  
B. Randomly tweaking prompt words until output changes under default system configuration in enterprise system configurations.  
C. Deleting the prompt and starting over under default system configuration within standard production deployment environments.  
D. Asking another user to rewrite prompt under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**A — Observing output defects (Discernment), naming the specif...**
Systematic prompt engineering isolates observed output defects and applies targeted structural fixes.
</details>

---

**42.** What is a "rolling context window" strategy for long chat applications?

A. Saving all tokens indefinitely during standard production API invocation in enterprise system configurations.  
B. Clearing system prompts after 10 turns during standard production API invocation in enterprise system configurations.  
C. Re-sending API keys on every message during standard production API invocation in enterprise system configurations.  
D. Retaining system prompt + initial turn + N most recent message turns while pruning old intermediate turns within standard production deployment environments.  

<details><summary>Answer</summary>
**D — Retaining system prompt + initial turn + N most recent me...**
Rolling windows bound token costs and prevent context crowding while preserving core system context.
</details>

---

**43.** Where should context documents (e.g. retrieved RAG chunks) be placed in relation to instructions?

A. At the very end of the prompt after questions across standard client implementation workflows within standard production deployment environments.  
B. In HTTP header string across standard client implementation workflows in enterprise system configurations.  
C. Inside XML tags (e.g. `<documents>`) before the specific user instruction or question.  
D. Embedded in image files across standard client implementation workflows in enterprise system configurations.  

<details><summary>Answer</summary>
**C — Inside XML tags (e.g. `<documents>`) before the specific ...**
Placing documents before final instructions ensures Claude reads full context before evaluating the requested task.
</details>

---

**44.** How can you guarantee JSON structure without relying solely on system prompt text instructions?

A. Set `temperature: 1.0` under default system configuration within standard production deployment environments.  
B. Define a tool with JSON schema and force selection using `tool_choice: {"type": "tool", "name": "your_tool"}`.  
C. Use markdown bolding under default system configuration in enterprise system configurations.  
D. Send request twice under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**B — Define a tool with JSON schema and force selection using ...**
Forcing tool choice guarantees output adheres to the validated JSON schema at the API protocol level.
</details>

---

**45.** What is an "indirect prompt injection" attack?

A. An attacker directly typing malicious instructions into a chat box during standard production API invocation in enterprise system configurations.  
B. Intercepting HTTPS traffic via Wi-Fi during standard production API invocation in enterprise system configurations.  
C. Stealing API keys from server memory during standard production API invocation in enterprise system configurations.  
D. Untrusted data ingested from external sources (e.g. website, PDF, email) containing hidden instructions that hijack model behavior within standard production deployment environments.  

<details><summary>Answer</summary>
**D — Untrusted data ingested from external sources (e.g. websi...**
Indirect injection attacks hide prompt overrides inside data files processed by the model (e.g. web pages, PDFs).
</details>

---

**46.** Which strategy mitigates prompt injection when processing untrusted web content?

A. Increasing temperature to 1.0 across standard client implementation workflows within standard production deployment environments.  
B. Removing system prompts across standard client implementation workflows in enterprise system configurations.  
C. Placing untrusted content in XML tags (`<untrusted_content>`) and instructing Claude to treat it strictly as data.  
D. Disabling API error handling across standard client implementation workflows in enterprise system configurations.  

<details><summary>Answer</summary>
**C — Placing untrusted content in XML tags (`<untrusted_conten...**
XML framing establishes explicit data/instruction boundaries, preventing untrusted text from being parsed as commands.
</details>

---

**47.** What is the role of an input/output safety guardrail layer?

A. Increasing token generation speed under default system configuration in enterprise system configurations.  
B. Inspecting input prompts and model responses against safety rules before passing them downstream.  
C. Compressing JSON payloads under default system configuration within standard production deployment environments.  
D. Encrypting client hard drives under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**B — Inspecting input prompts and model responses against safe...**
Guardrails act as external policy filters, blocking harmful inputs and validating model outputs before display.
</details>

---

**48.** In Claude Code / agent development, what do Claude Hooks allow developers to do?

A. Modify Anthropic model weights locally during standard production API invocation in enterprise system configurations.  
B. Bypass authentication requirements during standard production API invocation in enterprise system configurations.  
C. Format text as PDF documents during standard production API invocation in enterprise system configurations.  
D. Execute custom shell scripts or validation logic before/after tool execution or user commands within standard production deployment environments.  

<details><summary>Answer</summary>
**D — Execute custom shell scripts or validation logic before/a...**
Claude Hooks provide lifecycle event callbacks for auditing, safety filtering, and automated checks in CLI/agent tools.
</details>

---

**49.** What three top-level keys are required in a tool definition object for the Messages API?

A. `url`, `method`, `headers` within standard production deployment environments.  
B. `id`, `type`, `value` in enterprise system configurations.  
C. `name`, `description`, `input_schema`  
D. `function`, `code`, `language`.  

<details><summary>Answer</summary>
**C — `name`, `description`, `input_schema`**
Every tool payload in the Messages API requires a unique string `name`, clear `description`, and valid JSON `input_schema`.
</details>

---

**50.** What does `tool_choice: {"type": "auto"}` specify?

A. Claude must call a tool on every single turn under default system configuration within standard production deployment environments.  
B. Claude decides whether to call a tool or respond with text based on conversation context.  
C. Disables tool calls completely under default system configuration in enterprise system configurations.  
D. Automatically executes tools without returning to client under default system configuration.  

<details><summary>Answer</summary>
**B — Claude decides whether to call a tool or respond with tex...**
`type: "auto"` leaves tool usage optional, allowing the model to answer directly or select a tool when appropriate.
</details>

---

**51.** What content block type must be sent to Claude when returning the output of a tool execution?

A. `type: "tool_result"` with `tool_use_id` and `content` within standard production deployment environments.  
B. `type: "text"` with raw string during standard production API invocation.  
C. `type: "system"` during standard production API invocation in enterprise system configurations.  
D. `type: "image"` during standard production API invocation in enterprise system configurations.  

<details><summary>Answer</summary>
**A — `type: "tool_result"` with `tool_use_id` and `content` wi...**
Tool outputs must be packaged inside `tool_result` content blocks referencing the exact `tool_use_id` from the model's call.
</details>

---

**52.** When a tool fails execution (e.g. database timeout), how should the client report the failure?

A. Throw a client exception and abort across standard client implementation workflows within standard production deployment environments.  
B. Return an empty string across standard client implementation workflows in enterprise system configurations.  
C. Return `type: "tool_result"` with `tool_use_id`, `content: "Error details...", is_error: true`.  
D. Delete tool definition from future requests across standard client implementation workflows.  

<details><summary>Answer</summary>
**C — Return `type: "tool_result"` with `tool_use_id`, `content...**
Flagging `is_error: true` informs Claude of execution failures structurally, facilitating graceful error handling or retries.
</details>

---

**53.** In Model Context Protocol (MCP), what is the difference between Resources and Tools?

A. Resources are read-only data streams (like GET); Tools perform actions or state mutations (like POST).  
B. Resources run on client; Tools run on server under default system configuration in enterprise system configurations.  
C. Resources use XML; Tools use JSON under default system configuration within standard production deployment environments.  
D. There is no difference under default system configuration in enterprise system configurations.  

<details><summary>Answer</summary>
**A — Resources are read-only data streams (like GET); Tools pe...**
In MCP architecture, Resources expose readable contextual data (like GET), while Tools execute executable functions (like POST).
</details>