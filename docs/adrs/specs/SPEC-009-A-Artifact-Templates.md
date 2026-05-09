# SPEC-009-A: Artifact Template Format

| Field | Value |
|-------|-------|
| **Specification ID** | SPEC-009-A |
| **Parent ADR** | [ADR-009](../ADR-009-Markdown-First-Artifacts.md) |
| **Version** | 1.0 |
| **Status** | Active |
| **Last Updated** | 2026-05-09 |

---

## Overview

Defines the structure of the three Step 6 artefacts (sales deck, customer outreach plan, pre-seed investor deck) and the rules `commands/sprint-step-6.md` follows when populating them.

The templates live at:
- `docs/templates/sales-deck.md` — 6–8 slides for customer conversations
- `docs/templates/outreach-plan.md` — re-engagement messages + new-contact target list + outreach sequence
- `docs/templates/investor-deck.md` — 12 slides for pre-seed conversations

`/sprint-step-6` reads each template, populates it with the user's evidence from Steps 1–5, and writes the populated artefact to `.sprint/artifacts/`. The original templates in `docs/templates/` are never modified — they are read-only scaffolds.

## Universal rules across all three artefacts

1. **Every claim cites evidence.** Each slide / section that makes a claim about buyer pain, market dynamics, traction, or moat must reference the source — interview quotes (with pseudonym + interview number), expert framework citations (with source document), competitor verbatim quotes (with competitor name).
2. **No padding when evidence is missing.** If a slide's required evidence is missing, the slide is marked `[EVIDENCE MISSING: {what's needed}]` rather than fabricated. The user resolves the gap before the artefact is presentation-ready.
3. **Verbatim quotes only.** When citing buyers, use the verbatim language from the interview transcripts — do not paraphrase. Concept §6.
4. **Slide-per-section structure.** Each slide is a level-2 markdown heading with the slide number and title. Slide content sits below; speaker notes go in a fenced `> Speaker notes:` block at the end of each slide.
5. **Anti-sycophancy preamble in the artefact frontmatter.** Each populated artefact opens with a one-paragraph note for the user: "These artefacts are populated from Sprint state. Where evidence is marked missing, fill it in before presenting. Do not pad."

## Sales deck template

**Path:** `docs/templates/sales-deck.md`
**Slides:** 6–8
**Audience:** prospective customers in the user's chosen ICP

### Required slide order

| # | Slide | Required evidence |
|---|---|---|
| 1 | Buyer pain (verbatim quote opens) | One verbatim quote from the strongest theme in Theme Map, attributed to a pseudonymised buyer |
| 2 | Problem stated precisely | Plain-language problem statement; cite the recurrence (number of interviews) and costly-action signals |
| 3 | Differentiated solution | One paragraph + the positioning whitespace from Step 5; cite the verbatim language no competitor uses |
| 4 | Validation evidence | Theme Map summary + 2–3 strongest costly-action signals + count of interviews logged |
| 5 | Framework basis (optional, skip if it doesn't add credibility) | Expert framework citation showing the principle being adopted |
| 6 | Pricing or offer | Pricing landed in Step 4/5 work; cite the unit-economics reasoning if applicable |
| 7 | Next step | Specific named ask: book a 30-min walkthrough, take a paid pilot, intro to a peer |
| 8 | Appendix (optional) | Costly-Action Signal list with anonymised buyer detail |

The deck doubles as a validation-proof document: the buyer interview evidence sits alongside the pitch.

## Outreach plan template

**Path:** `docs/templates/outreach-plan.md`
**Sections:** 3

### Required sections

1. **Re-engagement messages for the buyers interviewed in Step 3.** Auto-generated from the Interview Log:
   - For each interviewee with a costly-action signal: a personalised re-engagement message in the spirit of "here's what I built based on what you told me", quoting the buyer's own verbatim phrase from the interview
   - One message per costly-action signal, with the buyer's pseudonym and the verbatim quote inline
   - The user replaces pseudonyms with real identifiers before sending
2. **New-contact target list.** Drawn from the user's Vertical Stack ICP definition + Step 4's expert framework + Step 5's positioning whitespace:
   - 15–25 new buyer profiles matching the ICP
   - For each: where to find them (community / role / company-size pattern), why they fit, the suggested first-touch hook (anchored to the validated theme)
3. **Outreach sequence.** A 3-touch cadence drafted around the validated problem (not a vague pitch):
   - Touch 1 — first contact, behaviour-anchored
   - Touch 2 — follow-up, references the validated theme
   - Touch 3 — closing ask, drawn from the sales deck's "next step"

## Investor deck template

**Path:** `docs/templates/investor-deck.md`
**Slides:** 12 + appendix
**Audience:** pre-seed investors

### Required slide order

| # | Slide | Required evidence |
|---|---|---|
| 1 | Problem | Buyer pain in verbatim words; recurrence count |
| 2 | Why now | Specific 2026-AI-era reasoning, not generic "AI is hot" |
| 3 | Solution | Plain language; what the user built / will build |
| 4 | Product | Working demo screenshot reference (if missing, marked) + 1–2 user-experience highlights |
| 5 | Market | Bottom-up sized from ICP × buyers-reachable, not top-down TAM |
| 6 | Business model | Priced against actual buyers; cite the buyer who paid for the workaround |
| 7 | Traction | Named buyers + costly-action signals + interview count + LOIs / pilots |
| 8 | Competition | Competitor cluster map from Step 5 + the cluster the user does not occupy |
| 9 | Moat | Specific lock-in mechanism: workflow / data flywheel / regulated-vertical access. Not "proprietary AI". |
| 10 | Team | Builder Profile from Step 1 — unfair advantages + relevant experience |
| 11 | Ask | Specific use of funds, runway extension, milestones |
| 12 | Appendix | Inference economics (cost per query × queries per buyer × buyer count); evals plan; buyer-interview tape pointer |

### 2026-AI-era non-negotiables

The Step 6 command bakes these in. Each is a checklist item the populated deck must satisfy or explicitly mark as missing:

- [ ] Working demo (slide 4)
- [ ] Real moat — workflow lock-in / data flywheel / regulated-vertical access (slide 9; "proprietary AI" is rejected)
- [ ] Evals — what success looks like, how it's measured (appendix)
- [ ] Inference economics — gross margin under inference cost (appendix)
- [ ] Buyer-interview tape pointer — `.sprint/interviews/` directory + Theme Map (appendix)

When a check is missing, the slide is marked `[EVIDENCE MISSING: {what's needed}]`. The user fills the gap before sending the deck.

## Where artefacts are written

`/sprint-step-6` writes populated artefacts to:

- `.sprint/artifacts/sales-deck.md`
- `.sprint/artifacts/outreach-plan.md`
- `.sprint/artifacts/investor-deck.md`
- `.sprint/artifacts/audio-overview.mp3` (only if NotebookLM bolt-on is configured; concept §4.6 calls this out as a supporting artefact)

Their paths are recorded in `.sprint/sprint.md` Artifacts section so subsequent Sprints / continue-quest commands can locate them.

## Acceptance criteria

This spec is fulfilled when:
- Three template files exist at `docs/templates/{sales-deck,outreach-plan,investor-deck}.md` with the slide / section structure above
- Each template uses placeholder `{{...}}` markers that the Step 6 command fills with state from `.sprint/sprint.md`
- The Step 6 command writes populated artefacts to `.sprint/artifacts/` without modifying the templates
- Slides where evidence is missing are marked `[EVIDENCE MISSING: ...]` rather than fabricated
- Each artefact opens with the anti-sycophancy preamble note for the user
- The investor deck satisfies (or explicitly marks missing) all five 2026-AI-era non-negotiables
