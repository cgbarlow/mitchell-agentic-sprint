# Worked Example 2 — Prosumer Tool, with Loopback

**Purpose:** voice-fidelity reference per [ADR-010](../adrs/ADR-010-TDD-Scope.md), and demonstration of Step 3 sub-flows (script linter, interview logging, theme map, saturation, loopback) per [SPEC-008-A](../adrs/specs/SPEC-008-A-Anti-Sycophancy.md) and concept §4.3 + §7.

**Scenario:** Fictional builder Sam, who's been building Notion-adjacent tools for years and has a thesis about a "knowledge graph for solo creators". Sam runs through Steps 1–3 and ends up triggering a loopback when the interviews surface no costly-action signals despite saturated themes.

This example is intentionally a *failed first attempt*. Concept §7: "make a 'no' cheap."

---

## Step 1 — Builder Profile (abridged)

> **Background:** 6 years building productivity tools. Three indie launches; one acquired ($120K), two flatlined. Active in two creator-economy Discord communities; ~600 Twitter followers in that niche.
>
> **Unfair advantages:** First-name access to ~25 active solo creators in the productivity-tool niche; ran a Notion template store for 18 months and saw the buying behaviour up close.
>
> **Runway:** 7 months solo, self-funded.
>
> **Rough idea:** "AI-powered knowledge graph for solo creators — auto-link your notes by topic, pull related content into your weekly plan."
>
> **Known buyers:** ~10 solo creators willing to take a call. None have paid for a knowledge-graph tool specifically (they use Notion / Obsidian for free).

## Step 2 — Vertical Stack v1

| Layer | Content |
|---|---|
| Vertical | Creator economy |
| Sub-vertical | Solo creators publishing weekly long-form content |
| ICP | Solo creators with 1k–10k newsletter subscribers, US/EU, currently using Notion or Obsidian |
| Specific workflow | Weekly content planning — picking what to write next based on past notes and audience response |
| AI leverage point | Auto-link related notes by topic; surface "you wrote about this six months ago, audience liked it" prompts during planning |

**Backup Verticals:**

1. Solo paid-newsletter operators (Substack/Beehiiv 1k+ paid subs) — same buyer with money in flight
2. Audio creators (podcasters with weekly schedules) — adjacent workflow

The Mini Council (not shown here for brevity) reaches **3 Pass for now, 2 In play** at Step 1→2; Sam advances with the conditions noted (no costly-action signal yet; pricing undecided).

---

## Step 3 — Sub-flow A: outreach + interview script generation

Sam runs `/sprint-step-3` and picks "Starting fresh — generate the interview script and outreach plan."

Gandalf produces a draft 9-question script. The Step 3 command shells out to the linter:

```bash
$ PYTHONPATH=${CLAUDE_PLUGIN_ROOT} python -m helpers.interview_validator /tmp/sprint-script-draft.txt
/tmp/sprint-script-draft.txt:1: ✓
/tmp/sprint-script-draft.txt:2: ✓
/tmp/sprint-script-draft.txt:3: hypothetical-would-you — "Would you…" speculates about future behaviour. Ask about past behaviour instead.
/tmp/sprint-script-draft.txt:4: ✓
/tmp/sprint-script-draft.txt:5: ✓
/tmp/sprint-script-draft.txt:6: opinion-would-it-be-useful — "Would it be useful…" leads to social-desirability bias.
/tmp/sprint-script-draft.txt:7: ✓
/tmp/sprint-script-draft.txt:8: ✓
/tmp/sprint-script-draft.txt:9: ✓
exit code: 1
```

The Step 3 command surfaces both violations and asks Sam: regenerate, override, or cancel. Sam picks **regenerate**. Gandalf re-asks questions 3 and 6 with the linter findings as feedback:

| # | Original (flagged) | Regenerated (linter-clean) |
|---|---|---|
| 3 | "Would you use a tool that auto-links your notes?" | "Walk me through the last time you wished one of your notes connected to another. What did you actually do — searched manually, gave up, used a tag system?" |
| 6 | "Would it be useful to see related past content during your weekly plan?" | "Tell me about the last weekly plan you wrote. How did you decide what to write about that week? What did you reference?" |

Re-run the linter on the rewritten questions:

```
$ PYTHONPATH=${CLAUDE_PLUGIN_ROOT} python -m helpers.interview_validator /tmp/sprint-script-draft-v2.txt
exit code: 0
```

Clean. Script locked into `.sprint/sprint.md` Interview Log → Outreach plan → Interview script.

