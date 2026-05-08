# Build Options — Mitchell Agentic Sprint

> **Phase D output** of the [research plan](research-plan.md). Three concrete build approaches, evaluated against the [gap analysis](gap-analysis.md). The [recommendation](RECOMMENDATION.md) selects one.

## At a glance

| | **Minimum** | **Moderate** | **Extensive** |
|---|---|---|---|
| Shape | Sibling plugin riding campaign-mode + six-animals | Same shape + 5 new NPC agents + step gates + loopback | Forked or standalone, plus tooling layer |
| Effort | ~2 weeks (1 engineer) | ~6–8 weeks (1 engineer) | ~12–16 weeks (1 engineer) |
| New SKILL.md files | 0 (uses profile packs) | 5 (Mini Council voices) | 5+ (plus possible step-specialist agents) |
| New commands | 2 | ~8 | ~8 + tooling commands |
| New state schema | Mirror of quest.md | New `.sprint/sprint.md` schema | Pipeline-shaped state with versioning |
| External tooling | None | Optional (banned-question linter) | Required (WebSearch, scrape, clustering, slide rendering, evals) |
| Acceptance bar | Friendly tester completes 6 steps end-to-end with usable markdown artifacts | Investor-conversation-ready artifacts; Mom Test enforced | Investor-grade slide artifacts; verified anti-sycophancy via eval; theme saturation detection on real data |
| Distribution | Claude Code plugin | Claude Code plugin | Claude Code plugin OR standalone web/desktop |
| **NotebookLM bolt-on (§4)** | Possible but thin value | **Strong fit (~+5 days)** | Replaces ~30% of tooling work; reduces Extensive scope |

## Option 1 — Minimum: profile-pack-themed sibling plugin

### Shape

A new Claude Code plugin published as `mitchell-agentic-sprint`, declaring `campaign-mode` and `six-animals` as marketplace dependencies. Two slash commands. Steps 1–6 are inline prompts inside those commands. Mini Council is implemented as five profile-packs that re-skin Cat / Bear / Dragon as the five voices.

### File inventory (new files only)

```
.claude-plugin/
  plugin.json
  marketplace.json (optional, if published as its own marketplace entry)
commands/
  sprint-start.md         # one-shot: bootstraps state, runs Step 1
  sprint-continue.md      # re-entry, dispatches to current step
profile-packs/
  mas-council/
    seed-vc.md            # skins dragon
    churned-customer.md   # skins cat
    competitor-founder.md # skins bear
    future-self.md        # skins owl
    grumpy-pm.md          # skins guardian
docs/
  templates/
    sales-deck.md
    outreach-plan.md
    investor-deck.md
  README.md
```

### What it reuses

- `gandalf-agent` — Step 1 framing, Step 4 expert-discovery framing
- `dragon-agent` — Step 6 final confrontation against criteria
- `guardian-agent` — invoked by `/sprint-continue` at step transitions
- `bear-agent` through `wolf-agent` — advisory layer if user wants team perspective
- `simon-agent` — orchestrator/synthesizer when consulting multiple animals
- conversation transcripts, progress log, AskUserQuestion conventions

### Worked example walkthrough

A user runs `/sprint-start`. Step 1 prompt invokes Gandalf-as-skin to ask the founder profile questions. State written to `.sprint/sprint.md`. Command ends with AskUserQuestion: "Continue to Step 2?" User picks Continue. `/sprint-continue` reads state, sees `step: 2`, runs the Step 2 prompt inline. Mini Council fires between Steps 1 and 2 by invoking the dragon agent five times in series, each time with a different profile from `mas-council/`. Aggregated critiques are presented; user can revise Step 1 or proceed.

### Why it works

The plugin model is genuinely generic — `commands/*.md` files self-register, profile packs are read by file convention. The Dragon's voice + tone is already adversarial and re-skinning gives us the Council voices for free *if* you accept that they'll all sound like the Dragon with different names.

### Why it doesn't work for the headline promise

- The Mini Council voices will lack domain heuristics. Re-skinning the Dragon as "Seed VC" gives you a Dragon who speaks in VC vocabulary, not a Seed VC who reasons about unit economics. Test: ask the skinned Dragon "what's a reasonable seed valuation for a vertical SaaS doing $10K MRR?" — it has no answer baked in.
- Steps 4 (expert discovery) and 5 (competitor analysis) require the user to provide their own research; the plugin can only structure it.
- Step 3 (interviews) cannot enforce Mom Test discipline — there's no banned-question linter. The script generator might still draft "would you use a tool that does X?" because the prompt is the only enforcement.
- No loopback handler — the user can manually edit state but a clean reset isn't supported.

