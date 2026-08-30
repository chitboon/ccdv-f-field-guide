# CCDV-F Domain Drill — Domain 6: key and rationales

Grade in one deferred pass. For every miss, note which it was: didn't know
it, misread the item, or picked the plausible-but-soft option.

---

**1. B** — Wrapping the reference material in `<context>` and the behavioral rules in `<instructions>` gives Claude a structural signal for which content is source data and which is a rule to follow, stopping the cross-contamination. Shortening the document just reduces its size without fixing the mixing; moving the whole block unchanged into a user turn keeps the same ambiguity; and asking Claude to disregard wording in a later turn is a patch that won't hold across new conversations. *(task 6.1; concept: xml_section_delimiting; item `d6d-01`)*

---

**2. C** — Live input/output example pairs show the exact formatting rather than describing it, which is what few-shot prompting is for and is far more reliable than prose alone. Repeating the same prose instruction three times doesn't add new information; a larger `max_tokens` addresses truncation, not formatting drift; and moving the instruction to the user turn changes where it lives, not whether it's demonstrated. *(task 6.1; concept: few_shot_pattern_demonstration; item `d6d-02`)*

---

**3. D** — Pre-filling the assistant turn with `{` forces the reply to continue as a JSON value from that exact character, eliminating the preface entirely. A stop sequence on the preface text only stops generation after it's already started being written; raising temperature makes phrasing less predictable, not more; and pushing cleanup work onto the client just works around a preventable server-side issue. *(task 6.1; concept: assistant_prefill; item `d6d-03`)*

---

**4. A** — Reasoning through each factor step by step before stating a verdict gives the model room to work through the combination consistently, which is the point of chain-of-thought prompting for multi-step reasoning. Skipping explanation removes exactly the reasoning space that's missing; capping `max_tokens` at 1 would cut off any answer at all, not just improve consistency; and moving the combination outside the prompt sidesteps the reasoning task rather than improving it. *(task 6.1; concept: chain_of_thought_reasoning; item `d6d-04`)*

---

**5. B** — A style described only in the abstract gives the model nothing concrete to match; a single worked example of the desired concise, formal tone would give it a pattern to follow. Style guidance can live in the system prompt just fine, so relocating it isn't the fix; "concise" being read as "one sentence" doesn't match the reported symptom of casual, wordy output; and nothing in the scenario suggests the instruction is being crowded out of context. *(task 6.1; concept: worked_example_over_description; item `d6d-05`)*

---

**6. C** — Replacing a negative instruction with a positive description of the desired form gives the model something to aim for, rather than only something to avoid, which tends to hold up better against pull from the input material. Restating the same negative instruction more forcefully doesn't change what it's asking for; removing the instruction removes any guidance at all; and relocating an unchanged prohibition to a different part of the prompt doesn't change its phrasing. *(task 6.1; concept: positive_instruction_framing; item `d6d-06`)*

---

**7. D** — Policy, tone, and escalation rules are stable across turns, which is exactly what the system prompt is for, leaving the user message to carry only what's specific to that turn's question. Reordering content within the user message doesn't change where the stable material lives; splitting it evenly doesn't address the underlying mismatch; and moving the turn-specific question into the system prompt puts the wrong content in the persistent slot. *(task 6.2; concept: system_prompt_vs_user_message; item `d6d-07`)*

---

**8. A** — Summarizing or dropping the oldest middle turns while keeping the system prompt and the opening turn intact controls context growth without losing the instructions or the original problem statement. Truncating the system prompt removes the very instructions the team wants preserved; starting over with no context loses the opening problem statement entirely; and sending the full history unmodified is exactly the growth the team is trying to avoid. *(task 6.2; concept: long_conversation_context_management; item `d6d-08`)*

---

**9. C** — A content block with `type: "image"` and a `source` object specifying `type: "base64"`, the correct `media_type`, and the base64 `data` is the structured way multimodal image input is represented in a request. Embedding the base64 string as plain text loses the structural markers the model relies on to treat it as image data; a `tool_result` block is for returning tool output, not for submitting user-supplied images; and there is no persistent system-prompt slot for image bytes. *(task 6.2; concept: multimodal_image_content_block; item `d6d-09`)*

---

**10. D** — Wrapping each document in `<document>` tags and placing the marked question after the closing tags gives the model a clear boundary between reference text and the actual instruction to act on. Deleting sources doesn't fix the lack of a boundary, it just reduces how often the confusion can occur; moving the question into the system prompt doesn't establish where the documents end; and capitalizing the question is a cosmetic change with no structural effect. *(task 6.2; concept: reference_material_boundary_tags; item `d6d-10`)*

---

**11. A** — A tool with a strict schema, such as a boolean `approved` field, forces the decision into structured arguments that a downstream script can read directly, instead of hunting for a keyword inside free-form prose. Restricting Claude to a single bare word still leaves a fragile string match on the other end; switching to `startswith` only narrows where the same substring bug can happen; and asking for markdown emphasis around the word is still a string-matching approach with a different search string. *(task 6.3; concept: tool_use_over_string_matching; item `d6d-11`)*

---

**12. B** — Validating the returned arguments against the schema right after the call catches a malformed type like a string `"null"` immediately, with a clear error, instead of letting it flow downstream to fail opaquely later. Automatic retries don't address a response that returns successfully but with the wrong type; logging for a weekly human review doesn't stop the bad value from being used in the meantime; and raising `max_tokens` has no bearing on whether a returned field has the correct type. *(task 6.3; concept: structured_output_validation; item `d6d-12`)*