Outreach plan also locked: target list of 22 named solo creators (drawn from Sam's Discord and Twitter network), Sales Navigator filter (creator-economy occupation tags + 1k+ followers + US/EU), 5 communities (two Discord servers, the Indie Hackers forum, two paid newsletters' chat groups), cold-outreach message ≤120 words anchored to "I noticed you wrote about [topic]; can I learn how you decide what to write next?"

---

## Step 3 — Sub-flow B: interviews logged

Sam runs the cold outreach over 12 days. Holds 8 interviews. Each one logged via `/sprint-step-3` → "Log a new interview".

Aggregated `.sprint/interviews/` directory (8 files). Excerpt of the log table written into `.sprint/sprint.md`:

| # | Pseudonym | Date | Length | Costly action? | Themes |
|---|---|---|---|---|---|
| 01 | newsletter-writer-1 | 2026-05-12 | 38min | no | weekly-planning-friction, search-failure, tag-decay |
| 02 | newsletter-writer-2 | 2026-05-13 | 42min | no | weekly-planning-friction, audience-uncertainty, tag-decay |
| 03 | youtube-essayist-1 | 2026-05-14 | 35min | no | search-failure, audience-uncertainty, batch-burnout |
| 04 | newsletter-writer-3 | 2026-05-15 | 41min | unclear | weekly-planning-friction, search-failure, tag-decay |
| 05 | substack-paid-1 | 2026-05-16 | 50min | no | weekly-planning-friction, search-failure, audience-uncertainty |
| 06 | newsletter-writer-4 | 2026-05-18 | 33min | no | weekly-planning-friction, tag-decay |
| 07 | youtube-essayist-2 | 2026-05-19 | 40min | no | search-failure, audience-uncertainty |
| 08 | newsletter-writer-5 | 2026-05-20 | 36min | no | weekly-planning-friction, search-failure |

