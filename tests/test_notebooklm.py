"""Tests for helpers/notebooklm.py — see SPEC-006-A.

The helper exposes pure-function prompt builders for the four NotebookLM
integration points (Steps 3, 4, 5, 6). The same prompt is used whether the
slash command routes to NotebookLM via MCP or to Claude in fallback mode.

Per Protocol 8: no mocks. is_mcp_available is exercised against real os.environ
copies; prompt builders are pure-Python string construction.
"""

from __future__ import annotations

import pytest

from helpers.notebooklm import (
    build_audio_overview_prompt,
    build_framework_synthesis_prompt,
    build_theme_map_prompt,
    build_whitespace_prompt,
    is_mcp_available,
)


# ---------- is_mcp_available ----------


def test_is_mcp_available_true_when_env_var_one():
    assert is_mcp_available({"MAS_NOTEBOOKLM_MCP": "1"}) is True


def test_is_mcp_available_false_when_env_var_zero():
    assert is_mcp_available({"MAS_NOTEBOOKLM_MCP": "0"}) is False


def test_is_mcp_available_false_when_env_var_missing():
    assert is_mcp_available({}) is False


def test_is_mcp_available_false_when_env_var_empty():
    assert is_mcp_available({"MAS_NOTEBOOKLM_MCP": ""}) is False


def test_is_mcp_available_accepts_true_truth_strings():
    """Be lenient on what counts as truthy; reject anything else."""
    for val in ("1", "true", "yes", "TRUE", "Yes"):
        assert is_mcp_available({"MAS_NOTEBOOKLM_MCP": val}) is True, val
    for val in ("0", "false", "no", "off", "", "anything-else"):
        assert is_mcp_available({"MAS_NOTEBOOKLM_MCP": val}) is False, val


# ---------- shared assertions for every prompt ----------


def _assert_anti_sycophancy_posture(prompt: str) -> None:
    """Every prompt must encode concept §6 anti-sycophancy posture."""
    lower = prompt.lower()
    # The prompt must require source-grounded citations
    assert "verbatim" in lower or "cite" in lower or "citation" in lower, (
        "prompt must demand verbatim/citation evidence"
    )
    # The prompt must refuse flattery / require honest gaps
    assert "no flattery" in lower or "refuse to flatter" in lower or "do not flatter" in lower, (
        "prompt must explicitly refuse flattery"
    )


def _assert_has_output_format(prompt: str) -> None:
    """Every prompt must specify the desired output structure."""
    lower = prompt.lower()
    assert "output" in lower or "format" in lower or "produce" in lower, (
        "prompt must specify output format"
    )


# ---------- theme map ----------


def test_theme_map_prompt_includes_arguments():
    p = build_theme_map_prompt(
        transcripts_count=8,
        vertical_summary="Solo creators with 1k–10k newsletter subscribers",
    )
    assert "8" in p
    assert "Solo creators with 1k–10k newsletter subscribers" in p


def test_theme_map_prompt_demands_costly_action_extraction():
    p = build_theme_map_prompt(
        transcripts_count=5, vertical_summary="any vertical"
    )
    assert "costly action" in p.lower() or "costly-action" in p.lower()


def test_theme_map_prompt_anti_sycophancy_and_format():
    p = build_theme_map_prompt(transcripts_count=4, vertical_summary="any")
    _assert_anti_sycophancy_posture(p)
    _assert_has_output_format(p)


def test_theme_map_prompt_handles_zero_transcripts():
    """The slash command should never call this with zero, but if it does the prompt
    must still be valid (not crash)."""
    p = build_theme_map_prompt(transcripts_count=0, vertical_summary="any")
    assert isinstance(p, str)
    assert len(p) > 0


# ---------- framework synthesis ----------


