"""Build a clean quarterly income-statement + inventory table.

Rules (see docs/03-cleaning.md):
- Duplicates: for each company/tag/period keep the latest version filed on or
  before CUTOFF (what an analyst saw in March 2023). Periods first reported
  after the cutoff (FY2023 epilogue) use their original filing.
- Quarters: use the reported 3-month figure if there is one; otherwise the
  difference of year-to-date figures. Q4 = full year - 9-month YTD (or minus
  Q1+Q2+Q3 when no 9-month figure exists).
- Fiscal-year label = calendar year the fiscal year starts in, so Walmart's
  "FY2023" (Feb 2022-Jan 2023) lines up with Target's and Kohl's FY2022.
- Every value carries a `*_method` column saying how it was obtained.

Usage: python3 src/clean_quarterly.py data/interim/facts_long.csv data/clean/quarterly.csv
"""
import sys
from pathlib import Path

import pandas as pd

CUTOFF = pd.Timestamp("2023-03-31")
FIRST_FY, LAST_FY = 2019, 2023

REV = "RevenueFromContractWithCustomerExcludingAssessedTax"
SGA = "SellingGeneralAndAdministrativeExpense"
LINES = {
    "Target": {"revenue": REV, "cogs": "CostOfGoodsAndServicesSold", "sga": SGA,
               "da": "DepreciationAndAmortization", "oi": "OperatingIncomeLoss"},
    # Walmart: total revenues (incl. membership fees) to match operating income;
    # net sales kept separately. No separate depreciation line.
    "Walmart": {"revenue": "Revenues", "net_sales": REV, "cogs": "CostOfRevenue",
                "sga": SGA, "oi": "OperatingIncomeLoss"},
    "Kohl's": {"revenue": REV, "cogs": "CostOfGoodsAndServicesSold", "sga": SGA,
               "da": "DepreciationAndAmortization", "oi": "OperatingIncomeLoss"},
}
INVENTORY = "InventoryNet"
TOL = pd.Timedelta(days=3)


def dedupe(df: pd.DataFrame) -> pd.DataFrame:
    """One value per company/tag/start/end, as seen at the cutoff."""
    df = df.sort_values("filed")
    before = df[df.filed <= CUTOFF].groupby(["company", "tag", "start", "end"], dropna=False).tail(1)
    after = df[df.filed > CUTOFF].groupby(["company", "tag", "start", "end"], dropna=False).head(1)
    keys = before.set_index(["company", "tag", "start", "end"]).index
    after = after[~after.set_index(["company", "tag", "start", "end"]).index.isin(keys)]
    return pd.concat([before, after])


def fiscal_calendar(facts: pd.DataFrame, raw: pd.DataFrame, company: str) -> pd.DataFrame:
    """Quarter start/end dates per fiscal year, from annual OI and quarterly revenue facts."""
    c = facts[facts.company == company]
    r = raw[raw.company == company]
    years = c[(c.tag == "OperatingIncomeLoss") & c.days.between(355, 375)][["start", "end"]].drop_duplicates()
    # Quarter ends from 10-Qs only: Kohl's FY2019 10-K mis-dates its quarterly
    # figures by 1-2 days (e.g. 2019-05-02 vs the 10-Q's 2019-05-04).
    # Uses the raw (pre-dedupe) rows, since dedupe may keep a later 10-K's copy.
    q_ends = r[(r.tag == LINES[company]["revenue"]) & r.days.between(80, 100)
               & (r.form == "10-Q")].end.drop_duplicates()
    rows = []
    for fy_start, fy_end in years.sort_values("start").itertuples(index=False):
        fy = fy_start.year
        if not FIRST_FY <= fy <= LAST_FY:
            continue
        ends = sorted(e for e in q_ends if fy_start < e < fy_end - TOL)
        if len(ends) != 3:
            raise ValueError(f"{company} FY{fy}: expected 3 interim quarter ends, got {ends}")
        ends.append(fy_end)
        starts = [fy_start] + [e + pd.Timedelta(days=1) for e in ends[:3]]
        for q, (s, e) in enumerate(zip(starts, ends), 1):
            rows.append({"company": company, "fy": fy, "q": q, "fy_start": fy_start,
                         "q_start": s, "q_end": e, "weeks": round(((e - s).days + 1) / 7)})
    return pd.DataFrame(rows)


def lookup(f: pd.DataFrame, start, end):
    m = f[(f.end == end) & ((f.start - start).abs() <= TOL)]
    return (m.iloc[0].val, m.iloc[0].filed) if len(m) else (None, None)


