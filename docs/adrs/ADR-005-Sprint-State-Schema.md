# ADR-005: `.sprint/sprint.md` State Schema with Named-Step Sections and Loopback Support

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-005 |
| **Initiative** | Sprint state persistence |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-08 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** persisting sprint state across Claude Code sessions per the concept's six-step linear pipeline and loopback-on-validation-failure pattern (concept §7),

**facing** the choice between mirroring campaign-mode's narrative `.campaign/quest.md` schema (free-form, single Quest Narrative + Success Criteria + Progress Log) or designing a step-pipeline-shaped schema with named sections per step,

**we decided for** a new `.sprint/sprint.md` schema with frontmatter (`step`, `last_approved_step`, `attempt`, `sprint-mode`, `created`) plus named markdown sections per step (Builder Profile, Vertical Stack, Interview Log, Expert Framework, Competitor Map, Artifacts) and a Loopback Log,

**and neglected** reusing campaign-mode's schema verbatim (its narrative shape doesn't accommodate per-step artifacts or step-gate enforcement), storing each step in a separate file (loses the single-source-of-truth view; complicates cross-step queries), and using a structured database (overkill for v0.1.0; defies the "markdown-first" thesis),

**to achieve** clean step-gate enforcement (helpers can read `last_approved_step` to decide if Step N+1 may proceed), loopback semantics that retain Builder Profile and Expert Framework while clearing Vertical Stack onward, and human-readable state that the user can edit when needed,

**accepting that** the schema introduces parsing complexity (handled by `helpers/sprint_state.py`), schema migrations between versions need a small version field and a one-shot migration helper if we ever change shape mid-build, and concurrent edits across Claude sessions are not supported — last write wins.

---

## Options Considered

| Option | Verdict |
|---|---|
| **Named-step markdown schema (Selected)** | Clean gate semantics; loopback semantics expressible; human-readable |
| Reuse `quest.md` shape verbatim | Rejected — narrative-shaped, doesn't fit the linear pipeline |
| One file per step | Rejected — loses single-source-of-truth |
| SQLite or JSON state | Rejected — overkill; opaque to user |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Implements | ADR-002 | Build tier | Loopback is a Moderate-tier requirement |
| Enables | ADR-007 | Step gate enforcement | Gates read `last_approved_step` from this schema |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| SPEC-005-A | Sprint State Schema | [specs/SPEC-005-A-Sprint-State-Schema.md](./specs/SPEC-005-A-Sprint-State-Schema.md) |
| Research | Gap analysis §4 (state schema) | [docs/research/gap-analysis.md](../research/gap-analysis.md) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-08 |
