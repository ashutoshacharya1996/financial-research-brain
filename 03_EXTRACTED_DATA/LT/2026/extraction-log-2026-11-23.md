# Extraction Log — LARSEN & TOUBRO LTD (LT)
Run date: 2026-11-23
Extracted by: Extraction Agent
Scope: 02_RAW_DOCUMENTS/LT/evidence-index.jsonl records with discovered_at after 2026-06-22 (weekly fetches 2026-06-28 … 2026-11-22) and collection_status in (downloaded, text_snapshot) — 73 records (72 PDFs + 1 text snapshot). Records discovered on 2026-06-22 itself were treated as part of the prior run and not re-processed.
Context-only inputs: 02_RAW_DOCUMENTS/LT/news-2026-06-28.md … news-2026-11-22.md (headline metadata, tier_3; not extracted).

---

## Documents extracted (44 records → 13 files)

| Output file | Records covered (hash prefix) |
|---|---|
| 2026/Q1FY27/quarterly-results.md | ecb42d3cd4 (Outcome of board meeting 28-Jul-2026, results + press release + LTPDL merger); a72fba6296 (6-Aug-2026 machine-readable resubmission of Q1 results) |
| 2026/Q1FY27/investor-presentation.md | 8f321266ad |
| 2026/Q2FY27/quarterly-results.md | da335b2be3 |
| 2026/Q2FY27/investor-presentation.md | 8a0416e463 |
| 2026/Q2FY27/order-wins.md | 6be982e4e4, 3e765a2e4d, 66821d0d30, ae31195ab7, 9ff57996d9, 704682b6f1, 4ec6ec0a1c, 9fa0dd2603, 7bbb23ba22, 81d6c24042, 177554f340, ecfd34bfdd, f4e62e9012, 4179fcfaf6, 76ba0f15b5 |
| 2026/Q3FY27/order-wins.md | e16363dce6, f3f71f9f5d, a4ecfab786, f4ed51842b, 8866d34200, eb3ceddd37, 278006de5e |
| 2026/events/credit-ratings-2026-09-04.md | 517847e44f (Moody's Baa1), 3041aa2fb0 (India Ratings), 8dfe76091c (CRISIL) |
| 2026/events/concession-divestments-2026-09-30.md | bf96ff4918 (Nabha completed), ba4af32785, 7b8f981661 (HMRL timeline extensions) |
| 2026/events/vyoma-data-centre-transfer-2026-08-11.md | d62f04a12e (BTA), a860c41c89 (BTA extension), 2e4a9fda93 (LTA Data Centres incorporation), 389527431b (Fortanix partnership) |
| 2026/events/realty-scheme-of-arrangement-2026-09-01.md | 8afb707bf2, e1fd03cd3e (EGM notice), 5fbccbe639 (meeting outcome), b48b67a0ca (NCLT admission) |
| 2026/events/senior-management-changes-2026-10-07.md | 5930deea42 (Hebbar resignation), 7628c045a6 (SMP promotions) |
| 2026/events/semiconductor-semicon-launch-2026-09-18.md | feb1a4460d |

## Documents skipped (29 records)

| Title (NSE category / subject) | Date | Local path | Reason skipped |
|---|---|---|---|
| Price to sales forward – TradingView (snapshot) | 2026-06-27 | 02_RAW_DOCUMENTS/LT/snapshots/2026-06-28/Price-to-sales-forward-of-Larsen-Toubro-Limited-NSE-LT---TradingView-9a3ac6c39a.txt | No extractable text (11 bytes: "Google News"); tier_3 |
| Trading Window closure (Q1 results) | 2026-06-25 | 02_RAW_DOCUMENTS/LT/raw/2026-06-28/Trading-Window-352b0b1e68.pdf | Routine compliance — trading window |
| ESG rating – CRISIL ESG 62→67 | 2026-06-24 | 02_RAW_DOCUMENTS/LT/raw/2026-06-28/General-Updates-cffb9ee958.pdf | ESG score update (non-credit); not material to financials |
| Newspaper publication – NCLT-convened meeting notice | 2026-06-29 | 02_RAW_DOCUMENTS/LT/raw/2026-07-05/Copy-of-Newspaper-Publication-7b804711ff.pdf | Routine — newspaper publication |
| Reg 74(5) depository certificate (Jun 2026) | 2026-07-06 | 02_RAW_DOCUMENTS/LT/raw/2026-07-12/Certificate-under-SEBI-Depositories-and-Participants-Regulations-2018-d16ea78288.pdf | Routine — depository certificate |
| Schedule of Q1 FY27 earnings call | 2026-07-17 | 02_RAW_DOCUMENTS/LT/raw/2026-07-19/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-1b6d193fe0.pdf | Schedule-only intimation |
| Press Release 24-Jul-2026 (Bagging/Receiving of orders) | 2026-07-24 | 02_RAW_DOCUMENTS/LT/raw/2026-07-26/Bagging-Receiving-of-orders-contracts-423f892721.pdf | No extractable text — corrupt PDF (pdftotext: "Couldn't find trailer dictionary"; 0 pages). Order content unknown; flag for re-collection |
| Newspaper publication – Q1 results advertisement | 2026-07-29 | 02_RAW_DOCUMENTS/LT/raw/2026-08-02/Copy-of-Newspaper-Publication-5ef637e854.pdf | Routine — newspaper publication (duplicates Q1 results) |
| Audio recording of Q1 FY27 earnings call | 2026-07-28 | 02_RAW_DOCUMENTS/LT/raw/2026-08-02/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-4148020ba7.pdf | Link-only intimation; no content |
| ESOP allotment (1,36,908 shares) | 2026-07-28 | 02_RAW_DOCUMENTS/LT/raw/2026-08-02/Allotment-of-Securities-215c076eca.pdf | Routine — ESOP allotment |
| ESG rating – SES 71.3→69.8 | 2026-06-27 | 02_RAW_DOCUMENTS/LT/raw/2026-08-02/Updates-9e8f90ddd5.pdf | ESG score update (unsolicited); not material. Note: cites "safety incidents" and "related party transaction concerns" |
| Schedule of analyst meets (Aug–Sep conferences) | 2026-08-06 | 02_RAW_DOCUMENTS/LT/raw/2026-08-09/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-c7011198da.pdf | Schedule-only intimation |
| Transcript of Q1 FY27 earnings call (intimation) | 2026-08-03 | 02_RAW_DOCUMENTS/LT/raw/2026-08-09/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-f5f2797d8c.pdf | Link-only — transcript hosted on investors.larsentoubro.com, not in filing. Flag for collection |
| ESG rating – NSE Ratings 62 | 2026-08-11 | 02_RAW_DOCUMENTS/LT/raw/2026-08-16/General-Updates-690d31245b.pdf | ESG score update; not material |
| Issue of tokenised NCDs (₹500 cr, 7.40%, Sep-2029) | 2026-09-09 | 02_RAW_DOCUMENTS/LT/raw/2026-09-13/Allotment-of-Securities-efda5a2a39.pdf | NCD issuance intimation — routine debt raise (small vs balance sheet) |
| Press release – first private tokenised bond | 2026-09-09 | 02_RAW_DOCUMENTS/LT/raw/2026-09-13/Press-Release-95feb70365.pdf | Same ₹500 cr NCD event; no financial/theme signal |
| Newspaper publication – NCLT admission & hearing notice | 2026-09-08 | 02_RAW_DOCUMENTS/LT/raw/2026-09-13/Copy-of-Newspaper-Publication-d9251603b3.pdf | Routine — newspaper publication (covered in realty scheme file) |
| ESG rating – Niche99 63 | 2026-09-17 | 02_RAW_DOCUMENTS/LT/raw/2026-09-20/Credit-Rating-f95358569f.pdf | ESG score (filed under "Credit Rating" category); not a credit rating |
| Schedule of analyst meets (CLSA, JPM, BofA, GS NDR) | 2026-09-16 | 02_RAW_DOCUMENTS/LT/raw/2026-09-20/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-69646ddf2a.pdf | Schedule-only intimation |
| ESOP allotment (28,903 shares) | 2026-09-15 | 02_RAW_DOCUMENTS/LT/raw/2026-09-20/Allotment-of-Securities-54d4823020.pdf | Routine — ESOP allotment |
| Trading Window closure (Q2 results) | 2026-09-25 | 02_RAW_DOCUMENTS/LT/raw/2026-09-27/Trading-Window-cb5563e359.pdf | Routine compliance — trading window |
| Schedule of Q2 FY27 earnings call | 2026-10-16 | 02_RAW_DOCUMENTS/LT/raw/2026-10-18/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-353fd33f12.pdf | Schedule-only intimation |
| Reg 74(5) depository certificate (Sep 2026) | 2026-10-12 | 02_RAW_DOCUMENTS/LT/raw/2026-10-18/Certificate-under-SEBI-Depositories-and-Participants-Regulations-2018-adc4b4596a.pdf | Routine — depository certificate |
| Newspaper publication – Q2 results advertisement | 2026-10-28 | 02_RAW_DOCUMENTS/LT/raw/2026-11-01/Copy-of-Newspaper-Publication-1b9cf791a6.pdf | Routine — newspaper publication (duplicates Q2 results) |
| Audio recording of Q2 FY27 earnings call | 2026-10-27 | 02_RAW_DOCUMENTS/LT/raw/2026-11-01/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-6d43baf5d1.pdf | Link-only intimation |
| ESOP allotment (21,098 shares) | 2026-10-27 | 02_RAW_DOCUMENTS/LT/raw/2026-11-01/Allotment-of-Securities-ea1fcc7fc5.pdf | Routine — ESOP allotment |
| Schedule of analyst meets (GS, CLSA, JM — Nov) | 2026-11-06 | 02_RAW_DOCUMENTS/LT/raw/2026-11-08/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-621f9fe906.pdf | Schedule-only intimation |
| RTA (KFin) corporate office address change | 2026-11-04 | 02_RAW_DOCUMENTS/LT/raw/2026-11-08/Updates-1b139ac1b1.pdf | Routine administrative |
| Transcript of Q2/H1 FY27 earnings call (intimation) | 2026-11-02 | 02_RAW_DOCUMENTS/LT/raw/2026-11-08/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-ada8460050.pdf | Link-only — transcript hosted on company website, not in filing. Flag for collection |

## Collection gaps flagged for Collection Agent

1. Q1 FY27 (28-Jul-2026) and Q2 FY27 (27-Oct-2026) earnings-call transcripts — only intimation letters collected; FY27 guidance status (10–12% revenue / order inflow) cannot be confirmed from tier_1 evidence.
2. 24-Jul-2026 press release (hash 423f892721) — corrupt download; re-fetch.
3. No duplicate content hashes found within this batch.
