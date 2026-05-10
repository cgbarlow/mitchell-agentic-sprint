# Mitchell Agentic Sprint

A Claude Code plugin that walks an AI-strong builder through six sequential steps to take one of their many ideas and prove out whether it can become a real business — adversarial by default, refusing flattery, demanding verbatim evidence.

By the end of the Sprint, the builder has a locked Vertical Stack, 15–30 buyer interviews captured verbatim, a Mom Test–disciplined theme map, an adapted expert framework, a competitor cluster map with positioning whitespace, and three markdown artefacts ready to take into customer conversations and pre-seed pitches: a **sales deck**, a **customer outreach plan**, and a **pre-seed investor deck**.

The Sprint does **not** build the product or the website. It gets the builder to the point where they know whether what they're building will sell, and they have the materials to prove it.

## Concept

Authored by **Scott Mitchell** (Mitchell Agentic Partners). Working name.

→ Full concept: [`docs/concept/concept.md`](docs/concept/concept.md)

## Status

**v0.1.0** — Claude Code plugin. The six steps are wired end-to-end with optional NotebookLM MCP augmentation for synthesis. Slide rendering (PPTX/PDF) and an anti-sycophancy regression eval set are deferred to v0.2.0+ per [ADR-009](docs/adrs/ADR-009-Markdown-First-Artifacts.md) and [ADR-002](docs/adrs/ADR-002-Build-Tier-Moderate-Plus-NotebookLM.md).

## Design principles

- **Adversarial by default** — every prompt refuses flattery and pushes back on vague answers (concept §6)
- **Behavioural over hypothetical** — interview scripts pass through a Mom Test linter that bans "would you…" questions before the user ever sees them ([SPEC-008-A](docs/adrs/specs/SPEC-008-A-Anti-Sycophancy.md))
- **Saturation over headcount** — interviews stop when the last 3 surface no new themes, not at an arbitrary count ([helpers/saturation.py](helpers/saturation.py))
- **Loopback on validation failure** — failed verticals retain Builder Profile, themes, and framework into the next attempt; Vertical Stack and downstream are cleared (concept §7, [SPEC-005-A](docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md))
- **Mini Council** — five skeptical NPC voices (Seed VC, Churned Customer, Competitor Founder, Future-Self, Grumpy PM) tear up the idea between Steps 1→2 and 4→5
- **Output is artefacts, not product** — three markdown artefacts populated from sprint state, no padding when evidence is missing ([ADR-009](docs/adrs/ADR-009-Markdown-First-Artifacts.md))

## Quick start

### Claude Cowork (recommended for MAS)

The Sprint is well-suited to Cowork. A six-step validation pipeline runs across multiple sessions over days or weeks, with persistent state at each gate and asynchronous artefact production — that's the shape Cowork is built for. Use Cowork unless you have a reason to prefer the CLI.

1. From the **Cowork** tab in Claude Desktop, select **+** → **Plugins** → **Add plugin**
2. **Add marketplace** — Select the **By Anthropic** dropdown, then **Add marketplace from GitHub** and enter:
   ```
   https://github.com/cgbarlow/skills
   ```
