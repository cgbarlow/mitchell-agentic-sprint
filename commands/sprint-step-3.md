---
description: Step 3 of the Mitchell Agentic Sprint — Buyer Interviews. Generate a behavioural-only interview script (Mom Test linted), log interviews, build a theme map, detect saturation. The heaviest step; concept §4.3.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Step 3 — Buyer Interviews

The heaviest step. The output is a validated problem statement, a theme map of buyer pain, a list of buyers who took costly action (the warmest leads in the world for the eventual product launch), and a clear go/no-go decision.

The rule from concept §4.3: *interview script bans hypothetical questions ("would you use a tool that does X"). It only asks about past behaviour ("walk me through the last time you ran into this problem"). It looks for costly action: have they spent money, hired someone, built a workaround, complained loudly. Stated problems are cheap. Revealed problems are signal.*

## Step 1: Verify state and gate

Use the Glob tool to check `.sprint/sprint.md` exists.

**If it does not exist:**

> No active sprint. Run `/sprint-start` to begin.

Stop.

**If it exists:** read `.sprint/sprint.md`. Parse frontmatter; read `last_approved_step`.

**If `last_approved_step < 2`:** apply the friendly-error pattern from SPEC-007-A:

```
Step 3 (Buyer Interviews) is gated on Step 2 (Vertical Stack) approval.

Current sprint state:
- Step: {state.step}
- Last approved step: {state.last_approved_step}
- Attempt: {state.attempt}

To advance to Step 3, complete Step 2 first.
```

Use `AskUserQuestion` to offer:
1. Run Step 2 now
2. Cancel

Stop.

**If `last_approved_step >= 2`:** proceed.

## Step 2: Determine sub-flow

Read `.sprint/sprint.md` Interview Log section and check whether `.sprint/interviews/` directory has existing interview files.

Use `AskUserQuestion` to route the user:

> **Step 3 — Buyer Interviews.** Where are you?

Options:

1. **Starting fresh — generate the interview script and outreach plan** (sub-flow A; required first time)
2. **Log a new interview** (sub-flow B; available after sub-flow A)
3. **Update the theme map across all interviews** (sub-flow C; available after at least one interview is logged)
4. **Check saturation** (sub-flow D; available after at least 3 interviews are logged)
5. **Conclude Step 3** (sub-flow E; advance to Step 4 — only available when at least one of Theme Map or Costly-Action Signals is non-empty)

If the user picks an option whose precondition is not met, surface that and ask again.

---

## Sub-flow A: Generate the interview script and outreach plan

The output of this sub-flow is:

- A **target list** of 15–30 named buyers in the user's chosen vertical (the user provides the names; you help them structure the list)
- A **Sales Navigator filter spec** the user can paste in
- **5 communities** where the buyer hangs out (forums, Slack/Discord groups, conferences, paid newsletters)
- A **cold-outreach message** template (≤120 words; behaviour-anchored)
- A **behavioural interview script** (8–12 questions; Mom Test discipline enforced via the linter)

### A.1: Invoke Gandalf for outreach plan

Adopt the full Gandalf identity from the campaign-mode plugin. Provide context:

> **Sprint context:** Mitchell Agentic Sprint, Step 3 (Buyer Interviews), sub-flow A.
>
> **Vertical Stack from Step 2 (full):** {paste the user's Vertical Stack section verbatim}
>
> **Builder Profile from Step 1 (full):** {paste the Builder Profile section verbatim}
>
> **Goal:** Help the user produce: target list, Sales Navigator filter, 5 communities, cold-outreach message, interview script.
>
> **Anti-sycophancy posture (concept §6):** Refuse vague answers. If the user says "I'll use my LinkedIn", ask which 30 names. If the user says "founders", ask company size and stage. The point is to surface the names *now*, not after they've spent two weeks "thinking about it".
>
> **Behavioural-only interview script:** This is the most important deliverable. The script must consist of 8–12 questions, every one of which asks about past behaviour. Banned phrasings include "would you", "do you think", "if you had", "how much would you pay", "would it be useful". Allowed phrasings include "walk me through the last time", "what do you currently do when", "what did you spend on… last quarter", "have you ever paid for…", "tell me about the workaround you built", "who else have you talked to about this".

After Gandalf produces a draft script, **run the linter** on each generated question.

### A.2: Run the linter

Use Bash to write the draft script to a temp file, then invoke the linter:

```bash
PYTHONPATH=${CLAUDE_PLUGIN_ROOT} python -m helpers.interview_validator /tmp/sprint-script-draft.txt
```

The linter exits 0 if clean, 1 if violations, 2 if invalid input.

**If clean (exit 0):** proceed to A.3.

**If violations (exit 1):** display the linter output to the user, then loop:

> The interview-script generator produced the following violations. The script will be regenerated. (You can override individual rulings if you have a specific reason — e.g., a phrase is procedural rather than hypothetical.)
>
> {linter output}

Use `AskUserQuestion`:

1. **Regenerate the violating questions only** (Recommended — Gandalf re-asks the script with the linter findings as feedback)
2. **Override one or more violations** (specify which; the question survives unchanged)
3. **Cancel sub-flow A** (return to Step 2 dispatcher)

For "regenerate", invoke Gandalf again with the linter output as feedback and re-run the linter. Repeat at most 3 times before surfacing manual review to the user.

### A.3: Persist the outreach plan and script

Use Edit to append to `.sprint/sprint.md` Interview Log section:

```markdown
### Outreach plan (locked {today's date})

#### Target list
{15-30 named buyers, table of name / role / company / connection path}

#### Sales Navigator filter
{filter spec block}

#### Communities
1. {community 1 — link, why this fits}
2. ...

#### Cold-outreach message template
> {≤120 word message, behaviour-anchored}

#### Interview script (linter-clean)
1. {question 1}
2. {question 2}
...
```

Append to Progress Log:

```
- **Progress** — Step 3 outreach plan + script locked ({today's date})
```

### A.4: Brief the user on sub-flow B

> Outreach plan is in `.sprint/sprint.md`. Send the cold-outreach message to your target list this week. As interviews happen, log each one with sub-flow B (or run `/sprint-step-3` again and pick "Log a new interview").
>
> The Sprint stops when **three consecutive interviews surface no new themes**, not at an arbitrary number. You will know when to stop because sub-flow D (saturation check) tells you.

---

## Sub-flow B: Log a new interview

### B.1: Capture the interview metadata

Use `AskUserQuestion` (one at a time):

1. **Pseudonym for the interviewee** (e.g., `dental-ap-manager-1`) — used as filename suffix
2. **Date of interview** (today's date defaults if user just says "today")
3. **Length in minutes**
4. **Did the buyer take costly action on this problem?** (paid for a workaround / hired someone / built something / complained publicly) — yes/no/unclear
5. **If yes, what was the costly action?** (free-text)

### B.2: Capture the transcript

Tell the user:

> Paste the interview transcript or summary below. Verbatim quotes are best — concept §6 makes "verbatim only" a headline rule. Don't paraphrase. If the buyer used a colourful phrase, keep it exactly.

Use Read or Bash to receive the transcript content from the user.

### B.3: Extract themes

Read the transcript. Extract 3–8 theme tags per interview. Tags are kebab-case noun phrases that describe a recurring buyer concern, e.g., `pricing-friction`, `manual-reconciliation`, `audit-paranoia`, `vendor-fatigue`, `onboarding-pain`.

Use `AskUserQuestion` to confirm the extracted themes (so the user has agency over the labels):

> **Proposed theme tags for this interview:**
>
> - {tag 1}
> - {tag 2}
> - {tag 3}
>
> Edit?

Options:
1. Accept as-is
2. Revise (user provides edits)

### B.4: Persist the interview file

Use Bash to ensure `.sprint/interviews/` exists, then use Write to create the interview file:

```bash
mkdir -p .sprint/interviews
```

Path: `.sprint/interviews/{NN}-{pseudonym}.md` where `{NN}` is the next two-digit interview number.

Content:

```markdown
---
interviewee-pseudonym: {pseudonym}
date: {date}
length-minutes: {length}
themes: [{tag1}, {tag2}, ...]
costly-action: {yes|no|unclear}
costly-action-detail: "{detail or empty}"
---

# Interview {NN}: {pseudonym}

{verbatim transcript or summary}
```

### B.5: Update Interview Log table

Use Edit to append to `.sprint/sprint.md` Interview Log section a row in a markdown table:

```markdown
| # | Pseudonym | Date | Length | Costly action? | Themes |
|---|---|---|---|---|---|
| {NN} | {pseudonym} | {date} | {length}min | {yes/no} | {themes joined by comma} |
```

If a Costly-Action Signal applies (`yes`), also append to the Costly-Action Signals subsection:

```markdown
- **{pseudonym}** ({date}) — {costly-action-detail}
```

### B.6: Append progress log

```
- **Progress** — Interview {NN} ({pseudonym}) logged; themes: {tags} ({date})
```

### B.7: Surface next steps

Use `AskUserQuestion`:

1. **Log another interview** (loop back to B.1)
2. **Update the theme map** (sub-flow C)
3. **Check saturation** (sub-flow D — only meaningful at ≥3 interviews)
4. **Pause**

---

## Sub-flow C: Update the theme map

### C.1: Aggregate themes across all interview files

Use Glob and Read to enumerate `.sprint/interviews/*.md`. For each file, parse the frontmatter `themes` list. Aggregate counts.

### C.2: Render the Theme Map

Use Edit to overwrite the Theme Map subsection of `.sprint/sprint.md` Interview Log with a sorted-by-frequency table:

```markdown
| Theme | Interviews | Buyers (pseudonyms) |
|---|---|---|
| pricing-friction | 7 | dental-ap-manager-1, ... |
| manual-reconciliation | 5 | ... |
| ... | | |
```

Themes appearing in 3+ interviews are bold; these are saturation candidates.

### C.3: Append progress log

```
- **Progress** — Theme map updated; {N} unique themes across {M} interviews ({today's date})
```

### C.4: Surface next steps — same options as B.7.

---

## Sub-flow D: Check saturation

### D.1: Build the JSON input

Use Glob to enumerate `.sprint/interviews/*.md` in alphabetical order (filename prefixes are zero-padded so this is interview order). For each, parse the frontmatter `themes` list.

Construct a JSON array of arrays:

```json
[
  ["pricing-friction", "manual-reconciliation"],
  ["pricing-friction", "vendor-fatigue"],
  ...
]
```

Write to a temp file: `/tmp/sprint-themes.json`.

### D.2: Run the saturation helper

```bash
PYTHONPATH=${CLAUDE_PLUGIN_ROOT} python -m helpers.saturation --human /tmp/sprint-themes.json
```

Display the human-readable output to the user.

### D.3: Decide

Use `AskUserQuestion`:

> {saturation output}

If the helper reports **saturated**:

1. **Conclude Step 3** (advance to sub-flow E)
2. **Run a few more interviews anyway** (loop back to B.1; user's call)
3. **Pause**

If the helper reports **not saturated**:

1. **Log another interview** (loop back to B.1)
2. **Pause**
3. **Conclude Step 3 anyway, accepting the under-saturation** (advance to sub-flow E with explicit acknowledgement; logs a Progress Log entry recording the choice)

---

## Sub-flow E: Conclude Step 3

### E.1: Verify required artifacts

Per SPEC-007-A Step 3 requires Interview Log with ≥3 interviews and a non-empty Theme Map. Check both. If either is missing, do not approve — tell the user what's missing and route them back to B or C.

### E.2: Surface the go/no-go question

Use `AskUserQuestion`:

> **Step 3 close-out.** What does the evidence say?

Options:

1. **Go — proceed to Step 4 (Framework)** — there are recurring themes with costly-action signals; the vertical is validated
2. **Loopback** — no costly-action signals or themes did not converge; reset Vertical Stack and try a different ICP / vertical / workflow per concept §7
3. **Pause** — sit with the evidence

If "Loopback", trigger `/sprint-loopback`.

### E.3: Approve Step 3 and advance

If "Go": update frontmatter via Edit:
- `step: 4`
- `last_approved_step: 3`

Append progress log:

```
- **Progress** — Step 3 (Buyer Interviews) complete; {N} interviews, {M} themes, {K} costly-action signals; Go ({today's date})
```

### E.4: Brief the user on Step 4

> Step 3 complete. Theme Map and Costly-Action Signals are locked.
>
> Step 4 (Framework) finds the named expert in your vertical, studies their work in depth, and adapts their framework to your specific ICP and workflow. The Mini Council can pressure-test the close-out before you advance — recommended given the cost of getting Step 4's expert choice wrong.

Use `AskUserQuestion`:

1. **Convene the Mini Council** to pressure-test the validated thesis (Recommended; sub-flow A→C of `/sprint-council` becomes Step 4→5 framing)
2. **Proceed directly to Step 4** (use `/sprint-step-4`, available from Phase 4)
3. **Pause** — return later via `/sprint-continue`

Never reference slash commands in user-facing text — use natural language.

---

## Injected Context

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Step gate spec (SPEC-007-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-007-A-Step-Gate-Commands.md`
- Anti-sycophancy spec (SPEC-008-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-008-A-Anti-Sycophancy.md`
- Interview validator: !`echo ${CLAUDE_PLUGIN_ROOT}/helpers/interview_validator.py`
- Saturation helper: !`echo ${CLAUDE_PLUGIN_ROOT}/helpers/saturation.py`
- Concept document (Step 3 detail, §4.3): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
