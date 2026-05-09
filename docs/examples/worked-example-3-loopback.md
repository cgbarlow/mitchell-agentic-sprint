# Worked Example 3 — Full Sprint Through Step 6 with Prior Loopback in History

**Purpose:** voice-fidelity reference per [ADR-010](../adrs/ADR-010-TDD-Scope.md), and end-to-end demonstration of a completed Sprint that produces all three Step 6 artefacts. This is the v0.1.0 reference for what a *finished* Sprint looks like.

**Scenario:** Continuing the fictional Sam from [worked-example-2](worked-example-2-prosumer.md). Attempt 1 disqualified solo-creators-with-newsletters (saturated themes, zero costly-action signals). Sam looped back. Attempt 2 picks up the conversation with paid-newsletter operators — buyers with revenue in flight. This example walks attempt 2 from re-entry at Step 2 through to a complete Step 6 with all three artefacts.

---

## Loopback Log (carried from attempt 1)

```markdown
- **attempt 1** — disqualified `creator-economy / solo-creators-with-newsletters-1k-10k / weekly-content-planning` (8 interviews, 0 costly-action signals despite saturated themes; ICP is not a paying buyer for this product class) (2026-05-21)
```

**Builder Profile, Backup Verticals, Theme Map (with attempt-1 themes), and Expert Framework were retained through the loopback.** Vertical Stack, Competitor Map, Positioning Whitespace, and Artifacts were cleared.

---

## Step 2 (attempt 2) — Vertical Stack v2

| Layer | Content |
|---|---|
| Vertical | Creator economy |
| Sub-vertical | **Paid-newsletter operators** (changed from solo creators) |
| ICP | **Substack/Beehiiv operators with 1k+ paid subscribers, $5K+ MRR, US/EU** (sharpened — has-revenue is the gate) |
| Specific workflow | Weekly content planning — same workflow, different buyer |
| AI leverage point | Auto-link related notes; surface "you wrote about this six months ago, audience response was X" prompts during planning |

**Backup Verticals (refreshed):**
1. Audio creators with weekly schedules + 1k+ paid subs (podcast operators monetising directly)
2. Course operators (cohort-based or self-paced) selling $200+ products

The Mini Council convenes again on the Step 1→2 transition. With the loopback evidence in scope:

| Voice | Verdict |
|---|---|
| 💼 Seed VC | **Pass for now** — "buyers have revenue in flight, but unit economics still need pricing data" |
| 💔 Churned Customer | **Pass for now** — "show me the Month-3 retention story" |
| ⚔️ Competitor Founder | **In play** — "Substack-native tools have weak knowledge-management; this is a real gap" |
| ⏳ Future-Self | **In play** — "the loopback was right. The lesson held." |
| 📋 Grumpy PM | **Pass for now** — "you're solo and you've already burned 12 days; tighten scope" |

**Tally: 0 Pass, 3 Pass-for-now, 2 In play.** Sam advances to Step 3.

---

## Step 3 (attempt 2) — Buyer Interviews

Sam runs the cold outreach. Replies are dramatically warmer than attempt 1 — paid-newsletter operators have revenue, they take their craft seriously, and they recognise the workflow pain. Six interviews logged in nine days.

### Interview Log (excerpt)

| # | Pseudonym | Date | Length | Costly action? | Themes |
|---|---|---|---|---|---|
| 09 | substack-paid-1 (re-engaged from attempt 1) | 2026-05-25 | 45min | **yes** | weekly-planning-friction, search-failure, audience-uncertainty, **paid-tooling-experimentation** |
| 10 | substack-paid-2 | 2026-05-26 | 38min | **yes** | weekly-planning-friction, audience-uncertainty, **paid-tooling-experimentation** |
| 11 | beehiiv-paid-1 | 2026-05-27 | 50min | **yes** | weekly-planning-friction, search-failure, **revenue-anxiety** |
| 12 | substack-paid-3 | 2026-05-28 | 42min | unclear | weekly-planning-friction, audience-uncertainty |
| 13 | beehiiv-paid-2 | 2026-05-29 | 36min | **yes** | search-failure, **paid-tooling-experimentation**, **revenue-anxiety** |
| 14 | substack-paid-4 | 2026-06-01 | 40min | **yes** | weekly-planning-friction, **paid-tooling-experimentation**, **revenue-anxiety** |

