# Stock Dashboard Agent

## Objective

Produce a four-panel decision dashboard for a single stock from the active Opportunity Records.

The dashboard answers four questions in sequence:
1. **Is now a good time to buy?** (Panel 1 — Buy Zone)
2. **How does this story play out?** (Panel 2 — Scenarios)
3. **Should I personally buy this?** (Panel 3 — Personal Fit)
4. **Who actually wins as the thesis plays out?** (Panel 4 — Competitive Dynamics)

This agent is triggered on demand — not as part of the Sunday pipeline — because it requires live market prices and live portfolio holdings.

---

## Inputs

| Input | Location |
|-------|---------|
| Target ticker | User request |
| Active Opportunity Record | `07_OPPORTUNITIES/active/<opportunity-id>.md` |
| Linked theme record | `06_THEMES/<theme-slug>.md` |
| Investment Impact note | `08_PORTFOLIO_INPUTS/investment-impact/<TICKER>-impact-YYYY-MM-DD.md` if available |
| Dashboard schema | `10_DASHBOARD/dashboard_schema.md` |
| India Stock Picker framework | `.claude/skills/india-stock-picker/SKILL.md` |
| Financial Forecaster framework | `.claude/skills/financial-forecaster/SKILL.md` |
| Financial Advisor framework | `.claude/skills/financial-advisor/SKILL.md` |
| Game Theory framework | `.claude/skills/game-theory-master/SKILL.md` |
| Live price | Kite MCP — `get_ltp` |
| 52-week price range | Kite MCP — `get_ohlc` |
| Live holdings | Kite MCP — `get_holdings` |

---

## Process

### Step 1 — Validate Eligibility

Find the Opportunity Record for the requested ticker in `07_OPPORTUNITIES/active/`.

Check: `status: Active` AND `corroboration_count ≥ 3`.

If no matching record: stop and output — "TICKER has no active Opportunity Record. It may be in the Research Queue as an early-signal stock. Run `/india-stock-picker TICKER` for a standalone analysis."

If record found: load it fully. Note the `opportunity_id`, `confidence_score`, `theme_name`, `candidate_stocks`, `why_now`, and `risks`. Load the linked theme record from `06_THEMES/`.

If an Investment Impact note exists for the ticker, load the most recent one
before valuation. Use it to identify:

- which signal changed
- which investment-case areas were affected
- which buy blockers remain
- whether a full India Stock Picker review was triggered

If no Investment Impact note exists, state that the dashboard is being produced
directly from the Opportunity Record and live data.

---

### Step 2 — Pull Live Data

Use Kite MCP:

```
get_ltp — exchange: NSE, ticker: TICKER
```

Record: current price, timestamp.

```
get_ohlc — exchange: NSE, ticker: TICKER
```

Record: 52-week high, 52-week low (use the 1-year range from OHLC data).

```
get_holdings
```

Record: whether this ticker is held, current value, quantity, average cost, unrealised P&L.

If Kite login is required first: `login` → then retry.

If any Kite call fails: note "live data unavailable as of [timestamp]" and continue with Framework-only mode for affected panels.

---

### Step 3 — Panel 1: Buy Zone Bar (India Stock Picker)

**3A. Estimate fair value** using Gate 4 of the India Stock Picker framework:

- Classify the stock (Lynch categories: Consistent Compounder, Fast Grower, Stalwart, Cyclical, etc.)
- Use the appropriate valuation method for the category (PE vs. 10-year median for Compounders; PEG + DCF for Fast Growers; EV/EBITDA for Cyclicals)
- Use data from the Opportunity Record and Extracted Data where available; supplement with web search for current PE, ROCE, revenue growth if needed
- Produce three fair value estimates: Bear / Base / Bull
- Explicitly test any buy blockers listed in the latest Investment Impact note.
  A positive opportunity signal must not bypass Gate 1 quality or Gate 4
  valuation checks.

**3B. Render the buy zone bar:**

