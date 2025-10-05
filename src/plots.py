from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


def get_project_root():
    """获取项目根目录"""
    return Path(__file__).resolve().parent.parent


def save_figure(figure, filename):
    """保存图表并确保路径存在"""
    screenshots_path = get_project_root() / 'dashboard' / 'screenshots'
    screenshots_path.mkdir(parents=True, exist_ok=True)  # 确保路径存在
    output_path = screenshots_path / filename
    figure.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()  # 关闭图形
    print(f"文件保存到: {output_path}")


def plot_gmv_and_channels():
    project_root = get_project_root()
    kpi_path = project_root / 'output' / 'kpi_summary.csv'
    channel_path = project_root / 'output' / 'region_contrib.csv'

    if not kpi_path.exists() or not channel_path.exists():
        print("缺少必要的文件，跳过绘图")
        return

    kpi = pd.read_csv(kpi_path, parse_dates=['month'])
    region_contrib = pd.read_csv(channel_path, parse_dates=['month'])

    # 绘制 GMV 波动（包含不同渠道）
    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(kpi['month'], kpi['gmv'], color='b', label='GMV', marker='o')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('GMV', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()  # 双 y 轴
    ax2.plot(region_contrib['month'], region_contrib['gmv'], color='g', label='Channel GMV', marker='x')
    ax2.set_ylabel('Channel GMV', color='g')
    ax2.tick_params(axis='y', labelcolor='g')

    fig.tight_layout()  # 自动调整图像布局
    plt.title('Monthly GMV and Channel GMV Comparison')

    save_figure(fig, 'gmv_and_channels.png')


def plot_region_gmv_ranking():
    project_root = get_project_root()
    rc_path = project_root / 'output' / 'region_contrib.csv'

    if not rc_path.exists():
        print("缺少必要的文件，跳过绘图")
        return

    df = pd.read_csv(rc_path, parse_dates=['month'])
    region_top = df.groupby('region')['gmv'].sum().sort_values(ascending=False).head(5).index.tolist()
    df_top = df[df['region'].isin(region_top)]

    # 排名堆叠图
    pivot = df_top.pivot_table(index='month', columns='region', values='gmv', aggfunc='sum').fillna(0)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.stackplot(pivot.index, pivot.values.T, labels=pivot.columns)
    ax.set_title('Region GMV (Top 5) with Rankings')
    ax.set_xlabel('Month')
    ax.set_ylabel('GMV')
    ax.legend(loc='upper left', fontsize=8)
    fig.tight_layout()

    save_figure(fig, 'region_gmv_top5_ranking.png')


def plot_repeat_rate_and_gmv():
    project_root = get_project_root()
    rep_path = project_root / 'output' / 'repeat_rate.csv'
    gmv_path = project_root / 'output' / 'kpi_summary.csv'

    if not rep_path.exists() or not gmv_path.exists():
        print("缺少必要的文件，跳过绘图")
        return

    rep = pd.read_csv(rep_path, parse_dates=['month'])
    gmv = pd.read_csv(gmv_path, parse_dates=['month'])

    # 绘制复购率和 GMV 对比
    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(rep['month'], rep['repeat_rate'], color='r', label='Repeat Rate', marker='o')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Repeat Rate', color='r')
    ax1.tick_params(axis='y', labelcolor='r')

    ax2 = ax1.twinx()
    ax2.plot(gmv['month'], gmv['gmv'], color='b', label='GMV', marker='x')
    ax2.set_ylabel('GMV', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    fig.tight_layout()
    plt.title('Monthly Repeat Rate and GMV Comparison')

    save_figure(fig, 'repeat_rate_and_gmv.png')


def main():
    plot_gmv_and_channels()  # 绘制 GMV 和渠道对比图
    plot_region_gmv_ranking()  # 绘制地区 GMV 排名堆叠图
    plot_repeat_rate_and_gmv()  # 绘制复购率与 GMV 关系图
    print("\n=== 图表生成完成 ===")


if __name__ == '__main__':
    main()
