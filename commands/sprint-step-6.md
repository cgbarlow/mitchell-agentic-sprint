---
description: Step 6 of the Mitchell Agentic Sprint — Synthesis. Populate the three artefact templates (sales deck, outreach plan, pre-seed investor deck) with the user's evidence from Steps 1–5. Optional NotebookLM audio overview. Concept §4.6.
allowed-tools: [Read, Write, Glob, Bash, Edit, AskUserQuestion]
---

# Step 6 — Synthesis

The final step. The user walks out with three written artefacts they can take into the world: a **sales deck** for customer conversations, a **customer outreach plan** for taking that deck to market, and a **pre-seed investor deck** that satisfies the 2026-AI-era non-negotiables.

Per [ADR-009](../docs/adrs/ADR-009-Markdown-First-Artifacts.md) the artefacts are markdown — slide-per-section structure with speaker notes, populated from `.sprint/sprint.md` state. Slides where evidence is missing are marked `[EVIDENCE MISSING: ...]` rather than padded.

When the NotebookLM bolt-on is configured, an additional **audio overview** artefact is generated — a ~10-minute briefing the user listens to before walking into a real conversation. This is the one Step 6 output without a Claude-only equivalent.

## Step 1: Verify state and gate

Use Glob to check `.sprint/sprint.md`. **If missing:** tell the user to run `/sprint-start` and stop.

Read `.sprint/sprint.md`; parse frontmatter; read `last_approved_step`.

**If `last_approved_step < 5`:** apply the friendly-error pattern from SPEC-007-A:

```
Step 6 (Synthesis) is gated on Step 5 (Competitor + Positioning) approval.

Current sprint state:
- Step: {state.step}
- Last approved step: {state.last_approved_step}
- Attempt: {state.attempt}

To advance to Step 6, complete Step 5 first.
```

Use `AskUserQuestion`:
1. Run Step 5 now
2. Cancel

Stop.

## Step 2: Detect NotebookLM availability

Same detection as Steps 4 and 5: `.sprint/setup.md` + `MAS_NOTEBOOKLM_MCP` env var.

## Step 3: Determine sub-flow

Read the current state's Artifacts section. Use `AskUserQuestion`:

> **Step 6 — Synthesis.** Where are you?

Options:

1. **Generate the sales deck** (sub-flow A; for customer conversations)
2. **Generate the outreach plan** (sub-flow B; depends on Step 3 Costly-Action Signals + Step 5 positioning)
3. **Generate the pre-seed investor deck** (sub-flow C; depends on all of Steps 1–5)
4. **Generate the audio overview** (sub-flow D; only if NotebookLM is configured)
5. **Conclude Step 6** (sub-flow E; complete the Sprint, advance state)

Sub-flows A, B, C can run in any order. Most users do A → B → C. Sub-flow D is optional (NotebookLM-only).

---

## Sub-flow A: generate the sales deck

### A.1: Read the template

Use Read on `${CLAUDE_PLUGIN_ROOT}/docs/templates/sales-deck.md` to load the template.

### A.2: Populate from sprint state

Read `.sprint/sprint.md`. Substitute every `{{...}}` placeholder with the corresponding evidence from state:

- `{{strongest_verbatim_quote}}` — the single most-cited verbatim quote from Theme Map's strongest theme
- `{{interviewee_pseudonym}}` and `{{interview_number}}` — citation metadata
- `{{problem_statement_in_plain_language}}` — derived from the strongest theme + costly-action signals
- `{{N}}`, `{{M}}` — interview recurrence counts from Theme Map
- `{{summary_of_costly_action_signals}}` — top 2–3 from the Costly-Action Signals section
- `{{positioning_whitespace_from_step_5}}` — from Positioning Whitespace section
- `{{theme_1}}`, `{{theme_2}}`, `{{theme_3}}` — top 3 themes by recurrence
- `{{expert_name}}` and `{{framework_focus_area}}` — from Expert Framework
- `{{pricing_landed_in_step_4_or_5}}` — pricing decision
- `{{specific_named_ask}}` — derived from positioning + costly-action signal pattern

For any placeholder where the source evidence is missing, replace with `[EVIDENCE MISSING: {what's needed}]`. **Do not pad.**

### A.3: Write the populated artefact

Use Bash to ensure `.sprint/artifacts/` exists:

```bash
mkdir -p .sprint/artifacts
```

Use Write to create `.sprint/artifacts/sales-deck.md` with the populated template content.

### A.4: Verify and report

Read the populated file. Count `[EVIDENCE MISSING:` markers. Report to the user:

