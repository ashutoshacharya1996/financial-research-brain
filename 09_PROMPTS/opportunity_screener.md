# Opportunity Screener

## Objective

Run every Sunday.

Synthesize all signals from the prior week — theme outputs, delta analysis, and new document arrivals — to produce the Weekly Opportunity Report:

1. **Top 10 Stocks for the Research Queue** — early-signal, one per stock, evidence-backed
2. **Top 3 High-Conviction Opportunities** — conviction-stage, meet full Opportunity Record thresholds

This is the engine's primary output. Every other agent feeds into this one.

---

## Inputs

| Input | Location |
|-------|---------|
| Active theme records | `06_THEMES/` |
| Extracted data from this week's documents | `03_EXTRACTED_DATA/` |
| Company-level delta and change detection outputs | `04_COMPANY_ANALYSIS/` |
| Sector-level trend notes | `05_SECTOR_ANALYSIS/` |
| Opportunity data model | `07_OPPORTUNITIES/opportunity_schema.md` |
| Prior week's report (for comparison) | `07_OPPORTUNITIES/weekly/` — most recent file |

---

## Process

### Step 1 — Load and Rank Active Themes

Load all theme records from `06_THEMES/`.

Filter to: Status = Emerging or Developing. Exclude Consensus, Mature, Declining, and Broken themes — those are no longer actionable.

Rank remaining themes by `corroboration_count` descending. This surfaces themes with the most cross-company evidence first.

---

### Step 2 — Identify Candidate Stocks Per Theme

For each top-ranked theme, pull the Beneficiaries list from the theme record.

Cross-reference each Beneficiary against this week's outputs in `04_COMPANY_ANALYSIS/`. Prioritize stocks where both a theme-level signal and a company-level delta signal are present in the same week. Convergence of signals — theme acceleration + company-specific evidence — is the primary selection criterion.

---

### Step 3 — Score Each Candidate Stock

Score every candidate stock on four dimensions:

| Dimension | What to Measure |
|-----------|----------------|
| **Signal Strength** | How many distinct source documents this week mentioned this theme in the context of this company |
| **Delta** | Is the signal accelerating, stable, or weakening compared to last week's report |
| **Specificity** | Are there concrete numbers (order book values, guidance revisions, capex amounts, contract values) — not just general mentions |
| **Timing** | Is there a near-term catalyst: upcoming results, policy announcement, capacity commissioning, contract award |

Assign a composite rank. Do not use precise numerical formulas — use judgment grounded in the evidence. The goal is a defensible ranking, not a mechanical one.

---

### Step 4 — Select Top 10 Research Queue Entries

Take the highest-ranked 10 stocks. Write one-sentence reasons for each.

Rules for reasons:
- Must be specific to this week's evidence
- Must name the source signal (e.g. "per Q4 FY25 earnings call" or "per NSE filing dated 2025-04-12")
- Must not be generic (e.g. "strong fundamentals" is not acceptable)
- Must not carry forward from last week without re-validation

---

### Step 5 — Identify High-Conviction Opportunities

From the Top 10, identify up to 3 stocks or clusters where evidence is strong enough to create or update a full Opportunity Record.

An Opportunity Record requires all four:
- A named theme with a record in `06_THEMES/`
- `corroboration_count` ≥ 3 (at least 3 distinct companies evidencing this theme this week or cumulatively)
- ≥ 2 concrete timing catalysts
- ≥ 1 clearly articulated risk

Stocks that meet only some criteria remain in the Research Queue as entries without a linked Opportunity Record. Do not force a stock into Section 2 if the evidence threshold is not met.

---

### Step 6 — Write the Weekly Report

Write the weekly output file at:

```
07_OPPORTUNITIES/weekly/YYYY-MM-DD.md
```

Use the format defined in `07_OPPORTUNITIES/weekly_output_template.md` exactly.

The date in the filename is the Sunday on which this report is generated.

---

### Step 7 — Create or Update Opportunity Records

For each of the Top 3 Opportunities:

- Check whether a file already exists in `07_OPPORTUNITIES/active/` with the matching `opportunity_id`.
- If yes: update the record. Refresh `last_validated`, update `corroboration_count`, add new evidence sources, revise `confidence_score` if warranted, update `trend_direction`.
- If no: create a new file using the schema defined in `07_OPPORTUNITIES/opportunity_schema.md`. Set `date_identified` to today's date, `status` to Active.

---

### Step 8 — Update Theme Linkages

For each Opportunity created or updated:

1. Open the linked theme record in `06_THEMES/`.
2. Add or update the `opportunity_id` in the theme's `Linked Opportunities` field.
3. Increment the theme's `Research Queue Appearances` count for any of its associated stocks that appeared in this week's Top 10.

This maintains the bidirectional link: Theme → Opportunity → Research Queue Entry.

---

## Output Format

See `07_OPPORTUNITIES/weekly_output_template.md` for the exact format.

Summary:
- **Section 1:** Markdown table, 10 rows, one stock per row with rank, reason, signal source, and optional opportunity link
- **Section 2:** Structured block per Opportunity — theme, confidence, trend, stocks, why-now bullets, risk bullets, evidence count, link to active file
- **Signal Notes:** 2–4 sentences on what changed vs. last week

---

## Rules

1. Every stock in the Top 10 must have a named source document as evidence. Undocumented signals are excluded.
2. Every Opportunity Record must have `corroboration_count` ≥ 3. Do not create an Opportunity Record for a single-company signal, no matter how strong.
3. Confidence scores above 8.0 require `contradictory_evidence` to be populated. High conviction without acknowledged risk is not permitted.
4. Do not carry forward last week's Top 10 unchanged. Every entry must be re-validated from this week's signals. An entry can return to the list, but its reason must cite this week's evidence.
5. Opportunities are research hypotheses, not investment recommendations. Do not frame them as buy calls.
6. If a theme's `trend_direction` changed to Weakening since last week, any linked Opportunity must be flagged for re-validation and its `confidence_score` reviewed.
7. The report must be written before end of Sunday. It covers signals from the Monday–Saturday window of the prior week.
