# Recommendation — Build Approach for Mitchell Agentic Sprint

> **Phase F output** of the [research plan](research-plan.md). The deliverable. Selects one of the three approaches in [build-options.md](build-options.md), drawing on the [gap analysis](gap-analysis.md).

## TL;DR

**Build the Moderate option as a Claude Code plugin that depends on `campaign-mode` and `six-animals`. Ship a Minimum-shaped walking skeleton in week 1 and put it in front of three friendly testers before committing to the remaining 6–7 weeks.**

Estimated total: 7–8 weeks for one engineer, with a hard go/no-go decision after week 1.

## The choice

**Recommended: Option 2 — Moderate.**

| Option | Verdict | Reason |
|---|---|---|
| Minimum | Reject as final shape | Cannot deliver the concept's headline promise (anti-sycophancy + investor-conversation-ready artifacts). Council voices will feel interchangeable; Mom Test discipline cannot be enforced; investor decks will lack defensible evidence. *However*, Minimum's first-week deliverables are reused as Moderate's walking skeleton — see "Phasing" below. |
| **Moderate** | **Select** | Hits the headline promise (real domain-knowledgeable Council voices, enforced Mom Test, working loopback) without front-loading tooling that may not be the bottleneck. Closes Q1–Q4 from the gap analysis with high confidence. Q5 (anti-sycophancy verification via eval) is deferred to Extensive — accepted risk. |
| Extensive | Defer | Premature. The concept itself flags core uncertainties (linear flow, named-expert assumption, whether AI can replace a coach). Building tooling for 12–16 weeks before validating those assumptions inverts cost-of-no. Tooling layer becomes justified only if Moderate ships and tester demand pulls it forward. |

## Phasing — week 1 walking skeleton

The first week of Moderate is shaped to be Minimum-equivalent: a runnable Step 1 + a single Council invocation, end-to-end. The point is to get something in front of testers fast.

| Week | Output | Decision gate |
|---|---|---|
| 1 | Plugin scaffolds. `/sprint-start` runs Step 1 with Gandalf-as-skin. `/sprint-council` invokes one Mini Council voice (Seed VC, drafted as the canonical voice). State written to `.sprint/sprint.md`. Three friendly testers run through Step 1 + Council. | **Go/no-go on Moderate.** If testers report the Seed VC voice has real domain depth and the Step 1 framing is useful, continue. If not, revisit. |
| 2–3 | Remaining 4 Council voices drafted. `/sprint-council` orchestrates all five. Step 2 (Vertical) command. Loopback command. | Continue if Council voices are differentiable. |
| 4–5 | Steps 3 (Buyer Interviews) + 4 (Framework). Banned-question linter. Saturation detector. | Continue if linter false-positive rate is acceptable. |
| 6–7 | Steps 5 (Competitor) + 6 (Synthesis). Three artifact templates. Three worked examples. Tester debriefs. | Ship. |
| 8 | Buffer / polish / docs. | Tag v0.1.0. |

If the week-1 gate fails, fallback options: (a) prompt-iterate on the Seed VC voice for another week before continuing; (b) downgrade scope to Minimum and accept the headline-promise gap; (c) escalate findings to Scott and reframe the product.

## Why Moderate is the right pick — five points

1. **The headline product promise is anti-sycophancy** (concept §6, §10). That requires the Council voices to actually push back with domain credibility. Minimum can't get there with profile-pack skinning alone (gap analysis §2). Moderate's 5 new SKILL.md files *can*.
2. **Mom Test discipline is the difference between "buyer interviews" and "founder reassurance theatre"** (concept §4.3). Minimum has no enforcement layer. Moderate's banned-question linter + saturation detector make the discipline operational.
3. **Loopback is the cost-of-no mechanism that prevents the concept's worst failure mode** — builders shipping doomed products because admitting wrongness is too expensive (concept §7). Minimum has no loopback handler. Moderate ships one.
4. **Extensive's tooling layer is solving downstream problems** (slide rendering, theme clustering, evals) that aren't on the critical path until users specifically demand them. We add them when the demand signal arrives, not speculatively.
5. **Campaign-mode is genuinely well-shaped to host this**, per the gap analysis. ~70% of the infrastructure is reusable as-is (transcripts, progress logging, AskUserQuestion conventions, profile system, six-animal advisory layer). We're extending, not fighting.

## Answers to the seven research questions

