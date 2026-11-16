# Delta Analysis — JNK INDIA LTD (JNKINDIA)
Period: Q2 FY27 (Jul-Sep 2026) vs Q1 FY27 (Apr-Jun 2026) vs Q4 FY26 (Jan-Mar 2026), plus event deltas 2026-06-28 to 2026-11-15
Analysis date: 2026-11-16
Prior delta files: delta-2026-Q4.md, delta-2026-june-update.md, delta-2026-june22-update.md (this file does not overwrite them)
Source documents (all tier_1 exchange filings unless labelled):
  Current: 03_EXTRACTED_DATA/JNKINDIA/2026/Q2FY27/{press-release,investor-presentation,earnings-call}.md
  Intermediate: 03_EXTRACTED_DATA/JNKINDIA/2026/Q1FY27/{press-release,investor-presentation,earnings-call}.md
  Prior: 03_EXTRACTED_DATA/JNKINDIA/2026/Q4FY26/{press-release-q4fy26,earnings-call}.md (the Q4 call extraction is from search snippets, not a transcript; treat its guidance and commentary as unverified)
  Events: 03_EXTRACTED_DATA/JNKINDIA/2026/events/ (order-cancellation-uae-2026-07-16, board-outcome-q1-results-2026-08-11, monitoring-agency-report-2026-08-13, corporate-presentation-emkay-2026-08-14, annual-report-fy26-2026-09-03, credit-rating-revision-2026-09-24, order-wins-flare-packages-2026-09-29, order-win-nigeria-jnk-global-2026-11-03, board-outcome-cfo-change-2026-11-05, routine-filings roll-up)
  Context only (tier_3): 02_RAW_DOCUMENTS/JNKINDIA/prices-*.json (yfinance), news-*.md headlines
  Open-blocker reference: 08_PORTFOLIO_INPUTS/investment-impact/JNKINDIA-impact-2026-06-22.md

Basis warning: Q1 was reported as "Total Income" with EBITDA INCLUDING other income. Q2 is reported as "Total Operational Revenue" with EBITDA EXCLUDING other income (guidance is "based on Total Operational Revenue"). The Q2 deck restates Q1 (= H1 less Q2). Restated Q1 and Q1FY26 figures below are derived arithmetic (H1 minus Q2) and are labelled "restated".

---

## Headline Delta

Growth stalled in Q2 FY27 (total operational revenue +3.4% YoY after +80.6% in Q1 and +69.2% in Q4 FY26), the order book has shrunk for two straight quarters (Rs 1,961 cr to 1,801 cr to 1,662 cr), the one named export order underpinning the June thesis (UAE/ADNOC) was cancelled, and management still holds FY27 guidance of 20-25% revenue growth and 12-14% EBITDA margin, which now rests on an H2 that must deliver roughly 63-64% of the year; the only offset is a ~Rs 500 cr Nigeria order received on 3 Nov from promoter JNK Global (related party).

## Financial Metric Deltas (consolidated, Rs Cr)

