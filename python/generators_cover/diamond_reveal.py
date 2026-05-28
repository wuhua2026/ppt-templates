"""钻石揭示封面生成器

生成以中央大钻石（MSO_SHAPE.DIAMOND）作为主视觉元素的封面，
周围散布小钻石装饰元素，标题文本定位在中央钻石内部。
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, set_shape_transparency
from python.animation import apply_animations_to_slide


class DiamondRevealCover(TemplateGenerator):
    """钻石揭示封面"""

    # 默认钻石色系
    DEFAULT_BG_DARK = "#1A0A2E"
    DEFAULT_BG_MID = "#2D1B69"
    DEFAULT_DIAMOND_PRIMARY = "#7C4DFF"
    DEFAULT_DIAMOND_SECONDARY = "#B388FF"
    DEFAULT_DIAMOND_LIGHT = "#E1BEE7"
    DEFAULT_ACCENT = "#CE93D8"
    DEFAULT_GOLD = "#FFD54F"

    def __init__(self, theme=None, **kwargs):
        super().__init__(theme=theme, **kwargs)
        self._title = "钻石揭示封面"
        self._subtitle = "Diamond Reveal Cover"

    def set_title(self, title):
        self._title = title
        return self

    def set_subtitle(self, subtitle):
        self._subtitle = subtitle
        return self

    def _get_color(self, attr, default_hex):
        if self.theme and hasattr(self.theme, attr):
            return getattr(self.theme, attr)
        return hex_to_rgb(default_hex)

    def generate(self):
        """生成钻石揭示封面幻灯片"""
        self.create_slide()

        bg_dark = self._get_color("bg_dark", self.DEFAULT_BG_DARK)
        bg_mid = self._get_color("bg_mid", self.DEFAULT_BG_MID)
        diamond_primary = self._get_color("primary", self.DEFAULT_DIAMOND_PRIMARY)
        diamond_secondary = self._get_color("secondary", self.DEFAULT_DIAMOND_SECONDARY)
        diamond_light = self._get_color("light", self.DEFAULT_DIAMOND_LIGHT)
        accent = self._get_color("accent", self.DEFAULT_ACCENT)
        gold = self._get_color("highlight", self.DEFAULT_GOLD)

        slide_width = Inches(10)
        slide_height = Inches(7.5)
        center_x = slide_width // 2
        center_y = slide_height // 2

        animations = []

        # --- 背景渐变 ---
        bg = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            0, 0, slide_width, slide_height,
            [bg_dark, bg_mid],
            angle=180,
        )
        animations.append((bg.shape_id, "fade_in", 0, 400))

        # --- 背景装饰：放射状光线效果（用细矩形模拟） ---
        import math
        ray_count = 12
        for i in range(ray_count):
            angle_deg = i * (360 / ray_count)
            angle_rad = math.radians(angle_deg)
            ray_length = 5.0
            ray_x = center_x + Inches(ray_length / 2 * math.cos(angle_rad)) - Inches(0.02)
            ray_y = center_y + Inches(ray_length / 2 * math.sin(angle_rad)) - Inches(0.4)
            ray = self.add_shape(
                MSO_SHAPE.RECTANGLE,
                ray_x, ray_y,
                Inches(0.04), Inches(0.8),
            )
            ray.fill.solid()
            ray.fill.fore_color.rgb = diamond_light
            ray.line.fill.background()
            set_shape_transparency(ray, 0.70)

            # 旋转射线
            from lxml import etree
            xfrm = ray._element.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm')
            if xfrm is not None:
                xfrm.set('rot', str(int(angle_deg * 60000)))

            animations.append((ray.shape_id, "fade_in", 100 + i * 50, 500))

        # --- 散布的小钻石装饰元素 ---
        small_diamond_positions = [
            # (x偏移, y偏移, 大小, 透明度, 颜色)
            (-2.5, -1.5, 0.5, 0.55, diamond_secondary),
            (-3.0, 0.8, 0.4, 0.60, accent),
            (2.2, -1.8, 0.45, 0.50, gold),
            (2.8, 1.0, 0.35, 0.65, diamond_light),
            (-1.8, 2.0, 0.55, 0.45, diamond_secondary),
            (1.5, 2.2, 0.4, 0.55, accent),
            (-2.8, -0.3, 0.3, 0.70, gold),
            (3.0, -0.5, 0.35, 0.60, diamond_light),
            (-1.0, -2.0, 0.3, 0.65, accent),
            (1.8, -0.8, 0.25, 0.70, diamond_secondary),
            (-0.5, 2.5, 0.4, 0.55, gold),
            (0.8, -2.2, 0.35, 0.60, diamond_light),
        ]

        for i, (off_x, off_y, size, alpha, color) in enumerate(small_diamond_positions):
            left = center_x + Inches(off_x) - Inches(size / 2)
            top = center_y + Inches(off_y) - Inches(size / 2)
            sd = self.add_shape(
                MSO_SHAPE.DIAMOND,
                left, top,
                Inches(size), Inches(size),
            )
            sd.fill.gradient()
            sd.fill.gradient_stops[0].color.rgb = color
            sd.fill.gradient_stops[0].position = 0.0
            sd.fill.gradient_stops[1].color.rgb = bg_mid
            sd.fill.gradient_stops[1].position = 1.0
            sd.line.fill.background()
            set_shape_transparency(sd, alpha)
            animations.append((sd.shape_id, "grow", 200 + i * 80, 500))

        # --- 中央大钻石（主视觉元素） ---
        main_diamond_size = 3.2
        main_diamond = self.add_shape(
            MSO_SHAPE.DIAMOND,
            center_x - Inches(main_diamond_size / 2),
            center_y - Inches(main_diamond_size / 2),
            Inches(main_diamond_size),
            Inches(main_diamond_size),
        )
        # 渐变填充
        main_diamond.fill.gradient()
        main_diamond.fill.gradient_stops[0].color.rgb = diamond_primary
        main_diamond.fill.gradient_stops[0].position = 0.0
        main_diamond.fill.gradient_stops[1].color.rgb = diamond_secondary
        main_diamond.fill.gradient_stops[1].position = 1.0
        main_diamond.line.color.rgb = gold
        main_diamond.line.width = Pt(2)
        animations.append((main_diamond.shape_id, "grow", 800, 900))

        # --- 内部光效钻石（叠加在大钻石上） ---
        inner_diamond_size = 2.4
        inner_diamond = self.add_shape(
            MSO_SHAPE.DIAMOND,
            center_x - Inches(inner_diamond_size / 2),
            center_y - Inches(inner_diamond_size / 2),
            Inches(inner_diamond_size),
            Inches(inner_diamond_size),
        )
        inner_diamond.fill.gradient()
        inner_diamond.fill.gradient_stops[0].color.rgb = diamond_light
        inner_diamond.fill.gradient_stops[0].position = 0.0
        inner_diamond.fill.gradient_stops[1].color.rgb = diamond_primary
        inner_diamond.fill.gradient_stops[1].position = 1.0
        inner_diamond.line.fill.background()
        set_shape_transparency(inner_diamond, 0.50)
        animations.append((inner_diamond.shape_id, "fade_in", 1200, 600))

        # --- 标题文本（位于中央钻石内部） ---
        title_box = self.add_textbox(
            self._title,
            center_x - Inches(1.4), center_y - Inches(0.4),
            Inches(2.8), Inches(0.8),
            font_size=26,
            font_color=RGBColor(0xFF, 0xFF, 0xFF),
            bold=True,
            alignment=PP_ALIGN.CENTER,
            font_name="Microsoft YaHei",
        )
        animations.append((title_box.shape_id, "fade_in", 1400, 700))

        # --- 副标题（钻石下方） ---
        subtitle_box = self.add_textbox(
            self._subtitle,
            center_x - Inches(2.0), center_y + Inches(2.0),
            Inches(4.0), Inches(0.6),
            font_size=16,
            font_color=RGBColor(0xCE, 0x93, 0xD8),
            bold=False,
            alignment=PP_ALIGN.CENTER,
            font_name="Microsoft YaHei",
        )
        animations.append((subtitle_box.shape_id, "fade_in", 1600, 700))

        # --- 底部装饰线 ---
        deco_line = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            center_x - Inches(1.5), center_y + Inches(2.6),
            Inches(3.0), Inches(0.04),
        )
        deco_line.fill.gradient()
        deco_line.fill.gradient_stops[0].color.rgb = diamond_primary
        deco_line.fill.gradient_stops[0].position = 0.0
        deco_line.fill.gradient_stops[1].color.rgb = gold
        deco_line.fill.gradient_stops[1].position = 1.0
        deco_line.line.fill.background()
        animations.append((deco_line.shape_id, "fade_in", 1800, 500))

        # --- 应用动画 ---
        apply_animations_to_slide(self.slide, animations)

        return self


if __name__ == "__main__":
    generator = DiamondRevealCover()
    generator.set_title("钻石揭示封面演示").set_subtitle("Diamond Reveal Animated Design")
    output = generator.generate().save("diamond_reveal_cover.pptx")
    print(f"已保存: {output}")
