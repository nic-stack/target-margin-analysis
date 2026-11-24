# Framing the business question

## The brief

> It's early 2023. "Revenue grew last year, but operating profit fell by about half. Nobody can explain why. Find out."
> — CEO, Target Corporation

Target FY2022 (ended 2023-01-28): revenue up ~2.9% to ~$109.1B; operating income down from ~$8.95B to ~$3.85B.
*(Rough figures from an uncleaned pull of SEC data; confirmed during cleaning.)*

## Scope decisions

- **Companies:** Target, compared with Walmart (grocery-heavy) and Kohl's (apparel and home).
- **Baselines:** FY2021 (prior year) and FY2019 (pre-pandemic).
- **Measure:** operating income, split into the cost-of-goods rate, the running-costs (SG&A) rate and depreciation.
- **Detail:** quarterly, FY2019–FY2023. Q4 = full year minus Q1–Q3.
- **Information cutoff:** 2023-03-31. A later "what actually happened" epilogue grades the call.
- **Item 7 unread until validation:** Target's own explanation (10-K Item 7, MD&A) isn't read until then. This isn't a fully blind analysis: markdowns and freight were already known as likely causes, and so were the FY2023 margin and the fact that it never got back to 8.4%.
- **Data:** SEC EDGAR company facts (including company inventory); BLS for prices and freight, Census for category sales. FRED was planned, but it dropped automated connections.
- **Deliverable:** a diagnosis plus 2–3 evidence-backed actions. No forecast.

## Guiding questions

1. **What broke?** Break the $5.1B drop into its parts: higher sales, the cost-of-goods rate, the running-costs rate and depreciation. Which part matters most?
2. **When?** In which quarters of FY2022 did the operating margin fall the most compared with the same quarter of FY2021?
3. **Why?** What pushed the cost-of-goods rate up: excess inventory and discounting, freight costs, or a shift in what customers bought? Which one does the evidence support best?
4. **Just Target?** Did Walmart's and Kohl's operating margins fall as much as Target's over the same period? Do the differences line up with how much each sells groceries versus discretionary goods?
5. **Normal or broken?** How much of the margin drop is the FY2021 pandemic boost wearing off, and how much is Target falling below its FY2019 level?

## Notes from framing

- Cost of goods, SG&A and operating margin don't add to 100% of revenue; Target reports depreciation on a separate line (~2.3% of revenue), so Q1 must include it.
- Retail is seasonal, so quarters are compared year over year, never with the previous quarter.
- Public filings don't report markdowns directly. Q3 can show which explanation the evidence fits best, but can't prove one.
- Walmart names its fiscal years one year ahead of Target and Kohl's, so periods are matched by end date.
- Rough split for Q5: margin 8.4% (FY2021) → 3.5% (FY2022), against 6.0% in FY2019. That's about half "return to normal" and half "below normal". *(Later correction: this describes the overall margin only. The cost-of-goods rate did not return to normal; see `04-analysis.md`, question 5.)*