| Metric | Q4 FY26 | Q1 FY27 | Q2 FY27 | Delta Type | Signal Strength | Notes |
|---|---|---|---|---|---|---|
| Revenue (YoY) | Total income 344.6, +69.2% | Total income 186.0, +80.6% (restated total operational revenue 182.7, ~+78% vs derived Q1FY26 102.5) | Total op. revenue 187.5, +3.4% (Revenue from ops 184.0, +3.2%) | Inflection down (sharp deceleration) | High | Q2 vs restated Q1 +2.6% QoQ. H1 FY27 370.2, +30.4% YoY. Mgmt cites "shipment delays and monsoon related disruption"; "around INR30 crores-INR40 crores" deferred. |
| EBITDA margin | 15.2% (incl. other income) | 11.8% as first reported (incl. OI); restated 10.2% (18.6/182.7, ex-OI) | 11.1% (ex-OI); H1 10.6% | Stable at lower level vs Q4; Q2 up ~90 bps vs restated Q1 | Medium | FY26 on ex-OI basis 12.5% (104.2/830.8). Margin is below the 12-14% guidance band lower end for H1. Employee cost Q2 21.0 vs 14.4 (+46% YoY); gross margin 26.2% vs 23.5%. |
| EBITDA (absolute) | 52.3 | 21.9 as reported (restated 18.6) | 20.8 (+6.6% YoY) | Deceleration | Medium | Standalone Q2 EBITDA 18.2 vs 20.1 (-9.5% YoY), margin 10.4%. |
| PAT | 33.0 (9.6%) | 9.6 (5.2%) | 13.3 (7.1%), +2.0% YoY | Deceleration (YoY +8.5x to +2.0%) | High | Q2 PBT 17.4 vs 17.8 (-2.0% YoY). Other income 5.1 vs 2.8; finance cost 4.9 vs 2.8; depreciation 3.5 vs 1.7. Standalone PAT 13.0 vs 13.6 (-4.1%). |
| Order book | 1,961.4 (31 Mar) | 1,801 (30 Jun) | 1,662 (30 Sep) | Inflection down | High | -8.2% then -7.7% QoQ; -15.3% vs March. Excludes the ~Rs 500 cr Nigeria order received 3 Nov (not yet in a reported order book). Management: "about INR1,500 crores of revenue ... available for the execution in the next financial year." |
| Order inflows | FY26 1,694.4 | Not disclosed for quarter | FY27 YTD ~Rs 530 cr to 5 Nov (slide chart; = ~500 Nigeria + 30 flares) | Deceleration | High | Derived implied net inflow from order-book roll-forward (revenue + change in book): ~Rs 22 cr Q1, ~Rs 49 cr Q2 (approximate; ignores adjustments; unclear whether Jun-30 book included the cancelled UAE order). Book-to-bill FY26 was ~2.0x. |
| Bid pipeline | n/a (not in Q4 extraction) | ~Rs 6,000 cr (analyst: up from 4,000) | ~Rs 5,000 cr ex recent wins | Deceleration | Medium | Some reduction is conversion; mgmt cites 50:50 domestic/export and 50:50 heater/non-heater. |
| Capex | not stated | not stated | PPE 24.3 vs 14.2 (Mar); CWIP 2.1 vs 8.4 | Stable | Low | No capacity capex announcement found in any document (see blocker 3). |
| Receivables / working capital | n/a | Unbilled revenue ~Rs 200-221 cr | Trade receivables (current) 390.6 vs 344.8 (Mar); payables 155.6 vs 191.3; cash & equivalents 6.9 vs 32.1; bank balances other 212.4 vs 166.9; borrowings (current) 82.3 vs 72.6; H1 CFO 2.8 vs 10.3 | Inflection down | High | Changes in working capital -14.1 (vs -4.2); taxes paid 15.2 (vs 5.2). Other current liabilities 268.1 vs 168.0 (not labelled in the deck; do not read as advances). |

## Management Tone Delta

**Demand commentary:**
- Prior (Q4 FY26 press release, 2026-05-20): "JNK India is well-positioned to capture opportunities in both traditional and sustainable energy sectors in India and abroad."
- Q1 (call 2026-08-12): "We continue to see encouraging traction across both domestic and international markets."
- Current (Q2 call 2026-11-06): "Large and technically complex projects can have longer decision-making cycles." and "October, generally October, November, we don't improve so much."
- Delta: Deteriorating (from confident to explaining delays; recovery pushed to Dec-Mar). Signal strength: Medium.

**Margin commentary:**
- Prior: Q4 FY26 exit margin 15.2% (incl. OI); FY27 target 14-15% per earlier extraction (unverified).
- Q1: "for JNK India alone, we have achieved an EBITDA of 14%, which is as per the guideline" (consolidated 11.8%; Chemdist "operating loss of about INR 3.6 crores").
- Current: "the EBITDA also we have achieved in excess of 11%"; commodity: "if you talk about copper, nickel, or any other aluminum fluctuating, that's a business risk."
- Delta: Deteriorating vs Q4/earlier guide; stable QoQ. Signal strength: High.

