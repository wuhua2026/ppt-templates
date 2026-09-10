"""
主生成脚本 - PPT模板资源库

本脚本用于一键生成所有PPT模板并组织到 templates/ 目录中。
作为项目的主构建脚本，可被 CI/CD 或手动触发。

运行方式：
  python scripts/generate_all.py                    # 生成所有模板
  python scripts/generate_all.py --theme blue       # 只生成蓝色主题
  python scripts/generate_all.py --type cover       # 只生成封面
  python scripts/generate_all.py --output ./out     # 指定输出目录

依赖安装：
  pip install -r requirements.txt
"""

import sys
import os
import time
import argparse

# 确保项目根目录在搜索路径中
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from pptx.dml.color import RGBColor

# 主题导入
from themes import ALL_THEMES

# 封面生成器
from python.generators_cover import (
    GeometricRotationCover,
    CircleRingCover,
    TrainMistCover,
    DiamondRevealCover,
    MinimalistGradientCover,
    SplitScreenCover,
    HollowMaskCover,
    LayeredDepthCover,
)

# 目录生成器
from python.generators_directory.diamond_animated import DiamondAnimatedGenerator
from python.generators_directory.circular_ring import CircularRingGenerator
from python.generators_directory.hexagon import HexagonGenerator
from python.generators_directory.sidebar import SidebarGenerator
from python.generators_directory.card_grid import CardGridGenerator
from python.generators_directory.timeline_style import TimelineStyleGenerator

# 时间轴生成器
from python.generators_timeline.horizontal import HorizontalTimeline
from python.generators_timeline.vertical import VerticalTimeline
from python.generators_timeline.dual_wave import DualWaveTimeline
from python.generators_timeline.spiral import SpiralTimeline

# 图表生成器
from python.generators_chart.bar_chart import BarChart
from python.generators_chart.pie_chart import PieChart
from python.generators_chart.line_chart import LineChart
from python.generators_chart.animated_chart import AnimatedBarChart

# 内容页生成器
from python.generators_content.text_image_layout import TextImageLayoutGenerator
from python.generators_content.three_column import ThreeColumnGenerator
from python.generators_content.four_grid import FourGridGenerator
from python.generators_content.full_image_overlay import FullImageOverlayGenerator
from python.generators_content.comparison import ComparisonGenerator

# 团队介绍生成器
from python.generators_team.team_grid import TeamGridGenerator
from python.generators_team.person_card import PersonCardGenerator
from python.generators_team.org_chart import OrgChartGenerator

# 结尾页生成器
from python.generators_ending.thank_you import ThankYouGenerator
from python.generators_ending.qr_code import QRCodeGenerator
from python.generators_ending.contact import ContactPageGenerator


# ============================================================
# 模板注册表
# ============================================================

# 模板注册表：定义所有可生成的模板及其元信息
# 每个模板条目包含：
#   - class: 生成器类
#   - name: 文件名标识
#   - label: 中文标签
#   - category: 类别（animated/static）
#   - type: 类型（cover/directory/timeline/team）
#   - title: 默认标题
#   - subtitle: 默认副标题（可选）
#   - use_items: 是否需要设置目录/列表数据
#   - use_events: 是否需要设置时间轴事件数据
#   - use_members: 是否需要设置团队成员数据

# ------------------------------------------------------------------ #
# 图表与内容页的示例数据
#
# 注意：各生成器的数据字段契约互不相同，不能像目录/时间轴那样共用一份
# DEFAULT_*。缺少示例数据时，图表页只会画出标题、内容页甚至一张幻灯片
# 都不会生成，因此每个模板条目都必须自带 sample。
# ------------------------------------------------------------------ #

# 柱状图 / 动画柱状图：list[dict{label, value}]，color 留空以使用内置调色板
DEFAULT_CHART_BAR_DATA = [
    {"label": "Q1", "value": 120},
    {"label": "Q2", "value": 168},
    {"label": "Q3", "value": 205},
    {"label": "Q4", "value": 182},
    {"label": "Q5", "value": 246},
    {"label": "Q6", "value": 298},
]

