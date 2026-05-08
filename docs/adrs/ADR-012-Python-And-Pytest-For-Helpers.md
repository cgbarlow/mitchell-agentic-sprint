# ADR-012: Python (with pytest) for Helpers

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-012 |
| **Initiative** | v0.1.0 helper-language choice |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-08 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** v0.1.0 needing four small helper modules (`sprint_state`, `interview_validator`, `saturation`, `notebooklm`) under Protocol 3 (TDD) and Protocol 8 (production-ready code only),

**facing** the choice of language for the helpers — Python, Bash/shell, Node.js/TypeScript, or Go,

**we decided for** Python ≥3.11 with `pytest` ≥9.0.3 as the test framework, `pyyaml` ≥6.0.3 for frontmatter parsing, and standard library for everything else,

**and neglected** Bash/shell (poor TDD ergonomics; weak typing; awkward YAML parsing), Node.js/TypeScript (heavier toolchain for what amounts to ~500 lines of utility code; less natural fit for the NotebookLM Python ecosystem), and Go (overkill for a four-module helper layer; deployment complexity for a Claude Code plugin),

**to achieve** strong TDD ergonomics via pytest, a stable language matched to the NotebookLM CLI ecosystem (the unified `nlm` package and `notebooklm-mcp` are Python and Python-installable), straightforward dependency management via `pyproject.toml`, and a runtime that's already on most developer machines,

**accepting that** users running the plugin must have Python ≥3.11 available (already a near-universal assumption), helper failures will surface as Python tracebacks rather than friendlier errors (mitigated by good exception handling at command-invocation boundaries), and the dependency graph adds `pyyaml` (single, stable, ubiquitous library — minimal risk).

---

## Options Considered

| Option | Verdict |
|---|---|
| **Python + pytest (Selected)** | Strong TDD ergonomics; matches NotebookLM ecosystem; near-universal runtime |
| Bash + bats | Rejected — weak typing; awkward YAML parsing |
| Node.js / TypeScript | Rejected — heavier toolchain than warranted |
| Go | Rejected — overkill |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Refines | ADR-010 | TDD scope | Names the test framework |
| Relates To | ADR-006 | NotebookLM via MCP | Python ecosystem alignment |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| Protocol | `docs/protocols.md` Protocol 3 — TDD | [../protocols.md](../protocols.md) |
| Protocol | `docs/protocols.md` Protocol 10 — Latest Stable Dependencies | [../protocols.md](../protocols.md) |
| Verified | pytest 9.0.3 on PyPI | [pypi.org/project/pytest](https://pypi.org/project/pytest/) (verified 2026-05-08) |
| Verified | PyYAML 6.0.3 on PyPI | [pypi.org/project/PyYAML](https://pypi.org/project/PyYAML/) (verified 2026-05-08) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-08 |
