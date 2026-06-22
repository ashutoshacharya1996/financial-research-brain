# Portfolio Inputs

## Purpose

Portfolio Inputs is the handoff zone between research discovery and investment decisions.

The Opportunity Discovery Engine produces **research signals** — "here's what changed, here's why it matters." Portfolio Inputs decides **whether those signals warrant investment action** — deeper underwriting, watchlist priority, or continued monitoring only.

## Decision Authority

| Stage | Agent | Output | Authority |
|-------|-------|--------|-----------|
| Delta Analysis | Delta Agent | What changed vs. prior period | Factual only — no opinions |
| Theme Detection | Theme Agent | Cross-company patterns | Signal strength and corroboration count |
| Opportunity Screener | Opportunity Screener | Top 10 + Top 3 research queue | Which signals are strongest |
| **Portfolio Handoff** | Opportunity Screener | 3 names for deeper review | Which deserve Investment Impact notes |
| **Investment Impact** | Investment Impact Agent | Impact assessment + decision | Pass / Watchlist / Deep Dive / Ignore |
| India Stock Picker | India Stock Picker | Valuation + quality gates | Pass / Watchlist / Buy candidate |
| Portfolio Fit | Financial Advisor | Personal fit + allocation | Add / Hold / Reduce / Exit |

## Key Principle

**Opportunity Discovery finds where to look. Investment Impact decides whether underwriting is needed. India Stock Picker decides Pass/Watchlist/Buy. Portfolio Fit decides whether Ashutosh actually allocates capital.**

Nobody in this chain decides to buy. The decision flows downward, with each layer enforcing its own gates. A positive opportunity signal cannot force a buy if Investment Impact flags a blocker (e.g. weak cash conversion, governance issue, valuation red flag, missing portfolio context).

## Folder Structure

```
08_PORTFOLIO_INPUTS/
  README.md                          (this file)
  investment_impact_template.md       (template for impact notes)
  investment-impact/                 (live impact notes, one per company per date)
    JNKINDIA-impact-2026-06-22.md
    BEL-impact-2026-06-22.md
    (etc.)
  weekly-brief-YYYY-MM-DD.md         (human-readable summary for the week)
```

## Workflow

1. **Sunday night:** Opportunity Screener identifies 3 candidates for Investment Impact review
2. **Monday morning:** Investment Impact Agent writes impact notes for those 3
3. **By Wednesday:** India Stock Picker deep-dives names flagged for Re-run or Upgrade
4. **By Friday:** Portfolio Fit decides allocation if picker recommends

## Files

- `investment_impact_template.md` — structure and fields for every impact note
- `investment-impact/` — timestamped impact notes (one per company per review cycle)
