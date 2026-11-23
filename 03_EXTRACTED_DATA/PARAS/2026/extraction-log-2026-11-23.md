# Extraction Log — PARAS DEFENCE & SPACE TECHNOLOGIES (PARAS)
Run date: 2026-11-23
Extracted by: Extraction Agent
Scope: evidence-index.jsonl records with discovered_at > 2026-06-22 and collection_status in (downloaded, text_snapshot);
news-*.md files 2026-06-28 … 2026-11-01 skimmed for context only (tier_3 headlines).
Text extraction: `pdftotext -layout`. All PDFs yielded a text layer (several are scanned with OCR noise — noted in the
relevant extraction files). No file returned empty text, so no "no extractable text" entries this run.

---

## Files written (material documents)

| Date | Document | Output |
|---|---|---|
| 2026-06-30 | IP License Agreement — Tandem Defense LLC (Guardian-1 counter-drone interceptor) | events/ip-license-tandem-defense-guardian-interceptor-2026-06-30.md |
| 2026-07-22 | MoU — Paras Semiconductors with MPSeDC (OSAT) | events/paras-semiconductors-mou-mpsedc-2026-07-22.md |
| 2026-07-22 | Press Release — ₹6,200 cr semiconductor facility | events/press-release-paras-semiconductors-6200cr-osat-2026-07-22.md |
| 2026-07-24 | Appointment of SMP — VP Business Development | events/smp-appointment-vp-business-development-2026-07-24.md |
| 2026-08-07 | Q1 FY27 results (Outcome of Board Meeting) | Q1FY27/quarterly-results.md |
| 2026-08-07 | Divestment of 47.5% in associate Krasny Paras | events/krasny-paras-associate-divestment-2026-08-07.md |
| 2026-08-18 | 17th AGM Notice (material RPT resolutions) | events/agm-notice-material-rpt-2026-08-18.md |
| 2026-09-11 | AGM voting results — RPT resolution 6 defeated | events/agm-voting-results-rpt-resolution-defeated-2026-09-11.md |
| 2026-09-28 | DRDO order ₹26.59 cr (hyperspectral space payload) | events/drdo-hyperspectral-space-payload-order-2026-09-28.md |
| 2026-09-30 | ICRA upgrade to [ICRA]A (Stable) | events/icra-rating-upgrade-2026-09-30.md |
| 2026-10-29 | Q2 / H1 FY27 results (Outcome of Board Meeting) | Q2FY27/quarterly-results.md |
| 2026-11-03 | Corrected Postal Ballot Notice — re-seeking Paras Anti-Drone RPT | events/postal-ballot-rpt-paras-antidrone-2026-11-03.md |

## Skipped — routine / schedule-only / duplicate (no individual file)

