# Gap Analysis — Mitchell Agentic Sprint vs Campaign-Mode + Six Animals

> **Phase C output** of the [research plan](research-plan.md). Maps MAS concept requirements against existing capability in `cgbarlow/campaign-mode` and `SimonMcCallum/six-animals` and identifies what must be built new.

## Method

Each MAS requirement is sourced from `docs/concept/concept.md`. For each, three columns:

- **Existing capability** — what campaign-mode or Six Animals gives us today, with file references
- **Gap** — what's missing or insufficient
- **How to close** — the concrete work, classified as *prompt-only* (re-use existing agents with new copy), *new SKILL.md* (new agent file), or *new code/state* (changes to commands or state schema)

## 1. Linear sequence enforcement (Q1)

| Aspect | Existing capability | Gap | How to close |
|---|---|---|---|
| Phase counter | `.campaign/quest.md` frontmatter has `phase: 1-6`; updated by command logic | Phase 1–6 in campaign-mode are *quest-themed* (Quest Definition, Character Setup, Execution, Guardian, Dragon, Debrief) and not strictly ordered (Council is optional and can fire mid-quest) | Replace phase model with `step: 1-6` named steps (Discovery, Vertical, Buyer Interviews, Framework, Competitor, Synthesis). New code/state. |
| Step completion gates | Guardian agent (`skills/guardian-agent/SKILL.md`) provides "approve / not yet / conditional" verdicts at checkpoints | Guardian's checkpoints are *user-invoked at any time*, not enforced as a precondition for advancing. MAS needs hard gates per step. | Wrap step transitions in a command that runs Guardian as a precondition. New code (one new command + state field `last_approved_step`). |
| Skip protection | None — campaign-mode trusts the user to advance phases sensibly | A user could run `/sprint-step-3` without completing 1 and 2 | Command guards check `last_approved_step ≥ N-1` before entering step N. New code. |
| Anchor to artifacts | `quest.md` has free-form Progress Log | MAS needs each step to declare *what artifact must exist before next step* (e.g., Step 2 outputs a Vertical Stack; Step 3 needs ≥15 interviews on file) | Per-step required-artifact list in state schema. New state. |

**Verdict on Q1:** Cannot be done by command rewrites alone. Requires new state fields and a new gate-checking command. ≈ 1 week of work.

## 2. Mini Council personas (Q2)

The five MAS Mini Council voices and their nearest existing analogues:

| MAS voice | Closest existing | Why partial | What's missing |
|---|---|---|---|
| Seed VC | Cat (risk) + Bear (strategy) | Cat flags risk; Bear articulates competitive position | Unit-economics heuristics, traction expectations, moat taxonomy ("workflow lock-in vs data flywheel vs proprietary AI"), 2026 AI-era investor lens (working demo, evals, inference economics — all called out in concept §6) |
| Churned customer | Cat (caution) + Puppy inverse | Cat warns of failure modes | Retrospective regret framing — "I paid and got burned" — is *post-purchase narrative*, not pre-purchase risk |
| Competitor founder | Cat + Bear | Cat maps threats; Bear positions | Market knowledge, competitive intelligence, knowledge of *gaps* in current offerings |
| Future-self-12-months | Owl (process) + Cat (unmitigated risks) | Owl tracks what was skipped | *Temporal hindsight* — "what did you regret not doing?" is a different orientation than present-tense risk assessment |
| Grumpy PM | Owl + Rabbit | Owl tracks timeline; Rabbit maps resources | *Pessimistic execution voice* — Owl/Rabbit are optimistic about clearing barriers; the Grumpy PM assumes barriers multiply |

**Verdict on Q2:** Profile packs *cannot* close this gap — profile packs only re-skin name/voice/emoji and cannot add domain heuristics or change evaluation logic (see `campaign-mode/docs/3_specs/SPEC-CM-009-A`). Each Council voice needs its own SKILL.md with embedded heuristics. **5 new SKILL.md files.** Each ≈ 1–2 days to draft + iterate against worked examples.

## 3. Step-specific intelligence (not in any existing framework)

Each of the 6 steps requires methodology that neither campaign-mode nor Six Animals encodes:

| Step | Methodology required | Source | Existing? |
|---|---|---|---|
| 1. Discovery | Founder profiling — unfair advantages, runway, vertical fit | Concept §4.1 | Generic mentor (Gandalf) provides framing only — no founder-fit heuristics |
| 2. Vertical | Vertical x sub-vertical x ICP x workflow x AI leverage stack | Concept §4.2 | None |
| 3. Buyer interviews | Mom Test discipline (banned hypothetical questions, costly-action signal detection, saturation rule) | Concept §4.3, §6 | None — new validator needed |
| 4. Framework | Named-expert discovery, framework adaptation (3 keep verbatim / 3 adapt) | Concept §4.4 | None — needs WebSearch + synthesis |
| 5. Competitor | Top-10 competitor analysis, positioning whitespace map | Concept §4.5 | None — needs WebSearch + scraping or user-provided URLs |
| 6. Synthesis | Three-artifact generation (sales deck, outreach plan, investor deck) | Concept §4.6 | None |

**Verdict:** This is the bulk of the new work. Roughly:
- Steps 1, 2 — prompt-only (new commands + Gandalf consultation pattern)
- Step 3 — needs a behavioral-interview validator (banned-question linter); prompt-only for the script generator
- Steps 4, 5 — need either WebSearch tooling or structured user-provided inputs; can start prompt-only with user-provided inputs and add tooling later
- Step 6 — prompt-only for markdown drafts; new code for slide rendering (PPTX/PDF)

## 4. State schema for named-step artifacts (Q4)

Current `.campaign/quest.md` schema:
```yaml
---
campaign-mode: Grow | Ship | Grow & Ship
phase: 1-6
created: YYYY-MM-DD
---
## Quest Narrative
## Success Criteria
## Anticipated Dragon
## Progress Log
```

MAS needs a multi-section schema that survives loopback (see §5). Proposed:

```yaml
---
sprint-mode: Solo | Coached
step: 1-6
last_approved_step: 0-6
attempt: 1-N        # increments on loopback
created: YYYY-MM-DD
---
## Builder Profile           # Step 1, persists across attempts
## Vertical Stack            # Step 2, replaced on loopback
### Backup Verticals
## Interview Log             # Step 3, transcripts at .sprint/interviews/
### Theme Map
### Costly-Action Signals
## Expert Framework          # Step 4, persists across attempts
## Competitor Map            # Step 5
### Positioning Whitespace
## Artifacts                 # Step 6
### Sales Deck path
### Outreach Plan path
### Investor Deck path
## Loopback Log              # records each attempt's vertical + reason for loopback
## Progress Log              # reused from campaign-mode
```

**Verdict on Q4:** Schema must be rewritten — quest.md is too thin. Loopback is supportable *if and only if* Builder Profile and Expert Framework persist across attempts (the concept explicitly says these are reusable; only Vertical Stack and downstream is replaced). New state schema doc + a small migration helper. ≈ 2 days.

## 5. Loopback semantics (Q4 cont'd)

Concept requirement (§7): on validation failure (no costly action found, scorecard < 65, no whitespace), loop back to Step 1 *retaining* user profile, interview themes, and framework knowledge — only the disqualified vertical and downstream is discarded.

| Aspect | Existing capability | Gap | How to close |
|---|---|---|---|
| "Not yet" handling | Guardian's "not yet" verdict comes with feedback and lets user iterate within the same step | MAS loopback is *cross-step* — fail Step 3, restart Step 2 with new vertical | New command `/sprint-loopback` that resets `last_approved_step` to 1 and clears Step 2+ sections while preserving Step 1 + accumulated themes |
| Three loopback flavours | None | Concept names three: different ICP same vertical / different vertical adjacent skills / different workflow same vertical | Each is a different reset depth — encode in the loopback command |
| Cost-of-no | Concept emphasizes "make a no cheap" | Campaign-mode's Dragon Prevails verdict is final-stage only | Per-step early-no handling — interview Saturation detection in Step 3 should fire loopback automatically when no costly-action signals after N interviews |

**Verdict on Q4:** Loopback is genuinely new logic. Roughly 1 week of work including the saturation detector for Step 3.

## 6. Anti-sycophancy enforcement (Q5)

Concept §6 makes this the headline product promise. Two questions: (a) where does it live, (b) how do we prove it's working.

