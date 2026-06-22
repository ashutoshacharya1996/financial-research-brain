# Stock Dashboard Schema

## Purpose

The Stock Dashboard is a per-stock decision support document combining four analytical frameworks into a single readable view. It is produced **on demand** (not as a Sunday pipeline stage) because it requires live market prices and live portfolio holdings — values that cannot be pre-computed.

Trigger: `/stock-dashboard [TICKER]`

Output path: `10_DASHBOARD/<TICKER>/dashboard-YYYY-MM-DD.md`

---

## Eligibility

Only stocks in `07_OPPORTUNITIES/active/` qualify for a dashboard. The Opportunity Record must have `status: Active` and `corroboration_count ≥ 3`.

If a stock is requested that has no active Opportunity Record, redirect: "TICKER is in the Research Queue but has no full Opportunity Record yet — run `/india-stock-picker TICKER` for a standalone analysis."

---

## Four Panels

### Panel 1 — Buy Zone Bar (India Stock Picker)

**Purpose:** Answers "Is now a good time to buy?"

**Inputs:** Live price (Kite `get_ltp`), 52-week range (Kite `get_ohlc`), Gates 1–5 of india-stock-picker framework, linked Opportunity Record confidence score.

**Output elements:**

**1A. Buy Zone Bar** — text visualization showing where current price sits:

```
CHEAP ←──[STRONG BUY]──[BUY ZONE]──[FAIR VALUE]──[WATCH]──[EXPENSIVE]──→
         ₹X₁           ₹X₂          ₹X₃           ₹X₄       ₹X₅
                    ▲ Current: ₹[price] ([date])
```

Price zone definitions (derived from Gate 4 fair value estimate):
| Zone | Price relative to fair value |
|------|------------------------------|
| Strong Buy | > 25% below fair value |
| Buy Zone | 10–25% below fair value |
| Fair Value | Within ± 10% of fair value |
| Watch | 10–25% above fair value |
| Expensive | > 25% above fair value |

If fair value cannot be computed (missing financial data): render bar as "Framework-only — live data required for pricing" and skip the bar.

**1B. Poised Score (1.0–10.0):**

Start with the Opportunity confidence score from the linked Opportunity Record.

Apply modifiers:
- Current price in Strong Buy zone: +1.0
- Current price in Buy Zone: +0.5
- Current price in Watch zone: −0.5
- Current price in Expensive zone: −1.5
- Gate 1 fully passed (all Mukherjea criteria): +0.5
- Gate 1 conditional pass (≥1 flag): 0
- Gate 1 fail: −2.0
- PE > 40 flag: −1.0
- PE 30–40 (acceptable but flagged): −0.5
- Debt flag (D/E > 1.0): −0.5
- Management Red flag (≥1): −1.0

Cap at 10.0, floor at 1.0.

**1C. ELI15 Explanation (2–3 sentences):**
Plain English. What does this score mean and why? No jargon. Analogy where possible.

---

### Panel 2 — Scenario Forecast (Financial Forecaster)

**Purpose:** Answers "How does this story play out?"

**Inputs:** Financial Forecaster condensed framework, linked Opportunity Record (why_now and risks), live price.

**Output elements:**

| Scenario | Probability | 2-Year Return | Key Trigger |
|----------|-------------|--------------|-------------|
| Bull | X% | +Y% | [one named trigger] |
| Base | Y% | +Z% | [one named trigger] |
| Bear | Z% | −W% | [one named trigger] |

Probabilities must sum to 100%.

One-sentence thesis per scenario (plain English, analogy first).

Confidence in probability estimates: High / Medium / Low + one-sentence reason.

Single most important variable to watch: the one factor that will most reliably signal which scenario is playing out.

---

### Panel 3 — Personal Fit (Financial Advisor)

**Purpose:** Answers "Should I personally buy this, given what I already hold?"

**Inputs:** Live Kite `get_holdings`, linked Opportunity Record, india-stock-picker portfolio rules (12-stock ceiling, Core/Extended tiers, FIRE horizon).

**Output elements:**

**3A. Current position:**
- Held / Not held
- If held: current value (₹), % of portfolio, unrealised P&L, holding period
- If not held: which slot would this fill (Core / Extended)?

**3B. Portfolio fit:**
- Sector weight post-addition (within / exceeds limit?)
- FIRE horizon fit: thesis duration vs. years to FIRE target
- What is the weakest current position this would displace?

