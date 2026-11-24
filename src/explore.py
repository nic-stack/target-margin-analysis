"""Bridge, timing, peers, baseline, and evidence for H1-H4.

Usage: .venv/bin/python src/explore.py      (run from the repo root)
Tables print to stdout and are saved in outputs/.
"""
import json

import openpyxl
import pandas as pd

pd.set_option("display.width", 200, "display.max_columns", 30)
q = pd.read_csv("data/clean/quarterly.csv", parse_dates=["q_start", "q_end"])
q["da"] = q.da.fillna(0)
q = q[q.fy <= 2022]  # information cutoff: FY2023 is kept for the epilogue only
PARTS = ["cogs", "sga", "da", "other_operating"]
CATS = {"Clothing & accessories": "448", "Furniture & home": "442", "Electronics & appliances": "443",
        "Sporting, hobby, toys, books": "451", "General merchandise": "452", "Grocery stores": "4451",
        "Health & personal care": "446"}
DISC = ["Clothing & accessories", "Furniture & home", "Electronics & appliances", "Sporting, hobby, toys, books"]
ESS = ["Grocery stores", "Health & personal care"]
BLS = {"PCU484121484121": "Truckload PPI", "PCU483111483111": "Deep-sea freight PPI", "WPU3012": "Truck freight PPI",
       "EIUIR4": "Import: consumer goods", "EIUIR40": "Import: nondurable cons. goods", "EIUIR41": "Import: durable cons. goods",
       "WPU0381": "PPI apparel", "CUUR0000SAA": "CPI apparel", "WPU12": "PPI home goods", "CUUR0000SAH3": "CPI home furnishings",
       "WPU02": "PPI processed food", "CUUR0000SAF11": "CPI food at home"}


def show(title, df, name, nd=2):
    print(f"\n=== {title}"); print(df.round(nd).to_string()); df.to_csv(f"outputs/{name}.csv")


def bridge(company, a, b, by=None):
    """Sales effect at old margin, plus each cost-rate change x new revenue. Sums exactly."""
    d = q[(q.company == company)]
    if by: d = d[d.q == by]
    s = d.groupby("fy")[["revenue", "oi"] + PARTS].sum()
    r0, r1 = s.loc[a, "revenue"], s.loc[b, "revenue"]
    out = {"sales effect": (r1 - r0) * s.loc[a, "oi"] / r0}
    for p in PARTS:
        out[p] = -(s.loc[b, p] / r1 - s.loc[a, p] / r0) * r1
    out["total"] = sum(out.values()); out["actual"] = s.loc[b, "oi"] - s.loc[a, "oi"]
    assert abs(out["total"] - out["actual"]) < 1e3
    return pd.Series(out) / 1e9


def bls():
    d = json.load(open("data/raw/bls/prices_2018_2024.json"))
    rows = [(BLS[s["seriesID"]], pd.Timestamp(int(x["year"]), int(x["period"][1:]), 1), float(x["value"]))
            for s in d["Results"]["series"] if s["seriesID"] in BLS for x in s["data"] if x["period"] != "M13"]
    return pd.DataFrame(rows, columns=["s", "m", "v"]).pivot(index="m", columns="s", values="v")


def census():
    wb = openpyxl.load_workbook("data/raw/census/mrtssales92-present.xlsx", read_only=True)
    rows = []
    for y in range(2018, 2024):
        for r in wb[str(y)].iter_rows(values_only=True):
            if r[1] and str(r[1]).startswith("ADJUSTED"): break          # not-adjusted block only
            for name, code in CATS.items():
                if str(r[0]).strip() == code:
                    for m, v in enumerate(r[2:14], 1): rows.append((name, pd.Timestamp(y, m, 1), float(v)))
    return pd.DataFrame(rows, columns=["s", "m", "v"]).pivot(index="m", columns="s", values="v")


def fq(df, how):
    """Monthly -> Target fiscal quarters (Feb-Apr, May-Jul, Aug-Oct, Nov-Jan)."""
    k = df.index - pd.DateOffset(months=1)
    fy, qq = k.year, (k.month - 1) // 3 + 1
    g = df.groupby([pd.Index(fy, name="fy"), pd.Index(qq, name="q")])
    out = g.agg(how)[g.size() == 3]
    return out[out.index.get_level_values('fy') <= 2022]


