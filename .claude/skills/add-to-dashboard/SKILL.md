---
name: add-to-dashboard
description: |
  Add a new stock to the Portfolio Candidates view in docs/index.html.
  Reads the completed stock-dashboard output for the ticker, maps all fields
  to the STOCKS array schema, and edits docs/index.html directly.
  Input is Claude only — no UI form required.
  Trigger on: "add [TICKER] to dashboard", "/add-to-dashboard [TICKER]",
  "add [TICKER] to candidates", "add [TICKER] to the lineup"
model: sonnet
---

# Add to Dashboard

## Objective

Insert a new stock entry into the `STOCKS` array in `docs/index.html` so the stock appears in the Portfolio Candidates tab of the research dashboard. Claude does the edit — no UI form.

---

## Process

### Step 1 — Verify prerequisite

Check whether a completed dashboard file exists at `10_DASHBOARD/<TICKER>/dashboard-YYYY-MM-DD.md`.

- If no dashboard file exists: tell the user to run `/stock-dashboard <TICKER>` first, then come back.
- If a dashboard file exists: proceed.

### Step 2 — Extract STOCKS schema fields

Read the dashboard file and map its content to the following fields. Every field is required unless marked optional:

| Field | Source in dashboard |
|---|---|
| `id` | Ticker symbol (uppercase) |
| `name` | Full company name |
| `exchange` | NSE or BSE |
| `price` | Live price from Panel 1 buy zone bar |
| `priceDate` | Date of price (format: 'DD Mon YYYY') |
| `fv.bear` | Bear case fair value from Panel 1 |
| `fv.base` | Base case fair value from Panel 1 |
| `fv.bull` | Bull case fair value from Panel 1 |
| `zone` | One of: 'strong-buy', 'buy-zone', 'fair-value', 'watch', 'expensive' |
| `zoneLabel` | Human label: 'Strong Buy', 'Buy Zone', 'Fair Value', 'Watch', 'Expensive' |
| `themes` | Array of theme slugs: 'defence', 'capex', 'ev', 'infra', etc. |
| `sectors` | Array of sector tags: 'psu', 'defence', 'capital-goods', 'engineering', 'small-cap', etc. |
| `poised` | Poised Score (1.0–10.0 decimal) from Panel 1 |
| `action` | One of: 'add', 'watch', 'hold', 'avoid' |
| `actionLabel` | Human label: 'Add this week', 'Add on dip', 'Hold', 'Avoid' |
| `watchPrice` | Target entry price if action is 'watch' (null if action is 'add') |
| `pe` | PE ratio (integer) |
| `revenue` | Annual revenue in ₹cr (integer) |
| `orderBook` | Order book value in ₹cr (integer, or null if not applicable) |
| `obCoverage` | Order book as multiple of revenue (float, or null) |
| `corroboration` | Corroboration count from linked Opportunity Record |
| `trend` | One of: 'accelerating', 'stable', 'weakening' |
| `confidence` | Opportunity confidence score (float) |
| `opportunityId` | ID of linked Opportunity Record (string, or null if Research Queue only) |
| `axes` | Object: `{opportunity, valuation, execution, moat, momentum}` — all floats 1–10 |
| `financials` | Array of 4 objects: `{lbl, val, sub, col?}` — key metrics for the financials table |
| `whyNow` | Array of 2–4 strings — timing catalyst bullets |
| `risks` | Array of 2–3 strings — key risk bullets |
| `scoreBreakdown` | Array of modifier rows + total — must sum to `poised` |
| `eli15` | ELI15 explanation of Poised Score (2–3 sentences) |
| `scenarios` | Array of 3 objects (Bull, Base, Bear): `{name, col, prob, return2yr, returnNum, thesis, assumption, falsifier}` — probs must sum to 100 |
| `watchVariable` | Single most important variable to watch |
| `watchSub` | One-sentence explanation of why this variable matters |
| `confLabel` | Confidence label: 'High', 'Medium–High', 'Medium', 'Low–Medium', 'Low' |
| `confReason` | One-sentence explanation of confidence level |
| `held` | Boolean — true if currently held in Kite portfolio |
| `slot` | 'Core' or 'Extended' |
| `portfolioRec` | Short recommendation label (e.g. 'Add this week', 'Add on dip — watch ₹X') |
| `portfolioBody` | 1–2 sentence portfolio rationale |
| `portfolioEntry` | Entry strategy sentence (price target + why) |
| `bias` | Behavioural bias warning sentence |
| `dynamics` | Object: `{gameType, gameNote, asymmetry, players[], valueRows[], valueSummary, equilibrium, wildcards[], eli15}` |

If any field cannot be extracted from the dashboard file and cannot be reasonably inferred, use a placeholder and add `// TODO: fill in [field]` as a JS comment on the same line.

### Step 3 — Build the stock object

Construct the complete JS object following the same structure as the BEL entry (first entry in STOCKS, lines ~409–459 of `docs/index.html`). Use BEL as the canonical template for field order and value types.

Verify: `scoreBreakdown` modifier values must arithmetically sum to `poised`. If they don't, adjust the modifier values — do not adjust `poised`.

### Step 4 — Insert into docs/index.html

Edit `docs/index.html`: find the closing `];` of the STOCKS array (the line that follows the last stock's closing `},`) and insert the new stock object immediately before it.

The array currently ends after PARAS. The new entry goes after PARAS's closing `},`.

### Step 5 — Confirm and push

Reply with:
```
Added [TICKER] to dashboard — [N] stocks now in STOCKS array.
Fields extracted from: 10_DASHBOARD/<TICKER>/dashboard-YYYY-MM-DD.md
TODOs (if any): [list any placeholder fields]
```

Then commit and push to the current branch with commit message:
`feat: add [TICKER] to dashboard STOCKS array`

---

## Rules

1. **scoreBreakdown must sum to poised.** Check the arithmetic before inserting. Adjust modifier values if needed, never the poised value.
2. **Scenario probabilities must sum to 100.** If they don't in the dashboard file, adjust to nearest round numbers that sum correctly.
3. **No dashboard file = no insertion.** Never invent stock data from memory. If there is no completed dashboard output, redirect to /stock-dashboard first.
4. **Research Queue-only stocks are allowed.** A stock does not need an active Opportunity Record to be added to the dashboard — set `opportunityId: null` for Research Queue stocks.
5. **One stock per invocation.** Do not batch multiple tickers in a single run.

---

## Model Tier

**Claude Sonnet** (or equivalent reasoning model).
This skill reads a dashboard file, maps fields, verifies arithmetic, and makes a surgical code edit — requires careful instruction-following and field mapping.
For a Groq-based pipeline: `llama-3.3-70b-versatile` is the closest match.
