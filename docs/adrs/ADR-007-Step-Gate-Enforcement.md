# ADR-007: Per-Step Command Gate Enforcement Using `last_approved_step`

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-007 |
| **Initiative** | Step sequence enforcement |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-08 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** the concept's strict 6-step linear pipeline (Discovery → Vertical → Buyer Interviews → Framework → Competitor → Synthesis) where each step's output is the input to the next, and the gap analysis identifying that campaign-mode trusts the user to advance phases sensibly with no enforcement,

**facing** the choice between hard gates (commands refuse to enter step N when step N-1 is not complete), soft gates (commands warn but allow advancement), and trust-the-user (no gate at all),

**we decided for** hard gates implemented via `last_approved_step` in `.sprint/sprint.md` frontmatter, where step commands check `last_approved_step >= N - 1` before allowing entry and raise a friendly error if the gate is not met, with `approve_step(state, N)` called by step commands themselves once the step's required artifact is present (Council remains pressure-test, not gatekeeper),

**and neglected** Council-as-gatekeeper (couples advancement to the user choosing to convene Council; users may legitimately skip Council and advance), Guardian-style separate gate command (over-engineered for v0.1.0 — adds another command to the surface area), and trust-the-user (defeats the concept's "force focus" first job — concept §3),

**to achieve** non-bypassable step ordering that matches the concept's linear pipeline, automatic advancement that doesn't require users to remember a separate "approve" command, and clean separation between advisory (Council) and gating (state-mutation),

**accepting that** users can manually edit `.sprint/sprint.md` to bump `last_approved_step` and bypass the gate (acceptable — they're consciously making that choice; the gate exists to prevent accidental skip, not malicious bypass), and that step commands are responsible for both writing the artifact and approving the step (single-responsibility violation that's acceptable for v0.1.0 simplicity).

---

## Options Considered

| Option | Verdict |
|---|---|
| **Hard gates via `last_approved_step` (Selected)** | Non-bypassable; clean state model; auto-approves on artifact completion |
| Council-as-gatekeeper | Rejected — couples advancement to Council; users may skip Council |
| Separate `/sprint-approve-step` command | Rejected — over-engineered for v0.1.0 |
| Trust the user (no gate) | Rejected — defeats "force focus" |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Depends On | ADR-005 | Sprint state schema | `last_approved_step` lives in the schema |
| Implements | ADR-002 | Build tier | Moderate-tier sequence enforcement |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| SPEC-007-A | Step Gate Commands | [specs/SPEC-007-A-Step-Gate-Commands.md](./specs/SPEC-007-A-Step-Gate-Commands.md) |
| Helper | `helpers/sprint_state.set_step` and `approve_step` | [../../helpers/sprint_state.py](../../helpers/sprint_state.py) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-08 |
