"""Tests for helpers/sprint_state.py — see SPEC-005-A.

Per Protocol 8, tests use real tmpdir fixtures rather than mocks of the file system.
"""

from datetime import date
from pathlib import Path

import pytest

from helpers.sprint_state import (
    CLEARED_ON_LOOPBACK,
    RETAINED_ON_LOOPBACK,
    GateError,
    SchemaError,
    SprintState,
    append_loopback_log,
    append_progress_log,
    approve_step,
    init_state,
    loopback,
    read_state,
    set_step,
    write_state,
)


# ---------- init / round-trip ----------


def test_init_state_defaults():
    s = init_state()
    assert s.schema_version == 1
    assert s.sprint_mode == "Solo"
    assert s.step == 1
    assert s.last_approved_step == 0
    assert s.attempt == 1
    assert s.created == date.today()
    # canonical sections exist as empty strings
    for name in (
        "Builder Profile",
        "Vertical Stack",
        "Backup Verticals",
        "Interview Log",
        "Theme Map",
        "Costly-Action Signals",
        "Expert Framework",
        "Competitor Map",
        "Positioning Whitespace",
        "Artifacts",
        "Loopback Log",
        "Progress Log",
    ):
        assert name in s.sections
        assert s.sections[name] == ""


def test_init_state_coached_mode():
    s = init_state(sprint_mode="Coached")
    assert s.sprint_mode == "Coached"


def test_init_state_rejects_invalid_mode():
    with pytest.raises(SchemaError):
        init_state(sprint_mode="Wibble")


def test_round_trip_preserves_all_fields(tmp_path: Path):
    s = init_state()
    s.sections["Builder Profile"] = "I built three SaaS products."
    s.sections["Progress Log"] = "- **Progress** — kicked off (2026-05-08)"
    p = tmp_path / "sprint.md"
    write_state(s, p)
    s2 = read_state(p)
    assert s2 == s


def test_read_raises_on_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        read_state(tmp_path / "missing.md")


def test_read_raises_on_missing_frontmatter(tmp_path: Path):
    p = tmp_path / "sprint.md"
    p.write_text("## Builder Profile\n\nNo frontmatter here.\n")
    with pytest.raises(SchemaError):
        read_state(p)


def test_read_raises_on_invalid_step_range(tmp_path: Path):
    """Manually craft a file with out-of-range step to verify read-side validation."""
    p = tmp_path / "sprint.md"
    p.write_text(
        "---\n"
        "schema-version: 1\n"
        "sprint-mode: Solo\n"
        "step: 7\n"
        "last_approved_step: 0\n"
        "attempt: 1\n"
        "created: 2026-05-08\n"
        "---\n\n## Builder Profile\n\n"
    )
    with pytest.raises(SchemaError):
        read_state(p)


# ---------- gate enforcement ----------


def test_set_step_allows_advance_when_gate_passed():
    s = init_state()
    s.last_approved_step = 1
    set_step(s, 2)
    assert s.step == 2


def test_set_step_raises_when_gate_not_passed():
    s = init_state()
    s.last_approved_step = 0
    with pytest.raises(GateError):
        set_step(s, 2)


def test_set_step_allows_step_one_with_gate_zero():
    s = init_state()
    set_step(s, 1)
    assert s.step == 1


def test_set_step_rejects_out_of_range():
    s = init_state()
    s.last_approved_step = 6
    with pytest.raises(SchemaError):
        set_step(s, 7)


def test_approve_step_is_monotonic():
    s = init_state()
    approve_step(s, 1)
    assert s.last_approved_step == 1
    approve_step(s, 3)
    assert s.last_approved_step == 3
    approve_step(s, 2)  # going backward must NOT decrease
    assert s.last_approved_step == 3


# ---------- loopback ----------


def test_retained_and_cleared_partition_canonical_sections():
    """The two sets must partition the canonical Step 2-5 + log sections."""
    canonical = {
        "Builder Profile",
        "Vertical Stack",
        "Backup Verticals",
        "Interview Log",
        "Theme Map",
        "Costly-Action Signals",
        "Expert Framework",
        "Competitor Map",
        "Positioning Whitespace",
        "Artifacts",
        "Loopback Log",
        "Progress Log",
    }
    assert RETAINED_ON_LOOPBACK | CLEARED_ON_LOOPBACK == canonical
    assert RETAINED_ON_LOOPBACK & CLEARED_ON_LOOPBACK == set()


