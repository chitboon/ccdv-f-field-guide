# CCDV-F Domain Drill — Domain 4: key and rationales

Grade in one deferred pass. For every miss, note which it was: didn't know
it, misread the item, or picked the plausible-but-soft option.

---

**1. C** — Code-based assertions work when there's one shape of right answer, like an enum; open-ended text needs a second LLM call scoring it against a rubric instead. Extending the schema can't judge free-text quality, dropping the field loses coverage entirely, and using a judge for the enum too throws away a cheaper, deterministic check that already works. *(task 4.1; concept: code_assertion_vs_judge; item `d4d-01`)*

---

**2. A** — Pairing known-correct extractions with deliberately broken edge cases like the missing signature block is exactly what a golden eval set is for: it catches failures a single-client demo never would. Throughput, injection probing, and supervised fine-tuning are all different purposes that fifty labeled documents could serve, but none matches what's described here. *(task 4.1; concept: golden_eval_dataset_construction; item `d4d-02`)*

---

**3. D** — Any prompt change needs to clear the existing golden set before shipping, precisely so a regression like the climbing error rate gets caught pre-deployment instead of discovered live. Temperature, staff sign-off on wording, and `max_tokens` are all unrelated to whether the rewritten prompt still classifies correctly. *(task 4.1; concept: regression_testing_prompt_change; item `d4d-03`)*

---

**4. B** — Systematic debugging means narrowing down which layer — prompt, tool schema, model, or application code — actually owns the failure before touching anything, which is exactly the step three engineers skipped by changing three different layers at once. Rolling back, paging based on ownership, and adding retries all react to the symptom without first locating its cause. *(task 4.1; concept: systematic_root_cause_debugging; item `d4d-04`)*

---

**5. C** — A response cut off mid-sentence paired with `stop_reason: max_tokens` is the signature of silent truncation: the model simply ran out of budget before finishing, and the field confirms it directly. Hallucination, tool misuse, and format drift each describe a different failure and would be confirmed by checking different evidence entirely. *(task 4.1; concept: failure_mode_silent_truncation; item `d4d-05`)*

---

**6. D** — Logging the full request, response, and intermediate tool calls per transaction produces a complete audit trail that makes intermittent failures diagnosable after the fact. Dashboard panels, lower alert thresholds, and longer retention windows only display aggregate statistics and cannot reveal the specific payload or failure mode of an individual transaction. *(task 4.1; concept: production_observability_logging; item `d4d-06`)*

---

**7. A** — Model-as-a-Judge evaluators are susceptible to verbosity bias (favoring longer answers); explicitly anchoring rubric criteria to penalize fluff and reward concise factual density calibrates scoring behavior. Eliminating the LLM judge discards semantic grading; hardcoding `max_tokens=50` truncates valid outputs; and switching model size does not fix rubric formulation. *(task 4.1; concept: llm_judge_verbosity_bias; item `d4d-07`)*

---

**8. B** — Using an LLM with few-shot adversarial prompts to generate synthetic variations (typos, colloquialisms, edge cases) proactively hardens the golden dataset against real-world distributions before deployment. Waiting for production failures exposes users to bugs; duplicating clean rows adds no diversity; and radio buttons eliminate conversational flexibility. *(task 4.1; concept: synthetic_edge_case_generation; item `d4d-08`)*

---

**9. D** — Plotting an Accuracy vs. Cost/Latency Pareto frontier on the golden dataset provides an objective trade-off curve to determine if accuracy improvements justify additional latency and token expenditure. Memory benchmarks ignore model accuracy; direct production deployment risks customer churn and unbudgeted costs; and local laptop tests lack statistical validity. *(task 4.1; concept: pareto_tradeoff_benchmarking; item `d4d-09`)*

---

**10. A** — Running automated multi-turn synthetic dialogues with per-turn JSON schema assertions validates format stability across multi-step conversations, catching late-turn format drift before production deployment. Higher temperatures increase randomness; single-turn manual inspection is blind to multi-turn degradation; and eliminating multi-turn flows breaks conversational UX. *(task 4.1; concept: multiturn_format_drift_testing; item `d4d-10`)*
