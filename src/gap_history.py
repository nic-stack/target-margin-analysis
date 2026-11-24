"""What inventory-minus-sales growth gaps were normal before the pandemic?

Sets the trigger levels for action A from each company's own history (quarters ending
mid-2009 to Feb 2020), using values filed by 2023-03-31. Growth is always within one
revenue tag, because companies changed tags over time.

Usage: .venv/bin/python src/gap_history.py   (run from the repo root; needs
data/interim/facts_long.csv, built by src/load_facts.py)
"""
import pandas as pd

CUTOFF, PRE_END = "2023-03-31", "2020-03-01"
REV = "RevenueFromContractWithCustomerExcludingAssessedTax"
TAGS = {"Target": ([REV, "SalesRevenueNet", "Revenues"], "CostOfGoodsAndServicesSold"),
        "Walmart": (["Revenues"], "CostOfRevenue"),
        "Kohl's": ([REV, "SalesRevenueNet"], "CostOfGoodsAndServicesSold")}

f = pd.read_csv("data/interim/facts_long.csv", parse_dates=["start", "end", "filed"])
f = f[(f.unit == "USD") & (f.filed <= CUTOFF)].sort_values("filed")


def quarterly(company, tag):
    """Reported 3-month values; Q4 = year minus nine months."""
    r = f[(f.company == company) & (f.tag == tag)].copy()
    r["days"] = (r.end - r.start).dt.days
    out = r[r.days.between(80, 100)].groupby("end").val.last()
    year = r[r.days.between(355, 375)].groupby("end").agg(val=("val", "last"), start=("start", "last"))
    nine = r[r.days.between(260, 285)].groupby("start").val.last()
    for e, row in year.iterrows():
        if e not in out.index:
            m = [v for s, v in nine.items() if abs((s - row.start).days) <= 3]
            if m:
                out.loc[e] = row.val - m[-1]
    return out.sort_index()


def year_ago(index, end):
    m = [x for x in index if 355 <= (end - x).days <= 375]
    return m[0] if m else None


rows = []
for company, (tags, cost_tag) in TAGS.items():
    inv = f[(f.company == company) & (f.tag == "InventoryNet")].groupby("end").val.last()
    cost = quarterly(company, cost_tag)
    done = set()
    for tag in tags:
        rev = quarterly(company, tag)
        for e, v in rev.items():
            p, ip = year_ago(rev.index, e), year_ago(inv.index, e)
            if e in done or e not in inv.index or p is None or ip is None:
                continue
            done.add(e)
            cc = (cost[e] / v - cost[p] / rev[p]) * 100 if e in cost.index and p in cost.index else None
            rows.append((company, e, (inv[e] / inv[ip] - 1) * 100 - (v / rev[p] - 1) * 100, cc))
d = pd.DataFrame(rows, columns=["company", "end", "gap", "cogs_rate_change"]).sort_values(["company", "end"])
pre = d[d.end < PRE_END].copy()
g = pre.groupby("company").gap
summary = pd.DataFrame({"quarters": g.size(), "median": g.median(), "max": g.max(),
                        **{f"above_{k}": g.apply(lambda s, k=k: (s > k).sum()) for k in (10, 15, 20)}}).round(1)
pre.round(2).to_csv("outputs/gap_history.csv", index=False)
summary.to_csv("outputs/gap_history_summary.csv")
print(summary.to_string())
print("\nTarget, pre-pandemic: cost-rate change (points, vs. year ago) after each gap above 10")
t = pre[pre.company == "Target"].reset_index(drop=True)
for i in t.index[t.gap > 10]:
    print(t.end[i].date(), "gap", round(t.gap[i], 1), "| next 4 quarters:", t.cogs_rate_change[i + 1:i + 5].round(1).tolist())
print("Target, all pre-pandemic quarters with a cost rate:", t.cogs_rate_change.notna().sum(),
      "| range", t.cogs_rate_change.min().round(1), "to", t.cogs_rate_change.max().round(1))