def test_loopback_retains_required_sections():
    s = init_state()
    s.last_approved_step = 3
    s.step = 4
    s.sections["Builder Profile"] = "PROFILE"
    s.sections["Theme Map"] = "THEMES"
    s.sections["Expert Framework"] = "EXPERT"
    loopback(s)
    assert s.sections["Builder Profile"] == "PROFILE"
    assert s.sections["Theme Map"] == "THEMES"
    assert s.sections["Expert Framework"] == "EXPERT"


def test_loopback_clears_required_sections():
    s = init_state()
    s.last_approved_step = 5
    s.step = 6
    s.sections["Vertical Stack"] = "OLD VERTICAL"
    s.sections["Competitor Map"] = "OLD COMPETITORS"
    s.sections["Positioning Whitespace"] = "OLD WHITESPACE"
    s.sections["Artifacts"] = "OLD ARTIFACTS"
    loopback(s)
    assert s.sections["Vertical Stack"] == ""
    assert s.sections["Competitor Map"] == ""
    assert s.sections["Positioning Whitespace"] == ""
    assert s.sections["Artifacts"] == ""


def test_loopback_resets_step_and_gate_and_increments_attempt():
    s = init_state()
    s.attempt = 1
    s.step = 5
    s.last_approved_step = 4
    loopback(s)
    assert s.step == 2
    assert s.last_approved_step == 1
    assert s.attempt == 2


def test_loopback_appends_to_loopback_log_when_reason_set_separately():
    """loopback() does not by itself append a log entry — that's append_loopback_log()'s job."""
    s = init_state()
    s.attempt = 1
    s.last_approved_step = 3
    s.step = 4
    append_loopback_log(s, vertical="dental SaaS", reason="no costly-action signals after 18 interviews")
    loopback(s)
    assert "dental SaaS" in s.sections["Loopback Log"]
    assert "no costly-action signals" in s.sections["Loopback Log"]


# ---------- append helpers ----------


def test_append_progress_log_uses_canonical_format():
    s = init_state()
    append_progress_log(s, "kicked off the sprint")
    assert s.sections["Progress Log"].startswith("- **Progress** — kicked off the sprint")
    assert str(date.today()) in s.sections["Progress Log"]


def test_append_progress_log_preserves_prior_entries():
    s = init_state()
    append_progress_log(s, "first")
    append_progress_log(s, "second")
    assert "first" in s.sections["Progress Log"]
    assert "second" in s.sections["Progress Log"]
    # second should follow first chronologically
    assert s.sections["Progress Log"].index("first") < s.sections["Progress Log"].index("second")


def test_append_loopback_log_records_attempt_and_reason():
    s = init_state()
    s.attempt = 2
    append_loopback_log(s, vertical="ag-tech CRM", reason="no buyer access")
    assert "attempt 2" in s.sections["Loopback Log"]
    assert "ag-tech CRM" in s.sections["Loopback Log"]
    assert "no buyer access" in s.sections["Loopback Log"]


# ---------- atomic write ----------


def test_write_is_atomic_no_partial_file_on_overwrite(tmp_path: Path):
    """The write_state implementation must use write-temp-then-rename so that a prior
    valid file is never partially overwritten. We verify by checking that after a
    write, the file is fully readable as a valid SprintState.
    """
    p = tmp_path / "sprint.md"
    s1 = init_state()
    s1.sections["Builder Profile"] = "v1"
    write_state(s1, p)
    s2 = init_state()
    s2.sections["Builder Profile"] = "v2"
    write_state(s2, p)
    # Re-read must succeed and reflect the second write entirely
    loaded = read_state(p)
    assert loaded.sections["Builder Profile"] == "v2"


def test_no_temp_files_left_behind(tmp_path: Path):
    p = tmp_path / "sprint.md"
    s = init_state()
    write_state(s, p)
    write_state(s, p)
    # Only sprint.md should remain — no .tmp files
    leftover = [f.name for f in tmp_path.iterdir() if f.name != "sprint.md"]
    assert leftover == []