# 饼图：list[dict{label, value}]
DEFAULT_CHART_PIE_DATA = [
    {"label": "华东", "value": 38},
    {"label": "华南", "value": 24},
    {"label": "华北", "value": 19},
    {"label": "西南", "value": 11},
    {"label": "其他", "value": 8},
]

# 折线图：series 为 list[dict{name, data:list[float]}]，data 是数值列表
DEFAULT_CHART_LINE_SERIES = [
    {"name": "2025", "data": [120.0, 150.0, 135.0, 200.0, 180.0, 220.0]},
    {"name": "2026", "data": [150.0, 178.0, 165.0, 236.0, 214.0, 268.0]},
]
DEFAULT_CHART_LINE_LABELS = ["1月", "3月", "5月", "7月", "9月", "11月"]

# 图文排版：list[dict{title, description}]，每项一页
DEFAULT_CONTENT_TEXT_IMAGE = [
    {"title": "项目背景", "description": "业务规模持续扩大，原有的人工制作方式已无法满足交付节奏，需要一套可复用、可参数化的演示文稿生成方案。"},
    {"title": "核心方案", "description": "以主题系统与生成器族解耦内容与样式，一份数据可同时驱动 Python 与 TypeScript 两端渲染。"},
]

# 三栏布局：list[dict{icon_text, title, description}]，最多 3 项
DEFAULT_CONTENT_THREE_COLUMN = [
    {"icon_text": "01", "title": "高效协同", "description": "统一的主题与版式规范，跨团队协作时无需反复对齐视觉细节。"},
    {"icon_text": "02", "title": "数据驱动", "description": "图表页由数据直接生成，数值变更后重新生成即可同步更新。"},
    {"icon_text": "03", "title": "持续演进", "description": "新增生成器只需登记进注册表，批量脚本与目录结构自动适配。"},
]

# 四宫格布局：list[dict{number, title, description}]，最多 4 项
DEFAULT_CONTENT_FOUR_GRID = [
    {"number": "01", "title": "市场分析", "description": "行业规模、增速与竞争格局的系统性梳理。"},
    {"number": "02", "title": "产品设计", "description": "核心功能定义、用户路径与交互原型。"},
    {"number": "03", "title": "技术方案", "description": "架构分层、关键选型与性能预算。"},
    {"number": "04", "title": "运营计划", "description": "渠道策略、节奏安排与效果度量。"},
]

# 全图叠加：list[dict{title, subtitle, description}]，每项一页
DEFAULT_CONTENT_FULL_IMAGE = [
    {"title": "品牌主张", "subtitle": "Brand Vision", "description": "让每一次表达都保持一致的质感与专业度。"},
    {"title": "产品理念", "subtitle": "Product Philosophy", "description": "把重复劳动交给脚本，把创造力留给内容本身。"},
]

# 时间轴目录：list[dict{number, title, subtitle}]，subtitle 缺失时卡片只显示标题
DEFAULT_TIMELINE_DIR_ITEMS = [
    {"number": "01", "title": "项目启动", "subtitle": "需求调研与范围确认"},
    {"number": "02", "title": "方案设计", "subtitle": "架构选型与原型评审"},
    {"number": "03", "title": "开发实施", "subtitle": "模块开发与联调"},
    {"number": "04", "title": "测试验收", "subtitle": "功能测试与性能压测"},
    {"number": "05", "title": "上线交付", "subtitle": "灰度发布与文档交付"},
]

# 对比布局：list[dict{left_title, left_items, right_title, right_items}]，每项一页
DEFAULT_CONTENT_COMPARISON = [
    {
        "left_title": "传统方式",
        "left_items": ["依赖人工排版，耗时且易出错", "多套文档风格难以统一", "复用需要复制粘贴再修改"],
        "right_title": "本方案",
        "right_items": ["脚本批量生成，分钟级交付", "七套主题保证视觉一致", "改参数即可整批重生成"],
    },
]


