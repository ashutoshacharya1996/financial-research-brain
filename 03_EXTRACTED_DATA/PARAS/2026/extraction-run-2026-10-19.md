# Extraction Run — PARAS — 2026-10-19

Scope: records in `02_RAW_DOCUMENTS/PARAS/evidence-index.jsonl` with collection_status in (downloaded, text_snapshot), discovered_at after 2026-06-23, extraction_status pending_extraction. 27 records in scope: 13 extracted, 14 skipped as administrative. `evidence-index.jsonl` not modified.

## Extracted (13)

| Filing date | Document | Output file |
|---|---|---|
| 2026-06-25 | Investor meet intimation (Astute, 27 Jun) | events/investor-meet-2026-06-25.md |
| 2026-06-30 | IP License Agreement (Tandem Defense / Powerus) | events/agreement-2026-06-30.md |
| 2026-07-22 | Press Release (MP semiconductor MoU) | events/press-release-2026-07-22.md |
| 2026-07-22 | General Updates (MPSeDC MoU) | events/mou-general-update-2026-07-22.md |
| 2026-08-04 | Investor meet intimation (Citi Access Day) | events/investor-meet-2026-08-04.md |
| 2026-08-07 | Outcome of Board Meeting (Q1 FY27 results) | Q1FY27/quarterly-results-2026-08-07.md |
| 2026-08-07 | Divestment of Krasny Paras stake | events/divestment-2026-08-07.md |
| 2026-08-14 | Investor meet intimation (Motilal Oswal conference) | events/investor-meet-2026-08-14.md |
| 2026-08-17 | Investor meet intimation (Kotak Manufacturing Forum) | events/investor-meet-2026-08-17.md |
| 2026-08-19 | Investor meet intimation (plant visit, 22 Aug) | events/investor-meet-2026-08-19.md |
| 2026-09-24 | Investor meet intimation (Nuvama CEO Forum) | events/investor-meet-2026-09-24.md |
| 2026-09-28 | Order from DRDO | events/order-win-2026-09-28.md |
| 2026-09-30 | Credit rating (ICRA upgrade) | events/credit-rating-2026-09-30.md |

## Skipped (14)

| Filing date | Document (content hash prefix) | Reason |
|---|---|---|
| 2026-06-29 | Trading Window (c328f41464) | Administrative: trading window closure notice |
| 2026-07-07 | Certificate under SEBI (Depositories and Participants) Regulations, 2018 (bccd9bd4f8) | Administrative: SEBI depositories compliance certificate |
| 2026-07-24 | Updates (e69493b3f1) | Administrative: amended Code for Prohibition of Insider Trading / UPSI policy; no business signal |
| 2026-07-24 | Appointment (e3709d658d) | Routine management change: appointment of Ms. Anushka Munjal Shah as VP-Business Development / Senior Management Personnel |
| 2026-08-07 | Updates (9b5d3f126e) | Shareholders-meeting notice: intimation of 17th AGM date (11 Sep 2026), cut-off date and e-voting window |
| 2026-08-07 | Record Date (2f2679ed09) | Administrative: record date 28 Aug 2026 for FY26 final dividend of Rs. 1/share (dividend already recommended 13 May; also stated in the Q1 board-outcome letter) |
| 2026-08-08 | Copy of Newspaper Publication (18eef59234) | Newspaper publication copy (results/notice advertisement) |
| 2026-08-19 | Copy of Newspaper Publication (444927357b) | Newspaper publication copy |
| 2026-08-18 | Shareholders meeting (0dd90b98be) | AGM notice plus FY26 Annual Report cover filing; content is AGM notice, e-voting instructions and RPT explanatory statements. Flag: explanatory statement mentions Controp-Paras order from L&T for CIWS program, Paras Indian Content "valued at approx. Rs. 293 Crore", RPT limits Rs. 450 Crore; reviewer may wish to extract separately |
| 2026-08-22 | Updates (8d72d10b19) | Shareholder communication on TDS on dividend; administrative/tax |
| 2026-09-11 | Shareholders meeting (090ebcbafb) | Summary of proceedings of 17th AGM; administrative |
| 2026-09-11 | Shareholders meeting (dc15072a80) | AGM voting results (Reg 44(3)); administrative. Flag: filing states resolution 6 (RPT with Paras Anti-Drone Technologies Pvt Ltd) "was not passed with requisite majority"; resolutions 1 to 5 passed |
| 2026-09-19 | Trading Window (1d5166a806) | Administrative: trading window closure notice |
| 2026-10-08 | Certificate under SEBI (Depositories and Participants) Regulations, 2018 (97074d9f59) | Administrative: SEBI depositories compliance certificate |

## Notes

- Investor-meet intimations contain no financial or management content (each states no UPSI to be shared); extracted for the event record and Theme Signal Log only.
- The Q1 FY27 filing is a results table (scanned); numbers were verified against page images. No press release, presentation or call transcript for Q1 FY27 is in scope, so guidance, order book and margin commentary are not available.