### Effort breakdown

| Work | Days |
|---|---|
| Plugin scaffolding + manifest | 1 |
| Two commands (sprint-start, sprint-continue) | 3 |
| Six step prompts (inline in commands) | 3 |
| Five profile-pack files | 2 |
| Three artifact templates (markdown) | 1 |
| Manual testing on one worked sprint | 2 |
| Docs + README | 1 |
| **Total** | **~13 days (≈ 2.5 weeks)** |

### Risks

- **Council shallowness** — the 5 voices feel interchangeable. Mitigation: aggressive prompt engineering per profile, accepting limit. Likely material.
- **Sequence skip** — user runs `/sprint-step-3` (or its inline equivalent) before completing 1–2. Mitigation: prompts begin with state-validation block. Likely.
- **Mom Test leak** — user gets a script that contains hypothetical questions. Mitigation: hand-curated bad-example list in the prompt. Probable.
- **Investor deck weakness** — generated decks are template-shaped but don't have the validation evidence the concept requires. Mitigation: refuse to pad missing sections; produce a "missing evidence" report instead. Probable.

### Kill criteria

After 5 friendly testers run the full Sprint, one or more of:
- ≥ 3 testers report Council voices feel interchangeable
- ≥ 2 testers produce decks with fabricated evidence
- ≥ 1 tester completes a Sprint with hypothetical-only interview questions

→ Revisit and either upgrade to Moderate or kill.

### Upgrade path to Moderate

Replace each profile-pack file with a new SKILL.md agent file. Add `/sprint-step-N` commands as gates. Add loopback command. Step prompts move from inline-in-command to inline-in-skill. ~80% of Minimum's work is preserved.

## Option 2 — Moderate: new NPC agents + step gates + loopback

### Shape

Same sibling-plugin shape as Minimum, plus:
- Five new SKILL.md NPC agents — each Mini Council voice gets its own file with embedded domain heuristics
- One command per step (`/sprint-step-1` through `/sprint-step-6`), with hard gates: each refuses to run if `last_approved_step < N-1`
- Explicit loopback command that resets state preserving Step 1 + accumulated themes
- Banned-hypothetical-question linter for Step 3 interview scripts (small Bash or Python helper)
- Markdown artifact generators for Step 6 outputs

### File inventory (new files)

```
.claude-plugin/
  plugin.json
commands/
  sprint-setup.md
  sprint-start.md
  sprint-step-1.md ... sprint-step-6.md
  sprint-council.md       # invokes the 5 voices in sequence
  sprint-loopback.md
  sprint-continue.md
skills/
  seed-vc-agent/SKILL.md
  churned-customer-agent/SKILL.md
  competitor-founder-agent/SKILL.md
  future-self-agent/SKILL.md
  grumpy-pm-agent/SKILL.md
docs/
  templates/
    sales-deck.md
    outreach-plan.md
    investor-deck.md
  examples/
    worked-example-1-vertical-saas.md
    worked-example-2-prosumer.md
    worked-example-3-loopback.md
  research/
    sprint-state-schema.md
helpers/
  validate-interview-script.sh    # banned-question linter
  count-saturation.sh              # rolling theme count for Step 3
```

### What it reuses

Everything Minimum reuses, plus:
- Guardian's "approve / not yet / conditional" verdict structure → adapted into per-step gate logic
- Dragon's voice/tone → adopted in each new SKILL.md as the adversarial preamble

### Worked example walkthrough

Same start as Minimum. After Step 1, user runs `/sprint-council`. The command invokes each of the 5 new NPC agents in sequence, each receiving the user's Step 1 profile + draft Vertical Stack. Each voice produces one *strongest* critique in their own voice with their own heuristics — Seed VC asks about TAM and traction velocity; Future-Self asks "what would you regret about this vertical in 12 months?" Aggregated critiques are presented. User chooses: revise Step 1, accept and continue to Step 2, or loopback. At Step 3, the interview-script generator produces the script and the linter blocks it if it contains banned hypothetical phrasing — script returns to the generator with feedback. After Step 3, if no costly-action signals after N=15 interviews, the saturation detector fires and the user is offered a loopback.

### Why it works for the headline promise

