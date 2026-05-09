# SPEC-007-A: Step Gate Commands

| Field | Value |
|-------|-------|
| **Specification ID** | SPEC-007-A |
| **Parent ADR** | [ADR-007](../ADR-007-Step-Gate-Enforcement.md) |
| **Version** | 1.0 |
| **Status** | Active |
| **Last Updated** | 2026-05-08 |

---

## Overview

Defines the gate-checking and gate-approval semantics that every `/sprint-step-N` command must implement, plus the friendly-error pattern for blocked entry and the approval ritual when artifacts are present.

## Gate semantics

| Step N | Required `last_approved_step` to enter | Required artifact section(s) before approval |
|---|---|---|
| 1 (Discovery) | 0 (always allowed; first step) | Builder Profile non-empty |
| 2 (Vertical) | 1 | Vertical Stack non-empty |
| 3 (Buyer Interviews) | 2 | Interview Log has ≥3 interviews; Theme Map non-empty |
| 4 (Framework) | 3 | Expert Framework non-empty (chosen expert + adaptation plan) |
| 5 (Competitor) | 4 | Competitor Map non-empty; Positioning Whitespace non-empty |
| 6 (Synthesis) | 5 | Artifacts section has at least one of Sales Deck / Outreach Plan / Investor Deck path populated |

## Command flow

Every `/sprint-step-N` command (where N ≥ 2) implements this flow:

1. **Verify state file exists** — Glob check on `.sprint/sprint.md`. If missing, tell the user to run `/sprint-start` and stop.
2. **Read state** — load via `helpers.sprint_state.read_state` (or its CLI equivalent if invoked from Bash).
3. **Check gate** — call `helpers.sprint_state.set_step(state, N)`. If `GateError` is raised:
   - Tell the user (in friendly natural language) which step is required first
   - Offer to invoke that step's command
   - Stop
4. **Run the step** — invoke Gandalf or the appropriate Sprint workflow for step N
5. **Write the artifact** — append to the relevant section(s) of `.sprint/sprint.md` via Edit
6. **Verify required artifacts** — read state again; check the "Required artifact section(s)" column above for step N
7. **Approve the step** — call `helpers.sprint_state.approve_step(state, N)` and write state back
8. **Append Progress Log entry** — `- **Progress** — Step N ({Step Name}) complete; {artifact summary} ({date})`
9. **Offer next-step options via AskUserQuestion** — Council pressure-test, advance to step N+1, or pause

## Friendly-error pattern

When the gate is not met, do **not** show a stack trace. Show a structured response:

```
Step {N} ({Step Name}) is gated on Step {N-1} ({Prior Step Name}) approval.

Current sprint state:
- Step: {state.step}
- Last approved step: {state.last_approved_step}
- Attempt: {state.attempt}

To advance to Step {N}, you need to complete Step {N-1} first.
```

Then offer via `AskUserQuestion`:
1. Run Step {N-1} now
2. Continue from current step (use `/sprint-continue`)
3. Cancel

## Approval ritual

A step is "approved" when:
1. The step command has run to completion
2. All required artifact sections for that step are non-empty
3. `approve_step(state, N)` has been called and state written back

Approval is **automatic** on successful step completion. Users do not need to remember a separate approval action.

If the user wants to revise an artifact after approval (e.g., re-write the Vertical Stack), they:
- Use `/sprint-loopback` (resets to Step 1 retaining Step 1 artifacts; clears Step 2+) for a fundamental redo
- Or simply re-run the step command, which will overwrite the artifact and re-approve

## Override (manual edit)

Users may manually edit `.sprint/sprint.md` to bump `last_approved_step` and bypass the gate. This is supported but unrecommended. Per ADR-007 the gate exists to prevent accidental skip, not malicious bypass.

## Acceptance criteria

This spec is fulfilled when:
- Every `/sprint-step-N` command for N ≥ 2 implements the 9-step command flow above
- `GateError` from `set_step` is caught and translated into the friendly-error pattern (no stack trace surfaces to the user)
- `approve_step` is called automatically on artifact completion
- Manual `last_approved_step` edits are respected on next read (no schema drift detection in v0.1.0)
- `tests/test_sprint_state.py` covers gate semantics for steps 1–6 (already covered for set_step and approve_step in Phase 1)
