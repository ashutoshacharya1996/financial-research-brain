---
name: india-stock-picker
description: |
  Blended stock analysis skill for Indian equities (NSE/BSE) combining four frameworks:
  Saurabh Mukherjea's quality screen, Charlie Munger's moat and mental models,
  Peter Lynch's growth classification, and Howard Marks' risk calibration.
  Trigger when the user asks to:
  - Analyse or deep-dive a specific Indian stock
  - Evaluate whether to hold or exit a legacy position
  - Screen a new idea before adding to the portfolio
  - Compare two or more Indian stocks in the same sector
  - Run a pruning decision on existing direct equity holdings
  Always integrates with:
  - macro-geo-lens (regime filter — mandatory for new additions)
  - stock-analyzer (snowflake quantitative layer)
  - wealth-advisor (portfolio fit, position sizing, FIRE implications)
  - Obsidian vault (research stored after every analysis)
  For any current price, valuation, or recommendation output, verify
  external data first. Never output Buy/Watchlist/Exit without dated sources.
---
# India Stock Picker — Blended Framework

## Non-Negotiable Rules

- Current prices, ratios, and filings are time-sensitive. Verify before use.
- Every current fact carries a date and source.
- Separate timeless judgments from current claims.
- Do not output Buy / Watchlist / Exit unless all minimum data checks passed.
- If current data is unavailable: Framework-only; no current recommendation.
- Run Gate 1 FIRST. Do not run full analysis on stocks that fail it.
- Position sizing and portfolio slot rules are mandatory output for any Buy verdict.
- Promoter pledging >20%, auditor resignation, or CFO/EBITDA <0.5 for 3+ years = automatic flag.
- PE > 40 = automatic flag requiring exceptional written justification before proceeding.

## Portfolio System (Always Apply)

### Tiered Structure

| Tier | Slots | Position Size | Entry Condition |
|---|---|---|---|
| Core | 5-7 stocks | 4-5% of equity each | Full framework pass, high conviction, Watchlist price reached |
| Extended | Up to 5 additional | 2-3% of equity each | Must score higher than weakest Core position |
| Hard ceiling | 12 stocks total | — | No exceptions |

### Slot Management Rules

- A Core slot is only free when a position is fully exited.
- Extended position cannot grow to Core size unless it formally displaces a Core position.
- Extended position not reaching conviction within 18 months exits automatically.
- Every new addition requires stating which slot it fills and what the weakest current position is.

### Current Equity Limits

- Total direct stock allocation: max 20% of equity portfolio
- Per-stock Core max: 4-5% of equity
- New entry size: 2-3%, scale to Core on conviction

## Minimum Current Data Checks

Before any recommendation verify:
1. Latest market price and date
2. Latest reported quarter — revenue, PAT, EBITDA, FCF
3. Latest ROCE (trailing 12 months or latest annual)
4. Promoter pledging % (latest quarter)
5. Auditor name and any recent changes
6. Material news, SEBI actions, or management changes in last 6 months

If any item missing: Framework-only mode.

## Data Source Ladder (India)

1. Screener.in — 10-year financials, ROCE, CFO, ratios. Primary source.
2. NSE/BSE filings — quarterly results, shareholding pattern, pledging data
3. SEBI EDGAR — regulatory filings, show-cause notices
4. Company IR page — annual reports, concall transcripts
5. Trendlyne / Tickertape — secondary cross-check
6. Moneycontrol — news only, never for numbers

## The Five-Gate Workflow

Run in exact order. Gate failure stops analysis.

### GATE 0 — Lynch: Category Classification

| Category | Definition | Key Lens |
|---|---|---|
| Consistent Compounder | 15%+ growth, low debt, decade track record | ROCE consistency, moat depth |
| Fast Grower | 20%+ growth, reinvestment story | Growth runway, balance sheet |
| Stalwart | Large, slow, stable, defensive | Valuation vs history |
| Cyclical | Metals, chemicals, energy, cement | Cycle position, through-cycle EBITDA |
| Turnaround | Distressed, thesis = recovery | Cash burn, debt covenants, evidence |
| Asset Play | Hidden value not in market cap | Asset quality, unlock trigger |

Turnarounds and asset plays: Extended tier only, 2-3% max.

### GATE 1 — Financial Quality Screen