| Title | Date | Local path | Reason skipped |
|---|---|---|---|
| Analysts/Institutional Investor Meet (Astute Investment Mgmt, 1x1, Jun 27) | 2026-06-25 | 02_RAW_DOCUMENTS/PARAS/raw/2026-06-28/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-4da2c25783.pdf | Schedule-only intimation; "no Unpublished Price Sensitive Information" |
| Trading Window closure (from Jul 1, 2026) | 2026-06-29 | 02_RAW_DOCUMENTS/PARAS/raw/2026-07-05/Trading-Window-c328f41464.pdf | Routine compliance |
| Reg. 74(5) Depository certificate, Q1 FY27 | 2026-07-07 | 02_RAW_DOCUMENTS/PARAS/raw/2026-07-12/Certificate-under-SEBI-Depositories-and-Participants-Regulations-2018-bccd9bd4f8.pdf | Routine compliance |
| Amendment to PIT Code (Insider Trading policy) | 2026-07-24 | 02_RAW_DOCUMENTS/PARAS/raw/2026-07-26/Updates-e69493b3f1.pdf | Routine policy update (38 pp policy text) |
| Newspaper publication — Q1 FY27 results | 2026-08-08 | 02_RAW_DOCUMENTS/PARAS/raw/2026-08-09/Copy-of-Newspaper-Publication-18eef59234.pdf | Newspaper reproduction of results already extracted (OCR largely illegible) |
| Intimation of 17th AGM date / e-voting cut-off | 2026-08-07 | 02_RAW_DOCUMENTS/PARAS/raw/2026-08-09/Updates-9b5d3f126e.pdf | Schedule-only |
| Record date for final dividend (Aug 28, 2026; ₹1/share) | 2026-08-07 | 02_RAW_DOCUMENTS/PARAS/raw/2026-08-09/Record-Date-2f2679ed09.pdf | Routine; dividend fact captured in Q1FY27 file |
| Investor meet — Citi India Industrials Access Day, Singapore/HK (Aug 11–13; 25 funds incl. Wellington, GSAM, T Rowe Price, Schroders, Allianz) | 2026-08-04 | 02_RAW_DOCUMENTS/PARAS/raw/2026-08-09/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-80e5bee571.pdf | Schedule-only; no UPSI. Noted as context for delta (investor outreach) |
| Investor meet — Motilal Oswal Global Investor Conference (Aug 19; 43 participants) | 2026-08-14 | 02_RAW_DOCUMENTS/PARAS/raw/2026-08-16/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-a69e8ee7b8.pdf | Schedule-only |
| Investor meet — Kotak Manufacturing Forum (Aug 20; 48 participants incl. GIC) | 2026-08-17 | 02_RAW_DOCUMENTS/PARAS/raw/2026-08-23/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-d05b351906.pdf | Schedule-only |
| Investor plant visit, Nerul (Aug 22) | 2026-08-19 | 02_RAW_DOCUMENTS/PARAS/raw/2026-08-23/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-c044ae688d.pdf | Schedule-only |
| Newspaper advertisement — 17th AGM | 2026-08-19 | 02_RAW_DOCUMENTS/PARAS/raw/2026-08-23/Copy-of-Newspaper-Publication-444927357b.pdf | Routine compliance |
| TDS on dividend communication | 2026-08-22 | 02_RAW_DOCUMENTS/PARAS/raw/2026-08-23/Updates-8d72d10b19.pdf | Routine shareholder communication |
| Summary of proceedings, 17th AGM | 2026-09-11 | 02_RAW_DOCUMENTS/PARAS/raw/2026-09-13/Shareholders-meeting-090ebcbafb.pdf | Procedural; MD's FY26 overview/outlook not transcribed in document ("he gave an overview of the performance … and the future outlook"). Chairman Sharad Virji Shah absent; MD Munjal Shah "concerned or interested in Agenda Item no 6" — captured in delta |
| Trading Window closure (from Oct 1, 2026) | 2026-09-19 | 02_RAW_DOCUMENTS/PARAS/raw/2026-09-20/Trading-Window-1d5166a806.pdf | Routine compliance |
| Investor meet — Nuvama Emerging India CEO Forum (Sep 28; 30 participants incl. ADIA 1x1) | 2026-09-24 | 02_RAW_DOCUMENTS/PARAS/raw/2026-09-27/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-b587226575.pdf | Schedule-only |
| Reg. 74(5) Depository certificate, Q2 FY27 | 2026-10-08 | 02_RAW_DOCUMENTS/PARAS/raw/2026-10-11/Certificate-under-SEBI-Depositories-and-Participants-Regulations-2018-97074d9f59.pdf | Routine compliance |
| Newspaper publication — Q2 FY27 results | 2026-10-30 | 02_RAW_DOCUMENTS/PARAS/raw/2026-11-01/Copy-of-Newspaper-Publication-1b5f957475.pdf | Newspaper reproduction (OCR illegible); results extracted from primary filing |
| Investor meet — Ashika Institutional Equities (Nov 5) | 2026-11-02 | 02_RAW_DOCUMENTS/PARAS/raw/2026-11-08/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-eec88c6d6f.pdf | Schedule-only |
| Original Postal Ballot Notice (superseded by corrigendum) | 2026-11-03 | 02_RAW_DOCUMENTS/PARAS/raw/2026-11-08/Shareholders-meeting-c85808497e.pdf | Superseded — company states incorrect version uploaded; corrected version extracted |
| Newspaper advertisement — Postal Ballot | 2026-11-04 | 02_RAW_DOCUMENTS/PARAS/raw/2026-11-08/Copy-of-Newspaper-Publication-7e76d68846.pdf | Routine compliance |
| Investor meet — BofA India Corporate Day, Singapore (Nov 16–17; incl. Morgan Stanley IM, UBS AM, Fullerton) | 2026-11-12 | 02_RAW_DOCUMENTS/PARAS/raw/2026-11-15/Analysts-Institutional-Investor-Meet-Con.-Call-Updates-4b41493e7a.pdf | Schedule-only |
| Duplicates in raw/2026-11-15/ (Analysts b587226575 & eec88c6d6f, Bagging 6a77f1f561, Certificate 97074d9f59, Newspaper 1b5f957475 & 7e76d68846, Credit-Rating c0dd39a25b, General-Updates f5aa7c6019, Outcome e6b0afaf52, Shareholders c85808497e, Trading-Window 1d5166a806) | — | 02_RAW_DOCUMENTS/PARAS/raw/2026-11-15/*.pdf | Byte-identical (same MD5) to earlier copies; index rows for 2026-11-15 are metadata_only |

## Not processed — metadata_only (no local text)

News RSS rows (TradingView, Upstox, Univest, Kalkine, Alice Blue, HDFC Sky, Whalesbook, simplywall.st, siam.in, Business
Standard, India Infoline, Moneycontrol) between 2026-06-28 and 2026-11-01. Treated as tier_3 context only. Notable
uncorroborated headline: "Paras Defence: Stock in radar after bagging ₹80.28 Cr DRDO order for air defence optics"
(Alice Blue, 2026-10-07) — no matching exchange filing in evidence.

## Follow-up on June 2026 "Change in Auditors" risk alert

- The June filing (02_RAW_DOCUMENTS/PARAS/raw/2026-06-22/Change-in-Auditors-2568a81c93.pdf, MD5 5f62a914…) is
  byte-identical to the Q4 FY26 "Outcome of Board Meeting" and "Dividend" PDFs in the same folder. Its content is
  "Re-appointment of internal Auditor" (M/s S M L and Co. LLP) and "Re-Appointment of Cost Auditor" (M/s Dinesh Jain &
  Company) for FY2026-27 — "Reason for Change … Re-appointment".
- Statutory auditor unchanged: CHATURVEDI & SHAH LLP (FRN 101720W/W100355) signed the FY26 audit report ("unmodified
  opinion"), the Q1 FY27 limited review (Aug 7, 2026) and the Q2 FY27 limited review (Oct 29, 2026), both "unmodified".
  The 17th AGM agenda contained no statutory-auditor appointment/removal item.
- Status: RESOLVED — benign (exchange category label, not a statutory auditor change).

## Data gaps

- No PARAS news-*.md file after 2026-11-01 (news feed appears to have dropped for 2026-11-08, 11-15, 11-22 fetches).
- No earnings-call transcript or investor presentation for Q1 or Q2 FY27 in evidence (intimations state "The
  presentation is available on the website" but the deck itself was not collected).
- Order book not disclosed in any filing since June.
- Postal ballot result (Paras Anti-Drone RPT) not yet in evidence.
