# Opportunity Schema

## Purpose

An Opportunity is the central object of the Opportunity Discovery Engine.

It represents a convergence of Theme + Evidence + Candidate Stocks + Timing + Risk that is specific enough and well-evidenced enough to direct research attention.

**Important:** Opportunity Records are **research objects**, not buy recommendations. They signal "where to look." A positive Opportunity Record is the START of underwriting, not the end. The Investment Impact Agent decides whether the signal warrants deeper review. The India Stock Picker gate-checks valuation and quality. The Portfolio Fit stage decides personal allocation. Positive signals cannot override failed quality gates, weak cash conversion, valuation red flags, or portfolio constraints.

There are two record types: the **Opportunity Record** (conviction-stage) and the **Research Queue Entry** (early-signal stage). A stock can appear in the Research Queue without a full Opportunity Record behind it. An Opportunity Record requires higher evidence thresholds.

---

## Record Type 1: Opportunity Record

Stored in: `07_OPPORTUNITIES/active/<opportunity-id>.md`

| Field                    | Type     | Description                                                                                                                                            |
| ------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `opportunity_id`         | string   | Unique slug. Format: `<theme-slug>-<YYYY>-Q<N>`. Example: `electric-grid-modernization-2026-Q1`                                                        |
| `theme_name`             | string   | Must reference an active theme in `06_THEMES/`                                                                                                         |
| `theme_status`           | enum     | Emerging / Developing / Consensus — pulled from the linked theme record                                                                                |
| `opportunity_stage`      | enum     | Discovery / Validation / Conviction                                                                                                                    |
| `confidence_score`       | decimal  | 1.0–10.0. Scores above 8.0 require `contradictory_evidence` to be populated                                                                            |
| `trend_direction`        | enum     | Accelerating / Stable / Weakening                                                                                                                      |
| `expected_horizon`       | enum     | 6-12m / 1-3y / 3-5y / 5y+                                                                                                                              |
| `candidate_stocks`       | list     | Each entry contains ticker, company name, rationale, and opportunity_fit_score                                                                         |
| `why_now`                | list     | 2–4 concrete timing catalysts. Must cite specific evidence (order book values, policy announcements, capacity commissioning dates, guidance revisions) |
| `risks`                  | list     | 2–4 specific risk factors (valuation, execution, regulatory, competitive displacement)                                                                 |
| `thesis_breakers`        | list     | Events that would invalidate the opportunity thesis                                                                                                    |
| `evidence_sources`       | list     | Source documents from this week. Each entry: company name + document type + date                                                                       |
| `corroboration_count`    | integer  | Number of distinct companies whose documents evidence this theme. Minimum 3 required for an active Opportunity Record                                  |
| `contradictory_evidence` | text     | What argues against this opportunity. Required when confidence_score > 8.0                                                                             |
| `date_identified`        | ISO date | When this Opportunity was first created                                                                                                                |
| `last_validated`         | ISO date | When evidence was last re-checked                                                                                                                      |
| `status`                 | enum     | Active / Monitoring / Closed                                                                                                                           |

---

## Candidate Stock Structure

Each stock should be stored as:

```yaml
candidate_stocks:

  - ticker: SIEMENS
    company_name: Siemens India
    opportunity_fit_score: 9.2
    rationale: Direct beneficiary of transmission and distribution capex expansion.

  - ticker: ABB
    company_name: ABB India
    opportunity_fit_score: 8.8
    rationale: Strong exposure to grid automation and power equipment demand.

  - ticker: CGPOWER
    company_name: CG Power
    opportunity_fit_score: 8.4
    rationale: Beneficiary of transformer and switchgear demand growth.
```

### Opportunity Fit Score

Measures how strongly a company is positioned to benefit from the opportunity.

Scale:

* 9–10 = Primary beneficiary
* 7–8 = Strong beneficiary
* 5–6 = Secondary beneficiary
* <5 = Weak or indirect exposure

This score is not a valuation score.

It measures strategic exposure to the opportunity.

---

