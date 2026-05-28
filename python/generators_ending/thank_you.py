"""感谢页生成器

大字"谢谢"居中，微妙几何装饰，下方联系方式，干净优雅的收尾。
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, set_shape_transparency
from python.animation import apply_animations_to_slide


class ThankYouGenerator(TemplateGenerator):
    """感谢页"""

    DEFAULT_PRIMARY = "#1A237E"
    DEFAULT_SECONDARY = "#283593"
    DEFAULT_ACCENT = "#3F51B5"
    DEFAULT_LIGHT = "#C5CAE9"
    DEFAULT_BG = "#F5F7FA"
    DEFAULT_TEXT_DARK = "#212121"
    DEFAULT_TEXT_MID = "#555555"

    def __init__(self, theme=None, **kwargs):
        super().__init__(theme=theme, **kwargs)
        self._title = "谢谢"
        self._subtitle = "Thank You"
        self._contact_line = "联系我们：contact@example.com"
        self._slogan = "期待与您的合作"

    def set_data(self, title=None, subtitle=None, contact_line=None, slogan=None):
        """设置感谢页数据"""
        if title is not None:
            self._title = title
        if subtitle is not None:
            self._subtitle = subtitle
        if contact_line is not None:
            self._contact_line = contact_line
        if slogan is not None:
            self._slogan = slogan
        return self

    def _get_color(self, attr, default_hex):
        if self.theme and hasattr(self.theme, attr):
            return getattr(self.theme, attr)
        return hex_to_rgb(default_hex)

    def generate(self):
        """生成感谢页"""
        self.create_slide()

        primary = self._get_color("primary", self.DEFAULT_PRIMARY)
        secondary = self._get_color("secondary", self.DEFAULT_SECONDARY)
        accent = self._get_color("accent", self.DEFAULT_ACCENT)
        light = self._get_color("light", self.DEFAULT_LIGHT)

        slide_w = Inches(10)
        slide_h = Inches(7.5)
        center_x = slide_w // 2
        center_y = slide_h // 2

        animations = []

        # --- Background gradient ---
        bg = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            0, 0, slide_w, slide_h,
            [primary, secondary],
            angle=135,
        )
        animations.append((bg.shape_id, "fade_in", 0, 600))

        # --- Decorative geometric elements ---
        # Large translucent diamond (top-left area)
        deco1 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(0.5), Inches(0.5), Inches(2.0), Inches(2.0),
        )
        deco1.fill.background()
        deco1.line.color.rgb = light
        deco1.line.width = Pt(1.5)
        set_shape_transparency(deco1, 0.6)
        animations.append((deco1.shape_id, "fade_in", 100, 600))

        # Small diamond near top-left
        deco2 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(1.5), Inches(1.0), Inches(0.6), Inches(0.6),
            fill_color=accent,
        )
        set_shape_transparency(deco2, 0.5)
        animations.append((deco2.shape_id, "fade_in", 150, 500))

        # Decorative circle (top-right area)
        deco3 = self.add_shape(
            MSO_SHAPE.OVAL,
            Inches(7.8), Inches(0.3), Inches(1.8), Inches(1.8),
        )
        deco3.fill.background()
        deco3.line.color.rgb = light
        deco3.line.width = Pt(1.2)
        set_shape_transparency(deco3, 0.55)
        animations.append((deco3.shape_id, "fade_in", 200, 600))

        # Small diamond (bottom-right area)
        deco4 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(8.5), Inches(5.8), Inches(1.2), Inches(1.2),
            fill_color=light,
        )
        set_shape_transparency(deco4, 0.5)
        animations.append((deco4.shape_id, "fade_in", 250, 600))

        # Small diamond bottom-left
        deco5 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(0.8), Inches(6.0), Inches(0.5), Inches(0.5),
            fill_color=accent,
        )
        set_shape_transparency(deco5, 0.55)
        animations.append((deco5.shape_id, "fade_in", 280, 500))

        # Thin horizontal decorative line
        deco_line = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(2.5), center_y - Inches(0.05), Inches(5.0), Inches(0.03),
            fill_color=light,
        )
        set_shape_transparency(deco_line, 0.3)
        animations.append((deco_line.shape_id, "fade_in", 300, 500))

        # --- Main title: 谢谢 ---
        title_box = self.add_textbox(
            self._title,
            Inches(1.0), center_y - Inches(1.5), Inches(8.0), Inches(1.5),
            font_size=64,
            font_color=RGBColor(0xFF, 0xFF, 0xFF),
            bold=True,
            alignment=PP_ALIGN.CENTER,
        )
        animations.append((title_box.shape_id, "fade_in", 400, 800))

        # --- Subtitle: Thank You ---
        subtitle_box = self.add_textbox(
            self._subtitle,
            Inches(1.0), center_y + Inches(0.2), Inches(8.0), Inches(0.8),
            font_size=28,
            font_color=light,
            bold=False,
            alignment=PP_ALIGN.CENTER,
        )
        animations.append((subtitle_box.shape_id, "fade_in", 500, 700))

        # --- Slogan ---
        slogan_box = self.add_textbox(
            self._slogan,
            Inches(1.5), center_y + Inches(1.2), Inches(7.0), Inches(0.6),
            font_size=16,
            font_color=RGBColor(0xC5, 0xCA, 0xE9),
            bold=False,
            alignment=PP_ALIGN.CENTER,
        )
        animations.append((slogan_box.shape_id, "fade_in", 600, 600))

        # --- Contact info line ---
        contact_box = self.add_textbox(
            self._contact_line,
            Inches(1.5), Inches(6.2), Inches(7.0), Inches(0.5),
            font_size=13,
            font_color=RGBColor(0x90, 0xA4, 0xAE),
            bold=False,
            alignment=PP_ALIGN.CENTER,
        )
        animations.append((contact_box.shape_id, "fade_in", 700, 500))

        # --- Bottom decorative gradient bar ---
        bottom_bar = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(2.5), Inches(6.8), Inches(5.0), Inches(0.04),
            [accent, light],
        )
        animations.append((bottom_bar.shape_id, "fade_in", 750, 400))

        # --- Apply animations ---
        apply_animations_to_slide(self.slide, animations)

        return self


if __name__ == "__main__":
    gen = ThankYouGenerator()
    gen.set_data(
        title="谢谢",
        subtitle="Thank You",
        contact_line="联系我们：contact@example.com",
        slogan="期待与您的合作",
    )
    output = gen.generate().save("thank_you.pptx")
    print(f"已保存: {output}")
