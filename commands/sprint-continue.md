---
description: Re-enter an active Mitchell Agentic Sprint where you left off. Reads .sprint/sprint.md, surfaces current state and next-step options, dispatches to the appropriate step or sub-flow.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Continue Sprint

`/sprint-continue` is the re-entry dispatcher. It reads the current state of `.sprint/sprint.md` and routes the user to the right next action — whether that's continuing a step in progress, advancing to the next step, convening the Mini Council, or pausing again.

## Step 1: Verify state

Use Glob to check `.sprint/sprint.md` exists.

**If it does not exist:**

> No active sprint. Run `/sprint-start` to begin a new one.

Stop.

**If it exists:** read `.sprint/sprint.md`. Parse frontmatter. Read the section content for context.

## Step 2: Surface current state

Tell the user (compact summary):

> **Sprint state**
>
> - Sprint mode: {sprint-mode}
> - Step: {step}
> - Last approved step: {last_approved_step}
> - Attempt: {attempt}
> - Created: {created}

Then a one-line per-section status:

> **Sections status:**
>
> - Builder Profile: {populated | empty}
> - Vertical Stack: {populated | empty}
> - Backup Verticals: {populated | empty}
> - Interview Log: {N interviews logged | empty}
> - Theme Map: {N themes | empty}
> - Costly-Action Signals: {N signals | empty}
> - Expert Framework: {populated | empty}
> - Competitor Map: {populated | empty}
> - Positioning Whitespace: {populated | empty}
> - Artifacts: {paths or "none generated"}
> - Loopback Log: {N entries | empty}

If `attempt > 1`, also surface the most recent Loopback Log entry so the user remembers why they're on this attempt.

## Step 3: Dispatch based on `(step, last_approved_step)`

Use `AskUserQuestion` to surface next-step options. The available options depend on the state.

### If `step == 1` and `last_approved_step == 0` (Step 1 in progress)

Options:
1. **Continue Step 1** — re-enter Discovery (`/sprint-start`)
2. **Pause** — stop here

### If `step == 1` and `last_approved_step == 1` (Step 1 done; awaiting Council or Step 2)

Options:
1. **Convene the Mini Council** — pressure-test Builder Profile and proposed Vertical Stack (`/sprint-council`) — Recommended
2. **Proceed to Step 2 (Vertical Stack)** (`/sprint-step-2`)
3. **Pause**

### If `step == 2` and `last_approved_step in {1, 2}` (Step 2 in progress or done)

Options:
1. **Continue Step 2** — re-enter Vertical Stack work (`/sprint-step-2`)
2. **Convene the Mini Council** — pressure-test the Vertical Stack (`/sprint-council`) — Recommended at this transition
3. **Proceed to Step 3 (Buyer Interviews)** if Step 2 is approved (`/sprint-step-3`)
4. **Loopback** — reset to Step 2 retaining Step 1 (`/sprint-loopback`)
5. **Pause**

### If `step == 3` and `last_approved_step in {2, 3}` (Step 3 in progress or done)

Options depend on Interview Log and saturation state:
1. **Log a new interview** (`/sprint-step-3` → sub-flow B)
2. **Update theme map** (`/sprint-step-3` → sub-flow C) — if at least one interview logged
3. **Check saturation** (`/sprint-step-3` → sub-flow D) — if at least 3 interviews logged
4. **Conclude Step 3** (`/sprint-step-3` → sub-flow E) — if Theme Map non-empty
5. **Loopback** (`/sprint-loopback`)
6. **Pause**

### If `step == 4` and `last_approved_step in {3, 4}` (Step 4 in progress or done)

Options:
1. **Continue Step 4** — re-enter Framework work (`/sprint-step-4`)
2. **Convene the Mini Council** — Step 4→5 transition is the second meaningful Council fire point (`/sprint-council`) — Recommended if Step 4 is approved
3. **Proceed to Step 5 (Competitor + Positioning)** if Step 4 approved (`/sprint-step-5`)
4. **Loopback**
5. **Pause**

### If `step == 5` and `last_approved_step in {4, 5}` (Step 5 in progress or done)

Options:
1. **Continue Step 5** (`/sprint-step-5`)
2. **Proceed to Step 6 (Synthesis)** if Step 5 approved (`/sprint-step-6`)
3. **Loopback**
4. **Pause**

### If `step == 6` and `last_approved_step in {5, 6}` (Step 6 in progress or sprint complete)

Options:
1. **Generate the next artefact** (`/sprint-step-6`) — sales deck / outreach plan / investor deck / audio overview
2. **View existing artefacts** — `ls .sprint/artifacts/`
3. **Conclude the Sprint** (`/sprint-step-6` → sub-flow E) — if artefacts populated and not yet approved
4. **Run another attempt** — `/sprint-start` (the current sprint archives automatically)
5. **Loopback** — useful if Step 6 surfaced gaps suggesting a different vertical
6. **Pause**

## Step 4: Route to the chosen action

Trigger the appropriate command based on the user's pick. Do not reference slash commands in user-facing text — describe the action ("convene the Council", "advance to Buyer Interviews", "loopback to Discovery") and route behind the scenes.

If the user picks "Pause", simply stop with a brief acknowledgement:

> Sprint state preserved. Run `/sprint-continue` when you're ready.

---

## Injected Context

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Step gate spec (SPEC-007-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-007-A-Step-Gate-Commands.md`
