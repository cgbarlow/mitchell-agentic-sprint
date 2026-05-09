# ADR-002: Build Tier — Moderate with NotebookLM Bolt-on

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-002 |
| **Initiative** | v0.1.0 scope and shape |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-08 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** building MAS v0.1.0 to deliver the concept's headline promise (anti-sycophancy + investor-conversation-ready artifacts) within a ~9-week budget,

**facing** three candidate build tiers identified in the [build-options research](../research/build-options.md) — Minimum (~2 weeks; profile-pack-only Council), Moderate (~7–8 weeks; new NPC agents + step gates + loopback), Extensive (~12–16 weeks; tooling layer with slide rendering, theme clustering, evals) — plus the NotebookLM bolt-on (~+1.5 weeks),

**we decided for** Moderate + NotebookLM bolt-on (non-Enterprise path), with the first week shaped as a Minimum-equivalent walking skeleton (Step 1 + single Seed VC Council voice) used as a tester gate before continuing,

**and neglected** Minimum-as-final-shape (cannot deliver the headline promise — Council voices feel interchangeable when re-skinned from Dragon; Mom Test discipline is unenforceable; investor decks lack defensible evidence) and Extensive (premature — concept §10 itself flags core uncertainties around linear flow, named-expert assumption, and AI-as-coach replacement; tooling layer becomes justified only after tester demand pulls it forward),

**to achieve** real domain-knowledgeable Mini Council voices, enforced Mom Test discipline, working loopback, markdown-first artifacts that close 80% of the headline value, and NotebookLM-augmented synthesis for Steps 3–6 that aligns with the concept's "verbatim quotes only" rule,

**accepting that** anti-sycophancy verification via eval set is deferred to v0.2.0, slide rendering (PPTX/PDF) is deferred to v0.2.0, and the unofficial NotebookLM CLI carries Google ToS risk that must be mitigated by a Claude-only fallback path.

---

## Options Considered

| Option | Verdict |
|---|---|
| **Moderate + NotebookLM bolt-on (Selected)** | Hits headline promise; testable in 9 weeks; integration deferred to week 5 doesn't block walking skeleton |
| Minimum only | Rejected — see [build-options §1 risks](../research/build-options.md) |
| Extensive | Rejected — premature per [recommendation §rationale](../research/RECOMMENDATION.md) |
| Moderate without NotebookLM | Considered — viable, but loses ~30% of synthesis quality on Steps 3–6 for ~1.5 weeks of work; user explicitly opted in to the bolt-on |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Enables | ADR-003 | Sibling-plugin shape | Implements the Moderate architecture |
| Enables | ADR-004 | Mini Council as new SKILL.md NPCs | Required by Moderate, not Minimum |
| Enables | ADR-006 | NotebookLM via MCP | The bolt-on portion |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| Research | Build options analysis | [docs/research/build-options.md](../research/build-options.md) |
| Research | Recommendation document | [docs/research/RECOMMENDATION.md](../research/RECOMMENDATION.md) |
| Concept | Mitchell Agentic Sprint concept | [docs/concept/concept.md](../concept/concept.md) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-08 |
