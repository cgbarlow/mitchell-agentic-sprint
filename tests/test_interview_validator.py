"""Tests for helpers/interview_validator.py — see SPEC-008-A.

Per Protocol 8 these tests use no mocks. The linter is pure-regex / pure-Python
and deterministic; tests run against real input.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

from helpers.interview_validator import (
    RULES,
    LintResult,
    LintViolation,
    lint_question,
    lint_script,
)


# ---------- registry sanity ----------


def test_rule_registry_is_non_empty():
    assert len(RULES) > 0


def test_rule_names_are_unique():
    names = [r.name for r in RULES]
    assert len(names) == len(set(names))


def test_every_rule_has_required_fields():
    for r in RULES:
        assert r.name
        assert r.explanation
        assert r.category in {
            "hypothetical",
            "opinion",
            "leading",
            "pricing-speculation",
            "future-tense",
            "commitment-fishing",
            "validation-seeking",
        }
        assert r.pattern is not None


# ---------- per-rule true-positive / true-negative coverage ----------


@pytest.mark.parametrize(
    "rule_name,positive,negative",
    [
        (
            "hypothetical-would-you",
            "Would you use a tool that automates invoice categorisation?",
            "Walk me through the last time you reconciled invoices manually.",
        ),
        (
            "hypothetical-do-you-think",
            "Do you think AI-driven scheduling would help your practice?",
            "Tell me about your scheduling routine last week.",
        ),
        (
            "hypothetical-if",
            "If you had a perfect tool for this, what would it look like?",
            "What did you do when this last broke?",
        ),
        (
            "hypothetical-future-tense",
            "Will you adopt a new tool if it solves this?",
            "What did you adopt last quarter to address this?",
        ),
        (
            "pricing-speculation",
            "How much would you pay for a tool like this?",
            "What did you pay for the workaround last month?",
        ),
        (
            "pricing-future",
            "What would it be worth to you to save those hours?",
            "What did saving those hours mean for the business last quarter?",
        ),
        (
            "opinion-do-you-like",
            "Do you like our approach to invoice matching?",
            "How does your current invoice matching work?",
        ),
        (
            "opinion-would-it-be-useful",
            "Would it be useful to have an AI auto-suggest categories?",
            "Tell me about a time auto-categorisation got something wrong.",
        ),
        (
            "leading-dont-you-think",
            "Don't you think this is a real problem?",
            "Walk me through how you've handled this in the past.",
        ),
        (
            "leading-wouldnt-it",
            "Wouldn't it be great if reconciliation were instant?",
            "What does the current reconciliation process feel like at month-end?",
        ),
        (
            "commitment-fishing",
            "Would you buy a service that does this for $99/month?",
            "Have you ever paid for a service that addresses this?",
        ),
        (
            "validation-seeking",
            "Does that make sense?",
            "What did I just summarise that doesn't match your experience?",
        ),
    ],
)
def test_rule_positive_and_negative(rule_name, positive, negative):
    pos_result = lint_question(positive)
    pos_rule_names = {v.rule for v in pos_result.violations}
    assert rule_name in pos_rule_names, (
        f"expected rule {rule_name!r} to flag positive case {positive!r}; "
        f"got rules: {sorted(pos_rule_names)}"
    )

    neg_result = lint_question(negative)
    neg_rule_names = {v.rule for v in neg_result.violations}
    assert rule_name not in neg_rule_names, (
        f"expected rule {rule_name!r} NOT to flag negative case {negative!r}; "
        f"got rules: {sorted(neg_rule_names)}"
    )


# ---------- structural ----------


def test_clean_question_returns_no_violations():
    r = lint_question("Walk me through the last time you ran into this problem.")
    assert r.is_clean
    assert r.violations == ()


def test_violation_records_span():
    r = lint_question("Would you use this tool?")
    assert not r.is_clean
    v = next(v for v in r.violations if v.rule == "hypothetical-would-you")
    start, end = v.span
    assert 0 <= start < end <= len(r.question)
    matched = r.question[start:end]
    # The match should at least contain "would you" (case-insensitive)
    assert "would you" in matched.lower()


def test_question_with_multiple_violations_records_all():
    """A single question that triggers multiple rules should report each."""
    # "Would it be useful" → opinion-would-it-be-useful
    # "if you had"        → hypothetical-if
    r = lint_question("Would it be useful if you had a tool that did this for you?")
    rule_names = {v.rule for v in r.violations}
    assert "opinion-would-it-be-useful" in rule_names
    assert "hypothetical-if" in rule_names


def test_lint_script_preserves_order():
    questions = [
        "Walk me through last Tuesday.",
        "Would you use a tool that automates this?",
        "What did you spend on the workaround last quarter?",
    ]
    results = lint_script(questions)
    assert len(results) == 3
    assert results[0].is_clean
    assert not results[1].is_clean
    assert results[2].is_clean
    # Order preserved
    assert [r.question for r in results] == questions


def test_lint_script_handles_empty_input():
    assert lint_script([]) == []


def test_case_insensitivity():
    """Rules must match regardless of case."""
    upper = lint_question("WOULD YOU USE A TOOL THAT AUTOMATES X?")
    lower = lint_question("would you use a tool that automates x?")
    upper_rules = {v.rule for v in upper.violations}
    lower_rules = {v.rule for v in lower.violations}
    assert "hypothetical-would-you" in upper_rules
    assert "hypothetical-would-you" in lower_rules


def test_past_tense_would_you_have_done_does_not_trigger():
    """The hypothetical-would-you rule must not fire on past-tense framings."""
    r = lint_question("Would you have used a tool like that last quarter?")
    rule_names = {v.rule for v in r.violations}
    assert "hypothetical-would-you" not in rule_names


# ---------- CLI ----------


def _run_cli(args: list[str], *, stdin: str | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Invoke the linter CLI as a subprocess. Uses the project root on PYTHONPATH."""
    project_root = Path(__file__).resolve().parent.parent
    env = {"PYTHONPATH": str(project_root), "PATH": "/usr/bin:/bin:/usr/local/bin"}
    return subprocess.run(
        [sys.executable, "-m", "helpers.interview_validator", *args],
        input=stdin,
        capture_output=True,
        text=True,
        env={**env},
        cwd=cwd or project_root,
    )


def test_cli_clean_file_exits_zero(tmp_path: Path):
    f = tmp_path / "script.txt"
    f.write_text("Walk me through last Tuesday.\nWhat did you spend on this last quarter?\n")
    r = _run_cli([str(f)])
    assert r.returncode == 0, r.stderr


def test_cli_dirty_file_exits_one(tmp_path: Path):
    f = tmp_path / "script.txt"
    f.write_text("Would you use a tool that automates X?\n")
    r = _run_cli([str(f)])
    assert r.returncode == 1, r.stderr
    assert "hypothetical-would-you" in r.stdout


def test_cli_missing_file_exits_two():
    r = _run_cli(["/no/such/path/script.txt"])
    assert r.returncode == 2


def test_cli_reads_stdin_when_no_args():
    r = _run_cli([], stdin="Would you use this?\n")
    assert r.returncode == 1
    assert "hypothetical-would-you" in r.stdout


def test_cli_reports_line_numbers(tmp_path: Path):
    f = tmp_path / "script.txt"
    f.write_text(
        dedent(
            """\
            Walk me through last Tuesday.
            Would you use a tool that automates X?
            What did you spend last quarter?
            """
        )
    )
    r = _run_cli([str(f)])
    assert r.returncode == 1
    # Violation should appear on line 2
    assert ":2:" in r.stdout
