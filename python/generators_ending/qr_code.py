"""二维码页生成器

大正方形二维码占位符，上方"扫码关注"文字，下方社交媒体文字，居中布局。
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, set_shape_transparency
from python.animation import apply_animations_to_slide


class QRCodeGenerator(TemplateGenerator):
    """二维码页"""

    DEFAULT_PRIMARY = "#1A237E"
    DEFAULT_SECONDARY = "#283593"
    DEFAULT_ACCENT = "#3F51B5"
    DEFAULT_LIGHT = "#C5CAE9"
    DEFAULT_BG = "#F5F7FA"
    DEFAULT_TEXT_DARK = "#212121"
    DEFAULT_TEXT_MID = "#555555"
    DEFAULT_TEXT_LIGHT = "#9E9E9E"

    def __init__(self, theme=None, **kwargs):
        super().__init__(theme=theme, **kwargs)
        self._heading = "扫码关注"
        self._sub_text = "扫描二维码，关注我们的公众号"
        self._social_links = ["微信: example_wechat", "微博: @example", "官网: www.example.com"]

    def set_data(self, heading=None, sub_text=None, social_links=None):
        """设置二维码页数据"""
        if heading is not None:
            self._heading = heading
        if sub_text is not None:
            self._sub_text = sub_text
        if social_links is not None:
            self._social_links = social_links
        return self

    def _get_color(self, attr, default_hex):
        if self.theme and hasattr(self.theme, attr):
            return getattr(self.theme, attr)
        return hex_to_rgb(default_hex)

    def generate(self):
        """生成二维码页"""
        self.create_slide()

        primary = self._get_color("primary", self.DEFAULT_PRIMARY)
        secondary = self._get_color("secondary", self.DEFAULT_SECONDARY)
        accent = self._get_color("accent", self.DEFAULT_ACCENT)
        light = self._get_color("light", self.DEFAULT_LIGHT)

        slide_w = Inches(10)
        slide_h = Inches(7.5)
        center_x = slide_w // 2

        animations = []

        # --- Background ---
        bg = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            0, 0, slide_w, slide_h,
            [primary, secondary],
            angle=135,
        )
        animations.append((bg.shape_id, "fade_in", 0, 500))

        # --- Decorative elements (top-left) ---
        deco1 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(0.4), Inches(0.4), Inches(0.7), Inches(0.7),
            fill_color=accent,
        )
        set_shape_transparency(deco1, 0.55)
        animations.append((deco1.shape_id, "fade_in", 100, 500))

        deco2 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(1.0), Inches(0.2), Inches(0.35), Inches(0.35),
            fill_color=light,
        )
        set_shape_transparency(deco2, 0.5)
        animations.append((deco2.shape_id, "fade_in", 130, 500))

        # Decorative circle (bottom-right)
        deco3 = self.add_shape(
            MSO_SHAPE.OVAL,
            Inches(8.5), Inches(6.2), Inches(1.5), Inches(1.5),
        )
        deco3.fill.background()
        deco3.line.color.rgb = light
        deco3.line.width = Pt(1.2)
        set_shape_transparency(deco3, 0.5)
        animations.append((deco3.shape_id, "fade_in", 150, 500))

        # --- Heading text ---
        heading_box = self.add_textbox(
            self._heading,
            Inches(1.5), Inches(1.0), Inches(7.0), Inches(0.8),
            font_size=36,
            font_color=RGBColor(0xFF, 0xFF, 0xFF),
            bold=True,
            alignment=PP_ALIGN.CENTER,
        )
        animations.append((heading_box.shape_id, "fade_in", 200, 600))

        # --- Sub text ---
        sub_box = self.add_textbox(
            self._sub_text,
            Inches(1.5), Inches(1.85), Inches(7.0), Inches(0.5),
            font_size=16,
            font_color=light,
            bold=False,
            alignment=PP_ALIGN.CENTER,
        )
        animations.append((sub_box.shape_id, "fade_in", 300, 500))

        # --- QR code placeholder (large square) ---
        qr_size = Inches(3.2)
        qr_left = center_x - qr_size // 2
        qr_top = Inches(2.7)

        # QR border frame
        qr_border_size = qr_size + Inches(0.2)
        qr_border = self.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            center_x - qr_border_size // 2, qr_top - Inches(0.1),
            qr_border_size, qr_border_size,
            fill_color=RGBColor(0xFF, 0xFF, 0xFF),
        )
        set_shape_transparency(qr_border, 0.1)
        animations.append((qr_border.shape_id, "fade_in", 350, 600))

        # QR placeholder rectangle
        qr_bg = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            qr_left, qr_top, qr_size, qr_size,
            fill_color=RGBColor(0xFF, 0xFF, 0xFF),
        )
        animations.append((qr_bg.shape_id, "fade_in", 400, 600))

        # QR placeholder text
        qr_text = self.add_textbox(
            "二维码",
            qr_left, qr_top + Inches(1.2), qr_size, Inches(0.8),
            font_size=22,
            font_color=hex_to_rgb(self.DEFAULT_TEXT_LIGHT),
            bold=False,
            alignment=PP_ALIGN.CENTER,
        )
        animations.append((qr_text.shape_id, "fade_in", 450, 500))

        # Small decorative pattern inside QR (simulate pattern)
        pattern_size = Inches(0.6)
        for px, py in [
            (qr_left + Inches(0.15), qr_top + Inches(0.15)),
            (qr_left + qr_size - Inches(0.75), qr_top + Inches(0.15)),
            (qr_left + Inches(0.15), qr_top + qr_size - Inches(0.75)),
        ]:
            corner = self.add_shape(
                MSO_SHAPE.RECTANGLE,
                px, py, pattern_size, pattern_size,
                fill_color=primary,
            )
            set_shape_transparency(corner, 0.2)

        # --- Social media icons text ---
        social_y = qr_top + qr_size + Inches(0.5)
        for i, link in enumerate(self._social_links):
            link_box = self.add_textbox(
                link,
                Inches(1.5), social_y + Inches(i * 0.4),
                Inches(7.0), Inches(0.35),
                font_size=13,
                font_color=RGBColor(0xC5, 0xCA, 0xE9),
                bold=False,
                alignment=PP_ALIGN.CENTER,
            )
            animations.append((link_box.shape_id, "fade_in", 500 + i * 100, 400))

        # --- Bottom gradient bar ---
        bottom_bar = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(2.0), Inches(6.8), Inches(6.0), Inches(0.04),
            [accent, light],
        )
        animations.append((bottom_bar.shape_id, "fade_in", 800, 400))

        # --- Apply animations ---
        apply_animations_to_slide(self.slide, animations)

        return self


if __name__ == "__main__":
    gen = QRCodeGenerator()
    gen.set_data(
        heading="扫码关注",
        sub_text="扫描二维码，关注我们的公众号",
        social_links=[
            "微信公众号: example_official",
            "微博: @example官方微博",
            "官网: www.example.com",
        ],
    )
    output = gen.generate().save("qr_code.pptx")
    print(f"已保存: {output}")
