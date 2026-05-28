"""
批量生成示例 - PPT模板资源库

本示例演示如何批量生成所有模板，遍历所有主题和生成器，
将生成的文件按类别组织到 templates/ 目录中。
运行方式：python examples/batch_generate.py
"""

import sys
import os
import time

# 确保项目根目录在搜索路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pptx.dml.color import RGBColor

from themes import ALL_THEMES
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
from python.generators_directory.diamond_animated import DiamondAnimatedGenerator
from python.generators_directory.circular_ring import CircularRingGenerator
from python.generators_directory.hexagon import HexagonGenerator
from python.generators_directory.sidebar import SidebarGenerator
from python.generators_directory.card_grid import CardGridGenerator


# ============================================================
# 配置：定义要生成的所有模板
# ============================================================

# 动画封面模板
ANIMATED_COVERS = [
    {
        "class": GeometricRotationCover,
        "name": "geometric_rotation",
        "label": "几何旋转封面",
        "title": "几何旋转封面",
        "subtitle": "Geometric Rotation Cover",
    },
    {
        "class": CircleRingCover,
        "name": "circle_ring",
        "label": "圆环转场封面",
        "title": "圆环转场封面",
        "subtitle": "Circle Ring Cover",
    },
    {
        "class": TrainMistCover,
        "name": "train_mist",
        "label": "列车穿雾封面",
        "title": "列车穿雾封面",
        "subtitle": "Train Mist Cover",
    },
    {
        "class": DiamondRevealCover,
        "name": "diamond_reveal",
        "label": "钻石揭示封面",
        "title": "钻石揭示封面",
        "subtitle": "Diamond Reveal Cover",
    },
]

# 静态封面模板
STATIC_COVERS = [
    {
        "class": MinimalistGradientCover,
        "name": "minimalist_gradient",
        "label": "极简渐变封面",
        "title": "极简渐变封面",
        "subtitle": "Minimalist Gradient Cover",
    },
    {
        "class": SplitScreenCover,
        "name": "split_screen",
        "label": "分屏封面",
        "title": "分屏封面",
        "subtitle": "Split Screen Cover",
    },
    {
        "class": HollowMaskCover,
        "name": "hollow_mask",
        "label": "镂空遮罩封面",
        "title": "镂空遮罩封面",
        "subtitle": "Hollow Mask Cover",
    },
    {
        "class": LayeredDepthCover,
        "name": "layered_depth",
        "label": "层次深度封面",
        "title": "层次深度封面",
        "subtitle": "Layered Depth Cover",
    },
]

# 动画目录模板
ANIMATED_DIRECTORIES = [
    {
        "class": DiamondAnimatedGenerator,
        "name": "diamond_animated",
        "label": "菱形动画目录",
        "title": "内容概览",
    },
    {
        "class": CircularRingGenerator,
        "name": "circular_ring",
        "label": "圆环目录",
        "title": "目录导航",
    },
    {
        "class": HexagonGenerator,
        "name": "hexagon",
        "label": "六边形目录",
        "title": "蜂巢目录",
    },
]

# 静态目录模板
STATIC_DIRECTORIES = [
    {
        "class": SidebarGenerator,
        "name": "sidebar",
        "label": "侧边栏目录",
        "title": "目录",
    },
    {
        "class": CardGridGenerator,
        "name": "card_grid",
        "label": "卡片网格目录",
        "title": "内容概览",
    },
]

# 目录模板的默认数据
DEFAULT_DIR_ITEMS = [
    {"number": "01", "title": "项目概述", "description": "项目背景与目标"},
    {"number": "02", "title": "市场分析", "description": "行业趋势与竞争格局"},
    {"number": "03", "title": "产品设计", "description": "核心功能与用户体验"},
    {"number": "04", "title": "技术方案", "description": "架构设计与技术选型"},
    {"number": "05", "title": "运营计划", "description": "推广策略与执行路径"},
    {"number": "06", "title": "财务规划", "description": "预算编制与收益预测"},
]


# ============================================================
# 生成函数
# ============================================================

def ensure_dir(path):
    """确保目录存在，不存在则创建"""
    os.makedirs(path, exist_ok=True)


def generate_cover(generator_config, theme, output_dir):
    """生成单个封面模板

    Args:
        generator_config: 模板配置字典
        theme: 主题对象
        output_dir: 输出目录

    Returns:
        tuple: (是否成功, 文件路径, 耗时秒数)
    """
    start = time.time()
    try:
        gen = generator_config["class"](theme=theme)

        # 设置标题（封面使用set_title链式调用）
        if hasattr(gen, "set_subtitle"):
            gen.set_title(generator_config["title"])
            gen.set_subtitle(generator_config["subtitle"])
        else:
            gen.set_title(generator_config["title"])

        gen.generate()

        filename = f"cover_animated_{generator_config['name']}.pptx" \
            if generator_config["class"] in [c["class"] for c in ANIMATED_COVERS] \
            else f"cover_static_{generator_config['name']}.pptx"
        filepath = os.path.join(output_dir, filename)
        gen.save(filepath)

        elapsed = time.time() - start
        return True, filepath, elapsed
    except Exception as e:
        elapsed = time.time() - start
        return False, str(e), elapsed


