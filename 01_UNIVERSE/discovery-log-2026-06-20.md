# Universe Discovery Log — 2026-06-20

## Nifty 500 Refresh

- Constituents confirmed: 113 (partial — see Access Limitation note below)
- New additions to index since last run: N/A (first run, no prior baseline)
- Dropped from index since last run: N/A (first run)

### Access Limitation

The NSE India official Nifty 500 PDF (`nsearchives.nseindia.com`) and major third-party data providers (MoneyWorks4Me, Univest, Trendlyne) returned HTTP 403 Forbidden during this run. The full 500-company list could not be fetched programmatically.

**What was populated:** The Nifty 50 constituents (all confirmed Nifty 500 members) plus ~60 well-known Nifty 200/500 mid-caps spanning all major sectors, sourced from knowledge of the index composition as of H1 2026.

**Recommended fix:** Subscribe to a data API (NSE direct data feed, Tiingo, or Polygon India) and store the API key as `NSE_DATA_API_KEY` in repository secrets. The universe-manager will prefer the API over web scraping on the next run.

**Coverage by sector (this run):**
| Sector | Companies |
|---|---|
| Financial Services | 12 |
| Information Technology | 8 |
| Capital Goods | 12 |
| Healthcare | 11 |
| Automobile and Auto Components | 9 |
| Fast Moving Consumer Goods | 9 |
| Metals & Mining | 7 |
| Power | 4 |
| Oil Gas & Consumable Fuels | 6 |
| Construction Materials | 6 |
| Realty | 5 |
| Chemicals | 3 |
| Telecommunication | 3 |
| Consumer Durables | 5 |
| Services | 3 |
| Textiles | 2 |

---

## News Discovery — New Stocks Added

| Ticker | Company | Sector | Why Flagged | Source |
|---|---|---|---|---|
| PARAS | Paras Defence & Space Technologies Ltd | Capital Goods | BEL subcontract for electro-optics worth Rs 52.82 crore; appears in 2+ news items this week (contract filing + price reaction) | [BusinessToday, June 2026](https://www.businesstoday.in/markets/stocks/story/defence-stock-jumps-over-30-in-2026-so-far-up-9-today-order-win-from-bel-q4-results-and-more-534887-2026-06-04) |
| JNKINDIA | JNK India Ltd | Capital Goods | Large UAE export order for waste gas handling systems (TA'ZIZ Salt Project, ADNOC); stock up 94% YTD 2026; appears in 2+ news items (order win + analyst coverage) | [Business Standard, June 9 2026](https://www.business-standard.com/markets/news/jnk-india-shares-jump-12-on-large-order-win-stock-up-94-in-2026-so-far-126060900243_1.html) |
| GABRIEL | Gabriel India Ltd | Automobile and Auto Components | Motilal Oswal initiates Buy coverage (target Rs 1266, ~24% upside); management guiding Rs 50,000 crore group revenue by 2030; diversifying into e-mobility and adjacent segments | [Business Standard, June 9 2026](https://www.business-standard.com/markets/news/gabriel-india-shares-rise-4-percent-motilal-oswal-initiates-coverage-with-buy-126060900240_1.html) |

---

## Stocks Considered But Not Added

| Ticker | Company | Reason not added |
|---|---|---|
| — | HAL (Hindustan Aeronautics) | Already in Nifty 500 base universe — filed as nifty_500, not news_discovery |
| — | L&T (Larsen & Toubro) | Already in Nifty 500 base universe — K9 Vajra-T contract will feed into next collection run |
| — | Susan Electricals | Only 1 distinct fundamental news source (bulk deal); price-action-only signal — does not meet 2-source fundamental threshold |

---

## Notable Themes Observed in News Sweep

These are not universe additions but inform the theme agent:

- **Defence manufacturing / export orders** — Multiple companies (Paras, HAL, L&T, Adani Defence, Tata Advanced Systems) appeared in context of ₹30,000 crore IAF UAV tender. Defence electronics supply chain showing broad order activity.
- **Industrial exports** — JNK India UAE order signals emerging Indian industrial export capability beyond IT/pharma.
- **Auto component re-rating** — Gabriel India analyst initiation points to structural transformation thesis in the auto ancillary space (EV adjacencies, sunroofs, solar dampers).

---

## Next Run Recommendation

- Set up NSE data API access to complete the remaining ~387 Nifty 500 companies.
- For the collection agent: prioritise HAL, LT, BEL, PARAS, JNKINDIA, GABRIEL for document collection — these have fresh fundamental catalysts this week.
