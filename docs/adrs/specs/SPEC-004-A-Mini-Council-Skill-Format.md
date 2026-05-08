# SPEC-004-A: Mini Council SKILL.md Format

| Field | Value |
|-------|-------|
| **Specification ID** | SPEC-004-A |
| **Parent ADR** | [ADR-004](../ADR-004-Mini-Council-Skills.md) |
| **Version** | 1.0 |
| **Status** | Active |
| **Last Updated** | 2026-05-08 |

---

## Overview

Defines the file structure, frontmatter, conventions, and output format that every Mini Council voice SKILL.md must follow. The canonical reference implementation is [`skills/seed-vc-agent/SKILL.md`](../../../skills/seed-vc-agent/SKILL.md). The other four voices (Churned Customer, Competitor Founder, Future-Self, Grumpy PM) follow the same structure with voice-specific Foundation and Core Skills sections.

## Frontmatter

```yaml
---
name: {voice}-agent          # kebab-case voice name (e.g., "seed-vc-agent")
description: |
  Mitchell Agentic Sprint Mini Council voice — the {Voice}. {one-paragraph
  description of the voice's lens and when it's invoked}. Operates with maximum
  context isolation. Invoke during Mini Council orchestration at Step 1→2 and
  Step 4→5 transitions, or directly via /sprint-council.
license: CC-BY-SA-4.0
metadata:
  author: Chris Barlow
  framework: Mitchell Agentic Sprint
  archetype: Mini Council
  role: {Voice} — {one-line lens description}
  source: campaign-mode dragon-agent (voice/tone) + {voice-specific source}
---
```

## Required sections (in order)

Every Mini Council SKILL.md must contain these sections:

1. **Title** — `# {Voice} Agent — Mini Council Voice {N} of 5`
2. **Speaker Identification** — emoji + voice name in bold; profile override path
3. **Mini Council Conventions** — shared across all five voices; defines identity rules, adversarial-by-default posture, voice and tone, single-question rule, context isolation
4. **Foundation: The {Voice} Lens** — voice-specific worldview and operating principles
5. **Core Skills** — 2–3 numbered skills, each with Process and Probe Examples
6. **Interaction Mechanics** — single-question rule reaffirmed
7. **What the {Voice} Is NOT** — boundaries vs other Council voices and campaign-mode NPCs
8. **Council Output Format** — three-verdict pattern (Pass / Pass for now / In play)
9. **Worked-example references** — pointer to `docs/examples/`

## Speaker emojis

Each voice has a default emoji used in `**🌱 Voice:**` speaker tags:

| Voice | Default Emoji |
|---|---|
| Seed VC | 💼 |
| Churned Customer | 💔 |
| Competitor Founder | ⚔️ |
| Future-Self (12 months) | ⏳ |
| Grumpy PM | 📋 |

Each can be overridden via `.sprint/profiles/{voice}.md` if the user wants to skin.

## Mini Council Conventions section (shared verbatim)

Every voice's "Mini Council Conventions" section must contain identical text covering:

- **Identity rules** — adopt voice fully; no blending; refer the user back to Gandalf for off-remit help
- **Adversarial-by-default posture (concept §6)** — refuse flattery; push back on vague answers; ban hypothetical evidence; cite or it didn't happen
- **Voice and tone** — terse, authoritative, unsentimental; no warmth; no exclamation marks; declarations not dialogue
- **Single-question rule** — exactly one `AskUserQuestion` per response
- **Context isolation** — receive Builder Profile + current step state; do NOT receive transcripts, Gandalf's notes, or other voices' transcripts

This text is duplicated across SKILL.md files because each is loaded independently when invoked. Per Protocol 12 the duplication is acceptable in documentation (specs and prompts) — code must not duplicate.

## Council Output Format (shared verbatim)

Every voice concludes with one of three verdicts, plainly stated:

- **Pass.** "I would not {invest|stay|fight you|be at peace with this past-me|let this ship} today. The reason is: [one sentence]. The specific evidence missing is: [one to three items]."
- **Pass for now.** "I would not {decide} today, but I would reconsider if [specific condition met]. Until then, this is not {investable|defensible|shippable|...}."
- **In play.** "This would clear my {pre-seed|customer-retention|competitive-attack|future-regret|ship-readiness} bar today. The strongest evidence is: [one sentence]. The remaining risk I'd track is: [one sentence]." (Used sparingly.)

Verbs adapt to the voice's lens but the three-verdict structure is fixed.

## Worked-example review (per ADR-010)

Voice fidelity is verified by manual worked-example review at gate reviews, not by automated eval. Each Mini Council orchestration in the worked examples must show the five voices producing meaningfully different critiques on the same input. If two voices produce indistinguishable verdicts on the same input, that's a fidelity bug — fix the prompts.

## Acceptance criteria

This spec is fulfilled when:
- Five SKILL.md files exist matching this structure (seed-vc, churned-customer, competitor-founder, future-self, grumpy-pm)
- Each frontmatter passes the field rules above
- Each contains the nine required sections
- The Mini Council Conventions text is byte-identical across files (copy-paste maintained; updates apply to all five together — DRY by procedure since SKILL.md inclusion is per-file by Claude Code)
- A worked-example sprint demonstrates voice differentiation across all five
