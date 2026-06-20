---
name: stock-dashboard
description: |
  Per-stock decision dashboard combining four frameworks into one document for any stock
  in the active Opportunity Records (07_OPPORTUNITIES/active/). Produces:
  - Panel 1: Buy Zone Bar (India Stock Picker) — where does current price sit vs fair value?
    Includes a Poised Score (1-10) and ELI15 explanation.
  - Panel 2: Scenario Forecast (Financial Forecaster) — Bull/Base/Bear with probabilities,
    2-year return range, and the single most important variable to watch.
  - Panel 3: Personal Fit (Financial Advisor) — live Kite holdings check, portfolio slot
    assessment, FIRE horizon fit, and a specific personal recommendation.
  - Panel 4: Competitive Dynamics (Game Theory Master) — who captures value as the thesis
    plays out, what equilibrium the industry converges to, behavioral wildcards.
  Requires live Kite MCP data (prices + holdings). On-demand only — not part of Sunday pipeline.
  Trigger on: "run dashboard for [stock]", "buy zone for [stock]", "should I buy [stock]",
  "show me the dashboard", "dashboard for [ticker]", "is [stock] a buy right now".
  Only eligible for stocks with active Opportunity Records (corroboration_count ≥ 3).
  For Research Queue-only stocks, redirect to /india-stock-picker.
model: sonnet
---

# Stock Dashboard

See full agent definition at `09_PROMPTS/stock_dashboard.md`.

This skill wraps that prompt for direct invocation via `/stock-dashboard [TICKER]`.

When triggered:
1. Read `09_PROMPTS/stock_dashboard.md` for the full 8-step process
2. Read `10_DASHBOARD/dashboard_schema.md` for the format contract
3. Confirm the ticker has an active Opportunity Record in `07_OPPORTUNITIES/active/`
4. Pull live data from Kite MCP (price, OHLC, holdings)
5. Execute all 4 panels in sequence
6. Write dashboard to `10_DASHBOARD/<TICKER>/dashboard-YYYY-MM-DD.md`
7. Update `10_DASHBOARD/summary-YYYY-MM-DD.md`

---

## Model Tier

**Claude Sonnet** (or equivalent reasoning model).
This agent synthesises across four frameworks, uses live data, and produces human-facing
decision support — requires strong instruction-following and multi-source reasoning.
For a Groq-based pipeline: `llama-3.3-70b-versatile` is the closest match.
