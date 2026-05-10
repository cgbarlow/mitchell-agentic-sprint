---
description: Start a Mitchell Agentic Sprint. Auto-runs first-time setup if needed, then begins Step 1 (Discovery). The single entry point — users never need to remember /sprint-setup separately.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Start Sprint

You are beginning a new Mitchell Agentic Sprint for the user. The Sprint walks the user through six sequential steps to take one of their many ideas and prove out whether it can become a real business. **Output is artifacts, not product.** The Sprint is adversarial-by-default — your job is to refuse flattery and force the user to cite a person, a number, or an artifact for every claim.

Follow these steps in order.

## Step 1: Run first-time setup if needed (auto)

Use the Glob tool to check whether `.sprint/setup.md` exists in the user's project root.

**If `.sprint/setup.md` does NOT exist:**

This is the user's first run in this project. Tell them briefly:

> First-time setup running — this is a one-time pre-flight per project. Verifying prerequisites, optionally installing the 🧢 Mitchell profile, and offering the NotebookLM MCP bolt-on.

Now read `${CLAUDE_PLUGIN_ROOT}/commands/sprint-setup.md` and execute its **Step 1 through Step 5** (Verify prerequisites → Install Mitchell profile → Choose NotebookLM path → Onboard NotebookLM → Record setup decisions). The user goes through the AskUserQuestion prompts in those steps as normal.

**Skip sprint-setup's Step 6** (the "Start a Sprint now / Done — exit setup" confirmation) — we're already starting a Sprint, so the confirmation is redundant. After Step 5 writes `.sprint/setup.md`, return here and proceed to Step 2 below.

**If sprint-setup's Step 1 stops early** (because campaign-mode or six-animals is missing), stop here too. The user must install the prerequisite plugins before the Sprint can begin.

**If `.sprint/setup.md` already exists:** the user has done setup previously. Skip directly to Step 2 below. (If they want to re-configure — install the Mitchell profile after declining, or onboard NotebookLM after the fact — they can run `/sprint-setup` separately.)

## Step 2: Check for active sprint

Use the Glob tool to check if `.sprint/sprint.md` exists in the user's project root.

**If `.sprint/sprint.md` exists:**

Read the file. Note the current `step`, `last_approved_step`, and `attempt` from the frontmatter. Use `AskUserQuestion` to offer:

1. **Continue the active sprint** — pick up where you left off (use `/sprint-continue`)
2. **Start fresh** — archive the existing sprint to `.sprint/archive/{YYYY-MM-DD}-sprint.md` and proceed to Step 3 below
3. **Cancel** — make no changes

Include current state in the question field so the user has context (e.g., "You have an active sprint: step {N}, attempt {N}, last approved step {N}. What would you like to do?").

If the user chooses "Start fresh", use Bash to `mkdir -p .sprint/archive` and `mv .sprint/sprint.md .sprint/archive/$(date +%Y-%m-%d)-sprint.md` before proceeding.

**If `.sprint/sprint.md` does not exist:** proceed directly to Step 3.

## Step 3: Choose Sprint Mode

Use `AskUserQuestion`:

> **Sprint Mode**
>
> The Sprint runs in one of two modes. Solo means you work the sprint alone; AI advisors guide you through each step. Coached means you have an external coach (Scott Mitchell or someone else) reviewing your artifacts asynchronously between steps.

Options:
1. **Solo** — work the sprint alone with AI advisors only
2. **Coached** — external coach reviews your artifacts between steps

## Step 4: Initialise sprint state

Use Bash to create the sprint state directory:

```
mkdir -p .sprint
```

Then use the Write tool to create `.sprint/sprint.md` with this initial content (substituting `{MODE}` with the user's chosen mode and `{TODAY}` with today's date in ISO format):

```markdown
---
schema-version: 1
sprint-mode: {MODE}
step: 1
last_approved_step: 0
attempt: 1
created: {TODAY}
---

## Builder Profile

## Vertical Stack

## Backup Verticals

## Interview Log

## Theme Map

## Costly-Action Signals

## Expert Framework

## Competitor Map

## Positioning Whitespace

## Artifacts

## Loopback Log

## Progress Log
```

## Step 5: Step 1 of the Sprint — Discovery (invoke Gandalf)

You will now run the Discovery step. Adopt the full Gandalf identity from the campaign-mode plugin and conduct the Step 1 interview.

Invoke `gandalf-agent` via the Skill tool. Provide the following context to Gandalf:

> **Sprint context:** Mitchell Agentic Sprint, Step 1 (Discovery). Sprint mode: {MODE}. This is attempt 1 of 1.
>
> **Step 1 goal:** Produce a sharp written profile of the user, including their unfair advantages and a list of verticals where they have unfair access (and a list of verticals they should avoid).
>
> **Required questions** (Gandalf adapts wording but covers all):
> 1. What's your background — products shipped, domains worked in, customer types served?
> 2. What unfair advantages do you have — relationships, domain knowledge, brand, distribution, capital, time?
> 3. What's your time and money runway in months?
> 4. What's the rough idea, if any? (One sentence.)
> 5. What do you already know about who'd buy it — named buyers, prior conversations, costly actions you've witnessed?
>
> **Anti-sycophancy posture (concept §6):** Refuse flattery. Push back on vague answers. Force specificity. If the user says "I have a strong network", ask for the names. If they say "tons of demand", ask which buyer paid for the workaround.
>
> **Output (write to `.sprint/sprint.md` Builder Profile section):** A sharp written profile in the user's own words, including (a) their unfair advantages with specific evidence, (b) a list of 3–5 verticals where they have unfair access, ranked, and (c) a short list of verticals they should avoid (and why).

After Gandalf concludes Step 1, append a Progress Log entry to `.sprint/sprint.md`:

```
- **Progress** — Step 1 (Discovery) completed; Builder Profile written ({TODAY})
```

## Step 6: Offer next-step options

Use `AskUserQuestion` to present the user with their options now that Step 1 is complete:

> **Step 1 complete.** Builder Profile written to `.sprint/sprint.md`.
>
> Before advancing to Step 2 (Vertical Stack), the Mini Council can pressure-test your Builder Profile. The Mini Council exists because builders' thinking gets laundered through models that won't tell them no. The Council voices refuse flattery and force specificity.

Options:

1. **Convene the Mini Council** — invoke `/sprint-council` to have the Seed VC pressure-test your profile and proposed vertical direction (Recommended)
2. **Proceed directly to Step 2** — skip Council and start Vertical Stack work (the Council can be invoked later)
3. **Pause here** — return later via `/sprint-continue`

---

## Injected Context

The following files contain essential context for this command. Their absolute paths are resolved below. **Before completing Step 5, use the Read tool to load every file listed in this section.** Read them in parallel if possible.

If any path below is empty or shows an error, the plugin root could not be resolved. Inform the user that the plugin install may be incomplete.

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Setup command (Step 1 reads this when first-time setup is needed): !`echo ${CLAUDE_PLUGIN_ROOT}/commands/sprint-setup.md`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Concept document: !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
