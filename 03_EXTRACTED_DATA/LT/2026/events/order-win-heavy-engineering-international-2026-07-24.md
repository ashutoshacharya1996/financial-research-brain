# Extracted Data — LARSEN & TOUBRO LTD (LT)
Document type: Press Release / Exchange Filing (Bagging/Receiving of orders/contracts)
Source: https://nsearchives.nseindia.com/corporate/PAM_24072026092018_PressRelease24072026.pdf
Local evidence: 02_RAW_DOCUMENTS/LT/raw/2026-07-26/Bagging-Receiving-of-orders-contracts-423f892721.pdf
Content hash: 423f892721bbb7b27e7142120588d36ed4bf69ad3e4173a04870017e1379cf58
Collection status: downloaded (file corrupted — see Collection failure reason)
Source tier: tier_1
Collection failure reason: Local PDF is truncated. The file's own /Linearized dictionary declares total expected length /L 3333353 bytes, but the file on disk is only 1,933,312 bytes (~58% of expected size) — the download was cut off before the file completed. Standard PDF readers (pypdf, pdfplumber/pdfminer, pikepdf, qpdf, Ghostscript) all fail to open/parse the file due to a missing xref/trailer and an incomplete final object. Manual recovery (regex scan for stream/endstream blocks + raw zlib inflation of each recovered stream) salvaged only the covering letter (page 1 of what is normally a multi-page release, per the sibling filing in this same batch) — the covering letter's subject line and signature block. The actual press release body (order value, client, geography detail, management quotes) sits later in the file, beyond the truncation point, and is not recoverable from this local copy.
Date: 2026-07-24
Quarter: Q2 FY27
Extracted by: Extraction Agent
Extraction date: 2026-07-27

---

## Financial Metrics

| Metric | Value | Period | vs Prior Period | Source Quote |
|--------|-------|--------|----------------|--------------|
| Revenue | | | | |
| EBITDA margin | | | | |
| PAT | | | | |
| Order book | | | | |
| Order inflows | Not recoverable — only order classification tier name "Large" survived in the truncated file; no rupee figure recovered | | | "L&T Heavy Engineering Wins Orders (Large*) in International Markets" |
| Capex | | | | |

## Guidance

Not applicable — not recoverable from the truncated file in any case (covering-letter subject line only).

## Management Commentary — Demand

Not recoverable. Only the covering letter to BSE/NSE survived; it contains no management quotes (those are addressed on the press-release body page, which is missing from this local copy).

## Management Commentary — Margins

Not recoverable.

## Management Commentary — Capacity / Expansion

Not recoverable.

## What Was Recovered (Covering Letter Only)

From the intimation letter to BSE Limited and National Stock Exchange of India Limited (dated July 24, 2026, signed by Subramanian Narayan, Company Secretary & Compliance Officer):

"Re : L&T Heavy Engineering Wins Orders (Large*) in International Markets"

"We enclose herewith a copy of Press Release that is being issued by the Company today, in connection with the above. We request you to take note of the same."

This establishes:
- Business unit: L&T Heavy Engineering
- Geography: "International Markets" (no specific country stated in the recovered text)
- Order classification tier: "Large" (asterisked — the classification table itself is on the missing press-release page and was not recovered from this document). For reference only, the sibling filing in this batch (content hash 6be982e4e4..., dated 2026-07-20) discloses L&T's classification bands as: Significant ₹1,000–2,500 Cr / Large ₹2,500–5,000 Cr / Major ₹5,000–10,000 Cr / Mega ₹10,000–15,000 Cr / Ultra-Mega >₹15,000 Cr. This band is NOT confirmed within this document itself and should be treated as contextual reference, not as an extracted fact of this filing.

## Named Catalysts

- L&T Heavy Engineering order win in international markets, classified "Large" per the filing's own subject line — specific client, country, and scope could not be recovered from the corrupted local file

## Named Risks

Not recoverable.

## Theme Signal Log

| Theme Category | Exact Quote | Context (bullish/cautious/neutral) |
|---|---|---|
| Export / global markets | "L&T Heavy Engineering Wins Orders (Large*) in International Markets" | Bullish — international order win for the Heavy Engineering business unit; magnitude and client unknown due to file corruption, so strength of signal cannot be fully assessed |

## Missing Data

- **Root cause: local PDF file is truncated/corrupted (see Collection failure reason above) — recollection from source is recommended.**
- Order value (exact ₹ figure)
- Client name and country/region within "International Markets"
- Scope of work / product-service description
- Management commentary and quotes
- Any financial metrics, guidance, catalysts, or risks normally found in the press-release body
