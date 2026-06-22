---
name: refresh-dashboard
description: >
  Refresh all stock cards in docs/index.html with live prices from Kite.
  Updates zone, valuation axis, scoreBreakdown zone modifier, poised total,
  action, held, and priceDate for every stock in the STOCKS array.
  Runs as the final step of the Monday pipeline, or on demand.
  Trigger on: "refresh dashboard", "update dashboard prices", "/refresh-dashboard",
  "update stock prices", "sync dashboard"
model: sonnet
---

# Refresh Dashboard

## Objective

Update every stock card in `docs/index.html` with live market data from Kite.
This is the only step that touches `docs/index.html` in the automated pipeline.
The layout is locked — do not change CSS, HTML structure, or JS logic. Only update
data values inside the STOCKS array and FALLBACK_META.

---

## Inputs

| Input | Source |
|---|---|
| Live price | Kite MCP `get_ltp` — `NSE:<TICKER>` for each stock |
| 52-week OHLC | Kite MCP `get_ohlc` — `NSE:<TICKER>` |
| Live holdings | Kite MCP `get_holdings` |
| Current STOCKS array | `docs/index.html` |

If Kite MCP returns "Please log in first" — stop and tell the user. Do not write
stale prices as if they were live.

---

## Process

### Step 1 — Extract tickers from STOCKS array

Read `docs/index.html`. Find every `id:'<TICKER>'` entry in the STOCKS array.
Build the list of tickers to refresh. Typical list: BEL, HAL, JNKINDIA, LT, PARAS, GABRIEL.

### Step 2 — Fetch live data from Kite

For all tickers in a single pass:
- `get_ltp` → live price for each ticker (format: `NSE:BEL`, `NSE:GABRIEL`, etc.)
- `get_ohlc` → 52-week high/low for each ticker
- `get_holdings` → check which tickers are currently held and at what quantity/average cost

Record the fetch timestamp as today's date in `DD Mon YYYY` format (e.g. `22 Jun 2026`).

### Step 3 — Recalculate zone for each stock

Use the existing `fv.bear`, `fv.base`, `fv.bull` values already in the STOCKS object
(do not change fair values — those are set by `/stock-dashboard` and require a full
investment framework run to change).

Zone classification (use live price vs fv values):

| Condition | zone | zoneLabel |
|---|---|---|
| price ≤ fv.bear | `strong-buy` | `Strong Buy` |
| price ≤ fv.base × 0.90 | `buy` | `Buy Zone` |
| price ≤ fv.base | `buy-zone` | `Buy Zone` |
| price ≤ fv.base × 1.10 | `fair-value` | `Fair Value` |
| price ≤ fv.bull | `watch` | `Watch` |
| price > fv.bull | `expensive` | `Expensive` |

### Step 4 — Recalculate valuation axis score

| zone | axes.valuation |
|---|---|
| `strong-buy` | 10.0 |
| `buy` | 8.5 |
| `buy-zone` | 7.5 |
| `fair-value` | 6.0 |
| `watch` | 4.0 |
| `expensive` | 2.0 |

### Step 5 — Update scoreBreakdown zone modifier

Find the scoreBreakdown row whose `lbl` contains "zone" or "Watch zone" or "Buy Zone"
or "Fair Value" (case-insensitive) — this is the valuation modifier row.

Replace its `lbl` and `val` with:

| zone | lbl | val | type |
|---|---|---|---|
| `strong-buy` | `Strong Buy zone (price ≤ bear FV)` | `+1.0` | `pos` |
| `buy` | `Buy Zone (price >10% below base FV)` | `+0.5` | `pos` |
| `buy-zone` | `Buy Zone (price ≤ base FV)` | `+0.5` | `pos` |
| `fair-value` | `Fair Value zone (price within 10% of base FV)` | `+0.0` | `neu` |
| `watch` | `Watch zone (price above base FV)` | `−0.5` | `neg` |
| `expensive` | `Expensive (price above bull FV)` | `−1.0` | `neg` |

Note: `+0.0` means the row still exists with `val:'0.0'` and `type:'neu'` — do not delete it.

### Step 6 — Recompute poised score

Sum all scoreBreakdown rows except the `type:'total'` row. Parse values carefully:
- `+0.5` → +0.5
- `−0.5` → −0.5 (note: `−` is a minus sign, not a hyphen)
- `7.5` (base row, no sign prefix) → +7.5

Update the `type:'total'` row `val` to the new sum (one decimal place, no sign prefix).
Update the top-level `poised` field to the same value.

Verify: sum of non-total rows must equal the total. If it does not, stop and report
the discrepancy rather than writing a wrong value.

### Step 7 — Update action and actionLabel

| zone | action | actionLabel |
|---|---|---|
| `strong-buy` | `add` | `Add now` |
| `buy` | `add` | `Add this week` |
| `buy-zone` | `add` | `Add this week` |
| `fair-value` | `watch` | `Watch` |
| `watch` | `watch` | `Add on dip` |
| `expensive` | `avoid` | `Avoid` |

### Step 8 — Update held field

Cross-reference the Kite holdings list. For each stock:
- If the ticker appears in holdings with qty > 0: `held: true`
- Otherwise: `held: false`

### Step 9 — Update price, priceDate, 52-week range

For each stock:
- `price`: live LTP (round to 2 decimal places)
- `priceDate`: fetch date in `DD Mon YYYY` format
- If the STOCKS object has `week52High` / `week52Low` fields: update them from `get_ohlc`

### Step 10 — Update FALLBACK_META.lastUpdated

Find `lastUpdated:` in FALLBACK_META (near the bottom of the JS section) and set it to
today's date in `YYYY-MM-DD` format.

### Step 11 — Write and commit

Edit `docs/index.html` with all field updates.

Commit message: `chore: dashboard price refresh YYYY-MM-DD`

Push to current branch.

Print a summary table:

```
| Ticker | Old Price | New Price | Old Zone | New Zone | Old Poised | New Poised | Held |
```

---

## Rules

- **Layout is locked.** Do not touch CSS, HTML structure, JS functions, or slicer logic.
- **Do not change fair values.** `fv.bear`, `fv.base`, `fv.bull` are set by `/stock-dashboard` only.
- **Do not change scenarios, financials, eli15, risks, or whyNow.** Price refresh only.
- **Poised math must be exact.** Never write a total that does not arithmetically equal the sum of its parts.
- **Kite login is mandatory.** If `get_ltp` fails, abort and tell the user — do not refresh with stale data.
- **One commit, all stocks.** Refresh all stocks in a single edit pass and a single commit.

---

## Model Tier

**Claude Sonnet** (or equivalent reasoning model).
This skill reads live market data, applies a calculation framework, and makes targeted
edits to a complex JS file — requires strong instruction-following and careful arithmetic.
For a Groq-based pipeline: `llama-3.3-70b-versatile` is the closest match.
