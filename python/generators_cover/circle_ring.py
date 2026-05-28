"""圆环转场封面生成器

生成包含中央大圆环（Donut）和同心小圆环的封面，
使用蓝色到青色渐变色系，标题位于主圆环内部。
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, create_circle_positions, set_shape_transparency
from python.animation import apply_animations_to_slide


class CircleRingCover(TemplateGenerator):
    """圆环转场封面"""

    # 默认蓝色-青色色系
    DEFAULT_BG_DARK = "#0D1B2A"
    DEFAULT_BG_MID = "#1B2838"
    DEFAULT_RING_OUTER = "#00BCD4"
    DEFAULT_RING_INNER = "#26C6DA"
    DEFAULT_ACCENT = "#4DD0E1"
    DEFAULT_HIGHLIGHT = "#80DEEA"
    DEFAULT_LIGHT = "#B2EBF2"

    def __init__(self, theme=None, **kwargs):
        super().__init__(theme=theme, **kwargs)
        self._title = "圆环转场封面"
        self._subtitle = "Circle Ring Cover"

    def set_title(self, title):
        self._title = title
        return self

    def set_subtitle(self, subtitle):
        self._subtitle = subtitle
        return self

    def _get_color(self, attr, default_hex):
        """从主题获取颜色，若无则使用默认色"""
        if self.theme and hasattr(self.theme, attr):
            return getattr(self.theme, attr)
        return hex_to_rgb(default_hex)

    def generate(self):
        """生成圆环转场封面幻灯片"""
        self.create_slide()

        bg_dark = self._get_color("bg_dark", self.DEFAULT_BG_DARK)
        bg_mid = self._get_color("bg_mid", self.DEFAULT_BG_MID)
        ring_outer = self._get_color("accent", self.DEFAULT_RING_OUTER)
        ring_inner = self._get_color("highlight", self.DEFAULT_RING_INNER)
        accent = self._get_color("primary", self.DEFAULT_ACCENT)
        highlight = self._get_color("secondary", self.DEFAULT_HIGHLIGHT)
        light = self._get_color("light", self.DEFAULT_LIGHT)

        slide_width = Inches(10)
        slide_height = Inches(7.5)
        center_x = slide_width // 2
        center_y = slide_height // 2

        # --- 深色背景 ---
        bg = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            0, 0, slide_width, slide_height,
            [bg_dark, bg_mid],
            angle=135,
        )

        animations = []

        # --- 中央大圆环 (Donut) ---
        main_ring_size = 3.6
        main_ring = self.add_shape(
            MSO_SHAPE.DONUT,
            center_x - Inches(main_ring_size / 2),
            center_y - Inches(main_ring_size / 2),
            Inches(main_ring_size),
            Inches(main_ring_size),
        )
        # 圆环渐变填充
        main_ring.fill.gradient()
        main_ring.fill.gradient_stops[0].color.rgb = ring_outer
        main_ring.fill.gradient_stops[0].position = 0.0
        main_ring.fill.gradient_stops[1].color.rgb = ring_inner
        main_ring.fill.gradient_stops[1].position = 1.0
        main_ring.line.fill.background()
        set_shape_transparency(main_ring, 0.15)
        animations.append((main_ring.shape_id, "grow", 0, 800))

        # --- 同心小圆环 ---
        ring_configs = [
            # (半径偏移, 大小, 透明度, 颜色, 动画延迟)
            (0.8, 1.8, 0.30, ring_inner, 200),
            (1.6, 1.2, 0.50, accent, 400),
            (2.2, 0.9, 0.60, highlight, 600),
            (2.8, 0.7, 0.70, light, 800),
        ]

        for radius_offset, size, transparency, color, delay in ring_configs:
            # 圆周上放置多个
            positions = create_circle_positions(0, 0, Inches(radius_offset), 3, start_angle=30)
            for px, py in positions:
                left = center_x + px - Inches(size / 2)
                top = center_y + py - Inches(size / 2)
                ring = self.add_shape(
                    MSO_SHAPE.DONUT,
                    left, top,
                    Inches(size), Inches(size),
                )
                ring.fill.gradient()
                ring.fill.gradient_stops[0].color.rgb = color
                ring.fill.gradient_stops[0].position = 0.0
                ring.fill.gradient_stops[1].color.rgb = bg_mid
                ring.fill.gradient_stops[1].position = 1.0
                ring.line.fill.background()
                set_shape_transparency(ring, transparency)
                animations.append((ring.shape_id, "fade_in", delay, 600))

        # --- 装饰环线（圆形轮廓） ---
        for size_in, clr, alpha in [(4.2, ring_outer, 0.40), (4.8, accent, 0.50), (5.4, highlight, 0.60)]:
            dec_ring = self.add_shape(
                MSO_SHAPE.DONUT,
                center_x - Inches(size_in / 2),
                center_y - Inches(size_in / 2),
                Inches(size_in), Inches(size_in),
            )
            dec_ring.fill.background()
            dec_ring.line.color.rgb = clr
            dec_ring.line.width = Pt(1.5)
            set_shape_transparency(dec_ring, alpha)
            animations.append((dec_ring.shape_id, "fade_in", 1000, 500))

        # --- 标题（位于主圆环内部） ---
        title_box = self.add_textbox(
            self._title,
            center_x - Inches(1.5), center_y - Inches(0.5),
            Inches(3.0), Inches(0.7),
            font_size=28,
            font_color=RGBColor(0xFF, 0xFF, 0xFF),
            bold=True,
            alignment=PP_ALIGN.CENTER,
            font_name="Microsoft YaHei",
        )
        animations.append((title_box.shape_id, "fade_in", 1200, 700))

        # --- 副标题 ---
        subtitle_box = self.add_textbox(
            self._subtitle,
            center_x - Inches(2.0), center_y + Inches(2.3),
            Inches(4.0), Inches(0.6),
            font_size=16,
            font_color=RGBColor(0xB2, 0xEB, 0xF2),
            bold=False,
            alignment=PP_ALIGN.CENTER,
            font_name="Microsoft YaHei",
        )
        animations.append((subtitle_box.shape_id, "fade_in", 1400, 700))

        # --- 应用动画 ---
        apply_animations_to_slide(self.slide, animations)

        return self


if __name__ == "__main__":
    generator = CircleRingCover()
    generator.set_title("圆环转场封面演示").set_subtitle("Blue to Teal Gradient Ring Design")
    output = generator.generate().save("circle_ring_cover.pptx")
    print(f"已保存: {output}")