> **Sales deck written to `.sprint/artifacts/sales-deck.md`.**
>
> {N} slides populated. {M} `[EVIDENCE MISSING: ...]` markers remain — fill these in before presenting.

Append to Progress Log:

```
- **Progress** — Step 6 sales deck generated; {M} evidence gaps to resolve ({today's date})
```

Update Artifacts section of `.sprint/sprint.md`:

```markdown
### Sales Deck
- Path: `.sprint/artifacts/sales-deck.md`
- Generated: {date}
- Evidence gaps: {M}
```

Use `AskUserQuestion`:
1. **Generate the next artefact** (B, C, or D)
2. **Pause** — fill in the gaps, return later

---

## Sub-flow B: generate the outreach plan

### B.1: Read the template

Use Read on `${CLAUDE_PLUGIN_ROOT}/docs/templates/outreach-plan.md`.

### B.2: Populate from sprint state

Three sections to populate.

**Section 1 — Re-engagement messages.** For each entry in Costly-Action Signals (or each Interview Log row marked `costly-action: yes`):
- Read the corresponding `.sprint/interviews/{NN}-{pseudonym}.md` file
- Extract the strongest verbatim quote from the transcript
- Populate one re-engagement message section with the buyer's pseudonym, the verbatim quote, the costly-action context, and a templated message anchored to that quote
- One message per costly-action signal; if there are zero, the section reports `[EVIDENCE MISSING: no costly-action signals to re-engage]`

**Section 2 — New-contact target list.** Use Gandalf to draft 15–25 new buyer profiles matching the locked Vertical Stack ICP, the validated theme, and the positioning whitespace. Each entry: handle/profile, where to find them, why they fit, first-touch hook anchored to a Theme Map theme.

**Section 3 — Outreach sequence.** Templated 3-touch cadence per `outreach-plan.md`; substitute `{{validated_theme}}`, `{{strongest_verbatim_quote_from_theme_map}}`, `{{count_of_interviews}}`, `{{ICP_role}}` from state.

### B.3: Write the populated artefact

`mkdir -p .sprint/artifacts && Write to .sprint/artifacts/outreach-plan.md`

### B.4: Verify and report

Same `[EVIDENCE MISSING:` count + Progress Log + Artifacts section update as sub-flow A.

---

## Sub-flow C: generate the pre-seed investor deck

### C.1: Read the template

Use Read on `${CLAUDE_PLUGIN_ROOT}/docs/templates/investor-deck.md`.

### C.2: Populate from sprint state

12 slides + appendix. Substitutions follow the slide order in SPEC-009-A:

- Slide 1 (Problem) — strongest verbatim quote + recurrence count
- Slide 2 (Why now) — `[EVIDENCE MISSING: 2026-AI-era specific reasoning]` if not surfaced earlier; the user must provide the inference-cost / workflow-unlock / regulatory-window argument
- Slide 3 (Solution) — one-paragraph from Vertical Stack AI leverage point
- Slide 4 (Product) — `[EVIDENCE MISSING: working demo]` if no demo link recorded
- Slide 5 (Market) — bottom-up sized from ICP definition + Costly-Action Signals + landed pricing
- Slide 6 (Business model) — pricing + the buyer who paid for the workaround + unit economics
- Slide 7 (Traction) — interview count, costly-action count, theme map summary, LOIs/pilots
- Slide 8 (Competition) — Competitor Map cluster table + the user's whitespace
- Slide 9 (Moat) — workflow lock-in / data flywheel / regulated-vertical access; reject "proprietary AI" — if the user's moat is "proprietary AI", mark `[EVIDENCE MISSING: real moat — proprietary AI is rejected by 2026 investors]`
- Slide 10 (Team) — Builder Profile from Step 1
- Slide 11 (Ask) — `[EVIDENCE MISSING: round size, use of funds, milestones]` if not previously discussed
- Slide 12 (Appendix) — inference economics table, evals plan, buyer-interview tape pointer

### C.3: Run the 2026-AI-era checklist

After populating, scan for the five non-negotiables:

- [ ] Working demo (slide 4)
- [ ] Real moat named (slide 9)
- [ ] Evals plan (appendix)
- [ ] Inference economics with gross margin (appendix)
- [ ] Buyer-interview tape pointer (appendix)

For each item, either confirm it's satisfied or mark `[EVIDENCE MISSING: ...]`. Surface the checklist results to the user.

### C.4: Write the populated artefact

`mkdir -p .sprint/artifacts && Write to .sprint/artifacts/investor-deck.md`

### C.5: Verify and report

Same `[EVIDENCE MISSING:` count + Progress Log + Artifacts section update.

---

## Sub-flow D: generate the audio overview (NotebookLM only)

