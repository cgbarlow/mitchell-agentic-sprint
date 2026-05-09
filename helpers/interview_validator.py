"""Mom Test linter for buyer-interview scripts — see SPEC-008-A.

Deterministic regex-based check. Each rule pairs a compiled regex with a
human-readable explanation. Pure-Python; no LLM, no external deps beyond stdlib.

Library API:
    lint_question(q: str) -> LintResult
    lint_script(qs: list[str]) -> list[LintResult]

CLI:
    python -m helpers.interview_validator [path]
    python -m helpers.interview_validator             # reads stdin
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

VALID_CATEGORIES = frozenset(
    {
        "hypothetical",
        "opinion",
        "leading",
        "pricing-speculation",
        "future-tense",
        "commitment-fishing",
        "validation-seeking",
    }
)


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    explanation: str
    category: str


@dataclass(frozen=True)
class LintViolation:
    rule: str
    explanation: str
    category: str
    span: tuple[int, int]


@dataclass(frozen=True)
class LintResult:
    question: str
    violations: tuple[LintViolation, ...]

    @property
    def is_clean(self) -> bool:
        return len(self.violations) == 0


def _r(name: str, pattern: str, explanation: str, category: str) -> Rule:
    if category not in VALID_CATEGORIES:
        raise ValueError(f"invalid category {category!r}")
    return Rule(
        name=name,
        pattern=re.compile(pattern, re.IGNORECASE),
        explanation=explanation,
        category=category,
    )


# Order matters only for human readability — every rule is checked independently.
RULES: tuple[Rule, ...] = (
    # NOTE: hypothetical-would-you uses negative lookahead to allow past-tense
    # framings like "Would you have used …" through.
    _r(
        "hypothetical-would-you",
        r"\bwould\s+you(?:r\s+\w+)?\s+(?!have\b)",
        '"Would you…" speculates about future behaviour. Ask about past behaviour instead.',
        "hypothetical",
    ),
    _r(
        "hypothetical-do-you-think",
        r"\bdo\s+you\s+think\b",
        '"Do you think…" solicits opinion, not behaviour.',
        "opinion",
    ),
    _r(
        "hypothetical-if",
        r"\bif\s+(?:you|we|they)\s+(?:had|could|were|would)\b",
        "Counterfactual hypothetical. Ask what actually happened.",
        "hypothetical",
    ),
    _r(
        "hypothetical-future-tense",
        r"\bwill\s+you\b",
        '"Will you…" projects future behaviour. Ask what already happened.',
        "future-tense",
    ),
    _r(
        "pricing-speculation",
        r"\bhow\s+much\s+would\s+you\s+pay\b",
        "Hypothetical pricing — buyers cannot accurately price products they have not bought.",
        "pricing-speculation",
    ),
    _r(
        "pricing-future",
        r"\bwhat\s+would\s+(?:it|that|this)\s+be\s+worth\b",
        "Hypothetical valuation. Ask about historical spend on the workaround.",
        "pricing-speculation",
    ),
    _r(
        "opinion-do-you-like",
        r"\bdo\s+you\s+like\b",
        "Pure opinion solicitation — invites politeness, not signal.",
        "opinion",
    ),
    _r(
        "opinion-would-it-be-useful",
        r"\bwould\s+(?:it|this|that)\s+be\s+(?:useful|helpful|valuable)\b",
        '"Would it be useful…" leads to social-desirability bias.',
        "opinion",
    ),
    _r(
        "leading-dont-you-think",
        r"\bdon'?t\s+you\s+think\b",
        "Strongly leading — primes the answer.",
        "leading",
    ),
    _r(
        "leading-wouldnt-it",
        r"\bwouldn'?t\s+it\s+be\b",
        "Strongly leading — primes the answer.",
        "leading",
    ),
    _r(
        "commitment-fishing",
        r"\bwould\s+you\s+(?:buy|use|adopt|switch\s+to|sign\s+up\s+for)\b",
        "Hypothetical commitment — buyers say yes to be polite, never act on it.",
        "commitment-fishing",
    ),
    _r(
        "validation-seeking",
        r"\bdoes\s+that\s+make\s+sense\b",
        "Validation-seeking — flags an interviewer who is leading rather than listening.",
        "validation-seeking",
    ),
)


def lint_question(question: str) -> LintResult:
    """Apply every rule in RULES to one question. Returns LintResult."""
    violations: list[LintViolation] = []
    for rule in RULES:
        for match in rule.pattern.finditer(question):
            violations.append(
                LintViolation(
                    rule=rule.name,
                    explanation=rule.explanation,
                    category=rule.category,
                    span=(match.start(), match.end()),
                )
            )
    return LintResult(question=question, violations=tuple(violations))


def lint_script(questions: list[str]) -> list[LintResult]:
    """Lint a list of questions in order; returns one LintResult per question."""
    return [lint_question(q) for q in questions]


# ---------- CLI ----------


def _format_violation(source: str, lineno: int, q: str, v: LintViolation) -> str:
    return f"{source}:{lineno}: {v.rule} — {v.explanation}"


def _read_questions(arg: str | None) -> tuple[list[str], str]:
    """Returns (questions, source-label). Raises FileNotFoundError if path missing."""
    if arg is None:
        return ([line.rstrip("\n") for line in sys.stdin if line.strip()], "<stdin>")
    p = Path(arg)
    if not p.exists():
        raise FileNotFoundError(arg)
    lines = p.read_text(encoding="utf-8").splitlines()
    # Keep blank lines as None so line numbers stay accurate? We'll filter blanks
    # but track original line numbers via enumerate over the full list.
    return ([(line if line.strip() else "") for line in lines], str(p))


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) > 1:
        print("usage: python -m helpers.interview_validator [path]", file=sys.stderr)
        return 2
    arg = argv[0] if argv else None
    try:
        questions, source = _read_questions(arg)
    except FileNotFoundError as exc:
        print(f"error: file not found: {exc}", file=sys.stderr)
        return 2

    any_violation = False
    for idx, q in enumerate(questions, start=1):
        if not q.strip():
            continue
        result = lint_question(q)
        if result.is_clean:
            print(f"{source}:{idx}: ✓")
        else:
            for v in result.violations:
                any_violation = True
                print(_format_violation(source, idx, q, v))
    return 1 if any_violation else 0


if __name__ == "__main__":
    sys.exit(main())
