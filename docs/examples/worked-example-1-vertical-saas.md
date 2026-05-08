# Worked Example 1 — Vertical SaaS (Step 1 + Mini Council)

**Purpose:** voice-fidelity reference per [ADR-010](../adrs/ADR-010-TDD-Scope.md). Demonstrates the five Mini Council voices producing meaningfully different critiques on the same input.

**Scenario:** Fictional builder Priya runs through Steps 1 and 2 of a Sprint, reaches a Vertical Stack draft, convenes the Mini Council. Identifying details fictional; the dynamics are illustrative.

---

## Builder Profile (from Step 1 with Gandalf)

> **Background:** 8 years building payments and reconciliation tooling at two fintech startups (one acquired, one alive). Shipped two production AP-automation systems used by mid-market accounting firms. Domain network: ~40 named accounting-firm partners on first-name basis from prior roles.
>
> **Unfair advantages:**
> - Inbound warm-intro path to ~12 mid-market AP managers via prior customers
> - Deep familiarity with the Bill / MineralTree / Tipalti competitive landscape
> - Personal experience implementing SOC 2 compliance at the prior employer
>
> **Time and money runway:** 9 months solo. Self-funded. Cofounder candidate identified but not committed.
>
> **Rough idea:** "AI-powered AP automation for mid-market accounting firms — fuzzy invoice-to-bank matching with audit trail."
>
> **Known buyers:** Three named AP managers willing to take a call (verbatim names redacted in this example). One paid $80/month for a hand-rolled bookkeeper-built workaround for 14 months — a genuine costly-action signal.

## Vertical Stack draft (from Step 2 with Gandalf)

| Layer | Content |
|---|---|
| Vertical | B2B fintech |
| Sub-vertical | Payments operations / AP automation |
| ICP | AP managers in mid-market accounting firms (50–500 client books, US-based, currently using Bill or QuickBooks Online) |
| Specific workflow | Monthly reconciliation between client books and bank statements — fuzzy invoice matching where vendor names mismatch and dates drift |
| AI leverage point | LLM-based fuzzy match with full audit trail; suggests matches; AP manager approves / rejects with one click |

**Backup Verticals:**

1. AP automation for solo bookkeepers (smaller deal size; faster sales motion)
2. AR collections automation for the same accounting-firm buyer (different workflow, same buyer)

---

## Mini Council convenes

The Council fires at the Step 1→2 transition. All five voices receive the Builder Profile and Vertical Stack draft. Each operates in isolation — no voice sees the others' critiques.

### 💼 Seed VC

> Your buyer is named. Your costly-action signal is one buyer paying $80/month for fourteen months for a bookkeeper-built workaround. That's good. It's not enough.
>
> Inference economics: you're running an LLM call per invoice for fuzzy matching. A mid-market firm processes how many invoices per month? Two thousand? At GPT-class pricing that's a non-trivial COGS line. What's your cost per invoice and what's the price you'd charge per invoice or per seat? If your gross margin breaks under inference, this is not a venture business.
>
> Moat: "fuzzy matching with audit trail" is a feature, not a moat. Bill ships this in eighteen months as a checkbox in their existing product. What's the workflow lock-in that survives Bill's response? You said SOC 2 experience — is that the moat, or is it just table stakes?
>
> **Verdict: Pass for now.** I would not fund this round today, but I would reconsider if (a) you can show one buyer paid you specifically — even $50 — for an early build of the matching feature, (b) you can articulate a workflow lock-in beyond "we have audit trail", and (c) you have a unit economics line that survives a 10x increase in inference cost. Until then, this is not investable.

### 💔 Churned Customer

