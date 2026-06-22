Opportunity Discovery Engine

## Weekly Workflow

**Sunday (automatic, no AI, no API keys):**

A GitHub Action runs at 09:00 IST and executes `scripts/fetch_evidence.py` with two lanes:

```
Lane A — Company Evidence Fetch
  Reads: 01_UNIVERSE/company_master.csv where fetch_enabled=true
  Writes: 02_RAW_DOCUMENTS/<TICKER>/  (prices, news, filings)

Lane B — Discovery News Fetch
  Broad market queries (order wins, L1 bids, capex plans, defence acquisitions, etc.)
  Writes: 02_RAW_DOCUMENTS/_discovery/YYYY-MM-DD/discovery-news.md
  Does NOT modify the universe. Discovery News Agent reviews this on Monday.
```

**Monday (local, Claude Code):**

```
git pull
claude
```

Then run: `/weekly-run`

```
Step 1a: /discovery-news-agent   → reviews _discovery/, writes summary
Step 1b: /universe-manager       → updates 01_UNIVERSE/company_master.csv
Step 2:  extraction → delta → themes  (for fetch_enabled=true companies)
Step 3:  /opportunity-screener   → Top 10 + Top 3 + Portfolio Handoff
Step 4:  /investment-impact      → for Portfolio Handoff names only
```

**To add a company to the fetch cycle:**
Universe Manager is the only agent that updates `01_UNIVERSE/company_master.csv`. Run `/universe-manager` and name the company, or let it be surfaced through the Discovery News Agent.

**Canonical universe file:** `01_UNIVERSE/company_master.csv` — do not maintain `data/company_master.csv` separately.

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
Portfolio Handoff              ← identifies 3 candidates for deeper review
      ↓
Investment Impact Agent       ← fact-checks signals, gates underwriting effort
      ↓
Investment Impact Notes       ← routing decision: Deep Dive / Watchlist / Track / Ignore
      ↓
India Stock Picker            ← valuation + quality gates (if Impact notes flags for review)
      ↓
Portfolio Fit Check           ← personal allocation decision
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

Organized by:

Company → Year → Quarter

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

Handoff zone between research discovery and investment decisions.

Contains:

* Weekly Portfolio Handoff (3 candidates for Investment Impact review)
* Investment Impact Notes (fact-checked signals, underwriting gates, routing decisions)
* Weekly ELI15 brief (human-readable summary)
* Stock dashboards (reference link to latest India Stock Picker output)

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

Agent 0 – Discovery News Agent

Reviews raw discovery output from Lane B (`02_RAW_DOCUMENTS/_discovery/`). Classifies signals by source tier (Tier 1–4). Surfaces new company candidates and risk alerts for Universe Manager review. **Cannot modify `01_UNIVERSE/company_master.csv`.** Trigger: `/discovery-news-agent`.

⸻

Agent 1 – Universe Manager

The **sole agent authorised to update `01_UNIVERSE/company_master.csv`**. Reads Discovery News Agent summary, evaluates signals against promotion/deprioritization rules, and decides universe membership. Sets `active_universe`, `fetch_enabled`, `status`, `priority`. Trigger: `/universe-manager`.

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
* Portfolio Handoff (3 names for deeper review)
* Updated Opportunity Records in `07_OPPORTUNITIES/active/`

⸻

Agent 6.5 – Investment Impact Agent

Fact-checks Portfolio Handoff signals, assesses underwriting impact, and gates whether India Stock Picker deep dive is warranted.

Decision types:

* Re-run India Stock Picker (Deep Dive)
* Upgrade Watchlist Priority
* Keep Tracking
* Ignore For Now

Output: Investment Impact Notes in `08_PORTFOLIO_INPUTS/investment-impact/`

Key rules:
* **Positive signals cannot override failed quality gates, weak cash conversion, valuation flags, or portfolio constraints.**
* **This agent never outputs Buy / Sell / Add / Exit.** Routing decision only.

⸻

Agent 7 – India Stock Picker

Runs on-demand when triggered by Investment Impact notes flagged for "Deep Dive" or "Upgrade Watchlist."

Evaluates: Valuation gates (fair value, buy zones), quality gates (delivery track record, cash conversion), and portfolio fit.

⸻

Agent 8 – Portfolio Fit / Financial Advisor

Runs on-demand after India Stock Picker clears gates.

Assesses: FIRE horizon alignment, portfolio slot availability, personal biases, holdings overlap.

Final decision: Add / Hold / Avoid

⸻

Agent 9 – Market Intelligence Agent

Monitors external sources and industry developments.

⸻

Agent 10 – Research Committee Agent

Challenges conclusions and seeks contradictory evidence (run as needed, not weekly).

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