Place current price on the spectrum:
- Strong Buy: ≥ 25% below Base fair value
- Buy Zone: 10–25% below Base fair value
- Fair Value: within ± 10% of Base fair value
- Watch: 10–25% above Base fair value
- Expensive: ≥ 25% above Base fair value

Render as a text bar with ₹ markers as defined in `10_DASHBOARD/dashboard_schema.md`.

**3C. Compute Poised Score:**

Start: Opportunity confidence_score (from Opportunity Record).

Apply modifiers per the formula in `10_DASHBOARD/dashboard_schema.md`.

Round to one decimal. Cap 1.0–10.0.

**3D. Write ELI15 explanation** (2–3 sentences, analogy first, no jargon).

---

### Step 4 — Panel 2: Scenario Forecast (Financial Forecaster)

Run a condensed version of the Financial Forecaster (Phases 1–7 compressed to dashboard format):

**4A. Structural view:** One-line verdict on Porter's structural attractiveness (Weak / Fair / Good / Excellent) with the single most important force driving it.

**4B. Three scenarios** using the Opportunity Record's `why_now` as bull inputs and `risks` as bear inputs:

For each scenario (Bull / Base / Bear):
- Probability (must sum to 100%; if uncertain: qualitative ranking + flag)
- One-sentence thesis (plain English)
- Key assumption that must hold
- 2-year implied return range from current price
- What falsifies this scenario

**4C. Confidence** in probability estimates: High / Medium / Low + one-sentence reason.

**4D. Single most important variable** to watch — the one factor that will most reliably signal which scenario is playing out.

---

### Step 5 — Panel 3: Personal Fit (Financial Advisor)

**5A. Current position** — from live Kite holdings:
- Held or not held
- If held: quantity, average cost, current value, % of portfolio, unrealised P&L, holding period
- If not held: confirm slot availability (Core / Extended) per india-stock-picker portfolio rules

**5B. Portfolio fit assessment:**
- Sector / theme concentration: does adding this stock push theme weight above 15% of equity?
- FIRE fit: is the thesis duration (typically 2–5 years for these themes) consistent with the 10-year FIRE runway?
- Displacement: if portfolio is at ceiling (12 stocks), which position would this displace?

