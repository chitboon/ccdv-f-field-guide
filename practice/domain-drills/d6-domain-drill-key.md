# CCDV-F Domain Drill — Domain 6: key and rationales

Grade in one deferred pass. For every miss, note which it was: didn't know
it, misread the item, or picked the plausible-but-soft option.

---

**1. B** — Wrapping `return_policy_doc` in `<policy_docs>` and behavioral constraints in `<guidelines>` provides unambiguous structural demarcation in the prompt string, preventing context contamination. Shortening the document or appending stop sequences does not resolve the lack of structural demarcation. *(task 6.1; concept: xml_section_delimiting; item `d6d-01`)*

---

**2. C** — Live input/output example pairs show the exact formatting rather than describing it, which is what few-shot prompting is for and is far more reliable than prose alone. Repeating the same prose instruction three times doesn't add new information; a larger `max_tokens` addresses truncation, not formatting drift; and moving the instruction to the user turn changes where it lives, not whether it's demonstrated. *(task 6.1; concept: few_shot_pattern_demonstration; item `d6d-02`)*

---

**3. D** — Appending `{"role": "assistant", "content": "{"}` as the final element of `messages` natively forces Claude to continue emitting JSON tokens from that opening character, bypassing any preamble. The application then parses `"{" + response.content[0].text`. Stop sequences, user prompt tricks, or invalid `"role": "system"` inside `messages` do not provide native assistant continuation. *(task 6.1; concept: assistant_prefill; item `d6d-03`)*


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

---

**13. B** — `stop_sequences` halts generation the moment the given string appears in the output, so `"\n"` cuts off anything Claude writes after the label on a following line — but it does nothing if Claude puts the justification on the *same* line as the label, so it narrows the failure mode rather than eliminating it structurally. Lowercasing, cost, and replacing `max_tokens` are all unrelated to what a stop sequence actually controls. *(task 6.3; concept: stop_sequences_output_boundary; item `d6d-13`)*

---

**14. A** — A cached block is matched as one exact prefix, so a value that changes on every request (the timestamp) sitting inside that block invalidates the whole segment's prefix match every single time, regardless of how stable the rest of the content is. Moving the volatile part out (after the stable content, or into its own block) restores a stable prefix for `company_docs` to actually get cached. Removing `cache_control`, raising the token count, or lengthening the TTL don't address the actual cause — a prefix that never repeats. *(task 6.2; concept: cached_prefix_stability; item `d6d-14`)*

---

**15. A** — Checking each chunk as it arrives inside the streaming loop is what lets the application react the moment the refusal phrase appears, instead of waiting for the entire response to buffer first — that's the whole point of consuming `text_stream` incrementally rather than only at the end. `get_final_text()` still waits for the full response, a low `max_tokens` doesn't guarantee an early enough cutoff for detection, and polling with fresh requests abandons streaming rather than using it correctly. *(task 6.3; concept: incremental_stream_parsing; item `d6d-15`)*

