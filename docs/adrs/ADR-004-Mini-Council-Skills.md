# ADR-004: Mini Council as Five New SKILL.md NPC Agents

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-004 |
| **Initiative** | Mini Council adversarial layer |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-08 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** the concept's "Mini Council" of five skeptical personas (seed VC, churned customer, competitor founder, future-self, grumpy PM) that tear up the user's idea between Steps 1→2 and Steps 4→5 to refuse flattery and force specificity per concept §6,

**facing** the choice of how to implement these five voices — as profile-pack skins on existing campaign-mode NPCs (Dragon, Cat, Owl), or as net-new SKILL.md NPC agents in MAS,

**we decided for** five new SKILL.md NPC agents (`seed-vc-agent`, `churned-customer-agent`, `competitor-founder-agent`, `future-self-agent`, `grumpy-pm-agent`), each with embedded domain heuristics, sharing a Mini Council Conventions section that lifts the voice/tone preamble verbatim from `campaign-mode/skills/dragon-agent/SKILL.md` lines 88–96,

**and neglected** profile-pack-only re-skinning of Dragon (cannot encode domain heuristics — a re-skinned Dragon "speaks in VC vocabulary" but doesn't "reason about unit economics"; gap analysis §2 confirmed profile packs only override `skin-name` and `emoji`), single composite "Council" agent that role-plays all five (loses voice differentiation, blends identities — explicitly forbidden by campaign-mode CLAUDE.md identity rules), and reusing six-animals as Council members (psychological archetypes are present-tense behavioural advisors, not domain-knowledgeable expert personas with temporal/emotional framings),

**to achieve** real domain depth in each voice (Seed VC actually knows 2026 inference economics; Churned Customer actually frames retrospective regret; Future-Self actually applies temporal hindsight), maximum context isolation per voice (each voice receives the user's state but not other voices' transcripts), and verifiable voice differentiation through worked-example review per ADR-010,

**accepting that** five new SKILL.md files is more code surface than a single profile pack, each voice needs prompt iteration to feel distinct (mitigated by shared Mini Council Conventions section that DRYs the conventions while letting each voice diverge on heuristics), and the Mini Council is independent of campaign-mode's Council animal-advisory layer (these are MAS-specific).

---

## Options Considered

| Option | Verdict |
|---|---|
| **Five new SKILL.md NPC agents (Selected)** | Real domain depth; isolated voices; verifiable differentiation |
| Profile-pack-only re-skin of Dragon × 5 | Rejected — profile packs cannot add heuristics; gap analysis §2 |
| Single composite "Council" agent | Rejected — loses voice differentiation; blends identities |
| Reuse six-animals as Council | Rejected — wrong archetype kind (behavioural vs expert/emotional) |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Implements | ADR-002 | Build tier | Moderate-tier requirement |
| Refines | ADR-003 | Sibling-plugin shape | Council voices live in our `skills/` directory |
| Reuses | (external) | campaign-mode dragon-agent voice/tone | Lifted via Protocol 12 (DRY) |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| SPEC-004-A | Mini Council SKILL.md Format | [specs/SPEC-004-A-Mini-Council-Skill-Format.md](./specs/SPEC-004-A-Mini-Council-Skill-Format.md) |
| Concept | Mitchell Agentic Sprint concept §6 | [docs/concept/concept.md](../concept/concept.md) |
| Research | Gap analysis §2 (Mini Council depth) | [docs/research/gap-analysis.md](../research/gap-analysis.md) |
| Source | campaign-mode dragon-agent voice/tone | [github.com/cgbarlow/campaign-mode](https://github.com/cgbarlow/campaign-mode/blob/main/skills/dragon-agent/SKILL.md) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-08 |
