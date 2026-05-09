"""NotebookLM integration prompt builders + availability check — SPEC-006-A.

Pure-function prompt builders for the four NotebookLM integration points
(Steps 3 theme map, 4 framework synthesis, 5 positioning whitespace, 6 audio
overview). The same prompt is used whether the slash command routes to
NotebookLM via MCP or to Claude in fallback mode.

The availability check is a thin wrapper around an environment variable signal
(`MAS_NOTEBOOKLM_MCP=1`) that the user sets when their NotebookLM MCP server
is configured. The slash command supplements this with Claude-side
introspection at invocation time.
"""

from __future__ import annotations

import os
from typing import Mapping

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def is_mcp_available(env: Mapping[str, str] | None = None) -> bool:
    """Return True iff the user's environment signals NotebookLM MCP availability."""
    source = env if env is not None else os.environ
    raw = source.get("MAS_NOTEBOOKLM_MCP", "")
    return raw.strip().lower() in _TRUTHY


# ---------- shared anti-sycophancy preamble ----------

_ANTI_SYCOPHANCY = """
Anti-sycophancy posture (concept §6, non-negotiable):
- Refuse to flatter. Open with the strongest finding the evidence supports.
- Cite or it didn't happen. Every claim must be backed by a verbatim quote, a
  number, or a referenced source document.
- Behavioural over hypothetical. Past behaviour is signal; opinion is noise.
- Surface gaps explicitly. If the evidence is thin, say so plainly. Do not
  pad. No flattery, no hedging.
""".strip()


# ---------- Step 3: theme map ----------


def build_theme_map_prompt(transcripts_count: int, vertical_summary: str) -> str:
    """Prompt for theme-map synthesis from interview transcripts already in the notebook."""
    return f"""You are synthesising a theme map across {transcripts_count} buyer-interview transcript(s) for a Mitchell Agentic Sprint.

Vertical context: {vertical_summary}

{_ANTI_SYCOPHANCY}

Task:
1. Identify recurring themes across the interview transcripts. A theme recurs when ≥2 buyers describe a similar pain, workflow, workaround, or aspiration.
2. For each theme, extract one or more verbatim quotes from the transcripts that demonstrate it. Cite the interviewee pseudonym + interview number for every quote.
3. Identify costly-action signals — specific instances where a buyer spent money, hired someone, built a workaround, or complained loudly about the underlying pain. List each one separately.
4. Flag the strongest theme (most recurrent, most evidence) and the weakest signal (theme that surfaces but lacks costly action).

Output format (markdown):

## Recurring themes

### {{theme tag — kebab-case}}
- Recurrence: {{N}} interviews
- Verbatim quotes:
  - "{{quote}}" — {{pseudonym, interview NN}}
  - "{{quote}}" — {{pseudonym, interview NN}}
- Costly action evidence: {{summary, or "none"}}

(Repeat per theme.)

## Costly-action signals (consolidated)

- **{{pseudonym, interview NN}}** — {{specific costly action with evidence}}

## Strongest theme
{{One paragraph naming the theme, the recurrence, and the costly-action evidence.}}

## Weakest signal
{{One paragraph naming a theme that surfaces but lacks costly-action evidence — these are the candidates for "real pain, no wallet" disqualification.}}
"""


# ---------- Step 4: framework synthesis ----------


def build_framework_synthesis_prompt(
    expert_name: str,
    icp_summary: str,
    workflow_summary: str,
) -> str:
    """Prompt for expert-framework synthesis from source documents in the notebook."""
    return f"""You are synthesising the expert framework of {expert_name} as it applies to a Mitchell Agentic Sprint.

ICP: {icp_summary}
Workflow: {workflow_summary}

The notebook contains source documents authored by or about {expert_name} — books, courses, long-form interviews, paid products, written essays. Synthesise their framework and split it into "keep verbatim" vs "adapt for our ICP".

{_ANTI_SYCOPHANCY}

Task:
1. Summarise the expert's framework in plain language — three to five core principles, not jargon. Each principle gets one sentence and a verbatim quote citation.
2. Identify three principles to **keep verbatim** — the parts of the framework that apply directly to this ICP and workflow without modification. For each, cite the source document.
3. Identify three principles to **adapt** — the parts that need adjustment for this specific ICP / workflow. For each, name what must change and why. Cite the source for the original.
4. Flag any principles you cannot map to this ICP / workflow at all — these are candidates for either rejecting the framework choice or narrowing it further. Do not pad if there are none.

Output format (markdown):

## Framework summary

1. **{{principle 1 name}}** — {{one-sentence statement.}} ({{verbatim citation, source document}})
2. **{{principle 2 name}}** — {{statement.}} ({{citation}})
...

## Keep verbatim (3)

### {{principle name}}
- Why it applies directly: {{one sentence}}
- Source: {{citation}}

## Adapt (3)

### {{principle name}}
- Original statement: "{{verbatim from source}}"
- Adaptation for our ICP / workflow: {{specific change with reason}}
- Source: {{citation}}

## Cannot map (0–N)

{{Either: "No principles in this framework fail to map." OR a list of principles that don't fit, with one-sentence reasons each. Do not invent reasons to pad.}}
"""


