Opportunity Discovery Engine

## Weekly Workflow

Current rule: Sunday runs collection only. Lane A fetches companies where
`fetch_enabled=true`; Lane B writes discovery evidence under
`02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/`. Universe Manager updates
`01_UNIVERSE/company_master.csv` later on Monday.

**Sunday (automatic):** A GitHub Action runs at 09:00 IST. It fetches prices, news, and exchange filings for companies where `fetch_enabled=true`, and also runs broad discovery collection using `scripts/fetch_evidence.py` - no AI, no API keys. Evidence is committed to `02_RAW_DOCUMENTS/`.

**Monday+ (local):** Pull the new evidence and run the AI pipeline locally:

```
git pull
claude
```

Then say: _"New evidence is in. Run extraction, discovery summary, Universe Manager, delta, themes, opportunity screener, and weekly brief. Skip only the collection step."_

Universe Manager runs on Monday after the discovery summary is generated from
`02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/`. It is the step that updates
`01_UNIVERSE/company_master.csv`. Sunday collection does not directly promote,
deprioritize, or remove companies.

Claude Code processes extraction â†’ delta â†’ themes â†’ opportunity screener â†’ weekly brief and commits the outputs.

If a stock from the weekly report looks investment-relevant, run the Investment
Impact layer before any stock-selection work:

```
Run investment impact notes for the top handoff names from this week's report.
```

This creates files in `08_PORTFOLIO_INPUTS/investment-impact/`. Those notes are
the bridge into India Stock Picker review. They are not buy/sell decisions.

To add a company to the fetch cycle: add or update the row in
`01_UNIVERSE/company_master.csv` and set `fetch_enabled: true`.

---

Mission

Build a machine that continuously narrows the market down to the few opportunities most likely to make money.

The system ingests company disclosures, earnings calls, exchange filings, industry reports, and market intelligence. It synthesizes that into a single weekly output: which stocks are worth researching right now, and why.

The central object is not a company. It is not a theme. It is an **Opportunity** â€” defined as:

```
Theme + Evidence + Candidate Stocks + Timing + Risk
```

Every Sunday, the system produces exactly two outputs:

1. **Top 10 Stocks Worth Researching** â€” the research queue for the week, grounded in specific evidence from the prior weekâ€™s documents
2. **Top 3 High-Conviction Opportunities** â€” conviction-stage convergences of theme acceleration, cross-company corroboration, and near-term catalysts

The output feeds a separate stock-selection and portfolio construction process. The systemâ€™s job is not to pick stocks. Its job is to continuously narrow the universe to where the evidence is pointing.

â¸»

System Architecture

Internet Sources
      â†“
Collection Agent
      â†“
Document Repository
      â†“
Extraction Agent
      â†“
Delta Analysis Agent
      â†“
Theme Detection Agent
      â†“
Opportunity Screener          â† produces the weekly Top 10 + Top 3
      â†“
Weekly Opportunity Report
      â†“
Investment Impact Layer       â† translates signals into underwriting triggers
      â†“
Market Intelligence Agent
      â†“
Research Brief Generator
      â†“
Portfolio Intelligence Output

â¸»

Research Universe

Initial Target Universe:

* Nifty 500 companies

Future Expansion:

* Entire NSE universe
* Global companies of strategic relevance
* Industry reports
* Macroeconomic sources
* Alternative data sources

â¸»

Repository Structure

financial-research-brain
00_SYSTEM
01_UNIVERSE
02_RAW_DOCUMENTS
03_EXTRACTED_DATA
04_COMPANY_ANALYSIS
05_SECTOR_ANALYSIS
06_THEMES
07_OPPORTUNITIES
08_PORTFOLIO_INPUTS
09_PROMPTS
10_AUTOMATION

â¸»

Folder Definitions

00_SYSTEM

System standards, operating procedures, architecture documentation, data dictionaries, and governance rules.

Examples:

* Research standards
* Naming conventions
* Operating manuals
* System architecture

â¸»

01_UNIVERSE

Master company universe and metadata.

Examples:

* Nifty 500 universe
* Sector classifications
* Company mappings
* Investor relations links
* NSE/BSE identifiers

â¸»

02_RAW_DOCUMENTS

Original source documents collected by the system.

Examples:

* Investor presentations
* Earnings call transcripts
* Annual reports
* Exchange filings
* Press releases
* Evidence indexes and retrieval failure metadata

Organized by:

Company â†’ Year â†’ Quarter

Collection principle:

* Sunday collection has two lanes: company-specific evidence for rows where
  `fetch_enabled=true`, and discovery-wide news for fresh ideas outside the
  tracked list.
* No individual website is mandatory. NSE/BSE are valuable evidence sources,
  but not dependencies; Google News RSS is a detector, not proof.
* Material signals should be corroborated through company IR, press releases,
  credit rating agencies, exchange metadata/filings, or credible media.
* Source retrieval is fallible. If a source blocks, times out, returns a
  paywall, or serves an invalid file, the workflow records metadata and failure
  reason instead of stopping.