The Mini Council voices have *real* domain heuristics:
- Seed VC's SKILL.md includes a 2026-AI-era investor checklist (working demo, evals, inference economics, moat taxonomy)
- Churned Customer's SKILL.md includes a regret-narrative framing (referenced from concept §6 quotes)
- Competitor Founder's SKILL.md includes a competitive-intelligence rubric (pricing, GTM, support burden)
- Future-Self's SKILL.md uses temporal hindsight prompts ("12 months from now, you tell me…")
- Grumpy PM's SKILL.md uses pessimistic-execution framing (resource multiplier, tech debt, competing priorities)

Step gates make sequence enforcement code-level, not convention-level. The interview linter makes Mom Test discipline enforceable, not aspirational. The loopback handler makes "make a no cheap" (concept §7) operational, not just stated.

### Effort breakdown

| Work | Days |
|---|---|
| Plugin scaffolding + state schema | 2 |
| Eight commands (setup, start, six step gates, council, loopback, continue) | 8 |
| Five new NPC SKILL.md files | 8 |
| Banned-question linter | 2 |
| Saturation detector | 1 |
| Three artifact templates + generators | 4 |
| Three worked examples | 4 |
| Manual testing on three full sprints incl. one loopback | 5 |
| Docs (README, schema doc, examples) | 3 |
| **Total** | **~37 days (≈ 7–8 weeks)** |

### Risks

- **Domain heuristics need iteration** — first drafts of the 5 voices will be uneven; expect 2–3 revision cycles per voice based on tester feedback. Material.
- **Linter false positives** — the banned-question check will flag legitimate questions ("how do you decide…?" can read as hypothetical). Mitigation: tune iteratively; allow user override with explicit acknowledgement. Probable.
- **State migration** — if `.sprint/sprint.md` schema evolves during build, existing in-flight sprints break. Mitigation: version the schema; add a tiny migration helper. Possible.
- **Campaign-mode upstream drift** — campaign-mode is on v0.4.x; major version bumps could break our extensions. Mitigation: pin a campaign-mode version in our manifest. Likely over time.
- **Slide rendering pressure** — testers will ask "where's the .pptx?" Mitigation: hold the line, document why markdown-first; agree to Extensive-tier add only after demand is proven.

### Kill criteria

- After 5 testers, < 3 reach genuinely investor-conversation-ready artifacts
- Council voices still feel interchangeable after 2 prompt-iteration rounds
- Linter false-positive rate > 30% making Step 3 frustrating

### Upgrade path to Extensive

The Moderate architecture survives intact. Extensive adds a tooling layer: WebSearch for Step 4/5, slide rendering, theme clustering, eval set. None of those force changes to the SKILL.md files or step commands.

## Option 3 — Extensive: pipeline-shaped fork with tooling

### Shape

Diverges from campaign-mode either by forking it or starting clean. Adds a service-shaped tooling layer that backs the slash commands. Possibly distributed as a standalone web/desktop product rather than as a Claude Code plugin (depends on Q6).

### Additional capabilities over Moderate

- **WebSearch + scrape pipeline** for Step 4 (expert discovery: book + course + interviews + revenue evidence) and Step 5 (top-10 competitor analysis: positioning, pricing, GTM)
- **Theme clustering** for Step 3: instead of counting strings, cluster interview transcripts semantically and detect saturation by inter-cluster similarity
- **Slide rendering** (PPTX via `python-pptx` or PDF via Reveal.js + headless Chrome) for the three Step 6 artifacts
- **Outreach drafter with re-engagement logic** — looks back at Interview Log, identifies costly-action signals, drafts personalised re-engagement messages quoting the buyer's own words
- **Sales Navigator filter generator** — translates Vertical Stack into a structured filter spec the user can paste in
- **Anti-sycophancy regression eval** — held-out set of 20–30 prompts where the user is wrong; assert each step's agents push back rather than flatter; run pre-release

### File inventory (additions over Moderate)

```
service/                     # small TypeScript or Python service
  src/
    web-research.ts          # WebSearch + light scrape
    cluster-themes.py        # interview clustering
    render-slides.ts         # PPTX/PDF generation
    eval-sycophancy.ts       # adversarial regression
  package.json
docs/
  evals/
    sycophancy-set.jsonl
    interview-discipline-set.jsonl
    council-fidelity-set.jsonl
```

### Why it might be necessary

- The concept's pitch is investor-grade decks. Markdown is acceptable for a tester demo but not for a distributable v1 product.
- Theme saturation detection on pasted-in interview text is a real ML problem; counting won't cut it past a few interviews.
- Anti-sycophancy verification can't be assumed — the concept itself flags it as an open question. An eval set is how we'd know.