**3C. Personal recommendation:**
One of four verdicts:
- **Add this week** — price is in buy zone, fits portfolio, no blocking issues
- **Add on dip — watch ₹X** — thesis is strong but price is above buy zone; specific entry price given
- **Hold** — already held; no action needed; or held at higher allocation than warranted
- **Avoid** — thesis doesn't fit portfolio, or blocking issue (PE flag, execution risk, sector overweight)

Verdict must cite: current price, current holding status, and specific reason.

**3D. Behavioural check:**
Name any active bias explicitly. Do not soften.

---

### Panel 4 — Competitive Dynamics (Game Theory Master)

**Purpose:** Answers "Who actually wins as this thesis plays out — and is it this company?"

**Inputs:** Game Theory Master framework, linked theme record (Game Theory View section), Opportunity Record candidate stocks and rationale.

**Output elements:**

**4A. The Game:**
- Players: who the key actors are (company, competitors, customers, regulator)
- Game type: zero-sum (fixed market share) or non-zero-sum (expanding market)? Sequential or simultaneous moves?
- Key information asymmetry: what does this company know that competitors don't — or vice versa?

**4B. Who Captures Value:**
As the thesis plays out, which player extracts the most margin?
- Is it this company, or does value leak to customers, suppliers, or competitors?
- Is the company's position in the supply chain strengthening or weakening?

**4C. Equilibrium:**
What stable outcome does this industry converge to over 3–5 years?
Is this company better or worse positioned in that equilibrium than today?

**4D. Behavioral Wildcards (2–3):**
Irrational or politically-driven moves that could disrupt the rational analysis:
- Government intervention (subsidies, procurement policy reversal, emergency import)
- Competitor desperation (price war despite negative returns, irrational M&A)
- Customer consolidation (government entities merging purchasing power)

**4E. ELI15 Summary (2 sentences):**
Plain English. "The strategic landscape basically means..."

---

## File Header (Mandatory)

Every dashboard must begin:

```markdown
# Stock Dashboard — [COMPANY NAME] ([TICKER])
Date: YYYY-MM-DD
Live price: ₹X (as of YYYY-MM-DD HH:MM IST via Kite)
Linked opportunity: [opportunity-id]
Opportunity confidence: X.X / 10 | Theme: [theme name] | Trend: [Accelerating/Stable/Weakening]
```

---

## Dashboard Summary Index

After producing individual dashboards, update `10_DASHBOARD/summary-YYYY-MM-DD.md`:

```markdown
# Dashboard Summary — YYYY-MM-DD

| Ticker | Company | Poised Score | Buy Zone Position | Scenario Most Likely | Personal Action |
|--------|---------|-------------|-------------------|---------------------|-----------------|
| BEL | Bharat Electronics | X.X / 10 | [zone] | [Bull/Base/Bear] X% | [verdict] |
```

One row per stock with an active Opportunity Record.

---

## Investment Impact Link

If a recent Investment Impact note exists, every dashboard must reference it in
the header:

```markdown
Investment impact note: 08_PORTFOLIO_INPUTS/investment-impact/<TICKER>-impact-YYYY-MM-DD.md
```

Panel 1 and Panel 3 must explicitly test the blockers from that note. A positive
Opportunity Record or Poised Score cannot override:

- failed financial quality gates
- weak cash conversion
- valuation flags
- missing live portfolio data
- missing portfolio slot
- unresolved governance issues

---

## Rules

1. **Live price is mandatory for Panel 1 bar.** If Kite fails, render bar as "unavailable" and note timestamp.
2. **Scenarios must sum to 100%.** If probability is uncertain, use "qualitative ranking only" and explain.
3. **Panel 3 must cite current holding.** Never give a portfolio recommendation without checking live Kite holdings first.
4. **Poised Score is not a buy signal.** It is an index of how well-positioned the stock is for entry right now — a high Poised Score in an expensive market is still a watch, not a buy.
5. **Dashboard is research, not advice.** Every dashboard ends with: "This is a research document, not investment advice. Verify all data before acting."
6. **Only stocks with active Opportunity Records qualify.** No dashboard for Research Queue-only stocks.
7. **Investment Impact notes are handoffs, not verdicts.** They can trigger underwriting or watchlist upgrades, but they cannot authorize a buy.