TEMPLATE_REGISTRY = [
    # ========== 动画封面 ==========
    {
        "class": GeometricRotationCover,
        "name": "geometric_rotation",
        "label": "几何旋转封面",
        "category": "animated",
        "type": "cover",
        "title": "几何旋转封面",
        "subtitle": "Geometric Rotation Cover",
    },
    {
        "class": CircleRingCover,
        "name": "circle_ring",
        "label": "圆环转场封面",
        "category": "animated",
        "type": "cover",
        "title": "圆环转场封面",
        "subtitle": "Circle Ring Cover",
    },
    {
        "class": TrainMistCover,
        "name": "train_mist",
        "label": "列车穿雾封面",
        "category": "animated",
        "type": "cover",
        "title": "列车穿雾封面",
        "subtitle": "Train Mist Cover",
    },
    {
        "class": DiamondRevealCover,
        "name": "diamond_reveal",
        "label": "钻石揭示封面",
        "category": "animated",
        "type": "cover",
        "title": "钻石揭示封面",
        "subtitle": "Diamond Reveal Cover",
    },

    # ========== 静态封面 ==========
    {
        "class": MinimalistGradientCover,
        "name": "minimalist_gradient",
        "label": "极简渐变封面",
        "category": "static",
        "type": "cover",
        "title": "极简渐变封面",
        "subtitle": "Minimalist Gradient Cover",
    },
    {
        "class": SplitScreenCover,
        "name": "split_screen",
        "label": "分屏封面",
        "category": "static",
        "type": "cover",
        "title": "分屏封面",
        "subtitle": "Split Screen Cover",
    },
    {
        "class": HollowMaskCover,
        "name": "hollow_mask",
        "label": "镂空遮罩封面",
        "category": "static",
        "type": "cover",
        "title": "镂空遮罩封面",
        "subtitle": "Hollow Mask Cover",
    },
    {
        "class": LayeredDepthCover,
        "name": "layered_depth",
        "label": "层次深度封面",
        "category": "static",
        "type": "cover",
        "title": "层次深度封面",
        "subtitle": "Layered Depth Cover",
    },

    # ========== 动画目录 ==========
    {
        "class": DiamondAnimatedGenerator,
        "name": "diamond_animated",
        "label": "菱形动画目录",
        "category": "animated",
        "type": "directory",
        "title": "内容概览",
        "use_items": True,
    },
    {
        "class": CircularRingGenerator,
        "name": "circular_ring",
        "label": "圆环目录",
        "category": "animated",
        "type": "directory",
        "title": "目录导航",
        "use_items": True,
    },
    {
        "class": HexagonGenerator,
        "name": "hexagon",
        "label": "六边形目录",
        "category": "animated",
        "type": "directory",
        "title": "蜂巢目录",
        "use_items": True,
    },

    # ========== 静态目录 ==========
    {
        "class": SidebarGenerator,
        "name": "sidebar",
        "label": "侧边栏目录",
        "category": "static",
        "type": "directory",
        "title": "目录",
        "use_items": True,
    },
    {
        "class": CardGridGenerator,
        "name": "card_grid",
        "label": "卡片网格目录",
        "category": "static",
        "type": "directory",
        "title": "内容概览",
        "use_items": True,
    },
    {
        "class": TimelineStyleGenerator,
        "name": "timeline_style",
        "label": "时间轴目录",
        "category": "static",
        "type": "directory",
        "title": "实施日程",
        "sample": DEFAULT_TIMELINE_DIR_ITEMS,
    },

    # ========== 时间轴 ==========
    {
        "class": HorizontalTimeline,
        "name": "horizontal",
        "label": "水平时间轴",
        "category": "static",
        "type": "timeline",
        "title": "企业发展历程",
        "use_events": True,
    },
    {
        "class": VerticalTimeline,
        "name": "vertical",
        "label": "垂直时间轴",
        "category": "static",
        "type": "timeline",
        "title": "发展历程",
        "use_events": True,
    },
    {
        "class": DualWaveTimeline,
        "name": "dual_wave",
        "label": "双波形时间轴",
        "category": "animated",
        "type": "timeline",
        "title": "发展历程",
        "use_events": True,
    },
    {
        "class": SpiralTimeline,
        "name": "spiral",
        "label": "螺旋时间轴",
        "category": "animated",
        "type": "timeline",
        "title": "发展历程",
        "use_events": True,
    },

    # ========== 图表 ==========
    {
        "class": BarChart,
        "name": "bar_chart",
        "label": "柱状图",
        "category": "static",
        "type": "chart",
        "title": "数据分析",
        "sample": DEFAULT_CHART_BAR_DATA,
    },
    {
        "class": PieChart,
        "name": "pie_chart",
        "label": "饼图",
        "category": "static",
        "type": "chart",
        "title": "占比分析",
        "sample": DEFAULT_CHART_PIE_DATA,
    },
    {
        "class": LineChart,
        "name": "line_chart",
        "label": "折线图",
        "category": "static",
        "type": "chart",
        "title": "趋势分析",
        # LineChart 的 set_data 需要 (series, x_labels) 两个位置参数
        "sample": (DEFAULT_CHART_LINE_SERIES, DEFAULT_CHART_LINE_LABELS),
    },
    {
        "class": AnimatedBarChart,
        "name": "animated_bar_chart",
        "label": "动画柱状图",
        "category": "animated",
        "type": "chart",
        "title": "数据展示",
        "sample": DEFAULT_CHART_BAR_DATA,
    },

    # ========== 内容页 ==========
    {
        "class": TextImageLayoutGenerator,
        "name": "text_image_layout",
        "label": "图文排版",
        "category": "static",
        "type": "content",
        "title": "内容展示",
        "sample": DEFAULT_CONTENT_TEXT_IMAGE,
    },
    {
        "class": ThreeColumnGenerator,
        "name": "three_column",
        "label": "三栏布局",
        "category": "static",
        "type": "content",
        "title": "三大优势",
        "sample": DEFAULT_CONTENT_THREE_COLUMN,
    },
    {
        "class": FourGridGenerator,
        "name": "four_grid",
        "label": "四宫格布局",
        "category": "static",
        "type": "content",
        "title": "核心要点",
        "sample": DEFAULT_CONTENT_FOUR_GRID,
    },
    {
        "class": FullImageOverlayGenerator,
        "name": "full_image_overlay",
        "label": "全图叠加",
        "category": "static",
        "type": "content",
        "title": "全图展示",
        "sample": DEFAULT_CONTENT_FULL_IMAGE,
    },
    {
        "class": ComparisonGenerator,
        "name": "comparison",
        "label": "对比布局",
        "category": "static",
        "type": "content",
        "title": "方案对比",
        "sample": DEFAULT_CONTENT_COMPARISON,
    },

    # ========== 团队介绍 ==========
    {
        "class": TeamGridGenerator,
        "name": "team_grid",
        "label": "团队网格",
        "category": "static",
        "type": "team",
        "title": "核心团队",
        "use_members": True,
    },
    {
        "class": PersonCardGenerator,
        "name": "person_card",
        "label": "人物介绍卡片",
        "category": "static",
        "type": "team",
        "title": "人物介绍",
    },
    {
        "class": OrgChartGenerator,
        "name": "org_chart",
        "label": "组织架构图",
        "category": "static",
        "type": "team",
        "title": "组织架构",
    },

    # ========== 结尾页 ==========
    {
        "class": ThankYouGenerator,
        "name": "thank_you",
        "label": "感谢页",
        "category": "static",
        "type": "ending",
        "title": "谢谢",
    },
    {
        "class": QRCodeGenerator,
        "name": "qr_code",
        "label": "二维码页",
        "category": "static",
        "type": "ending",
        "title": "扫码关注",
    },
    {
        "class": ContactPageGenerator,
        "name": "contact",
        "label": "联系方式页",
        "category": "static",
        "type": "ending",
        "title": "联系我们",
    },
]