# ---------- Step 5: positioning whitespace ----------


def build_whitespace_prompt(
    competitors: list[str],
    theme_map_summary: str,
    framework_summary: str,
) -> str:
    """Prompt for positioning-whitespace clustering across competitor pages."""
    competitor_list = (
        "\n".join(f"- {c}" for c in competitors)
        if competitors
        else "(no competitors provided — surface this as a finding)"
    )
    return f"""You are mapping positioning whitespace across competitor pages in a Mitchell Agentic Sprint.

Competitors in scope:
{competitor_list}

Theme map from buyer interviews:
{theme_map_summary}

Expert framework summary:
{framework_summary}

The notebook contains scraped or pasted-in pages from each competitor (landing pages, pricing pages, case studies). Cluster them by how they position, and identify the gaps where no competitor sits.

{_ANTI_SYCOPHANCY}

Task:
1. Cluster the competitors by their positioning theme — the dominant message they lead with on their landing page. Use 2–4 clusters; explicitly name the dominant message per cluster with verbatim quotes from each competitor's page.
2. Identify the **whitespace** — positioning angles that no competitor occupies but that the buyer interview themes suggest are valuable. Be specific: name the exact verbatim language the user could use that no competitor uses.
3. Recommend one positioning statement the user could own. It must (a) connect to a recurring theme from the buyer interviews, (b) draw on the expert framework, and (c) not be substantively occupied by any competitor cluster.
4. If you cannot find genuine whitespace — say so plainly. Do not invent positioning angles to pad.

Output format (markdown):

## Competitor clusters

### Cluster {{N}}: {{dominant message in plain language}}
- Members: {{competitor names}}
- Verbatim positioning quotes:
  - "{{quote}}" — {{competitor}}
  - "{{quote}}" — {{competitor}}
- What this cluster does well: {{one sentence}}
- What this cluster avoids: {{one sentence}}

(Repeat per cluster.)

## Whitespace (gaps)

- **{{gap name}}** — Buyers care about this (theme: {{theme tag}}, recurrence: {{N}} interviews). No competitor lands here. Verbatim phrasing the user could own: "{{phrase}}".

## Recommended positioning statement

> {{One-paragraph positioning statement the user can take into Step 6 deck work. Must reference a recurring theme + the expert framework + a whitespace angle.}}

## If there is no whitespace

{{Either: "Genuine whitespace exists." OR: a plain finding that the market is saturated and the user should consider Step 7 loopback to a different ICP / vertical / workflow. Do not pad.}}
"""


# ---------- Step 6: audio overview ----------


def build_audio_overview_prompt(builder_profile: str, vertical_summary: str) -> str:
    """Prompt for the Step 6 audio-overview narration. NotebookLM-only feature; no
    Claude-only equivalent (audio synthesis is the bolt-on's unique capability).
    """
    return f"""You are scripting a ~10-minute audio briefing for the user as they prepare for a pre-seed investor conversation, based on the full Mitchell Agentic Sprint notebook.

Builder profile: {builder_profile}

Vertical context: {vertical_summary}

This is a serious briefing, not entertainment. The user is going to listen to it before walking into a real conversation with a real seed VC. Tone: direct, evidence-anchored, no hype.

{_ANTI_SYCOPHANCY}

Task — produce an audio narration script structured as follows. The output should be paced for ~10 minutes when read at normal speed (approximately 1500 words).

1. **Opening (60 seconds).** State the vertical, the ICP, the workflow, the AI leverage point — in plain language. No hype. No "we're disrupting".
2. **Validation evidence (3 minutes).** Recurring themes from buyer interviews with verbatim quote highlights. Costly-action signals named. The strongest theme front-loaded.
3. **Differentiation (2 minutes).** The expert framework adopted, the positioning whitespace, the verbatim language nobody else uses.
4. **Risks and gaps (3 minutes).** This is the section the user needs most. Where is the evidence thin? Which Mini Council voice's verdict is still Pass-for-now? What would the seed VC ask that the user doesn't yet have an answer to? Surface these gaps explicitly.
5. **Ask (1 minute).** What the user is actually asking for in the conversation — not "$1M to disrupt the market" but a specific named ask grounded in the validation evidence.

Output format: a single markdown document with each section labelled. The document doubles as both the audio narration script and the briefing notes the user re-reads before the conversation.

Do **not** include music cues, sound effects, or theatre. This is briefing-grade content, not a podcast.
"""


__all__ = [
    "build_audio_overview_prompt",
    "build_framework_synthesis_prompt",
    "build_theme_map_prompt",
    "build_whitespace_prompt",
    "is_mcp_available",
]
