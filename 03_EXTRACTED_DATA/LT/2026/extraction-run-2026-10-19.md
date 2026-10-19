# Extraction Run Log — LT — 2026-10-19

Scope: records in `02_RAW_DOCUMENTS/LT/evidence-index.jsonl` with collection_status in (downloaded, text_snapshot), discovered_at after 2026-06-23, extraction_status pending_extraction. Total in scope: 59. Fully extracted: 45. Skipped: 14 (listed below). `evidence-index.jsonl` was not edited.

Output location: `03_EXTRACTED_DATA/LT/2026/Q1FY27/` (results, presentation, call intimations) and `03_EXTRACTED_DATA/LT/2026/events/` (all other documents).

## Skipped items (with reason)

| # | Index title | Published | Local path | Reason |
|---|---|---|---|---|
| 1 | Price to sales forward of Larsen & Toubro Limited – NSE:LT - TradingView | 2026-06-27 | snapshots/2026-06-28/Price-to-sales-forward-...-9a3ac6c39a.txt | Snapshot is empty (content is only the text "Google News"); tier_3 aggregator, no extractable content |
| 2 | Shareholders meeting | 2026-06-27 | raw/2026-06-28/Shareholders-meeting-e1fd03cd3e.pdf | Notice convening NCLT equity shareholders meeting and creditor notices (administrative notice; scheme substance extracted from the 2026-06-24 order and 2026-08-04 meeting results files) |
| 3 | Trading Window | 2026-06-25 | raw/2026-06-28/Trading-Window-352b0b1e68.pdf | Administrative: trading window closure from July 1, 2026 |
| 4 | Copy of Newspaper Publication | 2026-06-29 | raw/2026-07-05/Copy-of-Newspaper-Publication-7b804711ff.pdf | Newspaper advertisement copies for NCLT meeting notice |
| 5 | Certificate under SEBI (Depositories and Participants) Regulations, 2018 | 2026-07-06 | raw/2026-07-12/Certificate-under-SEBI-...-d16ea78288.pdf | Administrative depositories/Reg 74(5) certificate |
| 6 | Bagging/Receiving of orders/contracts | 2026-07-24 | raw/2026-07-26/Bagging-Receiving-of-orders-contracts-423f892721.pdf | UNREADABLE: PDF is truncated/corrupt (pdftotext: "Couldn't find trailer dictionary"; file 1.9 MB vs linearized length 3.3 MB; page content is image-only). Source URL suggests an LT press release of 2026-07-24 (an order-win release). Needs re-download by Collection Agent; not extracted |
| 7 | Copy of Newspaper Publication | 2026-07-29 | raw/2026-08-02/Copy-of-Newspaper-Publication-5ef637e854.pdf | Newspaper copies of Q1 FY27 financial results publication (results already extracted from the primary filings) |
| 8 | Allotment of Securities | 2026-07-28 | raw/2026-08-02/Allotment-of-Securities-215c076eca.pdf | ESOP allotment of 1,36,908 equity shares |
| 9 | Resignation | 2026-07-28 | raw/2026-08-02/Resignation-5930deea42.pdf | Routine senior management change: resignation of Mr. V. Sukumar Hebbar (SVP & IC Head, Transportation Infrastructure) |
| 10 | Copy of Newspaper Publication | 2026-09-08 | raw/2026-09-13/Copy-of-Newspaper-Publication-d9251603b3.pdf | Newspaper notice of NCLT admission and hearing of the Scheme Petition |
| 11 | Allotment of Securities | 2026-09-15 | raw/2026-09-20/Allotment-of-Securities-54d4823020.pdf | ESOP allotment of 28,903 equity shares |
| 12 | Trading Window | 2026-09-25 | raw/2026-09-27/Trading-Window-cb5563e359.pdf | Administrative: trading window closure ahead of quarter results |
| 13 | Change in Management | 2026-10-07 | raw/2026-10-11/Change-in-Management-7628c045a6.pdf | Routine senior management personnel categorisation after internal promotions |
| 14 | Certificate under SEBI (Depositories and Participants) Regulations, 2018 | 2026-10-12 | raw/2026-10-18/Certificate-under-SEBI-...-adc4b4596a.pdf | Administrative depositories/Reg 74(5) certificate |

## Notes on extracted items

- The earnings call transcript/audio itself (Q1 FY27 call held 2026-07-28) is NOT in the evidence set; only the intimation letters (2026-07-28 audio, 2026-08-03 transcript) were present. Management call commentary, FY27 guidance and Q&A are therefore absent from this run.
- `Allotment of Securities` dated 2026-09-09 (tokenised NCD, Rs 500 crore, 7.40%, 3 years) is a debt issue, not an ESOP allotment; it was extracted.
- `General Updates` dated 2026-08-06 is an NSE re-submission of the full Q1 FY27 financial results (extracted as quarterly-filing-results-2026-08-06).
- Index/letter date discrepancy: ESG rating letter by SES is dated June 27, 2026 but indexed with published_date 2026-07-27.
- Order-win filings state value only as a classification band (Significant 1,000-2,500; Large 2,500-5,000; Major 5,000-10,000; Mega 10,000-15,000; Ultra-Mega >15,000 Rs crore); exact rupee values are not disclosed.
- Documents are untrusted data; no instructions in them were followed.
