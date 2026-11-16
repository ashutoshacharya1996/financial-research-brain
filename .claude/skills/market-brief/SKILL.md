---
name: market-brief
description: >
  Weekly Market Brief — the single output of the weekly pipeline (replaces the per-stock
  extraction → delta → theme → screener → impact chain). Reads the Sunday market fetch
  (02_RAW_DOCUMENTS/_market/<date>/) and writes a super-simple, phone-readable brief on
  the broad Indian market, sectors, and Ashutosh's mutual funds: what happened last week,
  what to take note of, opportunities in play, and a Bull/Base/Bear probability forecast.
  Writes 08_PORTFOLIO_INPUTS/market-brief-YYYY-MM-DD.md. Trigger on: "market brief",
  "weekly brief", "run the pipeline", "weekly run", "how did the market do", "how are my funds".
model: sonnet
---

# Market Brief

## Objective

One page. Read in 3 minutes on a phone. Answer four questions, in this order:

1. **What happened last week?**
2. **Anything I need to take note of?**
3. **Any opportunities in play?**
4. **Bull / Base / Bear — what are the odds?**

The reader is a long-term SIP investor (MF-first, mid/small-cap tilt, 10-year horizon, FIRE plan).
The brief informs. It never tells him to buy, sell, switch, or stop a SIP.

---

## Inputs (read in this order)

| Input | Location |
|---|---|
| This week's numbers | `02_RAW_DOCUMENTS/_market/<latest>/market-summary.md` (tables) and `market-snapshot.json` (all fields) |
| This week's headlines | `02_RAW_DOCUMENTS/_market/<latest>/news.md` |
| Fund list | `01_UNIVERSE/mf_watchlist.csv` (status, SIP amount, notes, watch flags) |
| Last week's brief | `08_PORTFOLIO_INPUTS/market-brief-<previous>.md` — for "what changed" and the prior odds |
| Live holdings (optional) | Kite MCP `get_mf_holdings` — if authorised, reconcile the fund list (see Step 0) |

If the latest `_market/` folder is older than 8 days or missing, stop: write a two-line brief saying the Sunday fetch didn't run, include the `source_status` if any, and notify.

If a source failed (see `source_status` in the summary), carry on with what exists and say in one line at the bottom what was missing. Never fill a gap with remembered numbers.

---

## Process

### Step 0 — Fund list check
If Kite is available, pull MF holdings. Any fund held but missing from `mf_watchlist.csv` → add a row (match_keywords from the scheme name) and say so in the brief's footer. Any watchlist fund not held → flag in the footer; do not delete the row. If Kite is unavailable, use the CSV as-is and note "holdings not re-verified" in the footer.

### Step 1 — What happened (facts only)
From the summary tables: Nifty 50, Midcap 150, Smallcap 250 weekly moves; best 3 and worst 3 sectors by 1W; India VIX level/direction; FII/DII net; Brent, USD/INR, US 10Y if they moved meaningfully (Brent ±5%, INR ±1%, US10Y ±15 bps). Pair each move with the headline from `news.md` that explains it — only if a headline actually does; otherwise say "no clear single driver".

### Step 2 — Your funds
For each fund with data: 1W, 1M, 1Y, and 1Y vs its benchmark (`benchmark_key` → index 1Y). Flag only:
- 1Y lagging benchmark by > 5 pts → "lagging"
- > 15% below its 1Y NAV peak → "in drawdown"
- AMC/fund name in this week's news (`Your fund houses` section) → one-line what it was
- any `notes` watch flag that fired (e.g. Quant AMC SEBI news)
Everything else is "on track" — don't comment on it.

### Step 3 — Take note (max 3 bullets)
Only things that matter to a 10-year SIP investor or his locked rules:
- **War-chest trigger:** Nifty vs 22,000 (from `war_chest`). Mention every week in one line; highlight if within 5%.
- **Valuation regime:** Nifty 50 PE and Smallcap/Midcap PE vs the bands in the scoring table below.
- Regulatory / AMC events touching his funds, RBI decisions, tax/SEBI rule changes affecting MFs.
- A fund flag from Step 2.
If nothing qualifies, write "Nothing needs your attention this week." — that is a valid and good outcome.

