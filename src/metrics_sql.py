import sqlite3
import pandas as pd
from pathlib import Path

def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / "db" / "orders.sqlite"
    if not DB_PATH.exists():
        raise FileNotFoundError(f"找不到数据库：{DB_PATH}。请先运行 python src/build_db.py")

    conn = sqlite3.connect(DB_PATH)
    orders = pd.read_sql("SELECT * FROM orders", conn, parse_dates=["order_ts"])
    conn.close()

    orders["month"] = orders["order_ts"].dt.to_period("M").dt.to_timestamp()

    # 月度复购率
    user_month = orders.groupby(["month","user_id"]).size().reset_index(name="cnt")
    repeat_users = user_month.groupby("month").apply(lambda g: (g["cnt"]>=2).sum()).reset_index(name="repeat_users")
    active_users = user_month.groupby("month")["user_id"].nunique().reset_index(name="active_users")
    rep = repeat_users.merge(active_users, on="month")
    rep["repeat_rate"] = rep["repeat_users"] / rep["active_users"]

    # 地区贡献
    region_contrib = orders.groupby(["month","region"]).agg(
        gmv=("amount","sum"),
        orders=("order_id","count")
    ).reset_index()

    OUT = BASE_DIR / "output"
    OUT.mkdir(parents=True, exist_ok=True)
    rep.to_csv(OUT / "repeat_rate.csv", index=False, encoding="utf-8-sig")
    region_contrib.to_csv(OUT / "region_contrib.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {OUT/'repeat_rate.csv'} and {OUT/'region_contrib.csv'}")

if __name__ == "__main__":
    main()
