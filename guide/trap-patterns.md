# Trap Patterns — CCDV-F

Twelve core architectural and cognitive judgement traps frequently encountered on the CCDV-F exam: how each trap presents in a scenario, a concrete example, and the exact architectural discrimination that resolves it.

---

## 1. `stop_reason` Loop Control vs. Text Presence

**Objective 1.1 / 1.2 — Agent Loops & Workflows**

* **The Trap:** The model’s generated response contains conversational text (e.g., *"I have located the account and will now update the address"*), and the developer treats the presence of text as a completion signal, exiting the loop before the tool executes.
* **The Scenario:** An order management agent receives a user request. In its response turn, Claude emits text along with a `tool_use` block for `update_shipping_address`. The application loop inspects `response.content[0].text`, assumes the agent is responding to the user, and terminates without running the tool.
* **The Resolution:** **Prose is never a termination signal.** Autonomous loops must branch strictly on `stop_reason`. If `response.stop_reason == "tool_use"`, the loop must execute the tool and return the `tool_result`. Only terminate when `response.stop_reason == "end_turn"`.

---

## 2. Insecure Output Handling (OWASP LLM02) vs. Prompt Injection

**Objective 7.2 — Security & Vulnerability Remediation**

* **The Trap:** A question describes an application where untrusted web content leads to model-generated HTML or JavaScript executing in a user's browser (Cross-Site Scripting). Options tempt you to add prompt injection filters or system prompt warnings.
* **The Scenario:** A customer service dashboard summarizes user reviews using Claude and displays the summary on a web portal using `element.innerHTML = modelOutput`. A malicious reviewer injects an XSS payload that Claude mirrors in the summary.
* **The Resolution:** **This is an OUTPUT-side vulnerability (OWASP LLM02 Insecure Output Handling).** Filtering inputs or instructing Claude not to generate script tags fails because LLM outputs are non-deterministic and can be manipulated via indirect prompt injection. The correct remediation is **output-side context-aware escaping** (e.g. using `textContent` or HTML entity sanitizers) and treating all model outputs as untrusted data at the render boundary.

---

## 3. PreToolUse vs. PostToolUse Hook Lifecycles

**Objective 3.1 & 7.3 — Tool Execution Hooks**

* **The Trap:** Confusing the timing and authority of pre-execution vs. post-execution hooks.
* **The Scenario:** A developer wants to prevent an autonomous coding agent from executing dangerous shell commands (such as `rm -rf /` or unauthorized file deletion) and also ensure that any AWS secret access keys printed in command outputs are not stored in conversation history.
* **The Resolution:**
  * **`PreToolUse` Hook:** Runs *before* execution. Inspects proposed arguments and has the authority to **block/reject destructive actions** before the shell or database executes them.
  * **`PostToolUse` Hook:** Runs *after* execution. Inspects returned output and **sanitizes/masks sensitive data (PII, secrets)** before appending results into conversational context.

---

## 4. Tool Runner vs. Agent SDK vs. Managed Agents

**Objective 1.2 / 8.3 — Agent Development Toolkits**

* **The Trap:** Conflating Anthropic's distinct agent packages and execution tiers.
* **The Resolution:**
  * **Tool Runner (`client.beta.messages.tool_runner`):** Part of the standard Anthropic SDK. Loops over **only the tools you define**. Provides per-turn hooks, retries, and state management. Ships with **zero built-in tools**.
  * **Claude Agent SDK:** A separate package (Claude Code as a library). Ships with **built-in developer tools** (`Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`). Harness-only and self-hosted.
  * **Managed Agents:** Anthropic-hosted end-to-end agent service. Supplies **both** execution harness and sandboxed deployment containers hosted by Anthropic.

---

## 5. SDK Version Pinning vs. Server-Side Deprecation

**Objective 5.2 — Technical Fundamentals & SDK Wrappers**

* **The Trap:** Assuming that pinning the Python/Node SDK version in application dependencies will prevent breaking changes caused by Anthropic server-side API retirements.
* **The Scenario:** A production system pins `anthropic==0.25.0` in `requirements.txt`. Anthropic deprecates a legacy parameter on the server. An engineer claims the application is immune to breaking changes because the SDK version is locked.
* **The Resolution:** The Anthropic Messages API is **stateless and server-side**. Pinning the client SDK protects client code from client-side breaking changes, but **cannot force Anthropic's server to accept retired request shapes or parameters**. Upstream API contract changes must be addressed at the payload level.

---

## 6. Tool `description` vs. `strict: true`

**Objective 8.1 — Tool Definition & Schema**

