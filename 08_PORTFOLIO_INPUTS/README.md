# 08_PORTFOLIO_INPUTS

## Purpose

This folder is the handoff between the Opportunity Discovery Engine and the
separate stock-selection / portfolio-construction process.

The Opportunity Engine answers: "Where is evidence moving?"

Portfolio Inputs answer: "What does that evidence change about an investment
decision?"

No file in this folder is allowed to be a buy or sell recommendation by itself.
It may trigger a deeper India Stock Picker review, upgrade a watchlist priority,
or document blockers that prevent capital allocation.

---

## Folder Structure

```text
08_PORTFOLIO_INPUTS/
  README.md
  investment_impact_template.md
  weekly-brief-YYYY-MM-DD.md
  investment-impact/
    <TICKER>-impact-YYYY-MM-DD.md
```

---

## Output Types

### Weekly Brief

The weekly brief is a human-readable summary of the research queue and active
opportunities. It explains what changed, what matters, and what should be
watched next.

It is not an underwriting document.

### Investment Impact Note

An investment impact note is the formal bridge from discovery to underwriting.
It is created when a stock in the research queue or an active opportunity has a
material new signal that could affect:

- growth
- margins
- cash conversion
- moat
- management quality
- valuation
- portfolio fit

It must clearly separate positive evidence from actual buyability.

---

## Decision Authority

| Layer | Job | Allowed Output |
|---|---|---|
| Delta Analysis | Detect what changed | Positive / negative / neutral signal |
| Theme Detection | Connect signals across companies | Theme confidence and trend |
| Opportunity Screener | Rank where to research | Research queue and active opportunities |
| Investment Impact | Translate signal into underwriting impact | Re-run / upgrade watchlist / monitor / ignore |
| India Stock Picker | Underwrite business quality and valuation | Pass / Watchlist / Buy candidate |
| Portfolio Fit | Check holdings, sizing, and displacement | Actual portfolio action |

Rules:

1. A positive opportunity signal is not a buy signal.
2. A positive order-book or revenue delta must be checked against cash
   conversion and valuation.
3. A stock cannot move from "research queue" to "buy candidate" without an
   India Stock Picker review.
4. A buy candidate cannot become an actual portfolio action without live
   portfolio and position-size checks.

