"""图文排版 - 左图右文/右图左文布局"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb


class TextImageLayoutGenerator(TemplateGenerator):
    """图文排版生成器"""

    def __init__(self, theme=None):
        super().__init__(theme=theme)
        self.items = []
        self.title = "图文排版"
        self.accent_color = hex_to_rgb("#1976D2")

    def set_title(self, title):
        self.title = title

    def set_items(self, items):
        """设置内容项
        items: list of dict with keys 'title', 'description', 'image' (optional)
        """
        self.items = items

    def generate(self):
        for i, item in enumerate(self.items):
            self.create_slide()
            self._add_background()
            self._add_title_bar(i + 1)
            if i % 2 == 0:
                self._add_left_image(i, item)
            else:
                self._add_right_image(i, item)
        return self

    def _add_background(self):
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(10), Inches(7.5),
            fill_color=hex_to_rgb("#FFFFFF"),
        )

    def _add_title_bar(self, page_num):
        # Top accent bar
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(10), Inches(0.06),
            fill_color=self.accent_color,
        )
        # Page number
        self.add_textbox(
            f"{page_num:02d}",
            Inches(0.5), Inches(0.3),
            Inches(1), Inches(0.5),
            font_size=36, font_color=hex_to_rgb("#E0E0E0"),
            bold=True, alignment=PP_ALIGN.LEFT,
        )

    def _add_left_image(self, index, item):
        """左图右文布局"""
        # Image placeholder (left side)
        img_x, img_y = Inches(0.5), Inches(1.2)
        img_w, img_h = Inches(4.5), Inches(5.5)

        img_shape = self.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            img_x, img_y, img_w, img_h,
            fill_color=hex_to_rgb("#E3F2FD"),
            outline_color=hex_to_rgb("#BBDEFB"),
            outline_width=Pt(1),
        )

        # Image icon placeholder
        icon_size = Inches(1.0)
        self.add_shape(
            MSO_SHAPE.OVAL,
            img_x + (img_w - icon_size) // 2,
            img_y + (img_h - icon_size) // 2,
            icon_size, icon_size,
            fill_color=hex_to_rgb("#BBDEFB"),
        )
        self.add_textbox(
            "IMG",
            img_x + (img_w - icon_size) // 2,
            img_y + (img_h - icon_size) // 2 + Inches(0.2),
            icon_size, Inches(0.5),
            font_size=14, font_color=hex_to_rgb("#1976D2"),
            bold=True, alignment=PP_ALIGN.CENTER,
        )

        # Text area (right side)
        text_x = Inches(5.5)
        text_w = Inches(4.0)

        # Accent vertical line
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            text_x - Inches(0.15), Inches(1.5),
            Inches(0.05), Inches(1.0),
            fill_color=self.accent_color,
        )

        # Title
        self.add_textbox(
            item.get("title", ""),
            text_x, Inches(1.5), text_w, Inches(0.5),
            font_size=24, font_color=hex_to_rgb("#212121"),
            bold=True, alignment=PP_ALIGN.LEFT,
        )

        # Description
        self.add_textbox(
            item.get("description", ""),
            text_x, Inches(2.2), text_w, Inches(3.5),
            font_size=14, font_color=hex_to_rgb("#616161"),
            alignment=PP_ALIGN.LEFT,
        )

        # Bottom decorative dots
        for j in range(3):
            self.add_shape(
                MSO_SHAPE.OVAL,
                text_x + j * Inches(0.25), Inches(6.2),
                Inches(0.08), Inches(0.08),
                fill_color=self.accent_color,
            )

    def _add_right_image(self, index, item):
        """右图左文布局"""
        # Text area (left side)
        text_x = Inches(0.5)
        text_w = Inches(4.0)

        # Accent vertical line
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            text_x, Inches(1.5),
            Inches(0.05), Inches(1.0),
            fill_color=self.accent_color,
        )

        # Title
        self.add_textbox(
            item.get("title", ""),
            text_x + Inches(0.2), Inches(1.5), text_w, Inches(0.5),
            font_size=24, font_color=hex_to_rgb("#212121"),
            bold=True, alignment=PP_ALIGN.LEFT,
        )

        # Description
        self.add_textbox(
            item.get("description", ""),
            text_x + Inches(0.2), Inches(2.2), text_w, Inches(3.5),
            font_size=14, font_color=hex_to_rgb("#616161"),
            alignment=PP_ALIGN.LEFT,
        )

        # Image placeholder (right side)
        img_x, img_y = Inches(5.0), Inches(1.2)
        img_w, img_h = Inches(4.5), Inches(5.5)

        img_shape = self.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            img_x, img_y, img_w, img_h,
            fill_color=hex_to_rgb("#FFF3E0"),
            outline_color=hex_to_rgb("#FFE0B2"),
            outline_width=Pt(1),
        )

        # Image icon placeholder
        icon_size = Inches(1.0)
        self.add_shape(
            MSO_SHAPE.OVAL,
            img_x + (img_w - icon_size) // 2,
            img_y + (img_h - icon_size) // 2,
            icon_size, icon_size,
            fill_color=hex_to_rgb("#FFE0B2"),
        )
        self.add_textbox(
            "IMG",
            img_x + (img_w - icon_size) // 2,
            img_y + (img_h - icon_size) // 2 + Inches(0.2),
            icon_size, Inches(0.5),
            font_size=14, font_color=hex_to_rgb("#E65100"),
            bold=True, alignment=PP_ALIGN.CENTER,
        )

        # Bottom decorative dots
        for j in range(3):
            self.add_shape(
                MSO_SHAPE.OVAL,
                text_x + Inches(0.2) + j * Inches(0.25), Inches(6.2),
                Inches(0.08), Inches(0.08),
                fill_color=self.accent_color,
            )


if __name__ == "__main__":
    gen = TextImageLayoutGenerator()
    gen.set_title("产品介绍")
    gen.set_items([
        {
            "title": "智能分析平台",
            "description": "基于人工智能的数据分析平台，提供实时数据监控、\n智能预测、自动化报告生成等功能。\n\n支持多种数据源接入，可视化仪表盘定制，\n团队协作与权限管理。",
        },
        {
            "title": "移动端应用",
            "description": "跨平台移动应用，覆盖iOS和Android系统。\n\n支持离线模式、推送通知、数据同步，\n提供流畅的用户体验和简洁的操作界面。",
        },
        {
            "title": "云端服务",
            "description": "高可用性云端架构，99.99%服务可用性保障。\n\n自动弹性伸缩，按需付费，\n企业级安全防护与数据加密。",
        },
    ])
    gen.generate()
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'output_text_image_layout.pptx')
    gen.save(output_path)
    print(f"Saved to {output_path}")
