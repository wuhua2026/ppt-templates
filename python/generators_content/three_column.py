"""三栏布局 - 三等分列，图标+标题+描述"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, create_grid_positions


class ThreeColumnGenerator(TemplateGenerator):
    """三栏布局生成器"""

    def __init__(self, theme=None):
        super().__init__(theme=theme)
        self.items = []
        self.title = "三栏布局"
        self.accent_colors = [
            hex_to_rgb("#1976D2"),
            hex_to_rgb("#388E3C"),
            hex_to_rgb("#F57C00"),
        ]
        self.bg_colors = [
            hex_to_rgb("#E3F2FD"),
            hex_to_rgb("#E8F5E9"),
            hex_to_rgb("#FFF3E0"),
        ]

    def set_title(self, title):
        self.title = title

    def set_items(self, items):
        """设置三栏内容
        items: list of dict with keys 'icon_text', 'title', 'description'
        Maximum 3 items.
        """
        self.items = items[:3]

    def generate(self):
        self.create_slide()
        self._add_background()
        self._add_title()
        self._add_subtitle_line()
        self._add_columns()
        return self

    def _add_background(self):
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(10), Inches(7.5),
            fill_color=hex_to_rgb("#FAFAFA"),
        )

    def _add_title(self):
        self.add_textbox(
            self.title,
            Inches(0.5), Inches(0.4), Inches(9), Inches(0.6),
            font_size=30, font_color=hex_to_rgb("#212121"),
            bold=True, alignment=PP_ALIGN.CENTER,
        )

    def _add_subtitle_line(self):
        # Decorative line under title
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(4.3), Inches(1.1),
            Inches(1.4), Inches(0.04),
            fill_color=hex_to_rgb("#1976D2"),
        )

    def _add_columns(self):
        count = len(self.items)
        if count == 0:
            return

        col_w = Inches(2.6)
        col_h = Inches(4.8)
        gap = Inches(0.5)
        total_w = count * col_w + (count - 1) * gap
        start_x = (Inches(10) - total_w) // 2
        start_y = Inches(1.6)

        for i, item in enumerate(self.items):
            x = start_x + i * (col_w + gap)
            color = self.accent_colors[i % len(self.accent_colors)]
            bg_color = self.bg_colors[i % len(self.bg_colors)]

            # Column card
            card = self.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                x, start_y, col_w, col_h,
                fill_color=hex_to_rgb("#FFFFFF"),
                outline_color=hex_to_rgb("#E0E0E0"),
                outline_width=Pt(1),
            )

            # Top color strip
            self.add_shape(
                MSO_SHAPE.RECTANGLE,
                x, start_y,
                col_w, Inches(0.06),
                fill_color=color,
            )

            # Icon circle
            icon_size = Inches(0.9)
            icon_x = x + (col_w - icon_size) // 2
            icon_y = start_y + Inches(0.5)
            self.add_shape(
                MSO_SHAPE.OVAL,
                icon_x, icon_y, icon_size, icon_size,
                fill_color=bg_color,
            )

            # Icon text
            self.add_textbox(
                item.get("icon_text", str(i + 1)),
                icon_x, icon_y + Inches(0.15),
                icon_size, Inches(0.6),
                font_size=22, font_color=color,
                bold=True, alignment=PP_ALIGN.CENTER,
            )

            # Column title
            self.add_textbox(
                item.get("title", ""),
                x + Inches(0.15), start_y + Inches(1.7),
                col_w - Inches(0.3), Inches(0.4),
                font_size=16, font_color=hex_to_rgb("#212121"),
                bold=True, alignment=PP_ALIGN.CENTER,
            )

            # Separator
            self.add_shape(
                MSO_SHAPE.RECTANGLE,
                x + (col_w - Inches(0.8)) // 2, start_y + Inches(2.2),
                Inches(0.8), Inches(0.03),
                fill_color=color,
            )

            # Description
            self.add_textbox(
                item.get("description", ""),
                x + Inches(0.2), start_y + Inches(2.4),
                col_w - Inches(0.4), Inches(2.2),
                font_size=11, font_color=hex_to_rgb("#616161"),
                alignment=PP_ALIGN.CENTER,
            )


if __name__ == "__main__":
    gen = ThreeColumnGenerator()
    gen.set_title("核心能力")
    gen.set_items([
        {
            "icon_text": "01",
            "title": "数据驱动",
            "description": "通过大数据分析和机器学习技术，\n为企业提供精准的数据洞察，\n辅助决策优化与业务增长。",
        },
        {
            "icon_text": "02",
            "title": "技术创新",
            "description": "持续投入前沿技术研发，\n保持技术领先优势，\n为客户提供最优质的解决方案。",
        },
        {
            "icon_text": "03",
            "title": "服务至上",
            "description": "以客户为中心的服务理念，\n提供全方位技术支持和咨询服务，\n确保项目成功交付。",
        },
    ])
    gen.generate()
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'output_three_column.pptx')
    gen.save(output_path)
    print(f"Saved to {output_path}")
