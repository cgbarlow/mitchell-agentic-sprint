---
description: Convene the Mitchell Agentic Sprint Mini Council — five adversarial-by-default skeptical voices (Seed VC, Churned Customer, Competitor Founder, Future-Self, Grumpy PM) that pressure-test the user's current state. Refuses flattery; forces specificity; cites or it didn't happen.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Convene the Mini Council

The Mini Council is the adversarial heart of the Sprint. It exists because builders' thinking gets laundered through models that won't tell them no. Each Council voice refuses flattery, pushes back on vague answers, and forces the user to cite a person, a number, or an artifact for every claim.

The Council fires meaningfully at two transitions:

- **Step 1 → Step 2** — pressure-test Builder Profile and proposed Vertical Stack
- **Step 4 → Step 5** — pressure-test the validated thesis before competitor mapping

It can also be invoked at any time mid-sprint as a sanity check.

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

Read `step` and `last_approved_step` from frontmatter. Identify which transition this invocation covers:

- **Step 1→2** — `step` is 1 or 2 and `last_approved_step` ≥ 1 (or the user is mid-Step-2)
- **Step 4→5** — `step` is 4 or 5 and `last_approved_step` ≥ 4
- **Other** — anywhere else; flag and confirm

If invoked at any other state, use `AskUserQuestion`:

> The Mini Council is most useful between Step 1→2 and Step 4→5. You're currently at Step {N} (last approved: {last_approved_step}). The Council can still be invoked but will have less context to work with.

Options:
1. **Convene anyway** — proceed to Step 3
2. **Cancel** — stop

## Step 3: Brief the user on what's about to happen

Tell the user:

> The Mini Council is about to convene. Five voices will critique your current state in sequence:
>
> 1. **💼 Seed VC** — financial and traction skepticism (2026-AI-era pre-seed lens)
> 2. **💔 Churned Customer** — post-purchase regret; would I have stayed?
> 3. **⚔️ Competitor Founder** — where I'd attack you; what I'd copy or dismiss
> 4. **⏳ Future-Self (12 months from now)** — regret-driven temporal hindsight
> 5. **📋 Grumpy PM** — operational reality; what gets dropped on Tuesday
>
> Each voice operates in isolation. They do not share context with each other or with Gandalf. Each will end with one of three verdicts: **Pass** (would not advance), **Pass for now** (advance once condition met), or **In play** (clear to advance). The Council does not vote — you read all five verdicts and decide.

Use `AskUserQuestion` to confirm proceeding:

> Ready to convene? The full Council takes 5–15 minutes depending on how much you push back.

