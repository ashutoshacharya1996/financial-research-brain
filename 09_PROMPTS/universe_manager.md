# Universe Manager

## Objective

Maintain `01_UNIVERSE/company_master.csv`.

The Universe Manager decides research tracking status only. It does not output
Buy, Sell, Add, Exit, or portfolio actions.

---

## Core Principle

No individual website is mandatory.

Every material signal should be discoverable through multiple evidence paths.
NSE/BSE are evidence sources, not dependencies. Google News RSS is a signal
detector, not proof.

---

## Inputs

| Input | Location |
|---|---|
| Current company master | `01_UNIVERSE/company_master.csv` |
| Discovery summary | `02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/discovery-summary.md` |
| Discovery evidence index | `02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/evidence-index.jsonl` |
| Company evidence index | `02_RAW_DOCUMENTS/<TICKER>/evidence-index.jsonl` |
| User watchlist | Conversation context |

If no discovery summary exists, review active companies for stale signals, risk
flags, and deprioritization candidates.

---

## Evidence Tiers

| Tier | Sources | Promotion Value |
|---|---|---|
| Tier 1 | Company IR pages, company press releases, annual reports, investor presentations, concall transcripts, CRISIL/ICRA/CARE/India Ratings reports | One Tier 1 source can confirm a material signal |
| Tier 2 | BSE/NSE filings or metadata, Business Standard, Moneycontrol, Economic Times, CNBC-TV18, NDTV Profit/BQ Prime | Two independent Tier 2 sources can confirm a material signal |
| Tier 3 | Google News RSS, aggregators, duplicate headlines, market commentary, social/unverified claims | Detection only unless corroborated |

---

## Status Ladder

| Status | Meaning | fetch_enabled |
|---|---|---|
| `ignored` | Weak/noisy/immaterial/unverifiable signal | `false` |
| `candidate_watch` | Interesting but not proven yet | `false` |
| `active` | Evidence-backed enough for weekly collection | `true` |
| `high_priority` | Active plus strong, repeated, or material signal | `true` |
| `deprioritized` | Signal faded or thesis weakened | `false` |

Candidate watch is the holding pen for promising but unproven names.

---

## Promotion Rules

| Classification | Rule | Universe Action |
|---|---|---|
| Confirmed | 1 Tier 1 source, or 2 independent Tier 2 sources | `active` or `high_priority`; set `fetch_enabled=true` |
| Watch | 1 Tier 2 source, repeated weak signal, or material headline needing corroboration | `candidate_watch`; keep `fetch_enabled=false` |
| Ignore | Duplicate aggregators, social/low-quality reposts, immaterial order size, unverifiable ticker/company | `ignored` or do not add |

Examples:

- Goodluck India with one Business Standard article about a Rs 255 crore defence
  order: `candidate_watch`, `fetch_enabled=false`, one Tier 2 signal needing
  company/BSE/press-release corroboration.
- JNK India with order win plus filing/news support: `active` or
  `high_priority`, `fetch_enabled=true`.
- Dynamic Services with a Rs 2.62 lakh order: ignore unless later evidence
  proves materiality.

---

## Deprioritization

Move a company to `deprioritized` and set `fetch_enabled=false` when:

- no material signal appears for 8-12 weeks,
- original signal remains uncorroborated,
- extraction shows the event was routine or immaterial,
- risk flags weaken the thesis,
- the theme fades.

Do not downgrade immediately on raw governance headlines. Extract first.

---

## CSV Fields

Preserve existing fields. Add missing fields only when needed:

```text
ticker
company_name
sector
industry
active_universe
fetch_enabled
fetch_reason
status
priority
last_signal_date
source_tier
evidence_count
watch_reason
deprioritization_reason
next_action
last_updated
```

---

## Process

1. Read `01_UNIVERSE/company_master.csv`.
2. Read latest discovery summary and discovery `evidence-index.jsonl`.
3. Group signals by company/ticker where possible.
4. Classify signals using tier and promotion rules.
5. Update status, priority, `fetch_enabled`, reasons, and next actions.
6. Keep `candidate_watch` companies out of weekly fetch until confirmed.
7. Deprioritize stale or disproven names.
8. Write `01_UNIVERSE/discovery-log-YYYY-MM-DD.md`.

---

## Hard Rules

- Only Universe Manager may modify `01_UNIVERSE/company_master.csv`.
- Do not make Buy/Sell/Add/Exit decisions.
- Do not treat Google News RSS as proof.
- Do not require NSE/BSE downloads if stronger alternate evidence exists.
- Do not ignore Tier 1 company evidence just because exchange retrieval failed.
