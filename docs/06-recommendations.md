# So what?

Written as of early 2023, for the CEO. Gap test: `src/gap_backtest.py` → `outputs/gap_backtest.csv`. Trigger levels: `src/gap_history.py` → `outputs/gap_history*.csv`.

## The answer in one paragraph

Operating income fell $5.10B, and the higher cost-of-goods rate accounts for $5.06B of it. Excess inventory cleared with discounts best explains the Q2 spike, and is one of several causes over the full year. Inventory began building in FY2021. Demand shifted, but in our judgment that build and early ordering left Target more exposed.

## Actions

### A. Review inventory when it outruns sales (first)

> I'd have Target compare how fast stock is growing with how fast sales are growing, every quarter. If stock is growing more than **10 points** faster, look at why, by category. Above **15 points**, review before placing new Discretionary orders. Before the pandemic, Target's gap never passed 12.2 in 43 quarters, so 15 is unusual. It's a prompt to ask questions, not a prediction: Walmart passed 15 and its cost rate rose only about 1 point.

A closed gap doesn't mean margins have recovered.

The gap is inventory growth minus sales growth, each against the same quarter a year earlier.

| Gap (points) | Q1 FY21 | Q2 FY21 | Q3 FY21 | Q4 FY21 | Q1 FY22 | Q2 FY22 | Q3 FY22 | Q4 FY22 |
|---|---|---|---|---|---|---|---|---|
| Target | −0.6 | 17.3 | 4.3 | 21.1 | 39.1 | 32.6 | 11.1 | −4.2 |
| Walmart | 9.8 | 13.8 | 6.6 | 25.2 | 29.7 | 17.1 | 3.8 | −7.2 |
| Kohl's | −85.1 | −29.2 | −14.6 | 12.6 | 44.5 | 55.7 | 40.8 | 11.4 |

**Why 10 and 15.** There is no industry standard behind them. They come from what was normal over 43 quarters before the pandemic (mid-2009 to early 2020):

| | Median gap | Largest gap | Above 10 | Above 15 | Above 20 |
|---|---|---|---|---|---|
| Target | 0.9 | 12.2 | 4 | 0 | 0 |
| Walmart | −0.2 | 9.0 | 0 | 0 | 0 |
| Kohl's | 1.7 | 15.7 | 4 | 1 | 0 |

An earlier draft used 20, picked after seeing the results. Questioning that choice led to this check.

- **For:** at 15, Target was flagged in Q2 FY2021, four quarters before its worst cost-rate rise (+8.7 points, Q2 FY2022), and again in Q4 FY2021 through Q2 FY2022. Kohl's was flagged in Q1 FY2022, three quarters before its worst (+9.9, Q4).
- **Mixed record before the pandemic:** Target's four gaps above 10 came in three episodes. Two (Q4 FY2013 and Q2 FY2016) were followed within four quarters by a cost-rate rise of 1.3 points, the largest in the period. The other (Q3–Q4 FY2018) saw at most 0.5. Other events, such as the 2013 data breach, may explain some of this.
- **The Q2 FY2021 flag may be restocking:** a year earlier inventory had fallen 2.7% while sales rose 24.7%, which makes the gap look larger.
- **Against:** Walmart's gap was larger than Target's in Q4 FY2021, yet its cost rate rose at most 1.2 points. Target's gap fell to 4.3 in Q3 FY2021 before jumping again. Kohl's was also flagged in Q1 FY2020, when sales fell 41%.
- **Limits:** three companies. The levels rest on pre-pandemic history, but the choice of exactly 10 and 15 was made knowing the FY2021–FY2022 results. They are set for Target; other companies would need their own. Quarter-end company totals; the category review needs internal data.

### B. Commit to Discretionary stock in smaller amounts and later, especially owned brands

> I'd have Target commit to Discretionary goods in smaller amounts and later, especially its owned brands, which take longer to arrive. In 2022, Discretionary sales fell 3.4% while everyday categories grew 10.3%, so large early orders were a risk. The trade-off is possibly higher unit costs or some items running out.

- **For:** Discretionary sales fell 3.4% while Frequency sales rose 10.3% (Note 3). Owned brands, about a third of sales, generally need longer lead times and earlier ownership (Risk Factors).
- **Already in place:** purchase orders are cancellable by their terms, though Target may owe vendors unrecoverable outlays (Note 14). Target also cancelled orders and reduced Discretionary stock in 2022. So the change is committing less up front, not adding a right to cancel.
- **Cost:** may raise unit costs or cause stockouts. Owned brands generally carry higher margins than equivalent national brands, so cutting too far has a price.

### C. Show the CEO what each cause cost

> I'd give the CEO a quarterly breakdown of the cost increase: markdowns, freight, theft and loss, distribution, and product costs. Target's annual report names the causes but doesn't say how much each one cost. Without that split, it's hard to know what to fix first or whether A and B worked. Target may already track some of this internally, so the first step is to check what exists.

- **What:** split the cost-rate change each quarter into markdowns, freight, shrink, distribution costs and product cost net of price increases.
- **For:** the 10-K names these causes but sizes none of them, and Target's cost rate was still 2.8 points higher in Q4, when inventory was below the prior year.
- **Limit:** Target's accounting already uses markdowns and shrink estimates, so internal reporting may exist. The gap may only be in what is public.

A says when to look, B says what to change, and C shows whether it worked.

## Scale, not savings

One point of cost rate on FY2022 revenue is about $1.09B. Q2's cost-rate rise beyond the other quarters' average was worth about $1.36B. These show what was at stake. They don't estimate what the actions would recover.

## Not recommended

**Reviewing distribution center pay, headcount and new facilities.** Target names them as a margin pressure, but we can't size it and some may be long-term investment. C would show whether it matters.
