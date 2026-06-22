Opportunity Discovery Engine

## Weekly Workflow

**Sunday (automatic):** A GitHub Action runs at 09:00 IST. It fetches prices, news, and exchange filings for all active companies using `scripts/fetch_evidence.py` — no AI, no API keys. Raw evidence is committed to `02_RAW_DOCUMENTS/<TICKER>/`.

**Monday+ (local):** Pull the new evidence and run the AI pipeline locally:

```
git pull
claude
```

Then say: _"New evidence is in. Run the pipeline from extraction onwards. Skip universe discovery and collection."_

Claude Code processes extraction → delta → themes → opportunity screener → weekly brief and commits the outputs.

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

The central object is not a company. It is not a theme. It is an **Opportunity** — defined as:

```
Theme + Evidence + Candidate Stocks + Timing + Risk
```

Every Sunday, the system produces exactly two outputs:

1. **Top 10 Stocks Worth Researching** — the research queue for the week, grounded in specific evidence from the prior week’s documents
2. **Top 3 High-Conviction Opportunities** — conviction-stage convergences of theme acceleration, cross-company corroboration, and near-term catalysts

The output feeds a separate stock-selection and portfolio construction process. The system’s job is not to pick stocks. Its job is to continuously narrow the universe to where the evidence is pointing.

⸻

System Architecture

Internet Sources
      ↓
Collection Agent
      ↓
Document Repository
      ↓
Extraction Agent
      ↓
Delta Analysis Agent
      ↓
Theme Detection Agent
      ↓
Opportunity Screener          ← produces the weekly Top 10 + Top 3
      ↓
Weekly Opportunity Report
      ↓
Investment Impact Layer       ← translates signals into underwriting triggers
      ↓
Market Intelligence Agent
      ↓
Research Brief Generator
      ↓
Portfolio Intelligence Output

⸻

Research Universe

Initial Target Universe:

* Nifty 500 companies

Future Expansion:

* Entire NSE universe
* Global companies of strategic relevance
* Industry reports
* Macroeconomic sources
* Alternative data sources

⸻

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

⸻

Folder Definitions

00_SYSTEM

System standards, operating procedures, architecture documentation, data dictionaries, and governance rules.

Examples:

* Research standards
* Naming conventions
* Operating manuals
* System architecture

⸻

01_UNIVERSE

Master company universe and metadata.

Examples:

* Nifty 500 universe
* Sector classifications
* Company mappings
* Investor relations links
* NSE/BSE identifiers

⸻

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

Company → Year → Quarter

Collection principle:

* Source retrieval is fallible. If a source blocks, times out, returns a
  paywall, or serves an invalid file, the workflow records metadata and failure
  reason instead of stopping.
* For each company, `evidence-index.jsonl` is the machine-readable audit trail.
  Raw PDFs and text snapshots are local evidence for extraction, not permanent
  archives.
* Raw files may be removed after successful extraction and retention checks;
  extracted knowledge, metadata, URLs, hashes, and failure reasons remain.

⸻

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

⸻

04_COMPANY_ANALYSIS

Company-level analysis outputs.

Examples:

* Quarter-over-quarter comparisons
* Annual comparisons
* Change detection reports
* Management sentiment analysis

⸻

05_SECTOR_ANALYSIS

Sector-level intelligence.

Examples:

* IT sector trends
* Banking trends
* Defence trends
* Industrials trends
* Consumer demand trends

⸻

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

⸻

07_OPPORTUNITIES

The primary output of the Opportunity Discovery Engine.

Contains:

* Weekly Opportunity Reports (Top 10 + Top 3), one file per Sunday
* Active Opportunity Records, one file per live opportunity
* Opportunity schema and weekly report template

⸻

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

⸻

09_PROMPTS

Prompt library used by all agents.

Examples:

* Collection prompts
* Extraction prompts
* Theme detection prompts
* Delta analysis prompts

⸻

10_AUTOMATION

Automation logic and workflows.

Examples:

* GitHub Actions
* Scheduled jobs
* Collection workflows
* Update processes

⸻

Agent Framework

Agent 1 – Universe Manager

Maintains company universe and metadata.

⸻

Agent 2 – Collection Agent

Discovers and archives:

* NSE filings
* BSE filings
* Investor relations documents
* Earnings materials

⸻

Agent 3 – Extraction Agent

Converts unstructured documents into structured data.

⸻

Agent 4 – Delta Agent

Identifies changes versus prior periods.

Focus:

* Demand
* Margins
* Guidance
* Risks
* Capex
* Sentiment

⸻

Agent 5 – Theme Agent

Identifies recurring themes across companies and sectors.

⸻

Agent 6 – Opportunity Screener

Runs every Sunday. Synthesizes theme signals, delta outputs, and evidence weight into ranked Opportunities.

Outputs:

* Top 10 Stocks for the Research Queue
* Top 3 High-Conviction Opportunities
* Updated Opportunity Records in `07_OPPORTUNITIES/active/`
* Portfolio Handoff candidates for Investment Impact notes

⸻

Agent 6.5 – Investment Impact Agent

Bridges Opportunity Discovery to stock selection.

Purpose:

* Fact-check the specific signal
* Map the impact to growth, margins, cash conversion, moat, valuation, and portfolio fit
* Identify buy blockers
* Decide whether to re-run the India Stock Picker, upgrade watchlist priority, keep tracking, or ignore

Hard rule: this agent never outputs Buy / Sell / Add / Exit.

⸻

Agent 7 – Market Intelligence Agent

Monitors external sources and industry developments.

⸻

Agent 8 – Research Committee Agent

Challenges conclusions and seeks contradictory evidence.

Purpose:

* Reduce confirmation bias
* Surface key risks
* Identify thesis breakers

⸻

Research Principles

1. Primary sources take precedence over news sources.
2. Focus on changes rather than summaries.
3. Evidence must be traceable to source documents.
4. Themes require cross-company validation.
5. Contradictory evidence must always be documented.
6. Research outputs should be reusable across future analyses.
7. Every insight should answer: “Why does this matter for investors?”

⸻

Long-Term Objective

Create a continuously improving research intelligence system capable of identifying emerging market themes before they become consensus and delivering structured evidence-based insights to downstream investment decision systems.