**Costly-Action Signals:** **0 yes**. One **unclear** (newsletter-writer-3 mentioned paying $19 for a Notion template that "kind of did this" but couldn't remember the name; not a clear costly-action signal).

---

## Step 3 — Sub-flow C: theme map

Sam runs `/sprint-step-3` → "Update the theme map across all interviews".

```markdown
| Theme | Interviews | Buyers (pseudonyms) |
|---|---|---|
| **weekly-planning-friction** | 6 | newsletter-writer-1, -2, -3, -4, -5, substack-paid-1 |
| **search-failure** | 6 | newsletter-writer-1, -3, -4, -5, youtube-essayist-1, -2, substack-paid-1 |
| **audience-uncertainty** | 4 | newsletter-writer-2, youtube-essayist-1, -2, substack-paid-1 |
| **tag-decay** | 4 | newsletter-writer-1, -2, -3, -4 |
| batch-burnout | 1 | youtube-essayist-1 |
```

Three themes appear in 4+ interviews — strong clustering. But:

> **Costly-Action Signals:** none. No buyer paid for a knowledge-graph tool. One paid $19 for a Notion template once. The pain is real; the wallet is not.

---

## Step 3 — Sub-flow D: saturation check

Sam runs `/sprint-step-3` → "Check saturation". The command builds the JSON:

```json
[
  ["weekly-planning-friction", "search-failure", "tag-decay"],
  ["weekly-planning-friction", "audience-uncertainty", "tag-decay"],
  ["search-failure", "audience-uncertainty", "batch-burnout"],
  ["weekly-planning-friction", "search-failure", "tag-decay"],
  ["weekly-planning-friction", "search-failure", "audience-uncertainty"],
  ["weekly-planning-friction", "tag-decay"],
  ["search-failure", "audience-uncertainty"],
  ["weekly-planning-friction", "search-failure"]
]
```

And shells out:

```
$ PYTHONPATH=${CLAUDE_PLUGIN_ROOT} python -m helpers.saturation --human /tmp/sprint-themes.json
Total interviews: 8
Themes per interview (new only): [3, 1, 1, 0, 0, 0, 0, 0]
Consecutive interviews with no new themes (from end): 5
Threshold: 3
Saturated: YES — last 3 interviews surfaced no new themes; consider stopping here.
```

Saturation reached. Themes converged at interview 4. Interviews 6–8 added literally nothing new.

But the theme map says: the pain is present, and the wallet is not.

---

## Step 3 — Sub-flow E: the go/no-go decision

Sam runs `/sprint-step-3` → "Conclude Step 3".

The command surfaces:

> **Step 3 close-out.**
>
> 8 interviews logged. 4 strong recurring themes (weekly-planning-friction, search-failure, audience-uncertainty, tag-decay). Saturation reached — last 5 interviews added no new themes.
>
> **0 costly-action signals.** 1 unclear data point ($19 Notion template, recall failure). No buyer in this ICP has paid for a knowledge-graph tool.
>
> The themes are real. The buyers are not paying for them.

Sam's options:

1. **Go — proceed to Step 4** with the validated themes
2. **Loopback** — try a different ICP / vertical / workflow
3. **Pause**

Sam picks **Loopback**. The reasoning, captured in the loopback log: themes are real but solo creators are not a paying buyer for this product class. The backup vertical (paid-newsletter operators with skin in the game) is the next attempt.

---

## Loopback execution

Sam runs `/sprint-loopback`. The command asks:

- **Loopback flavour:** _Different ICP, same vertical_ (paid-newsletter operators are still in the creator economy)
- **Disqualified vertical:** `creator-economy / solo-creators-with-newsletters-1k-10k / weekly-content-planning`
- **Reason:** "8 interviews, 0 costly-action signals despite saturated themes; ICP is not a paying buyer for this product class"
- **Confirm:** yes

The command applies the SPEC-005-A retain/clear partition:

| Section | What happens |
|---|---|
| **Builder Profile** | **Retained** — Sam's unfair advantages are still real |
| **Backup Verticals** | **Retained** — the list of alternatives remains useful |
| **Vertical Stack** | **Cleared** — the disqualified vertical is gone |
| **Interview Log** | **Retained** — but tagged as `attempt 1` for traceability |
| **Theme Map** | **Retained** — these themes may apply to the next ICP too |
| **Costly-Action Signals** | **Retained** — empty in this case, but the section structure stays |
| **Expert Framework** | **Retained** — wasn't populated yet, but the section structure stays |
| **Competitor Map** | **Cleared** |
| **Positioning Whitespace** | **Cleared** |
| **Artifacts** | **Cleared** |

Frontmatter updates:

```diff
- step: 3
- last_approved_step: 3
- attempt: 1
+ step: 2
+ last_approved_step: 1
+ attempt: 2
```

**Loopback Log entry appended:**

```
- **attempt 1** — disqualified `creator-economy / solo-creators-with-newsletters-1k-10k / weekly-content-planning` (8 interviews, 0 costly-action signals despite saturated themes; ICP is not a paying buyer for this product class) (2026-05-21)
```

**Progress Log entry appended:**

```
- **Progress** — Loopback (different ICP, same vertical); disqualified `creator-economy / solo-creators-with-newsletters-1k-10k / weekly-content-planning` (2026-05-21)
```

---

## Re-entry at Step 2 — Vertical Stack v2

Sam runs `/sprint-step-2` (gate is now 1, attempt is 2). Gandalf re-engages, this time with two pieces of context Sam didn't have on attempt 1:

1. The themes from attempt 1 (still in the Theme Map) — `weekly-planning-friction` and `search-failure` were the strongest signals
2. The lesson from attempt 1 — "the problem is real but solo creators don't pay; pivot to ICPs with money in flight"

New Vertical Stack draft:

| Layer | Content |
|---|---|
| Vertical | Creator economy |
| Sub-vertical | **Paid-newsletter operators** (changed) |
| ICP | **Substack/Beehiiv operators with 1k+ paid subscribers, $5K+ MRR, US/EU** (sharpened — has-revenue is the gate) |
| Specific workflow | Weekly content planning — same workflow, different buyer |
| AI leverage point | Same — auto-link, surface past topics with audience-response data |

Sam advances. The Step 1→2 Mini Council convenes again on the new Stack, with the previous attempt's evidence in scope. (Continued in v0.1.0 Phase 4+ when Steps 4–6 ship.)

---

## What this example demonstrates

1. **Linter-gated script generation works.** Two violations on the first draft, regenerated to clean. The Step 3 command never surfaced violating questions to the user.
2. **Theme map + saturation = stop signal.** Sam ran 8 interviews, not because 8 was the magic number, but because saturation said so. Concept §6: "Saturation over headcount."
3. **Themes can be real and the buyer can still not pay.** Strong theme clustering + zero costly-action signals = loopback, not "great theme map, let's build". Concept §4.3: "Stated problems are cheap. Revealed problems are signal."
4. **Loopback is structured, not chaotic.** Builder Profile, Backup Verticals, Theme Map, and Expert Framework survived. Vertical Stack and downstream cleared. Sam re-entered Step 2 with everything she'd learned.
5. **The cost of "no" was 12 days and 8 conversations.** Not a year and a built product. Concept §7: "make a 'no' cheap."

This example is the canonical reference for the Phase 3 tester gate.
