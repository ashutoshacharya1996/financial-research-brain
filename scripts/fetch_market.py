#!/usr/bin/env python3
"""
Weekly market fetch — no AI, no API keys required.

Replaces the per-stock evidence fetch (scripts/fetch_evidence.py) as the
scheduled Sunday job. Collects the inputs the /market-brief skill needs:

1. Indian indices (broad + size + sectors) and global/macro markers  (yfinance, NSE)
2. Valuation + breadth for Indian indices                             (NSE allIndices)
3. FII / DII cash-market flows                                        (NSE)
4. NAV returns for every fund in 01_UNIVERSE/mf_watchlist.csv          (AMFI + mfapi.in)
5. Market / macro / AMC news headlines for the last 7 days            (Google News RSS)

Output: 02_RAW_DOCUMENTS/_market/<YYYY-MM-DD>/
  market-snapshot.json   all numbers, machine-readable
  market-summary.md      the same numbers as tables (what the brief reads first)
  news.md                headlines grouped by topic

Every source is fallible. A failure in one source is recorded in
`source_status` and never fails the run.
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install yfinance requests")
    sys.exit(1)

try:
    import yfinance as yf
except ImportError:  # the run continues; index data will be NSE-only
    yf = None


ROOT = Path(__file__).resolve().parent.parent
WATCHLIST_CSV = ROOT / "01_UNIVERSE" / "mf_watchlist.csv"
MARKET_DIR = ROOT / "02_RAW_DOCUMENTS" / "_market"
TODAY = datetime.now(timezone.utc).date()
OUT_DIR = MARKET_DIR / TODAY.isoformat()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/json,text/html,text/plain,*/*",
    "Accept-Language": "en-IN,en;q=0.9",
}

NSE_BASE = "https://www.nseindia.com"
AMFI_NAV_ALL = "https://www.amfiindia.com/spages/NAVAll.txt"
MFAPI = "https://api.mfapi.in/mf/{code}"

WAR_CHEST_TRIGGER_NIFTY = 22000  # locked decision; see financial-advisor locked-decisions

# key -> (display name, NSE allIndices name, [yfinance candidates], group)
INDICES = {
    "NIFTY_50": ("Nifty 50", "NIFTY 50", ["^NSEI"], "broad"),
    "SENSEX": ("Sensex", None, ["^BSESN"], "broad"),
    "NIFTY_500": ("Nifty 500", "NIFTY 500", ["^CRSLDX"], "broad"),
    "NIFTY_LARGEMID_250": ("Nifty LargeMidcap 250", "NIFTY LARGEMIDCAP 250", [], "size"),
    "NIFTY_MIDCAP_150": ("Nifty Midcap 150", "NIFTY MIDCAP 150", ["NIFTYMIDCAP150.NS"], "size"),
    "NIFTY_SMALLCAP_250": ("Nifty Smallcap 250", "NIFTY SMALLCAP 250", ["NIFTYSMLCAP250.NS"], "size"),
    "NIFTY_BANK": ("Bank", "NIFTY BANK", ["^NSEBANK"], "sector"),
    "NIFTY_FIN": ("Financial Services", "NIFTY FINANCIAL SERVICES", ["NIFTY_FIN_SERVICE.NS"], "sector"),
    "NIFTY_IT": ("IT", "NIFTY IT", ["^CNXIT"], "sector"),
    "NIFTY_AUTO": ("Auto", "NIFTY AUTO", ["^CNXAUTO"], "sector"),
    "NIFTY_PHARMA": ("Pharma", "NIFTY PHARMA", ["^CNXPHARMA"], "sector"),
    "NIFTY_FMCG": ("FMCG", "NIFTY FMCG", ["^CNXFMCG"], "sector"),
    "NIFTY_METAL": ("Metal", "NIFTY METAL", ["^CNXMETAL"], "sector"),
    "NIFTY_REALTY": ("Realty", "NIFTY REALTY", ["^CNXREALTY"], "sector"),
    "NIFTY_ENERGY": ("Energy", "NIFTY ENERGY", ["^CNXENERGY"], "sector"),
    "NIFTY_INFRA": ("Infrastructure", "NIFTY INFRASTRUCTURE", ["^CNXINFRA"], "sector"),
    "NIFTY_PSU_BANK": ("PSU Bank", "NIFTY PSU BANK", ["^CNXPSUBANK"], "sector"),
    "NIFTY_HEALTHCARE": ("Healthcare", "NIFTY HEALTHCARE INDEX", [], "sector"),
    "NIFTY_CONSUMER_DURABLES": ("Consumer Durables", "NIFTY CONSUMER DURABLES", [], "sector"),
    "NIFTY_DEFENCE": ("Defence", "NIFTY INDIA DEFENCE", [], "sector"),
    "NIFTY_CPSE": ("PSU (CPSE)", "NIFTY CPSE", ["^CNXCPSE"], "sector"),
    "INDIA_VIX": ("India VIX", "INDIA VIX", ["^INDIAVIX"], "risk"),
}

GLOBAL = {
    "SP500": ("S&P 500", ["^GSPC"]),
    "NASDAQ": ("Nasdaq", ["^IXIC"]),
    "BRENT": ("Brent crude ($)", ["BZ=F"]),
    "GOLD": ("Gold ($/oz)", ["GC=F"]),
    "USDINR": ("USD/INR", ["INR=X", "USDINR=X"]),
    "US10Y": ("US 10Y yield (%)", ["^TNX"]),
    "DXY": ("Dollar index", ["DX-Y.NYB"]),
}

NEWS_TOPICS = {
    "Market wrap": ["Sensex Nifty week", "Nifty weekly", "stock market India this week"],
    "Mid & small caps": ["Nifty midcap smallcap"],
    "Flows": ["FII outflow India equities", "DII inflow mutual fund SIP"],
    "RBI & macro": ["RBI repo rate", "India inflation CPI", "India GDP growth"],
    "Global": ["US Fed rate decision", "crude oil price"],
    "Mutual fund industry": ["SEBI mutual fund", "AMFI SIP inflows"],
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def session_get(session: requests.Session, url: str, retries: int = 3, timeout: int = 25, **kw):
    delay = 2
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=timeout, **kw)
            r.raise_for_status()
            return r
        except Exception as exc:  # noqa: BLE001
            if attempt == retries - 1:
                raise
            print(f"  retry {attempt + 1}/{retries} {url}: {exc}")
            time.sleep(delay)
            delay *= 2


def pct(new, old):
    try:
        if new is None or old in (None, 0):
            return None
        return round((float(new) / float(old) - 1) * 100, 2)
    except Exception:  # noqa: BLE001
        return None


def num(v):
    try:
        if v in (None, "", "-"):
            return None
        return float(str(v).replace(",", ""))
    except Exception:  # noqa: BLE001
        return None


def load_prior_snapshot() -> dict:
    if not MARKET_DIR.exists():
        return {}
    dirs = sorted(d for d in MARKET_DIR.iterdir() if d.is_dir() and d.name < TODAY.isoformat())
    for d in reversed(dirs):
        f = d / "market-snapshot.json"
        if f.exists():
            try:
                return json.loads(f.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                return {}
    return {}


# ---------------------------------------------------------------------------
# 1. price history via yfinance
# ---------------------------------------------------------------------------

def yf_series(candidates: list[str]):
    if yf is None:
        return None, None
    for sym in candidates:
        try:
            hist = yf.Ticker(sym).history(period="1y", auto_adjust=False)
            if hist is not None and not hist.empty and len(hist) > 5:
                return sym, hist["Close"].dropna()
        except Exception as exc:  # noqa: BLE001
            print(f"  yfinance {sym} failed: {exc}")
    return None, None


def series_stats(closes) -> dict:
    last = float(closes.iloc[-1])
    last_dt = closes.index[-1].date()

    def close_on_or_before(days):
        target = last_dt - timedelta(days=days)
        sub = closes[[d.date() <= target for d in closes.index]]
        return float(sub.iloc[-1]) if len(sub) else None

    out = {
        "last": round(last, 2),
        "as_of": last_dt.isoformat(),
        "chg_1w_pct": pct(last, close_on_or_before(7)),
        "chg_1m_pct": pct(last, close_on_or_before(30)),
        "chg_3m_pct": pct(last, close_on_or_before(91)),
        "chg_1y_pct": pct(last, float(closes.iloc[0])) if len(closes) > 200 else None,
        "high_52w": round(float(closes.max()), 2),
        "low_52w": round(float(closes.min()), 2),
    }
    out["from_52w_high_pct"] = pct(last, out["high_52w"])
    if len(closes) >= 50:
        out["dma_50"] = round(float(closes.iloc[-50:].mean()), 2)
    if len(closes) >= 200:
        out["dma_200"] = round(float(closes.iloc[-200:].mean()), 2)
        out["vs_200dma_pct"] = pct(last, out["dma_200"])
    return out


# ---------------------------------------------------------------------------
# 2. NSE allIndices (valuation, breadth) and 3. FII/DII
# ---------------------------------------------------------------------------

def nse_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    try:
        session_get(s, NSE_BASE, retries=2)
        time.sleep(1)
    except Exception as exc:  # noqa: BLE001
        print(f"  NSE prime failed: {exc}")
    return s


def fetch_nse_all_indices(s: requests.Session) -> dict:
    r = session_get(s, f"{NSE_BASE}/api/allIndices")
    rows = r.json().get("data", [])
    out = {}
    for row in rows:
        name = (row.get("index") or row.get("indexSymbol") or "").strip().upper()
        if not name:
            continue
        out[name] = {
            "last": num(row.get("last")),
            "chg_1d_pct": num(row.get("percentChange")),
            "chg_1m_pct": num(row.get("perChange30d")),
            "chg_1y_pct": num(row.get("perChange365d")),
            "pe": num(row.get("pe")),
            "pb": num(row.get("pb")),
            "div_yield": num(row.get("dy")),
            "high_52w": num(row.get("yearHigh")),
            "low_52w": num(row.get("yearLow")),
            "advances": num(row.get("advances")),
            "declines": num(row.get("declines")),
        }
    return out


def fetch_fii_dii(s: requests.Session) -> list:
    r = session_get(s, f"{NSE_BASE}/api/fiidiiTradeReact")
    data = r.json()
    rows = data if isinstance(data, list) else data.get("data", [])
    out = []
    for row in rows:
        out.append({
            "category": row.get("category"),
            "date": row.get("date"),
            "buy_cr": num(row.get("buyValue")),
            "sell_cr": num(row.get("sellValue")),
            "net_cr": num(row.get("netValue")),
        })
    return out


# ---------------------------------------------------------------------------
# 4. mutual funds
# ---------------------------------------------------------------------------

def load_watchlist() -> list[dict]:
    with WATCHLIST_CSV.open(encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("fund_name") or "").strip()]


def parse_amfi(text: str) -> list[tuple[str, str]]:
    schemes = []
    for line in text.splitlines():
        parts = line.split(";")
        if len(parts) >= 6 and parts[0].strip().isdigit():
            schemes.append((parts[0].strip(), parts[3].strip()))
    return schemes


EXCLUDE_WORDS = ("idcw", "dividend", "bonus", "regular", "payout", "reinvest", "segregated")


def resolve_scheme_code(fund: dict, schemes: list[tuple[str, str]]) -> tuple[str | None, str | None]:
    if (fund.get("scheme_code") or "").strip():
        return fund["scheme_code"].strip(), None
    kws = [k.strip().lower() for k in (fund.get("match_keywords") or "").split("|") if k.strip()]
    matches = []
    for code, name in schemes:
        low = name.lower()
        if not all(k in low for k in kws):
            continue
        if "direct" not in low or "growth" not in low:
            continue
        if any(w in low for w in EXCLUDE_WORDS):
            continue
        matches.append((len(name), code, name))
    if not matches:
        return None, None
    matches.sort()
    return matches[0][1], matches[0][2]


def nav_returns(navs: list[tuple[date, float]]) -> dict:
    """navs sorted newest first."""
    last_dt, last = navs[0]

    def nav_on_or_before(days):
        target = last_dt - timedelta(days=days)
        for d, v in navs:
            if d <= target:
                return v
        return None

    out = {
        "nav": round(last, 4),
        "nav_date": last_dt.isoformat(),
        "ret_1w_pct": pct(last, nav_on_or_before(7)),
        "ret_1m_pct": pct(last, nav_on_or_before(30)),
        "ret_3m_pct": pct(last, nav_on_or_before(91)),
        "ret_1y_pct": pct(last, nav_on_or_before(365)),
    }
    v3 = nav_on_or_before(365 * 3)
    out["cagr_3y_pct"] = round(((last / v3) ** (1 / 3) - 1) * 100, 2) if v3 else None
    v5 = nav_on_or_before(365 * 5)
    out["cagr_5y_pct"] = round(((last / v5) ** (1 / 5) - 1) * 100, 2) if v5 else None
    window = [v for d, v in navs if d >= last_dt - timedelta(days=365)]
    if window:
        peak = max(window)
        out["from_1y_peak_pct"] = pct(last, peak)
    return out


def fetch_funds(session: requests.Session, status: dict) -> list[dict]:
    funds = load_watchlist()
    try:
        schemes = parse_amfi(session_get(session, AMFI_NAV_ALL, timeout=60).text)
        status["amfi_navall"] = f"ok ({len(schemes)} schemes)"
    except Exception as exc:  # noqa: BLE001
        schemes = []
        status["amfi_navall"] = f"failed: {exc}"

    out = []
    for fund in funds:
        rec = {k: fund.get(k) for k in ("fund_name", "category", "benchmark_key", "status", "sip_amount", "notes")}
        code, matched_name = resolve_scheme_code(fund, schemes)
        rec["scheme_code"] = code
        rec["matched_scheme_name"] = matched_name
        if not code:
            rec["error"] = "scheme code not resolved — set scheme_code in mf_watchlist.csv"
            print(f"  [MF] {fund['fund_name']}: unresolved")
            out.append(rec)
            continue
        try:
            payload = session_get(session, MFAPI.format(code=code)).json()
            meta = payload.get("meta", {})
            rec["matched_scheme_name"] = rec["matched_scheme_name"] or meta.get("scheme_name")
            rec["amc"] = meta.get("fund_house")
            rec["scheme_category"] = meta.get("scheme_category")
            navs = []
            for row in payload.get("data", []):
                try:
                    navs.append((datetime.strptime(row["date"], "%d-%m-%Y").date(), float(row["nav"])))
                except Exception:  # noqa: BLE001
                    continue
            navs.sort(reverse=True)
            if navs:
                rec.update(nav_returns(navs))
                print(f"  [MF] {fund['fund_name']}: 1W {rec.get('ret_1w_pct')}%  1Y {rec.get('ret_1y_pct')}%")
            else:
                rec["error"] = "no NAV history"
        except Exception as exc:  # noqa: BLE001
            rec["error"] = f"mfapi failed: {exc}"
            print(f"  [MF] {fund['fund_name']}: {exc}")
        out.append(rec)
        time.sleep(0.5)
    return out


# ---------------------------------------------------------------------------
# 5. news
# ---------------------------------------------------------------------------

def fetch_news(session: requests.Session, funds: list[dict]) -> dict:
    topics = dict(NEWS_TOPICS)
    amcs = sorted({(f.get("fund_name") or "").split()[0] for f in funds if f.get("fund_name")})
    topics["Your fund houses"] = [f'"{a}" mutual fund' for a in amcs]
    cutoff = datetime.now(timezone.utc) - timedelta(days=8)
    out: dict[str, list] = {}
    seen = set()
    for topic, queries in topics.items():
        items = []
        for q in queries:
            url = (f"https://news.google.com/rss/search?q={urllib.parse.quote(q + ' when:7d')}"
                   f"&hl=en-IN&gl=IN&ceid=IN:en")
            try:
                root = ET.fromstring(session_get(session, url, retries=2).content)
            except Exception as exc:  # noqa: BLE001
                print(f"  [NEWS] {q}: {exc}")
                continue
            for it in root.findall(".//item")[:8]:
                title = (it.findtext("title") or "").strip()
                if not title or title in seen:
                    continue
                pub = (it.findtext("pubDate") or "").strip()
                try:
                    dt = datetime.strptime(pub, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
                    if dt < cutoff:
                        continue
                    pub = dt.date().isoformat()
                except Exception:  # noqa: BLE001
                    pass
                src = it.find("source")
                seen.add(title)
                items.append({
                    "query": q,
                    "title": title,
                    "source": src.text if src is not None and src.text else "",
                    "date": pub,
                    "url": (it.findtext("link") or "").strip(),
                })
        out[topic] = items
    return out


# ---------------------------------------------------------------------------
# summary markdown
# ---------------------------------------------------------------------------

def f(v, suffix="%"):
    return "—" if v is None else f"{v:+.2f}{suffix}" if suffix == "%" else f"{v:,.2f}"


def build_summary(snap: dict) -> str:
    L = [f"# Market Summary — week ending {snap['as_of']}", "",
         "Auto-generated by scripts/fetch_market.py. Numbers only — no interpretation.", ""]
    idx = snap["indices"]

    def idx_table(group, title):
        rows = [(k, v) for k, v in idx.items() if v.get("group") == group]
        if not rows:
            return
        L.extend([f"## {title}", "", "| Index | Level | 1W | 1M | 1Y | vs 200DMA | PE | from 52W high |",
                  "|---|---|---|---|---|---|---|---|"])
        if group == "sector":
            rows.sort(key=lambda kv: (kv[1].get("chg_1w_pct") is None, -(kv[1].get("chg_1w_pct") or 0)))
        for _, v in rows:
            L.append(f"| {v['name']} | {f(v.get('last'), '')} | {f(v.get('chg_1w_pct'))} | {f(v.get('chg_1m_pct'))} | "
                     f"{f(v.get('chg_1y_pct'))} | {f(v.get('vs_200dma_pct'))} | "
                     f"{'—' if v.get('pe') is None else v['pe']} | {f(v.get('from_52w_high_pct'))} |")
        L.append("")

    idx_table("broad", "Broad market")
    idx_table("size", "Size buckets")
    idx_table("risk", "Risk gauge")
    idx_table("sector", "Sectors (sorted by 1W)")

    if snap.get("global"):
        L.extend(["## Global & macro", "", "| Marker | Last | 1W | 1M | 1Y |", "|---|---|---|---|---|"])
        for v in snap["global"].values():
            L.append(f"| {v['name']} | {f(v.get('last'), '')} | {f(v.get('chg_1w_pct'))} | "
                     f"{f(v.get('chg_1m_pct'))} | {f(v.get('chg_1y_pct'))} |")
        L.append("")

    if snap.get("fii_dii"):
        L.extend(["## FII / DII (latest NSE day)", "", "| Category | Date | Net ₹ cr |", "|---|---|---|"])
        for r in snap["fii_dii"]:
            L.append(f"| {r.get('category')} | {r.get('date')} | {r.get('net_cr')} |")
        L.append("")

    wc = snap.get("war_chest", {})
    if wc:
        L.extend(["## War-chest trigger", "",
                  f"Nifty 50 {wc.get('nifty_last')} vs trigger {wc.get('trigger')} → "
                  f"{wc.get('distance_pct')}% above trigger", ""])

    L.extend(["## Your funds", "",
              "| Fund | Status | 1W | 1M | 3M | 1Y | 3Y CAGR | Benchmark 1M | Benchmark 1Y | from 1Y peak |",
              "|---|---|---|---|---|---|---|---|---|---|"])
    for m in snap["funds"]:
        b = idx.get(m.get("benchmark_key") or "", {})
        if m.get("error"):
            L.append(f"| {m['fund_name']} | {m.get('status')} | ⚠ {m['error']} | | | | | | | |")
            continue
        L.append(f"| {m['fund_name']} | {m.get('status')} | {f(m.get('ret_1w_pct'))} | {f(m.get('ret_1m_pct'))} | "
                 f"{f(m.get('ret_3m_pct'))} | {f(m.get('ret_1y_pct'))} | {f(m.get('cagr_3y_pct'))} | "
                 f"{f(b.get('chg_1m_pct'))} | {f(b.get('chg_1y_pct'))} | {f(m.get('from_1y_peak_pct'))} |")
    L.append("")

    L.extend(["## Source status", ""] + [f"- {k}: {v}" for k, v in snap["source_status"].items()] + [""])
    return "\n".join(L)


def build_news_md(news: dict) -> str:
    L = [f"# Market News — week ending {TODAY.isoformat()}", "", "Google News RSS, last 7 days. tier_3 — headlines only.", ""]
    for topic, items in news.items():
        L.extend([f"## {topic}", ""])
        if not items:
            L.extend(["_No items._", ""])
            continue
        for it in items:
            L.append(f"- {it['date']} — {it['title']} ({it['source']})")
        L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    status: dict[str, str] = {}
    prior = load_prior_snapshot()
    web = requests.Session()
    web.headers.update(HEADERS)

    print("--- NSE ---")
    nse = nse_session()
    try:
        nse_idx = fetch_nse_all_indices(nse)
        status["nse_all_indices"] = f"ok ({len(nse_idx)} indices)"
    except Exception as exc:  # noqa: BLE001
        nse_idx = {}
        status["nse_all_indices"] = f"failed: {exc}"
    try:
        fii_dii = fetch_fii_dii(nse)
        status["nse_fii_dii"] = "ok"
    except Exception as exc:  # noqa: BLE001
        fii_dii = []
        status["nse_fii_dii"] = f"failed: {exc}"

    print("--- Indices ---")
    indices = {}
    yf_ok = 0
    for key, (name, nse_name, candidates, group) in INDICES.items():
        rec = {"name": name, "group": group}
        sym, closes = yf_series(candidates)
        if closes is not None:
            rec.update(series_stats(closes))
            rec["source"] = f"yfinance:{sym}"
            yf_ok += 1
        n = nse_idx.get(nse_name or "", {})
        if n:
            for k in ("pe", "pb", "div_yield", "advances", "declines"):
                rec[k] = n.get(k)
            if rec.get("last") is None:
                rec.update({k: n.get(k) for k in ("last", "chg_1m_pct", "chg_1y_pct", "high_52w", "low_52w")})
                rec["from_52w_high_pct"] = pct(n.get("last"), n.get("high_52w"))
                prev = (prior.get("indices", {}).get(key) or {}).get("last")
                rec["chg_1w_pct"] = pct(n.get("last"), prev)
                rec["source"] = "nse:allIndices" + (" (+prior snapshot for 1W)" if prev else "")
        if rec.get("last") is None:
            rec["error"] = "no data"
        indices[key] = rec
        print(f"  {name}: {rec.get('last')} 1W {rec.get('chg_1w_pct')}")
    status["yfinance_indices"] = f"{yf_ok}/{len(INDICES)}" if yf else "yfinance not installed"

    glob = {}
    for key, (name, candidates) in GLOBAL.items():
        sym, closes = yf_series(candidates)
        if closes is not None:
            glob[key] = {"name": name, **series_stats(closes), "source": f"yfinance:{sym}"}
    status["yfinance_global"] = f"{len(glob)}/{len(GLOBAL)}"

    nifty = indices.get("NIFTY_50", {}).get("last")
    war_chest = {
        "trigger": WAR_CHEST_TRIGGER_NIFTY,
        "nifty_last": nifty,
        "distance_pct": pct(nifty, WAR_CHEST_TRIGGER_NIFTY),
    }

    print("--- Mutual funds ---")
    funds = fetch_funds(web, status)
    status["funds"] = f"{sum(1 for m in funds if not m.get('error'))}/{len(funds)} with NAV data"

    print("--- News ---")
    news = fetch_news(web, funds)
    status["news"] = f"{sum(len(v) for v in news.values())} headlines"

    snap = {
        "as_of": TODAY.isoformat(),
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "indices": indices,
        "global": glob,
        "fii_dii": fii_dii,
        "war_chest": war_chest,
        "funds": funds,
        "source_status": status,
    }
    (OUT_DIR / "market-snapshot.json").write_text(json.dumps(snap, indent=2), encoding="utf-8")
    (OUT_DIR / "market-summary.md").write_text(build_summary(snap), encoding="utf-8")
    (OUT_DIR / "news.md").write_text(build_news_md(news), encoding="utf-8")
    print(f"\nWrote {OUT_DIR.relative_to(ROOT)}/ — status: {json.dumps(status)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