* **The Trap:** Relying on `strict: true` in tool schemas to control *when* Claude invokes a tool.
* **The Scenario:** An application defines two tools with similar parameters: `search_customers` and `search_orders`. Both use `strict: true`. In production, Claude frequently invokes `search_customers` when users ask about order status.
* **The Resolution:** `strict: true` validates only syntactic JSON schema conformance (types, enums, required fields). It provides **zero semantic guidance** on whether invoking the tool is appropriate. The natural language **`description` is the specification** for Claude. Write detailed, unambiguous descriptions explaining the exact conditions under which the tool should and should not be invoked.

---

## 7. Structural Multi-Tenant Isolation vs. Prompt-Level Prefixes

**Objective 2.5 — Session Lifecycle & Security Architecture**

* **The Trap:** Attempting to enforce multi-tenant customer data isolation using natural language prefixes inside a shared conversational thread.
* **The Scenario:** A SaaS platform serves multiple enterprise tenants through a single persistent agent loop, prefixing each message with `[Tenant: AcmeCorp]`. A prompt injection in a customer support ticket tricks the agent into summarizing prior turns from another tenant.
* **The Resolution:** Multi-tenant boundaries must be **structural in the data architecture**:
  1. Maintain dedicated, separate `messages[]` arrays per tenant.
  2. Inject tenant-specific security policies into the top-level `system` parameter.
  3. Partition prompt caching prefixes independently per tenant.

---

## 8. Model Selection: Quality First vs. Cost/Latency Filters

**Objective 5.1 / 5.3 — Model Selection & Tradeoffs**

* **The Trap:** Starting model evaluation by selecting the cheapest or fastest model and attempting to prompt-engineer it into passing complex reasoning tasks.
* **The Scenario:** An engineering team building a multi-step code refactoring agent begins testing with a fast/lightweight model tier to minimize costs, spending weeks writing complex prompts to prevent formatting and logical failures.
* **The Resolution:** **Meet the quality bar first.** Always benchmark the workflow against the highest-capability tier to establish task feasibility and ground-truth baseline accuracy. Once feasibility is proven, evaluate whether a balanced or lightweight model can achieve acceptable accuracy. Hard cost and latency limits act as *filters* on the candidate pool, not the initial optimization target.

---

## 9. Parallel Tool Bundling: Single Turn vs. Sequential Messages

**Objective 2.1 / 8.1 — Parallel Tool Execution**

* **The Trap:** Responding to multiple parallel `tool_use` blocks with multiple sequential HTTP messages.
* **The Scenario:** Claude emits two parallel tool calls: `get_weather(city="Tokyo")` and `get_weather(city="Paris")`. The client executes Tokyo, sends a `role: "user"` message with Tokyo's result, then attempts to send another `role: "user"` message with Paris's result.
* **The Resolution:** Consecutive same-role messages violate API rules. The application must execute all parallel tool calls and return a **single message with `role: "user"`** containing the complete array of `tool_result` blocks for **every** `tool_use_id`.

---

## 10. Usage Billing Accounting & Separate Cache Counters

**Objective 5.4 — Cost & Usage Optimization**

* **The Trap:** Calculating total prompt token spend by summing only `input_tokens + output_tokens`.
* **The Scenario:** A billing pipeline tracks Claude API spend by extracting `usage.input_tokens` and `usage.output_tokens`. Finance notices a massive discrepancy between internal calculations and Anthropic's monthly invoice.
* **The Resolution:** `cache_creation_input_tokens` (billed at 1.25×) and `cache_read_input_tokens` (billed at 0.10×) are reported as **separate counters outside `input_tokens`**. On cached requests, `input_tokens` only counts the uncached suffix. Summing only `input_tokens + output_tokens` ignores the cached volume and under-reports actual spend.

---

## 11. Silent Truncation Detection

**Objective 2.1 / 4.1 — API Diagnostics & Truncation**

* **The Trap:** Assuming that an HTTP 200 response with well-formed text indicates successful, complete generation.
* **The Scenario:** A document synthesis service receives truncated summaries from Claude that cut off mid-sentence. The HTTP status is 200, and no exception is thrown by the SDK.
* **The Resolution:** Always inspect `response.stop_reason`. A `stop_reason == "max_tokens"` indicates that generation was cut off abruptly by token limits. Applications must detect this condition and trigger a continuation request or raise `max_tokens`.

---

## 12. Batch API Non-Deterministic Ordering

**Objective 2.2 / 5.4 — Batch Processing**

* **The Trap:** Correlating Message Batch results with submitted items using array index order (`zip(inputs, results)`).
* **The Scenario:** A batch job submits 500 document classification requests. The processing script iterates through `client.messages.batches.results()` assuming result #0 corresponds to input #0. Classifications are mismatched across all documents.
* **The Resolution:** Message Batch results are returned in **non-deterministic order**. Applications must assign a unique, deterministic **`custom_id`** to every request in the batch and correlate output results strictly by matching `result.custom_id`. Furthermore, verify `result.type == "succeeded"` before accessing `.message`.
