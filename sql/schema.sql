CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  user_id INTEGER,
  order_ts TEXT,
  amount REAL,
  quantity INTEGER,
  category TEXT,
  region TEXT,
  channel TEXT,
  is_new_user INTEGER
);