**Guidance:**
- Prior (Q4 FY26 extraction; secondary sources, unverified): FY27 revenue +25-30%, EBITDA 14-15%.
- Q1 call: "Our revenue growth guidance of around 20% to 25% remains intact ... EBITDA margin guidance of about 12% to 14%." Asked about the change from 14-15%, CEO: "For our understanding, what we have announced was 12% to 14%. But for some reason, we are missing something, these numbers, we'll recheck them. But there is no change". The corporate deck filed 2026-08-14 still says "On track for EBITDA margin guidance of 14 -15% and revenue growth of 25-30% for FY27".
- Current (Q2): "we continue to maintain our FY27 guidance of 20%-25% revenue growth and in EBITDA margin of 12%-14% on the operational revenue."
- Delta: Lowered vs the prior extraction (high-signal if the 25-30%/14-15% figures were company-stated; provenance unverified) and Maintained Q1 to Q2. Management disputes that any cut occurred. Derived H2 requirement: FY26 total operational revenue 830.8 x 1.20-1.25 = ~997-1,039; H1 370.2, so H2 needs ~627-669 (+14.7% to +22.3% YoY vs H2 FY26 546.9; ~63-64% of the year). To land the FY EBITDA margin at 12%, H2 margin must be ~12.8% (vs H1 10.6%); at 14%, ~15.9%.

**Green hydrogen / renewables:**
- Prior (Q4 FY26 PR): Chemdist "contributed ~7% share to the Group revenue"; green hydrogen order inflows named.
- Q1: Chemdist 8.8% of group revenue; "executing the green hydrogen project" ~Rs 50 cr "should get completed almost say, in this year"; "by year-end, we should be able to get it into the green"; JV revenue "anywhere about 10% to 15% of JNK India revenue".
- Current: Chemdist order book "about INR20 crores"; "will take some time, maybe about two years or so, to actually culminate into a larger amount of revenues"; Process Equipment segment revenue Q2 11.66 vs Q1 16.25 (Rs Cr, from filing, INR million 116.55 vs 162.53); segment result turned to +0.81 from -1.33 (OCR-derived). H1 segment revenue 27.9 = 7.7% of H1 revenue from operations vs 10-15% FY guide. Green hydrogen is not named in the Q2 press release.
- Delta: Weakening. Signal strength: Medium.

