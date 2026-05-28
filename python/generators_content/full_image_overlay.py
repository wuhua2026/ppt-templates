"""全图叠加 - 全幻灯片背景图+半透明文本覆盖层"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, set_shape_transparency


class FullImageOverlayGenerator(TemplateGenerator):
    """全图叠加生成器"""

    def __init__(self, theme=None):
        super().__init__(theme=theme)
        self.items = []
        self.title = "全图叠加"
        self.overlay_color = hex_to_rgb("#000000")
        self.overlay_transparency = 0.55

    def set_title(self, title):
        self.title = title

    def set_items(self, items):
        """设置叠加内容
        items: list of dict with keys 'title', 'subtitle', 'description'
        Each item becomes one slide.
        """
        self.items = items

    def generate(self):
        for i, item in enumerate(self.items):
            self.create_slide()
            self._add_full_background(i)
            self._add_overlay()
            self._add_text_content(i, item)
            self._add_bottom_bar()
        return self

    def _add_full_background(self, index):
        """全幻灯片背景（用纯色+渐变模拟图片占位）"""
        # Base gradient background
        bg_colors = [
            [hex_to_rgb("#1A237E"), hex_to_rgb("#283593")],
            [hex_to_rgb("#004D40"), hex_to_rgb("#00695C")],
            [hex_to_rgb("#BF360C"), hex_to_rgb("#D84315")],
            [hex_to_rgb("#4A148C"), hex_to_rgb("#6A1B9A")],
        ]
        colors = bg_colors[index % len(bg_colors)]
        bg = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(10), Inches(7.5),
            colors=colors,
        )

        # Decorative geometric shapes on background
        self.add_shape(
            MSO_SHAPE.OVAL,
            Inches(7), Inches(-1),
            Inches(4), Inches(4),
            fill_color=RGBColor(
                min(colors[0][0] + 20, 255),
                min(colors[0][1] + 20, 255),
                min(colors[0][2] + 20, 255),
            ),
        )
        self.add_shape(
            MSO_SHAPE.OVAL,
            Inches(-1), Inches(5),
            Inches(3), Inches(3),
            fill_color=RGBColor(
                min(colors[1][0] + 15, 255),
                min(colors[1][1] + 15, 255),
                min(colors[1][2] + 15, 255),
            ),
        )

    def _add_overlay(self):
        """半透明叠加层"""
        overlay = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(10), Inches(7.5),
            fill_color=self.overlay_color,
        )
        set_shape_transparency(overlay, self.overlay_transparency)

    def _add_text_content(self, index, item):
        """添加文字内容"""
        # Large page number
        self.add_textbox(
            f"{index + 1:02d}",
            Inches(0.8), Inches(0.8),
            Inches(2), Inches(1),
            font_size=60, font_color=RGBColor(255, 255, 255),
            bold=True, alignment=PP_ALIGN.LEFT,
        )

        # Title
        self.add_textbox(
            item.get("title", ""),
            Inches(0.8), Inches(2.2),
            Inches(8), Inches(1),
            font_size=36, font_color=RGBColor(255, 255, 255),
            bold=True, alignment=PP_ALIGN.LEFT,
        )

        # Separator line
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(3.3),
            Inches(2), Inches(0.04),
            fill_color=hex_to_rgb("#FF6F00"),
        )

        # Subtitle
        if item.get("subtitle"):
            self.add_textbox(
                item["subtitle"],
                Inches(0.8), Inches(3.6),
                Inches(8), Inches(0.5),
                font_size=20, font_color=RGBColor(255, 255, 255),
                alignment=PP_ALIGN.LEFT,
            )

        # Description
        if item.get("description"):
            self.add_textbox(
                item["description"],
                Inches(0.8), Inches(4.3),
                Inches(7), Inches(2.5),
                font_size=14, font_color=RGBColor(220, 220, 220),
                alignment=PP_ALIGN.LEFT,
            )

        # Quote style decorative element
        self.add_textbox(
            '"',
            Inches(0.5), Inches(2.0),
            Inches(0.5), Inches(0.6),
            font_size=48, font_color=hex_to_rgb("#FF6F00"),
            bold=True, alignment=PP_ALIGN.LEFT,
        )

    def _add_bottom_bar(self):
        """底部信息栏"""
        bar = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(6.8),
            Inches(10), Inches(0.7),
            fill_color=hex_to_rgb("#000000"),
        )
        set_shape_transparency(bar, 0.3)

        self.add_textbox(
            "CONFIDENTIAL  |  内部资料",
            Inches(0.8), Inches(6.9),
            Inches(8), Inches(0.4),
            font_size=10, font_color=RGBColor(200, 200, 200),
            alignment=PP_ALIGN.LEFT,
        )


if __name__ == "__main__":
    gen = FullImageOverlayGenerator()
    gen.set_title("全图叠加")
    gen.set_items([
        {
            "title": "引领数字化转型",
            "subtitle": "以技术驱动业务创新",
            "description": "在数字经济时代，我们致力于通过前沿技术赋能企业，实现业务流程的全面数字化升级。从数据采集到智能分析，从流程自动化到决策优化，提供端到端的数字化解决方案。",
        },
        {
            "title": "全球化战略布局",
            "subtitle": "立足中国，放眼世界",
            "description": "我们的业务已覆盖全球20+个国家和地区，服务超过500家企业客户。通过本地化运营和全球化协同，为不同市场提供定制化的解决方案。",
        },
        {
            "title": "可持续发展承诺",
            "subtitle": "科技向善，绿色未来",
            "description": "我们坚信科技应当服务于社会的可持续发展。通过优化能源效率、减少碳排放、推动循环经济，为建设绿色未来贡献力量。",
        },
    ])
    gen.generate()
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'output_full_image_overlay.pptx')
    gen.save(output_path)
    print(f"Saved to {output_path}")
