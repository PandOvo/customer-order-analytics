import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUT_IMG = BASE_DIR / "dashboard" / "screenshots"
    OUT_IMG.mkdir(parents=True, exist_ok=True)

    # GMV趋势
    kpi_path = BASE_DIR / "output" / "kpi_summary.csv"
    if kpi_path.exists():
        kpi = pd.read_csv(kpi_path, parse_dates=["month"])
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(kpi["month"], kpi["gmv"], marker="o")
        ax.set_title("Monthly GMV"); ax.set_xlabel("Month"); ax.set_ylabel("GMV")
        fig.tight_layout(); plt.savefig(OUT_IMG / "gmv_trend.png")

    # 复购率趋势
    rep_path = BASE_DIR / "output" / "repeat_rate.csv"
    if rep_path.exists():
        rep = pd.read_csv(rep_path, parse_dates=["month"])
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(rep["month"], rep["repeat_rate"], marker="o")
        ax.set_title("Monthly Repeat Rate"); ax.set_xlabel("Month"); ax.set_ylabel("Repeat Rate")
        fig.tight_layout(); plt.savefig(OUT_IMG / "repeat_rate.png")

    # 地区Top5堆叠
    rc_path = BASE_DIR / "output" / "region_contrib.csv"
    if rc_path.exists():
        df = pd.read_csv(rc_path, parse_dates=["month"])
        top_regions = df.groupby("region")["gmv"].sum().sort_values(ascending=False).head(5).index.tolist()
        df_top = df[df["region"].isin(top_regions)]
        pivot = df_top.pivot_table(index="month", columns="region", values="gmv", aggfunc="sum").fillna(0).sort_index()
        fig, ax = plt.subplots(figsize=(8,4))
        ax.stackplot(pivot.index, pivot.values.T, labels=pivot.columns)
        ax.set_title("Region GMV (Top 5)"); ax.set_xlabel("Month"); ax.set_ylabel("GMV")
        ax.legend(loc="upper left", fontsize=8)
        fig.tight_layout(); plt.savefig(OUT_IMG / "region_gmv_top5.png")

    print(f"Saved figures to {OUT_IMG}")

if __name__ == "__main__":
    main()
