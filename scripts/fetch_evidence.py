#!/usr/bin/env python3
"""
Weekly evidence fetch — no AI, no API keys required.

Lane A: Company Evidence Fetch
  Reads 01_UNIVERSE/company_master.csv where fetch_enabled=true.
  Fetches prices (yfinance), company news (Google News RSS), and exchange
  filings (NSE/BSE) for each tracked company.
  Output: 02_RAW_DOCUMENTS/<TICKER>/

Lane B: Discovery News Fetch
  Runs broad market/theme queries — not tied to any company list.
  Output: 02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/discovery-news.md
  This lane does NOT add companies to the universe. Discovery News Agent
  reviews the output; Universe Manager makes the addition decision.
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

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
RAW_DIR = ROOT / "02_RAW_DOCUMENTS"
DISCOVERY_DIR = RAW_DIR / "_discovery"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/html,application/xhtml+xml,*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

NSE_BASE = "https://www.nseindia.com"
BSE_API = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"

# Broad discovery queries for Lane B.
# These are market-wide signals — not company-specific.
# Source: Google News RSS, filtered to India business news.
DISCOVERY_QUERIES = [
    "India order win NSE stock",
    "India contract awarded defence",
    "India L1 bidder government",
    "India letter of award infrastructure",
    "India capacity expansion plant",
    "India capex announcement manufacturing",
    "India PLI approval production",
    "India export order industrial",
    "India joint venture technology",
    "India defence acquisition procurement",
    "India tender awarded railways",
    "India guidance raised earnings",
    "India commissioning commercial production",
    "India semiconductor plant electronics",
    "India data center order",
    "India green hydrogen order SECI",
    "India power transmission order PGCIL",
    "India railway order RVNL IRCON",
    "India promoter pledge SEBI order",
    "India credit rating downgrade CRISIL ICRA",
]


# ---------------------------------------------------------------------------
# Guardrail check
# ---------------------------------------------------------------------------

def check_legacy_csv():
    legacy = ROOT / "data" / "company_master.csv"
    if legacy.exists():
        print("=" * 70)
        print("FATAL: data/company_master.csv still exists.")
        print("This file is no longer the source of truth.")
        print("The canonical universe is: 01_UNIVERSE/company_master.csv")
        print("Delete data/company_master.csv before running this script.")
        print("=" * 70)
        sys.exit(1)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def retry_get(url: str, session: requests.Session, retries: int = 3, timeout: int = 15):
    delay = 2
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=timeout)
            r.raise_for_status()
            return r
        except Exception as e:
            if attempt == retries - 1:
                raise
            print(f"  Retry {attempt + 1}/{retries} for {url}: {e}")
            time.sleep(delay)
            delay *= 2
    return None


def prime_nse(session: requests.Session):
    try:
        retry_get(NSE_BASE, session)
        time.sleep(1)
    except Exception as e:
        print(f"  Warning: NSE prime failed: {e}")


# ---------------------------------------------------------------------------
# Lane A — Price fetch
# ---------------------------------------------------------------------------

def fetch_prices(row: dict, out_dir: Path):
    yf_symbol = row["yfinance_symbol"]
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
        out_file.write_text(json.dumps(data, indent=2))
        print(f"  [{row['ticker']}] Price: ₹{data['latest_close']} → {out_file.name}")
        return True
    except Exception as e:
        print(f"  [{row['ticker']}] Price fetch failed: {e}")
        return False


# ---------------------------------------------------------------------------
# Lane A — Company news fetch (Google News RSS)
# ---------------------------------------------------------------------------

def _parse_rss_items(content: bytes, cutoff: datetime) -> list:
    root = ET.fromstring(content)
    rows = []
    for item in root.findall(".//item")[:15]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_str = (item.findtext("pubDate") or "").strip()
        source_el = item.find("{http://search.yahoo.com/mrss/}credit")
        source = source_el.text if source_el is not None else "Google News"
        try:
            pub_dt = datetime.strptime(pub_str, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
            if pub_dt < cutoff:
                continue
            pub_date = pub_dt.strftime("%Y-%m-%d")
        except Exception:
            pub_date = TODAY
        rows.append((source, title, pub_date, link))
    return rows


def fetch_news(row: dict, out_dir: Path, session: requests.Session):
    query = f"{row['company_name']} {row['ticker']} NSE"
    rss_url = (
        f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}"
        f"&hl=en-IN&gl=IN&ceid=IN:en"
    )
    try:
        r = retry_get(rss_url, session)
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        items = _parse_rss_items(r.content, cutoff)

        if not items:
            print(f"  [{row['ticker']}] No recent news items found")
            return False

        lines = [
            f"# News — {row['company_name']} ({row['ticker']})",
            f"Fetched: {TODAY}",
            "",
            "| Source | Headline | Date | URL |",
            "|---|---|---|---|",
        ] + [f"| {s} | {t} | {d} | {l} |" for s, t, d, l in items]

        out_file = out_dir / f"news-{TODAY}.md"
        out_file.write_text("\n".join(lines))
        print(f"  [{row['ticker']}] News: {len(items)} items → {out_file.name}")
        return True
    except Exception as e:
        print(f"  [{row['ticker']}] News fetch failed: {e}")
        return False


# ---------------------------------------------------------------------------
# Lane A — Exchange filings
# ---------------------------------------------------------------------------

def _parse_date(raw: str) -> str:
    for fmt in ("%d-%b-%Y %H:%M:%S", "%Y%m%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw[:10] if len(raw) >= 10 else raw


def fetch_nse_filings(row: dict, session: requests.Session) -> list:
    symbol = row["nse_symbol"]
    url = f"{NSE_BASE}/api/corporate-announcements?index=equities&symbol={symbol}"
    try:
        r = retry_get(url, session)
        data = r.json()
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
            url_str = (
                f"https://nsearchives.nseindia.com/{attach}"
                if attach and not attach.startswith("http")
                else attach
            )
            filings.append({"date": date, "type": item.get("cmpyname", "Filing"),
                             "title": desc[:200], "url": url_str, "source": "NSE"})
        return filings
    except Exception as e:
        print(f"  [{row['ticker']}] NSE filings failed: {e}")
        return []


def fetch_bse_filings(row: dict, session: requests.Session) -> list:
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
        r = session.post(BSE_API, data=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        filings = []
        for item in (data.get("Table", []) or []):
            date_raw = item.get("NewsDate", "") or item.get("DissemDT", "")
            date = _parse_date(str(date_raw)) if date_raw else TODAY
            title = item.get("NEWSSUB", "") or item.get("HEADLINE", "")
            link = item.get("ATTACHMENTNAME", "") or ""
            url_str = (
                f"https://www.bseindia.com/xml-data/corpfiling/AttachHis/{link}"
                if link else ""
            )
            filings.append({"date": date, "type": "BSE Filing",
                             "title": title[:200], "url": url_str, "source": "BSE"})
        return filings
    except Exception as e:
        print(f"  [{row['ticker']}] BSE filings failed: {e}")
        return []


# ---------------------------------------------------------------------------
# Lane A — Catalogue update
# ---------------------------------------------------------------------------

CATALOGUE_HEADER = "| Date | Source | Type | Title | URL | Status |"
CATALOGUE_SEP = "|---|---|---|---|---|---|"


def update_catalogue(row: dict, out_dir: Path, filings: list):
    if not filings:
        return

    cat_file = out_dir / "catalogue.md"
    existing = cat_file.read_text(encoding="utf-8") if cat_file.exists() else ""
    is_legacy = CATALOGUE_HEADER not in existing

    known = set()
    for line in existing.splitlines():
        if line.startswith("|") and "http" in line:
            for p in [p.strip() for p in line.split("|")]:
                if p.startswith("http"):
                    known.add(p)
        if line.startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) > 2:
                known.add(parts[2].lower()[:60])

    new_rows = []
    for f in filings:
        url = f.get("url", "")
        title = f.get("title", "")
        if url in known or title.lower()[:60] in known:
            continue
        new_rows.append(
            f"| {f['date']} | {f['source']} | {f['type']} | {title} | {url} | New |"
        )
        if url:
            known.add(url)
        known.add(title.lower()[:60])

    if not new_rows:
        return

    rows_text = "\n".join(new_rows)
    if is_legacy:
        section = (
            f"\n\n## Exchange Filings — fetched {TODAY}\n\n"
            f"{CATALOGUE_HEADER}\n{CATALOGUE_SEP}\n{rows_text}\n"
        )
        cat_file.write_text(existing.rstrip() + section, encoding="utf-8")
    else:
        idx = existing.find(CATALOGUE_SEP)
        if idx == -1:
            cat_file.write_text(existing.rstrip() + f"\n{rows_text}\n", encoding="utf-8")
        else:
            insert_pos = idx + len(CATALOGUE_SEP)
            cat_file.write_text(
                existing[:insert_pos] + "\n" + rows_text + existing[insert_pos:],
                encoding="utf-8",
            )

    print(f"  [{row['ticker']}] Catalogue: {len(new_rows)} new filing(s) added")


# ---------------------------------------------------------------------------
# Lane B — Discovery news fetch (broad market/theme queries)
# ---------------------------------------------------------------------------

def fetch_discovery(session: requests.Session):
    """
    Lane B: broad market signal collection.
    Runs DISCOVERY_QUERIES against Google News RSS.
    Writes raw headlines to 02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/discovery-news.md.
    Does NOT parse company names. Does NOT modify 01_UNIVERSE/company_master.csv.
    Universe Manager and Discovery News Agent review this output on Monday.
    """
    print("\n=== Lane B: Discovery News Fetch ===\n")
    out_dir = DISCOVERY_DIR / TODAY
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "discovery-news.md"

    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    lines = [
        f"# Discovery News — {TODAY}",
        f"Fetched: {TODAY}",
        "",
        "Raw market signals for Discovery News Agent review.",
        "Source: Google News RSS. This file is read-only input for Universe Manager.",
        "Universe Manager is the only agent authorised to update company_master.csv.",
        "",
    ]

    total_items = 0
    for query in DISCOVERY_QUERIES:
        rss_url = (
            f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}"
            f"&hl=en-IN&gl=IN&ceid=IN:en"
        )
        try:
            r = retry_get(rss_url, session)
            items = _parse_rss_items(r.content, cutoff)
            lines.append(f"## {query}")
            lines.append("")
            lines.append("| Source | Headline | Date | URL |")
            lines.append("|---|---|---|---|")
            for source, title, date, link in items:
                lines.append(f"| {source} | {title} | {date} | {link} |")
                total_items += 1
            if not items:
                lines.append("_No items in the last 7 days._")
            lines.append("")
            time.sleep(0.5)
        except Exception as e:
            lines.append(f"_Query failed: {e}_")
            lines.append("")
            print(f"  Discovery query failed [{query}]: {e}")

    out_file.write_text("\n".join(lines))
    print(f"Discovery: {total_items} items across {len(DISCOVERY_QUERIES)} queries → {out_file}")
    return total_items > 0


# ---------------------------------------------------------------------------
# Universe loader
# ---------------------------------------------------------------------------

def load_companies() -> list:
    if not UNIVERSE_CSV.exists():
        print(f"ERROR: Universe CSV not found: {UNIVERSE_CSV}")
        sys.exit(1)
    with open(UNIVERSE_CSV, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("fetch_enabled", "").lower() == "true"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    check_legacy_csv()

    print(f"=== Weekly Evidence Fetch — {TODAY} ===\n")
    print(f"Universe: {UNIVERSE_CSV}")

    companies = load_companies()
    print(f"Lane A companies (fetch_enabled=true): {len(companies)}")
    for c in companies:
        print(f"  {c['ticker']} — {c['company_name']}")
    print()

    session = make_session()
    print("Priming NSE session...")
    prime_nse(session)

    # Lane A — Company Evidence Fetch
    print("\n=== Lane A: Company Evidence Fetch ===\n")
    successes, failures = 0, 0

    for row in companies:
        ticker = row["ticker"]
        out_dir = RAW_DIR / ticker
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n--- {ticker}: {row['company_name']} ---")

        ok_price = fetch_prices(row, out_dir)
        ok_news = fetch_news(row, out_dir, session)
        time.sleep(1)

        filings = fetch_nse_filings(row, session)
        time.sleep(1)
        if not filings:
            filings = fetch_bse_filings(row, session)
            time.sleep(1)

        if filings:
            print(f"  [{ticker}] Filings: {len(filings)} found")
            update_catalogue(row, out_dir, filings)
        else:
            print(f"  [{ticker}] Filings: none retrieved")

        if ok_price or ok_news or filings:
            successes += 1
        else:
            failures += 1
            print(f"  [{ticker}] WARNING: no data fetched")

    print(f"\nLane A: {successes} succeeded, {failures} failed")

    # Lane B — Discovery News Fetch
    fetch_discovery(session)

    print(f"\n=== Weekly Evidence Fetch Complete — {TODAY} ===")
    if failures == len(companies) and len(companies) > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
