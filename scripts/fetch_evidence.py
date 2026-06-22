#!/usr/bin/env python3
"""
Weekly evidence fetch — no AI, no API keys required.
Pulls prices (yfinance), news (Google News RSS), and exchange filings (NSE/BSE).
Commits raw evidence to the repo for Claude Code to process locally.
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
DATA_DIR = ROOT / "data"
RAW_DIR = ROOT / "02_RAW_DOCUMENTS"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/html,application/xhtml+xml,*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

NSE_BASE = "https://www.nseindia.com"
BSE_API = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"


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
    """Hit NSE homepage to establish cookies before API calls."""
    try:
        retry_get(NSE_BASE, session)
        time.sleep(1)
    except Exception as e:
        print(f"  Warning: NSE prime failed: {e}")


# ---------------------------------------------------------------------------
# Price fetch
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
# News fetch (Google News RSS)
# ---------------------------------------------------------------------------

def fetch_news(row: dict, out_dir: Path, session: requests.Session):
    query = f"{row['company_name']} {row['ticker']} NSE"
    rss_url = (
        f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}"
        f"&hl=en-IN&gl=IN&ceid=IN:en"
    )

    try:
        r = retry_get(rss_url, session)
        root = ET.fromstring(r.content)
        items = root.findall(".//item")[:15]

        rows = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        for item in items:
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

            rows.append(f"| {source} | {title} | {pub_date} | {link} |")

        if not rows:
            print(f"  [{row['ticker']}] No recent news items found")
            return False

        lines = [
            f"# News — {row['company_name']} ({row['ticker']})",
            f"Fetched: {TODAY}",
            "",
            "| Source | Headline | Date | URL |",
            "|---|---|---|---|",
        ] + rows

        out_file = out_dir / f"news-{TODAY}.md"
        out_file.write_text("\n".join(lines))
        print(f"  [{row['ticker']}] News: {len(rows)} items → {out_file.name}")
        return True
    except Exception as e:
        print(f"  [{row['ticker']}] News fetch failed: {e}")
        return False


# ---------------------------------------------------------------------------
# Exchange filings
# ---------------------------------------------------------------------------

def _parse_date(raw: str) -> str:
    """Parse NSE or BSE date strings to YYYY-MM-DD."""
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
            url_str = f"https://nsearchives.nseindia.com/{attach}" if attach and not attach.startswith("http") else attach
            filings.append({
                "date": date,
                "type": item.get("cmpyname", "Filing"),
                "title": desc[:200],
                "url": url_str,
                "source": "NSE",
            })
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
        r = retry_get(BSE_API, session)
        # BSE requires POST with form data
        r = session.post(BSE_API, data=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        filings = []
        for item in (data.get("Table", []) or []):
            date_raw = item.get("NewsDate", "") or item.get("DissemDT", "")
            date = _parse_date(str(date_raw)) if date_raw else TODAY
            title = item.get("NEWSSUB", "") or item.get("HEADLINE", "")
            link = item.get("ATTACHMENTNAME", "") or ""
            url_str = f"https://www.bseindia.com/xml-data/corpfiling/AttachHis/{link}" if link else ""
            filings.append({
                "date": date,
                "type": "BSE Filing",
                "title": title[:200],
                "url": url_str,
                "source": "BSE",
            })
        return filings
    except Exception as e:
        print(f"  [{row['ticker']}] BSE filings failed: {e}")
        return []


# ---------------------------------------------------------------------------
# Catalogue update
# ---------------------------------------------------------------------------

CATALOGUE_HEADER = "| Date | Source | Type | Title | URL | Status |"
CATALOGUE_SEP = "|---|---|---|---|---|---|"


def update_catalogue(row: dict, out_dir: Path, filings: list):
    if not filings:
        return

    cat_file = out_dir / "catalogue.md"
    existing = cat_file.read_text(encoding="utf-8") if cat_file.exists() else ""

    # Determine if this is legacy Claude format (5-col) or new format (6-col)
    is_legacy = CATALOGUE_HEADER not in existing

    # De-dupe: collect known URLs and titles already in the file
    known = set()
    for line in existing.splitlines():
        if line.startswith("|") and "http" in line:
            parts = [p.strip() for p in line.split("|")]
            for p in parts:
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
        # Append a new dated section so existing Claude-format data is untouched
        section = (
            f"\n\n## Exchange Filings — fetched {TODAY}\n\n"
            f"{CATALOGUE_HEADER}\n{CATALOGUE_SEP}\n{rows_text}\n"
        )
        cat_file.write_text(existing.rstrip() + section, encoding="utf-8")
    else:
        # Insert after the header separator row
        insert_after = CATALOGUE_SEP
        idx = existing.find(insert_after)
        if idx == -1:
            # No separator found — append
            cat_file.write_text(existing.rstrip() + f"\n{rows_text}\n", encoding="utf-8")
        else:
            insert_pos = idx + len(insert_after)
            cat_file.write_text(
                existing[:insert_pos] + "\n" + rows_text + existing[insert_pos:],
                encoding="utf-8",
            )

    print(f"  [{row['ticker']}] Catalogue: {len(new_rows)} new filing(s) added")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_companies() -> list:
    csv_path = DATA_DIR / "company_master.csv"
    with open(csv_path, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("active", "").lower() == "true"]


def main():
    import urllib.parse  # ensure available in module scope

    print(f"=== Weekly Evidence Fetch — {TODAY} ===\n")
    companies = load_companies()
    print(f"Active companies: {len(companies)}\n")

    session = make_session()
    print("Priming NSE session...")
    prime_nse(session)

    successes, failures = 0, 0

    for row in companies:
        ticker = row["ticker"]
        out_dir = RAW_DIR / ticker
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n--- {ticker}: {row['company_name']} ---")

        ok_price = fetch_prices(row, out_dir)
        ok_news = fetch_news(row, out_dir, session)
        time.sleep(1)

        # Try NSE first, fall back to BSE
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

    print(f"\n=== Done — {successes} succeeded, {failures} failed ===")
    if failures == len(companies):
        sys.exit(1)


if __name__ == "__main__":
    main()
