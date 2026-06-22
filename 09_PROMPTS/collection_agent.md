# Collection Agent

## Objective

Collect evidence, not just URLs.

For each tracked company, the Collection Agent must:

1. discover source items,
2. capture metadata,
3. attempt retrieval,
4. validate retrieved content,
5. save usable raw files or text snapshots,
6. index failures without stopping the run.

It must also run a broad discovery news lane under
`02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/` so the Universe Manager has fresh
signals for companies that are not already tracked.

Google News RSS is a signal detector, not proof. NSE/BSE are valuable evidence
sources, but the workflow must not depend on downloading NSE/BSE PDFs.

Do not summarize, analyse, or form opinions. Collection is deterministic and
non-AI.

---

## Source Retrieval Resilience Rule

All external sources are fallible:

- NSE / BSE
- company IR pages
- exchange archives
- PDFs and HTML pages
- RSS feeds
- news sites
- Screener, Moneycontrol, Business Standard, Economic Times, CNBC TV18
- any future external source

The workflow must never fail only because one source cannot be retrieved.

No individual website is mandatory. Every material signal should be discoverable
through multiple evidence paths.

For every discovered item:

1. save metadata,
2. attempt content download or text snapshot,
3. validate content before writing raw files,
4. save failure reason if retrieval fails,
5. continue to the next item.

---

## Collection Status Contract

Use exactly these statuses:

| Status | Meaning |
|---|---|
| `downloaded` | Raw file saved locally after content-type and file-signature validation |
| `text_snapshot` | Readable text saved locally when full raw download is unnecessary or unavailable |
| `metadata_only` | Metadata saved, but content unavailable |
| `failed` | Source was attempted, but the record is incomplete or unusable |

Never save an HTML error page as a PDF. Validate content type and file
signature before writing any raw file.

---

## Required Metadata

Every discovered source item must be written to `evidence-index.jsonl`, even
when retrieval fails:

```yaml
company:
ticker:
source_name:
source_type:
source_tier:
title:
published_date:
source_url:
discovered_at:
collection_status:
failure_reason:
alternate_sources_checked:
local_path:
content_hash:
```

`local_path` and `content_hash` are required only for `downloaded` and
`text_snapshot`.

---

## Storage Layout

```text
02_RAW_DOCUMENTS/<TICKER>/raw/YYYY-MM-DD/<safe-title>-<hash-prefix>.pdf
02_RAW_DOCUMENTS/<TICKER>/snapshots/YYYY-MM-DD/<safe-title>-<hash-prefix>.txt
02_RAW_DOCUMENTS/<TICKER>/evidence-index.jsonl
02_RAW_DOCUMENTS/<TICKER>/catalogue.md
```

Discovery-wide material remains under:

```text
02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/
02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/evidence-index.jsonl
02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/discovery-news.md
```

`evidence-index.jsonl` is the durable machine-readable audit trail.
`catalogue.md` is the human-readable view.

---

## Evidence Tiering

| Tier | Meaning | Handling |
|---|---|---|
| Tier 1 | Company IR pages, company press releases, annual reports, earnings calls, investor presentations, credit rating reports from CRISIL/ICRA/CARE/India Ratings | One Tier 1 source can confirm a material signal |
| Tier 2 | BSE/NSE filings or metadata, Business Standard, Moneycontrol, Economic Times, CNBC-TV18, NDTV Profit/BQ Prime | Two independent Tier 2 sources can confirm a material signal |
| Tier 3 | Google News RSS, aggregators, duplicate headlines, market commentary, social/unverified claims | Detection only unless corroborated |

---

## Discovery Lanes

| Lane | Role |
|---|---|
| Lane A | Tracked company evidence for `fetch_enabled=true` |
| Lane B | Broad news discovery; detects possible signals only |
| Lane C | Company website / IR discovery for high-signal names |
| Lane D | Corroboration search across company site, rating agencies, BSE/NSE metadata, and credible media |
| Lane E | Credit rating agency scan |

The scheduled script currently runs Lane A and Lane B and records
corroboration queries for Lane C/D/E follow-up.

---

## Signal Classification

| Classification | Rule |
|---|---|
| Confirmed | 1 Tier 1 source, or 2 independent Tier 2 sources |
| Watch | 1 Tier 2 source, repeated weak signals, or a material headline needing corroboration |
| Ignore | Duplicate aggregators, social/low-quality reposts, immaterial order size, unverifiable ticker/company |

---

## Rules

- Prefer company IR websites and NSE/BSE official filings over third-party sources.
- Do not summarize, extract, or analyse documents.
- Never let one bad source stop the run.
- Record `failure_reason` for 403, 404, 429, timeout, connection error,
  paywall, malformed response, unsupported file type, and validation failure.
- Reject fake PDFs such as HTML error pages with `.pdf` URLs.
- Preserve source URL and metadata even if the content is unavailable.
- Universe Manager decides what companies are tracked; Collection only gathers
  evidence for selected companies.
- Do not try to bypass NSE/BSE protections. Save the failure, try alternate
  evidence paths, and continue.
