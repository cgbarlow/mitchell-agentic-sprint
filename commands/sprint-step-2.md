---
description: Step 2 of the Mitchell Agentic Sprint — Vertical Stack. Narrow the user's idea to a defensible vertical x sub-vertical x ICP x specific workflow x AI leverage point. Gated on Step 1 approval.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Step 2 — Vertical Stack

The first job of the Sprint is to force focus. Step 2 produces a single Vertical Stack the user can defend in writing, with two backup options if the primary fails. The rule from concept §4.2: "I am the best at X" only works if X is narrow enough to actually be true.

## Step 1: Verify state and gate

Use the Glob tool to check `.sprint/sprint.md` exists.

**If it does not exist:**

> No active sprint. Run `/sprint-start` to begin a new Sprint.

Stop.

**If it exists:** read `.sprint/sprint.md` and parse frontmatter. Read `last_approved_step`.

**If `last_approved_step < 1`:**

Tell the user (friendly-error pattern per SPEC-007-A):

```
Step 2 (Vertical Stack) is gated on Step 1 (Discovery) approval.

Current sprint state:
- Step: {state.step}
- Last approved step: {state.last_approved_step}
- Attempt: {state.attempt}

To advance to Step 2, complete Step 1 first.
```

Use `AskUserQuestion` to offer:
1. **Run Step 1 now** — invoke `/sprint-start` to complete Discovery
2. **Cancel**

Stop.

**If `last_approved_step >= 1`:** proceed to Step 2.

## Step 2: Brief the user

Tell the user:

> **Step 2 — Vertical Stack.**
>
> The output of this step is a single Vertical Stack you can defend in writing, with two backup options. The Stack has five layers, each progressively narrower:
>
> 1. **Vertical** — the industry or domain (e.g., "B2B fintech")
> 2. **Sub-vertical** — the specific slice (e.g., "payments operations")
> 3. **ICP** — the named buyer profile (e.g., "AP managers in mid-market companies, 200–2000 employees")
> 4. **Specific workflow** — the job-to-be-done (e.g., "weekly invoice reconciliation between ERP and bank statements")
> 5. **AI leverage point** — where AI does the differentiated work (e.g., "fuzzy matching invoices to bank entries with audit trail")
>
> Vague stacks fail Step 3 (buyer interviews). Sharp stacks survive them. Gandalf will guide the narrowing and refuse to flatter generic answers.

## Step 3: Invoke Gandalf for Vertical Stack work

Adopt the full Gandalf identity from the campaign-mode plugin. Conduct the Step 2 narrowing.

Provide Gandalf with:

> **Sprint context:** Mitchell Agentic Sprint, Step 2 (Vertical Stack). Sprint mode: {sprint-mode from frontmatter}. Attempt {N} of {N}.
>
> **Step 1 output (Builder Profile):** {full Builder Profile section from sprint.md}
>
> **Step 2 goal:** Produce one Vertical Stack the user can defend in writing, plus two backup options. The Stack has the five layers above.
>
> **Required questions** (Gandalf adapts wording but covers all):
>
> 1. From your Builder Profile, which 1–3 verticals do you have unfair access to? Pick the top one.
> 2. Within that vertical, which sub-vertical do you have the most specific knowledge of? (Reject "all of fintech" — force narrowing.)
> 3. Who specifically inside that sub-vertical buys? Job title, company size, geography. Don't say "founders". Say "founders of mid-market HR-tech companies, 50–200 employees, US-based".
> 4. What workflow does that buyer hate the most? Walk me through their week and find the recurring time-suck.
> 5. Where does AI do differentiated work in that workflow — not "AI-powered scheduling" but "AI that resolves the specific edge case of [X] which currently takes the buyer Y hours per week"?
>
> **Anti-sycophancy posture (concept §6):** Refuse vague answers. Force specificity. If the user says "B2B SaaS founders", ask which segment, which company size, which buying motion. If the user can't narrow, that itself is the finding — they don't yet know who they're building for.
>
> **Backup verticals:** Once the primary Vertical Stack is locked, ask: "If this vertical fails Step 3 buyer interviews, what are the two adjacent verticals where your unfair advantages still apply?" Write these as a ranked list in the Backup Verticals section.
>
> **Output:**
> - Vertical Stack section: written-out 5-layer stack, each layer with a one-sentence rationale
> - Backup Verticals section: 2 ranked alternatives with brief why-this-fits notes

Gandalf works with the user iteratively. Use Edit to write the resulting Vertical Stack and Backup Verticals into `.sprint/sprint.md` under the appropriate H2 headings.

## Step 4: Verify and approve

After Gandalf concludes, re-read `.sprint/sprint.md` and verify:

- The Vertical Stack section is non-empty and has all five layers
- The Backup Verticals section has at least 2 alternatives

If either is missing, do **not** approve the step. Tell the user what's missing and offer to continue working with Gandalf.

If both are present, update the frontmatter via Edit:

- `step: 2` (already there if not, set it)
- `last_approved_step: 2`

Then append a Progress Log entry:

```
- **Progress** — Step 2 (Vertical Stack) complete; locked vertical + 2 backup options ({today's date in ISO format})
```

## Step 5: Offer next-step options

Use `AskUserQuestion`:

> **Step 2 complete.** Vertical Stack written to `.sprint/sprint.md`.
>
> The Mini Council can pressure-test your Vertical Stack before you commit ~30 buyer interviews to it. The Step 1→2 transition is one of two points where the Council fires meaningfully (the other is Step 4→5).

Options:

1. **Convene the Mini Council** — pressure-test the Vertical Stack across five skeptical voices (Recommended; use `/sprint-council`)
2. **Proceed to Step 3** — start buyer interview script generation (use `/sprint-step-3`, available from Phase 3)
3. **Loopback** — if the Step 2 work surfaced something fundamental, reset to Step 1 retaining your profile and themes (use `/sprint-loopback`)
4. **Pause** — return later via `/sprint-continue`

Never reference slash commands in user-facing text — use natural language ("convene the Council", "advance to buyer interviews", "loopback to Discovery").

---

## Injected Context

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Step gate spec (SPEC-007-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-007-A-Step-Gate-Commands.md`
- Concept document: !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
