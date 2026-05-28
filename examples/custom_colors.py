"""
自定义配色示例 - PPT模板资源库

本示例演示如何创建自定义主题配色，并将其应用到生成器中。
运行方式：python examples/custom_colors.py
"""

import sys
import os

# 确保项目根目录在搜索路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pptx.dml.color import RGBColor
from themes import BaseTheme, ALL_THEMES
from python.generators_cover import GeometricRotationCover, CircleRingCover, TrainMistCover
from python.generators_directory.diamond_animated import DiamondAnimatedGenerator


# ============================================================
# 方法一：继承BaseTheme创建完整自定义主题
# ============================================================

class TechOrangeTheme(BaseTheme):
    """科技橙主题 - 适合活力、创新类演示"""
    name = "科技橙"
    primary = RGBColor(255, 107, 53)    # #FF6B35
    secondary = RGBColor(255, 166, 43)  # #FFA62B
    accent = RGBColor(43, 87, 154)      # #2B579A
    background = RGBColor(250, 250, 250) # #FAFAFA
    text = RGBColor(40, 40, 40)         # #282828
    muted = RGBColor(140, 140, 140)     # #8C8C8C
    dark_bg = RGBColor(30, 30, 30)      # #1E1E1E


class ForestGreenTheme(BaseTheme):
    """森林绿主题 - 适合环保、自然类演示"""
    name = "森林绿"
    primary = RGBColor(34, 139, 87)     # #228B57
    secondary = RGBColor(107, 181, 132) # #6BB584
    accent = RGBColor(218, 165, 105)    # #DAA569
    background = RGBColor(248, 253, 248) # #F8FDF8
    text = RGBColor(33, 60, 42)         # #213C2A
    muted = RGBColor(120, 150, 130)     # #789682
    dark_bg = RGBColor(15, 30, 20)      # #0F1E14


# ============================================================
# 方法二：动态创建临时主题（不需要定义新类）
# ============================================================

def create_dynamic_theme(name, primary_hex, secondary_hex, accent_hex=None):
    """动态创建一个临时主题对象

    通过动态设置类属性的方式快速创建主题，无需继承BaseTheme。
    适合一次性使用或批量测试不同配色的场景。

    Args:
        name: 主题名称
        primary_hex: 主色十六进制（如 "#FF5733"）
        secondary_hex: 副色十六进制
        accent_hex: 强调色十六进制（可选）

    Returns:
        BaseTheme的实例对象
    """
    # 创建一个动态主题类
    DynamicTheme = type(
        f"DynamicTheme_{name}",
        (BaseTheme,),
        {
            "name": name,
            "primary": _hex_to_rgb(primary_hex),
            "secondary": _hex_to_rgb(secondary_hex),
            "accent": _hex_to_rgb(accent_hex or primary_hex),
            "background": RGBColor(255, 255, 255),
            "text": RGBColor(33, 33, 33),
            "muted": RGBColor(158, 158, 158),
            "dark_bg": RGBColor(26, 26, 46),
        },
    )
    return DynamicTheme()


def _hex_to_rgb(hex_color):
    """十六进制颜色字符串转RGBColor"""
    hex_color = hex_color.lstrip("#")
    return RGBColor(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


# ============================================================
# 演示部分
# ============================================================

def demo_existing_themes():
    """展示所有内置主题"""
    print("\n--- 内置主题列表 ---")
    for key, theme_cls in ALL_THEMES.items():
        theme = theme_cls()
        print(f"  {key}: {theme.name}  (主色: {theme.primary})")


def demo_custom_class_theme():
    """使用自定义类主题生成封面"""
    print("\n--- 使用自定义类主题: 科技橙 ---")
    theme = TechOrangeTheme()

    cover = GeometricRotationCover(theme=theme)
    cover.set_title("创新科技峰会")
    cover.set_subtitle("Innovation Tech Summit 2026")
    cover.generate()

    output = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "output_custom_orange.pptx")
    )
    cover.save(output)
    print(f"  已保存: {output}")
    return output


def demo_dynamic_theme():
    """使用动态主题生成封面"""
    print("\n--- 使用动态创建主题 ---")

    # 创建一个珊瑚粉主题
    coral_theme = create_dynamic_theme(
        name="珊瑚粉",
        primary_hex="#FF6B6B",
        secondary_hex="#FFA07A",
        accent_hex="#FFD93D",
    )
    print(f"  主题名: {coral_theme.name}")

    cover = CircleRingCover(theme=coral_theme)
    cover.set_title("粉色梦幻")
    cover.set_subtitle("Coral Pink Theme")
    cover.generate()

    output = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "output_custom_coral.pptx")
    )
    cover.save(output)
    print(f"  已保存: {output}")
    return output


def demo_theme_comparison():
    """同一模板使用不同主题生成，对比效果"""
    print("\n--- 主题对比: 同一目录页使用不同主题 ---")

    items = [
        {"number": "01", "title": "项目概述", "subtitle": "Overview"},
        {"number": "02", "title": "市场分析", "subtitle": "Market"},
        {"number": "03", "title": "产品设计", "subtitle": "Design"},
        {"number": "04", "title": "运营计划", "subtitle": "Operation"},
        {"number": "05", "title": "财务预测", "subtitle": "Finance"},
        {"number": "06", "title": "风险控制", "subtitle": "Risk"},
    ]

    # 选择几个有代表性的主题进行对比
    comparison_themes = [
        ("blue_technology", ALL_THEMES["blue_technology"]()),
        ("purple_gradient", ALL_THEMES["purple_gradient"]()),
        ("forest_green", ForestGreenTheme()),
    ]

    outputs = []
    for theme_key, theme in comparison_themes:
        gen = DiamondAnimatedGenerator(theme=theme)
        gen.set_title(f"{theme.name} - 目录")
        gen.set_items(items)
        gen.generate()

        output = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", f"output_theme_{theme_key}.pptx")
        )
        gen.save(output)
        outputs.append(output)
        print(f"  [{theme.name}] 已保存: {output}")

    return outputs


def main():
    """主函数"""
    print("=" * 55)
    print("  PPT模板资源库 - 自定义配色示例")
    print("=" * 55)

    # 1. 展示内置主题
    demo_existing_themes()

    # 2. 自定义类主题
    demo_custom_class_theme()

    # 3. 动态主题
    demo_dynamic_theme()

    # 4. 主题对比
    demo_theme_comparison()

    print("\n" + "=" * 55)
    print("  全部完成！")
    print("")
    print("  自定义主题的两种方式：")
    print("  方式1: 继承 BaseTheme 类，定义类属性（推荐，可复用）")
    print("  方式2: 使用 create_dynamic_theme() 函数（适合一次性使用）")
    print("")
    print("  提示：主题对象只需包含 primary、secondary、accent、")
    print("  background、text、muted、dark_bg 属性即可。")
    print("=" * 55)


if __name__ == "__main__":
    main()