3. **Install three plugins** from the marketplace: **Six Animals**, **Campaign Mode**, and **Mitchell Agentic Sprint** (the Sprint depends on the other two; per [ADR-003](docs/adrs/ADR-003-Sibling-Plugin-Shape.md))
4. **Begin your Sprint** — run:
   ```
   /sprint-start
   ```
   On the first run in a project, `/sprint-start` auto-invokes setup: prerequisites are verified and the **🧢 Mitchell** profile is offered (default install). The Sprint runs in Claude-only synthesis mode — fully featured for Cowork users. (The optional NotebookLM bolt-on for source-grounded synthesis is **Claude Code CLI only**; see [below](#optional-claude-code-cli-only-notebooklm-mcp-bolt-on) for that path.) Then Step 1 (Discovery) opens with Mitchell framing your unfair advantages, runway, and rough idea.

   To re-configure later (install Mitchell after declining, onboard NotebookLM after the fact), call `/sprint-setup` directly.

### Claude Code CLI

For terminal-first users:

1. **Install Claude Code** ([full guide](https://code.claude.com/docs/en/quickstart)):
   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   ```
2. **Add the marketplace** — in a Claude Code session:
   ```
   /plugin marketplace add cgbarlow/skills
   ```
3. **Install the three plugins:**
   ```
   /plugin install six-animals@cgbarlow-skills
   /plugin install campaign-mode@cgbarlow-skills
   /plugin install mitchell-agentic-sprint@cgbarlow-skills
   /reload-plugins
   ```
4. **Begin your Sprint:**
   ```
   /sprint-start
   ```
   First run auto-invokes setup (prerequisites, Mitchell profile, NotebookLM offer). Re-configure later via `/sprint-setup`.

Pinned compatibility: `campaign-mode@0.4.8`, `six-animals@0.1.2` (verified 2026-05-08). Or clone the repos into your `.claude/plugins/` directory if you'd rather skip the marketplace entirely.

### Optional (Claude Code CLI only): NotebookLM MCP bolt-on

**The NotebookLM bolt-on works in Claude Code CLI only — it does NOT work in Claude Cowork.** This is a platform constraint, not a Sprint limitation: `nlm setup add claude-code` writes to Claude Code (CLI)'s user-scope config (`~/.claude/...`), not Claude Desktop's `claude_desktop_config.json`. And per [Anthropic's Cowork + local MCP support article](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop), Cowork only bridges remote MCP servers (custom connectors); it doesn't pick up local stdio MCP servers from `claude_desktop_config.json` either. So even manual config-editing doesn't help Cowork users.

**Cowork users:** skip this entirely. Claude-only synthesis works for the entire Sprint. You miss the NotebookLM audio overview in Step 6, but the three written artefacts (sales deck, outreach plan, investor deck) are produced equally well.

**Claude Code CLI users:** opt in if you want it. Setup runs on your local machine:

```bash
uv tool install "notebooklm-mcp-cli>=0.6.6"   # uv handles Python ≥3.11 automatically
# or: pip install "notebooklm-mcp-cli>=0.6.6" (needs Python ≥3.11 already)
# or: pipx install notebooklm-mcp-cli

nlm login                      # browser-based; one-time
nlm setup add claude-code      # wires up MCP for Claude Code (CLI only)
nlm doctor                     # verify
```

After install, **restart Claude Code**. Subsequent sessions pick up the saved login. The Sprint reads `.sprint/setup.md` to decide whether to route synthesis through NotebookLM or fall back to Claude-only.

See [ADR-006](docs/adrs/ADR-006-NotebookLM-MCP-Integration.md) and [SPEC-006-A](docs/adrs/specs/SPEC-006-A-NotebookLM-MCP.md) for the full integration contract.

## Commands

| Command | Step | What it does |
|---|---|---|
| [`/sprint-start`](commands/sprint-start.md) | 1 | **The single entry point.** First run auto-invokes setup (verify prereqs → install 🧢 Mitchell profile → offer NotebookLM bolt-on); subsequent runs go straight to Step 1 Discovery framed by Mitchell. |
| [`/sprint-setup`](commands/sprint-setup.md) | re-config | Re-run only when you want to change setup choices (e.g. install Mitchell after declining, onboard NotebookLM after the fact). Auto-invoked by `/sprint-start` on first run. |
| [`/sprint-step-2`](commands/sprint-step-2.md) | 2 | Vertical Stack — narrow to vertical × sub-vertical × ICP × workflow × AI leverage |
| [`/sprint-step-3`](commands/sprint-step-3.md) | 3 | Buyer Interviews — Mom Test–linted scripts; saturation detection |
| [`/sprint-step-4`](commands/sprint-step-4.md) | 4 | Framework — find the named expert, adapt their framework |
| [`/sprint-step-5`](commands/sprint-step-5.md) | 5 | Competitor + Positioning Whitespace |
| [`/sprint-step-6`](commands/sprint-step-6.md) | 6 | Synthesis — populate the three markdown artefacts |
| [`/sprint-council`](commands/sprint-council.md) | between steps | Convene the five Mini Council voices in sequence |
| [`/sprint-loopback`](commands/sprint-loopback.md) | any time | Reset to Step 2 retaining profile + themes + framework |
| [`/sprint-continue`](commands/sprint-continue.md) | re-entry | Read sprint state, route to next action |

## Mini Council voices

Five new SKILL.md NPC agents (per [ADR-004](docs/adrs/ADR-004-Mini-Council-Skills.md) and [SPEC-004-A](docs/adrs/specs/SPEC-004-A-Mini-Council-Skill-Format.md)) — each with embedded domain heuristics, Dragon-style adversarial tone, and a three-verdict output (Pass / Pass for now / In play):

| Voice | Lens |
|---|---|
| 💼 [Seed VC](skills/seed-vc-agent/SKILL.md) | 2026-AI-era pre-seed: real moats, inference economics, working demo + evals + buyer-tape as table stakes |
| 💔 [Churned Customer](skills/churned-customer-agent/SKILL.md) | post-purchase regret — onboarding-promise audit, "I'd cancel because…" |
| ⚔️ [Competitor Founder](skills/competitor-founder-agent/SKILL.md) | rival operator — where I'd attack you; what I'd copy / what I'd dismiss |
| ⏳ [Future-Self (12 mo)](skills/future-self-agent/SKILL.md) | regret enumeration; "the version of you that succeeded did this one thing" |
| 📋 [Grumpy PM](skills/grumpy-pm-agent/SKILL.md) | operational reality — realistic timeline; "what gets dropped on Tuesday" |

The Council fires meaningfully at the Step 1→2 and Step 4→5 transitions.

## Mentor profile — 🧢 Mitchell

The Sprint's framing mentor is campaign-mode's [Gandalf NPC](https://github.com/cgbarlow/campaign-mode/blob/main/skills/gandalf-agent/SKILL.md) — the voice that frames Discovery (Step 1), the Vertical Stack (Step 2), and the expert-framework search (Step 4). MAS ships a profile pack that re-skins Gandalf as **🧢 Mitchell** — Scott Mitchell as the founder-mentor persona, asking the questions he'd ask in a real conversation.

`/sprint-setup` offers to install the profile by default. Decline if you want the default 🧙 Gandalf appearance, or remove `.campaign/profiles/gandalf.md` later. The profile pack itself ships at [`profile-packs/mitchell-agentic-sprint/gandalf.md`](profile-packs/mitchell-agentic-sprint/gandalf.md) and follows campaign-mode's [SPEC-CM-006-A profile format](https://github.com/cgbarlow/campaign-mode/blob/main/docs/3_specs/SPEC-CM-006-A-Character-Profile-Format.md).

## State

Sprint state lives at `.sprint/sprint.md` per [SPEC-005-A](docs/adrs/specs/SPEC-005-A-Sprint-State-Schema.md) — frontmatter (sprint mode, current step, last approved step, attempt counter) plus named markdown sections per step. The schema accommodates loopback semantics: Builder Profile / Backup Verticals / Interview Log / Theme Map / Costly-Action Signals / Expert Framework / Loopback Log / Progress Log are retained on loopback; Vertical Stack / Competitor Map / Positioning Whitespace / Artifacts are cleared.

Interview transcripts are stored verbatim per concept §6 at `.sprint/interviews/{NN}-{pseudonym}.md`.

Generated artefacts land at `.sprint/artifacts/`:

- `sales-deck.md`
- `outreach-plan.md`
- `investor-deck.md`
- `audio-overview.mp3` (NotebookLM bolt-on only)

## Architecture decisions

All twelve ADRs follow the enhanced WH(Y) format (per [ADR-001](docs/adrs/ADR-001-Enhanced-ADR-Format.md), ported from `cgbarlow/iris`):

| ADR | Title |
|---|---|
| [001](docs/adrs/ADR-001-Enhanced-ADR-Format.md) | Adopt Enhanced WH(Y) ADR Format |
| [002](docs/adrs/ADR-002-Build-Tier-Moderate-Plus-NotebookLM.md) | Build Tier — Moderate + NotebookLM bolt-on |
| [003](docs/adrs/ADR-003-Sibling-Plugin-Shape.md) | Sibling-Plugin Shape with hard `campaign-mode` + `six-animals` deps |
| [004](docs/adrs/ADR-004-Mini-Council-Skills.md) | Mini Council as five new SKILL.md NPC agents |
| [005](docs/adrs/ADR-005-Sprint-State-Schema.md) | `.sprint/sprint.md` State Schema with Loopback |
| [006](docs/adrs/ADR-006-NotebookLM-MCP-Integration.md) | NotebookLM via MCP — non-Enterprise, optional, Claude-only fallback |
| [007](docs/adrs/ADR-007-Step-Gate-Enforcement.md) | Per-Step Gate Enforcement via `last_approved_step` |
| [008](docs/adrs/ADR-008-Anti-Sycophancy-Approach.md) | Anti-Sycophancy via Dragon-style preambles + behavioural-interview linter |
| [009](docs/adrs/ADR-009-Markdown-First-Artifacts.md) | Markdown-First Artifacts; defer slide rendering to v0.2.0 |
| [010](docs/adrs/ADR-010-TDD-Scope.md) | TDD Scope — Code Only; Council Voices via Worked-Example Review |
| [011](docs/adrs/ADR-011-Branch-Strategy.md) | Single `feature/v0.1.0` Branch with Gated PR Review |
| [012](docs/adrs/ADR-012-Python-And-Pytest-For-Helpers.md) | Python (with pytest) for Helpers |

Specs sit alongside in [`docs/adrs/specs/`](docs/adrs/specs/).

## Worked examples

Three reference Sprints in [`docs/examples/`](docs/examples/):

- [Worked example 1 — Vertical SaaS](docs/examples/worked-example-1-vertical-saas.md) — Step 1 + Mini Council voice differentiation reference
- [Worked example 2 — Prosumer with loopback](docs/examples/worked-example-2-prosumer.md) — Step 3 saturation with zero costly-action signals → loopback to a different ICP
- [Worked example 3 — Full Sprint with prior loopback](docs/examples/worked-example-3-loopback.md) — full Step 1→6 walkthrough including all three populated artefacts

## Development

Helpers are Python ≥3.11 with pytest. Per [ADR-010](docs/adrs/ADR-010-TDD-Scope.md) every helper module has unit tests; Mini Council voice fidelity is verified by manual worked-example review at gate reviews.

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

Helpers live in [`helpers/`](helpers/):

- [`sprint_state.py`](helpers/sprint_state.py) — read/write `.sprint/sprint.md`, gate enforcement, loopback semantics, atomic writes
- [`interview_validator.py`](helpers/interview_validator.py) — Mom Test linter (12 regex rules across 7 categories) + `python -m` CLI
- [`saturation.py`](helpers/saturation.py) — interview-theme saturation detector + `python -m` CLI
- [`notebooklm.py`](helpers/notebooklm.py) — pure-function prompt builders for the four NotebookLM integration points + `is_mcp_available()`

Development protocols are vendored from [`cgbarlow/protocols`](https://github.com/cgbarlow/protocols) at [`docs/protocols.md`](docs/protocols.md). Protocol 13 (`{@html}` security) does not apply — MAS is a Claude Code plugin, not a Svelte project.

## Research

The build was preceded by structured research published under [`docs/research/`](docs/research/):

- [Research plan](docs/research/research-plan.md)
- [Gap analysis](docs/research/gap-analysis.md) — what MAS needs that neither campaign-mode nor Six Animals provides
- [Build options](docs/research/build-options.md) — Minimum / Moderate / Extensive trade-offs
- [Recommendation](docs/research/RECOMMENDATION.md) — the chosen path (Moderate + NotebookLM bolt-on)

## License

CC-BY-SA-4.0

## Authors

- **Scott Mitchell** — concept and product direction
- **Chris Barlow** — implementation
