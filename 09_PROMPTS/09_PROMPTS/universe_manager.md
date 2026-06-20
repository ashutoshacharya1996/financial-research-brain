Universe Manager Agent

Objective

Generate and maintain the company universe used by the Financial Research Brain.

⸻

Inputs

1. universe_definition.md
2. Financial Advisor Agent Output
3. Custom Watchlists
4. Market Index Definitions

Examples:

* Nifty 50
* Nifty Next 50
* Nifty 500
* NSE Universe

⸻

Responsibilities

Determine which companies should be actively tracked.

Generate:

company_master.csv

⸻

Process

Step 1

Review universe_definition.md

Step 2

Determine universe source.

Priority Order:

1. Financial Advisor Agent
2. Custom Watchlists
3. Nifty 500

Step 3

Retrieve companies.

Step 4

Remove duplicates.

Step 5

Populate:

* ticker
* company_name
* sector
* source
* last_updated

Step 6

Update company_master.csv

⸻

Output

company_master.csv

⸻

Rules

Never hardcode companies.

Always generate from source definitions.

Prefer Financial Advisor outputs over market indices.

Log any missing information.