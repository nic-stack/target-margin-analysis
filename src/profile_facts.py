"""Profile: what's in the SEC data for the lines our questions need.

Usage: python3 -I src/profile_facts.py data/interim/facts_long.csv
"""
import sys

import pandas as pd

# Income-statement and balance-sheet lines the guiding questions need.
CANDIDATES = [
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "SalesRevenueNet",
    "SalesRevenueGoodsNet",
    "CostOfGoodsAndServicesSold",
    "CostOfRevenue",
    "CostOfGoodsSold",
    "SellingGeneralAndAdministrativeExpense",
    "DepreciationDepletionAndAmortization",
    "DepreciationAndAmortization",
    "CostOfGoodsAndServicesSoldDepreciationAndAmortization",
    "OperatingIncomeLoss",
    "InventoryNet",
    "RetailRelatedInventoryMerchandise",
]
WINDOW = ("2019-01-01", "2024-03-31")


def main(csv: str) -> None:
    df = pd.read_csv(csv, parse_dates=["start", "end", "filed"])
    df = df[df.unit == "USD"]
    w = df[(df.end >= WINDOW[0]) & (df.end <= WINDOW[1])]

    print("=== Overall ===")
    print(df.groupby("company").agg(rows=("val", "size"), tags=("tag", "nunique"),
                                    first=("end", "min"), last=("end", "max")))

    print("\n=== Candidate lines, FY2019-FY2023 window ===")
    c = w[w.tag.isin(CANDIDATES)].copy()
    # Duration facts: ~quarter (80-100 days), ~half/9-month YTD, ~year (350-380).
    c["kind"] = pd.cut(c.days.fillna(-1), [-2, 0, 100, 290, 380, 10_000],
                       labels=["point-in-time", "quarter", "YTD 6/9-mo", "year", "other"])
    summary = (c.groupby(["company", "tag", "kind"], observed=True)
                 .agg(n=("val", "size"), periods=("end", "nunique"))
                 .reset_index())
    print(summary.to_string(index=False))

    print("\n=== Duplicates: same company/tag/period reported more than once ===")
    dup = c.groupby(["company", "tag", "start", "end"], dropna=False).agg(
        n=("val", "size"), distinct_vals=("val", "nunique"))
    print(f"periods reported >1 time: {(dup.n > 1).sum()} / {len(dup)}")
    print(f"...of which the values disagree (restated): {(dup.distinct_vals > 1).sum()}")
    print(dup[dup.distinct_vals > 1].head(15).to_string())

    print("\n=== Fiscal year ends per company (annual operating income) ===")
    oi = c[(c.tag == "OperatingIncomeLoss") & (c.kind == "year")]
    print(oi.groupby("company").end.apply(lambda s: sorted({d.date() for d in s})).to_string())


if __name__ == "__main__":
    main(sys.argv[1])
