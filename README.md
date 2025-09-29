# Customer & Order Analytics (Python + SQLite + matplotlib)

本项目用 **Python + SQLite + matplotlib** 完成一套客户与订单分析闭环：
数据生成 → 入库 → KPI/复购率/地区贡献 → RFM 客户分层 → Cohort 留存 → 可视化。

## 📦 项目结构
```
customer-order-analytics/
├─ data/raw/              # 原始CSV（脚本生成）
├─ db/                    # SQLite 数据库
├─ output/                # 指标与分析输出
├─ dashboard/screenshots/ # matplotlib 输出图
├─ sql/                   # SQL 模型（可选）
└─ src/                   # Python 源码
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install pandas numpy matplotlib openpyxl
```

### 2. 运行顺序
```bash
# 在项目根目录执行：

# 1) 生成模拟数据 (18个月订单级)
python src/generate_data.py

# 2) 建库并导入到 SQLite
python src/build_db.py          # 生成 db/orders.sqlite

# 3) 指标输出
python src/kpi_sql.py           # 输出 output/kpi_summary.csv
python src/metrics_sql.py       # 输出 output/repeat_rate.csv & region_contrib.csv
python src/rfm_sql_plus_py.py   # 输出 output/rfm_segments.csv
python src/cohort_sql_plus_py.py# 输出 output/cohort_table.csv

# 4) 绘制示例图（保存到 dashboard/screenshots/）
python src/plots.py
```

### 3. 一键运行
Windows:
```bash
run_all.bat
```
Mac/Linux:
```bash
bash run_all.sh
```

## 📊 输出文件

- **核心指标**
  - `output/kpi_summary.csv`：月 GMV、订单数、活跃用户、AOV
- **复购率 & 地区贡献**
  - `output/repeat_rate.csv`：月度复购率
  - `output/region_contrib.csv`：地区 × 月 GMV、订单数
- **RFM 客户分层**
  - `output/rfm_segments.csv`：R/F/M 分值与客户分层标签
- **Cohort 留存**
  - `output/cohort_table.csv`：首购 Cohort 留存宽表
- **可视化截图**
  - `dashboard/screenshots/gmv_trend.png`
  - `dashboard/screenshots/repeat_rate.png`
  - `dashboard/screenshots/region_gmv_top5.png`

## 🔍 业务洞察

- 西北地区在 2025Q3 的复购率较 Q2 下降 **~18%**，集中在 **食品饮料/家居**；建议在 **10–11 月**加大满减与套装促销。
- 高价值客户对 **电子**品类贡献 GMV **40%+**；针对华南近 60 天沉默人群推“以旧换新 + 提前购券”组合。
