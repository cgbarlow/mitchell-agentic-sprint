---
description: Step 5 of the Mitchell Agentic Sprint — Competitor and positioning whitespace. Cluster competitors, identify the gap nobody owns, draft a positioning statement the user can defend in three sentences. Concept §4.5.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Step 5 — Competitor and Positioning Whitespace

Concept §4.5: cluster the top competitors, synthesise with the interview themes (Step 3) and the expert framework (Step 4), and produce a positioning whitespace map. The output of this step is what the user takes into Step 6's deck work — they brief their AI builder against this positioning, not against a vague feature list.

This step uses NotebookLM when the bolt-on is configured. Without it, Step 5 falls back to Claude-only synthesis from user-pasted excerpts.

## Step 1: Verify state and gate

Use Glob to check `.sprint/sprint.md`. **If missing:** tell the user to run `/sprint-start` and stop.

Read `.sprint/sprint.md`; parse frontmatter; read `last_approved_step`.

**If `last_approved_step < 4`:** apply the friendly-error pattern from SPEC-007-A:

```
Step 5 (Competitor + Positioning) is gated on Step 4 (Framework) approval.

Current sprint state:
- Step: {state.step}
- Last approved step: {state.last_approved_step}
- Attempt: {state.attempt}

To advance to Step 5, complete Step 4 first.
```

Use `AskUserQuestion`:
1. Run Step 4 now
2. Cancel

Stop.

## Step 2: Detect NotebookLM availability

Same detection logic as `/sprint-step-4`: read `.sprint/setup.md` if present, fall back to checking `MAS_NOTEBOOKLM_MCP` env var. If both signals are absent, run in Claude-only fallback mode (no blocking — the Sprint always completes).

## Step 3: Determine sub-flow

Read the current state's Competitor Map and Positioning Whitespace sections. Use `AskUserQuestion`:

> **Step 5 — Competitor and positioning whitespace.** Where are you?

Options:

1. **Compile the competitor list** (sub-flow A; required first time — 5–10 competitors with their URLs)
2. **Add or update competitor sources** (sub-flow B; available after sub-flow A)
3. **Run the whitespace synthesis** (sub-flow C; available after at least 5 competitor sources are added)
4. **Lock the positioning statement** (sub-flow D; available after sub-flow C)
5. **Conclude Step 5** (sub-flow E; advance to Step 6)

If a precondition is unmet, surface that and ask again.

---

## Sub-flow A: compile the competitor list

The output is 5–10 named competitors in the user's vertical, each with a primary URL (landing page or pricing page) the synthesis layer will study.

Adopt Gandalf identity. Provide context (Vertical Stack, Theme Map, Expert Framework). Ask Gandalf to surface the 5–10 strongest competitors. Criteria: actively operating in this vertical, addressing the same buyer pain (or adjacent), with a public landing or pricing page the user can study.

Persist to `.sprint/sprint.md` Competitor Map section:

```markdown
### Competitor list (compiled {today's date})

| # | Competitor | URL | Why this fits |
|---|---|---|---|
| 1 | {name} | {url} | {one-line — buyer overlap or pain overlap} |
| 2 | ... | ... | ... |
```

Append to Progress Log:

```
- **Progress** — Step 5 competitor list compiled ({N} competitors) ({today's date})
```

Surface next sub-flow:
1. **Add competitor sources** (sub-flow B)
2. **Re-generate** (Gandalf re-asks)
3. **Pause**

---

## Sub-flow B: add competitor sources

For each competitor in the list, the user adds source material the synthesis layer will study — landing pages, pricing pages, case studies, founder interviews, comparison pages.

### B.1: NotebookLM path (if MCP available)

Reuse the existing notebook for this sprint (recorded under `.sprint/sprint.md` Artifacts → NotebookLM ID). For each source:
- Invoke `source_add` MCP tool with URL
- Record source name + competitor name + date added in Competitor Map → Sources subsection

### B.2: Claude-only fallback path

Tell the user:

> NotebookLM is not configured. Paste the most relevant excerpts from each competitor's site directly. For each source:
>
> - Competitor name + source type (landing page / pricing page / case study)
> - URL (for citation)
> - The excerpt — at minimum: hero headline, value prop, pricing if visible, one customer quote if shown

Read each pasted excerpt. Record under Competitor Map → Sources subsection.

### B.3: Surface next sub-flow

Use `AskUserQuestion`:
1. **Add another competitor's sources** (loop back to B)
2. **Run the whitespace synthesis** (sub-flow C — needs at least 5 competitors with sources added)
3. **Pause**

---

## Sub-flow C: run the whitespace synthesis

### C.1: Build the synthesis prompt

Use Bash to invoke the prompt builder:

```bash
PYTHONPATH=${CLAUDE_PLUGIN_ROOT} python -c "
from helpers.notebooklm import build_whitespace_prompt
print(build_whitespace_prompt(
    competitors={competitor_names_list},
    theme_map_summary={theme_map_one_paragraph_summary},
    framework_summary={expert_framework_one_paragraph_summary},
))
"
```

Capture the prompt.

### C.2: NotebookLM path

