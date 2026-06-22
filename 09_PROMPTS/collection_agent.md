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
| Tier 1 | Filings, company disclosures, annual reports, earnings calls, investor presentations, press releases, credit reports, high-quality industry reports | Prioritize download; if blocked, attempt corroboration |
| Tier 2 | News articles, discovery news, sector updates, order-win/capex/tender coverage | Save text snapshot or metadata; corroborate if signal is material |
| Tier 3 | Aggregator headlines, duplicate reposts, social chatter, unverified claims | Metadata-only is acceptable unless corroborated |

---

## Rules

- Prefer company IR websites and NSE/BSE official filings over third-party sources.
- Do not summarize, extract, or analyse documents.
- Never let one bad source stop the run.
- Record `failure_reason` for 403, 404, 429, timeout, connection error,
  paywall, malformed response
