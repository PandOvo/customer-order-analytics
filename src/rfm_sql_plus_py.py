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

    as_of = orders["order_ts"].max() + pd.Timedelta(days=1)
    horizon_start = as_of - pd.Timedelta(days=365)
    df = orders[(orders["order_ts"] < as_of) & (orders["order_ts"] >= horizon_start)].copy()

    rfm = df.groupby("user_id").agg(
        last_order=("order_ts","max"),
        freq=("order_id","count"),
        monetary=("amount","sum")
    ).reset_index()
    rfm["recency"] = (as_of - rfm["last_order"]).dt.days

    rfm["R"] = pd.qcut(rfm["recency"].rank(method="first"), 5, labels=[5,4,3,2,1]).astype(int)
    rfm["F"] = pd.qcut(rfm["freq"].rank(method="first"),    5, labels=[1,2,3,4,5]).astype(int)
    rfm["M"] = pd.qcut(rfm["monetary"].rank(method="first"),5, labels=[1,2,3,4,5]).astype(int)

    def seg(r,f,m):
        if r>=4 and f>=4 and m>=4: return "高价值"
        if r>=4 and f>=3:          return "保持关系"
        if r>=3 and m>=4:          return "潜力客户"
        if f>=3 or m>=3:           return "成长客户"
        if r==2 and f<=2:          return "预流失"
        if r==1:                   return "流失"
        return "一般"

    rfm["segment"] = rfm.apply(lambda x: seg(x.R,x.F,x.M), axis=1)

    OUT = BASE_DIR / "output"
    OUT.mkdir(parents=True, exist_ok=True)
    rfm[["user_id", "R", "F", "M", "recency", "freq", "monetary", "segment"]] \
        .to_csv(OUT / "rfm_segments.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {OUT/'rfm_segments.csv'}")

if __name__ == "__main__":
    main()
