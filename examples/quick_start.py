"""
快速入门示例 - PPT模板资源库

本示例演示如何快速生成一个包含封面、内容页和结束页的简单演示文稿。
运行方式：python examples/quick_start.py
"""

import sys
import os

# 确保项目根目录在搜索路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from python.base import TemplateGenerator
from python.generators_cover import GeometricRotationCover, DiamondRevealCover
from themes import ALL_THEMES


def create_simple_content_page(theme, title, content_items):
    """创建一个简洁的内容页

    Args:
        theme: 主题对象
        title: 页面标题
        content_items: 内容列表，每项为字符串

    Returns:
        TemplateGenerator: 生成器实例（用于链式调用save）
    """
    gen = TemplateGenerator(theme=theme)
    gen.create_slide()

    slide_w = Inches(10)
    slide_h = Inches(7.5)

    # 获取主题色（优先使用主题，否则使用默认色）
    primary = getattr(theme, "primary", RGBColor(0, 102, 204))
    text_color = getattr(theme, "text", RGBColor(33, 33, 33))
    muted = getattr(theme, "muted", RGBColor(158, 158, 158))

    # 背景色（取主题背景色，若无则白色）
    bg_color = getattr(theme, "background", RGBColor(255, 255, 255))

    # 绘制背景
    gen.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, slide_w, slide_h,
        fill_color=bg_color,
    )

    # 顶部装饰条
    gen.add_gradient_shape(
        MSO_SHAPE.RECTANGLE,
        0, 0, slide_w, Inches(0.06),
        [primary, getattr(theme, "secondary", primary)],
    )

    # 标题
    gen.add_textbox(
        title,
        Inches(0.8), Inches(0.5), Inches(8.4), Inches(0.8),
        font_size=28,
        font_color=text_color,
        bold=True,
        alignment=PP_ALIGN.LEFT,
    )

    # 装饰线
    gen.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(1.35), Inches(1.2), Inches(0.04),
        fill_color=primary,
    )

    # 内容条目
    y_start = Inches(1.8)
    for i, item in enumerate(content_items):
        y_pos = y_start + Inches(i * 0.65)

        # 序号圆点
        dot_size = Inches(0.35)
        gen.add_shape(
            MSO_SHAPE.OVAL,
            Inches(1.0), y_pos, dot_size, dot_size,
            fill_color=primary,
        )
        # 序号文字
        gen.add_textbox(
            str(i + 1),
            Inches(1.0), y_pos + Inches(0.02),
            dot_size, dot_size,
            font_size=14,
            font_color=RGBColor(255, 255, 255),
            bold=True,
            alignment=PP_ALIGN.CENTER,
        )

        # 内容文字
        gen.add_textbox(
            item,
            Inches(1.6), y_pos + Inches(0.03),
            Inches(7.5), Inches(0.35),
            font_size=16,
            font_color=text_color,
        )

    return gen


def create_simple_ending(theme, title="感谢聆听", subtitle="Thank You"):
    """创建一个简洁的结束页

    Args:
        theme: 主题对象
        title: 主标题
        subtitle: 副标题

    Returns:
        TemplateGenerator: 生成器实例
    """
    gen = TemplateGenerator(theme=theme)
    gen.create_slide()

    slide_w = Inches(10)
    slide_h = Inches(7.5)

    primary = getattr(theme, "primary", RGBColor(0, 102, 204))
    secondary = getattr(theme, "secondary", primary)
    dark_bg = getattr(theme, "dark_bg", RGBColor(26, 26, 46))

    # 深色背景渐变
    gen.add_gradient_shape(
        MSO_SHAPE.RECTANGLE,
        0, 0, slide_w, slide_h,
        [dark_bg, primary],
    )

    # 装饰圆
    gen.add_shape(
        MSO_SHAPE.OVAL,
        Inches(3.5), Inches(2.0), Inches(3.0), Inches(3.0),
        fill_color=secondary,
    )
    # 圆上添加透明覆盖
    from python.utils import set_shape_transparency
    circle = gen.slide.shapes[-1]
    set_shape_transparency(circle, 0.85)

    # 主标题
    gen.add_textbox(
        title,
        Inches(1.5), Inches(2.5), Inches(7.0), Inches(1.2),
        font_size=42,
        font_color=RGBColor(255, 255, 255),
        bold=True,
        alignment=PP_ALIGN.CENTER,
    )

    # 副标题
    gen.add_textbox(
        subtitle,
        Inches(1.5), Inches(3.8), Inches(7.0), Inches(0.6),
        font_size=20,
        font_color=getattr(theme, "muted", RGBColor(180, 180, 180)),
        alignment=PP_ALIGN.CENTER,
    )

    return gen


def main():
    """主函数：生成一个完整的简单演示文稿"""
    print("=" * 50)
    print("  PPT模板资源库 - 快速入门示例")
    print("=" * 50)

    # ---- 第一步：选择主题 ----
    # 可用主题：blue_technology, purple_gradient, dark_gold,
    #           minimalist_bw, ocean_blue, green_nature, red_business
    theme_name = "blue_technology"
    theme = ALL_THEMES[theme_name]()
    print(f"\n[1/4] 已选择主题: {theme.name}")

    # ---- 第二步：生成封面 ----
    print("[2/4] 正在生成封面...")
    cover = GeometricRotationCover(theme=theme)
    cover.set_title("PPT模板演示")
    cover.set_subtitle("快速入门 · Quick Start")
    cover.generate()
    cover_path = os.path.join(os.path.dirname(__file__), "..", "output_quick_cover.pptx")
    cover_path = os.path.abspath(cover_path)
    cover.save(cover_path)
    print(f"       封面已保存: {cover_path}")

    # ---- 第三步：生成内容页 ----
    print("[3/4] 正在生成内容页...")
    content = create_simple_content_page(
        theme,
        "项目概述",
        [
            "项目背景与目标：明确方向，聚焦核心价值",
            "技术架构设计：模块化、可扩展、高可用",
            "实施计划：分阶段推进，确保按时交付",
            "团队分工：跨部门协作，明确责任到人",
            "风险控制：提前识别风险，制定应对策略",
            "预期成果：量化目标，确保投资回报",
        ],
    )
    content_path = os.path.join(os.path.dirname(__file__), "..", "output_quick_content.pptx")
    content_path = os.path.abspath(content_path)
    content.save(content_path)
    print(f"       内容页已保存: {content_path}")

    # ---- 第四步：生成结束页 ----
    print("[4/4] 正在生成结束页...")
    ending = create_simple_ending(theme, "感谢聆听", "Thank You for Watching")
    ending_path = os.path.join(os.path.dirname(__file__), "..", "output_quick_ending.pptx")
    ending_path = os.path.abspath(ending_path)
    ending.save(ending_path)
    print(f"       结束页已保存: {ending_path}")

    # ---- 汇总 ----
    print("\n" + "=" * 50)
    print("  生成完成！共生成 3 个文件：")
    print(f"  1. {os.path.basename(cover_path)}")
    print(f"  2. {os.path.basename(content_path)}")
    print(f"  3. {os.path.basename(ending_path)}")
    print("")
    print("  提示：可以将这些页面合并为一个演示文稿，")
    print("  或单独使用某个页面作为模板。")
    print("=" * 50)


if __name__ == "__main__":
    main()
