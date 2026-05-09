# ADR-010: TDD Scope — Code Only; Council Voices via Worked-Example Review

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-010 |
| **Initiative** | v0.1.0 quality strategy |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-08 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** Protocol 3 (TDD) requiring tests before implementation for every feature and bug fix, applied to a v0.1.0 build that mixes Python helper code (linter, saturation detector, MCP glue) with prompt-driven SKILL.md NPC voices,

**facing** the question of how TDD applies to prompt content — whether Mini Council voices should have their own eval set (defined-bad inputs → expected pushback patterns) or whether prompt fidelity is verified by other means,

**we decided for** TDD strictly on Python code (`helpers/sprint_state.py`, `interview_validator.py`, `saturation.py`, `notebooklm.py`) with pytest-and-real-fixtures discipline, and **worked-example review** for SKILL.md voices — three documented worked-example sprints in `docs/examples/` that are manually compared for voice differentiation and adversarial fidelity,

**and neglected** building a per-voice eval set for v0.1.0 (~3–5 days extra; pulls Extensive-tier scope into Moderate; the concept itself flags anti-sycophancy verification as an open question best validated by users not by automated evals) and skipping TDD entirely on code (violates Protocol 3),

**to achieve** Protocol 3 compliance on the lightweight code where TDD is straightforward and high-value, while keeping eval set work scoped out of v0.1.0 in line with [ADR-002](./ADR-002-Build-Tier-Moderate-Plus-NotebookLM.md),

**accepting that** voice-fidelity regressions will not be caught by CI and rely on the worked-example review process at each tester gate, that this leaves Q5 (anti-sycophancy verification) as a residual risk for v0.1.0 to be addressed in v0.2.0, and that "Council voices via worked-example review" is a soft check — not a hard CI gate.

---

## Options Considered

| Option | Verdict |
|---|---|
| **TDD on code; worked-example review for voices (Selected)** | Protocol-compliant on code; defers eval set to v0.2.0; aligns with ADR-002 |
| TDD on code + small eval set per voice (~5 cases) | Considered — pulls ~3–5 days of Extensive scope into Moderate; rejected by user in plan-mode prompt |
| Full eval-driven TDD on every prompt | Rejected — premature for v0.1.0; ~1–2 weeks scope addition |
| No TDD anywhere | Rejected — Protocol 3 violation |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Refines | ADR-002 | Build tier | Operationalises the "deferred to Extensive" eval scope |
| Relates To | ADR-012 | Python + pytest | Names the test framework |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| Protocol | `docs/protocols.md` Protocol 3 — TDD | [../protocols.md](../protocols.md) |
| Plan | TDD strategy section | Build plan |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-08 |
