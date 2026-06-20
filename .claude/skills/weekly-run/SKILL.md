---
name: weekly-run
description: >
  Orchestrator for the Opportunity Discovery Engine weekly pipeline. Runs all 7 agents
  in sequence and commits outputs after each stage. Trigger when the user wants to run
  the full pipeline end-to-end, or when the weekly GitHub Actions cron fires.
  Trigger on: "run the pipeline", "weekly run", "full scan", "run everything",
  "Sunday run", "trigger the engine", "run all agents".
model: sonnet
---

# Weekly Run — Pipeline Orchestrator

## Objective

Run all 7 pipeline agents in dependency order. Commit outputs after each stage so partial runs are recoverable. The full pipeline produces one deliverable: `08_PORTFOLIO_INPUTS/weekly-brief-<YYYY-MM-DD>.md`.

---

## Execution Order

Run each stage fully before starting the next. If a stage produces no output (no new documents, no changes detected), log it and continue — do not abort.

### Stage 1 — Universe Manager
Invoke: `/universe-manager`

Refreshes `01_UNIVERSE/company_master.csv` with live Nifty 1000 constituents + news-discovered stocks.

Commit message: `chore: universe refresh YYYY-MM-DD`

---

### Stage 2 — Collection Agent
Invoke: `/collection-agent`

Catalogues latest documents for all companies in `company_master.csv`. Writes `02_RAW_DOCUMENTS/<TICKER>/catalogue.md`.

Commit message: `chore: document catalogue update YYYY-MM-DD`

---

### Stage 3 — Extraction Agent
Invoke: `/extraction-agent`

Processes any new documents found in Stage 2. Writes structured signal files to `03_EXTRACTED_DATA/`.

If no new documents: log "No new documents to extract" and continue.

Commit message: `feat: extracted signals YYYY-MM-DD`

---

### Stage 4 — Delta Agent
Invoke: `/delta-agent`

Compares current extracted data against prior period for each company. Writes delta reports to `04_COMPANY_ANALYSIS/`.

If no prior period data exists for a company: write a baseline file and flag.

Commit message: `feat: delta analysis YYYY-MM-DD`

---

### Stage 5 — Theme Agent
Invoke: `/theme-agent`

Clusters signals from delta reports into cross-company themes. Updates `06_THEMES/` records and writes `06_THEMES/theme-run-<YYYY-MM-DD>.md`.

Commit message: `feat: theme detection YYYY-MM-DD`

---

### Stage 6 — Opportunity Screener
Invoke: `/opportunity-screener`

Synthesises themes into Top 10 research queue + Top 3 high-conviction opportunities. Writes `07_OPPORTUNITIES/weekly/<YYYY-MM-DD>.md` and updates `07_OPPORTUNITIES/active/`.

Commit message: `feat: weekly opportunity report YYYY-MM-DD`

---

### Stage 7 — ELI15 Agent
Invoke: `/eli15-agent`

Converts the weekly opportunity report into a plain English brief. Writes `08_PORTFOLIO_INPUTS/weekly-brief-<YYYY-MM-DD>.md`.

Commit message: `feat: weekly brief YYYY-MM-DD`

---

## After All Stages

1. Print a summary of what each stage produced (files written, counts).
2. Flag any stages that were skipped or produced no output.
3. Link to the final brief: `08_PORTFOLIO_INPUTS/weekly-brief-<YYYY-MM-DD>.md`

---

## Error Handling

| Situation | Action |
|---|---|
| Stage fails | Log the error, commit whatever was produced, continue to next stage |
| No Nifty 1000 data available (network error) | Abort Stage 1, use existing company_master.csv, continue from Stage 2 |
| No documents collected | Skip Stages 3–4, run Stages 5–7 on prior period data |
| No new themes detected | Run Screener on existing theme records |

---

## Model Tier

**Claude Sonnet** (or equivalent reasoning model).
This agent coordinates other agents and makes stage-gate decisions — requires strong
instruction-following and reasoning.
For a Groq-based pipeline: `llama-3.3-70b-versatile` is the closest match.
