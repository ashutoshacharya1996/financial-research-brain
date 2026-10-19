# Extraction Run Log — GABRIEL (Gabriel India Ltd)
Run date: 2026-10-19
Extracted by: Extraction Agent
Scope: evidence-index.jsonl records with collection_status in (downloaded, text_snapshot), discovered_at after 2026-06-23, extraction_status pending_extraction (38 records, all NSE tier_1 PDFs). evidence-index.jsonl was not modified.

## Summary
- Records in scope: 38
- Extracted (one file each): 23
- Skipped as administrative: 15
- Not processed (out of scope): 1 record (NDTV Profit snapshot, discovered 2026-06-22, not after 2026-06-23)

## Files written (under 03_EXTRACTED_DATA/GABRIEL/2026/)
- Q1FY27/quarterly-results-2026-07-21.md (Board outcome incl. Q1 FY27 unaudited results; index title "Amendment to AOA/MOA")
- Q1FY27/investor-presentation-2026-07-21.md (Q1 FY27 investor presentation)
- Q1FY27/investor-presentation-2026-07-21-2.md (Business Update Presentation, Project Jupiter; index title "General Updates")
- events/acquisition-hl-klemove-2026-07-21.md
- events/earnings-call-intimation-2026-07-17.md
- events/earnings-call-recording-2026-07-22.md
- events/earnings-call-transcript-2026-07-29.md (notice only; transcript not in evidence)
- events/investor-meet-2026-07-27.md, investor-meet-2026-08-03.md, investor-meet-2026-09-09.md, investor-meet-2026-09-10.md (cancellation), investor-meet-2026-09-21.md
- events/credit-rating-2026-07-30.md (Crisil upgrade AA to AA+)
- events/credit-rating-2026-08-27.md (Crisil NCD assignment + rationale)
- events/acquisition-2026-08-21.md
- events/amendment-aoa-moa-2026-08-19.md
- events/press-release-2026-08-26.md
- events/outcome-of-board-meeting-2026-08-24.md
- events/clarification-valuation-2026-09-01.md
- events/preferential-allotment-2026-09-11.md
- events/committee-meeting-ncd-allotment-2026-09-10.md
- events/press-release-2026-10-06.md
- events/outcome-of-board-meeting-2026-10-06.md

## Skipped items (administrative)
| Index title | Published | Local evidence | Reason |
|---|---|---|---|
| Disclosure under SEBI Takeover Regulations | 2026-06-29 | raw/2026-07-05/Disclosure-under-SEBI-Takeover-Regulations-7e901bca42.pdf | Scanned PDF (no text layer; read visually). Asia Investments Pvt Ltd Reg 31(4)&(5) declaration of no encumbrance on promoter shares for FY2025-26; compliance disclosure, no financial/business signal. |
| Trading Window | 2026-06-29 | raw/2026-07-05/Trading-Window-27fd0f112d.pdf | Trading window closure from July 1, 2026 for Q1 FY27 results; administrative. |
| Reply to Clarification- Financial results | 2026-07-09 | raw/2026-07-12/Reply-to-Clarification--Financial-results-d4c4a2ced6.pdf | Reply to NSE deficiency email on May 27 board outcome (segment disclosure not required; revised XBRL uploaded); administrative/XBRL housekeeping. |
| Copy of Newspaper Publication | 2026-07-25 | raw/2026-07-26/Copy-of-Newspaper-Publication-4b6d171ddb.pdf | Newspaper copy of 64th AGM notice, e-voting, record date and book closure; AGM administrative. |
| Change in Director(s) | 2026-07-21 | raw/2026-07-26/Change-in-Director-s-38949d665b.pdf | Routine management change: Mr. Mahendra K. Goyal appointed Executive Director and Group CEO & MD (July 21, 2026 to July 20, 2031); Mr. Atul Jaggi re-designated Managing Director (Ride Control). Skipped per triage rule; flagged here for awareness. |
| Copy of Newspaper Publication | 2026-07-29 | raw/2026-08-02/Copy-of-Newspaper-Publication-3b92ce74b1.pdf | Newspaper copy of 64th AGM notice and e-voting information. |
| Updates | 2026-07-28 | raw/2026-08-02/Updates-d927b2847b.pdf | 64th AGM date (Aug 19, 2026), record date (Aug 12) and book closure (Aug 13-19) notice; AGM/record date administrative. |
| Shareholders meeting | 2026-07-28 | raw/2026-08-02/Shareholders-meeting-0c178193ac.pdf | Notice of 64th AGM (long document); AGM notice. |
| General Updates | 2026-08-07 | raw/2026-08-09/General-Updates-6ade4b5e6b.pdf | Clarification deleting a "Sub-total" row in AGM Notice table; AGM administrative. |
| Resignation | 2026-08-06 | raw/2026-08-09/Resignation-98c5faa111.pdf | Resignation of Company Secretary & Compliance Officer (Mr. Nilesh Jain); routine KMP change. |
| Shareholders meeting | 2026-08-20 | raw/2026-08-23/Shareholders-meeting-57934f9b1d.pdf | Scrutinizer's report and voting results of 64th AGM; shareholders-meeting administrative. |
| General Updates | 2026-08-20 | raw/2026-08-23/General-Updates-0efdab0f6e.pdf | Revised last working day (Aug 24, 2026) of Company Secretary; routine KMP change. |
| Shareholders meeting | 2026-08-19 | raw/2026-08-23/Shareholders-meeting-7e6292b263.pdf | Summary of proceedings of 64th AGM (includes final dividend Rs 3.10 per share resolution, auditor re-appointment); AGM administrative. |
| Trading Window | 2026-09-24 | raw/2026-09-27/Trading-Window-b8453d4682.pdf | Trading window closure from Oct 1, 2026 for Q2 FY27 results; administrative. |
| Copy of Newspaper Publication | 2026-10-02 | raw/2026-10-04/Copy-of-Newspaper-Publication-c99f9f203c.pdf | Newspaper notice of special window for re-lodgement of physical share transfer requests; administrative. |

## Data-quality flags
- Evidence record titled "Amendment to AOA/MOA" (published 2026-07-21, Jupiter_signed.pdf) actually contains the full July 21, 2026 Board outcome with Q1 FY27 standalone and consolidated results, the HL Mando Anand acquisition and the preferential allotment; extracted as quarterly-results.
- Evidence record titled "General Updates" (2026-07-21) is the Business Update Presentation on Project Jupiter.
- Written transcript of the Q1 FY27 earnings call is NOT in the evidence set (only the filing notice and an audio link); no Q&A or management commentary on the call could be extracted.
- Investor presentation: HL Klemove India adjusted EBITDA text layer reads "~ Rs 1293 Cr" (footnote marker adjoining); the Crisil rationale (separate file) states ~Rs 129 crore.
- Filing "Written Transcript" subject line says "Q1 FY26" while body says Q1 FY27 (as printed in source).
- Comparatives for Q1 FY26 and Q4 FY26 are restated (pooling of interest) and are not limited-reviewed for the Automotive Undertaking per the auditor.
