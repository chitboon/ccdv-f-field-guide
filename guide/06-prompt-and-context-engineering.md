# Domain 6: Prompt and Context Engineering (11.0% · 6 Items)

## Overview

Domain 6 covers the systematic design of prompts, context formatting, XML tag delimiting, few-shot demonstration strategies, structured output generation, and context window optimization.

---

## 1. XML Tag Delimiting & Recency Attention Weighting

Claude is trained to understand structured XML tags as structural semantic boundaries:

```xml
<system>
You are an expert financial claims auditor. Follow these rules:
1. Base all conclusions strictly on facts inside <policy_documents>.
2. If the policy does not state a coverage rule, respond with "UNKNOWN".
</system>

<policy_documents>
{{RELEVANT_INGESTED_POLICY_TEXT}}
</policy_documents>

<instructions>
Evaluate the claim below. First reason inside <thinking> tags, then emit your verdict.
</instructions>

Claim: {{CLAIM_DETAILS}}
```

### Key Formatting Invariants
* **Role Separation:** Encapsulate background documentation inside `<policy_documents>` and operational rules inside `<instructions>` to prevent document text from contaminating behavioral instructions.
* **Recency Attention Effect:** In prompts with long reference context, place the background documents **first** and place the operative question/instruction **at the bottom** after closing tags. This ensures the model’s attention mechanism focuses on the immediate task.

---

## 2. Few-Shot Exemplars

When zero-shot prompts fail to produce the exact formatting or edge-case handling desired, provide 2–3 canonical input/output examples inside `<examples>` tags:

```xml
<examples>
  <example>
    <input>Refund requested for order #102: item damaged in transit.</input>
    <output>{"category": "DAMAGE_TRANSIT", "priority": "HIGH", "action": "AUTO_REFUND"}</output>
  </example>
  <example>
    <input>Customer inquiry for order #105: where is my package?</input>
    <output>{"category": "TRACKING_INQUIRY", "priority": "LOW", "action": "SEND_TRACKING_LINK"}</output>
  </example>
</examples>
```

* **Why Exemplars Beat Prose:** Few-shot examples anchor the output distribution significantly better than lengthy multi-paragraph prose descriptions.
* **Consistency:** Ensure exemplars match the exact syntax, casing, and schema required.

---

## 3. Affirmative Phrasing & Chain-of-Thought (CoT)

* **Affirmative Phrasing:** State desired behavior positively (*"Provide 3 concise bullet points explaining the outcome"*) rather than negatively (*"Do not write paragraphs, do not be verbose"*). Negative constraints frequently pull formatting toward the banned behavior.
* **Chain-of-Thought Reasoning:** For complex logic, policy evaluations, or mathematical deductions, prompt Claude to think step-by-step inside `<thinking>` tags before emitting the final answer. This forces intermediate validation and prevents hasty errors.

---

## 4. Structured Output: Schema Enforcement vs. Deprecated Prefilling

When your application requires strict JSON:

* **MODERN APPROACH (Structured Outputs / Tools):**
  * Use tool definitions with `input_schema` or `output_config: {format: {...}}`.
  * The SDK’s `messages.parse()` helper automatically deserializes and validates against Pydantic models.
* ⚠️ **RETIRED ANTI-PATTERN (Assistant Prefilling):**
  * In earlier models, developers prefilled the assistant turn with `{"role": "assistant", "content": "{"}` to force raw JSON.
  * On current Claude models, assistant message prefilling **returns HTTP 400 Bad Request**. Enforce structure via tool definitions or structured outputs instead.

---

## 5. Defensive Parsing & Input Sanitization

### Input Sanitization is Structural, Not Escaping
* In standard software, sanitization involves escaping characters (e.g. `htmlspecialchars` or SQL escaping).
* For LLMs, string escaping provides negligible protection against prompt injection. Instead, **input sanitization is structural**:
  1. Wrap untrusted user data in explicit tags (e.g. `<user_input>`).
  2. Declare in `system` that content within `<user_input>` represents data to be processed, never executable instructions.
  3. Place operative rules after the untrusted data block.

### Defensive Output Parsing
Never assume model output is guaranteed to parse cleanly:
* Always wrap `json.loads()` or schema deserialization in exception handlers.
* Avoid brittle regex string slicing (e.g. stripping text before the first `{`), which fails if the JSON content contains nested braces or string literals.

---

## 6. Output Bounding via `stop_sequences`

* Pass an array of strings in `stop_sequences=["\n\n", "</claim_review>"]` at request time.
* The API halts generation the instant any stop sequence is encountered, setting `stop_reason: "stop_sequence"`.
* Note: A stop sequence halts generation on the matching string, but does not alter preceding characters generated on the same line.

---

## 7. Summary Checklist: Exam Invariants for Domain 6

- [ ] Place reference documents first and actionable instructions at the bottom.
- [ ] 2–3 few-shot examples inside `<examples>` outperform long prose instructions.
- [ ] Use affirmative phrasing; specify what to produce rather than what to omit.
- [ ] Instruct CoT reasoning inside `<thinking>` tags for multi-step logic.
- [ ] Assistant prefilling is retired and returns HTTP 400; use tool schemas or structured outputs.
- [ ] Input sanitization means XML delimiting and role separation, not character escaping.
- [ ] Defensive parsing must handle schema and JSON decode exceptions gracefully.
