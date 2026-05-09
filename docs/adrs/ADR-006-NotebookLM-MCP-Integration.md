# ADR-006: NotebookLM via MCP — Non-Enterprise Path, Optional Dependency, Claude-Only Fallback

| Field | Value |
|-------|-------|
| **Decision ID** | ADR-006 |
| **Initiative** | Synthesis-layer integration for Steps 3–6 |
| **Proposed By** | Chris Barlow |
| **Date** | 2026-05-09 |
| **Status** | Accepted |

---

## WH(Y) Decision Statement

**In the context of** the v0.1.0 plan to bolt NotebookLM onto MAS as a synthesis layer for Steps 3 (theme map), 4 (expert framework), 5 (positioning whitespace), and 6 (audio overview) per [ADR-002](./ADR-002-Build-Tier-Moderate-Plus-NotebookLM.md) and the [research evaluation](../research/build-options.md#option-4--notebooklm-bolt-on-tier-bridging),

**facing** three viable access paths — the official **Google Cloud NotebookLM Enterprise API** (Workspace/Enterprise customers only, requires GCP project + service account), the unofficial **`notebooklm-mcp-cli`** package (single install providing both `nlm` CLI + `notebooklm-mcp` server, cookie-based auth via `nlm login`, ~35 MCP tools, browser handshake on first run), and the open-source **`open-notebook`** self-hosted alternative (no Google dependency, but custom infra),

**we decided for** the unofficial `notebooklm-mcp-cli` package as the primary v0.1.0 integration path, declared as an **optional dependency** in `pyproject.toml`, with a **Claude-only fallback path** that uses the same prompt-builder functions for Step 3/4/5/6 synthesis tasks when the MCP server is not configured,

**and neglected** the Enterprise API for v0.1.0 (high friction for individual AI-builders — GCP setup, service account provisioning; documented as a v0.2.0 addition for org-deployed users), `open-notebook` self-hosted (operational complexity for the v1 user persona; revisit if testers ask), and a hard NotebookLM dependency without fallback (would gate the entire Sprint behind a Google account requirement — incompatible with the v1 audience),

**to achieve** strong source-grounded synthesis aligned with the concept's "verbatim quotes only" rule (concept §6) for Steps 3–6, low onboarding friction (one `pip install`, one `nlm login`, one `nlm setup add claude-code`), and a graceful degradation path that keeps every Sprint completable even without Google account access,

**accepting that** the unofficial path carries Google ToS risk (mitigated by documenting the Enterprise API as a v0.2.0 escape hatch and by keeping the Claude-only fallback always available), each builder needs their own Google account to use the bolt-on (acceptable for v1 immediate-network audience; raises a polish gap for general-public v2), notebook source / quota limits apply per Google's tier policies (out of MAS's control), and per Protocol 7 we use Context7 MCP **at integration time on the user's machine** to verify the latest install pattern at the moment of use — this ADR documents the May 2026 reference state but explicitly defers final version pinning to install time.

---

## Reference state (verified May 2026; verify with Context7 at install time per Protocol 7)

| Item | Value |
|---|---|
| Package | `notebooklm-mcp-cli` |
| Latest stable on PyPI | `0.6.6` (released 2026-05-07) |
| Installation | `pip install notebooklm-mcp-cli` (or `uv tool install`, or `pipx install`) |
| Auth | `nlm login` — browser-based; cookies persisted locally |
| MCP setup | `nlm setup add claude-code` — automatic JSON config |
| MCP tools surfaced | ~35 across `notebook_*`, `source_*`, `studio_*`, `download_*`, `research_*`, `tag`, `pipeline`, etc. |

For the v0.1.0 use cases MAS only needs `notebook_create`, `source_add`, `notebook_query`, `studio_create`, `download_artifact`. Other tools may be useful for v0.2.0+.

## Options Considered

| Option | Verdict |
|---|---|
| **`notebooklm-mcp-cli` as optional dependency, with Claude-only fallback (Selected)** | Low friction; matches v1 audience; graceful degradation; documented Enterprise escape hatch |
| Enterprise API direct | Rejected for v0.1.0 — high onboarding friction; defer to v0.2.0 for org-deployed users |
| `open-notebook` self-hosted | Rejected — operational complexity beyond what individual builders will tolerate; revisit if testers ask |
| Hard NotebookLM dependency (no fallback) | Rejected — gates the Sprint behind Google account access; incompatible with v1 audience |

---

## Dependencies

| Relationship | ADR ID | Title | Notes |
|--------------|--------|-------|-------|
| Implements | ADR-002 | Build tier — Moderate + NotebookLM bolt-on | The bolt-on portion of ADR-002 |
| Refines | ADR-003 | Sibling-plugin shape | Optional dependency declared in `pyproject.toml` |
| Relates To | ADR-012 | Python + pytest for helpers | Python ecosystem alignment with NotebookLM packaging |

---

## References

| Reference ID | Title | Location |
|--------------|-------|----------|
| SPEC-006-A | NotebookLM MCP Integration Points | [specs/SPEC-006-A-NotebookLM-MCP.md](./specs/SPEC-006-A-NotebookLM-MCP.md) |
| Research | Build options §4 NotebookLM bolt-on | [docs/research/build-options.md](../research/build-options.md) |
| Upstream | `notebooklm-mcp-cli` README | [github.com/jacob-bd/notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) |
| Upstream | PyPI package | [pypi.org/project/notebooklm-mcp-cli](https://pypi.org/project/notebooklm-mcp-cli/) |
| Protocol | `docs/protocols.md` Protocol 7 — Context7 MCP for Language Research | [../protocols.md](../protocols.md) |
| Protocol | `docs/protocols.md` Protocol 10 — Latest Stable Dependencies | [../protocols.md](../protocols.md) |

---

## Status History

| Status | Approver | Date |
|--------|----------|------|
| Accepted | Chris Barlow | 2026-05-09 |
