---
name: weekly-run
description: >
  Orchestrator for the weekly pipeline (redesigned 2026-11-16: broad market + mutual funds,
  not individual stocks). Checks the Sunday market fetch, runs /market-brief, commits, and
  notifies. Trigger on: "run the pipeline", "weekly run", "full scan", "run everything",
  "Monday run", "trigger the engine", "run all agents", "new evidence is in",
  "run the pipeline from extraction onwards".
model: sonnet
---

# Weekly Run — Market Brief Pipeline

## What changed (2026-11-16)

The user asked to stop tracking a fixed set of six stocks and instead track the broad
market across industries, centred on the mutual funds he holds. The weekly output is now
one super-simple brief: what happened, what to note, opportunities in play, and
Bull/Base/Bear odds.

**Legacy prompts map to the new pipeline.** "New evidence is in. Run the pipeline from
extraction onwards" (the scheduled routine's wording) means: run the steps below. Do NOT
run extraction-agent, delta-agent, theme-agent, opportunity-screener, investment-impact or
eli15-agent as part of the weekly run. Those skills still exist for on-demand stock research.

```
SUNDAY 09:00 IST (GitHub Action, no AI):
  scripts/fetch_market.py → 02_RAW_DOCUMENTS/_market/YYYY-MM-DD/
     market-snapshot.json · market-summary.md · news.md

MONDAY (Claude, this orchestrator):
  Step 1  Check the fetch
  Step 2  /market-brief  → 08_PORTFOLIO_INPUTS/market-brief-YYYY-MM-DD.md
  Step 3  Commit, push, notify
```

---

## Step 1 — Check the fetch

`git pull` (or fetch the default branch) and find the newest `02_RAW_DOCUMENTS/_market/<date>/`.

- Missing, or older than 8 days → the Sunday Action didn't run. Notify the user with that
  fact (and the Action's last run status if the GitHub tools can see it). Stop.
- Present → read `source_status` at the bottom of `market-summary.md`. If more than half the
  sources failed, still write the brief but lead the notification with the data gap.

## Step 2 — Market brief

Invoke `/market-brief` and follow it exactly.

## Step 3 — Commit, push, notify

- Commit message: `feat: market brief YYYY-MM-DD`
- Push to the session's working branch; open a draft PR if none is open.
- Send one notification. Banner = the Bull/Base/Bear odds + the single most important
  "take note" item (or "nothing needs your attention"). Body = the 3–4 line gist of the
  brief and the file path. A quiet week still gets a notification — the brief is the
  deliverable the user is waiting for.

---

## Error handling

| Situation | Action |
|---|---|
| No `_market/` folder this week | Notify "Sunday fetch didn't run"; do not write a brief from memory |
| Some sources failed | Write the brief; list gaps in its footer |
| Fund NAVs missing for a fund | Show "—" for that row; footer says to set `scheme_code` in `01_UNIVERSE/mf_watchlist.csv` |
| Kite unavailable | Use `mf_watchlist.csv`; footer says holdings not re-verified |

## Model Tier

Claude Sonnet (or equivalent).
