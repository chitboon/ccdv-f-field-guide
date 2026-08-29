# Domain 4: Evaluation, Testing, and Debugging (2.6% Weight · 1 Item)

## Overview
Domain 4 covers evaluation frameworks, LLM output quality testing, automated scoring, and systematic error diagnosis.

---

## Core Technical Concepts

### 1. Evaluation Architecture
- **Deterministic Assertion Tests:** Checking JSON schema compliance, exact key presence, regex pattern matching, or unit test suite execution.
- **LLM-as-a-Judge:** Using a stronger model (e.g. Claude 3.5 Sonnet) with clear evaluation rubrics to score complex responses.

### 2. Systematic Error Diagnosis
- Trace full API request/response payloads when debugging model hallucinations or unexpected tool parameter formats.
- Differentiate between API network errors (4xx/5xx), model reasoning errors (wrong tool chosen), and schema validation failures (malformed tool arguments).
