"""Saturation detector for buyer interviews — concept §4.3, §6.

Rule: a Sprint reaches saturation when the last N interviews surface no new themes.
The default threshold N=3 matches the concept's "three in a row" rule.

Library API:
    check_saturation(themes_by_interview: list[set[str]] | list[list[str]],
                     threshold: int = 3) -> SaturationStatus

CLI:
    python -m helpers.saturation [--threshold N] [--human] [path]
    # path is a JSON file: [["theme1", "theme2"], ["theme1"], ...]
    # If no path, reads JSON from stdin.
    # Exits 0 on success, 2 on invalid input.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SaturationStatus:
    saturated: bool
    consecutive_no_new: int
    threshold: int
    total_interviews: int
    new_themes_per_interview: tuple[int, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return {
            "saturated": self.saturated,
            "consecutive_no_new": self.consecutive_no_new,
            "threshold": self.threshold,
            "total_interviews": self.total_interviews,
            "new_themes_per_interview": list(self.new_themes_per_interview),
        }


def check_saturation(
    themes_by_interview: list[set[str]] | list[Iterable[str]],
    threshold: int = 3,
) -> SaturationStatus:
    """Determine whether the user has reached interview saturation.

    Each element of `themes_by_interview` is the set of themes that surfaced in
    that interview. A theme is "new" if it was not present in any earlier
    interview. The function returns a SaturationStatus carrying:

      - saturated: True iff the trailing `threshold` interviews each added zero
        new themes
      - consecutive_no_new: how many interviews from the end had zero new themes
      - new_themes_per_interview: per-interview count of new themes
    """
    if threshold <= 0:
        raise ValueError(f"threshold must be > 0, got {threshold}")

    seen: set[str] = set()
    new_counts: list[int] = []
    for raw in themes_by_interview:
        themes = set(raw)
        new = themes - seen
        new_counts.append(len(new))
        seen.update(themes)

    # Count consecutive interviews with zero new themes from the end.
    consecutive = 0
    for n in reversed(new_counts):
        if n == 0:
            consecutive += 1
        else:
            break

    saturated = consecutive >= threshold and len(new_counts) >= threshold

    return SaturationStatus(
        saturated=saturated,
        consecutive_no_new=consecutive,
        threshold=threshold,
        total_interviews=len(new_counts),
        new_themes_per_interview=tuple(new_counts),
    )


# ---------- CLI ----------


def _parse_input(arg: str | None) -> list[list[str]]:
    if arg is None:
        text = sys.stdin.read()
    else:
        p = Path(arg)
        if not p.exists():
            raise FileNotFoundError(arg)
        text = p.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("input must be a JSON array of arrays")
    out: list[list[str]] = []
    for i, row in enumerate(data):
        if not isinstance(row, list):
            raise ValueError(f"row {i} is not a list")
        out.append([str(t) for t in row])
    return out


def _render_human(status: SaturationStatus) -> str:
    lines = [
        f"Total interviews: {status.total_interviews}",
        f"Themes per interview (new only): {list(status.new_themes_per_interview)}",
        f"Consecutive interviews with no new themes (from end): {status.consecutive_no_new}",
        f"Threshold: {status.threshold}",
    ]
    if status.saturated:
        lines.append(
            f"Saturated: YES — last {status.threshold} interviews surfaced no new themes; "
            "consider stopping here."
        )
    else:
        remaining = max(0, status.threshold - status.consecutive_no_new)
        lines.append(
            f"Saturated: no — need {remaining} more no-new-theme interview(s) "
            "to hit the threshold."
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m helpers.saturation")
    parser.add_argument("path", nargs="?", help="JSON file with [[themes...], ...]; reads stdin if absent")
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Number of consecutive no-new-theme interviews required for saturation (default 3)",
    )
    parser.add_argument(
        "--human",
        action="store_true",
        help="Print human-readable output instead of JSON",
    )
    args = parser.parse_args(argv)

    try:
        rows = _parse_input(args.path)
    except FileNotFoundError as exc:
        print(f"error: file not found: {exc}", file=sys.stderr)
        return 2
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"error: invalid input: {exc}", file=sys.stderr)
        return 2

    try:
        status = check_saturation(rows, threshold=args.threshold)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.human:
        print(_render_human(status))
    else:
        print(json.dumps(status.to_dict()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
