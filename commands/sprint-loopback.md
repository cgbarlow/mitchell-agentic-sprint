---
description: Loopback the Sprint. Reset to Step 2 (Vertical Stack) retaining Builder Profile, Theme Map, and Expert Framework; clear Vertical Stack, Competitor Map, Positioning Whitespace, and Artifacts. Concept §7 — make a "no" cheap.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Loopback

Concept §7: when validation fails, the Sprint loops the user back without making them start from scratch. Builder Profile (Step 1), interview themes (Step 3), and expert framework (Step 4) survive the loopback. Vertical Stack and downstream artifacts are cleared.

The point is to make a "no" cheap. Most builders ship a doomed product because the cost of admitting they were wrong feels too high. The Sprint normalises pivoting back to Step 1 as a structured move, not a failure.

## Step 1: Verify state

Use the Glob tool to check `.sprint/sprint.md` exists.

**If it does not exist:**

> No active sprint. Loopback is meaningful only inside an active sprint.

Stop.

**If it exists:** read `.sprint/sprint.md`. Parse frontmatter.

**If `last_approved_step < 1`:**

> Loopback is meaningful from Step 2 onward. You're still at Step 1 (Discovery). If you want to revise your Builder Profile, run `/sprint-start` instead.

Stop.

## Step 2: Surface what survives and what is cleared

Tell the user (so they understand what's about to happen):

> **Loopback semantics** (per [SPEC-005-A](docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md)):
>
> **Retained** (these survive into the new attempt):
> - Builder Profile (Step 1 — your unfair advantages)
> - Backup Verticals (your prior list of alternatives)
> - Interview Log (verbatim transcripts; tagged with the disqualified vertical for traceability)
> - Theme Map (themes are vertical-agnostic enough to be reused)
> - Costly-Action Signals (warmest leads stay warm)
> - Expert Framework (the named expert and adapted framework)
> - Loopback Log (this loopback gets appended)
> - Progress Log (everything you've done so far stays)
>
> **Cleared** (these reset for the new attempt):
> - Vertical Stack
> - Competitor Map
> - Positioning Whitespace
> - Artifacts (sales deck, outreach plan, investor deck paths)
>
> Step resets to 2 (Vertical Stack), `last_approved_step` resets to 1, `attempt` increments.

## Step 3: Identify the loopback flavour

Per concept §7 there are three typical flavours. Use `AskUserQuestion`:

> **What kind of loopback is this?**

Options:

1. **Different ICP, same vertical** — pain is real but the targeted buyer was wrong; sharpen the ICP and re-attempt
2. **Different vertical, adjacent skills** — vertical doesn't have buyers willing to pay; an adjacent vertical where unfair advantages still apply might
3. **Different workflow, same vertical** — picked the wrong job-to-be-done; same buyer, different leverage point
4. **Other / I'll describe it** — free-form

## Step 4: Capture the disqualified vertical and reason

Use `AskUserQuestion` to capture the vertical name being disqualified:

> **Which vertical are you disqualifying?** Use the form `<vertical> / <sub-vertical> / <ICP>` from your current Vertical Stack.

(This question is free-form; the user types their answer.)

Then ask the reason:

> **What surfaced in this attempt that disqualified the vertical?** Examples: no costly-action signals after N interviews; the buyer interviewed but the buyer's problem wasn't worth their money; the competitor map showed no whitespace; the framework didn't fit the workflow.

## Step 5: Confirm before mutating

Use `AskUserQuestion`:

> **Confirm loopback?** This will clear Vertical Stack, Competitor Map, Positioning Whitespace, and Artifacts sections of `.sprint/sprint.md`. Builder Profile, Interview Log, Theme Map, Costly-Action Signals, and Expert Framework are retained. This is destructive but reversible via git if needed.

Options:

1. **Confirm — proceed with loopback**
2. **Cancel — make no changes**

If the user cancels, stop.

## Step 6: Apply the loopback

Use Edit on `.sprint/sprint.md` to:

1. **Append to Loopback Log** under the H2 heading:
   ```
   - **attempt {current attempt number}** — disqualified `{vertical name from Step 4}` ({reason from Step 4}) ({today's date})
   ```

2. **Append to Progress Log**:
   ```
   - **Progress** — Loopback ({flavour from Step 3}); disqualified `{vertical name}` ({today's date})
   ```

3. **Clear** the content under each of these H2 headings (leave the heading itself):
   - `## Vertical Stack`
   - `## Competitor Map`
   - `## Positioning Whitespace`
   - `## Artifacts`

4. **Update frontmatter**:
   - `step: 2`
   - `last_approved_step: 1`
   - `attempt: {previous + 1}`

5. **Retain unchanged** (do not edit):
   - `## Builder Profile`
   - `## Backup Verticals`
   - `## Interview Log`
   - `## Theme Map`
   - `## Costly-Action Signals`
   - `## Expert Framework`

## Step 7: Surface what to do next

Tell the user (terse and direct):

> Loopback complete. Attempt {N+1} now.
>
> Your Builder Profile is intact. Your interview themes from the previous attempt are intact (tagged for traceability). Your expert framework is intact.
>
> Cleared: Vertical Stack, Competitor Map, Positioning Whitespace, Artifacts. You re-enter at Step 2.

Use `AskUserQuestion`:

1. **Re-enter Step 2 (Vertical Stack)** — pick a new vertical with Gandalf's help, informed by what you just learned (use `/sprint-step-2`)
2. **Convene the Mini Council first** — pressure-test the loopback decision before re-entering Step 2 (use `/sprint-council`)
3. **Pause** — return later via `/sprint-continue`

Never reference slash commands in user-facing text — use natural language ("re-enter Vertical Stack", "convene the Council", "pause").

---

## Injected Context

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Concept §7 (the loop): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
