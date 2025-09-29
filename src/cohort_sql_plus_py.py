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

    orders["order_month"] = orders["order_ts"].dt.to_period("M").dt.to_timestamp()
    first = orders.groupby("user_id")["order_month"].min().rename("cohort")
    df = orders.join(first, on="user_id")
    df["cohort_index"] = ((df["order_month"].dt.year - df["cohort"].dt.year)*12
                          + (df["order_month"].dt.month - df["cohort"].dt.month))

    cohort_pivot = (df.groupby(["cohort","cohort_index"])["user_id"]
                      .nunique().reset_index()
                      .pivot(index="cohort", columns="cohort_index", values="user_id"))
    cohort_size = cohort_pivot[0]
    retention = cohort_pivot.divide(cohort_size, axis=0).round(4)

    OUT = BASE_DIR / "output"
    OUT.mkdir(parents=True, exist_ok=True)
    retention.to_csv(OUT / "cohort_table.csv")
    print(f"Saved {OUT/'cohort_table.csv'}")

if __name__ == "__main__":
    main()
