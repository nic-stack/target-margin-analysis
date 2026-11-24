"""Inventory growth minus sales growth (points), and which quarters a trigger flags.

Usage: .venv/bin/python src/gap_backtest.py      (run from the repo root)
"""
import pandas as pd

q = pd.read_csv("data/clean/quarterly.csv")
q = q[q.fy <= 2022].copy()  # information cutoff
q["cogs_rate"] = q.cogs / q.revenue * 100
prev = q[["company", "fy", "q", "revenue", "cogs_rate"]].assign(fy=q.fy + 1)
q = q.merge(prev, on=["company", "fy", "q"], how="left", suffixes=("", "_prev"))
q["sales_growth"] = (q.revenue / q.revenue_prev - 1) * 100
q["inventory_growth"] = (q.inventory / q.inventory_year_ago - 1) * 100
q["gap"] = q.inventory_growth - q.sales_growth
q["cogs_rate_change"] = q.cogs_rate - q.cogs_rate_prev
t = q[q.fy >= 2020].sort_values(["company", "fy", "q"])[
    ["company", "fy", "q", "inventory_growth", "sales_growth", "gap", "cogs_rate_change"]].round(1)
for level in (10, 15, 20):
    t[f"flag_{level}"] = t.gap > level
t.to_csv("outputs/gap_backtest.csv", index=False)
print(t.to_string(index=False))
for level in (10, 15, 20):
    print(level, {c: [f"FY{r.fy} Q{r.q}" for r in g[g[f"flag_{level}"]].itertuples()] for c, g in t.groupby("company")})
