"""Reader/writer for `.sprint/sprint.md` — see SPEC-005-A.

The on-disk format is YAML frontmatter followed by markdown sections, each section
introduced by a level-2 heading. Sub-sections (level-3 and deeper) are kept inside
their parent section as raw markdown.
"""

from __future__ import annotations

import os
import re
import tempfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable

import yaml

# Canonical section ordering for the on-disk file.
CANONICAL_SECTIONS: tuple[str, ...] = (
    "Builder Profile",
    "Vertical Stack",
    "Backup Verticals",
    "Interview Log",
    "Theme Map",
    "Costly-Action Signals",
    "Expert Framework",
    "Competitor Map",
    "Positioning Whitespace",
    "Artifacts",
    "Loopback Log",
    "Progress Log",
)

RETAINED_ON_LOOPBACK: frozenset[str] = frozenset(
    {
        "Builder Profile",
        "Backup Verticals",
        "Interview Log",
        "Theme Map",
        "Costly-Action Signals",
        "Expert Framework",
        "Loopback Log",
        "Progress Log",
    }
)

CLEARED_ON_LOOPBACK: frozenset[str] = frozenset(
    {
        "Vertical Stack",
        "Competitor Map",
        "Positioning Whitespace",
        "Artifacts",
    }
)

VALID_SPRINT_MODES: frozenset[str] = frozenset({"Solo", "Coached"})


class SchemaError(ValueError):
    """Raised when sprint.md violates SPEC-005-A."""


class GateError(RuntimeError):
    """Raised when a step transition violates the gate (last_approved_step < N-1)."""


@dataclass
class SprintState:
    schema_version: int
    sprint_mode: str
    step: int
    last_approved_step: int
    attempt: int
    created: date
    sections: dict[str, str] = field(default_factory=dict)


# ---------- public API ----------


def init_state(sprint_mode: str = "Solo") -> SprintState:
    """Create a fresh SprintState with sensible defaults and all canonical sections empty."""
    if sprint_mode not in VALID_SPRINT_MODES:
        raise SchemaError(
            f"sprint_mode must be one of {sorted(VALID_SPRINT_MODES)}, got {sprint_mode!r}"
        )
    return SprintState(
        schema_version=1,
        sprint_mode=sprint_mode,
        step=1,
        last_approved_step=0,
        attempt=1,
        created=date.today(),
        sections={name: "" for name in CANONICAL_SECTIONS},
    )


def read_state(path: Path) -> SprintState:
    """Parse sprint.md from disk. Raises SchemaError on malformed content."""
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter(text)
    state = _state_from_frontmatter(frontmatter)
    state.sections = _parse_sections(body)
    # Ensure every canonical section is present, even if absent in the file
    for name in CANONICAL_SECTIONS:
        state.sections.setdefault(name, "")
    _validate(state)
    return state


