# CCDV-F Domain Drill — Domain 4: Eval, Testing, and Debugging

6 items, one correct answer each. Untimed. Answer all 6 first, then grade
against the key in one pass — item by item, reading each rationale,
including the ones you got right. This is a small, single-sub-objective
domain on the real exam, but the drill still gives you a full sitting of
practice against it.

---

**1.** `[task 4.1 · code assertion vs model-as-judge]` A code-review bot returns JSON with a `severity` field (enum: low/medium/high) and a `summary` field (free text explaining the issue). The team already validates `severity` against a JSON schema, but two engineers disagree on how to grade `summary`, since correct summaries can differ completely in wording. What should the eval do?

A. Extend the JSON schema to cover `summary` too, rejecting any phrasing the validator hasn't already been given as an example.
B. Remove `summary` from the eval altogether, since only enum-shaped fields can be checked without a second model call.
C. Keep the schema validator for `severity` and add a Model-as-a-Judge call that scores `summary` against a written rubric.
D. Replace the schema validator with a Model-as-a-Judge call for both fields so one grading method covers the whole payload.

---

**2.** `[task 4.1 · golden eval dataset construction]` A team building a contract-clause extractor has only tested it against contracts from one client, so every extraction the demo shows looks correct. Before wider rollout, an engineer proposes assembling 50 contracts with known-correct extracted fields, including three intentionally malformed contracts missing a signature block. What is this engineer building?

A. A golden eval dataset, since it pairs known-correct answers with edge cases the extractor must also handle correctly.
B. A load-testing harness, since 50 documents is enough volume to estimate the extractor's throughput under concurrent requests.
C. A prompt-injection test suite, since malformed contracts are the standard way to probe for injected instructions.
D. A fine-tuning corpus, since labeled examples like these are what gets fed into a supervised training run.

---

**3.** `[task 4.1 · regression test before shipping]` A support-ticket classifier prompt has been passing 38/40 items on the team's golden eval set for months. An engineer rewrites the prompt to fix a wording complaint from support staff and, without re-running the eval, ships it directly to production, where the classification error rate quietly climbs over the next two days. What step was skipped?

A. Increasing `max_tokens` for the classification call, since longer completions typically reduce ticket misclassification rates overall.
B. Lowering the model's temperature setting, since a wording change alone should never affect classification accuracy at all.
C. Asking support staff to approve the new wording, since their original complaint was about tone rather than accuracy.
D. Re-running the golden eval set against the new prompt before shipping, to catch any regression versus the 38/40 baseline.

---

**4.** `[task 4.1 · systematic root-cause debugging]` A tool-using agent starts failing roughly 1 in 5 calls to a `lookup_order` tool in production. One engineer immediately swaps in a different model, another rewrites the system prompt, and a third adds more few-shot examples — all within an hour, none of it fixing the failure rate. What did the team skip before making changes?

A. Rolling back to the previous production deployment immediately, since any regression should be reverted before it is investigated.
B. Isolating whether the failure traces to the prompt, the tool schema, the model choice, or the application code before changing anything.
C. Paging the on-call engineer for `lookup_order`, since ownership of the failing tool determines who should fix it.
D. Increasing the retry count on `lookup_order` calls, since intermittent failures are usually resolved by trying again.

---

**5.** `[task 4.1 · silent truncation detection]` A document-summarization response consistently ends with an unfinished sentence such as "The vendor agreed to" whenever the source document exceeds roughly 3,000 words, and the API response's `stop_reason` field reads `max_tokens` in every one of those cases. Which failure mode is this, and how would you confirm it?

A. Tool misuse — confirmed by checking whether the model invoked a tool it was never given permission to call.
B. Hallucination — confirmed by comparing the summary's claims against facts actually present in the source document.
C. Silent truncation — confirmed by the `stop_reason` field reading `max_tokens` rather than a natural end-of-turn stop.
D. Format drift — confirmed by validating the response's structure against the schema the API contract requires.

