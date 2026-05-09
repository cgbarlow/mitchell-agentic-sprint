# SPEC-008-A: Behavioural-Interview Linter Rules

| Field | Value |
|-------|-------|
| **Specification ID** | SPEC-008-A |
| **Parent ADR** | [ADR-008](../ADR-008-Anti-Sycophancy-Approach.md) |
| **Version** | 1.0 |
| **Status** | Active |
| **Last Updated** | 2026-05-09 |

---

## Overview

Defines the rules and matching semantics for `helpers/interview_validator.py` — the Mom Test linter that catches hypothetical questions, opinion solicitations, leading questions, and pricing speculation in Step 3 buyer-interview scripts before the user runs the interview.

The linter is **deterministic** (pure regex; no LLM) for v0.1.0. The library API and the `python -m helpers.interview_validator` CLI both produce the same output: a list of `LintResult` per question, each containing zero or more `LintViolation` records.

## Public API

```python
from helpers.interview_validator import lint_question, lint_script, LintResult, LintViolation

result: LintResult = lint_question("Would you use a tool that automates X?")
# result.is_clean is False
# result.violations contains a LintViolation with rule="hypothetical-would-you"

results: list[LintResult] = lint_script([
    "Would you use a tool that automates X?",
    "Walk me through the last time you ran into this problem.",
])
# results[0].is_clean is False
# results[1].is_clean is True
```

## CLI

```
$ python -m helpers.interview_validator script.txt
script.txt:1: hypothetical-would-you — "Would you use…" speculates about future behaviour
script.txt:2: ✓
exit code: 1 (some violations found)
```

When invoked with no arguments, reads questions from stdin, one per line.

Exit codes:
- `0` — all questions clean
- `1` — at least one violation
- `2` — invalid input (e.g. file not found)

## Rule registry

Each rule has:
- `name` (kebab-case identifier)
- `pattern` (compiled regex; `re.IGNORECASE`)
- `explanation` (one-line human-readable)
- `category` (`hypothetical | opinion | leading | pricing-speculation | future-tense`)

| Rule | Pattern (informal) | Explanation |
|---|---|---|
| `hypothetical-would-you` | `\bwould\s+(?:you|your\s+\w+)\s+(?!have\s+\w+ed)` | "Would you…" projects future behaviour; ban unless followed by past-tense ("Would you have done…") |
| `hypothetical-do-you-think` | `\bdo\s+you\s+think\b` | Solicits opinion; not behaviour |
| `hypothetical-if` | `\bif\s+(?:you|we|they)\s+(?:had|could|were|would)\b` | Counterfactual hypothetical |
| `hypothetical-future-tense` | `\bwill\s+you\b` | Future-tense projection |
| `pricing-speculation` | `\bhow\s+much\s+would\s+you\s+pay\b` | Hypothetical pricing — buyers cannot accurately price hypothetical products |
| `pricing-future` | `\bwhat\s+would\s+(?:it|that)\s+be\s+worth\b` | Variant of hypothetical pricing |
| `opinion-do-you-like` | `\bdo\s+you\s+like\b` | Pure opinion solicitation |
| `opinion-would-it-be-useful` | `\bwould\s+(?:it|this|that)\s+be\s+(?:useful|helpful|valuable)\b` | Leads to social-desirability bias |
| `leading-dont-you-think` | `\bdon't\s+you\s+think\b` | Strongly leading |
| `leading-wouldnt-it` | `\bwouldn't\s+it\s+be\b` | Strongly leading |
| `commitment-fishing` | `\bwould\s+you\s+(?:buy|use|adopt|switch\s+to)\b` | Hypothetical commitment — buyers say yes to be polite, never act |
| `validation-seeking` | `\bdoes\s+that\s+make\s+sense\b` | Validation-seeking; flags an interviewer who is leading rather than listening |

## Permitted question patterns (informational, not enforced)

The linter does not certify that a question is **good** — only that it is not **obviously bad**. The Step 3 command's prompt instructs Gandalf and the interview-script generator to favour these patterns:

- "Walk me through the last time…"
- "What do you currently do when…"
- "How did you handle… last week / last month?"
- "Have you ever paid for…?"
- "What did you spend on… last quarter?"
- "Who else have you talked to about this?"
- "Tell me about the workaround you built."

These are about past behaviour and costly action. They are not enforced positively (a script can pass the linter without any of them) — but the command's prompt insists on them.

## Output format

```python
@dataclass(frozen=True)
class LintViolation:
    rule: str            # rule name, e.g. "hypothetical-would-you"
    explanation: str     # one-line human-readable
    category: str        # category from the table above
    span: tuple[int, int]  # char range in the question (start, end)

@dataclass(frozen=True)
class LintResult:
    question: str
    violations: tuple[LintViolation, ...]

    @property
    def is_clean(self) -> bool:
        return len(self.violations) == 0
```

## False-positive handling

Some legitimate questions may match a rule (e.g., "Would you have a moment to walk me through…" matches `hypothetical-would-you` but is procedural). The linter flags but does not silently filter — the user (or the calling command) decides whether to override.

The Step 3 command surfaces violations to the user with the rule name and explanation. The user can:
- Accept the linter's verdict and ask for a re-generated question
- Override with explicit acknowledgement ("This is procedural, not hypothetical — keep")
- Ignore (not recommended)

False-positive rate is a known risk per the build plan. SPEC-008-A v1.1 may tune the patterns based on tester feedback at the Phase 3 gate.

## Future work (v0.2.0+)

Not in v0.1.0:

- **LLM-based judge** — an optional layer that runs each question through an LLM with a prompt asking "is this question hypothetical, leading, or opinion-based?" Gated by an environment variable (`MAS_LLM_LINTER=1`); fails open when no LLM is configured. Layered on top of the regex registry, not replacing it.
- **Per-vertical rule extensions** — some verticals have legitimate "would you" patterns (e.g., medical "would you describe yourself as…"). Per-vertical override files in `.sprint/linter-overrides/`.
- **Auto-rewrite suggestions** — given a violating question, propose a behavioural rewrite. Requires LLM.

## Acceptance criteria

This spec is fulfilled when:
- Every rule in the table above is implemented in `RULES` in `helpers/interview_validator.py`
- Each rule has at least one true-positive test case (a question that should match) and one true-negative (a question that should not match)
- `lint_script` returns one `LintResult` per input question, in order
- The CLI (`python -m helpers.interview_validator`) reads from a file or stdin and prints one diagnostic per violation
- The CLI exits 0 when clean, 1 when violations, 2 when input is invalid
- All tests pass under pytest (Protocol 3) with no mocks (Protocol 8)