#### 1A. Mukherjea Quality Gate

| Criterion | Threshold | Source |
|---|---|---|
| 10-year ROCE | Consistently >15% (8 of 10 years) | Screener.in |
| 10-year revenue CAGR | >10% | Screener.in |
| Debt/Equity | <0.5 non-financials | Screener.in |
| CFO/EBITDA | >0.7 for 3+ consecutive years | Screener.in |
| Promoter pledging | <20% | BSE shareholding |
| Unpledged promoter holding | >=40% | BSE shareholding |
| Auditor stability | No resignation in last 5 years | Annual report |
| SEBI actions | None material in last 3 years | SEBI EDGAR |

Exception for cyclicals: use 7-year ROCE average.
Exception for turnarounds: flag, Extended tier only.

#### 1B. Valuation and Financial Ratios

| Metric | Strong Preference | Acceptable | Flag |
|---|---|---|---|
| PE Ratio | <=20 | 20-30 | 30-40 needs justification; >40 auto-flag |
| PE vs own 5-yr history | Below median | At median | Above median |
| PE vs sector peers | Below median | At median | Premium without justification |
| PEG Ratio | <0.5 | 0.5-1.0 | >1.0 |
| Debt/Equity | <0.5 | 0.5-1.0 | >1.0 |
| Interest Coverage Ratio | >=5x | 3-5x | <3x |
| Current Ratio | >=1.5 | 1.0-1.5 | <1.0 |
| ROCE 3-yr average | >=15% | 12-15% | <12% |
| ROE 3-yr average | >=15% | 12-15% | <12% |
| Sales Growth 3-yr | >=15% | 10-15% | <10% |
| EPS Growth 3-yr | >=20% | 15-20% | <15% |

PE treatment: <=30 strong preference. PE 30-40 requires explicit written justification. PE >40 automatic flag.

#### 1C. Working Capital Quality

| Check | Green | Yellow | Red |
|---|---|---|---|
| Debtor days YoY | Reducing | Stable | Increasing |
| Inventory days YoY | Reducing | Stable | Increasing |
| Payable days YoY | Stable or increasing | Slight reduction | Sharp reduction |
| Cash Conversion Cycle | Reducing | Stable | Increasing without explanation |
| CFO positive | Yes consistently | Occasional dip | Negative |

Gate 1 result: Pass / Fail / Conditional pass (state reason)

If Fail: output "Failed financial screen. Full analysis not warranted." Stop.

### GATE 2 — Qualitative Business Analysis

Work through all 15 points:

1. Business model — how does it make money?
2. Revenue split by segment, margins per segment, TAM/SAM/SOM
3. Criticality of products in industry value chain
4. Competitive landscape per segment
5. Industry growth rate vs company growth rate vs competitor growth rate
6. Market share per segment — gaining, stable, or losing?
7. Competitors margins per segment — who has pricing power?
8. Porter's 5-forces analysis
9. Tailwinds for company and industry
10. Headwinds for company and industry
11. Durable Competitive Advantage / Sustainable moat
12. Management characteristics — promoter pedigree, legal history, red flags
13. Expected growth drivers — orderbook, capacity, price vs volume, new markets, new products, cost optimisation, acquisitions
14. Valuation vs competitors, industry, history — DCF intrinsic value vs current price (conservative and base only)
15. Thesis falsifiability — what specific event would prove this thesis wrong?

Gate 2 result: Strong pass / Pass / Weak pass / Fail

### GATE 3 — Munger: Moat and Management

#### 3A. Circle of Competence

Can you explain in two sentences why this business earns sustainably above its cost of capital?

If No: outside the circle. Framework-only. Do not proceed.

#### 3B. Moat Assessment

| Moat Type | Indian Examples | Durability Test |
|---|---|---|
| Cost advantage | Titan, Coal India | Can competitors match unit economics? |
| Switching cost | HDFC Bank, TCS | Would customers absorb 20% price hike? |
| Network effect | BSE, NSE, CAMS | Does value compound with each new user? |
| Intangible/Brand | Asian Paints, Page Industries | Is brand a pricing tool not just recognition? |
| Efficient scale | Container Corp, IEX | Market too small for second player? |
| Regulatory | HDFC Life, SBI Cards | Licence or genuine advantage? Score lower. |