# ============================================================
# 示例数据
# ============================================================

# 默认目录项数据
DEFAULT_DIR_ITEMS = [
    {"number": "01", "title": "项目概述", "description": "项目背景与目标"},
    {"number": "02", "title": "市场分析", "description": "行业趋势与竞争格局"},
    {"number": "03", "title": "产品设计", "description": "核心功能与用户体验"},
    {"number": "04", "title": "技术方案", "description": "架构设计与技术选型"},
    {"number": "05", "title": "运营计划", "description": "推广策略与执行路径"},
    {"number": "06", "title": "财务规划", "description": "预算编制与收益预测"},
]

# 默认时间轴事件数据
DEFAULT_TIMELINE_EVENTS = [
    {"label": "公司成立", "date": "2020", "detail": "初创团队组建"},
    {"label": "产品研发", "date": "2021", "detail": "核心产品上线"},
    {"label": "市场拓展", "date": "2022", "detail": "全国市场布局"},
    {"label": "A轮融资", "date": "2023", "detail": "完成千万融资"},
    {"label": "国际化", "date": "2024", "detail": "海外市场开拓"},
]

# 默认团队成员数据
DEFAULT_TEAM_MEMBERS = [
    {"name": "张明", "title": "CEO 首席执行官"},
    {"name": "李华", "title": "CTO 首席技术官"},
    {"name": "王芳", "title": "CPO 首席产品官"},
    {"name": "赵强", "title": "CFO 首席财务官"},
    {"name": "陈静", "title": "COO 首席运营官"},
    {"name": "刘伟", "title": "CMO 首席营销官"},
]