### Why it might be premature

- Concept §10 ("What this concept might be wrong about") suggests the founder himself is uncertain about the linear flow, the named-expert assumption, and whether AI can replace a coach. Spending 3 months building tooling before validating those assumptions is the wrong order.
- Slide rendering is well-trodden but tedious; doing it before user demand is proven is speculative.
- Maintaining a fork or standalone product loses the campaign-mode upstream + community.

### Effort breakdown

| Work | Days |
|---|---|
| Everything in Moderate | 37 |
| Service scaffolding (TS or Python) | 5 |
| Web research pipeline | 7 |
| Theme clustering | 5 |
| Slide rendering | 8 |
| Outreach drafter with re-engagement | 4 |
| Sales Navigator filter generator | 2 |
| Anti-sycophancy eval set + harness | 6 |
| Integration testing | 5 |
| Docs | 3 |
| **Total** | **~82 days (≈ 16 weeks)** |

### Risks

- **Scope creep on slide rendering** — designers will always want more. Mitigation: lock to a single template per artifact, no customisation in v1.
- **Eval fidelity** — measuring sycophancy is itself a research problem. The eval set may pass while real users still feel flattered. Mitigation: combine automated eval with structured tester debriefs.
- **Service complexity** — adding a TS/Python service introduces a deployment surface. Mitigation: keep stateless; deploy as a single binary or container.
- **Distribution decision** — if Extensive is selected, Q6 (distribution channel) becomes load-bearing earlier.

### Kill criteria

This tier is justified *only* if Moderate ships and demonstrates demand for tooling-layer capabilities. Building Extensive without that demand signal is the bad path.

## Option 4 — NotebookLM bolt-on (tier-bridging)

This is not a fourth standalone option — it's an **integration layer** that attaches to either Moderate or Extensive. Per the [issue #1 comment from cgbarlow](https://github.com/cgbarlow/mitchell-agentic-sprint/issues/1#issuecomment-4410281069), evaluating Google NotebookLM for synthesis and artifact work.

### What's available (May 2026)

