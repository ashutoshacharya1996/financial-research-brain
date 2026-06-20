# Opportunity Schema

## Purpose

An Opportunity is the central object of the Opportunity Discovery Engine.

It represents a convergence of Theme + Evidence + Candidate Stocks + Timing + Risk that is specific enough and well-evidenced enough to direct research attention and, ultimately, investment consideration.

There are two record types: the **Opportunity Record** (conviction-stage) and the **Research Queue Entry** (early-signal stage). A stock can appear in the Research Queue without a full Opportunity Record behind it. An Opportunity Record requires higher evidence thresholds.

---

## Record Type 1: Opportunity Record

Stored in: `07_OPPORTUNITIES/active/<opportunity-id>.md`

| Field | Type | Description |
|---|---|---|
| `opportunity_id` | string | Unique slug. Format: `<theme-slug>-<YYYY>-Q<N>`. Example: `electric-grid-modernization-2025-Q2` |
| `theme_name` | string | Must reference an active theme in `06_THEMES/` |
| `theme_status` | enum | Emerging / Developing / Consensus — pulled from the linked theme record |
| `confidence_score` | decimal | 1.0–10.0. Scores above 8.0 require `contradictory_evidence` to be populated |
| `trend_direction` | enum | Accelerating / Stable / Weakening |
| `candidate_stocks` | list | Each entry: ticker + company name + one-sentence rationale specific to this opportunity |
| `why_now` | list | 2–4 concrete timing catalysts. Must cite specific evidence (order book values, policy announcements, capacity commissioning dates, guidance revisions) |
| `risks` | list | 2–4 specific risk factors (valuation, execution, regulatory, competitive displacement) |
| `evidence_sources` | list | Source documents from this week. Each entry: company name + document type + date |
| `corroboration_count` | integer | Number of distinct companies whose documents evidence this theme. Minimum 3 required for an active Opportunity Record |
| `contradictory_evidence` | text | What argues against this opportunity. Required when confidence_score > 8.0 |
| `date_identified` | ISO date | When this Opportunity was first created |
| `last_validated` | ISO date | When evidence was last re-checked |
| `status` | enum | Active / Monitoring / Closed |

### Status Definitions

- **Active** — evidence is current, confidence is holding or rising, warrants ongoing research
- **Monitoring** — theme is still valid but signal has weakened; carry forward with reduced weight
- **Closed** — thesis has played out, been broken, or is now consensus and no longer actionable

---

## Record Type 2: Research Queue Entry

Stored in: `07_OPPORTUNITIES/weekly/YYYY-MM-DD.md` (Section 1 of weekly report)

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1–10, determined by the Opportunity Screener each week |
| `ticker` | string | NSE ticker symbol |
| `company_name` | string | Full company name |
| `reason` | string | One sentence. Must be specific and evidence-backed. Not generic. |
| `linked_opportunity_id` | string | Optional. Reference to an Opportunity Record if one exists |
| `source_signal` | string | What triggered this entry: earnings call mention / filing keyword / theme acceleration / delta signal |
| `week_of` | ISO date | The Sunday on which this report was published |

### Relationship Between Record Types

```
Research Queue Entry  →  (may graduate to)  →  Opportunity Record
     (early signal)                              (conviction-stage)
```

A queue entry requires: one named source document as evidence.
An opportunity record requires: corroboration_count ≥ 3, ≥ 2 timing catalysts, ≥ 1 articulated risk.

---

## Opportunity Lifecycle

```
Signal detected (queue entry)
        ↓
Evidence accumulates across multiple companies
        ↓
Opportunity Record created (status: Active)
        ↓
Evidence strengthens → confidence_score rises
        ↓
Theme plays out / goes consensus / breaks
        ↓
Status → Closed → moved to 07_OPPORTUNITIES/closed/
```
