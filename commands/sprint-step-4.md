---
description: Step 4 of the Mitchell Agentic Sprint — Framework. Find the named expert in the user's vertical, synthesise their framework, and produce a "3 to keep verbatim / 3 to adapt" plan plus a 2-week reading/watching list. Concept §4.4.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Step 4 — Framework

Concept §4.4: instead of inventing your own framework, find the named expert in your vertical, study their work in depth, and adapt their framework to your specific ICP and workflow.

This step uses NotebookLM when the bolt-on is configured (recommended — `nlm` provides source-grounded synthesis with citations across the expert's books, courses, and interviews). Without the bolt-on, Step 4 falls back to Claude-only synthesis from user-pasted excerpts.

## Step 1: Verify state and gate

Use Glob to check `.sprint/sprint.md`. **If missing:** tell the user to run `/sprint-start` and stop.

Read `.sprint/sprint.md` and parse frontmatter. Read `last_approved_step`.

**If `last_approved_step < 3`:** apply the friendly-error pattern from SPEC-007-A:

```
Step 4 (Framework) is gated on Step 3 (Buyer Interviews) approval.

Current sprint state:
- Step: {state.step}
- Last approved step: {state.last_approved_step}
- Attempt: {state.attempt}

To advance to Step 4, complete Step 3 first.
```

Use `AskUserQuestion`:
1. Run Step 3 now
2. Cancel

Stop.

## Step 2: Detect NotebookLM availability

Read `.sprint/setup.md` if it exists. Look for `notebooklm-mcp: available | unavailable | declined` in frontmatter.

Also check the `MAS_NOTEBOOKLM_MCP` environment variable. If set to a truthy value (`1`, `true`, `yes`, `on`), treat as available even if `setup.md` says otherwise (the user may have configured after running setup).

**If neither signal indicates available:**

Tell the user:

> NotebookLM MCP is not configured. Step 4 can run in Claude-only synthesis mode — you'll paste expert excerpts and Claude synthesises directly.
>
> If you'd rather configure NotebookLM first (recommended for source-grounded citations), run `/sprint-setup` and come back. Otherwise, continue.

Use `AskUserQuestion`:
1. Continue in Claude-only mode
2. Pause to run `/sprint-setup` first

If "pause", stop.

## Step 3: Determine sub-flow

Read the current state's Expert Framework section. Use `AskUserQuestion`:

> **Step 4 — Framework.** Where are you?

Options:

1. **Generate candidate experts** (sub-flow A; required first time — produces a ranked list of 5 candidates)
2. **Pick an expert and start synthesis** (sub-flow B; available after sub-flow A produces candidates)
3. **Add or update expert sources** (sub-flow C; available after an expert is picked)
4. **Run the framework synthesis** (sub-flow D; available after sources are added)
5. **Build the reading/watching list** (sub-flow E; available after synthesis is complete)
6. **Conclude Step 4** (sub-flow F; advance to Step 5)

If a precondition is unmet, surface that and ask again.

---

## Sub-flow A: generate candidate experts

The output is 5 candidate experts in the user's vertical, ranked by fit, each with evidence on the four criteria from concept §4.4.

### A.1: Invoke Gandalf for candidate generation

Adopt the full Gandalf identity from the campaign-mode plugin. Provide context:

> **Sprint context:** Mitchell Agentic Sprint, Step 4 (Framework), sub-flow A.
>
> **Vertical Stack from Step 2 (full):** {paste verbatim}
>
> **Theme Map from Step 3 (full):** {paste verbatim}
>
> **Costly-Action Signals from Step 3 (full):** {paste verbatim}
>
> **Goal:** Produce 5 candidate experts whose framework could be adopted and adapted for the user's ICP and workflow.
>
> **Eligibility criteria** (each candidate must meet all four):
> 1. **Real commercial track record** — revenue from operating in this space, not just content. Cite the company / product / role.
> 2. **A published book or course** that captures their framework in depth.
> 3. **Multiple long-form interviews** (podcasts, YouTube, conference talks) where they articulate the framework.
> 4. **A paid product the user can study** — their own SaaS / consulting / book sold for >$50.
>
> **Anti-sycophancy posture (concept §6):** Do not propose experts whose claim to expertise is "they have a Twitter following" or "they wrote a popular article". The bar is *commercial operator who has done the work*. If you cannot find five candidates who meet the bar, return four — do not pad.

Gandalf produces the ranked list with one paragraph per candidate covering the four criteria.

### A.2: Persist the candidates

Use Edit to append to `.sprint/sprint.md` Expert Framework section:

```markdown
### Candidate experts (generated {today's date})

1. **{Name}** — {one-paragraph evidence covering all four criteria}. Source: {primary work + URL or citation}.
2. **{Name}** — ...
3. **{Name}** — ...
4. **{Name}** — ...
5. **{Name}** — ...

(If fewer than 5 candidates met the bar, the list ends with: "Only {N} candidates met the bar. Do not pad.")
```

Append a Progress Log entry:

```
- **Progress** — Step 4 candidate experts generated ({N} candidates) ({today's date})
```

### A.3: Surface next sub-flow

Use `AskUserQuestion`:

1. **Pick one of these candidates** (sub-flow B)
2. **Re-generate** (something is off about the list — tell Gandalf what to change)
3. **Pause** — return later via `/sprint-continue`

---

## Sub-flow B: pick an expert

Use `AskUserQuestion` listing the candidates by name. The user picks one.

Append to `.sprint/sprint.md` Expert Framework section:

```markdown
### Chosen expert (locked {today's date})

**{Name}**

Why this expert (one paragraph from the candidate evidence): {paste from sub-flow A}.
```

Append a Progress Log entry:

```
- **Progress** — Step 4 expert chosen: {Name} ({today's date})
```

Surface next sub-flow:

1. **Add expert source documents** (sub-flow C)
2. **Pause**

---

## Sub-flow C: add expert source documents

The user provides URLs or pastes excerpts from the expert's:
- Book(s) — table of contents + key chapter excerpts
- Course landing page + curriculum
- 2–3 long-form interviews (podcast transcripts or YouTube transcripts)
- Their paid product's positioning page (if applicable)

### C.1: Detect path

If NotebookLM MCP is available (per Step 2 detection): the sources are added to the user's NotebookLM notebook.

If unavailable: the user pastes excerpts directly into the chat for Claude to synthesise from.

### C.2: NotebookLM path

If a notebook for this sprint already exists (the Artifacts section of `.sprint/sprint.md` has a `NotebookLM ID` entry), reuse it. Otherwise, invoke the `notebook_create` MCP tool with name `MAS Sprint — {sprint date} — attempt {N}` and record the returned ID under Artifacts.

For each source the user provides:
- Invoke the `source_add` MCP tool with the URL (or pasted text)
- Record the source name + type + date added in `.sprint/sprint.md` Expert Framework subsection:

```markdown
### Sources (NotebookLM-backed)

- **{Source title}** ({type: book / course / interview / product page}, added {date}) — {URL or "pasted excerpt"}
```

### C.3: Claude-only fallback path

Tell the user:

> NotebookLM is not configured. Paste source excerpts directly here. For each source, include:
>
> - Title and type (book / course / interview / product page)
> - Source URL (for citation)
> - The relevant excerpt — chapter outline, full transcript, or key passages
>
> The synthesis quality depends on what you paste. Verbatim transcripts beat paraphrases; chapter outlines beat summaries.

Read each pasted excerpt. Record under Expert Framework → Sources subsection (same shape as C.2 but with "(Claude-only)" annotation).

### C.4: Surface next sub-flow

Use `AskUserQuestion`:
1. **Add another source** (loop back to C)
2. **Run the framework synthesis** (sub-flow D — needs at least 2 sources of differing types)
3. **Pause**

---

## Sub-flow D: run the framework synthesis

### D.1: Build the synthesis prompt

Use Bash to invoke the prompt builder:

```bash
PYTHONPATH=${CLAUDE_PLUGIN_ROOT} python -c "
from helpers.notebooklm import build_framework_synthesis_prompt
print(build_framework_synthesis_prompt(
    expert_name='{expert name}',
    icp_summary='{ICP from Vertical Stack}',
    workflow_summary='{Workflow from Vertical Stack}',
))
"
```

Capture the prompt output.

### D.2a: NotebookLM path

If available, invoke the `notebook_query` MCP tool with the prompt and the notebook ID. Capture the response.

### D.2b: Claude-only fallback

Run the prompt directly through Claude with the pasted source excerpts in scope. Same output structure expected.

### D.3: Persist the framework synthesis

Append to `.sprint/sprint.md` Expert Framework section:

```markdown
### Framework synthesis (locked {today's date})

#### Summary

{Three to five core principles in plain language with verbatim quote citations}

#### Keep verbatim (3)

1. **{principle name}** — Why it applies directly: {one sentence}. Source: {citation}.
2. **{principle name}** — ...
3. **{principle name}** — ...

#### Adapt (3)

1. **{principle name}** — Original: "{verbatim from source}". Adaptation: {specific change}. Source: {citation}.
2. ...
3. ...

#### Cannot map

{Either "No principles failed to map." OR a list with one-sentence reasons each.}
```

Append a Progress Log entry:

```
- **Progress** — Step 4 framework synthesis complete ({today's date})
```

### D.4: Surface next sub-flow

Use `AskUserQuestion`:
1. **Build the reading/watching list** (sub-flow E)
2. **Re-run synthesis** (the keep/adapt split feels wrong — Gandalf re-asks)
3. **Pause**

---

## Sub-flow E: build the reading/watching list

The user gets a 2-week reading and watching list. Concept §4.4: *what the user gets is a chosen expert, a clear adaptation plan, and a reading and watching list to consume in the next two weeks.*

Adopt Gandalf identity. Provide context (expert name, framework synthesis, ICP, workflow). Ask Gandalf to produce a sequenced list:

- Week 1: 2–3 highest-priority items (foundational chapters, the most-cited interview, the keystone case study)
- Week 2: 3–5 deepening items (less-foundational chapters, supplementary interviews, application examples)

Each item: title, type, link/citation, time estimate, one-sentence reason it's on the list.

Append to `.sprint/sprint.md` Expert Framework:

```markdown
### Reading & watching list (2 weeks)

#### Week 1 — Foundations
- [ ] {item} ({type}) — {time estimate} — {one-sentence reason}. {citation}
- [ ] ...

#### Week 2 — Deepening
- [ ] {item} ({type}) — {time estimate} — {one-sentence reason}. {citation}
- [ ] ...
```

Surface next:
1. **Conclude Step 4** (sub-flow F)
2. **Pause**

---

## Sub-flow F: conclude Step 4

### F.1: Verify required artifacts

Per SPEC-007-A Step 4 requires Expert Framework section non-empty (chosen expert + adaptation plan). Confirm:
- Chosen expert subsection populated
- Framework synthesis subsection populated with both keep-verbatim and adapt entries

If either is missing, do not approve. Tell the user what's missing and route them back to D.

### F.2: Approve Step 4

Update frontmatter via Edit:
- `step: 5`
- `last_approved_step: 4`

Append progress log:

```
- **Progress** — Step 4 (Framework) complete; expert: {Name}; reading/watching list scheduled ({today's date})
```

### F.3: Surface options

Use `AskUserQuestion`:

> **Step 4 complete.** Expert framework locked, reading/watching list scheduled.
>
> The Mini Council fires meaningfully again at the Step 4→5 transition. Recommended before advancing — Step 5's positioning whitespace work depends heavily on whether the chosen framework actually fits the ICP.

Options:

1. **Convene the Mini Council** to pressure-test the framework choice (Recommended; use `/sprint-council`)
2. **Proceed to Step 5 (Competitor)** — competitor analysis + positioning whitespace (use `/sprint-step-5`, ships in Phase 5)
3. **Loopback** — if the synthesis surfaced that the framework doesn't fit (use `/sprint-loopback`)
4. **Pause** — return later via `/sprint-continue`

Never reference slash commands in user-facing text — use natural language.

---

## Injected Context

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Step gate spec (SPEC-007-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-007-A-Step-Gate-Commands.md`
- NotebookLM integration spec (SPEC-006-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-006-A-NotebookLM-MCP.md`
- NotebookLM helper: !`echo ${CLAUDE_PLUGIN_ROOT}/helpers/notebooklm.py`
- Concept document (Step 4 detail, §4.4): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
