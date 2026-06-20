---
name: collection-agent
description: >
  Collection Agent for the Opportunity Discovery Engine. Trigger when the user wants to
  find and catalogue source documents for companies in the universe — IR websites, NSE/BSE
  filings, earnings transcripts, investor presentations, annual reports, press releases.
  Reads from 01_UNIVERSE/company_master.csv and writes document catalogues to
  02_RAW_DOCUMENTS/. Run after universe-manager, before extraction-agent. Trigger on:
  "run collection", "find documents", "collect filings", "catalogue documents",
  "find earnings calls", "collect for [company name]".
---

# Collection Agent

## Objective

For each company in the universe, locate and catalogue the latest source documents. Record where they are — do not download, summarise, or analyse them.

---

## Inputs

| Input | Location |
|---|---|
| Companies to collect for | `01_UNIVERSE/company_master.csv` |
| Existing catalogue (to avoid re-collecting) | `02_RAW_DOCUMENTS/<TICKER>/catalogue.md` (if exists) |

Default: collect for all companies in `company_master.csv` where the latest document is more than 7 days old or no catalogue exists.

User can also specify a single company: "collect for Siemens" → collect only for `SIEMENS`.

---

## Process

**Step 1** — Load `company_master.csv`. Filter to companies needing collection (no recent catalogue or explicitly requested).

**Step 2** — For each company, locate:
1. Investor Relations (IR) website — search `[company name] investor relations site`
2. NSE filing page — `https://www.nseindia.com/companies-listing/corporate-filings-financial-results`
3. BSE filing page — `https://www.bseindia.com/corporates/ann.html`

**Step 3** — Identify the latest version of each document type:
- Latest Annual Report (PDF)
- Latest Investor Presentation (PDF or slides)
- Latest Earnings Call Transcript (PDF or text)
- Latest Quarterly Result Filing (NSE/BSE)
- Latest Press Release (if any in last 30 days)

**Step 4** — For each document found, record:
- Document type
- Publication date
- Quarter (e.g. Q4 FY25)
- Source URL
- Whether it is new since last collection run

**Step 5** — Write catalogue to `02_RAW_DOCUMENTS/<TICKER>/catalogue.md`.

---

## Output Format

`02_RAW_DOCUMENTS/<TICKER>/catalogue.md`:

```markdown
# Document Catalogue — [COMPANY NAME] ([TICKER])
Last updated: YYYY-MM-DD

| Document Type | Date | Quarter | Source URL | New This Run |
|---|---|---|---|---|
| Earnings Call Transcript | YYYY-MM-DD | Q4 FY25 | [URL] | Yes/No |
| Investor Presentation | YYYY-MM-DD | Q4 FY25 | [URL] | Yes/No |
| Annual Report | YYYY-MM-DD | FY25 | [URL] | Yes/No |
| Quarterly Filing (NSE) | YYYY-MM-DD | Q4 FY25 | [URL] | Yes/No |
| Press Release | YYYY-MM-DD | — | [URL] | Yes/No |

## IR Website
[URL]

## NSE Filing Page
[URL]

## Notes
[Any access issues, missing documents, or unusual findings]
```

---

## Rules

- Prefer company IR websites and NSE/BSE official filings over third-party sources.
- Do not summarise, extract, or analyse documents — cataloguing only.
- If a document URL requires login or payment, note it and skip.
- Flag if a company has no earnings call transcript available (common for smaller companies).
- Mark each document as `New This Run: Yes` only if it was published since the last collection date.
- If a company has no public IR presence, log it and escalate to user.