Options:
1. **Yes — convene the full Council** — proceed to Step 4
2. **Convene only one voice** — useful when you want a quick pressure-test (proceed to Step 4 with the user's chosen single voice)
3. **Cancel** — stop

If "only one voice" — ask which voice in a follow-up `AskUserQuestion`.

## Step 4: Invoke each voice in turn

Per the Mini Council Conventions in each voice's SKILL.md, every voice receives **the same context**:

- Builder Profile (full)
- Vertical Stack draft (if Step 2 has begun)
- Theme Map (if Step 3 has begun)
- Expert Framework (if Step 4 is complete)
- Competitor Map (if Step 5 is complete)
- Whether this is a Step 1→2 or Step 4→5 invocation
- The current `attempt` number from frontmatter

Each voice does **not** receive:

- The user's conversation transcripts (context isolation)
- Notes from Gandalf
- Animal advisor feedback
- **The other Council voices' responses** — each voice critiques in isolation

Invoke each voice in this order (unless the user picked a single voice):

1. **Seed VC** — load `${CLAUDE_PLUGIN_ROOT}/skills/seed-vc-agent/SKILL.md`. Adopt the full Seed VC identity. Conduct the appropriate Core Skill (Vertical Stack interrogation for Step 1→2; pre-seed deck pressure-test for Step 4→5). Conclude with the Council verdict format. Display in full.
2. **Churned Customer** — load `${CLAUDE_PLUGIN_ROOT}/skills/churned-customer-agent/SKILL.md`. Adopt full identity. Onboarding-promise audit (Step 1→2) or value-decay pressure-test (Step 4→5). Verdict.
3. **Competitor Founder** — load `${CLAUDE_PLUGIN_ROOT}/skills/competitor-founder-agent/SKILL.md`. Where-I'd-attack-you analysis (Step 1→2) or distribution-vs-product gap test (Step 4→5). Verdict.
4. **Future-Self** — load `${CLAUDE_PLUGIN_ROOT}/skills/future-self-agent/SKILL.md`. Twelve-month regret enumeration (Step 1→2) or trough-month-four pressure-test (Step 4→5). Verdict.
5. **Grumpy PM** — load `${CLAUDE_PLUGIN_ROOT}/skills/grumpy-pm-agent/SKILL.md`. Realistic-timeline interrogation (Step 1→2) or team-resilience pressure-test (Step 4→5). Verdict.

Between voices, give the user a brief beat ("Next: ⚔️ Competitor Founder.") but do **not** summarise or interpret. Each voice speaks for itself.

## Step 5: Aggregate the verdicts

After all five voices have spoken (or after the single chosen voice has spoken), display an aggregated summary:

```
## Council verdicts

| Voice | Verdict | Headline finding |
|---|---|---|
| 💼 Seed VC | {Pass | Pass for now | In play} | {one-line summary of their finding} |
| 💔 Churned Customer | {verdict} | {one-line} |
| ⚔️ Competitor Founder | {verdict} | {one-line} |
| ⏳ Future-Self | {verdict} | {one-line} |
| 📋 Grumpy PM | {verdict} | {one-line} |
```

Then state plainly:

- Number of **Pass** verdicts (advance is risky)
- Number of **Pass for now** verdicts (specific conditions to address)
- Number of **In play** verdicts (clear to advance)

Do **not** weight or vote. Do **not** soften the language. Present the data as-is.

## Step 6: Append Council outcome to sprint state

Append a Progress Log entry to `.sprint/sprint.md`:

```
- **Progress** — Mini Council convened ({invocation context}); verdicts: {N} Pass, {N} Pass-for-now, {N} In-play ({date})
```

## Step 7: Offer next-step options

Use `AskUserQuestion` to present the user with their options. Tailor to the verdict pattern:

**If most verdicts are Pass (≥3 of 5):**

The Council strongly recommends loopback or significant revision before advancing.

1. **Loopback** — reset to Step 1 retaining Builder Profile + Theme Map + Expert Framework; clear Vertical Stack onward (use `/sprint-loopback`)
2. **Address the highest-priority gap** — pick one Council voice's finding and work on it before re-convening
3. **Pause and reflect** — return later via `/sprint-continue`

**If verdicts are mixed (mostly Pass-for-now):**

The Council identified specific conditions to address before advancing.

1. **Address the named conditions** — work the conditions, then re-convene the Council
2. **Proceed anyway, accepting the residual risk** — advance to next step (Step 2 via `/sprint-step-2`, or Step 5 via `/sprint-step-5` if at the Step 4→5 transition) understanding the conditions are unmet
3. **Pause** — return later via `/sprint-continue`

**If most verdicts are In play (≥3 of 5):**

The Council clears the user to advance.

1. **Proceed to next step** — Step 2 (Vertical Stack) or Step 5 (Competitor Map), depending on invocation context
2. **Address the residual risks the Council named** — optional polish before advancing
3. **Pause** — return later

In all cases, never reference slash commands in user-facing text. Use natural language ("loopback to Discovery", "advance to Vertical Stack", "address the Seed VC's evidence gap") and trigger the appropriate command behind the scenes.

---

## Injected Context

The following files contain essential context for this command. **Before completing Step 4, use the Read tool to load every file listed in this section.** Read them in parallel.

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Seed VC skill: !`echo ${CLAUDE_PLUGIN_ROOT}/skills/seed-vc-agent/SKILL.md`
- Churned Customer skill: !`echo ${CLAUDE_PLUGIN_ROOT}/skills/churned-customer-agent/SKILL.md`
- Competitor Founder skill: !`echo ${CLAUDE_PLUGIN_ROOT}/skills/competitor-founder-agent/SKILL.md`
- Future-Self skill: !`echo ${CLAUDE_PLUGIN_ROOT}/skills/future-self-agent/SKILL.md`
- Grumpy PM skill: !`echo ${CLAUDE_PLUGIN_ROOT}/skills/grumpy-pm-agent/SKILL.md`
- Mini Council format spec (SPEC-004-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-004-A-Mini-Council-Skill-Format.md`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Concept document (anti-sycophancy posture, §6): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