**Costly-Action Signals: 5 yes, 1 unclear.** Out of 6 interviews. This is the dramatic difference between attempts.

Specific costly-action evidence:
- substack-paid-1 paid $39/month for a content-calendar tool last year, cancelled, now uses Notion + a paid Notion template ($49 one-time)
- substack-paid-2 hired a freelance editor for $1200/quarter to help her decide what to write next
- beehiiv-paid-1 paid for two competing tools simultaneously for 4 months, cancelled both
- beehiiv-paid-2 built her own custom Airtable workflow over 30 hours of personal time
- substack-paid-4 pays $99/month for a content-research tool she only uses one feature of

### Theme Map (attempt-2 themes augmented with attempt-1 retained themes)

| Theme | Interviews (attempt 2 + attempt 1) | Notable verbatim quotes |
|---|---|---|
| **weekly-planning-friction** | 5 (a2) + 6 (a1) = 11 | "I dread Mondays. Every Monday I spend two hours staring at my notes deciding what to write. Every. Monday." (substack-paid-2) |
| **paid-tooling-experimentation** | 4 (a2 only — new in this attempt) | "I've spent maybe $400 in the last year on tools that promised this. None worked." (beehiiv-paid-1) |
| **search-failure** | 3 (a2) + 6 (a1) = 9 | "I know I wrote about this. I cannot find it. So I rewrite it badly." (substack-paid-1) |
| **revenue-anxiety** | 3 (a2 only — new in this attempt) | "Every week I publish and I don't know if it'll churn subscribers. I just guess." (beehiiv-paid-2) |
| **audience-uncertainty** | 3 (a2) + 4 (a1) = 7 | "I have no idea what my paid subscribers actually want next." (substack-paid-3) |

### Saturation check

```
$ PYTHONPATH=${CLAUDE_PLUGIN_ROOT} python -m helpers.saturation --human /tmp/sprint-themes.json
Total interviews: 6
Themes per interview (new only): [4, 0, 1, 0, 0, 0]
Consecutive interviews with no new themes (from end): 3
Threshold: 3
Saturated: YES — last 3 interviews surfaced no new themes; consider stopping here.
```

Sam concludes Step 3 with **6 interviews, 5 costly-action signals, 5 strong recurring themes, 4 themes new to attempt 2**. Real pain *and* real wallet. Decision: **Go**.

---

## Step 4 — Framework

Sam runs `/sprint-step-4`. Gandalf surfaces 5 candidate experts. Sam picks **Mike Schultz** (running fictional consulting firm "RAIN Group" with a published book, multiple long-form interviews on creator-economy podcasts, and a paid course). Source documents added to the NotebookLM notebook (Sam configured the bolt-on between attempts).

Framework synthesis (excerpt of the populated Expert Framework section):

```markdown
### Framework synthesis (locked 2026-06-04)

#### Summary

1. **Insight buying** — Buyers buy from sellers who teach them something. Demonstrate insight first, sell second. ("In the new selling, sellers earn the right to be heard by demonstrating insight." — Schultz, *Insight Selling* p.17)
2. **Workflow integration** — The strongest sales motion is one that integrates with the buyer's existing workflow, not one that asks the buyer to adopt a new ritual. (Schultz, podcast interview with Greg Isenberg, 2025)
3. **Differential value articulation** — Articulate the value not in absolute terms but in *differential* terms: what does the buyer get from you that they cannot get from doing nothing? (Schultz, *Insight Selling* p.43)

#### Keep verbatim (3)

1. **Insight buying** — applies directly because paid-newsletter operators are themselves insight-buyers in their own market; they recognise the pattern when they see it. Source: *Insight Selling* p.17.
2. **Differential value articulation** — applies directly to the "$400 spent on tools that didn't work" cohort; they need to see the differential, not just the feature list. Source: *Insight Selling* p.43.
3. **Curiosity over qualification** — applies directly because Sam's Step 3 outreach already reads as curiosity-driven. Source: podcast 2025.

#### Adapt (3)

1. **Workflow integration** — Original: "integrate with existing tools". Adaptation: integrate with Substack and Beehiiv's editor surfaces, not just adjacent tools. Source: podcast 2025.
2. **Insight artefacts** — Original: "publish insight pieces". Adaptation: ship insight in-product (the planning interface itself shows the buyer something they didn't know about their own back catalogue). Source: course.
3. **Pricing anchoring** — Original: "anchor on enterprise prices". Adaptation: anchor on the $400/year buyers already spend on adjacent tools. Source: book p.91.

#### Cannot map

No principles failed to map.
```

