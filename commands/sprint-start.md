---
description: Start a Mitchell Agentic Sprint — six-step validation pipeline that walks an AI-strong builder from rough idea to investor-conversation-ready artifacts
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Start Sprint

You are beginning a new Mitchell Agentic Sprint for the user. The Sprint walks the user through six sequential steps to take one of their many ideas and prove out whether it can become a real business. **Output is artifacts, not product.** The Sprint is adversarial-by-default — your job is to refuse flattery and force the user to cite a person, a number, or an artifact for every claim.

Follow these steps in order.

## Step 1: Check for active sprint

Use the Glob tool to check if `.sprint/sprint.md` exists in the user's project root.

**If `.sprint/sprint.md` exists:**

Read the file. Note the current `step`, `last_approved_step`, and `attempt` from the frontmatter. Use `AskUserQuestion` to offer:

1. **Continue the active sprint** — pick up where you left off (use `/sprint-continue`)
2. **Start fresh** — archive the existing sprint to `.sprint/archive/{YYYY-MM-DD}-sprint.md` and proceed to Step 2 below
3. **Cancel** — make no changes

Include current state in the question field so the user has context (e.g., "You have an active sprint: step {N}, attempt {N}, last approved step {N}. What would you like to do?").

If the user chooses "Start fresh", use Bash to `mkdir -p .sprint/archive` and `mv .sprint/sprint.md .sprint/archive/$(date +%Y-%m-%d)-sprint.md` before proceeding.

**If `.sprint/sprint.md` does not exist:** proceed directly to Step 2.

## Step 2: Choose Sprint Mode

Use `AskUserQuestion`:

> **Sprint Mode**
>
> The Sprint runs in one of two modes. Solo means you work the sprint alone; AI advisors guide you through each step. Coached means you have an external coach (Scott Mitchell or someone else) reviewing your artifacts asynchronously between steps.

Options:
1. **Solo** — work the sprint alone with AI advisors only
2. **Coached** — external coach reviews your artifacts between steps

## Step 3: Initialise sprint state

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

## Step 4: Step 1 — Discovery (invoke Gandalf)

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

## Step 5: Offer next-step options

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

The following files contain essential context for this command. Their absolute paths are resolved below. **Before completing Step 4, use the Read tool to load every file listed in this section.** Read them in parallel if possible.

If any path below is empty or shows an error, the plugin root could not be resolved. Inform the user and suggest running `/sprint-setup` (Phase 4 onwards) to install dependencies.

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Sprint protocols (build-time): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/protocols.md`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Concept document: !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
