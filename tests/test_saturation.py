"""Tests for helpers/saturation.py — see SPEC-008-A and concept §4.3, §6.

Saturation rule: "the user keeps going until the last three interviews surface
no new themes." Tests cover the rule, threshold customisation, and the CLI.

Per Protocol 8: no mocks. Tests use real synthetic theme sequences and real
subprocess invocation for the CLI.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from helpers.saturation import SaturationStatus, check_saturation


# ---------- core logic ----------


def test_empty_input_not_saturated():
    s = check_saturation([])
    assert s.saturated is False
    assert s.total_interviews == 0
    assert s.consecutive_no_new == 0


def test_single_interview_not_saturated():
    s = check_saturation([{"pricing-friction"}])
    assert s.saturated is False
    assert s.total_interviews == 1


def test_two_interviews_with_threshold_three_not_saturated():
    s = check_saturation([{"a"}, {"b"}], threshold=3)
    assert s.saturated is False


def test_all_new_themes_each_interview_not_saturated():
    seq = [{"a"}, {"b"}, {"c"}, {"d"}, {"e"}]
    s = check_saturation(seq, threshold=3)
    assert s.saturated is False
    assert s.consecutive_no_new == 0


def test_last_three_no_new_themes_saturated():
    """Three consecutive interviews surface no new themes → saturated."""
    seq = [
        {"a", "b"},     # interview 1: 2 new
        {"a", "c"},     # interview 2: 1 new (c)
        {"a", "b"},     # interview 3: 0 new — start of streak
        {"b", "c"},     # interview 4: 0 new
        {"a"},          # interview 5: 0 new
    ]
    s = check_saturation(seq, threshold=3)
    assert s.saturated is True
    assert s.consecutive_no_new == 3


def test_streak_resets_when_new_theme_appears():
    seq = [
        {"a", "b"},     # 2 new
        {"a"},          # 0 new
        {"b"},          # 0 new — streak of 2
        {"c"},          # 1 new — resets to 0
        {"a"},          # 0 new — streak of 1 again
    ]
    s = check_saturation(seq, threshold=3)
    assert s.saturated is False
    assert s.consecutive_no_new == 1


def test_empty_set_counts_as_zero_new_themes():
    seq = [{"a"}, set(), set(), set()]
    s = check_saturation(seq, threshold=3)
    assert s.saturated is True
    assert s.consecutive_no_new == 3


def test_reintroduced_theme_does_not_count_as_new():
    """A theme that was seen earlier, then absent, then back — is NOT new on reintroduction."""
    seq = [
        {"a"},      # 1 new
        {"b"},      # 1 new
        {"a"},      # 0 new (a was seen before)
        {"b"},      # 0 new
        {"a"},      # 0 new — streak = 3
    ]
    s = check_saturation(seq, threshold=3)
    assert s.saturated is True
    assert s.consecutive_no_new == 3


def test_threshold_customisation():
    seq = [{"a"}, {"a"}, {"a"}]  # only 1st interview adds a theme; 2 more no-new → streak 2
    s = check_saturation(seq, threshold=2)
    assert s.saturated is True
    assert s.consecutive_no_new == 2


def test_threshold_must_be_positive():
    with pytest.raises(ValueError):
        check_saturation([{"a"}], threshold=0)


def test_threshold_one_fires_immediately_after_no_new():
    """With threshold=1, a single no-new-themes interview triggers."""
    seq = [{"a"}, {"a"}]
    s = check_saturation(seq, threshold=1)
    assert s.saturated is True
    assert s.consecutive_no_new == 1


def test_list_of_lists_accepted_as_input():
    """API accepts list[list[str]] (e.g. parsed JSON) as well as list[set[str]]."""
    seq = [["a", "a"], ["a"], ["a"], ["a"]]  # duplicates within an interview ignored
    s = check_saturation(seq, threshold=3)
    assert s.saturated is True


def test_new_themes_per_interview_recorded():
    seq = [{"a", "b"}, {"a"}, {"c"}, {"c"}]
    s = check_saturation(seq, threshold=3)
    assert s.new_themes_per_interview == (2, 0, 1, 0)


# ---------- CLI ----------


def _run_cli(args: list[str], *, stdin: str | None = None) -> subprocess.CompletedProcess:
    project_root = Path(__file__).resolve().parent.parent
    return subprocess.run(
        [sys.executable, "-m", "helpers.saturation", *args],
        input=stdin,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(project_root), "PATH": "/usr/bin:/bin:/usr/local/bin"},
        cwd=project_root,
    )


def test_cli_emits_json_by_default(tmp_path: Path):
    f = tmp_path / "themes.json"
    f.write_text(json.dumps([["a", "b"], ["a"], ["a"], ["a"]]))
    r = _run_cli([str(f)])
    assert r.returncode == 0, r.stderr
    payload = json.loads(r.stdout)
    assert payload["saturated"] is True
    assert payload["consecutive_no_new"] == 3
    assert payload["total_interviews"] == 4


def test_cli_human_flag_prints_human_readable(tmp_path: Path):
    f = tmp_path / "themes.json"
    f.write_text(json.dumps([["a"], ["a"], ["a"]]))
    r = _run_cli(["--human", str(f)])
    assert r.returncode == 0
    assert "Saturated" in r.stdout
    assert "Total interviews" in r.stdout


def test_cli_threshold_flag(tmp_path: Path):
    f = tmp_path / "themes.json"
    f.write_text(json.dumps([["a"], ["a"]]))
    # Default threshold 3 → not saturated
    r1 = _run_cli([str(f)])
    assert json.loads(r1.stdout)["saturated"] is False
    # threshold 1 → saturated
    r2 = _run_cli(["--threshold", "1", str(f)])
    assert json.loads(r2.stdout)["saturated"] is True


def test_cli_reads_stdin_when_no_path():
    r = _run_cli([], stdin=json.dumps([["a"], ["a"], ["a"], ["a"]]))
    assert r.returncode == 0
    assert json.loads(r.stdout)["saturated"] is True


def test_cli_invalid_json_exits_two(tmp_path: Path):
    f = tmp_path / "themes.json"
    f.write_text("not json at all")
    r = _run_cli([str(f)])
    assert r.returncode == 2


def test_cli_missing_file_exits_two():
    r = _run_cli(["/no/such/path/themes.json"])
    assert r.returncode == 2