#### 3C. Management Quality

| Check | Green | Yellow | Red |
|---|---|---|---|
| Capital allocation | Buybacks/dividends when no IRR | Fair-price acquisitions | Premium acquisitions no ROIC clarity |
| Promoter behaviour | Buying stock no pledging | Stable pledge | Increasing pledge or insider selling |
| Disclosure quality | Proactive honest about misses | Reactive | Blames externals consistently |
| Related-party transactions | Minimal disclosed | Present but explained | Large unexplained |
| Compensation | Reasonable vs peers | High but ROIC-linked | Excessive not performance-linked |
| Legal/regulatory history | Clean | Minor resolved | Ongoing material |
| Auditor stability | Stable reputable firm | Changed once with reason | Frequent changes or resignations |
| Key personnel | Stable clear succession | Some turnover | Frequent senior exits |

One Red: downgrade management two levels.
Two Reds: exit consideration regardless of business quality.

#### 3D. Inversion

What would have to be true for this investment to fail completely?
- What kills the moat?
- What kills the growth story?
- What makes the thesis wrong? Is it falsifiable?

If failure path is unclear: do not understand the business well enough. Stop.

### GATE 4 — Lynch: Growth and Valuation

#### 4A. PEG Ratio

PEG = P/E divided by Expected EPS growth rate %

- PEG < 0.5 = Very attractive
- PEG 0.5-1.0 = Reasonable for high-quality business
- PEG 1.0-1.5 = Fair, needs moat to justify
- PEG > 1.5 = Expensive unless growth visibility exceptional

Use 3-year average historical growth or conservative forward estimate. Never single peak year.

#### 4B. Valuation Method by Category

| Category | Method | Buy Zone |
|---|---|---|
| Consistent Compounder | P/E vs own 10-year median | At or below median |
| Fast Grower | PEG + DCF 12-13% discount rate | PEG <1.0, DCF >25% margin of safety |
| Stalwart | Dividend yield + P/E vs peers | Yield at 5-year high |
| Cyclical | EV/EBITDA through-cycle average | Near trough not peak EBITDA |
| Turnaround | Price/tangible book | Only when cash burn visibly stopping |
| Asset Play | Discount to asset value | >40% discount, clear unlock trigger |

#### 4C. Required Margin of Safety

| Category | Minimum MoS |
|---|---|
| Consistent Compounder | 15% |
| Fast Grower | 25% |
| Cyclical | 30% vs cycle-average |
| Turnaround / Asset Play | 40% |

### GATE 5 — Marks: Risk Calibration

#### 5A. Cycle Position

Where is this sector? Early / Mid / Late / Peak

Are current valuations pricing peak or trough?

#### 5B. Second-Level Thinking

- What does consensus believe?
- What do you believe that is different and why?
- If right: upside? If wrong: downside?
- Is risk/reward asymmetric in your favour?

#### 5C. Downside First

- Bear case: what goes wrong, estimated loss %
- Can you hold through 40% drawdown for 18 months?
- Is position size calibrated to downside not upside?

## Patience Check (Mandatory Before Any Buy Verdict)

Answer all three before outputting Buy:

1. **Price discipline:** Is current price within required margin of safety or being rationalised?
2. **FOMO test:** If stock is 20% higher in 6 months with no fundamental change would you regret not buying? If yes — FOMO driving decision not valuation. Route to Watchlist.
3. **18-month hold:** Would you be comfortable if stock went nowhere for 18 months with thesis intact?

If any answer triggers doubt: output Watchlist with specific entry price. Do not force a Buy.

## Output Format

Use this structure exactly:

```
---
India Stock Analysis — COMPANY NAME (TICKER)
Analysis date: YYYY-MM-DD
Mode: Framework-only | Current-data-backed
Category (Lynch): [type]
Portfolio tier if buying: Core | Extended | Watchlist | Pass

CONCLUSION FIRST
- Verdict: Buy Core | Buy Extended | Watchlist | Watch | Exit | Framework-only
- Confidence: Low | Medium | High
- If Buy — slot: Fills slot X of Core/Extended. Current weakest position: [name]
- If Watchlist — entry price: ₹X (Y% below current as of [date])
- If Exit — tax note: LTCG/STCG sequencing recommendation
- Top 3 reasons:
  1.
  2.
  3.

GATE 1 — Financial Quality Screen
1A Mukherjea Gate: [complete table with dated values]
1B Valuation Ratios: [complete table]
1C Working Capital Quality: [Debtor/Inventory/Payable days trend]
Gate 1 result: Pass | Fail | Conditional (reason)

GATE 2 — Qualitative Business Analysis
[All 15 points]
Gate 2 result: Strong pass | Pass | Weak pass | Fail

GATE 3 — Munger Moat and Management
Circle of competence: Inside | Edge | Outside
Moat type and depth: [type] — Strong/Moderate/Weak/None
Moat durability: 10+ years | 5-10 years | <5 years | Uncertain
Threat vectors: [specific, not generic]
Management quality: [per criterion Green/Yellow/Red with reasoning]
Inversion: [specific failure paths, no generic risks]

GATE 4 — Lynch Valuation
Category: [with justification]
Current PE / PEG / EV-EBITDA: [value, date, source]
PE vs own 5-yr median: above/at/below
PE vs sector median: above/at/below
Base fair value: ₹X (method + key assumptions)
Bear / Base / Bull: ₹X / ₹Y / ₹Z
Current MoS: X% (required Y%)
Valuation verdict: Cheap | Fair | Expensive

GATE 5 — Marks Risk Calibration
Cycle position: Early | Mid | Late | Peak
Consensus vs your view: [what market believes vs differentiated thesis]
Bear case: [specific, what goes wrong]
Estimated downside if wrong: X%
Risk/reward: [asymmetry assessment]

PATIENCE CHECK
1. Price discipline: confirmed | rationalised?
2. FOMO test: valuation-driven | fear of missing out?
3. 18-month hold: yes/no with reasoning
Patience verdict: Buy now | Watchlist at ₹X

PORTFOLIO FIT
Current portfolio: X stocks, X Core, X Extended, X slots remaining
Existing exposure (direct + via MFs): %
Sector weight post-addition: % (within | exceeds limit?)
FIRE horizon fit: thesis horizon vs 10-year FIRE runway
Slot being filled: Core X | Extended X
Weakest current position this would displace: [name]

KEY WATCHPOINTS
Area | Current View | Why It Matters | What to Watch Next
Business quality | | |
Moat | | |
Management | | |
Financials | | |
Valuation | | |
Biggest risk | | |

SOURCES
[Every current claim — source name, date, URL or filing reference]
---
```

## Legacy Pruning Mode

When analysing an existing holding from the 44-stock portfolio:

```
LEGACY HOLD ASSESSMENT
- Original thesis: what was the buy thesis?
- Thesis status: Intact | Weakening | Broken | Never had one
- Sunk cost check: If I had cash today would I buy this at current price? If No: exit signal.
- Tax sequencing:
    LTCG (>1 year): 12.5% — harvest within ₹1.25L annual exemption
    STCG (<1 year): 20% — avoid in high-income months where possible
    Losses: harvest to offset gains, 3-year carry-forward limit
- Replacement test: Is there better use of this capital in current Watchlist?
```

Priority order for pruning: Broken thesis > Never had a thesis > Weakening thesis > Tax-loss harvest candidates.

## Integration Handoffs

- **Macro overlay:** Call macro-geo-lens compact 4 signals for new additions. Not required for pruning.
- **Quantitative layer:** financial-advisor skill handles snowflake and DCF. This skill handles qualitative judgment.
- **Portfolio close:** Confirm position sizing, slot management, and FIRE fit.
- **Vault write:** After every analysis write `02-Research/stocks/TICKER.md` with verdict, date, entry price, watchpoints, next review trigger.

## Output Length

- **Quick triage / legacy hold first pass:** Gate 1 + Conclusion. One screen.
- **Standard new idea:** All gates. Two to three screens.
- **Full conviction deep dive before Core position:** All gates + full 15-point checklist. Read annual report first.

## What This Skill Does NOT Do

- Predict stock price movements or give entry/exit timing
- Replace reading the annual report for genuine conviction positions
- Skip pushback because user is excited
- Validate thesis without running all gates
- Output Buy without identifying specific portfolio slot
- Allow portfolio to exceed 12 stocks under any framing
- Use aggressive valuation assumptions in DCF or fair value estimates