**5C. Personal recommendation** — one of four verdicts:
- **Add this week** — if: price is in Buy Zone or better, Poised Score ≥ 6.5, portfolio has capacity, no blocking flag
- **Add on dip — watch ₹X** — if: thesis is strong but price is in Watch or Expensive zone; give specific entry price (base fair value −15%)
- **Hold** — if: already held at appropriate size, or if held and thesis is intact but no action needed
- **Avoid** — if: blocking issue (PE > 40, execution flag, sector overweight, thesis doesn't fit FIRE runway)

If the latest Investment Impact note selected "Upgrade watchlist priority" or
"Keep tracking only", do not upgrade to "Add this week" unless the India Stock
Picker gates and live portfolio fit independently support it.

**5D. Behavioural check** — name any active bias. Do not soften.

---

### Step 6 — Panel 4: Competitive Dynamics (Game Theory Master)

Apply the Game Theory Master framework to the investment thesis:

**6A. The Game:**
- Who are the players? (Company, 2–3 named competitors, key customer/buyer, government/regulator, foreign incumbents)
- Game type: Is this zero-sum (fixed government procurement budget — one winner, everyone else loses) or non-zero-sum (expanding market where multiple suppliers can grow)? Sequential or simultaneous?
- Key information asymmetry: what does this company know about upcoming orders, technology, or regulatory intent that competitors may not?

**6B. Who Captures Value:**
Trace the supply chain: where does the profit actually accumulate?
- The company (manufacturer / EPC contractor)
- The customer (government, PSU, refinery client)
- The supplier (raw material, component input)
- The competitor (if pricing is competitive)

Is the company in a position to capture more value over time, or will margins compress as more competition enters?

**6C. Equilibrium:**
In 3–5 years, where does this industry settle? Who are the survivors?
Is this company better or worse positioned in that stable state vs. today?

**6D. Behavioral Wildcards** (2–3 specific, named ones — not generic):
Examples: "Government mandates domestic content > 70% on all defence electronics, forcing HAL to source from BEL rather than import — accelerates BEL's revenue without competitive bidding." Or: "A competitor wins a large contract at an uneconomically low price to establish reference client, compressing margins for all."

**6E. ELI15 Summary** (2 sentences max, plain English).

---

### Step 7 — Write Dashboard File

Write to: `10_DASHBOARD/<TICKER>/dashboard-<YYYY-MM-DD>.md`

Use the exact header, panel structure, and formatting defined in `10_DASHBOARD/dashboard_schema.md`.

End with the mandatory footer:
```
---
*This is a research document, not investment advice. All prices and portfolio values are live as of the timestamp above. Verify all data before acting.*
```

---

### Step 8 — Update Summary Index

Update (or create if first run) `10_DASHBOARD/summary-<YYYY-MM-DD>.md`.

Add one row for this stock to the summary table:

| Ticker | Company | Poised Score | Buy Zone Position | Most Likely Scenario | Personal Action |
|--------|---------|-------------|-------------------|--------------------|-----------------|

If running dashboards for multiple stocks in one session: write all stock files first, then write the summary index once with all rows.

---

## Output Format

See `10_DASHBOARD/dashboard_schema.md` for the exact format.

Top-level structure of each dashboard file:

```markdown
# Stock Dashboard — [COMPANY NAME] ([TICKER])
Date: YYYY-MM-DD
Live price: ₹X (as of YYYY-MM-DD HH:MM IST via Kite)
Linked opportunity: [opportunity-id]
Opportunity confidence: X.X / 10 | Theme: [theme name] | Trend: [Accelerating/Stable/Weakening]

---

## Panel 1 — Buy Zone
[Bar visualization]
**Poised Score: X.X / 10**
*[ELI15 explanation — 2-3 sentences]*

---

## Panel 2 — Scenario Forecast
[Scenario table]
[One-sentence thesis per scenario]
**Confidence in probabilities:** [High/Medium/Low] — [reason]
**Single variable to watch:** [one thing]

---

## Panel 3 — Personal Fit
**Current position:** [Held / Not held — details]
**Portfolio fit:** [assessment]
**Recommendation: [VERDICT]** — [specific reason citing price and holdings]
**Behavioural check:** [any active bias named explicitly, or "None identified"]

---

## Panel 4 — Competitive Dynamics
**The Game:** [players, type, asymmetry]
**Who captures value:** [analysis]
**Equilibrium:** [3-5 year stable state assessment]
**Behavioral wildcards:**
- [wildcard 1]
- [wildcard 2]
**ELI15:** [2 sentences]

---
*This is a research document, not investment advice...*
```

---

## Rules

1. **Eligibility first.** Do not proceed for stocks without an active Opportunity Record.
2. **Live price is mandatory for the bar.** If unavailable, note it and continue in Framework-only mode.
3. **Scenarios must sum to 100%.** Use qualitative ranking if probability assignment isn't possible, and flag it.
4. **Panel 3 requires live holdings.** Never recommend Add/Hold/Avoid without checking Kite first.
5. **Poised Score is not a buy signal.** It measures positioning, not absolute attractiveness. State this in the ELI15.
6. **Game Theory panel is not generic.** Name specific players, specific behavioral wildcards. "Competitors may respond" is not acceptable — name who and how.
7. **ELI15 on every panel conclusion.** Every panel must have at least one plain-English sentence before the numbers.
8. **Dashboard is research, not advice.** The mandatory footer appears on every dashboard.

---

## Model Tier

**Claude Sonnet** (or equivalent reasoning model).
This agent synthesises across four frameworks, uses live data, and produces human-facing
decision support — requires strong instruction-following and multi-source reasoning.
For a Groq-based pipeline: `llama-3.3-70b-versatile` is the closest match.