---

**6.** `[task 4.1 · production logging for diagnosability]` A production agent has been failing intermittently for a week, but when engineers investigate, the only surviving record is a `status: error` line in an aggregate metrics dashboard — no request, no response, no intermediate tool calls. What logging practice would have made this incident diagnosable after the fact?

A. Adding a second dashboard panel that graphs error rate against request volume over the same time period.
B. Lowering the alert threshold on the metrics dashboard, so smaller error-rate increases trigger a page sooner next time.
C. Increasing the retention window on the aggregate dashboard, so last week's error count stays visible for longer.
D. Logging the full request, response, and intermediate tool calls per transaction, not just an aggregate error count.

---

**7.** `[task 4.1 · LLM judge calibration & verbosity bias]` An automated Model-as-a-Judge pipeline evaluates technical support explanations generated by Claude. Reviewing the evaluation logs, QA notices that the evaluator model consistently assigns higher scores (5/5) to lengthy, 4-paragraph responses filled with pleasantries, while penalizing concise, 2-sentence responses that are factually complete and more accurate. What evaluation calibration adjustment fixes this verbosity bias?

A. Anchor the judge prompt with explicit rubric criteria penalizing extraneous prose and rewarding factual density.
B. Remove the LLM judge completely and replace semantic evaluation with character-count length thresholds in Python.
C. Lower the evaluated model's `max_tokens` to 50 so all candidate responses are physically forced to be ultra-short.
D. Switch the judge model to a smaller high-speed model that cannot process multi-paragraph outputs during evals.

---

**8.** `[task 4.1 · synthetic edge case generation for golden sets]` A healthcare startup prepares to benchmark an appointment-scheduling assistant. Historical customer chat logs only contain standard English phrases, but production users frequently submit typos, medical abbreviations, and regional colloquialisms. The team needs to stress-test the intent recognition pipeline against these rare patterns before launch. How should the team expand its golden evaluation dataset?

A. Wait until production deployment generates real customer failures, then retrospectively add them to the test suite.
B. Use an LLM with few-shot adversarial prompts to generate synthetic dialect variations and realistic user typos.
C. Duplicate existing clean benchmark examples ten times each to artificially increase the size of the test suite.
D. Restrict the production user interface to radio buttons only, eliminating free-form conversational user inputs.

---

**9.** `[task 4.1 · Pareto trade-off benchmarking across model candidates]` An engineering team evaluates whether to replace Claude 3.5 Haiku with Claude 3.5 Sonnet in an entity-extraction microservice processing 500,000 documents daily. To make a data-driven architectural decision, what metric benchmarking analysis should the team run against their golden evaluation dataset?

A. Benchmark solely on peak memory consumption across worker nodes, ignoring token pricing and task accuracy scores.
B. Deploy Claude 3.5 Sonnet directly to 100% of production traffic for a month and analyze total cloud billing costs.
C. Measure single-turn prompt latency on an engineer's local laptop without executing evaluation dataset assertions.
D. Plot an Accuracy vs. Cost/Latency Pareto frontier across both models on the golden set to verify accuracy gains.

---

**10.** `[task 4.1 · multi-turn format drift detection]` A multi-turn customer intake agent is required to return an updated JSON summary object at the end of every conversation turn. In production, developers observe that while turns 1 through 3 produce valid JSON, by turn 8 the model's output drifts into unstructured conversational bullet points, breaking downstream database parsers. What testing practice would have caught this regression during CI?

A. Executing automated multi-turn synthetic conversation runs with per-turn JSON schema validation assertions in CI.
B. Increasing the system prompt's temperature setting to 1.0 so output formats vary more widely during unit tests.
C. Manually inspecting the first turn of every test case and assuming subsequent conversational turns stay identical.
D. Removing the multi-turn conversational requirement and forcing users to submit all intake data in a single turn.

