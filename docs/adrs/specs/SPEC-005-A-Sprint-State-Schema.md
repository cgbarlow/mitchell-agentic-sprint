# SPEC-005-A: `.sprint/sprint.md` State Schema

| Field | Value |
|-------|-------|
| **Specification ID** | SPEC-005-A |
| **Parent ADR** | [ADR-005](../ADR-005-Sprint-State-Schema.md) |
| **Version** | 1.0 |
| **Status** | Active |
| **Last Updated** | 2026-05-08 |

---

## Overview

Defines the on-disk format of `.sprint/sprint.md` (per-project sprint state) and the semantics of the per-section content. Read and write helpers live at `helpers/sprint_state.py`.

## File location

`.sprint/sprint.md` — created by `/sprint-setup` in the user's project root. The `.sprint/` directory is gitignored at user level.

## Frontmatter

```yaml
---
schema-version: 1
sprint-mode: Solo | Coached
step: 1                  # the step the user is currently on (1-6)
last_approved_step: 0    # highest step number whose gate has been passed; gates Step N+1
attempt: 1               # increments on loopback
created: 2026-05-08
---
```

Field rules:

- `schema-version` is reserved for future migration; v0.1.0 always emits `1`
- `sprint-mode` selects framing: `Solo` (default; user works alone) or `Coached` (Scott or another coach reviews artifacts asynchronously)
- `step` is 1–6
- `last_approved_step` is 0–6; Step N+1 commands refuse to run when `last_approved_step < N`
- `attempt` increments by 1 each time `/sprint-loopback` is invoked
- `created` is set on first write and never changed

## Section structure

```markdown
## Builder Profile

<written in Step 1; persists across all attempts>

## Vertical Stack

<written in Step 2; cleared and re-written on loopback>

### Backup Verticals

## Interview Log

<written in Step 3; transcripts live at .sprint/interviews/>

### Theme Map

### Costly-Action Signals

## Expert Framework

<written in Step 4; persists across attempts>

## Competitor Map

<written in Step 5; cleared on loopback>

### Positioning Whitespace

## Artifacts

### Sales Deck
<path to artifact>

### Outreach Plan
<path to artifact>

### Investor Deck
<path to artifact>

## Loopback Log

<each loopback adds an entry: attempt N, vertical disqualified, reason>

## Progress Log

<reused from campaign-mode convention; appended to silently by agents at meaningful milestones>
```

## Loopback semantics

When `/sprint-loopback` runs:

| Section | Behaviour |
|---|---|
| Builder Profile | **Retained** |
| Vertical Stack | **Cleared** |
| Backup Verticals | **Retained** (the user's prior backup options become input to the next attempt) |
| Interview Log | **Retained** but tagged with the disqualified vertical for traceability |
| Theme Map | **Retained** (themes are vertical-agnostic enough to be reused) |
| Costly-Action Signals | **Retained** (warmest leads stay warm) |
| Expert Framework | **Retained** |
| Competitor Map | **Cleared** |
| Positioning Whitespace | **Cleared** |
| Artifacts | **Cleared** |
| Loopback Log | **Appended** with attempt number, disqualified vertical, reason |
| Progress Log | **Appended** with the loopback event |

After loopback: `step` resets to `2` (Vertical), `last_approved_step` resets to `1`, `attempt` increments.

## Helper API

`helpers/sprint_state.py` exposes:

- `read_state(path: Path) -> SprintState` — parse the file; raise on schema violation
- `write_state(state: SprintState, path: Path) -> None` — atomic write (write to temp, rename)
- `set_step(state, step: int) -> None` — validate transition; raise if illegal
- `approve_step(state, step: int) -> None` — sets `last_approved_step` to `max(current, step)`
- `loopback(state) -> None` — applies the table above
- `append_progress_log(state, message: str) -> None` — append a Progress Log entry
- `append_loopback_log(state, vertical: str, reason: str) -> None`

Each helper has unit tests in `tests/test_sprint_state.py` per Protocol 3.

## Acceptance criteria

- A round-trip read/write preserves all fields and content
- Gate enforcement: `set_step(state, N)` raises when `last_approved_step < N - 1`
- Loopback retains the sections marked Retained above; clears the Cleared sections
- Atomic writes survive process kill mid-write (temp + rename pattern)