**International:**
- Prior: UAE TA'ZIZ/ADNOC incinerator order (2026-06-08; Rs 100-300 cr class), "first major export order"; 97.5% of order book domestic (Q4 extraction).
- Q1: order cancelled (communication dated 2026-07-16); "this is very rarest of rare case rather in last 15 years"; new Iraq registered office; Africa (Nigeria, Ethiopia) focus; "All export projects, we will be doing together. I mean, JNK Global will be getting the orders and they will be subcontracting to us. It is a back-to-back basis."
- Current: ~Rs 500 cr Nigeria heater package from JNK Global (Major class; related-party, arm's length), "the largest export order on us till date" and "a repeat order which we had successfully executed 10 years back"; Kenya refinery inquiries expected Dec, order finalisation in 4-5 months; Nigeria/fertilizer further Rs 700-800 cr in pipeline; Dangote balance scope "possibility ... We can expect in another two to three months".
- Delta: Mixed. Original anchor lost; replaced by a larger but promoter-routed order. Signal strength: High.

## Theme Signal Deltas

| Theme Category | Prior Period (Q4 FY26 / Jun update) | Current Period (Q1-Q2 FY27) | Delta |
|---|---|---|---|
| Export / global markets | Strong (UAE order; "India and abroad") | Mixed: UAE cancelled; ~Rs 500 cr Nigeria via related party; Kenya/Dangote pipeline; Iraq office | Weakening, then partially restored (quality lower: related-party, back-to-back) |
| EV / energy transition (green hydrogen, renewables) | Strong (Chemdist ~7% revenue; green hydrogen orders) | Chemdist order book Rs 20 cr; large revenue "about two years"; renewable named but unspecific in Q2 PR | Weakening |
| Manufacturing / PLI / capex cycle | Strong (order book 1,961, +81% YoY) | Order book 1,662; pipeline 5,000 (from 6,000); BPCL Bina execution; BPCL Vizag (about Rs 5,000 cr opportunity, tenders in 6-8 months, not in pipeline); NTPC bids due 20 Nov; new offshore/metals/minerals line | Stable demand pipeline, weakening conversion |
| Margin expansion / operating leverage | Strong (Q4 15.2%; operating leverage visible) | H1 10.6%; Q2 11.1%; employee cost +46% YoY; guidance band 12-14% | Weakening |
| Working capital improvement | Mentioned positively in impact note (not corroborated) | Receivables up, cash down, CFO weak; BG limit enhancement needed; CRISIL limits raised to Rs 604 cr, outlook to Stable; unbilled Rs ~200-221 cr; IPO proceeds fully absorbed by working capital | Weakening (credit outlook improved) |
| Grid / Defence / Data centre / Railways | Absent | Absent | Not a theme for this company |

## New Mentions This Period
- Order cancellation: "informing that the aforesaid order stands cancelled" (2026-07-16)
- New line of business and Iraq branch: "adoption of new line of business" (mining/steel/cement EPC, offshore, marine/heavy-lift, BOO/BOT); medium-term target "around 3 to 5 years, we want to move this non-heating segment to around 40% of our revenue"
- CFO change (third CFO since Dec 2025): "Mr. Praveen Sood as the Chief Financial Officer ... with effect from November 12, 2026"
- CRISIL: "Outlook revised from 'Negative'; Rating Reaffirmed" (A-/Stable; facilities Rs 604 cr from Rs 457 cr)
- JNK Global activist dispute raised by an analyst: "matter is sub judice, we would not like to comment on that as of now"
- Disclosure quality: Q1 standalone P&L errors in first deck ("some kind of error in the standalone numbers"); Nigeria order range "300 to 600" admitted error
- Revenue recognition: "now we are going on the input method" (contract assets/unbilled)
- Trade receivable ageing at 31 Mar 2026 (annual report, standalone): Rs 1,087.5 million (35.5% of gross) outstanding more than 1 year from due date

## Dropped Mentions
- UAE/ADNOC TA'ZIZ order and the "H2 FY27 shipment" framing: absent from Q2 materials (last seen: "Incinerator Package ... TA'ZIZ Salt Project, ADNOC" 2026-06-08)
- Green hydrogen by name in the Q2 press release (last seen Q1 PR: "They are executing the green hydrogen project")
- The 25-30% / 14-15% FY27 guidance (last seen Q4 FY26 extraction and 2026-08-14 deck)
- Q1 pipeline "~Rs 6,000 cr" replaced by ~Rs 5,000 cr

## Event Deltas (2026-06-28 to 2026-11-15)
- 2026-07-16 UAE order terminated by CC7 (licensor approval not received); "no impact on declared revenue and associated profit"; no costs incurred per mgmt.
- 2026-08-11 Board: new business line, Iraq branch, SMP changes; ratified at AGM (2026-09-25; all items passed; related-party item 6 had 7.26% against; Bang Hee Kim fee item 5 had 9.54% against).
- 2026-08-13 CRISIL monitoring report: IPO proceeds Rs 2,816.99m fully utilised (Rs 2,646.50m working capital, Rs 170.49m general corporate purposes); no deviation.
- 2026-09-24 CRISIL A-/Stable (outlook from Negative); facilities Rs 604 cr.
- 2026-09-28/29 two flare orders (~Rs 30 cr aggregate, 16 months).
- 2026-11-03 ~Rs 500 cr Nigeria heater package from JNK Global (18 months FOB; related-party).
- 2026-11-05 Interim CFO resigned; new CFO from 12 Nov.
- Price context (tier_3, yfinance): close Rs 475.5 (2026-06-28) to Rs 456.25 (08-16) to Rs 380.4 (11-08) to Rs 366.55 (11-15); P/E 41.2 to 27.1; 52-week high Rs 558. Headlines: +9.21% on 14 Aug after Q1; -6.27% to Rs 370.70 on 6 Nov (Q2 day) (tier_3 news).

## Open Blocker Status (from 08_PORTFOLIO_INPUTS/investment-impact/JNKINDIA-impact-2026-06-22.md)

DATA-INTEGRITY NOTE ON THE IMPACT NOTE: several inputs in that note do not match tier_1 filings: it cites FY26 revenue "Rs 285 crore" and FY27 guidance "Rs 350-380 crore" (filed FY26 total revenue is Rs 838.0 cr; FY27 guidance is a growth %), a price of "Rs 1380" and P/E 42x (yfinance close was Rs 475.5 on 2026-06-28; P/E 41.2), "DSO 34 days (down from 42 in Q3)", and "Capex approved FY26-27 for 40% capacity increase" (no such statement found in any document in this batch). Treat those inputs as unverified until the impact note is re-run.

1. Valuation premium / margin of safety: Price trigger (a) "15% pullback" is met on the numbers (about -23% vs 2026-06-28 close; about -34% vs 52-week high; P/E down to ~27x, tier_3). Trigger (b) "visible FY27 revenue beat +5%" is not met (Q2 growth +3.4%, guidance 20-25% maintained, no beat). Status: price condition met; fundamental support weaker. Not a clean unlock.
2. Export order repeatability: The anchor order (UAE TA'ZIZ) was cancelled. Impact-note unlock required "2-3 follow-on orders with ADNOC or similar Gulf-region buyers in Q1-Q2 FY27": not met. Substitute: ~Rs 500 cr Nigeria heater order from promoter JNK Global (back-to-back, related-party, arm's length per filing), which is larger but different in kind (not an independent repeat customer); Kenya/Dangote scope uncertain ("We are not confirming definitely it will come or not"). Status: original blocker not cleared; thesis re-based onto a related-party channel.
3. Execution risk / capex / staffing ramp: Execution slippage is now evidenced (Q2 revenue +3.4%; "INR30 crores-INR40 crores" deferred by shipment delays and monsoon; Oct-Nov recovery "not so much"). Staffing ramp is on track (employee cost +46% YoY; "20 specialised executives" hired per Aug deck) but compresses margin. No capex delay announcement and no capacity-expansion figures were found. Status: open and worsened; kill-trigger "capex delay announcement" not triggered, but execution-slip trigger effectively met.
4. Working capital / cash conversion (impact note: "green light"): Not corroborated and indicators deteriorated: consolidated receivables +13% in six months, cash 6.9 vs 32.1, H1 operating cash flow 2.8 vs 10.3, trade payables -19%, borrowings up, finance cost +75% YoY in Q2; 35.5% of Mar-26 standalone receivables more than 1 year past due; management says "we might need a bank guarantee limit enhancement" (CRISIL raised LC/BG lines; outlook to Stable). Management says no funding plan needed. Status: open; leaning negative; verify receivable ageing at Sep-26 (not disclosed).
5. Order book growth (unlock: "2x order book growth QoQ"): Not met; order book fell 8.2% in Q1 and 7.7% in Q2. Pro forma for the Nigeria order the book is about Rs 2,160 cr (derived, indicative; not a company figure). Status: unmet; partial post-quarter rebuild.
6. Guidance: impact-note trigger "management guidance upgrade": no upgrade; instead lower than earlier-extracted guidance and internally inconsistent documents. Status: unmet.

## Key Signals Summary

1. **Revenue growth collapse to +3.4% YoY in Q2 with order book down two quarters** — Inflection down — Strength: High
   Evidence: "Total Operational Income 187.5 181.4 3.4%"; "our order book as on September 30, 2026 stands at Rs. 1,662 crores" (vs Rs 1,961.4 cr March)
2. **UAE export order cancelled; replaced by Rs ~500 cr related-party Nigeria order** — Mixed event delta — Strength: High
   Evidence: "informing that the aforesaid order stands cancelled" / "the largest export order on us till date" (via JNK Global)
3. **Guidance maintained at 20-25% / 12-14% but contradictory documents and an H2-heavy requirement** — Lowered vs prior extraction / Maintained QoQ — Strength: High
   Evidence: "continue to maintain our FY27 guidance of 20%-25% revenue growth and in EBITDA margin of 12%-14%"; Aug-14 deck: "14 -15% and revenue growth of 25-30%"
4. **Working capital strain and cash decline** — Inflection down — Strength: High
   Evidence: Cash & equivalents 6.9 vs 32.1 (Mar-26); H1 "Net Cash from Operating Activities 2.8" vs 10.3
5. **Green hydrogen/Chemdist timeline pushed out** — Weakening — Strength: Medium
   Evidence: "maybe about two years or so, to actually culminate into a larger amount of revenues"; Chemdist order book "about INR20 crores"
6. **Governance/disclosure noise: third CFO in under a year, standalone deck errors, order-range error, JNK Global activist dispute** — Strength: Medium
   Evidence: "Mr. Anand Agarwal ... has tendered his resignation"; "some kind of error in the standalone numbers"
7. **Credit outlook improved to Stable; new business lines and bid pipeline (Rs 5,000 cr; BPCL Vizag opportunity ~Rs 5,000 cr; NTPC bid due 20 Nov)** — Strengthening (positive offsets) — Strength: Medium
   Evidence: "Crisil A-/Stable (Outlook revised from 'Negative'; Rating Reaffirmed)"

## Flags

[x] Guidance revised (down vs earlier extraction: 25-30% / 14-15% to 20-25% / 12-14%; management denies a change; 2026-08-14 deck still shows old range; unresolved)
[x] Auditor / management change (CFO: Pravin Sathe resigned 16 Dec 2025; interim Anand Agarwal 12 Mar 2026 to 5 Nov 2026; Praveen Sood from 12 Nov 2026; statutory auditor P G Bhagwat LLP unchanged, no qualification; senior management personnel changes on 11 Aug)
[ ] Promoter pledge change (not covered by documents in this batch; shareholding pattern not collected)
[x] New related-party transactions mentioned (Nigeria order from promoter JNK Global, "within related party transactions ... at 'arm's length basis'"; AGM material RPT approval; Non-Executive Director consultancy fee item)
[x] Legal or regulatory mention new this quarter (licensor approval cause of order termination; activist MJ Partners vs JNK Global board "sub judice" as raised by an analyst, management declined comment; JNK Global cooperation agreement "not yet renewed" formally)
[x] Data-quality flags: EBITDA basis changed between Q1 (incl. OI) and Q2 (ex-OI); Q1 press release states Q1FY26 income as "Rs. 10.30 cr" vs table 103.0; original Q1 deck standalone P&L wrong (revised filed 12 Aug); decks show BSE code 544220 vs 544167; Q2 deck axis label "Nov-27*"; board-outcome financial tables are OCR text; Q4 FY26 call extraction was snippet-based
[x] Scanned/low-text documents: none (all manifest documents had >300 chars; shortest 1,397 chars)

## Recommended routing input (for investment-impact re-run; not a Buy/Sell view)
Re-run the impact note with corrected inputs. On the evidence here, signal strength of the June "export momentum" thesis has declined; blockers 2-5 remain open or worse, blocker 1 (price) has partially cleared. Watch list before next review: Dangote balance scope (2-3 months), Kenya refinery inquiries (Dec), NTPC bid (20 Nov), Q3 FY27 order book and receivables, whether H2 revenue tracks ~Rs 627-669 cr, clarification of guidance range, new CFO commentary.
