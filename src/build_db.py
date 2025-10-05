import sqlite3
import pandas as pd
from pathlib import Path

def main():

    BASE_DIR = Path(__file__).resolve().parent.parent

    DB_DIR = BASE_DIR / "db"
    DB_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = DB_DIR / "orders.sqlite"

    RAW_DIR = BASE_DIR / "data" / "raw"
    csv_path = RAW_DIR / "orders.csv"
    alt_path = BASE_DIR / "src" / "data" / "raw" / "orders.csv"

    if not csv_path.exists():
        if alt_path.exists():
            csv_path = alt_path
        else:
            raise FileNotFoundError(f"找不到订单CSV：{csv_path} 或 {alt_path}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id     INTEGER PRIMARY KEY,
            user_id      INTEGER,
            order_ts     TEXT,
            amount       REAL,
            quantity     INTEGER,
            category     TEXT,
            region       TEXT,
            channel      TEXT,
            is_new_user  INTEGER
        );
    """)
    orders = pd.read_csv(csv_path)
    orders.to_sql("orders", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print(f"Database built at {DB_PATH}")

if __name__ == "__main__":
    main()
