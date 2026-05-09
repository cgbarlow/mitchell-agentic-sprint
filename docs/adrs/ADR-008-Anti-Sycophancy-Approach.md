# ADR-008: Anti-Sycophancy via Dragon-Style Preambles + Behavioural-Interview Linter

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-008 |
| **Initiative** | Anti-sycophancy enforcement (concept §6, §10) |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-09 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** the concept's headline promise that MAS is adversarial-by-default — refusing flattery, banning hypothetical questions, demanding citations — and the gap analysis identifying that prompt-level adversarial framing closes most of the gap while a verification eval set is deferred to v0.2.0,

**facing** the choice of how to operationalise anti-sycophancy across the v0.1.0 surface area: prompts only (cheap, prompt-fragile), prompts + a behavioural-interview linter on Step 3 scripts (deterministic for the highest-leverage check), or full eval-driven verification (Extensive-tier scope),

**we decided for** a two-layer approach: (a) Dragon-style adversarial preambles lifted verbatim into every Mini Council SKILL.md (already in place from Phases 1–2 per [ADR-004](./ADR-004-Mini-Council-Skills.md)), and (b) a deterministic behavioural-interview linter (`helpers/interview_validator.py`) that catches Mom Test violations in Step 3 generated scripts via a pattern-rule registry,

**and neglected** prompt-only enforcement (the Step 3 script generator is the single highest-risk place for hypothetical-question leakage; relying solely on the prompt to police itself is exactly the failure mode the concept warns against), full eval-driven verification (~1–2 weeks of scope addition; deferred to v0.2.0 per [ADR-002](./ADR-002-Build-Tier-Moderate-Plus-NotebookLM.md)), and an LLM-based judge for nuanced detection (introduces an external dependency in the test loop — Protocol 8 prefers deterministic checks for v0.1.0; LLM-based check can be added as an optional layer later),

**to achieve** prompt-level adversarial posture across all five Council voices and the Discovery / Vertical / Buyer / Framework / Competitor / Synthesis flows, plus a deterministic, testable, fast linter that intercepts Mom Test violations before the user ever sees the generated interview script,

**accepting that** the regex layer can be bypassed by paraphrase (mitigated by a comprehensive rule registry and the Step 3 command's instruction to re-generate when the linter fires), prompt-level adversarial posture is not eval-verified in v0.1.0 (residual Q5 risk per [ADR-002](./ADR-002-Build-Tier-Moderate-Plus-NotebookLM.md)), and the linter has no LLM check in v0.1.0 (deferred — see SPEC-008-A "future work").

---

## Options Considered

| Option | Verdict |
|---|---|
| **Dragon-style preambles + deterministic regex linter (Selected)** | Two leverage points, both shipping v0.1.0; deterministic linter catches the highest-risk class |
| Prompts only | Rejected — Step 3 is exactly where the concept warns about hypothetical leakage |
| Prompts + LLM-judge linter | Rejected for v0.1.0 — adds external dependency in the test loop; LLM-check can layer on later |
| Full eval-driven verification | Rejected — Extensive-tier; deferred to v0.2.0 per ADR-002 |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Implements | ADR-002 | Build tier — Moderate | Anti-sycophancy is the headline promise |
| Refines | ADR-004 | Mini Council SKILL.md | Preamble layer lives in each Council voice's SKILL.md |
| Reuses | (external) | campaign-mode dragon-agent voice/tone (lines 88–96) | Lifted into every Mini Council SKILL.md per Protocol 12 |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| SPEC-008-A | Behavioural-Interview Linter Rules | [specs/SPEC-008-A-Anti-Sycophancy.md](./specs/SPEC-008-A-Anti-Sycophancy.md) |
| Concept | Mitchell Agentic Sprint concept §6 + §10 | [docs/concept/concept.md](../concept/concept.md) |
| Source | The Mom Test (Rob Fitzpatrick) — concept §9 reference | (external; no local copy) |
| Research | Gap analysis §6 (anti-sycophancy enforcement) | [docs/research/gap-analysis.md](../research/gap-analysis.md) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-09 |
