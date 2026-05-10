# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.3.1] - 2026-05-10

### Changed
- **NotebookLM bolt-on reframed as power-user opt-in, not the default.** The platform constraints (Cowork's sandbox can't touch the user's local Claude Desktop config or browser) mean every NotebookLM setup requires Mac-side commands and a browser-based Google login — there is no zero-friction path with the current platform. Rather than burying users in setup steps for a feature most won't need, `/sprint-setup` now leads with **"Skip — use Claude-only synthesis (Recommended for most users)"** as option 1 and surfaces the Mac-side commitment explicitly before the user opts in. The trade-off (lose NotebookLM-specific audio overview, keep all three written artefacts) is stated upfront.
- `/sprint-setup` no longer attempts in-sandbox NotebookLM install. Cowork's sandbox is a remote VM with no access to the user's local Claude Desktop config — so even if `notebooklm-mcp-cli` installs successfully in the sandbox, the wire-up step (`nlm setup add claude-code`) modifies a Mac-side config file the sandbox cannot reach. The in-sandbox install was wasted effort. Step 4 now gives one clean set of Mac-side commands.
- README NotebookLM section retitled "Optional (power-user setup): NotebookLM MCP bolt-on" with the same up-front "most users should skip this" framing.

[v0.3.1]: https://github.com/cgbarlow/mitchell-agentic-sprint/releases/tag/v0.3.1

## [v0.3.0] - 2026-05-09

UX release. Removes the two-command `/sprint-setup` then `/sprint-start` friction (`/sprint-start` is now the single entry point) and adds first-class **Claude Cowork** support — the setup command no longer requires Bash and the NotebookLM bolt-on instructions account for Cowork's Python 3.10 sandbox limitation.

### Changed
- **`/sprint-start` auto-invokes setup on first run.** Detects missing `.sprint/setup.md`, runs sprint-setup's Steps 1–5, then continues directly into Step 1 (Discovery). No more two-step UX. `/sprint-setup` remains callable directly for re-configuration.
- **`/sprint-setup` is Cowork-compatible.** Profile install uses Read + Write instead of `mkdir + cp` (Bash optional), so it works in Cowork's no-shell environment. Existing-profile backup uses Read + Write to `.bak.{date}` instead of `mv`.
- **NotebookLM bolt-on now installs via `uv tool install` to work around Cowork's Python 3.10 sandbox.** `uv` provisions Python 3.11 on demand by downloading prebuilt binaries, so the in-Cowork install usually succeeds without leaving the sandbox. Setup tries `uv tool install` first; if that fails (network/filesystem restrictions in the sandbox), falls back to host-machine install instructions. CLI users on Python ≥3.11 hosts get the same `uv tool install` path which also works fine.
- README Quick Start drops the explicit `/sprint-setup` step in both Cowork and CLI paths; just `/sprint-start`.
- Commands table reorders: `/sprint-start` is the headline entry point; `/sprint-setup` is documented as the re-config command.
- `plugin.json` version 0.2.0 → 0.3.0 (Cowork update detection)

### Fixed
- `commands/sprint-start.md` injected-context "Before completing Step 4" reference now correctly points at the renumbered Step 5 (Discovery)

[v0.3.0]: https://github.com/cgbarlow/mitchell-agentic-sprint/releases/tag/v0.3.0

## [v0.2.0] - 2026-05-09

Minor feature release. Adds the **🧢 Mitchell profile pack** for the Gandalf NPC and restores the **Cowork-priority README** structure that PR #9's squash dropped. The default Sprint experience now opens with Mitchell as the framing mentor — Scott Mitchell as the founder-mentor persona, asking the questions he'd ask in a real conversation.

### Added
- **🧢 Mitchell profile pack** — re-skins campaign-mode's Gandalf NPC as Scott Mitchell, the founder-mentor persona. Profile pack file at `profile-packs/mitchell-agentic-sprint/gandalf.md` follows campaign-mode's SPEC-CM-006-A profile format (frontmatter `archetype: gandalf`, `skin-name: "Mitchell"`, `emoji: "🧢"` + Character Concept / Tone and Voice / Name sections).
- `/sprint-setup` Step 2 — offers to install the Mitchell profile to `.campaign/profiles/gandalf.md` (default install). Handles existing-profile case with keep / overwrite-with-backup / cancel options. Records the decision in `.sprint/setup.md` (`gandalf-profile: installed | declined | preexisting`; `gandalf-skin-name`).

### Changed
- `plugin.json` version 0.1.0 → 0.2.0 (Cowork update detection)
- README Quick Start now leads with **Claude Cowork** as the recommended install path, with Claude Code CLI as a secondary section for terminal-first users (mirrors campaign-mode's two-path structure). MAS is shaped like a Cowork workload — a six-step pipeline across multiple sessions over days/weeks with persistent state and asynchronous artefact production.
- README adds a "Mentor profile — 🧢 Mitchell" subsection between Mini Council voices and State, explaining the re-skin and where to find the profile pack.

[v0.2.0]: https://github.com/cgbarlow/mitchell-agentic-sprint/releases/tag/v0.2.0

## [v0.1.0] - 2026-05-09

First public release. Mitchell Agentic Sprint as a Claude Code plugin: 6-step linear pipeline (Discovery → Vertical Stack → Buyer Interviews → Framework → Competitor + Positioning Whitespace → Synthesis), adversarial-by-default Mini Council with five domain-knowledgeable NPC voices, deterministic Mom Test linter, theme-saturation detector, structural loopback semantics, three markdown artefact templates (sales deck / outreach plan / pre-seed investor deck) populated from sprint state, and an optional NotebookLM MCP bolt-on for source-grounded synthesis with a Claude-only fallback that keeps every Sprint completable. **89 passing pytest tests** across the four helper modules. Twelve WH(Y) ADRs and eight specs document the build.

### Added — build foundation (Phase 1)
- `.gitignore`, `pyproject.toml` (Python ≥3.11, pytest 9.0.3, pyyaml 6.0.3 — verified 2026-05-08 against PyPI per Protocol 10), `CHANGELOG.md`, GitHub Actions test workflow
- Claude Code plugin manifest (`.claude-plugin/plugin.json`) and marketplace declaration with hard `campaign-mode@0.4.8` and `six-animals@0.1.2` dependencies
- `helpers/sprint_state.py` — read/write `.sprint/sprint.md`, gate enforcement, loopback semantics, atomic writes (22 passing tests, no mocks per Protocol 8)
- `skills/seed-vc-agent/SKILL.md` — canonical Mini Council voice with 2026-AI-era pre-seed lens
- `commands/sprint-start.md` — Step 1 Discovery flow invoking gandalf-agent

### Added — Mini Council expansion + Step 2 + loopback (Phase 2)
- Four remaining Mini Council voices: `churned-customer-agent`, `competitor-founder-agent`, `future-self-agent`, `grumpy-pm-agent`
- `commands/sprint-council.md` orchestrating all five voices in sequence; optional single-voice mode; aggregates verdicts into a summary table without voting
- `commands/sprint-step-2.md` — Vertical Stack with five-layer narrowing (vertical / sub-vertical / ICP / workflow / AI leverage); gated on Step 1 approval per SPEC-007-A
- `commands/sprint-loopback.md` — concept §7 retain/clear semantics; user names disqualified vertical and reason
- `docs/examples/worked-example-1-vertical-saas.md` — voice-fidelity reference

### Added — Step 3 Buyer Interviews + linter + saturation (Phase 3)
- `helpers/interview_validator.py` — Mom Test linter with 12 deterministic regex rules across 7 categories (hypothetical, opinion, leading, pricing-speculation, future-tense, commitment-fishing, validation-seeking); library API + `python -m` CLI (27 passing tests)
- `helpers/saturation.py` — interview-theme saturation detector (concept §4.3 three-in-a-row rule); library API + `python -m` CLI with JSON-default and `--human` output (19 passing tests)
- `commands/sprint-step-3.md` — 5-sub-flow dispatcher; sub-flow A shells out to the linter and regenerates violating questions before the user sees them; sub-flow D shells out to the saturation helper
- `docs/examples/worked-example-2-prosumer.md` — Step 3 sub-flows end-to-end with loopback

### Added — Step 4 Framework + NotebookLM MCP (Phase 4)
- `helpers/notebooklm.py` — pure-function prompt builders for the four NotebookLM integration points (Step 3 theme map, Step 4 framework synthesis, Step 5 positioning whitespace, Step 6 audio overview); `is_mcp_available()` for code-side branching (21 passing tests verifying anti-sycophancy posture, output format requirements, argument inclusion, determinism)
- `notebooklm-mcp-cli>=0.6.6` declared as `[notebooklm]` optional extra (verified 2026-05-09 against PyPI)
- `commands/sprint-setup.md` — one-time pre-flight; verifies prerequisite plugins; optionally onboards NotebookLM MCP (install / `nlm login` / `nlm setup add claude-code` / `nlm doctor`); records outcome to `.sprint/setup.md`
- `commands/sprint-step-4.md` — 6-sub-flow Step 4 dispatcher (generate 5 candidate experts → pick one → add sources → framework synthesis → reading/watching list → conclude); routes through NotebookLM `notebook_query` MCP tool when available, Claude-only fallback otherwise

### Added — Steps 5 + 6 + artifacts + worked example #3 (Phase 5)
- Three read-only artifact templates: `docs/templates/{sales-deck,outreach-plan,investor-deck}.md` — slide-per-section structure with speaker notes and `{{placeholder}}` markers populated by `/sprint-step-6`
- `commands/sprint-step-5.md` — Competitor + Positioning Whitespace (concept §4.5); explicit handling of "no genuine whitespace" finding as a decision point (loopback / proceed / pause)
- `commands/sprint-step-6.md` — Synthesis (concept §4.6); populates the three markdown artefacts to `.sprint/artifacts/` from sprint state with no padding (`[EVIDENCE MISSING: ...]` markers explicit); runs the 2026-AI-era investor-deck 5-non-negotiables checklist; optional NotebookLM `studio_create` audio overview
- `commands/sprint-continue.md` — re-entry dispatcher; reads sprint state, surfaces per-section status, presents context-appropriate next-step options based on `(step, last_approved_step)`
- `docs/examples/worked-example-3-loopback.md` — full Step 1→6 worked example continuing fictional Sam from worked-example-2; demonstrates all three populated artefacts plus the audio overview reference

### Architecture decisions
- [ADR-001](docs/adrs/ADR-001-Enhanced-ADR-Format.md) — Adopt enhanced WH(Y) ADR format (ported from `cgbarlow/iris`)
- [ADR-002](docs/adrs/ADR-002-Build-Tier-Moderate-Plus-NotebookLM.md) — Build tier: Moderate + NotebookLM bolt-on
- [ADR-003](docs/adrs/ADR-003-Sibling-Plugin-Shape.md) — Sibling-plugin shape with hard `campaign-mode` + `six-animals` deps
- [ADR-004](docs/adrs/ADR-004-Mini-Council-Skills.md) — Mini Council as five new SKILL.md NPC agents
- [ADR-005](docs/adrs/ADR-005-Sprint-State-Schema.md) — `.sprint/sprint.md` state schema with named-step sections + loopback support
- [ADR-006](docs/adrs/ADR-006-NotebookLM-MCP-Integration.md) — NotebookLM via MCP (non-Enterprise, optional, Claude-only fallback)
- [ADR-007](docs/adrs/ADR-007-Step-Gate-Enforcement.md) — Per-step gate enforcement via `last_approved_step`
- [ADR-008](docs/adrs/ADR-008-Anti-Sycophancy-Approach.md) — Anti-sycophancy via Dragon-style preambles + behavioural-interview linter
- [ADR-009](docs/adrs/ADR-009-Markdown-First-Artifacts.md) — Markdown-first artifacts (defer slide rendering to v0.2.0)
- [ADR-010](docs/adrs/ADR-010-TDD-Scope.md) — TDD on code only; Council voices via worked-example review
- [ADR-011](docs/adrs/ADR-011-Branch-Strategy.md) — Single `feature/v0.1.0` branch with gated PR review
- [ADR-012](docs/adrs/ADR-012-Python-And-Pytest-For-Helpers.md) — Python (with pytest) for helpers

### Deferred to v0.2.0+
- Slide rendering (PPTX/PDF generation via python-pptx)
- WebSearch + scrape pipeline for Step 4/5 (currently relies on user-pasted inputs or NotebookLM)
- Anti-sycophancy regression eval set
- NotebookLM Enterprise API path
- Sales Navigator filter generator
- CRM integration for outreach
- Theme clustering beyond simple count saturation
- Profile-pack themes for Council voices

[Unreleased]: https://github.com/cgbarlow/mitchell-agentic-sprint/compare/v0.1.0...HEAD
[v0.1.0]: https://github.com/cgbarlow/mitchell-agentic-sprint/releases/tag/v0.1.0