| Layer | Existing capability | Gap | How to close |
|---|---|---|---|
| Voice/tone | Dragon already enforces "no encouragement, no warmth, no hedging" (`skills/dragon-agent/SKILL.md` lines 88–96) | Dragon is *one* agent at the *end* of a quest. MAS needs adversarial posture in *every* step prompt | Reuse Dragon's tone guidance verbatim in each new SKILL.md and step command preamble. Prompt-only. |
| Behavioural enforcement | None | Mom Test discipline (banned hypothetical questions in interview script) | Banned-question linter — regex/LLM check on generated interview scripts. Small new code. |
| Verification | None | "Does the model actually push back, or does it flatter under pressure?" | Eval set: 20–30 prompts where the user is wrong, and the expected response is pushback. Run before each release. New work, classified as test infrastructure. |
| Council adversarial fidelity | Dragon evaluates work product; Guardian gates progression | Mini Council needs to *attack* the user's reasoning at Step 1→2 and Step 4→5 boundaries | New Council orchestration: invoke each of the 5 voices in sequence, each receiving the same context, each producing one strongest critique. Aggregate, present to user. New code (one new command). |

**Verdict on Q5:** Tone is prompt-only via Dragon-style preambles. *Verification* requires an eval set — that's an Extensive-tier deliverable, not Moderate-tier. The Mini Council orchestration command is moderate-tier, ≈ 3 days of work after the 5 voices exist.

## 7. Final artifact generation (Q3)

Three Step 6 outputs:

| Artifact | Prompt-only feasibility | When tooling becomes necessary |
|---|---|---|
| Sales deck (6–8 slides) | High — markdown can carry slide-per-section structure with headlines + speaker notes; user pastes into their own slide tool | If user wants a `.pptx` or `.pdf` directly. PPTX generation via `python-pptx` is well-trodden. |
| Customer outreach plan | High — markdown sections (re-engagement messages, target list, sequence). The hard part is *retrieving* who to re-engage; that's solved by the Interview Log persisting across attempts | None until we want CRM integration |
| Pre-seed investor deck (12 slides) | Medium — the *structure* is prompt-only; the *evidence* (interview tape, evals, inference economics) requires real inputs from prior steps. If those inputs are missing, the prompt should refuse to pad rather than fabricate | Slide rendering as above. Also: VC-grade decks usually need a designer pass — out of scope. |

**Verdict on Q3:** Markdown-first artifacts close 80% of the value. Slide rendering is genuinely optional for v1 — it's polish, not core. Tooling is *not* on the critical path until users specifically demand it.

### 7a. NotebookLM as a synthesis layer (Q3 augmented)

Per Issue #1 comment, evaluating Google NotebookLM as an artifact / synthesis layer. Findings as of May 2026:

| Access path | Status | Fit for MAS |
|---|---|---|
| Google Cloud **NotebookLM Enterprise API** (released Sep 2025) | Official, supports notebook CRUD, source management, audio overview generation, queries. Workspace/Enterprise customers only — not consumer. | Viable for organisations on Google Workspace Enterprise. Adds Google Cloud auth surface to MAS. |
| Unofficial Python API + CLI (`tmc/nlm`, `notebooklm-cli`, `notebooklm-py`) | Active community projects; cookie-based auth via dedicated browser profile | Lowest-friction for individual builders. Per-user authentication; rate-limit and ToS risk. |
| MCP servers (`PleasePrompto/notebooklm-mcp`, `julianoczkowski/notebooklm-mcp-2026`, `roomi-fields/notebooklm-mcp`) | Multiple actively maintained; designed for Claude Code, Claude Desktop, Cursor, VS Code. As of Jan 2026 the CLI + MCP merged into a single `nlm` package | **Strongest fit** — MAS as a Claude Code plugin can declare an optional MCP dependency. User installs the MCP server; MAS skills invoke NotebookLM tools through it. |

**What NotebookLM can do that's directly relevant to MAS:**

- **Step 3 (Buyer interviews)** — Drop interview transcripts into a notebook; ask for theme map, saturation analysis, costly-action signal extraction. NotebookLM's source-grounding posture aligns with the "verbatim quotes only" rule (concept §6).
- **Step 4 (Framework)** — Drop the chosen expert's books/courses/interview transcripts in; ask for "summarise their framework, identify 3 to keep verbatim and 3 to adapt for our ICP".
- **Step 5 (Competitor)** — Drop top-10 competitor websites/case studies in; ask for clustering and positioning whitespace map.
- **Step 6 (Synthesis)** — Drop everything in; generate audio overview (10-min podcast briefing for the founder pre-VC meeting), mind map of the validated thesis, briefing doc that complements the three written artifacts. **Not a slide renderer** — NotebookLM does not output PPTX. It outputs prose, audio, and visual maps.

