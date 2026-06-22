#!/usr/bin/env python3
"""
Weekly evidence fetch - no AI, no API keys required.

Collects deterministic evidence for the Opportunity Discovery Engine:
- prices from yfinance
- company news from Google News RSS
- NSE/BSE filings
- local raw files or text snapshots where retrieval succeeds
- durable metadata records where retrieval fails

External sources are fallible. A single 403, timeout, paywall, malformed
response, or HTML error page must never fail the weekly collection run.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance not installed. Run: pip install yfinance requests")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install yfinance requests")
    sys.exit(1)


ROOT = Path(__file__).parent.parent
UNIVERSE_CSV = ROOT / "01_UNIVERSE" / "company_master.csv"
LEGACY_DATA_CSV = ROOT / "data" / "company_master.csv"
RAW_DIR = ROOT / "02_RAW_DOCUMENTS"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
DISCOVERY_DIR = RAW_DIR / "_discovery" / TODAY
NOW_ISO = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

COLLECTION_STATUSES = {"downloaded", "text_snapshot", "metadata_only", "failed"}
COLLECTOR_VERSION = "resilient-discovery-index-v3-corroboration"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/json,text/html,application/xhtml+xml,application/pdf,*/*",
    "Accept-Language": "en-IN,en;q=0.9",
    "Connection": "keep-alive",
}

NSE_BASE = "https://www.nseindia.com"
BSE_API = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"

DISCOVERY_QUERIES = [
    '"order win" NSE India stock',
    '"L1 bidder" India listed company',
    '"capacity expansion" India listed company',
    '"capex" "NSE" "exchange filing"',
    '"export order" India listed company',
    '"defence order" India listed company',
    '"green hydrogen" India listed company',
    '"railway order" India listed company',
    '"semiconductor" India listed company',
    '"PLI scheme" India listed company',
    '"new plant" India listed company',
    '"credit rating" India listed company',
]


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def retry_get(
    url: str,
    session: requests.Session,
    retries: int = 3,
    timeout: int = 20,
    **kwargs,
) -> requests.Response:
    delay = 2
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response
        except Exception as exc:
            if attempt == retries - 1:
                raise
            print(f"  Retry {attempt + 1}/{retries} for {url}: {exc}")
            time.sleep(delay)
            delay *= 2
    raise RuntimeError(f"unreachable retry state for {url}")


def prime_nse(session: requests.Session) -> None:
    """Hit NSE homepage to establish cookies before API/archive calls."""
    try:
        retry_get(NSE_BASE, session)
        time.sleep(1)
    except Exception as exc:
        print(f"  Warning: NSE prime failed: {exc}")


# ---------------------------------------------------------------------------
# File, metadata, and validation helpers
# ---------------------------------------------------------------------------


def safe_slug(value: str, fallback: str = "source") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())[:90].strip("-")
    return cleaned or fallback


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def rel_path(path: Path | None) -> str:
    if not path:
        return ""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_bool(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"true", "1", "yes", "y"}


def expected_is_pdf(source: dict) -> bool:
    url = (source.get("source_url") or source.get("url") or "").lower()
    title = (source.get("title") or "").lower()
    source_type = (source.get("source_type") or source.get("type") or "").lower()
    return url.endswith(".pdf") or ".pdf?" in url or "pdf" in source_type or "filing" in source_type or "annual report" in title


def looks_like_block_page(text: str) -> bool:
    lower = text.lower()
    block_markers = [
        "access denied",
        "forbidden",
        "cloudflare",
        "captcha",
        "enable javascript",
        "too many requests",
        "login",
        "sign in",
        "subscribe",
        "paywall",
    ]
    return any(marker in lower for marker in block_markers)


def html_to_text(content: bytes) -> str:
    text = content.decode("utf-8", errors="ignore")
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)<br\s*/?>", "\n", text)
    text = re.sub(r"(?is)</p\s*>", "\n", text)
    text = re.sub(r"(?is)<.*?>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def validate_response_content(response: requests.Response, source: dict) -> tuple[str | None, str | None]:
    content = response.content or b""
    if not content:
        return None, "Empty response body"

    content_type = (response.headers.get("content-type") or "").lower()
    wants_pdf = expected_is_pdf(source)

    if wants_pdf:
        if not content.startswith(b"%PDF"):
            snippet = html_to_text(content[:3000])
            if looks_like_block_page(snippet) or "<html" in content[:500].lower().decode("utf-8", errors="ignore"):
                return None, "Expected PDF but received HTML/block/error page"
            return None, "Expected PDF but file signature was not %PDF"
        return "pdf", None

    if content.startswith(b"%PDF"):
        return "pdf", None

    if "text/html" in content_type or content.lstrip().startswith((b"<html", b"<!DOCTYPE", b"<!doctype")):
        text = html_to_text(content)
        if not text:
            return None, "HTML response had no readable text"
        if looks_like_block_page(text):
            return None, "HTML response appears to be blocked, paywalled, or login-only"
        return "text", None

    if content_type.startswith("text/") or "json" in content_type:
        text = content.decode("utf-8", errors="ignore").strip()
        if not text:
            return None, "Text response had no readable content"
        return "text", None

    return None, f"Unsupported content type: {content_type or 'unknown'}"


def load_existing_index(out_dir: Path) -> tuple[list[dict], set[str], set[str]]:
    index_file = out_dir / "evidence-index.jsonl"
    records: list[dict] = []
    urls: set[str] = set()
    hashes: set[str] = set()
    if not index_file.exists():
        return records, urls, hashes

    for line in index_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        records.append(record)
        if record.get("source_url"):
            urls.add(record["source_url"])
        if record.get("content_hash"):
            hashes.add(record["content_hash"])
    return records, urls, hashes


def append_index_record(out_dir: Path, record: dict) -> None:
    status = record.get("collection_status")
    if status not in COLLECTION_STATUSES:
        raise ValueError(f"invalid collection_status: {status}")

    index_file = out_dir / "evidence-index.jsonl"
    index_file.parent.mkdir(parents=True, exist_ok=True)
    with index_file.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def base_record(row: dict, source: dict, status: str) -> dict:
    rec = {
        "company": row.get("company_name", ""),
        "ticker": row.get("ticker", ""),
        "source_name": source.get("source_name", source.get("source", "")),
        "source_type": source.get("source_type", source.get("type", "")),
        "source_tier": source.get("source_tier", infer_source_tier(source)),
        "title": source.get("title", ""),
        "published_date": source.get("published_date", source.get("date", "")),
        "source_url": source.get("source_url", source.get("url", "")),
        "discovered_at": NOW_ISO,
        "collection_status": status,
        "failure_reason": "",
        "alternate_sources_checked": source.get("alternate_sources_checked", []),
        "local_path": "",
        "content_hash": "",
        "extraction_status": "pending_extraction" if status in {"downloaded", "text_snapshot"} else "unavailable",
    }
    for discovery_field in ("discovery_action", "corroboration_status", "corroboration_queries"):
        if discovery_field in source:
            rec[discovery_field] = source[discovery_field]
    return rec


def infer_source_tier(source: dict) -> str:
    source_name = (source.get("source_name") or source.get("source") or "").lower()
    source_type = (source.get("source_type") or source.get("type") or "").lower()
    if source_name in {"nse", "bse"} or "filing" in source_type or "annual report" in source_type:
        return "tier_1"
    if "news" in source_type or "rss" in source_type:
        return "tier_3"
    return "tier_3"


def save_source_content(out_dir: Path, source: dict, response: requests.Response, content_kind: str) -> tuple[str, str]:
    content = response.content or b""
    digest = sha256_bytes(content)
    title_slug = safe_slug(source.get("title", "source"))

    if content_kind == "pdf":
        target_dir = out_dir / "raw" / TODAY
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{title_slug}-{digest[:10]}.pdf"
        path.write_bytes(content)
        return rel_path(path), digest

    text = html_to_text(content) if content.lstrip().startswith((b"<", b"<!")) or b"<html" in content[:500].lower() else content.decode("utf-8", errors="ignore").strip()
    text_bytes = text.encode("utf-8")
    text_digest = sha256_bytes(text_bytes)
    target_dir = out_dir / "snapshots" / TODAY
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{title_slug}-{text_digest[:10]}.txt"
    path.write_text(text, encoding="utf-8")
    return rel_path(path), text_digest


def collect_source_item(
    row: dict,
    out_dir: Path,
    source: dict,
    session: requests.Session,
    known_urls: set[str],
    known_hashes: set[str],
    allow_snapshot: bool = True,
) -> dict | None:
    source_url = source.get("source_url") or source.get("url") or ""
    if not source_url:
        record = base_record(row, source, "failed")
        record["failure_reason"] = "Missing source URL"
        append_index_record(out_dir, record)
        return record

    if source_url in known_urls:
        return None

    record = base_record(row, source, "metadata_only")

    try:
        response = retry_get(source_url, session)
        content_kind, failure_reason = validate_response_content(response, source)
        if not content_kind:
            record["collection_status"] = "metadata_only"
            record["failure_reason"] = failure_reason or "Content validation failed"
            append_index_record(out_dir, record)
            known_urls.add(source_url)
            return record

        if content_kind == "text" and not allow_snapshot:
            record["collection_status"] = "metadata_only"
            record["failure_reason"] = "Text snapshot disabled for this source"
            append_index_record(out_dir, record)
            known_urls.add(source_url)
            return record

        local_path, digest = save_source_content(out_dir, source, response, content_kind)
        if digest in known_hashes:
            record["collection_status"] = "metadata_only"
            record["failure_reason"] = "Duplicate content hash already collected"
        else:
            record["collection_status"] = "downloaded" if content_kind == "pdf" else "text_snapshot"
            record["local_path"] = local_path
            record["content_hash"] = digest
            record["extraction_status"] = "pending_extraction"
            known_hashes.add(digest)
        append_index_record(out_dir, record)
        known_urls.add(source_url)
        return record
    except requests.HTTPError as exc:
        status_code = getattr(exc.response, "status_code", "unknown")
        record["collection_status"] = "metadata_only"
        record["failure_reason"] = f"HTTP {status_code} from source URL"
    except requests.Timeout:
        record["collection_status"] = "metadata_only"
        record["failure_reason"] = "Timeout"
    except requests.RequestException as exc:
        record["collection_status"] = "metadata_only"
        record["failure_reason"] = f"Connection error: {exc}"
    except Exception as exc:
        record["collection_status"] = "failed"
        record["failure_reason"] = f"Unhandled retrieval error: {exc}"

    append_index_record(out_dir, record)
    known_urls.add(source_url)
    return record


# ---------------------------------------------------------------------------
# Price fetch
# ---------------------------------------------------------------------------


def fetch_prices(row: dict, out_dir: Path) -> bool:
    yf_symbol = row.get("yfinance_symbol") or f"{row['ticker']}.NS"
    ticker_obj = yf.Ticker(yf_symbol)
    try:
        info = ticker_obj.info
        hist = ticker_obj.history(period="2d")
        if hist.empty:
            print(f"  [{row['ticker']}] No price history from yfinance")
            return False

        latest = hist.iloc[-1]
        data = {
            "ticker": row["ticker"],
            "company_name": row["company_name"],
            "as_of": TODAY,
            "currency": info.get("currency", "INR"),
            "latest_close": round(float(latest["Close"]), 2),
            "latest_open": round(float(latest["Open"]), 2),
            "latest_high": round(float(latest["High"]), 2),
            "latest_low": round(float(latest["Low"]), 2),
            "volume": int(latest["Volume"]),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "source": f"yfinance:{yf_symbol}",
        }

        out_file = out_dir / f"prices-{TODAY}.json"
        out_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"  [{row['ticker']}] Price: {data['latest_close']} -> {out_file.name}")
        return True
    except Exception as exc:
        print(f"  [{row['ticker']}] Price fetch failed: {exc}")
        return False


# ---------------------------------------------------------------------------
# News fetch (Google News RSS)
# ---------------------------------------------------------------------------


def fetch_news(row: dict, out_dir: Path, session: requests.Session, known_urls: set[str], known_hashes: set[str]) -> bool:
    query = f"{row['company_name']} {row['ticker']} NSE"
    rss_url = (
        f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}"
        f"&hl=en-IN&gl=IN&ceid=IN:en"
    )

    try:
        response = retry_get(rss_url, session)
        root = ET.fromstring(response.content)
        items = root.findall(".//item")[:15]

        rows = []
        saved_count = 0
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        for item in items:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub_str = (item.findtext("pubDate") or "").strip()
            source_el = item.find("source")
            source_name = source_el.text if source_el is not None and source_el.text else "Google News"

            try:
                pub_dt = datetime.strptime(pub_str, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
                if pub_dt < cutoff:
                    continue
                pub_date = pub_dt.strftime("%Y-%m-%d")
            except Exception:
                pub_date = TODAY

            rows.append(f"| {source_name} | {title} | {pub_date} | {link} |")

            news_source = {
                "source_name": source_name,
                "source_type": "News RSS",
                "source_tier": "tier_3",
                "title": title,
                "published_date": pub_date,
                "source_url": link,
            }
            record = collect_source_item(row, out_dir, news_source, session, known_urls, known_hashes, allow_snapshot=True)
            if record and record["collection_status"] in {"text_snapshot", "metadata_only"}:
                saved_count += 1

        if not rows:
            print(f"  [{row['ticker']}] No recent news items found")
            return False

        lines = [
            f"# News - {row['company_name']} ({row['ticker']})",
            f"Fetched: {TODAY}",
            "",
            "| Source | Headline | Date | URL |",
            "|---|---|---|---|",
        ] + rows

        out_file = out_dir / f"news-{TODAY}.md"
        out_file.write_text("\n".join(lines), encoding="utf-8")
        print(f"  [{row['ticker']}] News: {len(rows)} items, {saved_count} indexed -> {out_file.name}")
        return True
    except Exception as exc:
        print(f"  [{row['ticker']}] News fetch failed: {exc}")
        return False


# ---------------------------------------------------------------------------
# Discovery news fetch
# ---------------------------------------------------------------------------


def fetch_discovery_news(session: requests.Session) -> bool:
    """Collect broad market discovery news independent of fetch_enabled companies."""
    DISCOVERY_DIR.mkdir(parents=True, exist_ok=True)
    _, known_urls, known_hashes = load_existing_index(DISCOVERY_DIR)
    discovery_row = {
        "ticker": "_DISCOVERY",
        "company_name": "Market Discovery",
    }

    cutoff = datetime.now(timezone.utc) - timedelta(days=14)
    markdown_rows = []
    indexed_count = 0
    failed_queries = 0

    print("\n--- Discovery News: broad market scan ---")
    for query in DISCOVERY_QUERIES:
        rss_url = (
            f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}"
            f"&hl=en-IN&gl=IN&ceid=IN:en"
        )
        try:
            response = retry_get(rss_url, session)
            root = ET.fromstring(response.content)
            items = root.findall(".//item")[:10]
        except Exception as exc:
            failed_queries += 1
            print(f"  [DISCOVERY] Query failed: {query} ({exc})")
            continue

        for item in items:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub_str = (item.findtext("pubDate") or "").strip()
            source_el = item.find("source")
            source_name = source_el.text if source_el is not None and source_el.text else "Google News"

            try:
                pub_dt = datetime.strptime(pub_str, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
                if pub_dt < cutoff:
                    continue
                pub_date = pub_dt.strftime("%Y-%m-%d")
            except Exception:
                pub_date = TODAY

            markdown_rows.append(f"| {query} | {source_name} | {title} | {pub_date} | {link} |")
            source = {
                "source_name": source_name,
                "source_type": "Discovery News",
                "source_tier": "tier_3",
                "title": title,
                "published_date": pub_date,
                "source_url": link,
                "discovery_action": "pending_review",
                "corroboration_status": "needs_corroboration",
                "corroboration_queries": [],
            }
            record = collect_source_item(
                discovery_row,
                DISCOVERY_DIR,
                source,
                session,
                known_urls,
                known_hashes,
                allow_snapshot=True,
            )
            if record and record["collection_status"] in COLLECTION_STATUSES:
                indexed_count += 1

    if markdown_rows:
        lines = [
            "# Discovery News",
            f"Fetched: {TODAY}",
            "",
            "| Query | Source | Headline | Date | URL |",
            "|---|---|---|---|---|",
        ] + markdown_rows
        out_file = DISCOVERY_DIR / "discovery-news.md"
        out_file.write_text("\n".join(lines), encoding="utf-8")
        print(f"  [DISCOVERY] News: {len(markdown_rows)} items, {indexed_count} indexed -> {rel_path(out_file)}")
        if failed_queries:
            print(f"  [DISCOVERY] Query failures: {failed_queries} (workflow continued)")
        return True

    print("  [DISCOVERY] No recent discovery news items found")
    if failed_queries:
        print(f"  [DISCOVERY] Query failures: {failed_queries}")
    return False


# ---------------------------------------------------------------------------
# Exchange filings
# ---------------------------------------------------------------------------


def _parse_date(raw: str) -> str:
    for fmt in ("%d-%b-%Y %H:%M:%S", "%Y%m%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw[:10] if len(raw) >= 10 else raw


def fetch_nse_filings(row: dict, session: requests.Session) -> list[dict]:
    symbol = row.get("nse_symbol") or row["ticker"]
    url = f"{NSE_BASE}/api/corporate-announcements?index=equities&symbol={symbol}"
    try:
        response = retry_get(url, session)
        data = response.json()
        if not isinstance(data, list):
            return []

        cutoff = (datetime.now(timezone.utc) - timedelta(days=60)).strftime("%Y-%m-%d")
        filings = []
        for item in data:
            desc = item.get("desc", "") or item.get("subject", "")
            date_raw = item.get("date", "") or item.get("an_dt", "")
            date = _parse_date(str(date_raw)) if date_raw else TODAY
            if date < cutoff:
                continue
            attach = item.get("attchmntFile", "") or item.get("nsurl", "")
            url_str = f"https://nsearchives.nseindia.com/{attach}" if attach and not attach.startswith("http") else attach
            filings.append({
                "published_date": date,
                "date": date,
                "source_name": "NSE",
                "source": "NSE",
                "source_type": "Exchange Filing",
                "type": item.get("cmpyname", "Exchange Filing"),
                "source_tier": "tier_1",
                "title": desc[:200],
                "source_url": url_str,
                "url": url_str,
            })
        return filings
    except Exception as exc:
        print(f"  [{row['ticker']}] NSE filings failed: {exc}")
        return []


def fetch_bse_filings(row: dict, session: requests.Session) -> list[dict]:
    bse_code = row.get("bse_code", "")
    if not bse_code:
        return []
    params = {
        "strCat": "-1",
        "strPrevDate": (datetime.now(timezone.utc) - timedelta(days=60)).strftime("%Y%m%d"),
        "strScrip": bse_code,
        "strSearch": "P",
        "strToDate": datetime.now(timezone.utc).strftime("%Y%m%d"),
        "strType": "C",
    }
    try:
        session.get(BSE_API, timeout=15)
        response = session.post(BSE_API, data=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        filings = []
        for item in (data.get("Table", []) or []):
            date_raw = item.get("NewsDate", "") or item.get("DissemDT", "")
            date = _parse_date(str(date_raw)) if date_raw else TODAY
            title = item.get("NEWSSUB", "") or item.get("HEADLINE", "")
            link = item.get("ATTACHMENTNAME", "") or ""
            url_str = f"https://www.bseindia.com/xml-data/corpfiling/AttachHis/{link}" if link else ""
            filings.append({
                "published_date": date,
                "date": date,
                "source_name": "BSE",
                "source": "BSE",
                "source_type": "Exchange Filing",
                "type": "BSE Filing",
                "source_tier": "tier_1",
                "title": title[:200],
                "source_url": url_str,
                "url": url_str,
            })
        return filings
    except Exception as exc:
        print(f"  [{row['ticker']}] BSE filings failed: {exc}")
        return []


def collect_filings(
    row: dict,
    out_dir: Path,
    filings: Iterable[dict],
    session: requests.Session,
    known_urls: set[str],
    known_hashes: set[str],
) -> list[dict]:
    records = []
    for filing in filings:
        record = collect_source_item(row, out_dir, filing, session, known_urls, known_hashes, allow_snapshot=False)
        if record:
            records.append(record)
    return records


def attach_alternate_sources(filings: list[dict]) -> list[dict]:
    """Record same-title NSE/BSE alternates when both exchanges surface a filing."""
    by_title: dict[str, list[dict]] = {}
    for filing in filings:
        key = safe_slug(filing.get("title", "").lower())[:60]
        if not key:
            continue
        by_title.setdefault(key, []).append(filing)

    for filing in filings:
        key = safe_slug(filing.get("title", "").lower())[:60]
        alternates = []
        for other in by_title.get(key, []):
            if other is filing:
                continue
            other_url = other.get("source_url") or other.get("url")
            if other_url:
                alternates.append({
                    "source_name": other.get("source_name", other.get("source", "")),
                    "source_url": other_url,
                })
        filing["alternate_sources_checked"] = alternates
    return filings


# ---------------------------------------------------------------------------
# Catalogue update
# ---------------------------------------------------------------------------


CATALOGUE_HEADER = "| Date | Source | Type | Title | Source URL | Local Path | Hash | Collection Status |"
CATALOGUE_SEP = "|---|---|---|---|---|---|---|---|"


def update_catalogue(row: dict, out_dir: Path, records: list[dict]) -> None:
    if not records:
        return

    cat_file = out_dir / "catalogue.md"
    existing = cat_file.read_text(encoding="utf-8") if cat_file.exists() else ""

    known_urls = set()
    for line in existing.splitlines():
        if line.startswith("|") and "http" in line:
            parts = [part.strip() for part in line.split("|")]
            for part in parts:
                if part.startswith("http"):
                    known_urls.add(part)

    new_rows = []
    for record in records:
        url = record.get("source_url", "")
        if url and url in known_urls:
            continue
        new_rows.append(
            "| {date} | {source} | {type} | {title} | {url} | {local_path} | {hash} | {status} |".format(
                date=record.get("published_date", ""),
                source=record.get("source_name", ""),
                type=record.get("source_type", ""),
                title=(record.get("title", "") or "").replace("|", "/"),
                url=url,
                local_path=record.get("local_path", ""),
                hash=(record.get("content_hash", "") or "")[:12],
                status=record.get("collection_status", ""),
            )
        )
        if url:
            known_urls.add(url)

    if not new_rows:
        return

    section = (
        f"\n\n## Evidence collected {TODAY}\n\n"
        f"{CATALOGUE_HEADER}\n{CATALOGUE_SEP}\n"
        + "\n".join(new_rows)
        + "\n"
    )
    cat_file.write_text(existing.rstrip() + section, encoding="utf-8")
    print(f"  [{row['ticker']}] Catalogue: {len(new_rows)} evidence record(s) added")


# ---------------------------------------------------------------------------
# Retention cleanup
# ---------------------------------------------------------------------------


def cleanup_raw_evidence(out_dir: Path, retention_days: int = 30) -> int:
    index_file = out_dir / "evidence-index.jsonl"
    if not index_file.exists():
        return 0

    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    deleted = 0
    for line in index_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        status = record.get("collection_status")
        extraction_status = record.get("extraction_status")
        local_path = record.get("local_path")
        content_hash = record.get("content_hash")
        source_url = record.get("source_url")
        if status not in {"downloaded", "text_snapshot"}:
            continue
        if extraction_status != "extracted":
            continue
        if not (local_path and content_hash and source_url):
            continue
        full_path = ROOT / local_path
        if not full_path.exists():
            continue
        modified = datetime.fromtimestamp(full_path.stat().st_mtime, tz=timezone.utc)
        if modified > cutoff:
            continue
        try:
            full_path.unlink()
            deleted += 1
        except OSError as exc:
            print(f"  Warning: cleanup failed for {local_path}: {exc}")
    return deleted


# ---------------------------------------------------------------------------
# Company loading
# ---------------------------------------------------------------------------


def normalize_company_row(row: dict) -> dict:
    ticker = row.get("ticker", "").strip()
    return {
        **row,
        "ticker": ticker,
        "company_name": row.get("company_name", ticker).strip(),
        "nse_symbol": (row.get("nse_symbol") or ticker).strip(),
        "yfinance_symbol": (row.get("yfinance_symbol") or f"{ticker}.NS").strip(),
        "bse_code": (row.get("bse_code") or "").strip(),
    }


def load_companies() -> list[dict]:
    if UNIVERSE_CSV.exists():
        with UNIVERSE_CSV.open(newline="", encoding="utf-8") as handle:
            rows = [normalize_company_row(row) for row in csv.DictReader(handle)]
        if rows and "fetch_enabled" in rows[0]:
            companies = [row for row in rows if parse_bool(row.get("fetch_enabled"))]
            print(f"Universe source: {rel_path(UNIVERSE_CSV)} (fetch_enabled=true)")
            return companies
        if rows and "active_universe" in rows[0]:
            companies = [row for row in rows if parse_bool(row.get("active_universe"))]
            print(f"Universe source: {rel_path(UNIVERSE_CSV)} (active_universe=true fallback)")
            return companies
        print(f"Universe source: {rel_path(UNIVERSE_CSV)} (schema lacks fetch flags; using first 25 rows as transition fallback)")
        return rows[:25]

    if LEGACY_DATA_CSV.exists():
        print(f"WARNING: canonical universe missing; falling back to legacy {rel_path(LEGACY_DATA_CSV)}")
        with LEGACY_DATA_CSV.open(newline="", encoding="utf-8") as handle:
            return [normalize_company_row(row) for row in csv.DictReader(handle) if parse_bool(row.get("active"))]

    raise FileNotFoundError("No company master found at 01_UNIVERSE/company_master.csv")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print(f"=== Weekly Evidence Fetch - {TODAY} ===\n")
    print(f"Collector version: {COLLECTOR_VERSION}\n")
    companies = load_companies()
    print(f"Companies selected for fetch: {len(companies)}\n")
    if not companies:
        print("No companies selected for Lane A. Discovery Lane B will still run.")

    session = make_session()
    print("Priming NSE session...")
    prime_nse(session)

    successes, failures = 0, 0

    for row in companies:
        ticker = row["ticker"]
        out_dir = RAW_DIR / ticker
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n--- {ticker}: {row['company_name']} ---")

        _, known_urls, known_hashes = load_existing_index(out_dir)

        ok_price = fetch_prices(row, out_dir)
        ok_news = fetch_news(row, out_dir, session, known_urls, known_hashes)
        time.sleep(1)

        nse_filings = fetch_nse_filings(row, session)
        time.sleep(1)
        bse_filings = fetch_bse_filings(row, session)
        time.sleep(1)

        filings = attach_alternate_sources(nse_filings + bse_filings)
        if filings:
            print(f"  [{ticker}] Filings discovered: {len(filings)}")
        else:
            print(f"  [{ticker}] Filings: none retrieved from APIs")

        filing_records = collect_filings(row, out_dir, filings, session, known_urls, known_hashes)
        downloaded_or_indexed = [r for r in filing_records if r and r.get("collection_status") in COLLECTION_STATUSES]
        update_catalogue(row, out_dir, downloaded_or_indexed)

        deleted = cleanup_raw_evidence(out_dir)
        if deleted:
            print(f"  [{ticker}] Retention cleanup: deleted {deleted} old raw file(s)")

        if ok_price or ok_news or downloaded_or_indexed:
            successes += 1
        else:
            failures += 1
            print(f"  [{ticker}] WARNING: no data fetched or indexed")

    discovery_ok = fetch_discovery_news(session)

    print(f"\n=== Done - Lane A: {successes} succeeded, {failures} failed; Lane B discovery: {'ok' if discovery_ok else 'no items'} ===")
    if companies and failures == len(companies) and not discovery_ok:
        sys.exit(1)
    if not companies and not discovery_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
