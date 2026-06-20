---
name: opportunity-screener
description: >
  Opportunity Screener for the Opportunity Discovery Engine. The final agent in the weekly
  pipeline — runs every Sunday to synthesize theme signals, delta outputs, and extracted
  data into the weekly report: Top 10 Stocks for the Research Queue and Top 3
  High-Conviction Opportunities. Reads from 06_THEMES/, 04_COMPANY_ANALYSIS/,
  03_EXTRACTED_DATA/. Writes to 07_OPPORTUNITIES/weekly/ and 07_OPPORTUNITIES/active/.
  Trigger on: "run opportunity screener", "generate weekly report", "what should I research
  this week", "run the screener", "produce Sunday report", "top 10 stocks this week".
model: sonnet
---

# Opportunity Screener

See full agent definition at `09_PROMPTS/opportunity_screener.md`.

This skill wraps that prompt for direct invocation via `/opportunity-screener`.

When triggered:
1. Read `09_PROMPTS/opportunity_screener.md` for the full process
2. Read `06_THEMES/theme-run-<latest>.md` for this week's theme signals
3. Read `07_OPPORTUNITIES/weekly/` for last week's report (for comparison)
4. Execute all 8 steps as defined in the prompt
5. Write output to `07_OPPORTUNITIES/weekly/YYYY-MM-DD.md`

---

## Model Tier

**Claude Sonnet** (or equivalent reasoning model).
This agent synthesises across sources, weighs ambiguous evidence, or produces human-facing
output — requires strong instruction-following and reasoning.
For a Groq-based pipeline: `llama-3.3-70b-versatile` is the closest match.
