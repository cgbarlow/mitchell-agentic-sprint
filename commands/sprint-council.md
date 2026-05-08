---
description: Convene the Mitchell Agentic Sprint Mini Council to pressure-test the user's current state. Adversarial-by-default skeptical voices that refuse flattery and force specificity.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Convene the Mini Council

The Mini Council is the adversarial heart of the Sprint. It exists because builders' thinking gets laundered through models that won't tell them no. Council voices refuse flattery, push back on vague answers, and force the user to cite a person, a number, or an artifact for every claim.

**Phase 1 walking skeleton scope:** only the Seed VC voice is implemented. The remaining four voices (Churned Customer, Competitor Founder, Future-Self, Grumpy PM) ship in Phase 2.

Follow these steps in order.

## Step 1: Verify sprint state

Use the Glob tool to check `.sprint/sprint.md` exists.

**If it does not exist:**

Tell the user:

> No active sprint found. Run `/sprint-start` first to begin a new Sprint.

Stop here.

**If it exists:**

Read `.sprint/sprint.md`. Confirm the user has at least a Builder Profile (Step 1 output). If the Builder Profile section is empty, tell the user:

> Step 1 (Discovery) is not yet complete. The Council needs a Builder Profile to evaluate. Return to `/sprint-start` to complete Discovery first.

Stop here.

## Step 2: Determine invocation context

Read the `step` and `last_approved_step` from frontmatter. The Mini Council fires meaningfully at two transitions:

- **Step 1 → Step 2** (`step` is 1 or 2 with `last_approved_step` ≥ 1): pressure-test Builder Profile and proposed Vertical Stack
- **Step 4 → Step 5** (`step` is 4 or 5 with `last_approved_step` ≥ 4): pressure-test the validated thesis before competitor mapping

Identify which transition this invocation covers based on current state. If the user is at any other point, the Council can still be invoked but flag this in your introduction:

> The Mini Council is most useful between Step 1→2 and Step 4→5. You're currently at Step {N}. Convene anyway? (use AskUserQuestion to confirm)

## Step 3: Invoke Seed VC

Adopt the Seed VC identity by loading the skill from the injected context paths below. Provide the Seed VC with:

- The current Builder Profile (full)
- The current Vertical Stack draft, if it exists (Step 2 work)
- The current Theme Map, if Step 3 has begun
- The current Expert Framework, if Step 4 is complete
- Whether this is a Step 1→2 or Step 4→5 invocation
- The current `attempt` number from frontmatter

Do **not** provide the Seed VC with:

- The user's conversation transcripts (context isolation)
- Notes from Gandalf
- Animal advisor feedback

The Seed VC will produce a verdict (Pass / Pass for now / In play) per their SKILL.md output format. Display the full critique to the user.

## Step 4: Append Council outcome to sprint state

After the Seed VC concludes, append a Progress Log entry to `.sprint/sprint.md`:

```
- **Progress** — Mini Council (Seed VC) verdict: {Pass | Pass for now | In play} ({TODAY})
```

If the Seed VC's verdict is Pass and the user is at the Step 1→2 transition, they may want to loopback (revise their Vertical Stack) before advancing. Surface this in the next step.

## Step 5: Offer next-step options

Use `AskUserQuestion` to present the user with their options after the Council critique. Tailor the options to the current step and the verdict:

**If the verdict is Pass (cannot advance as-is):**

1. **Loopback** — revise the Builder Profile and try a different vertical direction (use `/sprint-loopback` — available from Phase 2)
2. **Address the specific evidence gap** — go back to Step 1 framing with Gandalf to fill the missing evidence
3. **Pause and reflect** — return later via `/sprint-continue`

**If the verdict is Pass for now (advance once condition met):**

1. **Address the specific condition** — go back to refine the Builder Profile or Vertical Stack
2. **Proceed anyway** — advance to next step understanding the Council reservation (use `/sprint-step-2` — available from Phase 2)

**If the verdict is In play (clear to advance):**

1. **Proceed to Step 2 (Vertical Stack)** — narrow the vertical-stack-with-AI-leverage definition (use `/sprint-step-2` — available from Phase 2)
2. **Pause here** — return later via `/sprint-continue`

In all cases, never reference slash commands in user-facing text — use natural language ("convene the Council again", "proceed to Vertical Stack", "loopback to Discovery") and trigger the appropriate command behind the scenes.

---

## Injected Context

The following files contain essential context for this command. **Before completing Step 3, use the Read tool to load every file listed in this section.**

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Seed VC skill definition: !`echo ${CLAUDE_PLUGIN_ROOT}/skills/seed-vc-agent/SKILL.md`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Concept document (anti-sycophancy posture, §6): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