| Q | Question | Answer | Where to read |
|---|---|---|---|
| Q1 | Sequence fit | Achievable through new state schema + new gate command, not pure rewrite. Moderate scope. | gap-analysis §1 |
| Q2 | Mini Council depth | Profile packs insufficient. Need 5 new SKILL.md files with embedded domain heuristics. | gap-analysis §2 |
| Q3 | Artifact reach | Markdown-first closes 80% of value. Slide rendering is optional polish, defer to Extensive. | gap-analysis §7 |
| Q4 | Loopback semantics | New schema + 1 new command. Achievable in Moderate. | gap-analysis §4–5 |
| Q5 | Anti-sycophancy enforcement | Tone via prompt preambles (free, lifted from Dragon). Verification via eval set is Extensive-tier — accepted as residual risk for Moderate v1. | gap-analysis §6 |
| Q6 | Distribution | **Open — assumes Claude Code plugin for Moderate.** If standalone web/desktop is required, Extensive is the floor and recommendation changes. | open question |
| Q7 | Ownership | **Open — assumes one engineer, presumed to be Chris.** Affects time budget but not architecture. | open question |

## Next actions (concrete)

1. **User answers the six open questions** (below) — blocks everything downstream. ETA: 1 conversation.
2. **Spin up plugin scaffolding** in this repo: `.claude-plugin/plugin.json`, `commands/`, `skills/`, `docs/templates/`, `.sprint/` ignored. ETA: half a day.
3. **Draft `seed-vc-agent/SKILL.md`** as the canonical Council voice. Includes: 2026-AI-era investor checklist, moat taxonomy, traction expectations, voice/tone borrowed from Dragon. This file becomes the template for the other four. ETA: 2 days.
4. **Build the Step 1 + Council walking skeleton** end-to-end. Tester-facing. ETA: 4 days, ending by end of week 1.
5. **Recruit three friendly testers** from Chris's immediate network. Send them through Step 1 + Council. Run debrief interviews using Mom Test discipline. ETA: ongoing through week 2.

## Residual open questions for the user

These are open in the [research plan](research-plan.md) and remain unanswered. Each shapes execution:

1. **Distribution channel (Q6)** — Claude Code plugin? Claude Desktop plugin? Cursor? Standalone? *Recommendation assumes Claude Code plugin.*
2. **Spike or paper-only?** — Recommendation collapses this question by *making the spike the week-1 walking skeleton*. The week-1 deliverable is the spike; if it satisfies, we continue to full Moderate.
3. **Time budget** — Is 7–8 weeks acceptable? Is there a hard date?
4. **Coupling tolerance** — Hard `campaign-mode` dependency OK, or does MAS need to stand alone? *Recommendation assumes hard dependency.*
5. **v1 user persona** — Immediate AI-builder network or general-public AI-builders? *Recommendation assumes immediate network for v1, raises bar for v2.*
6. **Scott's involvement** — High-fidelity loop (Scott reviews artifacts as we go) or low-fidelity (Scott waits for v1)? *Recommendation assumes high-fidelity — Scott reviews after week 1 walking skeleton, before committing remaining 6 weeks.*

## What success looks like 90 days from now

- v0.1.0 tagged on `mitchell-agentic-sprint` repo
- Three completed Sprints by friendly testers, with all six steps and at least one loopback observed
- Three artifact sets (sales deck + outreach plan + investor deck) shared with Scott for review
- A documented assessment of whether the Mini Council voices feel adversarial-with-credibility or just adversarial
- A short list of Extensive-tier capabilities that user feedback has *pulled forward* (e.g., "everyone asked for PPTX → add slide rendering"). Without that signal, no Extensive work happens.

## What success does not look like

- A polished plugin that no one has used end-to-end
- Slide rendering before three testers have completed Step 6
- An anti-sycophancy eval set built before we know what real users find sycophantic
- A second product extension (e.g., a CRM integration, a buyer-database lookup) before v0.1.0 ships

## Confidence and what could change this recommendation

**High confidence:**
- Campaign-mode + Six Animals are well-shaped hosts (Q1–Q4)
- Markdown-first artifacts cover the headline promise (Q3)
- Moderate is the right scope for v1 (Q1–Q4)

**Medium confidence:**
- The 5 Council voices will feel sufficiently differentiated *after* the first prompt-iteration round (Q2). Tested in week 1.
- Mom Test linter false-positive rate will be acceptable (gap analysis §3). Tested in week 4–5.

**Low confidence:**
- Anti-sycophancy holds under sustained pressure from real users without an eval set (Q5). Accepted risk for v1; revisit for v2.
- Distribution as Claude Code plugin is the right channel for the v1 audience (Q6). Open question.

This recommendation is reversible until week-1 gate. After that, the architectural commitments (state schema, command structure) are difficult to back out.
