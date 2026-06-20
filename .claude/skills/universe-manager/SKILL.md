---
name: universe-manager
description: >
  Universe Manager for the Opportunity Discovery Engine. Trigger when the user wants to
  generate or update the company universe in 01_UNIVERSE/company_master.csv. Reads from
  universe_definition.md and priority sources (financial advisor outputs, custom watchlists,
  Nifty 500). Run this first before any other agent. Trigger on: "run universe manager",
  "update company list", "populate universe", "rebuild company master", "which companies
  should we track".
---

# Universe Manager

## Objective

Generate and maintain `01_UNIVERSE/company_master.csv` — the master list of companies actively tracked by the Opportunity Discovery Engine.

---

## Inputs

| Input | Location |
|---|---|
| Universe definition and priority rules | `01_UNIVERSE/universe_definition.md` |
| Financial advisor outputs (highest priority) | If provided by user in conversation |
| Custom watchlists (second priority) | If provided by user in conversation |
| Market index definitions (fallback) | Nifty 50 / Nifty Next 50 / Nifty 500 |

---

## Process

**Step 1** — Read `01_UNIVERSE/universe_definition.md` to confirm current rules.

**Step 2** — Determine universe source using priority order:
1. Financial advisor output (if present in conversation)
2. Custom watchlist (if provided by user)
3. Nifty 500 (default fallback)

**Step 3** — Retrieve the company list from the chosen source.

**Step 4** — Remove duplicates (same company appearing via multiple sources).

**Step 5** — Populate all fields for each company:
- `ticker` — NSE ticker symbol
- `company_name` — full legal name
- `sector` — GICS or NSE sector classification
- `source` — which source this company came from
- `last_updated` — today's date

**Step 6** — Write to `01_UNIVERSE/company_master.csv`.

---

## Output

`01_UNIVERSE/company_master.csv` with headers:
```
ticker,company_name,sector,source,last_updated
```

---

## Rules

- Never hardcode companies. Always generate from source definitions.
- Prefer financial advisor outputs over indices.
- Log any companies where data is missing or ambiguous.
- If starting from Nifty 500, use the current constituent list — not a memorised one. Fetch via web search if needed.
