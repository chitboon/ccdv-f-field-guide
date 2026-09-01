# CCDV-F Field Guide & Study Suite

An official-grade, community-maintained field guide and practice suite for the **Claude Certified Developer – Foundations** (CCDV-F) exam.

---

## Exam Blueprint & Specifications

- **Format:** 53 items · 120 minutes · Scaled score 100–1000 · Pass at 720
- **Cost / Validity:** $125 · 12 months validity · Proctored online or test centre

| Domain | Weight | Items | Domain Guide |
|---|---|---|---|
| **Agents and Workflows** | 14.7% | 8 | [01-agents-and-workflows.md](guide/01-agents-and-workflows.md) |
| **Applications and Integration** | **33.1%** | **18** | [02-applications-and-integration.md](guide/02-applications-and-integration.md) |
| **Claude Code** | 3.1% | 2 | [03-claude-code.md](guide/03-claude-code.md) |
| **Eval, Testing, and Debugging** | 2.6% | 1 | [04-eval-testing-and-debugging.md](guide/04-eval-testing-and-debugging.md) |
| **Model Selection and Optimization** | 16.8% | 9 | [05-model-selection-and-optimization.md](guide/05-model-selection-and-optimization.md) |
| **Prompt and Context Engineering** | 11.0% | 6 | [06-prompt-and-context-engineering.md](guide/06-prompt-and-context-engineering.md) |
| **Security and Safety** | 8.1% | 4 | [07-security-and-safety.md](guide/07-security-and-safety.md) |
| **Tools and MCPs** | 10.6% | 5 | [08-tools-and-mcps.md](guide/08-tools-and-mcps.md) |
| **Total** | **100%** | **53** | **Exact blueprint allocation** |

---

## What's Included in This Repository

1. **[Domain Mental Model Guides](guide/)**: Detailed technical notes and code patterns for all 8 blueprint domains.
2. **Practice Suite**:
   - **[API & LLM Diagnostic Quiz](practice/diagnostic-quiz/ccdv-f-diagnostic-quiz.md)** (15 items)
   - **[Phase 1 Concept Drills](practice/concept-drills/ccdv-f-concept-drills.md)** (53 items)
   - **[Phase 2 Scenario Domain Drills](practice/scenario-drills/ccdv-f-scenario-drills.md)** (53 items)
   - **Domain Drills (rebuilt, scenario-based, sealed key)** — 2×+ exam volume per domain (131 items total):
     [D1](practice/domain-drills/d1-domain-drill.md) (16) ·
     [D2](practice/domain-drills/d2-domain-drill.md) (52) ·
     [D3](practice/domain-drills/d3-domain-drill.md) (6) ·
     [D4](practice/domain-drills/d4-domain-drill.md) (6) ·
     [D5](practice/domain-drills/d5-domain-drill.md) (18) ·
     [D6](practice/domain-drills/d6-domain-drill.md) (15) ·
     [D7](practice/domain-drills/d7-domain-drill.md) (8) ·
     [D8](practice/domain-drills/d8-domain-drill.md) (10)
   - **[Full Mock Exam 1 (blueprint-exact, sealed key)](practice/mocks/mock-1.md)** (53 items, 8 multi-response)
   - **[Full Mock Exam 2 (blueprint-exact, sealed key)](practice/mocks/mock-2.md)** (53 items, 8 multi-response)
3. **Automated Quality & Provenance Gate Tools**:
   - `python3 tools/check-item-quality.py` — Evaluates position balance (chi-square), longest run (≤ 3), answer length ratio, and rank spread.
   - `python3 tools/check-provenance.py` — Provenance scanner ensuring 100% original rephrasings.
   - `python3 tools/check-nearclone.py` — Detects item overlap against reference papers.

---

## Audit Verification

Run item quality validation across all practice sets:

```bash
python3 tools/check-item-quality.py \
  practice/diagnostic-quiz/ccdv-f-diagnostic-quiz.md \
  practice/concept-drills/ccdv-f-concept-drills.md \
  practice/scenario-drills/ccdv-f-scenario-drills.md
```

The `domain-drills/` sets and both mocks use a sealed-key format (answers in a separate `*-key.md` file, not inline) and must be checked one set at a time with `--key`, e.g.:

```bash
python3 tools/check-item-quality.py practice/mocks/mock-1.md \
  --key practice/mocks/mock-1-key.md
python3 tools/check-item-quality.py practice/domain-drills/d2-domain-drill.md \
  --key practice/domain-drills/d2-domain-drill-key.md
```

Substitute `d1` through `d8` for the other seven domains. All 5 flat practice sets plus all 8 domain-drill sets pass all 9 cue quality targets (`check-item-quality.py`), the provenance scan, and the near-clone check.

---

## Sources & License

- See [SOURCES.md](SOURCES.md).
- Released under [CC BY 4.0](LICENSE).
- Unofficial study guide. Not affiliated with, endorsed by, or sponsored by Anthropic.