# ============================================================
# 核心生成逻辑
# ============================================================

def ensure_output_dirs(base_dir):
    """创建所有必要的输出目录

    Args:
        base_dir: 模板输出根目录
    """
    subdirs = [
        "animated/cover",
        "animated/directory",
        "animated/timeline",
        "animated/chart",
        "animated/transition",
        "static/cover",
        "static/directory",
        "static/timeline",
        "static/chart",
        "static/content",
        "static/ending",
        "static/team",
        "complete",
    ]
    for subdir in subdirs:
        os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)


def generate_template(template_info, theme, base_dir):
    """生成单个模板

    Args:
        template_info: 模板注册表条目
        theme: 主题对象
        base_dir: 输出根目录

    Returns:
        dict: 包含 success, filepath, elapsed, error 的结果字典
    """
    start = time.time()
    result = {
        "success": False,
        "filepath": "",
        "elapsed": 0,
        "error": None,
    }

    try:
        # 实例化生成器
        gen = template_info["class"](theme=theme)

        # 设置标题
        if hasattr(gen, "set_title"):
            gen.set_title(template_info["title"])

        # 封面需要设置副标题
        if "subtitle" in template_info:
            if hasattr(gen, "set_subtitle"):
                gen.set_subtitle(template_info["subtitle"])

        # 设置数据
        if template_info.get("use_items"):
            if hasattr(gen, "set_items"):
                gen.set_items(DEFAULT_DIR_ITEMS)
            elif hasattr(gen, "set_data"):
                gen.set_data(DEFAULT_DIR_ITEMS)

        if template_info.get("use_events"):
            if hasattr(gen, "set_data"):
                gen.set_data(DEFAULT_TIMELINE_EVENTS)

        if template_info.get("use_members"):
            if hasattr(gen, "set_members"):
                gen.set_members(DEFAULT_TEAM_MEMBERS)

        # 设置示例数据：优先 set_items，其次 set_data。
        # sample 为元组时表示 set_data 需要多个位置参数（如 LineChart 的 series + x_labels）。
        if "sample" in template_info:
            sample = template_info["sample"]
            if hasattr(gen, "set_items"):
                gen.set_items(sample)
            elif isinstance(sample, tuple):
                gen.set_data(*sample)
            else:
                gen.set_data(sample)

        # 生成
        gen.generate()

        # 构建输出路径（包含主题名避免覆盖）
        category = template_info["category"]
        page_type = template_info["type"]
        theme_key = [k for k, v in ALL_THEMES.items() if type(theme) is v]
        theme_name = theme_key[0] if theme_key else "default"
        filename = f"{template_info['name']}_{theme_name}.pptx"
        filepath = os.path.join(base_dir, category, page_type, filename)
        result["filepath"] = filepath

        # 保存
        gen.save(filepath)

        result["success"] = True
    except Exception as e:
        result["error"] = str(e)

    result["elapsed"] = time.time() - start
    return result


