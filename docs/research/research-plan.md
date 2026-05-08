# Research Plan — Mitchell Agentic Sprint

> **Issue:** [cgbarlow/mitchell-agentic-sprint#1](https://github.com/cgbarlow/mitchell-agentic-sprint/issues/1) — *Research: review concept docs and supporting frameworks and provide options*
>
> **Scope of this plan:** the *plan for the research effort*, not the research itself. The deliverable of executing this plan is a written recommendation on how to build MAS, not the build itself.

## Context

Scott Mitchell has authored the concept for **Mitchell Agentic Sprint (MAS)** — an AI-led product that walks an "AI-strong builder" through six sequential steps to take a single idea from rough notion to investor-conversation-ready: Discovery → Vertical → Buyer interviews → Framework/expert research → Competitor/positioning → Sales deck + outreach plan + pre-seed investor deck. Concept doc: `docs/concept/concept.md`.

Distinctive design constraints from the concept:
- **Adversarial-by-default** (anti-sycophancy is the explicit headline posture)
- **Behavioral over hypothetical** in interview generation (banned questions, costly-action signal tracking)
- **Saturation over headcount** for stopping interviews
- **Loopback on validation failure** that *retains learning* across attempts (different ICP / different vertical / different workflow)
- **Mini Council** — 5 skeptical personas (seed VC, churned customer, competitor founder, future-self-12-months, grumpy PM) tear up the idea between Steps 1→2 and 4→5
- **Output is artifacts, not product** — MAS does not build the app or the website

The user's stated thesis is that `cgbarlow/campaign-mode` (already cloned at `/workspaces/workspace-basic/campaign-mode/`) could host MAS. Campaign-mode is itself a Claude Code plugin built on the Six Animals framework, with quest-shaped multi-agent orchestration (Gandalf/Dragon/Guardian + 6 animal advisors).

## What we already know (Phase 1 results)

Two Explore passes were run this session — see findings below. Headlines:

**Campaign-mode is structurally suitable, but quest-shaped:**
- Plugin model is generic — new commands and skills register by file convention; no proprietary registration.
- Commands (`/start-quest`, `/continue-quest`, `/council`, `/campaign-setup`) are domain-agnostic in mechanism but quest-themed in copy. Renaming/repurposing is possible without forking.
- `.campaign/quest.md` state schema is narrative-flexible — accommodates a 6-step pipeline with named artifacts.
- Profile packs (`profile-packs/`) skin agents narratively (name/voice/emoji) but **cannot reshape evaluation logic**. New domain-knowledgeable personas need new SKILL.md files.
- Gandalf/Dragon/Guardian core roles are reusable as-is for "framing", "adversarial test", and "step gate" respectively.
- Conversation transcripts and progress logging infrastructure are reusable for verbatim buyer-interview capture.
- Phase ordering is enforced in command logic — strict 6-step linear sequence requires forking the four commands or wrapping them.

**Six Animals offers collaborative critique, not domain expertise:**
- The six archetypes (Bear/Cat/Owl/Puppy/Rabbit/Wolf) are *behavioral/psychological* (McClelland needs theory + Self-Determination Theory). MAS Mini Council voices are *expert + emotional + temporal*.
- Five of six animals naturally resist groupthink (Cat especially), but adversarial bite comes from campaign-mode's Dragon, not Six Animals.
- Profile-pack skinning of animals to MAS Council voices is possible but thin — the Seed VC needs unit-economics heuristics; the Churned Customer needs retrospective-regret framing; the Competitor Founder needs market knowledge — none of which Six Animals encodes.

**Verdict on the thesis:** campaign-mode + Six Animals get us ~70% of the way. The remaining 30% is genuinely new: linear-sequence enforcement, domain-knowledgeable Mini Council agents, behavioral-interview validation, loopback state handling, and concrete artifact generators.

## Research questions

The research effort exists to answer these questions with enough confidence to commit to a build approach:

1. **Sequence fit** — Can campaign-mode's phase model host a strict linear 6-step pipeline through command rewrites only, or is forking required?
2. **Mini Council depth** — Can the 5 skeptical personas be implemented as profile-packs over existing agents, or do they need new SKILL.md NPCs with domain heuristics?
3. **Artifact reach** — How far can prompt-driven Claude alone get on the three final outputs (sales deck, outreach plan, investor deck)? Where does external tooling become necessary (slide rendering, theme clustering, web research, scraping)?
4. **Loopback semantics** — Does retain-learning-across-attempts require schema changes to `.campaign/quest.md`, or can it ride existing infrastructure?
5. **Anti-sycophancy enforcement** — Is prompt-level adversarial framing sufficient, or do we need a regression eval set per step?
6. **Distribution** — Claude Code plugin, Claude Desktop plugin, Cursor extension, standalone web product, or hybrid? Affects all other choices.
7. **Ownership** — Is this Chris-built solo, Chris+Scott, or contracted? Affects scope realism.

## Approach (research execution phases)

| Phase | Activity | Output | Status |
|-------|----------|--------|--------|
| **A** | Read concept doc + supporting frameworks | Notes | ✅ done this session |
| **B** | Map campaign-mode + Six Animals extension surface | Two Explore reports (above) | ✅ done this session |
| **C** | Gap analysis — write up what MAS needs that neither framework provides, mapped to Q1–Q5 | `docs/research/gap-analysis.md` in mitchell-agentic-sprint repo | Not started |
| **D** | Build options writeup — flesh out the three options below with effort, risks, dependencies | `docs/research/build-options.md` | Not started |
| **E** | (Optional) Spike — implement Step 1 (Discovery) end-to-end on the moderate option to de-risk the new-NPC pattern and the loopback flow | Working branch + spike report | Decision point |
| **F** | Recommendation — single ADR-style doc selecting one option with rationale | `docs/research/RECOMMENDATION.md` | Not started |

Phases A–B are effectively complete. Phases C, D, F are documentation; Phase E is the only optional engineering work and is gated by the user's appetite for de-risking before commitment.

## The three build options the research evaluates

### Minimum — Profile-pack-themed sibling plugin

**Shape:** A new Claude Code plugin, `mitchell-agentic-sprint`, that depends on `campaign-mode` and `six-animals`. Adds two commands: `/sprint-start`, `/sprint-continue`. Steps 1–6 are inline prompts inside those commands. Mini Council is 5 profile-packs that re-skin Cat/Bear/Dragon as the 5 voices. State stored at `.sprint/sprint.md` mirroring `quest.md`.

**Reuses:** Gandalf (Step 1 framing), Dragon (Step 6 confrontation), Guardian (step gates), all six animals (advisory layer), conversation transcripts, progress logging.

**Builds new:** 2 commands, 5 profile packs, state schema doc, 3 markdown artifact templates.

**Effort:** ~2 weeks for one engineer.

**Acceptance bar:** A friendly tester can complete the 6 steps end-to-end and walk out with usable (not investor-grade) markdown artifacts.

**Risks:**
- Mini Council voices feel thin without domain heuristics (Q2)
- Investor deck may not be defensible against a real seed VC (Q3)
- Sequence enforcement is by convention, not code — easy to skip steps

### Moderate — New NPC agents + step gates + loopback

**Shape:** Same sibling-plugin shape, but adds 5 new SKILL.md NPCs (Seed-VC, Churned-Customer, Competitor-Founder, Future-Self, Grumpy-PM) each with embedded domain heuristics. Step-specific Guardian variants enforce step gates. Explicit loopback handler retains user profile + themes + expert knowledge across attempts. Behavioral-interview validator (banned-question linter) enforces Mom Test discipline. Markdown artifact generators for the three Step 6 outputs.

**Reuses:** Gandalf, Dragon, Guardian (as variant base), six animals, transcripts, progress logging.

**Builds new:** 5 NPC SKILL.md files, 6 step-gate variants, loopback state handler, interview validator, 3 artifact generators, ~3 worked-example sprints in `docs/examples/`.

**Effort:** ~6–8 weeks for one engineer.

**Acceptance bar:** A tester reaches genuinely investor-conversation-ready artifacts; Mom Test discipline is enforced, not just suggested.

**Risks:**
- Domain heuristics for the 5 voices need iteration with real users (Q2)
- Outreach drafts will need human polish — not a one-shot
- Some campaign-mode upstream changes may break our extensions

### Extensive — Pipeline-shaped fork with tooling

**Shape:** Fork campaign-mode (or stand up a new repo with no dependency) and rebuild around an explicit step-pipeline state schema. Add web research tooling for expert and competitor discovery (WebSearch + light scraping + synthesis). Theme map with saturation detection (cluster interview transcripts, detect "three in a row no new themes"). Slide-format outputs (PPTX or PDF). Anti-sycophancy regression eval set per step. Outreach drafter that pulls from interview history for re-engagement messages. Sales Navigator filter generator.

**Reuses:** Selected campaign-mode patterns (transcripts, isolation rules) ported by hand.

**Builds new:** Everything in Moderate, plus the tooling layer above. Likely a small TypeScript or Python service backing the slash commands.

**Effort:** ~12–16 weeks for one engineer.

**Acceptance bar:** Investor-grade slide artifacts; verified anti-sycophancy via eval; theme saturation detection working on real interview transcripts.

**Risks:**
- Scope creep on slide rendering (template fidelity, branding, formats)
- Eval fidelity — measuring sycophancy is itself a research problem
- Maintaining a fork loses upstream benefits from campaign-mode evolution

## Recommendation (provisional, pending Phases C–F)

The honest answer is **Moderate**, with an explicit *Minimum-first walking skeleton* delivered in week 1 and used as the demo for soliciting user feedback before committing the remaining 5–7 weeks.

Rationale: Minimum is too thin to deliver the concept's headline promise (anti-sycophancy + investor-grade artifacts). Extensive front-loads tooling that may not be the bottleneck — Scott's concept itself flags that "the anti-sycophancy posture might feel harsh" and "AI may not catch the moment a builder is bullshitting themselves" as open questions. Those are validated through users, not through more tooling. Moderate gives us the shape needed to put it in front of testers; we add Extensive-tier tooling only if specific tests demand it.

This recommendation is *provisional* and the research's job is to confirm or overturn it.

## Critical files and locations

**Read during research:**
- `/workspaces/workspace-basic/mitchell-agentic-sprint/docs/concept/concept.md` — concept (read)
- `/workspaces/workspace-basic/campaign-mode/CLAUDE.md` — conventions (read)
- `/workspaces/workspace-basic/campaign-mode/skills/{gandalf,dragon,guardian}-agent/SKILL.md` — NPC shapes
- `/workspaces/workspace-basic/campaign-mode/commands/*.md` — command shapes
- `/workspaces/workspace-basic/campaign-mode/profile-packs/` — profile pack format
- `/workspaces/workspace-basic/campaign-mode/docs/3_specs/SPEC-CM-009-A-Profile-Pack-Format.md`
- `/workspaces/workspace-basic/campaign-mode/docs/3_specs/SPEC-CM-012-A-*` — transcript protocol
- `/workspaces/workspace-basic/six-animals/skills/{bear,cat,owl,puppy,rabbit,wolf,simon}-agent/SKILL.md` — animal shapes

**Written during research (in mitchell-agentic-sprint repo):**
- `docs/research/gap-analysis.md` — Phase C output
- `docs/research/build-options.md` — Phase D output (the three options, expanded)
- `docs/research/spike-report.md` — Phase E output, if performed
- `docs/research/RECOMMENDATION.md` — Phase F output (the deliverable)

## Verification — how we know the research is done

The research is complete when the recommendation doc:
1. Names a single chosen option (Min / Mod / Ext)
2. Answers each of the seven research questions with evidence
3. Lists the next 3–5 concrete actions to start the build (with owners and rough sizing)
4. Identifies the open questions that *cannot* be resolved by research and must be answered by user testing

If a spike is performed (Phase E), the spike report must additionally show:
- One Step 1 (Discovery) flow runnable end-to-end
- Demonstrated loopback (a deliberately-failed validation that recovers prior context)
- One Mini Council persona invoked with domain heuristics, evaluated for adversarial fidelity (does it actually push back, or does it flatter?)

## Open questions for the user (please answer in PR review)

1. **Distribution channel** — Claude Code plugin? Claude Desktop plugin? Cursor extension? Standalone? (Affects everything downstream.)
2. **Spike or paper-only?** — Should research include Phase E (1 week of code), or stop at Phase F (documentation only)?
3. **Time budget** — Is there a deadline on the build? On the research?
4. **Coupling tolerance** — Are you OK with a hard `campaign-mode` dependency, or do you want MAS to stand alone for licensing/distribution reasons?
5. **v1 user persona** — Your immediate AI-builder network (5–20 people) or general-public AI-builders (which raises the polish bar significantly)?
6. **Scott's involvement** — Is Scott reviewing artifacts as we go (high-fidelity loop) or shipping you the concept and waiting for v1 (low-fidelity loop)?

## Out of scope for the research

- Implementing MAS (that's the build, downstream of this research)
- User interviews with target builders (that's user research, separate workstream)
- Branding, naming, visual design
- Competitive product analysis (Greg Isenberg's Startup Empire, AI-builder accelerators, etc.)
- Pricing / commercial model (the concept itself states v1 is not commercial)
