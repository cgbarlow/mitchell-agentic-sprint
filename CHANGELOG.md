# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Build foundation on `feature/v0.1.0`: `.gitignore`, `pyproject.toml` (Python ≥3.11, pytest 9.0.3, pyyaml 6.0.3 — verified 2026-05-08), `CHANGELOG.md`, GitHub Actions test workflow
- Phase 1 ADRs (001, 002, 003, 005, 010, 011, 012) and specs (SPEC-001-A WH(Y) format, SPEC-003-A plugin manifest, SPEC-005-A sprint state schema)
- Claude Code plugin manifest (`.claude-plugin/plugin.json`) and marketplace declaration with hard `campaign-mode` (0.4.8) and `six-animals` (0.1.2) dependencies
- `helpers/sprint_state.py` — read/write of `.sprint/sprint.md`, gate enforcement, loopback semantics, atomic writes (22 passing pytest tests, no mocks per Protocol 8)
- `skills/seed-vc-agent/SKILL.md` — canonical Mini Council voice (1 of 5); 2026-AI-era pre-seed lens with Dragon-style adversarial tone
- `commands/sprint-start.md` — Step 1 Discovery flow invoking gandalf-agent with anti-sycophancy posture
- `commands/sprint-council.md` — single-voice Council invocation (Seed VC) for Phase 1 walking skeleton