def run_generation(themes_filter=None, types_filter=None, output_dir=None):
    """执行批量生成

    Args:
        themes_filter: 主题过滤列表（theme_key列表），None表示全部
        types_filter: 类型过滤列表（cover/directory/timeline/chart/content/team/ending），None表示全部
        output_dir: 输出目录，None则使用默认的 templates/

    Returns:
        dict: 生成统计结果
    """
    # 确定输出目录
    if output_dir is None:
        base_dir = os.path.join(project_root, "templates")
    else:
        base_dir = output_dir

    ensure_output_dirs(base_dir)

    # 确定要生成的主题
    if themes_filter:
        themes_to_gen = {k: v for k, v in ALL_THEMES.items() if k in themes_filter}
    else:
        themes_to_gen = ALL_THEMES

    # 确定要生成的模板类型
    if types_filter:
        templates_to_gen = [
            t for t in TEMPLATE_REGISTRY
            if t["type"] in types_filter
        ]
    else:
        templates_to_gen = TEMPLATE_REGISTRY

    # 统计
    stats = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "total_time": 0.0,
        "results": [],
    }

    print(f"\n  输出目录: {base_dir}")
    print(f"  主题数: {len(themes_to_gen)}")
    print(f"  模板类型数: {len(templates_to_gen)}")
    print(f"  预计生成: {len(themes_to_gen) * len(templates_to_gen)} 个文件")

    # 遍历主题
    for theme_key, theme_cls in themes_to_gen.items():
        theme = theme_cls()
        print(f"\n{'━' * 60}")
        print(f"  主题: {theme.name}")
        print(f"{'━' * 60}")

        for tmpl in templates_to_gen:
            stats["total"] += 1

            result = generate_template(tmpl, theme, base_dir)

            status = "[OK]" if result["success"] else "[FAIL]"
            label = tmpl["label"]
            elapsed = result["elapsed"]

            if result["success"]:
                stats["success"] += 1
                filename = os.path.basename(result["filepath"])
                print(f"  {status} {label:<20} {filename:<45} {elapsed:.2f}s")
            else:
                stats["failed"] += 1
                print(f"  {status} {label:<20} 错误: {result['error']}")

            stats["results"].append({
                "theme": theme.name,
                "label": label,
                "category": tmpl["category"],
                "type": tmpl["type"],
                "success": result["success"],
                "filepath": result["filepath"],
                "elapsed": result["elapsed"],
                "error": result["error"],
            })

            stats["total_time"] += result["elapsed"]

    return stats