> I bought a tool like this two years ago. The pitch was identical to yours: "fuzzy match invoices, audit trail, one-click approve". I paid $400 a month for a year. I cancelled.
>
> Why I cancelled: by month four, the matches were good on the easy invoices and useless on the hard ones — the same invoices I was already manually reconciling. The 80/20 went the wrong way. I was paying $400 a month to save myself fifteen minutes on the easy stuff, while still doing two hours on the hard stuff myself. The tool didn't get smarter as we added data. The audit trail was beautiful but I never used it because I'd already approved the easy ones in one click.
>
> Walk me through the buyer's month four. Specifically, what's the audit trail being used for at month four — internal review, external compliance, manager spot-check? If the answer is "we don't really use it", you're carrying the cost of the audit feature without the retention benefit.
>
> Pricing: $80/month is the workaround price. The buyer paid that for a *human* bookkeeper. Are you priced where you replace the bookkeeper, or where you augment the bookkeeper? Those are different products and different pricing models.
>
> **Verdict: Pass for now.** I would not stay a customer of this product today, but I would reconsider if you can name a Month-6 cohort retention number from a beta with at least three buyers. Until then, this is not retention-defensible.

### ⚔️ Competitor Founder

> I'm at Bill. Or I'm at MineralTree. Or I'm at any of the four other AP automation tools the buyer already pays for. I sell into the same accounting-firm buyer.
>
> Where I'd attack you: integrations. The accounting firm runs QuickBooks Online for some clients, Xero for others, Sage Intacct for the bigger ones, and the rare NetSuite client. To be useful you need three integrations on day one. Each integration is six weeks of engineering. You have nine months and you're solo. The math doesn't work.
>
> Where I'd dismiss you: SOC 2. You said you have prior experience. That's not the same as having a SOC 2 report. Procurement at the accounting firm asks for the report and you don't have one. I do. I win that deal regardless of fuzzy-match accuracy.
>
> What I'd copy from you tomorrow: nothing yet. The "audit trail with one-click approve" is already in our roadmap. The fuzzy-matching is in our R&D queue and shipping in twelve months as a feature add.
>
> **Verdict: Pass.** I would not worry about this competitor today. The reason is: you have no compliance position and your integration roadmap is unscoped. The specific evidence missing: (a) a signed letter of intent or paid contract from one of the named buyers, (b) a SOC 2 readiness plan with timeline, (c) a real integration plan that fits in nine months solo or commits to a cofounder hire. Until then, you're not on my competitive radar.

### ⏳ Future-Self (12 months from now)

> I'm Priya, twelve months from today. I worked this vertical for a year. Here's what I regret.
>
> The decision I deferred: pricing. I told myself I'd "figure out pricing once we have customers." I didn't. By month four I was charging $200/month because that's what I anchored on, and by month seven I knew I should have been at $1200/month — but I'd already signed three contracts at $200 and couldn't raise without churning them. Pricing was the bottleneck the whole year. I should have set it on day one. You should set it this week.
>
> The relationship I didn't build: the accounting firm's *technology* partner — the IT lead, not the AP manager. I sold to AP managers all year. AP managers loved me. AP managers don't sign procurement. By month nine I was learning IT-stakeholder language from scratch. You have ~12 warm intros via prior customers — at least three of them are at firms where you can ask for a 15-minute introduction to the IT lead. Do that this week.
>
> The vertical-specific risk I treated as generic: regulatory drift. AP automation in accounting firms is creeping into "client money handling" territory. State CPA boards are starting to weigh in. By month ten I had a state board inquiry I hadn't anticipated. You can avoid this by reading two specific state CPA board opinions — I know which two but you should find them this week.
>
> The version of me that succeeded did this one thing differently: she committed to pricing on day fourteen and never re-opened the conversation.
>
> **Verdict: Pass for now.** I would not be at peace with this past-me today, but I would reconsider if you make the pricing decision this week and have the IT-stakeholder conversation by end of month one. Until then, this is a regret-shaped year ahead.

### 📋 Grumpy PM

