Universe Definition

Purpose

The company universe should be generated dynamically.

The system must not rely on manually maintained company lists.

⸻

Universe Priority

Priority 1:
Financial Advisor Agent Output

Priority 2:
Custom Watchlists

Priority 3:
Nifty 500 Constituents

⸻

Default Behaviour

If no Financial Advisor output exists:

Use Nifty 500.

If Financial Advisor output exists:

Use all companies under active coverage.

Remove duplicates.

Generate company_master.csv automatically.

⸻

Generated Output

company_master.csv

Fields:

* ticker
* company_name
* sector
* source
* last_updated

⸻

Future Enhancements

Additional metadata may include:

* NSE Symbol
* BSE Code
* Industry
* Market Cap
* Investor Relations URL
* Coverage Status