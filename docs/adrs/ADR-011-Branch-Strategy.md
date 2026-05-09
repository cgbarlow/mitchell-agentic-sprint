# ADR-011: Single `feature/v0.1.0` Branch with Gated PR Review at Each Phase

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-011 |
| **Initiative** | v0.1.0 development workflow |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-08 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** Protocol 4 requiring all changes on a feature branch (no direct commits to `main`) for a build that spans ~9 weeks across 5 implementation phases,

**facing** the choice between many small phase-by-phase branches with gated merges, a single long-lived feature branch with PR review on the open branch, or many ADR/spec-sized branches,

**we decided for** a single `feature/v0.1.0` branch from `main`, kept open for the duration of the build, with Scott reviewing work-in-progress at each phase gate via the open PR, and a single squash-merge to `main` at v0.1.0 release,

**and neglected** phase-by-phase branches with gated merges (creates merge friction every 1–2 weeks; risks main becoming unstable if a phase merges before its gate passes) and per-ADR branches (high churn for solo build; over-engineered),

**to achieve** Protocol 4 compliance, a single coherent v0.1.0 PR with full journey traceability, in-flight tester feedback via the open PR, and a clean v0.1.0 commit on `main` after merge,

**accepting that** the open branch will accumulate ~9 weeks of commits before merge (mitigated by clear commit messages per phase), `main` will be silent during the build (acceptable — there are no other consumers of `main` in this period), and rebases against `main` will be unnecessary because nothing else lands on `main` while the branch is open.

---

## Options Considered

| Option | Verdict |
|---|---|
| **Single `feature/v0.1.0` branch (Selected)** | Selected by user in plan-mode prompt; Protocol 4 compliant; minimises merge friction |
| One branch per phase | Rejected — adds merge friction every 1–2 weeks; risks unstable main |
| One branch per ADR/spec pair | Rejected — high churn for solo build |
| Direct commits to main | Rejected — Protocol 4 violation |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Refines | ADR-002 | Build tier | Operationalises the phasing |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| Protocol | `docs/protocols.md` Protocol 4 — Feature Branches | [../protocols.md](../protocols.md) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-08 |
