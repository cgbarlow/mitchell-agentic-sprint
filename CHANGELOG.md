# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — Phase 1 (walking skeleton)
- Build foundation on `feature/v0.1.0`: `.gitignore`, `pyproject.toml` (Python ≥3.11, pytest 9.0.3, pyyaml 6.0.3 — verified 2026-05-08), `CHANGELOG.md`, GitHub Actions test workflow
- Phase 1 ADRs (001, 002, 003, 005, 010, 011, 012) and specs (SPEC-001-A WH(Y) format, SPEC-003-A plugin manifest, SPEC-005-A sprint state schema)
- Claude Code plugin manifest (`.claude-plugin/plugin.json`) and marketplace declaration with hard `campaign-mode` (0.4.8) and `six-animals` (0.1.2) dependencies
- `helpers/sprint_state.py` — read/write of `.sprint/sprint.md`, gate enforcement, loopback semantics, atomic writes (22 passing pytest tests, no mocks per Protocol 8)
- `skills/seed-vc-agent/SKILL.md` — canonical Mini Council voice (1 of 5); 2026-AI-era pre-seed lens with Dragon-style adversarial tone
- `commands/sprint-start.md` — Step 1 Discovery flow invoking gandalf-agent with anti-sycophancy posture
- `commands/sprint-council.md` — single-voice Council invocation (Seed VC) for Phase 1 walking skeleton

### Added — Phase 5 (Steps 5 + 6 + artifact templates + worked example #3)
- ADR-009 (markdown-first artifacts; defer slide rendering to v0.2.0) and SPEC-009-A (sales deck 6–8 slides, outreach plan 3 sections, investor deck 12 slides + appendix; universal rules of evidence-citation, no-padding, verbatim quotes, 2026-AI-era investor-deck non-negotiables checklist)
- Three read-only artifact templates: `docs/templates/{sales-deck,outreach-plan,investor-deck}.md` — slide-per-section structure with speaker notes and `{{placeholder}}` markers populated by `/sprint-step-6`
- `commands/sprint-step-5.md` — Competitor + Positioning Whitespace (concept §4.5) with NotebookLM `notebook_query` integration when MCP available; explicit handling of "no genuine whitespace" finding as a decision point
- `commands/sprint-step-6.md` — Synthesis (concept §4.6) populating the three markdown artifacts to `.sprint/artifacts/` from sprint state; runs the 2026-AI-era 5-non-negotiable investor-deck checklist; optional NotebookLM `studio_create` audio overview (the one Step 6 artifact without a Claude-only equivalent)
- `commands/sprint-continue.md` — re-entry dispatcher; reads sprint state, surfaces per-section status, presents context-appropriate next-step options based on `(step, last_approved_step)`
- `docs/examples/worked-example-3-loopback.md` — full Step 1→6 worked example continuing fictional Sam from worked-example-2; demonstrates artefacts + loopback evidence flowing into a successful attempt 2; canonical reference for "what a finished v0.1.0 Sprint looks like"

### Added — Phase 4 (Step 4 Framework + NotebookLM MCP integration)
- ADR-006 (NotebookLM via MCP — non-Enterprise path, optional dependency, Claude-only fallback) and SPEC-006-A (integration points, MCP tool-call pattern, helper API, onboarding flow, on-disk artifact paths)
- `helpers/notebooklm.py` — pure-function prompt builders for the four NotebookLM integration points (Step 3 theme map, Step 4 framework synthesis, Step 5 positioning whitespace, Step 6 audio overview); `is_mcp_available()` for code-side branching; 21 passing pytest tests verifying anti-sycophancy posture, output format requirements, argument inclusion, and determinism
- `pyproject.toml` declares `notebooklm-mcp-cli>=0.6.6` as `[notebooklm]` optional extra (verified 2026-05-09 against PyPI per Protocol 10)
- `commands/sprint-setup.md` — one-time pre-flight; verifies campaign-mode + six-animals; optionally onboards NotebookLM MCP (install / `nlm login` / `nlm setup add claude-code` / `nlm doctor`); records outcome to `.sprint/setup.md`
- `commands/sprint-step-4.md` — 6-sub-flow Step 4 dispatcher (generate 5 candidate experts → pick one → add sources → framework synthesis → reading/watching list → conclude); shells out to `helpers.notebooklm` for prompt construction; routes through NotebookLM `notebook_query` MCP tool when available, Claude-only fallback otherwise

### Added — Phase 3 (Step 3 Buyer Interviews + linter + saturation)
- ADR-008 (anti-sycophancy via Dragon-style preambles + behavioural-interview linter) and SPEC-008-A (linter rule registry, 12 rules across 7 categories)
- `helpers/interview_validator.py` — Mom Test linter with 12 deterministic regex rules; library API + `python -m` CLI; 27 passing pytest tests covering each rule's true-positive/true-negative, structural cases, and CLI exit codes
- `helpers/saturation.py` — interview-theme saturation detector (concept §4.3 "three in a row" rule, configurable threshold); library API + `python -m` CLI with JSON-default and `--human` output; 19 passing pytest tests
- `commands/sprint-step-3.md` — 5-sub-flow dispatcher (generate script + outreach / log interview / update theme map / check saturation / conclude). Sub-flow A shells out to the linter and regenerates violating questions before the user sees them. Sub-flow D shells out to the saturation helper.
- `docs/examples/worked-example-2-prosumer.md` — second worked example showing Step 3 sub-flows end-to-end and a loopback (saturated themes + zero costly-action signals → reset to a paid-newsletter ICP)

### Added — Phase 2 (Mini Council expansion + Step 2 + loopback)
- Phase 2 ADRs: ADR-004 (Mini Council as five new SKILL.md NPCs), ADR-007 (per-step gate enforcement via `last_approved_step`)
- Phase 2 specs: SPEC-004-A (Mini Council SKILL.md format), SPEC-007-A (step gate command flow + friendly-error pattern)
- Four remaining Mini Council voices: `churned-customer-agent`, `competitor-founder-agent`, `future-self-agent`, `grumpy-pm-agent` — each with voice-specific Foundation, Core Skills, and three-verdict Council Output Format
- `commands/sprint-council.md` rewritten to orchestrate all five voices in sequence (with optional single-voice mode); aggregates verdicts into a summary table without voting
- `commands/sprint-step-2.md` — Vertical Stack work; gated on Step 1 approval; invokes Gandalf with the five-layer narrowing (vertical / sub-vertical / ICP / workflow / AI leverage); auto-approves on artifact completion
- `commands/sprint-loopback.md` — concept §7 retain/clear semantics; user names disqualified vertical and reason; clears Vertical Stack / Competitor Map / Positioning Whitespace / Artifacts; retains Builder Profile / Backup Verticals / Interview Log / Theme Map / Costly-Action Signals / Expert Framework / Loopback Log / Progress Log
- `docs/examples/worked-example-1-vertical-saas.md` — voice-fidelity reference per ADR-010; demonstrates the five voices producing meaningfully different critiques on the same input