---

## Step 5 — Competitor + Positioning Whitespace

Sam compiles 7 competitors (Notion, Obsidian, Roam, two Substack/Beehiiv-native tools, one Notion-template ecosystem, one paid newsletter-research tool). Each added as a NotebookLM source. Whitespace synthesis runs.

Excerpt from Competitor Map and Positioning Whitespace:

```markdown
## Competitor Map

### Cluster 1: Note-management tools (general)
- Members: Notion, Obsidian, Roam
- Verbatim positioning: "Your second brain", "Connected notes", "Networked thought"
- What they do well: capture, retrieval primitives, plugin ecosystems
- What they avoid: any opinionated workflow for paid newsletter operators specifically

### Cluster 2: Newsletter-native tooling
- Members: {Tool A}, {Tool B}
- Verbatim positioning: "Newsletter analytics", "Subscriber growth"
- What they do well: subscriber-side analytics
- What they avoid: pre-publication content planning; treat the editor as a black box

### Cluster 3: Generalist content-research tools
- Members: {Tool C}
- Verbatim positioning: "AI-powered content research"
- What they do well: external trend signals
- What they avoid: the operator's own back catalogue

## Positioning Whitespace

### Gap 1: pre-publication planning anchored to the operator's own back catalogue + audience response
- Buyer theme: weekly-planning-friction (recurrence: 11), search-failure (recurrence: 9)
- No competitor cluster lands here
- Verbatim phrasing the user could own: "Mondays you stare at your notes. We hand you Mondays back."

### Gap 2: differential-value articulation for paid-tooling-experimentation cohort
- Buyer theme: paid-tooling-experimentation (recurrence: 4 — all attempt-2 buyers)
- Verbatim phrasing the user could own: "We're not another tool. We're the one that connects to what you already wrote."

### Locked positioning statement (2026-06-08)

> Mondays you stare at your notes. Every other tool starts from scratch — we start from your back catalogue. We hand you Mondays back, with the differential evidence (which past piece earned subscribers, which lost them) you have nowhere else.

**Theme connection:** weekly-planning-friction (recurrence 11), search-failure (9), paid-tooling-experimentation (4).
**Framework connection:** Differential value articulation (Schultz, p.43).
**Whitespace anchor:** "We start from your back catalogue."
```

---

## Step 6 — Synthesis (the v0.1.0 close-out)

Sam runs `/sprint-step-6`. All four artefacts generated.

### Sales deck (excerpt — slides 1, 4, 7 of 7)