### Step 4 — Opportunities in play (max 3)
Category- or sector-level only (e.g. "Pharma at 52-week low with PE below 5-yr average", "Smallcaps 20% off highs"). Each one: what, the number that makes it interesting, and what would confirm it. Frame as "worth watching" / "where a lump sum from the war chest would historically have done well" — never "buy". Prefer zero opportunities to a weak one.

### Step 5 — Bull / Base / Bear (next 3 months, Nifty 50)
Score the six signals below, sum them, map to probabilities, then adjust by at most ±10 pts per scenario for one named news factor. Probabilities are whole numbers summing to 100. Show the score table — the reader should see why the odds are what they are.

| Signal | +1 (bullish) | 0 | −1 (bearish) |
|---|---|---|---|
| Trend | Nifty > 200DMA by > 3% | within ±3% | < 200DMA by > 3% |
| Momentum | Nifty 1M > +2% | −2% to +2% | < −2% |
| Valuation | Nifty PE < 19 | 19–23 | > 23 |
| Fear | VIX < 13 | 13–18 | > 18 (or +25% WoW) |
| Breadth | Midcap 150 & Smallcap 250 both beat Nifty over 1M | mixed | both lag Nifty by > 2 pts |
| Flows/Macro | FII net buyers AND Brent < $80 | mixed | FII net sellers AND (Brent > $90 or INR −1% WoW) |

| Total score | Bull | Base | Bear |
|---|---|---|---|
| +4 to +6 | 45 | 45 | 10 |
| +2 to +3 | 35 | 50 | 15 |
| −1 to +1 | 25 | 50 | 25 |
| −3 to −2 | 15 | 50 | 35 |
| −6 to −4 | 10 | 45 | 45 |

Scenario definitions (Nifty 50, 3 months): **Bull** > +7% · **Base** −5% to +7% · **Bear** < −5%.
If a signal's input is missing, score it 0 and say so. State the change vs last week's odds and the one signal that moved them.

### Step 6 — Write the file
`08_PORTFOLIO_INPUTS/market-brief-YYYY-MM-DD.md` (date = Monday of the run, or today if run ad-hoc).

---

## Output Format (exact)

```markdown
# Market Brief — week ending DD Mon YYYY

**In one line:** [the week in ≤ 20 words]

## 1. What happened
| | Week | Level |
|---|---|---|
| Nifty 50 | +x.x% | 24,xxx |
| Midcap 150 | | |
| Smallcap 250 | | |
| India VIX | | |
Best sectors: A +x%, B +x%, C +x% · Worst: D −x%, E −x%, F −x%
- [driver 1 — fact + source headline]
- [driver 2]
- [driver 3 — optional]

## 2. Your funds
| Fund | Week | 1Y | vs benchmark (1Y) | Flag |
|---|---|---|---|---|
(one row per fund; Flag column blank unless Step 2 fired)

## 3. Take note
- [max 3 — or "Nothing needs your attention this week."]

## 4. Opportunities in play
- [max 3 — what · the number · what would confirm it — or "None worth flagging."]

## 5. Next 3 months — Nifty odds
🟢 Bull XX% · 🟡 Base XX% · 🔴 Bear XX%   (last week: XX / XX / XX)
| Signal | Reading | Score |
|---|---|---|
(six rows) | **Total** | | **±N** |
Why it moved: [one sentence]

**SIPs:** continue as planned. [This line is fixed every week.]

---
Data: [sources ok / missing]. Holdings: [verified via Kite / not re-verified]. Not investment advice — research signals only.
```

---

## Rules

1. **≤ 450 words** in the brief body. Tables don't count toward the limit; prose does.
2. **Numbers come from the snapshot only.** No remembered prices, no estimates. A missing number is "—".
3. **No Buy / Sell / Switch / Stop / Exit language.** SIPs always continue — the plan is built for drawdowns.
4. **Name the bias if the week invites one** (e.g. recency bias after a sharp fall) in one line under Take note.
5. **Plain English.** No jargon without a 5-word explanation in brackets the first time it appears (e.g. "200DMA (200-day average price)").
6. **Notify** after writing: lead with the odds and the single most important "take note" item; include the file path.

## Model Tier

Claude Sonnet (or equivalent). Mostly deterministic reading of tables; the judgement is in Steps 1, 3 and 4.