If available, invoke `notebook_query` with the prompt and the notebook ID. Capture the response.

### C.3: Claude-only fallback

Run the prompt directly through Claude with the pasted competitor excerpts in scope.

### C.4: Persist the whitespace synthesis

Append to `.sprint/sprint.md` Competitor Map and Positioning Whitespace sections:

```markdown
## Competitor Map

### Sources

(table of competitors + URLs + excerpts/source-IDs from sub-flow B)

### Cluster {N}: {dominant message}

- Members: {competitor names}
- Verbatim positioning quotes:
  - "{quote}" — {competitor}
  - "{quote}" — {competitor}
- What this cluster does well: {sentence}
- What this cluster avoids: {sentence}

(repeat per cluster — 2–4 clusters)

## Positioning Whitespace

### Gap 1: {gap name}

- Buyer theme it serves: {theme tag, recurrence count}
- No competitor cluster lands here
- Verbatim phrasing the user could own: "{phrase}"

(repeat per gap — usually 1–3)
```

If the synthesis surfaces *no genuine whitespace*, write that finding plainly under Positioning Whitespace:

```markdown
## Positioning Whitespace

**No genuine whitespace surfaced.** Every positioning angle the buyers care about is occupied by an existing competitor cluster. This is a signal — see "Conclude Step 5" for next-step options.
```

Append to Progress Log:

```
- **Progress** — Step 5 whitespace synthesis complete; {N} competitor clusters, {M} positioning gaps ({today's date})
```

### C.5: Surface next sub-flow

Use `AskUserQuestion`:
1. **Lock a positioning statement** (sub-flow D)
2. **Re-run synthesis** (the cluster map feels off — Gandalf re-asks)
3. **Pause**

---

## Sub-flow D: lock the positioning statement

Adopt Gandalf identity. Provide context (Theme Map, Framework synthesis, Competitor Map, Positioning Whitespace). Ask Gandalf to draft three candidate positioning statements anchored to the strongest gap. Each candidate must:

1. Connect to a recurring theme from the buyer interviews (cite the theme tag)
2. Draw on the expert framework (cite the principle)
3. Not overlap substantively with any competitor cluster (cite the verbatim language no competitor uses)
4. Be defendable in three sentences

Display the three candidates. Use `AskUserQuestion` to pick one (or "none, regenerate", or "draft a fourth myself").

Once a statement is locked, persist:

```markdown
## Positioning Whitespace

### Locked positioning statement ({today's date})

> {three-sentence positioning statement}

**Theme connection:** {theme tag, recurrence}
**Framework connection:** {principle from expert framework}
**Whitespace anchor:** "{verbatim language that no competitor cluster uses}"
```

Append to Progress Log:

```
- **Progress** — Step 5 positioning statement locked ({today's date})
```

---

## Sub-flow E: conclude Step 5

### E.1: Verify required artifacts

Per SPEC-007-A Step 5 requires Competitor Map non-empty and Positioning Whitespace non-empty. Confirm both. If either is missing, do not approve. Tell the user what's missing.

If the Positioning Whitespace section reports "No genuine whitespace surfaced", surface this as a decision point — *not* an automatic block. Use `AskUserQuestion`:

> **The synthesis surfaced no genuine whitespace.** Every angle the buyers care about is owned by an existing competitor cluster. This is a real signal that the vertical is saturated for the chosen ICP / workflow / framework.

Options:

1. **Loopback** — reset to Step 2 retaining Builder Profile + themes + framework; try a different ICP / workflow (use `/sprint-loopback`)
2. **Proceed anyway** — accept the saturation finding; advance to Step 6 with a positioning statement that's a sharper-execution-of-existing-cluster, not a whitespace play (the user explicitly acknowledges)
3. **Pause** — sit with the evidence

If "proceed anyway", append to Progress Log:

```
- **Progress** — Step 5 concluded without whitespace; user acknowledged saturation, proceeding to Step 6 ({today's date})
```

### E.2: Approve Step 5

If artifacts are present and the user is advancing, update frontmatter via Edit:
- `step: 6`
- `last_approved_step: 5`

Append to Progress Log:

```
- **Progress** — Step 5 (Competitor + Positioning) complete; {N} clusters, {locked positioning statement summary} ({today's date})
```

### E.3: Surface options

Use `AskUserQuestion`:

> **Step 5 complete.** Competitor Map and Positioning Whitespace locked.
>
> Step 6 is the synthesis step — three artefacts ready to take into customer conversations and pre-seed pitches.

Options:

1. **Proceed to Step 6 (Synthesis)** — generate sales deck, outreach plan, investor deck (use `/sprint-step-6`)
2. **Pause** — return later via `/sprint-continue`

Never reference slash commands in user-facing text.

---

## Injected Context

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Step gate spec (SPEC-007-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-007-A-Step-Gate-Commands.md`
- NotebookLM integration spec (SPEC-006-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-006-A-NotebookLM-MCP.md`
- NotebookLM helper: !`echo ${CLAUDE_PLUGIN_ROOT}/helpers/notebooklm.py`
- Concept document (Step 5 detail, §4.5): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
