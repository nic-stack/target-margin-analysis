"""Chart and one-page PDF for docs/brief.md.

Usage: .venv/bin/python src/make_brief.py   (run from the repo root; needs Google Chrome)
"""
import subprocess
import tempfile
from pathlib import Path

import markdown
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SRC, PDF, PNG = Path("docs/brief.md"), Path("docs/brief.pdf"), Path("outputs/brief_chart.png")


def chart():
    t = pd.read_csv("outputs/gap_backtest.csv")
    t = t[(t.company == "Target") & t.fy.isin([2021, 2022])].reset_index(drop=True)
    x = list(range(len(t)))
    inv, sales, gap = "#B5121B", "#4A4A4A", "#E9B8BB"
    fig, ax = plt.subplots(figsize=(8.4, 2.75))
    ax.fill_between(x, t.sales_growth, t.inventory_growth, where=t.inventory_growth > t.sales_growth,
                    interpolate=True, color=gap, alpha=.45, lw=0)
    ax.plot(x, t.inventory_growth, color=inv, lw=2.4, marker="o", ms=5)
    ax.plot(x, t.sales_growth, color=sales, lw=2, marker="s", ms=4.5, ls="--")
    ax.axhline(0, color="#999", lw=.8)
    for i in (1, 3, 4, 5):
        ax.annotate(f"gap {t.gap[i]:.0f}", (i, t.inventory_growth[i]), xytext=(-9 if i == 3 else 0, 8), textcoords="offset points",
                    ha="center", fontsize=8.5, color=inv)
    ax.text(x[-1] + .12, t.inventory_growth.iloc[-1], "Inventory", color=inv, va="center", fontsize=9.5, fontweight="bold")
    ax.text(x[-1] + .12, t.sales_growth.iloc[-1] + 1.5, "Sales", color=sales, va="center", fontsize=9.5, fontweight="bold")
    ax.annotate("Worst profit drop", (5, t.sales_growth[5]), xytext=(5, -9), ha="center", fontsize=8.5, color=sales,
                arrowprops=dict(arrowstyle="-", color=sales, lw=.8))
    ax.set_xticks(x)
    ax.set_xticklabels([f"Q{r.q}\nFY{r.fy}" for r in t.itertuples()], fontsize=8.5)
    ax.set_ylim(-13, 52)
    ax.set_xlim(-.3, len(t) - .2)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))
    ax.tick_params(axis="y", labelsize=8.5)
    ax.set_title("Inventory grew faster than sales from mid-2021 until late 2022", loc="left", fontsize=11, fontweight="bold")
    ax.text(0, -.31, "Target, change from the same quarter a year earlier. Gap = inventory growth minus sales growth, in points. Source: SEC filings.",
            transform=ax.transAxes, fontsize=7.5, color="#555")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig(PNG, dpi=200, bbox_inches="tight")


CSS = """@page{size:letter;margin:.45in .6in}body{font:9.3pt/1.32 Helvetica,Arial,sans-serif;color:#1c1c1c;margin:0}
h1{font-size:17pt;margin:0 0 4pt;color:#B5121B}h2{font-size:10.8pt;margin:7pt 0 2pt;color:#B5121B}p{margin:2pt 0 4pt}
ul,ol{margin:2pt 0 3pt;padding-left:15pt}li{margin:1.5pt 0}table{border-collapse:collapse;width:100%;margin:4pt 0}
th{background:#f3f3f3;font-size:8.6pt}th,td{border:.6pt solid #ccc;padding:3pt 5pt;text-align:center}
img{display:block;width:88%;margin:4pt auto 2pt}hr{border:0;border-top:.6pt solid #bbb;margin:6pt 0 3pt}hr+p{font-size:7.6pt;color:#555;margin:0}"""


def pdf():
    body = markdown.markdown(SRC.read_text(), extensions=["tables", "sane_lists"])
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Why Target\'s profit fell while revenue grew</title><style>{CSS}</style></head><body>{body}</body></html>'
    with tempfile.TemporaryDirectory() as d:
        page = Path(d, "brief.html")
        page.write_text(html.replace("../outputs/", Path("outputs").resolve().as_uri() + "/"))
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={d}/profile",
                        f"--print-to-pdf={PDF.resolve()}", page.as_uri()], check=True, capture_output=True, timeout=90)


if __name__ == "__main__":
    chart()
    pdf()
    print(PDF)