def test_framework_synthesis_prompt_includes_arguments():
    p = build_framework_synthesis_prompt(
        expert_name="April Dunford",
        icp_summary="Substack/Beehiiv operators with 1k+ paid subscribers",
        workflow_summary="Weekly content planning",
    )
    assert "April Dunford" in p
    assert "Substack/Beehiiv operators with 1k+ paid subscribers" in p
    assert "Weekly content planning" in p


def test_framework_synthesis_prompt_demands_keep_adapt_split():
    p = build_framework_synthesis_prompt(
        expert_name="Anyone", icp_summary="any ICP", workflow_summary="any"
    )
    lower = p.lower()
    # Must surface the "3 to keep verbatim / 3 to adapt" structure (concept §4.4)
    assert "keep verbatim" in lower
    assert "adapt" in lower


def test_framework_synthesis_prompt_anti_sycophancy_and_format():
    p = build_framework_synthesis_prompt("X", "Y", "Z")
    _assert_anti_sycophancy_posture(p)
    _assert_has_output_format(p)


# ---------- whitespace ----------


def test_whitespace_prompt_lists_competitors():
    p = build_whitespace_prompt(
        competitors=["Competitor A", "Competitor B", "Competitor C"],
        theme_map_summary="Pricing-friction recurring; manual-reconciliation common",
        framework_summary="April Dunford positioning model — alternatives + uniques + value",
    )
    assert "Competitor A" in p
    assert "Competitor B" in p
    assert "Competitor C" in p


def test_whitespace_prompt_includes_inputs():
    p = build_whitespace_prompt(
        competitors=["X"],
        theme_map_summary="THEMES",
        framework_summary="FRAMEWORK",
    )
    assert "THEMES" in p
    assert "FRAMEWORK" in p


def test_whitespace_prompt_demands_gap_articulation():
    p = build_whitespace_prompt(
        competitors=["X", "Y"], theme_map_summary="", framework_summary=""
    )
    lower = p.lower()
    assert "gap" in lower or "whitespace" in lower or "no one" in lower or "undersold" in lower


def test_whitespace_prompt_anti_sycophancy_and_format():
    p = build_whitespace_prompt(competitors=["A"], theme_map_summary="", framework_summary="")
    _assert_anti_sycophancy_posture(p)
    _assert_has_output_format(p)


def test_whitespace_prompt_handles_empty_competitor_list():
    p = build_whitespace_prompt(competitors=[], theme_map_summary="", framework_summary="")
    assert isinstance(p, str)
    assert len(p) > 0


# ---------- audio overview ----------


def test_audio_overview_prompt_includes_arguments():
    p = build_audio_overview_prompt(
        builder_profile="Sam, ex-fintech eng with 8 years in payments-ops",
        vertical_summary="AP automation for mid-market accounting firms",
    )
    assert "Sam, ex-fintech eng with 8 years in payments-ops" in p
    assert "AP automation for mid-market accounting firms" in p


def test_audio_overview_prompt_specifies_briefing_tone_not_entertainment():
    p = build_audio_overview_prompt("X", "Y")
    lower = p.lower()
    # The audio overview is a serious briefing, not infotainment
    assert "briefing" in lower or "brief" in lower
    # Must demand inclusion of risks/gaps, not just wins
    assert "risk" in lower or "gap" in lower or "weakness" in lower


def test_audio_overview_prompt_anti_sycophancy_and_format():
    p = build_audio_overview_prompt("X", "Y")
    _assert_anti_sycophancy_posture(p)
    _assert_has_output_format(p)


# ---------- prompts are idempotent / deterministic ----------


def test_prompt_builders_are_deterministic():
    """Same inputs → same prompt (pure functions)."""
    p1 = build_theme_map_prompt(5, "vertical")
    p2 = build_theme_map_prompt(5, "vertical")
    assert p1 == p2

    p1 = build_framework_synthesis_prompt("X", "Y", "Z")
    p2 = build_framework_synthesis_prompt("X", "Y", "Z")
    assert p1 == p2
