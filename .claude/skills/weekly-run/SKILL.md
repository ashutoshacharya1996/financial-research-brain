---
name: weekly-run
description: >
  Orchestrator for the Opportunity Discovery Engine weekly pipeline. Runs all
  pipeline stages in dependency order and commits outputs after each stage.
  Trigger when the user wants to run the full pipeline end-to-end.
  Trigger on: "run the pipeline", "weekly run", "full scan", "run everything",
  "Monday run", "trigger the engine", "run all agents".
model: sonnet
---

# Weekly Run — Pipeline Orchestrator

## Objective

Run the Monday pipeline in full dependency order. The Sunday automation (`fetch_evidence.py`) runs separately and automatically. This orchestrator processes what Sunday collected.

Final deliverable: `08_PORTFOLIO_INPUTS/weekly-brief-<YYYY-MM-DD>.md`

---

## Context: Sunday vs Monday

```
SUNDAY (automated, Python, no AI, no API keys):
  fetch_evidence.py
  ├── Lane A → 02_RAW_DOCUMENTS/<TICKER>/       (company evidence)
  └── Lane B → 02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/  (broad market signals)

MONDAY (Claude, 4 steps — this orchestrator):
  Step 1a: /discovery-news-agent   (review discovery, write summary)
  Step 1b: /universe-manager       (update universe from summary)
  Step 2:  /extraction-agent → /delta-agent → /theme-agent
  Step 3:  /opportunity-screener   (Top 10 + Top 3 + Portfolio Handoff)
  Step 4:  /investment-impact      (for Portfolio Handoff names only)
```

---

## Execution

Run each step fully before starting the next. If a step produces no output, log it and continue — do not abort.

---

### Step 1a — Discovery News Agent

Invoke: `/discovery-news-agent`

Reads `02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/discovery-news.md`.
Produces `02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/discovery-summary.md`.

If no discovery file exists from this week: log "No discovery data — Lane B may not have run" and continue to Step 1b with prior week's summary if available.

Commit message: `chore: discovery news summary YYYY-MM-DD`

---

### Step 1b — Universe Manager

Invoke: `/universe-manager`

Reads the discovery summary from Step 1a plus the live Nifty 1000.
Updates `01_UNIVERSE/company_master.csv` — promotes, deprioritizes, or adds companies.
Writes `01_UNIVERSE/discovery-log-YYYY-MM-DD.md`.

This is the only step that modifies the universe CSV.

Commit message: `chore: universe update YYYY-MM-DD`

---

### Step 2 — Evidence Processing

For all companies where `fetch_enabled=true` in `01_UNIVERSE/company_master.csv`:

**2a — Extraction Agent**
Invoke: `/extraction-agent`
Processes new documents in `02_RAW_DOCUMENTS/<TICKER>/`.
Writes to `03_EXTRACTED_DATA/`.
If no new documents: log and continue.

**2b — Delta Agent**
Invoke: `/delta-agent`
Compares current vs prior period for each company.
Writes to `04_COMPANY_ANALYSIS/<TICKER>/`.
If no prior period: write baseline and flag.

**2c — Theme Agent**
Invoke: `/theme-agent`
Clusters cross-company signals into themes.
Updates `06_THEMES/` records.
Writes `06_THEMES/theme-run-YYYY-MM-DD.md`.

Commit message: `feat: evidence processing YYYY-MM-DD`

---

### Step 3 — Opportunity Screener

Invoke: `/opportunity-screener`

Synthesises theme signals into:
- Top 10 Research Queue
- Top 3 High-Conviction Opportunities
- Portfolio Handoff (up to 3 names with strongest signal + strongest blocker)

Writes `07_OPPORTUNITIES/weekly/YYYY-MM-DD.md`.
Updates `07_OPPORTUNITIES/active/` records.

Commit message: `feat: weekly opportunity report YYYY-MM-DD`

---

### Step 4 — Investment Impact Notes

Invoke: `/investment-impact` for each Portfolio Handoff name from Step 3.

Writes `08_PORTFOLIO_INPUTS/investment-impact/<TICKER>-impact-YYYY-MM-DD.md`.

**Only for Portfolio Handoff names** — not for all Top 10 stocks.

Investment Impact routing options:
- Re-run full India Stock Picker review
- Upgrade watchlist priority
- Keep tracking only
- Ignore for now

Investment Impact must never output: Buy / Sell / Add / Exit

Then invoke: `/eli15-agent`
Converts the weekly opportunity report into the plain-English brief.
Writes `08_PORTFOLIO_INPUTS/weekly-brief-YYYY-MM-DD.md`.

Commit message: `feat: weekly brief YYYY-MM-DD`

---

## After All Steps

1. Print a summary of what each step produced (files written, counts).
2. Flag any steps that were skipped or produced no output.
3. Link to the final brief: `08_PORTFOLIO_INPUTS/weekly-brief-YYYY-MM-DD.md`
4. List the Portfolio Handoff names and their Investment Impact routing decisions.

---

## Error Handling

| Situation | Action |
|---|---|
| Step 1a fails (no discovery file) | Use prior week's summary if available; log warning; continue to 1b |
| Step 1b fails (Nifty 1000 fetch error) | Use existing company_master.csv; log warning; continue |
| No new documents in Step 2a | Skip extraction; run delta against prior extracted data |
| No new themes detected | Run Screener on existing theme records |
| Any step fails | Commit whatever was produced; log error; continue to next step |

---

## Decision Authority (for reference)

| Agent | Decides |
|---|---|
| Discovery News Agent | What signals appeared |
| Universe Manager | Universe membership and fetch priority |
| Delta Agent | What changed at the company level |
| Theme Agent | Cross-company signal patterns |
| Opportunity Screener | Where to direct research attention |
| Investment Impact Agent | Whether underwriting is warranted; what the blockers are |
| India Stock Picker | Pass / Watchlist / Buy candidate |
| Portfolio Fit | Whether Ashutosh should actually allocate capital |

No agent overrides a blocker from a downstream agent.

---

## Model Tier

**Claude Sonnet** (or equivalent reasoning model).
This agent coordinates other agents and makes stage-gate decisions.
For a Groq-based pipeline: `llama-3.3-70b-versatile` is the closest match.