* For each company, `evidence-index.jsonl` is the machine-readable audit trail.
  Raw PDFs and text snapshots are local evidence for extraction, not permanent
  archives.
* Raw files may be removed after successful extraction and retention checks;
  extracted knowledge, metadata, URLs, hashes, and failure reasons remain.
* Discovery-wide news is saved to
  `02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/evidence-index.jsonl` and
  `discovery-news.md` for Universe Manager review.

Universe status principle:

* `candidate_watch` means interesting but unproven, with `fetch_enabled=false`.
* `active` and `high_priority` mean evidence-backed enough for weekly fetch,
  with `fetch_enabled=true`.
* `deprioritized` means the signal faded or the thesis weakened, with
  `fetch_enabled=false`.

â¸»

03_EXTRACTED_DATA

Structured information extracted from source documents.

Examples:

* Revenue
* Margins
* Guidance
* Capex
* Order books
* Management commentary
* Risk statements

â¸»

04_COMPANY_ANALYSIS

Company-level analysis outputs.

Examples:

* Quarter-over-quarter comparisons
* Annual comparisons
* Change detection reports
* Management sentiment analysis

â¸»

05_SECTOR_ANALYSIS

Sector-level intelligence.

Examples:

* IT sector trends
* Banking trends
* Defence trends
* Industrials trends
* Consumer demand trends

â¸»

06_THEMES

Cross-company thematic analysis.

Examples:

* AI infrastructure
* Defence exports
* Manufacturing capex cycle
* Data center expansion
* Energy transition

Each theme should contain:

* Description
* Evidence
* Beneficiaries
* Risks
* Confidence score
* Trend direction

â¸»

07_OPPORTUNITIES

The primary output of the Opportunity Discovery Engine.

Contains:

* Weekly Opportunity Reports (Top 10 + Top 3), one file per Sunday
* Active Opportunity Records, one file per live opportunity
* Opportunity schema and weekly report template

â¸»

08_PORTFOLIO_INPUTS

Outputs consumed by the portfolio and stock-selection systems.

Examples:

* Theme rankings
* Opportunity lists
* Risk alerts
* Sector scorecards
* Company watchlists
* Investment Impact notes that bridge opportunity signals into underwriting

Rule:

* A positive Opportunity signal can create a handoff.
* Only the India Stock Picker can create a Buy / Watchlist / Pass verdict.
* Only Portfolio Fit can convert a Buy candidate into an actual portfolio action.

â¸»

09_PROMPTS

Prompt library used by all agents.

Examples:

* Collection prompts
* Extraction prompts
* Theme detection prompts
* Delta analysis prompts

â¸»

10_AUTOMATION

Automation logic and workflows.

Examples:

* GitHub Actions
* Scheduled jobs
* Collection workflows
* Update processes

â¸»

Agent Framework

Agent 1 â€“ Universe Manager

Maintains company universe and metadata.

â¸»

Agent 2 â€“ Collection Agent

Discovers and archives:

* NSE filings
* BSE filings
* Investor relations documents
* Earnings materials

â¸»

Agent 3 â€“ Extraction Agent

Converts unstructured documents into structured data.

â¸»

Agent 4 â€“ Delta Agent

Identifies changes versus prior periods.

Focus:

* Demand
* Margins
* Guidance
* Risks
* Capex
* Sentiment

â¸»

Agent 5 â€“ Theme Agent

Identifies recurring themes across companies and sectors.

â¸»

Agent 6 â€“ Opportunity Screener

Runs every Sunday. Synthesizes theme signals, delta outputs, and evidence weight into ranked Opportunities.

Outputs:

* Top 10 Stocks for the Research Queue
* Top 3 High-Conviction Opportunities
* Updated Opportunity Records in `07_OPPORTUNITIES/active/`
* Portfolio Handoff candidates for Investment Impact notes

â¸»

Agent 6.5 â€“ Investment Impact Agent

Bridges Opportunity Discovery to stock selection.

Purpose:

* Fact-check the specific signal
* Map the impact to growth, margins, cash conversion, moat, valuation, and portfolio fit
* Identify buy blockers
* Decide whether to re-run the India Stock Picker, upgrade watchlist priority, keep tracking, or ignore

Hard rule: this agent never outputs Buy / Sell / Add / Exit.

â¸»

Agent 7 â€“ Market Intelligence Agent

Monitors external sources and industry developments.

â¸»

Agent 8 â€“ Research Committee Agent

Challenges conclusions and seeks contradictory evidence.

Purpose:

* Reduce confirmation bias
* Surface key risks
* Identify thesis breakers

â¸»

Research Principles

1. Primary sources take precedence over news sources.
2. Focus on changes rather than summaries.
3. Evidence must be traceable to source documents.
4. Themes require cross-company validation.
5. Contradictory evidence must always be documented.
6. Research outputs should be reusable across future analyses.
7. Every insight should answer: â€œWhy does this matter for investors?â€

â¸»

Long-Term Objective

Create a continuously improving research intelligence system capable of identifying emerging market themes before they become consensus and delivering structured evidence-based insights to downstream investment decision systems.