| Path | Status | Sources |
|---|---|---|
| Google Cloud **NotebookLM Enterprise API** | Official, released Sep 2025. Notebook CRUD, sources, audio overviews, queries. Workspace/Enterprise customers only. | [Google Cloud docs](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) |
| Unofficial **CLI** (`tmc/nlm`, `notebooklm-cli`) | Active. Cookie-based auth via dedicated browser profile. Cookies persist; auto-refresh on expiry. | [tmc/nlm](https://github.com/tmc/nlm), [jacob-bd/notebooklm-cli](https://github.com/jacob-bd/notebooklm-cli) |
| **MCP servers** (multiple) | Multiple actively maintained projects targeting Claude Code, Claude Desktop, Cursor, VS Code. As of Jan 2026 the CLI + MCP merged into a single `nlm` package. | [PleasePrompto/notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp), [julianoczkowski/notebooklm-mcp-2026](https://github.com/julianoczkowski/notebooklm-mcp-2026), [jacob-bd/notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) |
| Open-source clone (`open-notebook`) | Self-hosted alternative, more flexible, no Google dependency | [lfnovo/open-notebook](https://github.com/lfnovo/open-notebook) |

### Where NotebookLM helps

| MAS step | What NotebookLM does | Replaces |
|---|---|---|
| 3. Buyer interviews | Theme map + saturation analysis from interview transcripts; verbatim quote extraction | Bespoke theme clustering (Extensive tier) |
| 4. Framework | Summarises an expert's books/courses/interview tape; produces "what to keep / what to adapt" splits | WebSearch + scrape + manual synthesis (Extensive tier) |
| 5. Competitor | Clustering across competitor websites; positioning whitespace candidates | WebSearch + scrape (Extensive tier) |
| 6. Synthesis | Audio overview (10-min podcast briefing for the founder pre-VC meeting); mind map of the validated thesis; briefing doc | Augments — does not replace — the three written artifacts |

NotebookLM's source-grounding posture aligns with MAS's "verbatim quotes only" rule (concept §6). It does **not** replace Mini Council adversarial logic, the Mom Test linter, or PPTX rendering.

### Architectural shape

```
┌─────────────────────────────────────────────┐
│  Claude Code session                         │
│  ┌──────────────────┐    ┌────────────────┐ │
│  │  MAS plugin      │───▶│ NotebookLM MCP │ │
│  │  (Moderate tier) │    │ server (local) │ │
│  └──────────────────┘    └───────┬────────┘ │
└──────────────────────────────────│──────────┘
                                   │
                                   ▼
                  ┌────────────────────────────┐
                  │  NotebookLM (Google)       │
                  │  - notebook per sprint     │
                  │  - sources: transcripts,   │
                  │    expert docs, competitor │
                  │    pages                   │
                  │  - outputs: themes, audio, │
                  │    mind map, briefing      │
                  └────────────────────────────┘
```

MAS's step commands invoke NotebookLM tools through MCP at:
- Step 3 close-out: push interview transcripts to a notebook, request theme map
- Step 4 mid-step: push expert source documents (user-provided URLs/PDFs), request framework summary
- Step 5 mid-step: push competitor URLs, request positioning whitespace
- Step 6 close-out: request audio overview from the full notebook

### Effort over Moderate baseline

| Work | Days |
|---|---|
| MCP server selection + installation docs | 1 |
| Optional dependency declaration in plugin.json | 0.5 |
| Step command patches to invoke MCP tools | 2 |
| Auth onboarding flow (one-time browser-cookie or OAuth setup) | 1 |
| Manual testing on one full sprint with NotebookLM-augmented synthesis | 1.5 |
| Docs (which MCP server, how to install, how to auth) | 1 |
| **Total over Moderate** | **~7 days (≈ 1.5 weeks)** |

If applied to Extensive instead, this *reduces* Extensive's scope by replacing ~3 weeks of bespoke tooling (theme clustering, web research pipeline, partial slide synthesis) with the MCP integration. Net: Extensive + NotebookLM ≈ 12 weeks (vs 16 weeks for full bespoke Extensive).

### Risks

- **Auth friction** — first-run cookie setup or OAuth handshake will trip up some testers. Mitigation: `/sprint-setup` walks through it interactively.
- **Vendor lock-in** — NotebookLM is closed-source / Google-owned. Mitigation: keep the integration optional; MAS still works without it.
- **ToS risk on unofficial path** — Google could block unofficial automation. Mitigation: support both the unofficial CLI and the Enterprise API; document switching.
- **Adversarial fidelity** — NotebookLM is grounded but not adversarial-by-default; if MAS uses NotebookLM-generated content for the Mini Council inputs, the Council still needs to attack the synthesis. Mitigation: NotebookLM produces facts, Mini Council attacks the *interpretation*.
- **Notebook limits** — NotebookLM Plus has higher source/notebook limits but still bounded; long-running multi-attempt sprints may hit them. Mitigation: archive old sources between attempts.
- **Per-user account requirement** — each builder needs their own Google/Workspace account. Acceptable for v1 (immediate network) but a polish gap for general-public v2.

### Kill criteria

After 3 testers run a full sprint with NotebookLM augmentation:
- ≥ 2 testers report the auth setup is a blocker
- The NotebookLM-generated theme map / framework synthesis is rejected by Scott as low-quality compared to Claude-only synthesis
- ToS strike from Google on the unofficial path with no enterprise fallback

→ Make NotebookLM truly optional; don't depend on it for v1 happy path.

### Recommended adoption pattern

- Make MCP integration **optional**, not required, in `plugin.json`
- v1: support `nlm` CLI + one MCP server (pick the most-maintained at integration time, likely the unified `nlm` + `notebooklm-mcp` package)
- v2: add Enterprise API path for org-deployed users
- Always maintain a Claude-only fallback path so MAS works without NotebookLM (slower, less fluent synthesis, but functional)

## How to choose

The choice depends on:

1. **Ownership and time budget (Q7)** — Moderate is 7–8 weeks for one engineer. Extensive is twice that. Minimum is 2.5 weeks but doesn't deliver the headline promise.
2. **Distribution (Q6)** — if standalone web/desktop is required, Extensive is the floor and you also need a frontend. If Claude Code plugin is acceptable, Moderate suffices.
3. **Tester pool size and v1 user persona** — your immediate AI-builder network (5–20 people) tolerates Moderate's rough edges; general-public AI-builders need Extensive's polish.
4. **Spike or paper-only (research question)** — if user wants the spike, do one Step 1 + one Council invocation in Moderate's shape, ~1 week, before committing to the full Moderate build.
5. **NotebookLM bolt-on (§4)** — independent decision. If yes, adds ~1.5 weeks to Moderate or shrinks Extensive by ~3 weeks. Highest fit when v1 audience is comfortable with a Google account dependency.

The [recommendation](RECOMMENDATION.md) makes a concrete pick subject to those open questions.
