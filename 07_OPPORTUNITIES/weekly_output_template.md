# Weekly Opportunity Report — Template

This file defines the exact format the Opportunity Screener must produce every Sunday.

Each Sunday's report is saved as: `07_OPPORTUNITIES/weekly/YYYY-MM-DD.md`

---

## Template

```
# Weekly Opportunity Report — [YYYY-MM-DD]

---

## Section 1: Research Queue — Top 10 Stocks Worth Investigating

These are not buy recommendations. This is your research queue for the week.

| Rank | Stock | Reason | Signal Source | Opportunity Link |
|------|-------|--------|---------------|-----------------|
| 1 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |
| 2 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |
| 3 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |
| 4 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |
| 5 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |
| 6 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |
| 7 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |
| 8 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |
| 9 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |
| 10 | [Company Name] | [One-sentence, evidence-specific reason] | [Document type + company + date] | [opportunity-id or —] |

---

## Section 2: High-Conviction Opportunities

These meet the full Opportunity Record threshold: ≥ 3 corroborating companies, ≥ 2 timing catalysts, ≥ 1 articulated risk.

---

### Opportunity #1

**Theme:** [Theme name — must exist in 06_THEMES/]
**Confidence:** [X.X / 10]
**Trend:** [Accelerating / Stable / Weakening]
**Stocks:** [Ticker1, Ticker2, Ticker3]

**Why Now:**
- [Specific catalyst with evidence — e.g. "Order book up 34% YoY per Siemens Q4 call"]
- [Specific catalyst with evidence]
- [Specific catalyst with evidence]

**Risks:**
- [Specific risk — e.g. "Valuations at 40x P/E leave no room for execution miss"]
- [Specific risk]

**Evidence:** [N] companies this week | [List: Company – Document Type – Date]
**Opportunity File:** active/[opportunity-id].md

---

### Opportunity #2

**Theme:** [Theme name]
**Confidence:** [X.X / 10]
**Trend:** [Accelerating / Stable / Weakening]
**Stocks:** [Ticker1, Ticker2, Ticker3]

**Why Now:**
- [Catalyst]
- [Catalyst]

**Risks:**
- [Risk]
- [Risk]

**Evidence:** [N] companies this week | [List: Company – Document Type – Date]
**Opportunity File:** active/[opportunity-id].md

---

### Opportunity #3

**Theme:** [Theme name]
**Confidence:** [X.X / 10]
**Trend:** [Accelerating / Stable / Weakening]
**Stocks:** [Ticker1, Ticker2, Ticker3]

**Why Now:**
- [Catalyst]
- [Catalyst]

**Risks:**
- [Risk]
- [Risk]

**Evidence:** [N] companies this week | [List: Company – Document Type – Date]
**Opportunity File:** active/[opportunity-id].md

---

## Signal Notes

[2–4 sentences. What changed vs. last week? Which themes strengthened, which weakened, any new themes entering the pipeline, any opportunities that were closed or downgraded.]

---

## Portfolio Handoff

These are not buy recommendations. They are the items that deserve an
Investment Impact note before any India Stock Picker review.

| Priority | Stock / Opportunity | Why It Needs Handoff | Required Next File |
|----------|---------------------|----------------------|--------------------|
| 1 | [Ticker or opportunity-id] | [Material signal and strongest blocker] | `08_PORTFOLIO_INPUTS/investment-impact/[TICKER]-impact-[YYYY-MM-DD].md` |
| 2 | [Ticker or opportunity-id] | [Material signal and strongest blocker] | `08_PORTFOLIO_INPUTS/investment-impact/[TICKER]-impact-[YYYY-MM-DD].md` |
| 3 | [Ticker or opportunity-id] | [Material signal and strongest blocker] | `08_PORTFOLIO_INPUTS/investment-impact/[TICKER]-impact-[YYYY-MM-DD].md` |
```

---

## Formatting Rules

- Section 1 reasons must be specific. "Strong order book" is not acceptable. "Order book up 34% YoY per Q4 earnings call" is acceptable.
- Section 2 confidence scores use one decimal place (e.g. 8.7, not 8 or 8.70).
- Every stock in Section 1 must have a named source document in the Signal Source column.
- Every Opportunity in Section 2 must have a corresponding file in `07_OPPORTUNITIES/active/`.
- Signal Notes must reference at least one change from the prior week's report.
- Portfolio Handoff must list only signals material enough to affect underwriting.
- Portfolio Handoff must name the strongest blocker; positive evidence alone is not enough.
- Do not use Buy / Sell / Add / Exit language anywhere in the weekly report.