def write_state(state: SprintState, path: Path) -> None:
    """Atomically write state to disk (write to temp + rename)."""
    _validate(state)
    serialized = _serialize(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write to temp file in same directory, then atomically rename.
    fd, tmp_path = tempfile.mkstemp(
        prefix=".sprint-", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(serialized)
        os.replace(tmp_path, path)
    except Exception:
        # Clean up temp file on failure
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def set_step(state: SprintState, step: int) -> None:
    """Advance the current step. Raises GateError if last_approved_step < step-1."""
    if not 1 <= step <= 6:
        raise SchemaError(f"step must be 1..6, got {step}")
    if step - 1 > state.last_approved_step:
        raise GateError(
            f"cannot advance to step {step}: last_approved_step is {state.last_approved_step}"
        )
    state.step = step


def approve_step(state: SprintState, step: int) -> None:
    """Mark step as gate-approved. Monotonic — never decreases."""
    if not 1 <= step <= 6:
        raise SchemaError(f"step must be 1..6, got {step}")
    state.last_approved_step = max(state.last_approved_step, step)


def loopback(state: SprintState) -> None:
    """Reset state for a new attempt: clear Step 2+ artifacts; retain profile + themes + framework."""
    for name in CLEARED_ON_LOOPBACK:
        state.sections[name] = ""
    state.attempt += 1
    state.step = 2
    state.last_approved_step = 1


def append_progress_log(state: SprintState, message: str) -> None:
    """Append a Progress Log entry in the canonical format."""
    entry = f"- **Progress** — {message} ({date.today().isoformat()})"
    _append_section_line(state, "Progress Log", entry)


def append_loopback_log(state: SprintState, *, vertical: str, reason: str) -> None:
    """Append a Loopback Log entry recording the disqualified vertical and reason."""
    entry = (
        f"- **attempt {state.attempt}** — disqualified `{vertical}` "
        f"({reason}) ({date.today().isoformat()})"
    )
    _append_section_line(state, "Loopback Log", entry)


# ---------- internals ----------


def _validate(state: SprintState) -> None:
    if state.schema_version != 1:
        raise SchemaError(f"schema_version must be 1, got {state.schema_version}")
    if state.sprint_mode not in VALID_SPRINT_MODES:
        raise SchemaError(
            f"sprint_mode must be one of {sorted(VALID_SPRINT_MODES)}, got {state.sprint_mode!r}"
        )
    if not 1 <= state.step <= 6:
        raise SchemaError(f"step must be 1..6, got {state.step}")
    if not 0 <= state.last_approved_step <= 6:
        raise SchemaError(
            f"last_approved_step must be 0..6, got {state.last_approved_step}"
        )
    if state.attempt < 1:
        raise SchemaError(f"attempt must be >= 1, got {state.attempt}")


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def _split_frontmatter(text: str) -> tuple[dict, str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        raise SchemaError("missing or malformed YAML frontmatter")
    raw_yaml, body = m.group(1), m.group(2)
    try:
        data = yaml.safe_load(raw_yaml) or {}
    except yaml.YAMLError as exc:
        raise SchemaError(f"frontmatter is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise SchemaError("frontmatter must be a YAML mapping")
    return data, body


_REQUIRED_FRONTMATTER_KEYS = (
    "schema-version",
    "sprint-mode",
    "step",
    "last_approved_step",
    "attempt",
    "created",
)


def _state_from_frontmatter(data: dict) -> SprintState:
    missing = [k for k in _REQUIRED_FRONTMATTER_KEYS if k not in data]
    if missing:
        raise SchemaError(f"frontmatter missing required keys: {missing}")
    created = data["created"]
    if isinstance(created, str):
        created = date.fromisoformat(created)
    if not isinstance(created, date):
        raise SchemaError("created must be a date or ISO date string")
    return SprintState(
        schema_version=int(data["schema-version"]),
        sprint_mode=str(data["sprint-mode"]),
        step=int(data["step"]),
        last_approved_step=int(data["last_approved_step"]),
        attempt=int(data["attempt"]),
        created=created,
        sections={},
    )


_H2_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)


def _parse_sections(body: str) -> dict[str, str]:
    """Parse markdown body into section-name -> content blob (everything until next H2)."""
    sections: dict[str, str] = {}
    matches = list(_H2_RE.finditer(body))
    for i, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        sections[name] = content
    return sections


def _serialize(state: SprintState) -> str:
    fm = {
        "schema-version": state.schema_version,
        "sprint-mode": state.sprint_mode,
        "step": state.step,
        "last_approved_step": state.last_approved_step,
        "attempt": state.attempt,
        "created": state.created.isoformat(),
    }
    fm_text = yaml.safe_dump(fm, sort_keys=False).strip()
    parts = [f"---\n{fm_text}\n---\n"]
    for name in CANONICAL_SECTIONS:
        content = state.sections.get(name, "")
        parts.append(f"\n## {name}\n")
        if content:
            parts.append(f"\n{content}\n")
    # Preserve any non-canonical sections (e.g. user-added) at the end
    for name, content in state.sections.items():
        if name in CANONICAL_SECTIONS:
            continue
        parts.append(f"\n## {name}\n")
        if content:
            parts.append(f"\n{content}\n")
    return "".join(parts)


def _append_section_line(state: SprintState, section: str, line: str) -> None:
    existing = state.sections.get(section, "")
    if existing:
        state.sections[section] = f"{existing.rstrip()}\n{line}"
    else:
        state.sections[section] = line


__all__ = [
    "CANONICAL_SECTIONS",
    "CLEARED_ON_LOOPBACK",
    "RETAINED_ON_LOOPBACK",
    "VALID_SPRINT_MODES",
    "GateError",
    "SchemaError",
    "SprintState",
    "append_loopback_log",
    "append_progress_log",
    "approve_step",
    "init_state",
    "loopback",
    "read_state",
    "set_step",
    "write_state",
]