```markdown
## Slide 1 — Buyer pain (open with their words)

> "I dread Mondays. Every Monday I spend two hours staring at my notes deciding what to write. Every. Monday."
> — substack-paid-2, interview 10

> Speaker notes: This quote landed in five separate interviews in close variants. Open with this. Don't paraphrase — the buyer in the room nods because the buyer in the room is staring at their Monday too.

---

## Slide 4 — Validation evidence

**What we have heard:**

| Theme | Buyers | Costly-action evidence |
|---|---|---|
| Weekly-planning-friction | 5 of 6 paid-newsletter buyers | $39/mo abandoned, $1200/quarter editor, 30-hour Airtable build |
| Paid-tooling-experimentation | 4 of 6 | "$400 in the last year on tools that didn't work" |
| Search-failure | 3 of 6 | "I rewrite it badly because I can't find it" |

**Total interviews logged (this attempt):** 6. **Buyers who took costly action:** 5 of 6.

> Speaker notes: The 5-of-6 ratio is the single strongest data point. Be ready to share interview pseudonyms (and, with permission, real names) if asked.

---

## Slide 7 — Next step

**Specific ask:** Take a 4-week paid pilot at $99/month. We will load your existing back catalogue and show you next Monday's recommendations on Friday.

> Speaker notes: 4 weeks. $99. Loaded with their actual content. The pilot is the conversion event — if Monday-Friday lands, they renew. If not, they don't.
```

### Outreach plan (excerpt — re-engagement message for one buyer)

```markdown
## Section 1 — Re-engagement messages

### substack-paid-1 (interview 9)

**Verbatim quote:** "I've spent maybe $400 in the last year on tools that promised this. None worked."
**Costly-action context:** Paid $39/month for a content-calendar tool last year, cancelled. Now uses Notion + a $49 one-time Notion template.

**Re-engagement message:**

> Subject: I built the thing you described
>
> Hi {first_name},
>
> When we talked in May, you told me "I've spent maybe $400 in the last year on tools that promised this. None worked." — and you mentioned cancelling the content-calendar tool after the matches stopped getting better at month four.
>
> I built it. The version that learns from your back catalogue and your audience response, not from a generic content-trends database.
>
> Want to take a look? I can show you the working version on your actual newsletter in 20 minutes — Wednesday or Friday next week?
>
> Sam
```

### Investor deck (excerpt — slides 1, 7, 9, 12 of 12)

```markdown
## Slide 1 — Problem

> "I dread Mondays. Every Monday I spend two hours staring at my notes deciding what to write. Every. Monday."
> — substack-paid-2, interview 10

**Recurrence:** 11 of 14 paid-newsletter operators interviewed across two sprint attempts described variants of this problem.

---

## Slide 7 — Traction

**Named buyers:** 5 with costly-action evidence (this Sprint attempt) + 8 from prior attempt's adjacent cohort.
**Costly-action signals:** 5 of 6 interviews this attempt.
**Interviews logged:** 14 total across two attempts (6 in attempt 2, 8 in attempt 1 retained for cross-vertical signal).
**Themes validated:** weekly-planning-friction (11), search-failure (9), audience-uncertainty (7), paid-tooling-experimentation (4 attempt-2-only).

**LOIs / pilots / paying customers:**

| Buyer | Stage | Date | Evidence |
|---|---|---|---|
| beehiiv-paid-1 | Verbal LOI for paid pilot | 2026-06-02 | "Yes, set me up at $99/mo for 4 weeks if you can show next Monday on Friday" |
| substack-paid-2 | Verbal LOI for paid pilot | 2026-06-03 | "I'll pay $99 for a month if it cuts Monday in half" |
| substack-paid-1 | Re-engagement queue | 2026-06-08 | Costly-action history; will receive re-engagement message |

---

## Slide 9 — Moat

**Lock-in mechanism:** Workflow lock-in around the operator's own back catalogue.

**Specifically:** every week the operator publishes, the system ingests the new content and the audience-response data (open rate, click rate, churn). Over six months the system holds a model of the operator's voice + audience that no competitor can replicate from external signals. Switching cost compounds with usage.

**Not "proprietary AI".** The foundation models are the same models everyone has. The defensibility is the buyer's own data, captured under their consent in a workflow they keep using.

---

## Slide 12 — Appendix

### Inference economics (detail)

| Metric | Value | Source |
|---|---|---|
| Cost per query (foundation model) | $0.008 | Claude Sonnet API, 8K tokens average |
| Queries per buyer per month | ~40 | 4 planning sessions × 10 queries |
| Total inference cost per buyer per month | $0.32 | calculated |
| Price per buyer per month | $99 | landed in pilot pricing |
| Gross margin per buyer | ~99% | calculated |

### Evals plan

Two evals tracked weekly: (1) Monday-saving — average minutes saved per planning session, self-reported by pilot buyers; (2) Differential evidence accuracy — does the system correctly identify high-audience-response past pieces vs low-response? Manual gold set of 50 hand-labelled past pieces per pilot buyer.

### Buyer-interview tape pointer

- Total interviews: 14 (across two sprint attempts; attempt-1 themes retained as cross-vertical signal per loopback semantics)
- Theme map: `.sprint/sprint.md` Theme Map section
- Costly-action signal log: 5 yes, 1 unclear (attempt 2); 0 yes, 1 unclear (attempt 1 — the loopback rationale)
- Sample verbatim quotes available; pseudonymised by default; with permission, real names

### Sprint provenance

This deck was generated through a structured 6-step Mitchell Agentic Sprint discovery and validation process across two attempts. The first attempt disqualified the solo-creators-with-newsletters ICP after 8 interviews surfaced saturated themes with zero costly-action signals — a fast "no" that re-anchored the second attempt to paid-newsletter operators with revenue in flight.
```

