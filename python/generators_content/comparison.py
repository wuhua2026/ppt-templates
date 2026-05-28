"""对比布局 - 双栏对比 + 中间VS分隔"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb


class ComparisonGenerator(TemplateGenerator):
    """对比布局生成器"""

    def __init__(self, theme=None):
        super().__init__(theme=theme)
        self.items = []
        self.title = "对比布局"
        self.left_color = hex_to_rgb("#1976D2")
        self.right_color = hex_to_rgb("#E53935")
        self.vs_color = hex_to_rgb("#FF6F00")

    def set_title(self, title):
        self.title = title

    def set_items(self, items):
        """设置对比内容
        items: list of dict with keys:
            'left_title', 'right_title',
            'left_items': list of str, 'right_items': list of str
        Each item becomes one slide.
        """
        self.items = items

    def generate(self):
        for item in self.items:
            self.create_slide()
            self._add_background()
            self._add_title()
            self._add_comparison_columns(item)
            self._add_vs_divider()
            self._add_bottom_accent()
        return self

    def _add_background(self):
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(10), Inches(7.5),
            fill_color=hex_to_rgb("#FFFFFF"),
        )

    def _add_title(self):
        self.add_textbox(
            self.title,
            Inches(0.5), Inches(0.3), Inches(9), Inches(0.6),
            font_size=28, font_color=hex_to_rgb("#333333"),
            bold=True, alignment=PP_ALIGN.CENTER,
        )

    def _add_comparison_columns(self, item):
        col_w = Inches(3.8)
        col_h = Inches(5.0)
        left_x = Inches(0.6)
        right_x = Inches(5.6)
        start_y = Inches(1.3)

        # Left column card
        left_card = self.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left_x, start_y, col_w, col_h,
            fill_color=hex_to_rgb("#F5F8FF"),
        )
        # Left top color bar
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            left_x, start_y,
            col_w, Inches(0.06),
            fill_color=self.left_color,
        )

        # Left title
        self.add_textbox(
            item.get("left_title", ""),
            left_x + Inches(0.3), start_y + Inches(0.3),
            col_w - Inches(0.6), Inches(0.5),
            font_size=20, font_color=self.left_color,
            bold=True, alignment=PP_ALIGN.CENTER,
        )

        # Left items
        left_items = item.get("left_items", [])
        for j, text in enumerate(left_items):
            item_y = start_y + Inches(1.1) + j * Inches(0.7)
            # Bullet circle
            self.add_shape(
                MSO_SHAPE.OVAL,
                left_x + Inches(0.3), item_y + Inches(0.05),
                Inches(0.18), Inches(0.18),
                fill_color=self.left_color,
            )
            # Text
            self.add_textbox(
                text,
                left_x + Inches(0.6), item_y,
                col_w - Inches(0.9), Inches(0.35),
                font_size=12, font_color=hex_to_rgb("#424242"),
                alignment=PP_ALIGN.LEFT,
            )

        # Right column card
        right_card = self.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            right_x, start_y, col_w, col_h,
            fill_color=hex_to_rgb("#FFF5F5"),
        )
        # Right top color bar
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            right_x, start_y,
            col_w, Inches(0.06),
            fill_color=self.right_color,
        )

        # Right title
        self.add_textbox(
            item.get("right_title", ""),
            right_x + Inches(0.3), start_y + Inches(0.3),
            col_w - Inches(0.6), Inches(0.5),
            font_size=20, font_color=self.right_color,
            bold=True, alignment=PP_ALIGN.CENTER,
        )

        # Right items
        right_items = item.get("right_items", [])
        for j, text in enumerate(right_items):
            item_y = start_y + Inches(1.1) + j * Inches(0.7)
            # Bullet circle
            self.add_shape(
                MSO_SHAPE.OVAL,
                right_x + Inches(0.3), item_y + Inches(0.05),
                Inches(0.18), Inches(0.18),
                fill_color=self.right_color,
            )
            # Text
            self.add_textbox(
                text,
                right_x + Inches(0.6), item_y,
                col_w - Inches(0.9), Inches(0.35),
                font_size=12, font_color=hex_to_rgb("#424242"),
                alignment=PP_ALIGN.LEFT,
            )

    def _add_vs_divider(self):
        """中间VS分隔"""
        center_x = Inches(5)
        center_y = Inches(3.8)

        # Vertical line (top)
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            center_x - Inches(0.02), Inches(1.5),
            Inches(0.04), Inches(1.8),
            fill_color=hex_to_rgb("#E0E0E0"),
        )

        # VS circle
        circle_size = Inches(0.8)
        self.add_shape(
            MSO_SHAPE.OVAL,
            center_x - circle_size / 2, center_y - circle_size / 2,
            circle_size, circle_size,
            fill_color=self.vs_color,
        )
        self.add_textbox(
            "VS",
            center_x - circle_size / 2, center_y - Inches(0.18),
            circle_size, circle_size,
            font_size=20, font_color=RGBColor(255, 255, 255),
            bold=True, alignment=PP_ALIGN.CENTER,
        )

        # Vertical line (bottom)
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            center_x - Inches(0.02), center_y + Inches(0.5),
            Inches(0.04), Inches(1.8),
            fill_color=hex_to_rgb("#E0E0E0"),
        )

    def _add_bottom_accent(self):
        """底部装饰"""
        # Left half accent
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(7.2),
            Inches(5), Inches(0.3),
            fill_color=self.left_color,
        )
        # Right half accent
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(5), Inches(7.2),
            Inches(5), Inches(0.3),
            fill_color=self.right_color,
        )


if __name__ == "__main__":
    gen = ComparisonGenerator()
    gen.set_title("方案对比")
    gen.set_items([
        {
            "left_title": "方案A: 自主研发",
            "right_title": "方案B: 外部采购",
            "left_items": [
                "完全掌控技术栈",
                "长期成本较低",
                "可根据需求灵活定制",
                "需要组建专业团队",
                "开发周期较长",
                "技术风险需要自行承担",
            ],
            "right_items": [
                "快速上线部署",
                "初期投入较低",
                "借助成熟解决方案",
                "依赖供应商支持",
                "定制化程度有限",
                "长期维护成本较高",
            ],
        },
    ])
    gen.generate()
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'output_comparison.pptx')
    gen.save(output_path)
    print(f"Saved to {output_path}")