def print_summary(stats):
    """打印生成汇总报告

    Args:
        stats: 统计结果字典
    """
    print("\n" + "=" * 60)
    print("  生成汇总报告")
    print("=" * 60)
    print(f"  总计: {stats['total']} 个模板")
    print(f"  成功: {stats['success']} 个")
    print(f"  失败: {stats['failed']} 个")
    print(f"  总耗时: {stats['total_time']:.2f} 秒")
    if stats['total'] > 0:
        avg_time = stats['total_time'] / stats['total']
        print(f"  平均耗时: {avg_time:.2f} 秒/模板")

    # 按类别统计
    categories = {}
    for r in stats["results"]:
        cat = r["type"]
        if cat not in categories:
            categories[cat] = {"total": 0, "success": 0}
        categories[cat]["total"] += 1
        if r["success"]:
            categories[cat]["success"] += 1

    print("\n  按类别统计:")
    for cat, count in categories.items():
        print(f"    {cat:<12} {count['success']}/{count['total']} 成功")

    # 失败详情
    failures = [r for r in stats["results"] if not r["success"]]
    if failures:
        print("\n  失败详情:")
        for f in failures:
            print(f"    [{f['theme']}] {f['label']}: {f['error']}")

    print("=" * 60)


# ============================================================
# 命令行入口
# ============================================================

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="PPT模板资源库 - 主生成脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/generate_all.py                         # 生成所有模板
  python scripts/generate_all.py --theme blue_technology # 只生成蓝色科技主题
  python scripts/generate_all.py --type cover            # 只生成封面模板
  python scripts/generate_all.py --output ./my_templates # 指定输出目录

可用主题:
  blue_technology  - 蓝色科技
  purple_gradient  - 紫色渐变
  dark_gold        - 暗金奢华
  minimalist_bw    - 极简黑白
  ocean_blue       - 海洋蓝
  green_nature     - 自然绿
  red_business     - 红色商务

可用类型:
  cover       - 封面模板
  directory   - 目录模板
  timeline    - 时间轴模板
  chart       - 图表模板
  content     - 内容页模板
  team        - 团队介绍模板
  ending      - 结尾页模板
        """,
    )
    parser.add_argument(
        "--theme", "-t",
        nargs="+",
        help="指定主题（可多个），如: --theme blue_technology purple_gradient",
    )
    parser.add_argument(
        "--type", "-T",
        nargs="+",
        help="指定模板类型（可多个），如: --type cover directory",
    )
    parser.add_argument(
        "--output", "-o",
        help="指定输出目录（默认: templates/）",
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="列出所有可用主题",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="列出所有注册模板",
    )
    return parser.parse_args()


def list_themes():
    """列出所有可用主题"""
    print("\n可用主题:")
    print(f"  {'key':<20} {'名称':<12} {'主色'}")
    print(f"  {'─'*20} {'─'*12} {'─'*10}")
    for key, cls in ALL_THEMES.items():
        theme = cls()
        print(f"  {key:<20} {theme.name:<12} {theme.primary}")


def list_templates():
    """列出所有注册模板"""
    print("\n已注册模板:")
    print(f"  {'标签':<16} {'类别':<8} {'类型':<10} {'文件名'}")
    print(f"  {'─'*16} {'─'*8} {'─'*10} {'─'*35}")
    for tmpl in TEMPLATE_REGISTRY:
        filename = f"{tmpl['type']}_{tmpl['category']}_{tmpl['name']}.pptx"
        print(f"  {tmpl['label']:<16} {tmpl['category']:<8} {tmpl['type']:<10} {filename}")


def main():
    """主入口函数"""
    args = parse_args()

    # 列出信息
    if args.list_themes:
        list_themes()
        return
    if args.list_templates:
        list_templates()
        return

    print("=" * 60)
    print("  PPT模板资源库 - 主生成脚本")
    print("  generate_all.py")
    print("=" * 60)

    # 执行生成
    start_time = time.time()
    stats = run_generation(
        themes_filter=args.theme,
        types_filter=args.type,
        output_dir=args.output,
    )
    elapsed = time.time() - start_time

    # 打印汇总
    print_summary(stats)

    print(f"\n  脚本总耗时: {elapsed:.2f} 秒")

    # 返回状态码
    sys.exit(0 if stats["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
