"""Epilogue: what happened after the March 2023 cutoff, to grade the brief.

Uses the latest filed value for each period, so Target's FY2022 cost-of-goods rate here is
75.4% after the 2025 restatement (75.43), against 75.36 as filed in March 2023.

Usage: .venv/bin/python src/epilogue.py   (run from the repo root; needs
data/interim/facts_long.csv, built by src/load_facts.py)
"""
import pandas as pd

REV = "RevenueFromContractWithCustomerExcludingAssessedTax"
LINES = {"Target": (REV, "CostOfGoodsAndServicesSold"), "Walmart": ("Revenues", "CostOfRevenue"),
         "Kohl's": (REV, "CostOfGoodsAndServicesSold")}
SGA, OI = "SellingGeneralAndAdministrativeExpense", "OperatingIncomeLoss"

f = pd.read_csv("data/interim/facts_long.csv", parse_dates=["start", "end", "filed"])
f = f[f.unit == "USD"].sort_values("filed")
f["days"] = (f.end - f.start).dt.days


def annual(company, tag):
    x = f[(f.company == company) & (f.tag == tag) & (f.form == "10-K") & f.days.between(355, 375)]
    s = x.groupby("end").val.last()
    s.index = s.index.map(lambda e: e.year - 1)  # fiscal year = calendar year it starts in
    return s


def quarters(company, tag):
    x = f[(f.company == company) & (f.tag == tag)]
    out = x[x.days.between(80, 100)].groupby("end").val.last()
    year = x[x.days.between(355, 375)].groupby("end").agg(val=("val", "last"), start=("start", "last"))
    nine = x[x.days.between(260, 285)].groupby("start").val.last()
    for e, r in year.iterrows():
        if e not in out.index:
            m = [v for s, v in nine.items() if abs((s - r.start).days) <= 3]
            if m:
                out.loc[e] = r.val - m[-1]
    return out.sort_index()


rows, gaps = [], []
for c, (rev_tag, cost_tag) in LINES.items():
    d = pd.DataFrame({"revenue": annual(c, rev_tag), "cogs": annual(c, cost_tag), "sga": annual(c, SGA), "oi": annual(c, OI)}).loc[2021:]
    d["op_margin"], d["cogs_rate"], d["sga_rate"] = [d[k] / d.revenue * 100 for k in ("oi", "cogs", "sga")]
    d["revenue_B"], d["oi_B"] = d.revenue / 1e9, d.oi / 1e9
    rows.append(d.assign(company=c).reset_index(names="fy"))
    rev = quarters(c, rev_tag)
    inv = f[(f.company == c) & (f.tag == "InventoryNet")].groupby("end").val.last()
    for e, v in rev[rev.index > "2023-02-05"].items():
        p = [x for x in rev.index if 355 <= (e - x).days <= 375]
        ip = [x for x in inv.index if 355 <= (e - x).days <= 375]
        if e in inv.index and p and ip:
            gaps.append((c, e.date(), (inv[e] / inv[ip[0]] - 1) * 100 - (v / rev[p[0]] - 1) * 100))
t = pd.concat(rows)[["company", "fy", "revenue_B", "oi_B", "op_margin", "cogs_rate", "sga_rate"]]
t.round(2).to_csv("outputs/epilogue.csv", index=False)
g = pd.DataFrame(gaps, columns=["company", "quarter_end", "gap"])
g.round(1).to_csv("outputs/epilogue_gaps.csv", index=False)
print(t.round(2).to_string(index=False))
print(g[g.company == "Target"].round(1).to_string(index=False))
print("flags above 10:", {c: int((x.gap > 10).sum()) for c, x in g.groupby("company")}, "above 15:", {c: int((x.gap > 15).sum()) for c, x in g.groupby("company")}, "quarters:", g.groupby("company").size().to_dict())