if __name__ == "__main__":
    show("Q1/Q5 bridge, $B", pd.DataFrame({f"{c} {a}->{b}": bridge(c, a, b) for c in ["Target", "Walmart", "Kohl's"]
         for a, b in [(2021, 2022), (2019, 2022)]} | {"Target 2019->2021": bridge("Target", 2019, 2021)}).T, "bridge")
    for c in ["Target", "Walmart", "Kohl's"]:
        show(f"Q2 {c}: FY2021->FY2022 by quarter, $B", pd.DataFrame({f"Q{k}": bridge(c, 2021, 2022, k) for k in range(1, 5)}).T, f"bridge_q_{c[:4]}")
    w = q.copy()
    w["oi%"] = w.oi / w.revenue * 100; w["cogs%"] = w.cogs / w.revenue * 100; w["sga%"] = w.sga / w.revenue * 100
    w["inv_yoy"] = (w.inventory / w.inventory_year_ago - 1) * 100
    w["days_inv"] = w.inventory / w.cogs * w.weeks * 7
    prev = w[["company", "fy", "q", "revenue", "oi%", "cogs%", "sga%", "days_inv"]].assign(fy=w.fy + 1)
    w = w.merge(prev, on=["company", "fy", "q"], suffixes=("", "_p"), how="left")
    w["rev_yoy"] = (w.revenue / w.revenue_p - 1) * 100
    for m in ["oi%", "cogs%", "sga%", "days_inv"]: w[f"d_{m}"] = w[m] - w[f"{m}_p"]
    w["inv_gap"] = w.inv_yoy - w.rev_yoy
    show("H1 inventory vs sales", w[w.fy.between(2021, 2022)].set_index(["company", "fy", "q"])[
        ["rev_yoy", "inv_yoy", "inv_gap", "days_inv", "d_days_inv", "cogs%", "d_cogs%", "d_sga%", "oi%", "d_oi%"]], "inventory", 1)
    base = w[w.fy == 2019].set_index(["company", "q"])
    x = w[w.fy == 2022].set_index(["company", "q"])
    show("FY2022 vs FY2019 same quarter (points)", pd.DataFrame({"d_oi": x["oi%"] - base["oi%"], "d_cogs": x["cogs%"] - base["cogs%"],
         "d_sga": x["sga%"] - base["sga%"], "days_inv": x.days_inv, "days_inv_2019": base.days_inv}), "vs2019", 1)
    ir = q.assign(r=q.inventory / q.revenue * 100).pivot_table(index=["company", "q"], columns="fy", values="r")
    ir["22 vs 19 %"] = (ir[2022] / ir[2019] - 1) * 100; ir["22 vs 21 %"] = (ir[2022] / ir[2021] - 1) * 100
    show("H1 inventory as % of quarter's sales", ir, "inv_to_sales", 1)
    a = q.groupby(["company", "fy"])[["revenue", "cogs", "sga", "da", "oi"]].sum().loc["Target"]
    m = a.oi / a.revenue; R = a.revenue[2022] / 1e9
    print("\n=== Q5 split of the $5.10B: sales %.2f | to FY2019 margin %.2f | below FY2019 margin %.2f" % (
        bridge("Target", 2021, 2022)["sales effect"], -(m[2021] - m[2019]) * R, -(m[2019] - m[2022]) * R))
    show("Target rates, % of revenue", a.div(a.revenue, axis=0) * 100, "target_rates", 2)
    t = w[(w.company == "Target") & (w.fy == 2022)].set_index("q")
    floor = t["d_cogs%"].drop(2).mean()
    print("Q2 spike above the other three quarters' average rise (%.1f pts): $%.2fB" % (floor, (t.loc[2, "d_cogs%"] - floor) / 100 * t.loc[2, "revenue"] / 1e9))
    P = fq(bls(), "mean")
    show("H2/H4 price growth YoY %", (P.groupby("q").pct_change() * 100).loc[2021:2022], "prices", 1)
    show("Price level, FY2019 average = 100", P / P.loc[2019].mean() * 100, "price_levels", 0)
    C = census(); C["DISCRETIONARY"] = C[DISC].sum(axis=1); C["ESSENTIALS"] = C[ESS].sum(axis=1)
    C = fq(C, "sum")
    show("H3 Census store sales YoY %", (C.groupby("q").pct_change() * 100).loc[2021:2022], "census", 1)
    sh = (C.DISCRETIONARY / (C.DISCRETIONARY + C.ESSENTIALS) * 100).unstack("q"); sh["year"] = C.groupby("fy").apply(
        lambda d: d.DISCRETIONARY.sum() / (d.DISCRETIONARY + d.ESSENTIALS).sum() * 100)
    show("H3 discretionary share of (disc.+essentials) %", sh, "disc_share", 1)