### 2026-AI-era investor-deck checklist (Sam's actual run)

- [x] **Working demo** (slide 4: link to live demo on substack-paid-1's actual back catalogue)
- [x] **Real moat** named — workflow lock-in via the operator's own back catalogue (slide 9)
- [x] **Evals** plan (appendix)
- [x] **Inference economics** with gross margin (~99%) (appendix)
- [x] **Buyer-interview tape pointer** (appendix)

All five satisfied. The deck ships.

### Audio overview

NotebookLM generated a 9:47 audio overview from the full notebook (interview transcripts + expert sources + competitor pages). Saved to `.sprint/artifacts/audio-overview.mp3`. Sam listens to it before the first paid-pilot conversation with beehiiv-paid-1.

---

## Final Sprint state

```yaml
schema-version: 1
sprint-mode: Solo
step: 6
last_approved_step: 6
attempt: 2
created: 2026-04-15
```

**Artefacts:**
- `.sprint/artifacts/sales-deck.md` — 0 evidence gaps
- `.sprint/artifacts/outreach-plan.md` — 0 evidence gaps
- `.sprint/artifacts/investor-deck.md` — 0 evidence gaps
- `.sprint/artifacts/audio-overview.mp3` — 9 minutes 47 seconds

**Loopback Log:**
- attempt 1 — disqualified `creator-economy / solo-creators-with-newsletters-1k-10k / weekly-content-planning` (8 interviews, 0 costly-action signals despite saturated themes; ICP is not a paying buyer for this product class) (2026-05-21)

**Progress Log entries:** 27 across two attempts.

---

## What this example demonstrates

1. **The Sprint completes.** Twelve weeks of structured work; two attempts; one disqualified vertical and one validated one. Sam walks out with three artefacts and an audio briefing.
2. **Loopback is structurally additive.** Attempt 1's themes show up in attempt 2's evidence — `weekly-planning-friction` was already 6-buyers-strong before attempt 2 added 5 more. The investor deck cites the cumulative 11.
3. **Costly action is the difference.** Attempt 1: 0 of 8. Attempt 2: 5 of 6. Same builder, same problem-class, same skills — different ICP. The Sprint's job was to find this out cheaply.
4. **The 2026-AI-era checklist is a real hurdle.** All five non-negotiables can be satisfied. Working demo: live, on a real buyer's content. Real moat: not "proprietary AI" but workflow lock-in around the buyer's own data. Inference economics: ~99% gross margin (cost per query is dominated by buyer-paid pricing). Evals plan: two specific, weekly-tracked metrics. Buyer-interview tape: 14 interviews, named pseudonyms, with permission paths to real names.
5. **The artefacts are usable this week.** The sales deck has no `[EVIDENCE MISSING:` markers. The outreach plan has named buyers and templated messages anchored to their verbatim words. The investor deck satisfies the checklist. Sam takes them into conversations on Monday.

This example is the canonical reference for "what a finished v0.1.0 Sprint looks like".
