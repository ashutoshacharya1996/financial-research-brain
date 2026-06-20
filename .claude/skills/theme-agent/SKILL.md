---
name: theme-agent
description: >
  Theme Agent for the Opportunity Discovery Engine. Trigger when the user wants to detect,
  update, or score cross-company themes from this week's extracted signals and delta outputs.
  Reads from 03_EXTRACTED_DATA/ and 04_COMPANY_ANALYSIS/, writes theme records to 06_THEMES/.
  Run after delta agent, before opportunity screener. Trigger on: "run theme detection",
  "update themes", "what themes are emerging", "cluster signals into themes",
  "theme analysis", "which themes are strengthening".
---

# Theme Agent

## Objective

Identify and update cross-company themes — patterns that appear across multiple companies' documents in the same week.

A theme is not a sector. A sector is static. A theme is a signal with direction: it is either strengthening, stable, or weakening, and it is visible across multiple companies' own words.

One company mentioning grid modernisation is noise. Seven companies mentioning it, three of them with order book data to back it up, is a theme.

---

## Inputs

| Input | Location |
|---|---|
| This week's theme signal logs | `03_EXTRACTED_DATA/*/` — Theme Signal Log sections |
| This week's delta outputs | `04_COMPANY_ANALYSIS/*/delta-<latest>.md` — Theme Signal Deltas |
| Existing theme records | `06_THEMES/` — all current theme files |
| Theme dashboard definition | `06_THEMES/theme_dashboard_definition.md` |

---

## Process

### Step 1 — Aggregate This Week's Theme Signals

Scan every Theme Signal Log from this week's extracted documents and every Theme Signal Delta from this week's delta outputs.

Build a raw signal list:

```
Theme Category | Company | Signal Type | Strength | Quote
```

### Step 2 — Count Corroboration

For each theme category, count:
- How many distinct companies mentioned it this week
- How many had it as a **new mention** (vs recurring)
- How many had it with **Strengthening** delta vs **Fading** delta
- How many cited **concrete numbers** (order values, capex amounts, capacity figures) vs general language

`corroboration_count` = number of distinct companies with evidence this week.

### Step 3 — Classify Each Theme

For each theme with corroboration_count ≥ 2, classify:

**Status** (where is it in its lifecycle?):
- **Emerging** — appearing for the first time across multiple companies, no prior theme record
- **Developing** — has a prior record, corroboration_count growing, signal strengthening
- **Consensus** — widely known, appearing in analyst reports and media, no longer early
- **Mature** — well-established, growth in mentions slowing
- **Declining** — fewer companies mentioning it vs prior periods
- **Broken** — companies that were primary evidence are now contradicting the thesis

**Trend Direction** (what happened this week vs last week?):
- **Accelerating** — corroboration_count up, stronger language, more concrete data
- **Stable** — similar count and language as last week
- **Weakening** — count down, language more hedged, fewer concrete numbers

### Step 4 — Score Confidence (1–10)

Confidence is not a gut feel. It is a function of:

| Factor | High confidence | Low confidence |
|---|---|---|
| Corroboration count | ≥ 5 companies | 2–3 companies |
| Evidence type | Concrete numbers (order values, ₹ capex) | General language only |
| Management specificity | Named timelines, named customers | Vague positive commentary |
| Contradictory evidence | None or minor | Present and material |
| Duration | Theme has been consistent ≥ 3 weeks | New this week only |

Assign a decimal score (e.g. 7.4, not just 7). Write one sentence justifying the score.

### Step 5 — Update or Create Theme Records

For each theme:

- **If a theme file already exists in `06_THEMES/`**: update it. Refresh `corroboration_count`, `confidence_score`, `trend_direction`, `status`, `last_updated`, and append new evidence to `Evidence` and `Supporting Data`.
- **If no theme file exists**: create one using the structure in `theme_dashboard_definition.md`.

File naming: `06_THEMES/<theme-slug>.md` (e.g. `electric-grid-modernization.md`)

### Step 6 — Flag Broken Themes

If any existing theme now has contradictory evidence from ≥ 2 companies this week, update its status to **Declining** or **Broken** and document the contradictions explicitly in the `Counter Arguments` field.

Do not delete broken themes. Archive them with `status: Broken` and the date they broke.

---

## Output Format

Each theme file follows `06_THEMES/theme_dashboard_definition.md` exactly:

```markdown
# Theme: [Theme Name]

## Status
[Emerging / Developing / Consensus / Mature / Declining / Broken]

## Confidence Score
[X.X / 10]
Justification: [one sentence]

## Trend Direction
[Accelerating / Stable / Weakening]

## Evidence

Companies mentioning this theme this week:
| Company | Document | Date | Signal Type | Strength | Quote |
|---|---|---|---|---|---|
| | | | | | |

## Supporting Data

Filings, earnings calls, and presentations providing concrete data:
- [Company] — [document type] — [date]: [specific data point, e.g. "order book up 34% YoY"]

## Beneficiaries

Companies likely to gain from this theme:
- [Company] — [reason, one sentence]

## Linked Opportunities

Opportunity Records in 07_OPPORTUNITIES/active/ grounded in this theme:
- [opportunity-id] — Confidence: X.X / Status: Active|Monitoring|Closed

## Research Queue Appearances

Appearances of theme-related stocks in weekly Top 10 over last 4 weeks: [N]

## Potential Losers

Companies likely to be negatively impacted:
- [Company] — [reason]

## Game Theory View

Who captures the economics of this theme?
Who gets squeezed?
Who gains bargaining power?

## Counter Arguments

Evidence against this theme, or reasons it may not play out:
- [specific counter-evidence with source]

## Corroboration Count
[N] companies this week | [N] companies cumulative

## Last Updated
[YYYY-MM-DD]
```

---

## Theme Run Summary

At the end of each run, write a summary to `06_THEMES/theme-run-<YYYY-MM-DD>.md`:

```markdown
# Theme Agent Run — [YYYY-MM-DD]

## Themes Updated
- [theme name] — [status] — [confidence] — [trend]

## Themes Created
- [theme name] — new, corroboration: N

## Themes Downgraded
- [theme name] — [old status] → [new status] — reason

## Themes Broken
- [theme name] — broken by: [company evidence]

## Top 5 by Corroboration Count
1. [theme] — N companies
2.
3.
4.
5.

## Ready for Opportunity Screener
Themes passing to screener (Emerging or Developing, confidence ≥ 5.0):
- [theme list]
```

---

## Rules

1. **Corroboration minimum is 2.** A single-company signal is not a theme — leave it in the delta output and revisit next week.
2. **Concrete evidence ranks above language.** A theme with one company citing specific order values outweighs three companies using vague positive language.
3. **Update, don't rewrite.** When updating an existing theme, add to the evidence table — don't delete prior evidence. Themes have memory.
4. **Broken themes stay.** Mark as Broken, document why, keep the file. Broken themes are learning data.
5. **Confidence > 8.0 requires explicit counter-arguments.** High conviction must acknowledge its own weaknesses.
6. **Write the run summary last.** It is the handoff document to the Opportunity Screener.