**What NotebookLM cannot do for MAS:**

- Replace the Mini Council adversarial logic (NotebookLM is grounded but not adversarial-by-default)
- Replace the Mom Test linter (NotebookLM doesn't enforce interview methodology)
- Render `.pptx` slides — slide rendering remains a separate question
- Run inside a fully self-contained Claude Code plugin without external auth (cookie or OAuth)

**Auth/coupling friction:**

- Cookie-based auth (unofficial CLI/MCP): user logs into Google in a dedicated browser profile, cookies are extracted, login persists. Friction at first run, smooth thereafter. ToS risk if Google blocks unofficial automation.
- Enterprise API: requires Google Workspace Enterprise + GCP project + service account. High friction for individual builders; appropriate for organisational deployments.

**Verdict on Q3 augmented:** NotebookLM is a serious option for Steps 3–6 *synthesis*, particularly via MCP. It does **not** eliminate the slide-rendering question (NotebookLM doesn't produce PPTX) but it *does* replace much of the Extensive-tier theme clustering + web research tooling with a single integration. Treated as a tier-bridging option below.

## Cross-cutting: what we get for free

These campaign-mode capabilities are reusable as-is, no work needed:

- Conversation transcripts (`.campaign/conversations/{date}-{agent}.md` verbatim record) — **directly serves the verbatim-quote requirement in Concept §6**
- Progress Log format and triggers
- AskUserQuestion presentation rules (one question, context summary)
- Profile system (light skinning of NPCs even if we don't use it for the Council)
- Six Animals as advisory layer for the user's *team thinking* (orthogonal to the Mini Council)

## Summary — what must be built

Classified by type of work:

**New SKILL.md files (5):**
- `seed-vc-agent/SKILL.md`
- `churned-customer-agent/SKILL.md`
- `competitor-founder-agent/SKILL.md`
- `future-self-agent/SKILL.md`
- `grumpy-pm-agent/SKILL.md`

**New commands (≈ 8):**
- `/sprint-setup` (bootstraps `.sprint/` directory)
- `/sprint-start` (Step 1 entry)
- `/sprint-step-N` (one each for steps 2–6, gated on prior-step approval)
- `/sprint-council` (Mini Council orchestration; runs at Step 1→2 and Step 4→5 transitions)
- `/sprint-loopback` (resets to Step 1 with retained context)
- `/sprint-continue` (re-entry)

**New state schema:**
- `.sprint/sprint.md` (replaces `.campaign/quest.md` shape)
- `.sprint/interviews/{N}-{interviewee-pseudonym}.md` per buyer interview

**New code (lightweight):**
- Banned-hypothetical-question linter for interview scripts
- Saturation detector for Step 3 (count themes-since-last-new-theme)

**New code (heavy, only in Extensive tier):**
- Slide rendering (PPTX/PDF)
- WebSearch + scrape for expert and competitor discovery
- Theme clustering for the saturation detector beyond simple count
- Anti-sycophancy regression eval

**Optional integration (tier-bridging, see §7a):**
- NotebookLM via MCP — replaces much of the heavy tooling above for Steps 3–6 synthesis, at the cost of an external auth surface and Google dependency

**Pure prompt engineering (no code):**
- Step 1–6 command prompts
- Mini Council voice prompts (within their SKILL.md files)
- Anti-sycophancy preambles (lifted from Dragon)
- Artifact templates (sales deck, outreach plan, investor deck)

## Map to research questions

| Q | Question | Answer | Confidence |
|---|---|---|---|
| Q1 | Sequence fit | Requires schema + new gate command — not pure rewrite, but not a fork either | High |
| Q2 | Mini Council depth | Profile packs insufficient; need 5 new SKILL.md files | High |
| Q3 | Artifact reach | Markdown-first closes 80%; slide rendering is optional | High |
| Q4 | Loopback semantics | Schema rewrite + 1 new command | High |
| Q5 | Anti-sycophancy | Tone prompt-only; verification needs eval set (Extensive tier only) | Medium — verification claim untested |
| Q6 | Distribution | **Open — needs user input** | n/a |
| Q7 | Ownership | **Open — needs user input** | n/a |

Q6 and Q7 are addressed in the [recommendation](RECOMMENDATION.md) where build-tier choice depends on user answers.
