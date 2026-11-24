"""Flatten SEC EDGAR companyfacts JSON files into one long table.

Each row is one reported number: company, tag, unit, period start/end,
value, and which filing (form, fiscal year/period, filed date) reported it.

Usage: python3 -I src/load_facts.py data/raw data/interim/facts_long.csv
"""
import json
import sys
from pathlib import Path

import pandas as pd

COMPANIES = {27419: "Target", 104169: "Walmart", 885639: "Kohl's"}


def flatten(path: Path) -> pd.DataFrame:
    d = json.loads(path.read_text())
    rows = []
    for taxonomy, tags in d["facts"].items():
        for tag, body in tags.items():
            for unit, facts in body["units"].items():
                for f in facts:
                    rows.append(
                        {
                            "cik": d["cik"],
                            "company": COMPANIES.get(d["cik"], d["entityName"]),
                            "taxonomy": taxonomy,
                            "tag": tag,
                            "unit": unit,
                            "start": f.get("start"),
                            "end": f["end"],
                            "val": f["val"],
                            "accn": f["accn"],
                            "fy": f.get("fy"),
                            "fp": f.get("fp"),
                            "form": f.get("form"),
                            "filed": f.get("filed"),
                            "frame": f.get("frame"),
                        }
                    )
    df = pd.DataFrame(rows)
    for c in ("start", "end", "filed"):
        df[c] = pd.to_datetime(df[c])
    df["days"] = (df["end"] - df["start"]).dt.days
    return df


def main(raw_dir: str, out_csv: str) -> None:
    df = pd.concat([flatten(p) for p in sorted(Path(raw_dir).glob("CIK*.json"))])
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"{len(df):,} rows -> {out_csv}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