## Opportunity Stage Definitions

### Discovery

Theme is emerging.

Evidence exists but remains limited.

Research should focus on validation.

Typical characteristics:

* Corroboration count below 3
* Limited management commentary
* Early signals appearing

### Validation

Evidence is accumulating.

Multiple companies are independently confirming the same story.

Typical characteristics:

* Corroboration count ≥ 3
* Multiple evidence sources
* Clear timing catalysts

### Conviction

Evidence is strong and consistent.

Suitable for India Stock Picker review and portfolio consideration.

Typical characteristics:

* Multiple corroborating companies
* Strong timing catalysts
* Risks understood
* Thesis remains differentiated from consensus

---

## Status Definitions

### Active

Evidence is current, confidence is holding or rising, warrants ongoing research.

### Monitoring

Theme remains valid but signal has weakened.

Carry forward with reduced weight and increased scrutiny.

### Closed

Thesis has played out, broken, or become fully consensus and no longer offers meaningful opportunity.

---

## Record Type 2: Research Queue Entry

Stored in: `07_OPPORTUNITIES/weekly/YYYY-MM-DD.md` (Section 1 of weekly report)

| Field                   | Type     | Description                                                                                           |
| ----------------------- | -------- | ----------------------------------------------------------------------------------------------------- |
| `rank`                  | integer  | 1–10, determined by the Opportunity Screener each week                                                |
| `ticker`                | string   | NSE ticker symbol                                                                                     |
| `company_name`          | string   | Full company name                                                                                     |
| `reason`                | string   | One sentence. Must be specific and evidence-backed. Not generic.                                      |
| `linked_opportunity_id` | string   | Optional. Reference to an Opportunity Record if one exists                                            |
| `source_signal`         | string   | What triggered this entry: earnings call mention / filing keyword / theme acceleration / delta signal |
| `week_of`               | ISO date | The Sunday on which this report was published                                                         |

---

## Relationship Between Record Types

```text
Research Queue Entry
        ↓
   Early Signal
        ↓
Evidence Accumulates
        ↓
Opportunity Record
        ↓
India Stock Picker
        ↓
Financial Advisor
        ↓
Portfolio Action
```

A queue entry requires:

* One named source document as evidence

An opportunity record requires:

* Corroboration count ≥ 3
* At least 2 timing catalysts
* At least 1 articulated risk
* Defined thesis breakers

---

## Opportunity Lifecycle

```text
Signal detected
(Research Queue)

        ↓

Evidence accumulates across multiple companies

        ↓

Opportunity Record created
(Stage: Discovery)

        ↓

Corroboration increases
Catalysts identified

        ↓

Stage: Validation

        ↓

Evidence strengthens
Confidence rises

        ↓

Stage: Conviction

        ↓

Portfolio Handoff
(Opportunity Screener identifies 3 candidates for deeper review)

        ↓

Investment Impact Note
(Fact-check signal, assess impact, identify blockers, gate underwriting)

        ↓

Routing Decision:
- Re-run India Stock Picker (Deep Dive)
- Upgrade Watchlist Priority
- Keep Tracking
- Ignore For Now

        ↓

India Stock Picker Review (if Impact Note flags for Deep Dive)

        ↓

Portfolio Fit Decision

        ↓

Status: Closed
(thesis played out, broken, or consensus)
```

---

## Example

```yaml
opportunity_id: electric-grid-modernization-2026-Q1

theme_name: Electric Grid Modernization

theme_status: Developing

opportunity_stage: Conviction

confidence_score: 8.7

trend_direction: Accelerating

expected_horizon: 5y+

corroboration_count: 6

candidate_stocks:
  - Siemens India
  - ABB India
  - CG Power

why_now:
  - Record transmission capex announced
  - Transformer demand exceeding supply
  - State utility modernization programs accelerating

risks:
  - Project execution delays
  - Valuation expansion already pricing in growth

thesis_breakers:
  - Transmission capex slowdown
  - Order growth drops below 10%
  - Major project cancellations

status: Active
```
