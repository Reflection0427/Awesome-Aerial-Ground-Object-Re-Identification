import re
import matplotlib.pyplot as plt
import matplotlib as mpl
from collections import defaultdict
import os
import numpy as np

# Keep SVG output byte-for-byte stable when the underlying data has not changed.
mpl.rcParams['svg.hashsalt'] = 'awesome-agreid-publication-trend'

# --- 1. 定义会议/期刊列表 (根据你的 README 内容定制) ---

# CCF-A 类 (你文中出现过的)
CCF_A_VENUES = [
    # 会议
    'CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'AAAI', 'IJCAI', 'SIGGRAPH',
    # 期刊
    'TPAMI', 'IJCV', 'TIP', 'TIFS', 'TVCG'
]

# CCF-B 类 (根据你的 README 内容提取)
# 注意：Information Fusion, WACV, ESWA 在 CCF 目录中通常归为 C 类，
# 但如果你希望将它们统计为 B 类，可以在下面列表中解除注释或添加。
CCF_B_VENUES = [
    # 你文中明确出现的 CCF-B 类期刊/会议
    'TNNLS',  # IEEE Transactions on Neural Networks and Learning Systems
    'TMM',  # IEEE Transactions on Multimedia
    'TCSVT',  # IEEE Transactions on Circuits and Systems for Video Technology
    'TITS',  # IEEE Transactions on Intelligent Transportation Systems
    'ICIP', 'ICASSP', 'ICPR', 'BMVC',  # 常规 CV B类会议
    'CVIU', 'PR', 'Pattern Recognition', 'NeuCom',  # 常规 CV B类期刊
    'TASLP',

    # [可选] 如果你想把这些高水平但 CCF 评级为 C 的也算作 B 类展示，请取消注释：
    # 'WACV', 'Inform Fusion', 'Information Fusion', 'ESWA'
]


def parse_readme(filepath):
    """解析 README.md 文件，统计每年论文总数、CCF-A 和 CCF-B 论文数"""
    year_counts = defaultdict(int)
    ccf_a_counts = defaultdict(int)
    ccf_b_counts = defaultdict(int)

    # 匹配年份 (201x - 203x)
    year_pattern = re.compile(r'\b(20[123]\d)\b')

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        in_paper_section = False
        for line in lines:
            # 只统计正式论文表，避免 Spotlight 中的论文被重复计算。
            if "## 📝 Papers & Methods" in line:
                in_paper_section = True
            if "## 💾 Datasets" in line or "## 📈 Star History" in line:
                in_paper_section = False

            if not in_paper_section:
                continue

            # 简单的行过滤器：必须包含链接 ([) 且看起来像是一个条目
            if '[' in line and ']' in line and ('http' in line or 'arXiv' in line or 'Paper' in line):
                year_match = year_pattern.search(line)
                if year_match:
                    year = int(year_match.group(1))
                    year_counts[year] += 1

                    # 优先匹配 CCF-A
                    is_ccf_a = False
                    for venue in CCF_A_VENUES:
                        # 使用正则边界匹配，防止部分匹配 (例如匹配到 TIP 但实际是 TIFS, 虽这两个都是A但逻辑要严谨)
                        if re.search(r'\b' + re.escape(venue) + r'\b', line, re.IGNORECASE):
                            is_ccf_a = True
                            ccf_a_counts[year] += 1
                            break

                    # 如果不是 A，再检查是否是 CCF-B
                    if not is_ccf_a:
                        for venue in CCF_B_VENUES:
                            if re.search(r'\b' + re.escape(venue) + r'\b', line, re.IGNORECASE):
                                ccf_b_counts[year] += 1
                                break

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None, None, None
    return year_counts, ccf_a_counts, ccf_b_counts


