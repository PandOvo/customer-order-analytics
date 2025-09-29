import numpy as np
import pandas as pd
from pathlib import Path

def main():
    rng = np.random.default_rng(20250929)

    n_users = 16000
    days = pd.date_range('2024-04-01', '2025-09-30', freq='D')
    regions = ['华东','华南','华北','西南','西北','东北']
    categories = ['美妆','电子','家居','食品饮料','服饰','母婴']
    channels = ['APP','小程序','PC','线下']

    users = pd.DataFrame({
        'user_id': np.arange(100000, 100000+n_users),
        'region_home': rng.choice(regions, n_users, p=[.26,.22,.18,.14,.10,.10]),
        'signup_dt': rng.choice(pd.date_range('2024-01-01','2025-06-30', freq='D'), n_users)
    })

    order_counts = rng.integers(0, 16, size=n_users) + (rng.random(n_users)<0.35).astype(int)*rng.integers(3, 12, n_users)
    order_counts = np.clip(order_counts, 0, 60)

    rows, oid = [], 1
    for u, cnt, reg in zip(users['user_id'], order_counts, users['region_home']):
        if cnt == 0: 
            continue
        order_days = rng.choice(days, size=cnt)
        order_days.sort()
        for d in order_days:
            cat = rng.choice(categories, p=[.18,.23,.17,.20,.14,.08])
            ch = rng.choice(channels, p=[.45,.28,.18,.09])
            base = {'美妆':80, '电子':600, '家居':200, '食品饮料':60, '服饰':150, '母婴':120}[cat]
            season = 1.0
            if pd.Timestamp(d).month in [6,11,12]:
                season *= rng.uniform(1.15, 1.5)

            amount = max(1, rng.normal(base, base*0.35)) * season
            qty = int(max(1, round(rng.normal(1.6, 0.9))))
            rows.append([oid, u, pd.Timestamp(d).strftime('%Y-%m-%d %H:%M:%S'),
                         float(round(amount,2)), qty, cat, reg, ch])
            oid += 1

    orders = pd.DataFrame(rows, columns=['order_id','user_id','order_ts','amount','quantity','category','region','channel'])
    orders['is_new_user'] = False
    first_order = orders.sort_values(['user_id','order_ts']).groupby('user_id').head(1).assign(is_new_user=True)[['order_id','is_new_user']]
    orders = orders.merge(first_order, on='order_id', how='left', suffixes=('','_first'))
    orders['is_new_user'] = orders['is_new_user'] | orders['is_new_user_first'].fillna(False)
    orders.drop(columns=['is_new_user_first'], inplace=True)

    BASE_DIR = Path(__file__).resolve().parent.parent
    RAW_DIR = BASE_DIR / "data" / "raw"
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    orders.to_csv(RAW_DIR / "orders.csv", index=False, encoding="utf-8-sig")
    users.to_csv(RAW_DIR / "users.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {RAW_DIR / 'orders.csv'} and {RAW_DIR / 'users.csv'}")


if __name__ == '__main__':
    main()