def generate_directory(generator_config, theme, output_dir):
    """生成单个目录模板

    Args:
        generator_config: 模板配置字典
        theme: 主题对象
        output_dir: 输出目录

    Returns:
        tuple: (是否成功, 文件路径, 耗时秒数)
    """
    start = time.time()
    try:
        gen = generator_config["class"](theme=theme)
        gen.set_title(generator_config["title"])

        # 目录模板需要设置数据项
        if hasattr(gen, "set_items"):
            gen.set_items(DEFAULT_DIR_ITEMS)

        gen.generate()

        is_animated = generator_config["class"] in [c["class"] for c in ANIMATED_DIRECTORIES]
        category = "animated" if is_animated else "static"
        filename = f"directory_{category}_{generator_config['name']}.pptx"
        filepath = os.path.join(output_dir, filename)
        gen.save(filepath)

        elapsed = time.time() - start
        return True, filepath, elapsed
    except Exception as e:
        elapsed = time.time() - start
        return False, str(e), elapsed


# ============================================================
# 主流程
# ============================================================

def main():
    """主函数：遍历所有主题和生成器，批量生成模板"""
    print("=" * 60)
    print("  PPT模板资源库 - 批量生成工具")
    print("=" * 60)

    # 项目根目录
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    templates_dir = os.path.join(project_root, "templates")

    # 创建输出目录结构
    animated_dir = os.path.join(templates_dir, "animated")
    static_dir = os.path.join(templates_dir, "static")
    ensure_dir(os.path.join(animated_dir, "cover"))
    ensure_dir(os.path.join(animated_dir, "directory"))
    ensure_dir(os.path.join(animated_dir, "timeline"))
    ensure_dir(os.path.join(animated_dir, "chart"))
    ensure_dir(os.path.join(animated_dir, "transition"))
    ensure_dir(os.path.join(static_dir, "cover"))
    ensure_dir(os.path.join(static_dir, "directory"))
    ensure_dir(os.path.join(static_dir, "timeline"))
    ensure_dir(os.path.join(static_dir, "chart"))
    ensure_dir(os.path.join(static_dir, "content"))
    ensure_dir(os.path.join(static_dir, "ending"))
    ensure_dir(os.path.join(static_dir, "team"))

    # 统计信息
    total_count = 0
    success_count = 0
    fail_count = 0
    total_time = 0.0
    results = []

    # ---- 遍历所有主题 ----
    for theme_key, theme_cls in ALL_THEMES.items():
        theme = theme_cls()
        print(f"\n{'─' * 60}")
        print(f"  主题: {theme.name} ({theme_key})")
        print(f"{'─' * 60}")

        # 动画封面
        print("  [动画封面]")
        for config in ANIMATED_COVERS:
            total_count += 1
            ok, path, elapsed = generate_cover(
                config, theme,
                os.path.join(animated_dir, "cover"),
            )
            total_time += elapsed
            if ok:
                success_count += 1
                results.append((theme.name, "动画封面", config["label"], os.path.basename(path), elapsed))
                print(f"    [OK] {config['label']} ({elapsed:.2f}s)")
            else:
                fail_count += 1
                print(f"    [FAIL] {config['label']}: {path}")

        # 静态封面
        print("  [静态封面]")
        for config in STATIC_COVERS:
            total_count += 1
            ok, path, elapsed = generate_cover(
                config, theme,
                os.path.join(static_dir, "cover"),
            )
            total_time += elapsed
            if ok:
                success_count += 1
                results.append((theme.name, "静态封面", config["label"], os.path.basename(path), elapsed))
                print(f"    [OK] {config['label']} ({elapsed:.2f}s)")
            else:
                fail_count += 1
                print(f"    [FAIL] {config['label']}: {path}")

        # 动画目录
        print("  [动画目录]")
        for config in ANIMATED_DIRECTORIES:
            total_count += 1
            ok, path, elapsed = generate_directory(
                config, theme,
                os.path.join(animated_dir, "directory"),
            )
            total_time += elapsed
            if ok:
                success_count += 1
                results.append((theme.name, "动画目录", config["label"], os.path.basename(path), elapsed))
                print(f"    [OK] {config['label']} ({elapsed:.2f}s)")
            else:
                fail_count += 1
                print(f"    [FAIL] {config['label']}: {path}")

        # 静态目录
        print("  [静态目录]")
        for config in STATIC_DIRECTORIES:
            total_count += 1
            ok, path, elapsed = generate_directory(
                config, theme,
                os.path.join(static_dir, "directory"),
            )
            total_time += elapsed
            if ok:
                success_count += 1
                results.append((theme.name, "静态目录", config["label"], os.path.basename(path), elapsed))
                print(f"    [OK] {config['label']} ({elapsed:.2f}s)")
            else:
                fail_count += 1
                print(f"    [FAIL] {config['label']}: {path}")

    # ---- 输出汇总 ----
    print("\n" + "=" * 60)
    print("  批量生成完成！")
    print(f"  总模板数: {total_count}")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  总耗时: {total_time:.2f}s")
    print(f"  输出目录: {templates_dir}")
    print("")

    # 输出详细结果表
    if results:
        print("  生成详情：")
        print(f"  {'主题':<10} {'类别':<8} {'模板名':<16} {'文件名':<40} {'耗时'}")
        print(f"  {'─'*10} {'─'*8} {'─'*16} {'─'*40} {'─'*8}")
        for theme_name, category, label, filename, elapsed in results:
            print(f"  {theme_name:<10} {category:<8} {label:<16} {filename:<40} {elapsed:.2f}s")

    print("=" * 60)


if __name__ == "__main__":
    main()
