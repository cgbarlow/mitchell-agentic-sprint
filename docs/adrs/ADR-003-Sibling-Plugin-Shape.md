# ADR-003: Sibling-Plugin Shape with Hard `campaign-mode` and `six-animals` Dependencies

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-003 |
| **Initiative** | v0.1.0 plugin architecture |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-08 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** packaging MAS as a Claude Code plugin per [ADR-002](./ADR-002-Build-Tier-Moderate-Plus-NotebookLM.md),

**facing** the choice of how to relate to existing infrastructure — `cgbarlow/campaign-mode` provides reusable NPC agents (Gandalf, Dragon, Guardian), conversation transcript machinery, progress logging, and AskUserQuestion conventions, and `SimonMcCallum/six-animals` provides six advisory agents that can serve as an optional team-thinking layer alongside MAS,

**we decided for** a sibling Claude Code plugin (`mitchell-agentic-sprint`) that declares `campaign-mode` and `six-animals` as hard marketplace dependencies, reuses their agents and conventions, and adds MAS-specific commands and Mini Council NPC agents on top,

**and neglected** forking campaign-mode (loses upstream improvements; doubles maintenance burden), building a fully standalone plugin (loses ~70% of reusable infrastructure for no architectural benefit), and treating campaign-mode as an *optional* dependency (forces us to re-implement Gandalf/Dragon/Guardian voice and tone — a Protocol 12 DRY violation),

**to achieve** maximum reuse of campaign-mode's transcript and progress-log infrastructure (which directly serves the concept's "verbatim quotes only" rule), inheritance of established NPC voice patterns, and a clean plugin boundary that lets MAS evolve without forking,

**accepting that** users must install `campaign-mode` and `six-animals` to use MAS, our `plugin.json` must pin specific versions of those dependencies (initial pin: `campaign-mode@0.4.8`, `six-animals@0.1.2`), and any major version bump in either dependency may break MAS until we update.

---

## Options Considered

| Option | Verdict |
|---|---|
| **Sibling plugin with hard deps (Selected)** | Maximum reuse; clean boundary; ~70% infrastructure inherited |
| Fork campaign-mode | Rejected — loses upstream; doubles maintenance |
| Fully standalone plugin | Rejected — re-implements ~30% of campaign-mode for no gain |
| Optional campaign-mode dependency | Rejected — forces re-implementation of NPC voice patterns; DRY violation |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Implements | ADR-002 | Build tier | Realises the Moderate architecture |
| Enables | ADR-004 | Mini Council NPC agents | Council agents reuse Dragon's voice/tone preamble |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| SPEC-003-A | Plugin Manifest and Marketplace Declaration | [specs/SPEC-003-A-Plugin-Manifest.md](./specs/SPEC-003-A-Plugin-Manifest.md) |
| Upstream | campaign-mode plugin manifest | [github.com/cgbarlow/campaign-mode](https://github.com/cgbarlow/campaign-mode) |
| Upstream | six-animals plugin manifest | [github.com/SimonMcCallum/six-animals](https://github.com/SimonMcCallum/six-animals) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-08 |