> Let me look at the timeline. You have nine months. Solo.
>
> Required to ship a product mid-market accounting firms will buy:
> - Three integrations (QBO, Xero, Sage Intacct) — six weeks each = eighteen weeks
> - SOC 2 readiness — twelve weeks minimum, can run in parallel but eats engineering attention
> - The actual AI/matching product — you say six weeks. Multiply by three. Eighteen weeks.
> - Onboarding flow that makes the tool usable without a six-week services engagement — four weeks
> - Audit/observability so you can debug the AI when it's wrong — four weeks (skipped at your peril)
> - Sales motion — at least 50% of your time once you have a v0
>
> That's roughly 60 weeks of work. You have 36. The math doesn't math.
>
> What gets dropped on Tuesday: the third integration. By Tuesday week eight, Sage Intacct is harder than QBO and Xero and you'll skip it "for v1". Then the buyer at the accounting firm with three Sage Intacct clients — the buyer who would have paid you $1200/month — passes because you don't support their largest clients.
>
> **Verdict: Pass.** This will not ship in any reasonable timeline. The reason: integration work you haven't scoped will eat 18 weeks you don't have. The specific evidence missing: a credible plan that either (a) commits to one integration first and explicitly defers the others, (b) commits to a cofounder hire in month one, or (c) prices the v1 high enough that one buyer covers most of the runway. Until then, the timeline is a fantasy.

---

## Council aggregation

| Voice | Verdict | Headline finding |
|---|---|---|
| 💼 Seed VC | Pass for now | Need workflow lock-in beyond audit trail; need unit economics that survives 10x inference cost |
| 💔 Churned Customer | Pass for now | Month-6 retention story is unproven; pricing is unclear |
| ⚔️ Competitor Founder | Pass | No compliance position; integration roadmap unscoped |
| ⏳ Future-Self (12 mo) | Pass for now | Pricing decision deferred; IT-stakeholder relationship not built |
| 📋 Grumpy PM | Pass | Integration timeline blows up the runway |

**Tally:** 2 Pass, 3 Pass for now, 0 In play.

The Council does not vote. Priya reads all five and decides.

## What voice differentiation looks like (the point of this example)

Each voice attacked a different axis:

- Seed VC went after **funding-defensibility**: moat, unit economics, traction quality
- Churned Customer went after **retention**: month-four reality, pricing as cancellation trigger
- Competitor Founder went after **competitive position**: compliance, integrations, the "boring stuff that wins procurement"
- Future-Self went after **deferred decisions**: pricing, IT-stakeholder relationship, regulatory drift
- Grumpy PM went after **operational reality**: timeline math, what gets dropped on Tuesday

Two voices reached **Pass** (Competitor Founder, Grumpy PM); three reached **Pass for now**. None reached **In play**. The recurring theme — pricing, compliance, integrations, retention — is the user's actual punch list. The Council is doing its job: refusing flattery, forcing specificity, naming the work.

If two voices had produced near-identical critiques, that would be a **voice-fidelity bug** to fix in the prompts.

## What the user does next

Per Priya's read of the verdicts:

1. **Address the integration timeline math (Grumpy PM)** — she commits in writing to QBO + Xero only for v1, defers Sage Intacct, prices v1 at $1500/month to compensate for narrower coverage
2. **Make the pricing decision (Future-Self)** — done this week; pricing locked at $1500/month, never re-opened
3. **Build the IT-stakeholder relationship (Future-Self)** — three intros to IT leads via prior accounting-firm customers, scheduled in month one
4. **Begin SOC 2 readiness now (Competitor Founder)** — engages a SOC 2 consultant, twelve-week timeline running in parallel with build
5. **Re-convene the Mini Council** when these conditions are addressed, specifically to test whether the Seed VC's "moat beyond audit trail" gap closes when she has signed-LOI evidence

If those steps don't produce visible movement, **loopback** to a more compliance-forward or narrower-integration vertical (e.g., backup option #1: AP automation for solo bookkeepers — single integration, simpler procurement). Concept §7: make a "no" cheap.
