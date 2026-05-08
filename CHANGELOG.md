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

### Added — Phase 2 (Mini Council expansion + Step 2 + loopback)
- Phase 2 ADRs: ADR-004 (Mini Council as five new SKILL.md NPCs), ADR-007 (per-step gate enforcement via `last_approved_step`)
- Phase 2 specs: SPEC-004-A (Mini Council SKILL.md format), SPEC-007-A (step gate command flow + friendly-error pattern)
- Four remaining Mini Council voices: `churned-customer-agent`, `competitor-founder-agent`, `future-self-agent`, `grumpy-pm-agent` — each with voice-specific Foundation, Core Skills, and three-verdict Council Output Format
- `commands/sprint-council.md` rewritten to orchestrate all five voices in sequence (with optional single-voice mode); aggregates verdicts into a summary table without voting
- `commands/sprint-step-2.md` — Vertical Stack work; gated on Step 1 approval; invokes Gandalf with the five-layer narrowing (vertical / sub-vertical / ICP / workflow / AI leverage); auto-approves on artifact completion
- `commands/sprint-loopback.md` — concept §7 retain/clear semantics; user names disqualified vertical and reason; clears Vertical Stack / Competitor Map / Positioning Whitespace / Artifacts; retains Builder Profile / Backup Verticals / Interview Log / Theme Map / Costly-Action Signals / Expert Framework / Loopback Log / Progress Log
- `docs/examples/worked-example-1-vertical-saas.md` — voice-fidelity reference per ADR-010; demonstrates the five voices producing meaningfully different critiques on the same input
