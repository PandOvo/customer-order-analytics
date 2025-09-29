import sqlite3
import pandas as pd
from pathlib import Path

def main():
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / "db" / "orders.sqlite"
    if not DB_PATH.exists():
        raise FileNotFoundError(f"找不到数据库：{DB_PATH}。请先运行 python src/build_db.py")

    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT substr(order_ts,1,7) as month,
           SUM(amount) as gmv,
           COUNT(order_id) as orders_cnt,
           COUNT(DISTINCT user_id) as users_active
    FROM orders
    GROUP BY month
    ORDER BY month;
    """
    kpi = pd.read_sql(query, conn)
    conn.close()

    kpi["month"] = pd.to_datetime(kpi["month"] + "-01")
    kpi["aov"] = kpi["gmv"] / kpi["orders_cnt"]

    OUT = BASE_DIR / "output"
    OUT.mkdir(parents=True, exist_ok=True)
    kpi.to_csv(OUT / "kpi_summary.csv", index=False)
    print(f"Saved {OUT/'kpi_summary.csv'}")

if __name__ == "__main__":
    main()
