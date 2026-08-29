# Domain 6: Prompt Crafting & Context Engineering (11.0% Weight · 6 Items)

## Overview
Domain 6 tests XML tags, system prompt structuring, few-shot demonstration design, structured output techniques, and context window management.

---

## Core Technical Techniques

### 1. XML Tag Structure
- Claude is fine-tuned to process structured XML tags (`<system>`, `<context>`, `<instructions>`, `<example>`, `<documents>`).
- Wrap retrieved documents in XML containers to prevent prompt injection and context confusion.

### 2. Structured Output & Prefilling
- **JSON Schema via Tools:** Define tool parameters with strict JSON schemas to force structured response formats.
- **Assistant Message Prefilling:** Prefill assistant response text (e.g. `{`) to enforce direct JSON output without conversational preambles.

### 3. Few-Shot Exemplars
- Provide 2–3 concrete input/output examples inside `<example>` XML tags to establish exact output format and edge-case handling.
