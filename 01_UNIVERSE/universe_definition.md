# Universe Definition

## Purpose

The Opportunity Discovery Engine tracks a dynamic universe of Indian equities. The universe is not static — companies enter when evidence warrants, move between states as signals strengthen or weaken, and exit active tracking when their thesis breaks or goes stale.

**The canonical universe file is:** `01_UNIVERSE/company_master.csv`

No other file controls universe membership. `fetch_evidence.py` reads only from this file. Universe Manager is the only agent authorised to write to it.

---

## Two Flags

Every company in the universe has two independent boolean flags:

| Flag | Meaning |
|---|---|
| `active_universe=true` | The company belongs in the research universe and is eligible for tracking |
| `fetch_enabled=true` | The Sunday `fetch_evidence.py` script should fetch company-specific evidence for it |

A company can be `active_universe=true` and `fetch_enabled=false` — it is in the universe but not yet worth the weekly fetch cost. This is the default for newly discovered companies.

`fetch_enabled=true` requires explicit promotion by Universe Manager.

---

## Status Values

| Status | Meaning | Typical fetch_enabled |
|---|---|---|
| `active` | Strong current signal; thesis is developing or conviction-stage | true |
| `monitoring` | Relevant but less urgent; thesis intact but quieter | false (or monthly) |
| `paused` | No fresh signal in 8–12 weeks; fetch stopped | false |
| `archived` | Thesis broken or stale; no fetch unless manually reactivated | false |

---

## Priority Values

`high` / `medium` / `low`

Priority governs scheduling within the Monday pipeline — higher priority companies get extraction and delta analysis first when pipeline time is constrained.

---

## CSV Schema

```
ticker, company_name, sector, industry,
active_universe, fetch_enabled, fetch_reason,
priority, status, last_reviewed, source, notes,
deprioritization_reason, next_review_date,
yfinance_symbol, nse_symbol, bse_code
```

`yfinance_symbol`, `nse_symbol`, `bse_code` are required only for `fetch_enabled=true` companies. Leave blank for monitoring/paused/archived companies.

---

## Universe Priority Order

When a conflict exists between sources:

1. User watchlist (highest — always included, no threshold required)
2. Active thesis companies (companies with an active Opportunity Record)
3. News-discovered companies (≥ 2 distinct fundamental sources this week)
4. Nifty 1000 constituents (floor — all are eligible but not all are `fetch_enabled`)

---

## Promotion Rules

Promote a company from `fetch_enabled=false` to `fetch_enabled=true` when **two or more** of the following are true:

- Primary-source evidence strengthens (filing, earnings call, regulatory announcement)
- Theme corroboration increases (company appears in 2+ theme runs)
- Order book or order inflow improves with concrete ₹ data
- Guidance improves with named targets
- A named catalyst becomes concrete (signed contract, commissioning date confirmed)
- Company appears repeatedly across discovery runs (≥ 2 consecutive weeks)

Record the reason in `fetch_reason` and set `last_reviewed` to today.

---

## Deprioritization Rules

Companies and themes move both ways. Downgrade when:

- No meaningful thesis-relevant update for 8–12 weeks → status: `paused`
- No material update for 2 quarters → status: `archived`
- Theme corroboration weakens below 2 companies
- Order delay or cancellation confirmed
- Guidance cut (not just missed — actual downward revision)
- Margin compression over 2+ quarters with no recovery thesis
- Cash conversion deterioration (DSO rising, FCF negative and worsening)
- Valuation fully prices in upside (opportunity closed)
- Thesis breaker triggered (as defined in the linked Opportunity Record)

**Do not immediately stop fetching on serious negative news.** Governance issues, rating downgrades, order cancellations, or promoter pledge spikes should create risk-alert tracking first — set status to `monitoring` and document in `notes`. Only move to `paused` or `archived` after a review cycle confirms the thesis is broken.

Every downgrade must populate:
- `deprioritization_reason` — what changed and why it matters
- `next_review_date` — when to re-evaluate

---

## Source Values

| Source | Meaning |
|---|---|
| `nifty_1000` | Nifty 1000 constituent (index membership) |
| `nifty_500` | Nifty 500 constituent |
| `news_discovery` | Surfaced via Lane B discovery sweep |
| `watchlist` | Manually added by user |
| `opportunity_record` | Added because it appears in an active Opportunity Record |

---

## Discovery Source Policy

When evaluating discovery signals, Universe Manager applies a tiered source quality filter:

**Tier 1 — Official / Primary (highest weight):**
NSE corporate announcements, BSE corporate announcements, company IR pages, PIB India, Ministry of Defence, Ministry of Power, Ministry of Railways, MNRE, Ministry of Heavy Industries, DPIIT / PLI updates, SEBI orders

**Tier 2 — Credible business news:**
Business Standard, Economic Times, Moneycontrol, CNBC-TV18, Livemint, Financial Express, Hindu BusinessLine

**Tier 3 — Credit / risk:**
CRISIL, ICRA, India Ratings, CARE Ratings

**Tier 4 — Theme-specific:**
Defence: MoD, DRDO, BEL/HAL/BDL/shipyard filings, DAC updates
Railways: Indian Railways, RVNL/IRCON/RITES/Titagarh/BEML filings
Power: Power Ministry, CEA, PGCIL, REC, PFC filings
Green hydrogen/renewables: MNRE, SECI, NTPC Green, ACME/Adani/Reliance filings
Data centers: STT/NTT/AdaniConneX filings and infra reports
Semiconductors/electronics: MeitY, Invest India, DPIIT, company filings

**Avoid:** Telegram, WhatsApp-style news, unsourced social media, anonymous blogs, random tips. A Tier 2 article repeating a Tier 4 rumour does not count as independent corroboration.

---

## Guardrails

1. `fetch_evidence.py` must not decide universe membership.
2. Universe Manager is the only agent that writes to `01_UNIVERSE/company_master.csv`.
3. Sunday company fetch (`fetch_evidence.py`) only reads `fetch_enabled=true` rows.
4. Discovery fetch (Lane B) writes to `02_RAW_DOCUMENTS/_discovery/` only — never to the universe CSV.
5. Discovery News Agent may suggest candidates but may not modify the universe CSV.
6. Do not maintain `data/company_master.csv` separately. If it exists and differs from `01_UNIVERSE/company_master.csv`, the Sunday script will exit with a fatal error.
7. Positive opportunity signal is not a buy signal. Route to Investment Impact before any underwriting.
8. If a stock has positive delta but weak cash conversion, rich valuation, governance uncertainty, or missing portfolio fit — route to Investment Impact / Watchlist, not Buy.
