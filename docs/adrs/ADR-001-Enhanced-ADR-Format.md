# ADR-001: Adopt Enhanced WH(Y) ADR Format

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-001 |
| **Initiative** | Build foundation for v0.1.0 |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-08 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** building Mitchell Agentic Sprint v0.1.0 under the protocols vendored at `docs/protocols.md` (Protocol 1: every architectural decision must be captured as an ADR; Protocol 2: every implementing ADR must have a spec),

**facing** the choice of which ADR format to adopt — and the cost of writing a format ourselves when a battle-tested one already exists in `cgbarlow/iris`,

**we decided for** porting the enhanced WH(Y) ADR format from [iris's ADR-001](https://github.com/cgbarlow/iris/blob/main/docs/adrs/ADR-001-Enhanced-ADR-Format.md), with `docs/adrs/` for ADRs and `docs/adrs/specs/` for specs,

**and neglected** rolling our own minimal format (would diverge from established practice across cgbarlow projects), Michael Nygard's classic four-section ADR (lacks separation of decision from implementation; conflates rationale with code), and a TOGAF-style enterprise framework (excessive ceremony for a solo build),

**to achieve** consistency across cgbarlow projects, separation of stable decision records from evolving specifications, and reuse of the dependency-tracking and governance metadata already proven in iris,

**accepting that** porting introduces a one-time learning curve, requires SPEC files to live separately from ADRs, and ties this project's documentation conventions to a sibling project.

---

## Options Considered

| Option | Verdict |
|---|---|
| **Port iris's enhanced WH(Y) format (Selected)** | Proven format; consistent with sibling cgbarlow projects; Protocol 1 in `docs/protocols.md` already references the WH(Y) format by name |
| Nygard four-section ADR | Rejected — conflates decision rationale with implementation; no rejected-alternatives discipline |
| Custom minimal format | Rejected — divergence cost; reinventing existing solution; Protocol 12 (DRY) violation |
| TOGAF / heavyweight enterprise framework | Rejected — adoption friction; misfit for a solo build |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Enables | ADR-002 onward | All other ADRs in this project | They use the WH(Y) format defined here |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| SPEC-001-A | WH(Y) Statement Format and Section Structure | [specs/SPEC-001-A-WHY-Format.md](./specs/SPEC-001-A-WHY-Format.md) |
| Source ADR | iris ADR-001 (canonical format definition) | [github.com/cgbarlow/iris/.../ADR-001](https://github.com/cgbarlow/iris/blob/main/docs/adrs/ADR-001-Enhanced-ADR-Format.md) |
| Protocol | `docs/protocols.md` Protocol 1 — Architecture Decision Records | [../protocols.md](../protocols.md) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-08 |