def quarter_values(facts, company, tag, cal):
    f = facts[(facts.company == company) & (facts.tag == tag)]
    out = {}
    for fy, g in cal.groupby("fy"):
        g = g.sort_values("q")
        fy_start = g.fy_start.iloc[0]
        prev_end, vals = None, {}
        for r in g.itertuples():
            v, filed = lookup(f, r.q_start, r.q_end)
            method = "reported"
            if v is None:
                cum, filed = lookup(f, fy_start, r.q_end)
                prev = 0 if prev_end is None else lookup(f, fy_start, prev_end)[0]
                if cum is not None and prev is not None:
                    v, method = cum - prev, ("Q4 = year - 9mo" if r.q == 4 else "YTD difference")
                elif r.q == 4 and cum is not None and all(vals.get(k) is not None for k in (1, 2, 3)):
                    v, method = cum - sum(vals[k] for k in (1, 2, 3)), "Q4 = year - Q1-Q3"
                else:
                    method = "missing"
            vals[r.q] = v
            out[(fy, r.q)] = (v, method, filed)
            prev_end = r.q_end
    return out


def build(facts_csv: str) -> pd.DataFrame:
    df = pd.read_csv(facts_csv, parse_dates=["start", "end", "filed"])
    df = df[df.unit == "USD"]
    tags = {t for lines in LINES.values() for t in lines.values()} | {INVENTORY}
    facts = dedupe(df[df.tag.isin(tags)])

    frames = []
    for company, lines in LINES.items():
        cal = fiscal_calendar(facts, df, company)
        for line, tag in lines.items():
            qv = quarter_values(facts, company, tag, cal)
            cal[line] = [qv[(r.fy, r.q)][0] for r in cal.itertuples()]
            cal[f"{line}_method"] = [qv[(r.fy, r.q)][1] for r in cal.itertuples()]
        inv = facts[(facts.company == company) & (facts.tag == INVENTORY)].set_index("end").val
        cal["inventory"] = cal.q_end.map(inv)
        # Year-ago inventory: balance sheet at the quarter end ~52 weeks earlier
        # (10-Qs report the same quarter of the prior year as a comparative).
        def year_ago(end):
            m = inv[(abs((inv.index - (end - pd.Timedelta(weeks=52))).days) <= 7)]
            return m.iloc[0] if len(m) else None
        cal["inventory_year_ago"] = cal.q_end.map(year_ago)
        frames.append(cal)
    q = pd.concat(frames, ignore_index=True)

    # Fill cost of goods from the income-statement identity where it's missing.
    # Only valid where the identity is verified (see checks()).
    da = q.get("da", 0).fillna(0)
    implied = q.revenue - q.sga - da - q.oi
    gap = q.cogs.isna() & implied.notna()
    q.loc[gap, "cogs"] = implied[gap]
    q.loc[gap, "cogs_method"] = "identity: rev - sga - da - oi"

    # Anything else between revenue and operating income (Kohl's impairments,
    # store closings, real-estate gains). Zero for Target and Walmart.
    q["other_operating"] = q.revenue - q.cogs - q.sga - da - q.oi
    return q


def checks(q: pd.DataFrame, facts_csv: str) -> None:
    print("=== Identity check: revenue - cogs - sga - da - oi (should be ~0) ===")
    ok = q[q.cogs_method != "identity: rev - sga - da - oi"].copy()
    ok["residual_$M"] = (ok.other_operating / 1e6).round(0)
    print(ok.groupby("company")["residual_$M"].describe()[["count", "min", "max"]].to_string())
    big = ok[ok["residual_$M"].abs() > 5]
    if len(big):
        print("Quarters with residual > $5M:")
        print(big[["company", "fy", "q", "residual_$M"]].to_string(index=False))

    print("\n=== Value methods ===")
    for line in ["revenue", "cogs", "sga", "da", "oi"]:
        print(line, q.groupby("company")[f"{line}_method"].value_counts().to_dict())

    print("\n=== Missing values ===")
    print(q[["company", "fy", "q"] + [c for c in ["revenue", "cogs", "sga", "da", "oi", "inventory"]]]
          .set_index(["company", "fy", "q"]).isna().sum().to_string())


def annual_check(q: pd.DataFrame, facts_csv: str) -> None:
    """Sum of the four quarters vs the annual figure in the 10-K (cutoff version)."""
    df = pd.read_csv(facts_csv, parse_dates=["start", "end", "filed"])
    facts = dedupe(df[(df.unit == "USD") & df.days.between(355, 375)])
    print("\n=== Quarters vs 10-K annual totals ($M, max abs difference) ===")
    for company, lines in LINES.items():
        for line, tag in lines.items():
            f = facts[(facts.company == company) & (facts.tag == tag)].set_index("end").val
            g = q[q.company == company].groupby("fy").agg(total=(line, "sum"), end=("q_end", "max"))
            g["annual"] = g.end.map(f)
            diff = ((g.total - g.annual).abs() / 1e6).max()
            print(f"{company:8} {line:10} {diff:8.1f}   years checked: {g.annual.notna().sum()}")


def main(facts_csv: str, out_csv: str) -> None:
    q = build(facts_csv)
    checks(q, facts_csv)
    annual_check(q, facts_csv)
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    q.to_csv(out_csv, index=False)
    print(f"\n{len(q)} company-quarters -> {out_csv}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