### D.1: Verify availability

If NotebookLM MCP is not configured, tell the user:

> The audio overview is the one Step 6 artefact that requires the NotebookLM bolt-on — there is no Claude-only equivalent for audio synthesis. Run `/sprint-setup` to configure NotebookLM if you want this artefact, or skip and proceed with the three markdown artefacts.

Stop sub-flow D.

### D.2: Build the audio prompt

```bash
PYTHONPATH=${CLAUDE_PLUGIN_ROOT} python -c "
from helpers.notebooklm import build_audio_overview_prompt
print(build_audio_overview_prompt(
    builder_profile={builder_profile_summary},
    vertical_summary={vertical_stack_summary},
))
"
```

### D.3: Generate via MCP

Invoke the `studio_create` MCP tool with the prompt and the notebook ID. NotebookLM produces the audio overview as an artefact. Use `download_artifact` to save it locally.

`mkdir -p .sprint/artifacts && save to .sprint/artifacts/audio-overview.mp3`

### D.4: Verify and report

> **Audio overview written to `.sprint/artifacts/audio-overview.mp3`.** ~10 minutes; briefing-grade, not entertainment. Listen before walking into your next investor or customer conversation.

Append to Progress Log + Artifacts section.

---

## Sub-flow E: conclude Step 6

### E.1: Verify required artifacts

Per SPEC-007-A Step 6 requires the Artifacts section to have at least one of Sales Deck / Outreach Plan / Investor Deck path populated. Most users will have all three; some may stop after just one.

If none is populated, do not approve. Tell the user that no artefact has been generated yet — route them back to A/B/C.

### E.2: Final report

Surface the v0.1.0 close-out summary:

> **Sprint complete.** Attempt {N} of {M}.
>
> Artefacts:
> - Sales deck: `.sprint/artifacts/sales-deck.md` ({M_sales} evidence gaps to resolve)
> - Outreach plan: `.sprint/artifacts/outreach-plan.md` ({M_outreach} gaps)
> - Investor deck: `.sprint/artifacts/investor-deck.md` ({M_investor} gaps)
> - Audio overview: `.sprint/artifacts/audio-overview.mp3` ({status})
>
> The Sprint trained you to refuse flattery and demand verbatim evidence. The artefacts are now yours. Two outcomes are on the table:
>
> 1. **A buyer ready to pay.** You have the sales deck and the validation evidence behind it. The outreach plan tells you who to talk to and how.
> 2. **A pre-seed conversation that doesn't flinch.** You have the investor deck and the artefacts an investor expects. The 2026-AI-era checklist tells you what's still missing.
>
> The Sprint doesn't decide which you go for. It got you to the point where either is real.

### E.3: Approve Step 6 and advance

Update frontmatter via Edit:
- `step: 6`
- `last_approved_step: 6`

Append to Progress Log:

```
- **Progress** — Step 6 (Synthesis) complete; {N_artifacts} artefact(s) in .sprint/artifacts/; Sprint v{attempt} concluded ({today's date})
```

### E.4: Surface options

Use `AskUserQuestion`:

> **Sprint v{attempt} complete.** Where to next?

Options:

1. **Done — close the Sprint** (no further action; the artefacts and the state are persistent in `.sprint/`)
2. **Run another attempt** — start a new sprint via `/sprint-start` (the previous sprint state archives automatically)
3. **Loopback to a different ICP / vertical** — useful if you've completed a Sprint but the artefacts surfaced gaps that suggest a different vertical (use `/sprint-loopback`)

Never reference slash commands in user-facing text.

---

## Injected Context

- Plugin root: !`echo ${CLAUDE_PLUGIN_ROOT}`
- Sales deck template: !`echo ${CLAUDE_PLUGIN_ROOT}/docs/templates/sales-deck.md`
- Outreach plan template: !`echo ${CLAUDE_PLUGIN_ROOT}/docs/templates/outreach-plan.md`
- Investor deck template: !`echo ${CLAUDE_PLUGIN_ROOT}/docs/templates/investor-deck.md`
- Sprint state schema (SPEC-005-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md`
- Step gate spec (SPEC-007-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-007-A-Step-Gate-Commands.md`
- Artifact templates spec (SPEC-009-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-009-A-Artifact-Templates.md`
- NotebookLM integration spec (SPEC-006-A): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/adrs/specs/SPEC-006-A-NotebookLM-MCP.md`
- NotebookLM helper: !`echo ${CLAUDE_PLUGIN_ROOT}/helpers/notebooklm.py`
- Concept document (Step 6 detail, §4.6): !`echo ${CLAUDE_PLUGIN_ROOT}/docs/concept/concept.md`
