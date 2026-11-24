# Exploratory analysis

Script: `src/explore.py` (run with `.venv/bin/python src/explore.py`). Tables: `outputs/`. Full run: `outputs/analysis_run.txt`.
The analysis stops at FY2022. SEC figures are as filed by the 2023-03-31 cutoff. Census and BLS figures were downloaded in November 2026 and may include later revisions, so this is not strictly a March 2023 view.

## Findings by guiding question

**1. What broke?** Target's operating income fell $5.10B. Cost-of-goods rate −$5.06B, SG&A rate −$0.33B, depreciation rate +$0.03B, higher sales +$0.26B. The parts sum exactly.

**2. When?** Q1 −$1.03B (20%), **Q2 −$2.15B (42%)**, Q3 −$0.99B (19%), Q4 −$0.94B (18%). Two components: a cost-of-goods rate 2.8–4.3 points higher in every other quarter, and a Q2 spike (+8.7) worth about $1.4B beyond the other quarters' average rise. The split is descriptive, not causal.

**3. Why?** See hypotheses.

**4. Just Target?** Change in full-year operating margin: Target −4.9 points, Kohl's about −7.3, Walmart about −1.2. Cost-of-goods rate: Target +4.6, Kohl's +4.4 (mostly Q4: +9.9), Walmart +1.0. Walmart's SG&A jumped in Q3 (−$2.2B effect). Walmart's earnings releases explain it: $3.325B of opioid legal charges, recorded in Q3 ([Q3 release](https://corporate.walmart.com/content/dam/corporate/documents/press-center/walmart-releases-q3-fy23-earnings/q3-fy23-earnings-release.pdf)). [Its Q4 release](https://corporate.walmart.com/content/dam/corporate/documents/press-center/walmart-releases-q4-and-fy23-earnings/earnings-release-fy23-q4.pdf) also excludes $849M of reorganization and restructuring charges in Q4 FY2022 and $108M of restructuring charges in FY2021. Walmart's margin change is:

| | FY2021 | FY2022 | Change (points) |
|---|---|---|---|
| As reported | 4.5% ($25.94B) | 3.3% ($20.43B) | −1.2 |
| Excluding the opioid charges only | 4.5% | 3.9% | −0.6 |
| Walmart's adjusted operating income | 4.5% ($26.05B) | 4.0% ($24.60B) | −0.5 |

Both releases came out before the 2023-03-31 cutoff. Without the one-offs Walmart's drop is smaller, so the gap with Target is wider. The year-end accrual of $2.95B is lower than the charge; we haven't confirmed why. Target's 10-K shows no comparable adjustment to operating income; 

Kohl's −7.3 stands as reported. Its earnings releases ([FY2022](https://corporate.kohls.com/news/kohls-reports-fourth-quarter-and-full-year-fiscal-2022-financial-results), [FY2021](https://s204.q4cdn.com/271435555/files/doc_financials/2021/q4/Press-Release-Q4-2021-FINAL-1.pdf)) show no operating-level adjustments in either year; the only one, a $201M debt extinguishment loss in FY2021, falls below operating income. Its filings tag a $22M asset impairment in FY2022 that Kohl's didn't adjust for, about 0.1 points. Its Q4 FY2022 release also cites "proactive measures" for 2023, not sized as a one-off.

**5. Normal or broken?** By margin: $2.70B of the drop is the return to FY2019's margin and $2.66B is below it (+$0.26B from sales). **But the cost-of-goods rate did not return to normal:** 70.2% (FY2019), 70.7% (FY2021), 75.4% (FY2022). The FY2021 gain was in SG&A (20.8% → 18.6%) and depreciation (3.0% → 2.2%), and it largely held in FY2022. So "pandemic boost wearing off" is an arithmetic comparison, not the mechanism.

## Hypotheses

*Updated in validation: the H3 size, the H4 wording and the SG&A point are corrected in `05-validation.md`.*

| | Evidence for | Evidence against / limits | Verdict |
|---|---|---|---|
| H1 inventory and discounts | Inventory +43% / +36% against sales +4% / +4% in Q1–Q2; Q2 spike follows; inventory below the prior year by Q4; Kohl's shows a similar pattern with its spike in Q4 | Walmart's inventory rose 32% / 26% with only +1 point in cost rate. Target's cost rate was still +2.8 in Q4, when inventory was 3% below the prior year (though still 50% above FY2019, and 12% above it relative to sales, so it may not have fully cleared). Rate was already up in Q3–Q4 FY2021. Inventory/sales was 6–19% above FY2019, against 11–38% above a lean FY2021 in Q1–Q3. No markdown data | **Best fit for the Q2 spike; not enough for the rest** |
| H2 freight | Truckload PPI +35% / +28% in Q1–Q2, deep-sea +23–34% all year; fits a cost rate raised in every quarter | Truckload +2.7% by Q4, though levels stayed high. Walmart faced similar markets with +1 point. Target's freight spend isn't in the data, and these indexes miss ocean import contract rates | **Plausible for the persistent part; cannot be sized** |
| H3 mix shift | Discretionary stores −1.3% against essentials +6.6% in Q2 | Discretionary share fell only 1.0 point (33.8 → 32.8). At a 20-point margin gap (assumption) that is ~0.2 points of 4.6. Store types, not Target's own mix | **Weak directly; may be why stock went unsold (H1)** |
| H4 unpassed supplier prices | Home goods: PPI +8.5–12.3% against CPI +6.7–9.9%; food squeezed in Q1 only | Apparel PPI and CPI similar; import prices of consumer goods up only 0.5–3.1%; tests the market, not Target's prices | **Weak to modest** |

## What these findings don't show

- **Not proof of cause.** There is no markdown data, so the evidence can't show that discounting excess inventory caused the drop. H1 fits the Q2 spike best; it doesn't account for the rest.
- **Not fully blind or purely March 2023.** See the question and data-profile notes, and the data notes below.
- **Two peers, not an industry.** Two peers were chosen on purpose: one grocery-heavy (Walmart), one discretionary-heavy (Kohl's). They show direction, not an industry average. Product mix is only one difference between them: Kohl's sales also fell, and Walmart's reported result includes one-off charges (see question 4).

## Corrections to earlier notes

- "About half is a return to normal" (question notes) described the margin only; see question 5.
- "Most of the damage was in Q2": it was 42%.
- Target inventory was 50–68% above FY2019, not 40–50%, and peaked in Q3, not Q2. Kohl's revenue fell in all four FY2022 quarters.
- The cleaning notes' "identity holds exactly" is true by construction for Kohl's, because `other_operating` is the residual. Real tests: Target 14 quarters, Walmart 20, Kohl's 12 (FY2021–22 plus FY2023), all zero. The derived Target FY2020 quarters also sum to the reported annual figure.
- The −$129M Kohl's residual was matched to a $127M gain, but a $2M impairment runs the other way, so about $4M is unexplained. Kohl's "other" items were not all traced.

## Data notes

- FRED dropped automated connections, so prices come from BLS (`data/raw/bls`) and sales from Census (`data/raw/census`), the original sources. Census's inventory file was not available.
- BLS figures are also today's versions, and producer prices are revised after first release.
- Census figures are today's revised versions, not the March 2023 vintage, and are not adjusted for seasonality (year-over-year comparisons only). Store-based categories exclude online-only sellers.
