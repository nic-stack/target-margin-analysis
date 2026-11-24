# Cleaning

**Output:** `data/clean/quarterly.csv`. It has 60 rows (3 companies × FY2019–FY2023 × 4 quarters), with revenue, cost of goods, SG&A, depreciation, other operating items, operating income and quarter-end inventory (current and year-ago).
**Script:** `src/clean_quarterly.py` (input: `data/interim/facts_long.csv` from `src/load_facts.py`).

## Cleaning rules

| Issue | Rule |
|---|---|
| Each number reported several times (later filings repeat earlier periods) | Keep the latest version filed on or before **2023-03-31**, which is what an analyst saw then. Periods first reported after the cutoff (FY2023 epilogue) use their original filing. |
| Target FY2022 restated in 2025 (cost of goods $82.229B → $82.306B) | Covered by the cutoff rule: we use **$82.229B**, as filed in March 2023. |
| No standalone Q4 | Q4 = full year − nine-month year-to-date. Other missing quarters = difference of year-to-date figures. |
| Target cost of goods not tagged in six quarters (FY2020 Q1–Q4, FY2021 Q1–Q2) | Derived as revenue − SG&A − depreciation − operating income. **Verified first:** the identity is exactly $0 on all 14 quarters where every line is reported. |
| Kohl's FY2019 10-K mis-dates its quarters by 1–2 days (e.g. 2019-05-02 vs 2019-05-04) | Quarter dates come from 10-Qs only. Amounts are identical. |
| Kohl's has extra operating lines in FY2019–FY2020 (impairments, store closings, a $127M real-estate gain in Q2 FY2020) | Kept as `other_operating`, so revenue − all costs = operating income holds for every company. Zero for Kohl's from FY2021 onward. |
| Walmart: fiscal-year names run one year ahead | Every fiscal year is labelled by the calendar year it starts in. Walmart "FY2023" (Feb 2022–Jan 2023) = FY2022 here. |
| Walmart: two revenue figures | `revenue` = total revenues incl. membership and other income, consistent with operating income. `net_sales` kept separately. |
| Walmart: no separate depreciation line | Depreciation sits inside cost of goods and SG&A. Walmart's component rates are **not directly comparable** with Target's and Kohl's; compare operating margin directly. |
| Target's FY2018 quarters use an older revenue label | Table starts at FY2019. Year-ago inventory for FY2019 comes from the prior-year balance sheets reported in the 10-Qs. |

## Checks passed

- **Identity:** revenue − cost of goods − SG&A − depreciation = operating income. Zero residual for Target (14 fully reported quarters), Walmart (20) and Kohl's from FY2021 (12). Kohl's FY2019–FY2020 holds only because `other_operating` is the residual.
- **Annual totals:** for every company and line, the four quarters add up to the 10-K annual figure within $2M (rounding).
- **No gaps:** no missing values, except depreciation for Walmart (by design).

## Caveats to carry forward

- **53-week years:** Target's and Kohl's FY2023 had 53 weeks (Target's Q4 was 14 weeks). FY2023 growth rates are slightly flattered; this only affects the epilogue.
- **Target's cost of goods** for FY2020–Q2 FY2021 is derived, not reported. It's exact by the verified identity, but it isn't a directly reported figure.

## Clean annual summary (% of revenue)

| Company | FY | Revenue $B | Op. income $B | Op. margin | Cost of goods | SG&A | Depreciation |
|---|---|---|---|---|---|---|---|
| Target | 2019 | 78.1 | 4.66 | 6.0% | 70.2% | 20.8% | 3.0% |
| Target | 2021 | 106.0 | 8.95 | 8.4% | 70.7% | 18.6% | 2.2% |
| Target | 2022 | 109.1 | 3.85 | 3.5% | 75.4% | 18.9% | 2.2% |
| Walmart | 2019 | 524.0 | 20.57 | 3.9% | 75.3% | 20.8% | n/a |
| Walmart | 2021 | 572.8 | 25.94 | 4.5% | 74.9% | 20.6% | n/a |
| Walmart | 2022 | 611.3 | 20.43 | 3.3% | 75.9% | 20.8% | n/a |
| Kohl's | 2019 | 20.0 | 1.10 | 5.5% | 60.8% | 28.6% | 4.6% |
| Kohl's | 2021 | 19.4 | 1.68 | 8.6% | 58.9% | 28.2% | 4.3% |
| Kohl's | 2022 | 18.1 | 0.25 | 1.4% | 63.3% | 30.9% | 4.5% |
