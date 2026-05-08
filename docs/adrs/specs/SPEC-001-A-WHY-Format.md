# SPEC-001-A: WH(Y) Statement Format and Section Structure

| Field | Value |
|-------|-------|
| **Specification ID** | SPEC-001-A |
| **Parent ADR** | [ADR-001](../ADR-001-Enhanced-ADR-Format.md) |
| **Version** | 1.0 |
| **Status** | Active |
| **Last Updated** | 2026-05-08 |

---

## Overview

This specification defines the WH(Y) statement format and the canonical ADR section structure for `mitchell-agentic-sprint`. It is a **light port** of iris's [SPEC-001-A](https://github.com/cgbarlow/iris/blob/main/docs/adrs/specs/SPEC-001-A-WHY-Format.md) — the canonical reference for the format's full detail, examples, and rationale. Refer to iris's spec for anything not covered here.

## WH(Y) statement structure

Every ADR must contain a WH(Y) decision statement composed of the following six clauses, in order:

```
In the context of <functional context or component>,
facing <non-functional concern, problem, or constraint>,
we decided for <chosen decision or option>,
and neglected <rejected alternatives>,
to achieve <intended benefits or qualities>,
accepting that <trade-offs or consequences>.
```

Each clause is a single sentence fragment. The six clauses combine into one structured paragraph at the top of every ADR.

## Required ADR sections

Every ADR file must contain the following sections in order:

1. **Title** — `# ADR-NNN: <Title>`
2. **Metadata table** — Decision ID, Initiative, Proposed By, Date, Status
3. **WH(Y) Decision Statement** — the six-clause statement
4. **Options Considered** — table of options with verdicts (Selected / Rejected with reason)
5. **Dependencies** — table of ADR relationships (Depends On, Relates To, Supersedes, Refines, Enables)
6. **References** — table of related specs, source documents, and protocols
7. **Status History** — table of status changes with approver and date

Optional sections (use when relevant): Problem Statement, Opportunity, Implementation Notes, Governance.

## Required Spec sections

Every SPEC file must contain:

1. **Title** — `# SPEC-NNN-X: <Title>`
2. **Metadata table** — Specification ID, Parent ADR, Version, Status, Last Updated
3. **Overview** — what the spec covers
4. **The implementation detail** — the body of the spec, organised by topic
5. (Optional) **Acceptance criteria** — testable conditions for the spec to be considered fulfilled

## Status vocabulary

| ADR Status | Meaning |
|---|---|
| Proposed | Drafted but not yet accepted |
| Accepted | Decision in force; ADR is immutable |
| Superseded | Replaced by a newer ADR (cite the superseding ADR) |
| Deprecated | No longer applicable but not formally replaced |

| Spec Status | Meaning |
|---|---|
| Draft | In progress; subject to change |
| Active | In effect; updates allowed (specs are living documents per Protocol 2) |
| Retired | No longer applicable |

## Filename conventions

- ADR files: `docs/adrs/ADR-NNN-Kebab-Case-Title.md`
- Spec files: `docs/adrs/specs/SPEC-NNN-X-Kebab-Case-Title.md`, where `NNN` matches the parent ADR and `X` is a letter (`A`, `B`, `C`...) when one ADR has multiple specs

## Acceptance criteria

This spec is fulfilled when:
- All ADRs in `docs/adrs/` follow the section structure above
- All SPEC files reference their parent ADR in the metadata table
- ADRs marked "Accepted" are not modified (a new ADR is created to supersede instead)
- Filename conventions are respected
