# Extraction Run Log — JNK India Ltd (JNKINDIA)
Run date: 2026-10-19
Agent: Extraction Agent
Scope: evidence-index.jsonl records with collection_status in (downloaded, text_snapshot), discovered_at after 2026-06-23, extraction_status pending_extraction (26 records). evidence-index.jsonl not modified.

## Extracted (15 documents)

| Published | Document | Output file |
|---|---|---|
| 2026-07-16 | Update: UAE incinerator order cancelled | events/order-cancellation-2026-07-16.md |
| 2026-08-07 | Intimation: Emkay Global Conference meeting (14 Aug) | events/investor-meet-schedule-emkay-2026-08-07.md |
| 2026-08-07 | Intimation: Q1FY27 earnings call invite | events/earnings-call-invite-2026-08-07.md |
| 2026-08-11 | Q1FY27 Press Release | Q1FY27/press-release-2026-08-11.md |
| 2026-08-11 | Outcome of Board Meeting (results, MOA amendment, Iraq branch) | Q1FY27/board-outcome-2026-08-11.md |
| 2026-08-11 | Q1FY27 Investor Presentation (original; erroneous standalone slide) | Q1FY27/investor-presentation-2026-08-11.md |
| 2026-08-12 | Revised Q1FY27 Investor Presentation | Q1FY27/investor-presentation-2026-08-12.md |
| 2026-08-12 | Audio recording intimation of Q1FY27 call | events/earnings-call-audio-2026-08-12.md |
| 2026-08-13 | CRISIL Monitoring Agency Report (IPO proceeds) | events/monitoring-agency-report-2026-08-13.md |
| 2026-08-14 | Corporate presentation (Emkay conference) | events/investor-presentation-emkay-2026-08-14.md |
| 2026-08-19 | Q1FY27 earnings call transcript (call 2026-08-12) | Q1FY27/earnings-call-2026-08-12.md |
| 2026-09-03 | Annual Report FY26 + AGM notice (index title "Shareholders meeting") | Q4FY26/annual-report-2026-09-03.md |
| 2026-09-11 | Intimation: investor meetings 22 Sep 2026 | events/investor-meet-schedule-2026-09-11.md |
| 2026-09-24 | CRISIL credit rating revision | events/credit-rating-2026-09-24.md |
| 2026-09-29 | Two flare package orders (domestic) | events/order-win-2026-09-29.md |

Triage note: the 2026-09-03 "Shareholders meeting" filing was extracted rather than skipped because it contains the full FY26 Annual Report (substantive), not just an AGM notice. Extraction was limited to highlights, management messages, MD&A and Board's Report financial sections.

## Skipped (11)

| Published | Document (index title) | Local file hash | Reason |
|---|---|---|---|
| 2026-06-26 | JNKINDIA Forecast - Price Target - Prediction for 2027 - TradingView (News RSS snapshot) | 9a3ac6c39a | Snapshot contains only the text "Google News"; no extractable content (unusable) |
| 2026-06-25 | Trading Window | 9fb5e46eb7 | Administrative: trading window closure from 1 Jul 2026 (insider trading code) |
| 2026-07-10 | Certificate under SEBI (Depositories and Participants) Regulations, 2018 | 811638d1d7 | Administrative: Reg 74(5) RTA certificate for quarter ended 30 Jun 2026 |
| 2026-08-13 | Copy of Newspaper Publication | f58ab8f6bb | Newspaper copy of Q1FY27 results (Financial Express / Navshakti); duplicates results already extracted; Marathi text not machine-readable |
| 2026-09-04 | Record Date | 6680fc6d29 | Administrative: book closure 19-25 Sep 2026, record date 18 Sep 2026 for FY26 final dividend |
| 2026-09-04 | Updates (AGM notice / annual report weblink letter) | 29d4220970 | Administrative: Reg 36(1)(b) letter sent to shareholders without registered email |
| 2026-09-04 | Copy of Newspaper Publication | c2664affe8 | Newspaper publication copy (AGM / e-voting notice type); administrative |
| 2026-09-25 | Shareholders meeting (AGM summary of proceedings) | cfabd8a9d5 | Shareholders-meeting filing; procedural summary of 16th AGM (agenda items, no financial data or outlook) |
| 2026-09-29 | Shareholders meeting (Scrutinizer's report and e-voting results) | e5954cd624 | Shareholders-meeting filing; voting results only |
| 2026-09-28 | Trading Window | c3cca2f173 | Administrative: trading window closure from 1 Oct 2026 |
| 2026-10-14 | Certificate under SEBI (Depositories and Participants) Regulations, 2018 | 6b8175be4f | Administrative: Reg 74(5) RTA certificate for quarter ended 30 Sep 2026 |

## Data quality flags

- Guidance conflict: Q1FY27 earnings call (2026-08-12) states revenue growth 20-25% and EBITDA margin 12-14%; Aug 2026 corporate presentation (filed 2026-08-14) states EBITDA margin 14-15% and revenue growth 25-30% for FY27. Both recorded as printed.
- Original Q1FY27 investor presentation (2026-08-11) had incorrect standalone P&L; management acknowledged the error on the call and filed a revised deck on 2026-08-12.
- Press release text quotes "Rs. 10.30 cr in Q1FY26" total income while the table shows 103.0.
- Board outcome filing results pages are scanned images; OCR figures may contain noise.
- Decks show "BSE: 544220" while exchange letters give scrip code 544167.
- Existing earlier extraction press-release-uae-order-2026-06-08.md is superseded in status by the cancellation filing (order-cancellation-2026-07-16.md); the earlier file was not edited.
- Metadata-only records (news RSS, Change in Management, Integrated Filing, Outcome of Board Meeting, AOA/MOA, etc.) were out of scope (status not downloaded/text_snapshot).
