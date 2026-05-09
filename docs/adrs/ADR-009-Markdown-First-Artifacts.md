# ADR-009: Markdown-First Artifacts; Defer Slide Rendering to v0.2.0

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-009 |
| **Initiative** | Step 6 synthesis output format |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-09 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** Step 6 producing the three concept-§4.6 artefacts (sales deck, customer outreach plan, pre-seed investor deck) for the user to take into customer conversations and pre-seed pitches,

**facing** the choice of artefact output format — markdown templates the user pastes into their own slide tool, generated `.pptx` files via `python-pptx`, generated `.pdf` files via Reveal.js + headless Chrome, or a polished slide-builder UI with branding controls,

**we decided for** markdown-first artefacts — three template files (`sales-deck.md`, `outreach-plan.md`, `investor-deck.md`) under `docs/templates/`, each with slide-per-section structure and speaker-notes blocks, populated by Step 6 with the user's actual evidence from Steps 1–5,

**and neglected** PPTX generation in v0.1.0 (~1 week of `python-pptx` integration plus template-fidelity edge cases; pulls Extensive-tier scope into Moderate per [ADR-002](./ADR-002-Build-Tier-Moderate-Plus-NotebookLM.md)), PDF rendering via Reveal.js (additional toolchain — headless Chrome — for marginal-over-markdown gain), and a slide-builder UI (out of scope for a Claude Code plugin v0.1.0; designers will always want more controls),

**to achieve** the concept's headline value at v0.1.0 (a builder walks out of Step 6 with three artefacts they can take to a customer conversation or a VC meeting *this week*), low rendering complexity (markdown survives clipboard, version control, code review, and email), preserved evidence chain (every slide cites the buyer interview / framework citation / competitor verbatim that supports it — slides without evidence are explicitly marked, not padded),

**accepting that** the user must paste the markdown into their preferred slide tool (Keynote / Google Slides / PowerPoint / Pitch / Marp) themselves, the artefacts will not have visual polish in v0.1.0 (acceptable — the concept frames v1 as "everything you need to brief your AI builder of choice" rather than a polished deliverable), and slide rendering becomes a v0.2.0 priority *only if* tester demand pulls it forward (per the recommendation's "no Extensive without demand signal" rule).

---

## Options Considered

| Option | Verdict |
|---|---|
| **Markdown templates with slide-per-section structure (Selected)** | Highest leverage for v0.1.0; preserves evidence chain; user owns the rendering choice |
| `python-pptx` PPTX generation | Rejected for v0.1.0 — ~1 week of integration + template fidelity edge cases; defer to v0.2.0 |
| Reveal.js + headless Chrome PDF | Rejected — additional toolchain for marginal-over-markdown gain |
| Custom slide-builder UI | Rejected — out of scope for a Claude Code plugin |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Implements | ADR-002 | Build tier — Moderate | Markdown-first is a Moderate-tier choice |
| Refines | ADR-006 | NotebookLM via MCP | NotebookLM augments synthesis via prompt builders; output remains markdown |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| SPEC-009-A | Artifact Template Format | [specs/SPEC-009-A-Artifact-Templates.md](./specs/SPEC-009-A-Artifact-Templates.md) |
| Concept | Mitchell Agentic Sprint concept §4.6 | [docs/concept/concept.md](../concept/concept.md) |
| Research | Build options §1 / §2 risk: "investor deck weakness" mitigation | [docs/research/build-options.md](../research/build-options.md) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-09 |
