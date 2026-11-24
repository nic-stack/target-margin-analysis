# Data profile and hypotheses

## What's in the data

Source: SEC EDGAR company facts (XBRL), one file per company in `data/raw/`.
`src/load_facts.py` flattens them into `data/interim/facts_long.csv` (70,115 rows, one per reported number).
`src/profile_facts.py` profiles the lines the guiding questions need (FY2019–FY2023).

| | Target | Walmart | Kohl's |
|---|---|---|---|
| Revenue | `RevenueFromContractWithCustomer…` | same, plus `Revenues` (includes membership and other income) | same |
| Cost of goods | `CostOfGoodsAndServicesSold` | `CostOfRevenue` | `CostOfGoodsAndServicesSold` |
| SG&A | `SellingGeneralAndAdministrativeExpense` | same | same |
| Depreciation | separate line | **not a separate line** (inside cost of goods / SG&A) | separate line |
| Operating income | `OperatingIncomeLoss` | same | same |
| Inventory | `InventoryNet` (quarter-end) | same | same |
| Fiscal year ends | late Jan / early Feb | Jan 31 | late Jan / early Feb |

## Data issues found (handled in cleaning)

1. **No standalone Q4.** Filings report Q1–Q3 and the full year, so Q4 = full year − Q1–Q3.
2. **Each number appears several times.** 545 of 583 periods are repeated because later filings repeat earlier periods as comparatives. Need one rule for which copy to keep.
3. **Restatement.** Target's FY2022 cost of goods was $82.229B in the 10-K filed 2023-03-08, then $82.306B in the 10-K filed 2025-03-12 ($77M moved from SG&A into cost of goods). Under the 2023-03-31 cutoff we use the original figure.
4. **Missing quarters.** Target's 10-Qs from Q1 FY2020 to Q2 FY2021 don't tag cost of goods at all, including the FY2021 quarters that FY2022 is compared with. It can be derived as revenue − SG&A − depreciation − operating income. That identity has to be verified on quarters where all four are reported.
5. **Walmart depreciation isn't broken out,** so its cost-of-goods and SG&A rates aren't strictly comparable with Target's. Compare operating margin directly, and treat the component rates as directional only.
6. **Walmart's fiscal-year labels** run one year ahead. Periods are matched by end date.

## First signal from the profile

Target's quarterly operating income (uncleaned, $B):

| Quarter ending | FY2021 | FY2022 |
|---|---|---|
| Q1 (Apr/May) | 2.37 | 1.35 |
| Q2 (Jul) | 2.47 | **0.32** |
| Q3 (Oct) | 2.01 | 1.02 |

The drop isn't spread evenly: Q2 FY2022 is where profit nearly vanished (The analysis later showed Q2 was 42% of the full-year drop). This bears on guiding question 2.

## Hypotheses

Chosen to pursue (all aimed at guiding question 3, "what pushed the cost-of-goods rate up?"):

| # | Hypothesis | Supported if… | Data |
|---|---|---|---|
| H1 | Too much inventory, cleared with discounts | Inventory grew much faster than sales, then the cost-of-goods rate jumped | SEC inventory and sales |
| H2 | Freight and shipping costs | Freight prices peaked in 2022, and Walmart's and Kohl's cost rates also rose | BLS freight price indexes, comparison companies |
| H3 | Customers bought cheaper things (fewer discretionary goods, more groceries and essentials) | Census sales moved toward essentials, and the companies most exposed to discretionary goods were hit hardest | Census sales by category, Kohl's vs. Walmart |
| H4 | Suppliers raised prices but Target didn't raise its own | Wholesale prices rose faster than consumer prices in Target's categories | Producer vs. consumer price indexes (BLS) |

Not pursued as hypotheses:
- **Running costs (SG&A) and the pandemic boost wearing off** are still measured, because guiding questions 1 and 5 already cover them.
- **Shrink (theft/loss) and one-off charges** go in the limitations section. Public data can't test shrink, and the only one-off found so far is a $77M restatement.

The four hypotheses can all be true at once. The aim is to size how much each one contributed, not to pick a single winner.

## Analyst's prediction (recorded 2026-11-19, before further analysis)

**H1, too much inventory cleared with discounts, is the most likely cause.** This is checked against the evidence in the analysis and against Target's own explanation in validation.

Note: this prediction was not fully blind. Inventory markdowns and freight were already known as publicly cited causes, and so were the FY2023 margin and the fact that it never got back to 8.4%.
