Company Universe

This folder contains the master company universe tracked by the Financial Research Brain.

The company universe serves as the source of truth for all downstream agents.

Agents should never use hardcoded company lists.

All company-level activities must reference company_master.csv.

The universe will initially contain Nifty 500 companies and may later expand to the broader NSE universe.

Responsibilities:

* Company metadata
* Sector classification
* NSE identifiers
* BSE identifiers
* Investor Relations URLs
* Tracking status

Downstream Dependencies:

* Collection Agent
* Extraction Agent
* Delta Agent
* Theme Agent
* Market Intelligence Agent