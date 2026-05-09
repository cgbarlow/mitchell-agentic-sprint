# SPEC-006-A: NotebookLM MCP Integration Points

| Field | Value |
|-------|-------|
| **Specification ID** | SPEC-006-A |
| **Parent ADR** | [ADR-006](../ADR-006-NotebookLM-MCP-Integration.md) |
| **Version** | 1.0 |
| **Status** | Active |
| **Last Updated** | 2026-05-09 |

---

## Overview

Defines (a) where NotebookLM augments MAS (Steps 3, 4, 5, 6), (b) the MCP tool-call pattern for each integration point, (c) the Claude-only fallback semantics, (d) the on-disk artifact paths, and (e) the user-facing onboarding flow that lives in `commands/sprint-setup.md`.

The `helpers/notebooklm.py` module exposes pure-function **prompt builders** for each integration point. The same prompt is used whether the call routes to NotebookLM via MCP or to Claude in fallback mode. The slash command (not the helper) decides which path to take, based on whether the NotebookLM MCP server is configured in the user's environment.

## Integration points

| Step | Integration goal | Source documents fed to the notebook | NotebookLM output | Fallback (Claude-only) |
|---|---|---|---|---|
| 3 (Buyer Interviews) | Theme map + saturation evidence | `.sprint/interviews/*.md` (verbatim transcripts) | Theme list with verbatim quote citations per theme; recurrence counts | Claude reads transcripts; produces theme list using the same prompt; cites quotes inline |
| 4 (Framework) | Expert framework synthesis | URLs / PDFs / transcripts of the chosen expert's books, courses, long-form interviews | Framework summary; "3 to keep verbatim" / "3 to adapt for our ICP" split with citations | Claude summarises from user-pasted excerpts; same output structure |
| 5 (Competitor) | Positioning whitespace clustering | Top-10 competitor URLs (pricing pages, landing pages, case studies) | Competitor cluster map; positioning gaps; verbatim quote evidence per cluster | Claude synthesises from user-pasted excerpts; same output structure |
| 6 (Synthesis) | Audio overview + mind map (artefacts) | The full notebook (everything from Steps 3–5 already added as sources) | Audio overview (~10 min, MP3); mind map | Skipped in fallback — Claude-only path produces only markdown synthesis; audio is a NotebookLM-only feature |

Step 6's audio overview is the one feature that has no Claude-only equivalent. When the MCP server is absent, the Step 6 command surfaces this gap explicitly: the user gets the markdown artefacts but is told that audio overview requires the bolt-on.

## MCP tool-call pattern

The slash commands invoke NotebookLM through these `notebooklm-mcp-cli`-exposed MCP tools:

| Sprint moment | MCP tool | Arguments | Purpose |
|---|---|---|---|
| Step 3 sub-flow A enters | `notebook_create` | `name="MAS Sprint — {date}"` | One notebook per sprint attempt; reused across Steps 3–6 |
| Step 3 sub-flow B (each interview logged) | `source_add` | `notebook=<id>, url_or_text=<transcript>` | Add the interview transcript as a notebook source |
| Step 3 sub-flow C (theme map) | `notebook_query` | `notebook=<id>, query=<theme_map_prompt>` | Synthesize theme map from current sources |
| Step 4 (expert sources added) | `source_add` | `notebook=<id>, url_or_text=<expert_doc>` | Add each expert source |
| Step 4 (framework synthesis) | `notebook_query` | `notebook=<id>, query=<framework_prompt>` | Produce keep-verbatim / adapt split |
| Step 5 (competitor pages added) | `source_add` | `notebook=<id>, url_or_text=<competitor_url>` | Add each competitor page |
| Step 5 (whitespace clustering) | `notebook_query` | `notebook=<id>, query=<whitespace_prompt>` | Cluster competitors and surface gaps |
| Step 6 (audio overview) | `studio_create` | `notebook=<id>, type="audio_overview"` | Generate ~10 min podcast briefing |
| Step 6 (download) | `download_artifact` | `notebook=<id>, artifact=<id>` | Save to `.sprint/artifacts/audio-overview.mp3` |

The notebook ID is recorded in `.sprint/sprint.md` Artifacts section so the Sprint can resume mid-stream without re-creating the notebook.

## Helper module API (`helpers/notebooklm.py`)

```python
def is_mcp_available(env: dict[str, str] | None = None) -> bool:
    """Return True iff the user's environment has the NotebookLM MCP server configured.

    For v0.1.0 we use a simple env-var signal (`MAS_NOTEBOOKLM_MCP=1`) the user sets
    in their `.claude/settings.json` mcpServers section or shell environment. The
    slash command also checks for tool availability via Claude's introspection at
    invocation time — this helper is for code-side branching only.
    """

def build_theme_map_prompt(transcripts_count: int, vertical_summary: str) -> str:
    """Prompt for Step 3 theme-map synthesis. Same prompt for MCP and Claude-only paths."""

def build_framework_synthesis_prompt(
    expert_name: str, icp_summary: str, workflow_summary: str
) -> str:
    """Prompt for Step 4 expert-framework synthesis."""

def build_whitespace_prompt(
    competitors: list[str], theme_map_summary: str, framework_summary: str
) -> str:
    """Prompt for Step 5 positioning-whitespace clustering."""

def build_audio_overview_prompt(builder_profile: str, vertical_summary: str) -> str:
    """Prompt for Step 6 audio-overview narration."""
```

All prompts are pure functions of their arguments. Tests cover construction, sectioning, and that each prompt embeds the anti-sycophancy posture from concept §6.

## Onboarding flow (`commands/sprint-setup.md`)

The `/sprint-setup` command is a one-time pre-flight per project:

1. Verify `campaign-mode` and `six-animals` are installed (per ADR-003).
2. Detect whether NotebookLM MCP is configured.
3. If not, offer to configure:
   - Show the install command for the current OS / package manager
   - Run `nlm login` interactively (browser handshake)
   - Run `nlm setup add claude-code`
   - Verify with `nlm doctor`
4. Document the Claude-only fallback for users who decline.
5. Write `.sprint/setup.md` recording the chosen configuration so subsequent commands can dispatch correctly.

## On-disk artifact paths

| Artifact | Path | Step |
|---|---|---|
| Sprint state | `.sprint/sprint.md` | all |
| Interview transcripts | `.sprint/interviews/{NN}-{pseudonym}.md` | 3 |
| Setup record | `.sprint/setup.md` | all (written by `/sprint-setup`) |
| Notebook ID record | `.sprint/sprint.md` Artifacts → NotebookLM ID | 3+ |
| Audio overview | `.sprint/artifacts/audio-overview.mp3` | 6 |
| Mind map (when supported) | `.sprint/artifacts/mind-map.png` | 6 |

The `.sprint/artifacts/` directory is created lazily by Step 6.

## Acceptance criteria

This spec is fulfilled when:
- `helpers/notebooklm.py` exposes the four prompt builders + `is_mcp_available`
- Tests cover each prompt builder for required-content presence (anti-sycophancy posture, source citation requirements, output format)
- `commands/sprint-setup.md` implements the four-step onboarding above
- `commands/sprint-step-4.md` integrates the framework-synthesis path with both NotebookLM and Claude-only routing
- ADR-006's reference state (May 2026) is documented; the spec instructs the implementer to verify with Context7 at install time
- The Claude-only fallback path is exercised by all Step 3/4/5 commands when MCP is unavailable
- Step 6's audio-overview limitation is documented (NotebookLM-only feature; no Claude-only equivalent)