def plot_chart_pami(year_counts, ccf_a_counts, ccf_b_counts, output_path):
    """
    绘制符合 IEEE/PAMI 风格的出版级图表 (Total, CCF-A, CCF-B)
    """
    if not year_counts:
        print("No data found to plot.")
        return

    # 数据准备：排序年份
    years = sorted(year_counts.keys())

    # 过滤掉过于久远的年份（可选，防止图表太长），这里保留全部
    # years = [y for y in years if y >= 2020]

    total_vals = [year_counts[y] for y in years]
    ccf_a_vals = [ccf_a_counts[y] for y in years]
    ccf_b_vals = [ccf_b_counts[y] for y in years]

    # --- 样式设置 ---
    plt.rcParams['font.family'] = 'serif'
    # plt.rcParams['font.serif'] = ['Times New Roman'] # 如果系统支持
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['font.size'] = 11
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['axes.linewidth'] = 1.0

    # 画布大小 (宽, 高)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

    # --- 绘图 ---
    bar_width = 0.25
    index = np.arange(len(years))

    # 1. Total Publications (蓝色, 最左)
    rects1 = ax.bar(index - bar_width, total_vals, bar_width,
                    label='Total Publications',
                    color='#4A90E2', alpha=0.9,
                    edgecolor='black', linewidth=0.8, zorder=3)

    # 2. CCF-A Venues (红色, 中间, 斜线纹理)
    rects2 = ax.bar(index, ccf_a_vals, bar_width,
                    label='CCF-A Venues',
                    color='#E74C3C', alpha=0.9,
                    edgecolor='black', linewidth=0.8, hatch='//', zorder=3)

    # 3. CCF-B Venues (森林绿 - Forest Green, 纯色无纹理)
    rects3 = ax.bar(index + bar_width, ccf_b_vals, bar_width,
                    label='CCF-B Venues',
                    color='#E23E3C', alpha=0.9,  # 颜色修改
                    edgecolor='black', linewidth=0.8, zorder=3)

    # --- 细节修饰 ---
    # Y轴网格
    ax.yaxis.grid(True, linestyle='--', which='major', color='#D3D3D3', alpha=0.5, zorder=0)
    ax.set_axisbelow(True)

    # 标签
    ax.set_xlabel('Year', fontweight='bold', labelpad=8)
    ax.set_ylabel('Number of Papers', fontweight='bold', labelpad=8)
    # ax.set_title('Publication Trend', fontweight='bold', pad=15) # 可选标题

    # X轴刻度
    ax.set_xticks(index)
    ax.set_xticklabels(years)

    # 去除多余边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.0)
    ax.spines['bottom'].set_linewidth(1.0)

    # 图例
    ax.legend(frameon=False, loc='upper left', ncol=1)

    # 数值标注函数
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{height}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 2),  # vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8)

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()

    # 确保保存目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 保存 SVG (矢量) 和 PNG (位图)
    plt.savefig(output_path, format='svg', bbox_inches='tight', metadata={'Date': None})
    # Matplotlib writes trailing spaces in multi-line SVG paths. Normalizing them
    # keeps diffs clean without changing the rendered image.
    with open(output_path, 'r', encoding='utf-8') as svg_file:
        normalized_svg = '\n'.join(line.rstrip() for line in svg_file.read().splitlines()) + '\n'
    with open(output_path, 'w', encoding='utf-8') as svg_file:
        svg_file.write(normalized_svg)
    print(f"Chart saved to {output_path}")
    plt.close()


if __name__ == "__main__":
    # 路径处理：假设脚本在 scripts/ 下，README 在根目录
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file_path))

    # 如果脚本就在根目录运行，请取消下面这行的注释并注释上面两行
    # project_root = os.path.dirname(current_file_path)

    readme_path = os.path.join(project_root, 'README.md')
    output_image_path = os.path.join(project_root, 'assets', 'publication_trend.svg')

    print(f"Scanning: {readme_path}")

    if os.path.exists(readme_path):
        y_counts, a_counts, b_counts = parse_readme(readme_path)
        if y_counts:
            # 打印一下统计结果以供调试
            print("-" * 30)
            print(f"{'Year':<6} {'Total':<6} {'CCF-A':<6} {'CCF-B':<6}")
            for y in sorted(y_counts.keys()):
                print(f"{y:<6} {y_counts[y]:<6} {a_counts[y]:<6} {b_counts[y]:<6}")
            print("-" * 30)

            plot_chart_pami(y_counts, a_counts, b_counts, output_image_path)
        else:
            print("No papers found. Check the parsing logic.")
    else:
        print(f"README not found at {readme_path}")
