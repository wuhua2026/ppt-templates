"""联系方式页生成器

联系信息布局：邮箱、电话、网站、地址，每项带图标/标签，干净卡片式布局。
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, add_shadow, set_shape_transparency
from python.animation import apply_animations_to_slide


class ContactPageGenerator(TemplateGenerator):
    """联系方式页"""

    DEFAULT_PRIMARY = "#1A237E"
    DEFAULT_SECONDARY = "#283593"
    DEFAULT_ACCENT = "#3F51B5"
    DEFAULT_LIGHT = "#C5CAE9"
    DEFAULT_BG = "#F5F7FA"
    DEFAULT_CARD_BG = "#FFFFFF"
    DEFAULT_TEXT_DARK = "#212121"
    DEFAULT_TEXT_MID = "#555555"
    DEFAULT_TEXT_LIGHT = "#9E9E9E"
    DEFAULT_BORDER = "#E0E0E0"

    # Default contact items
    DEFAULT_ITEMS = [
        {"icon": "EMAIL", "label": "电子邮箱", "value": "contact@example.com"},
        {"icon": "TEL", "label": "联系电话", "value": "+86 138-0000-0000"},
        {"icon": "WEB", "label": "官方网站", "value": "www.example.com"},
        {"icon": "ADDR", "label": "办公地址", "value": "北京市朝阳区某某路100号"},
    ]

    def __init__(self, theme=None, **kwargs):
        super().__init__(theme=theme, **kwargs)
        self._title = "联系方式"
        self._items = list(self.DEFAULT_ITEMS)
        self._company_name = "Example公司"

    def set_data(self, title=None, items=None, company_name=None):
        """设置联系方式数据
        items: list of dict with keys 'icon', 'label', 'value'
        """
        if title is not None:
            self._title = title
        if items is not None:
            self._items = items
        if company_name is not None:
            self._company_name = company_name
        return self

    def _get_color(self, attr, default_hex):
        if self.theme and hasattr(self.theme, attr):
            return getattr(self.theme, attr)
        return hex_to_rgb(default_hex)

    def generate(self):
        """生成联系方式页"""
        self.create_slide()

        primary = self._get_color("primary", self.DEFAULT_PRIMARY)
        accent = self._get_color("accent", self.DEFAULT_ACCENT)
        light = self._get_color("light", self.DEFAULT_LIGHT)

        slide_w = Inches(10)
        slide_h = Inches(7.5)

        animations = []

        # --- Background ---
        self.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, slide_w, slide_h,
                       fill_color=hex_to_rgb(self.DEFAULT_BG))

        # --- Top gradient accent bar ---
        top_bar = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            0, 0, slide_w, Inches(0.06),
            [primary, accent],
        )
        animations.append((top_bar.shape_id, "fade_in", 0, 400))

        # --- Title ---
        title_box = self.add_textbox(
            self._title,
            Inches(0.5), Inches(0.4), Inches(9.0), Inches(0.7),
            font_size=30, font_color=hex_to_rgb(self.DEFAULT_TEXT_DARK),
            bold=True, alignment=PP_ALIGN.CENTER,
        )
        animations.append((title_box.shape_id, "fade_in", 100, 500))

        # --- Title underline ---
        deco = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(3.8), Inches(1.15), Inches(2.4), Inches(0.04),
            [primary, accent],
        )
        animations.append((deco.shape_id, "fade_in", 200, 400))

        # --- Company name ---
        company_box = self.add_textbox(
            self._company_name,
            Inches(1.0), Inches(1.45), Inches(8.0), Inches(0.5),
            font_size=16,
            font_color=accent,
            bold=False,
            alignment=PP_ALIGN.CENTER,
        )
        animations.append((company_box.shape_id, "fade_in", 250, 500))

        # --- Contact cards layout ---
        n_items = len(self._items)
        if n_items <= 4:
            cols = 2
            rows = 2
        else:
            cols = 3
            rows = (n_items + 2) // 3

        card_w = Inches(3.6)
        card_h = Inches(2.0)
        gap_x = Inches(0.5)
        gap_y = Inches(0.4)

        total_w = cols * card_w + (cols - 1) * gap_x
        total_h = rows * card_h + (rows - 1) * gap_y
        start_x = (slide_w - total_w) // 2
        start_y = Inches(2.2) + (Inches(5.0) - total_h) // 2

        for idx, item in enumerate(self._items):
            row, col = divmod(idx, cols)
            cx = start_x + col * (card_w + gap_x)
            cy = start_y + row * (card_h + gap_y)

            delay_base = 300 + idx * 120

            # Card background
            card = self.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                cx, cy, card_w, card_h,
                fill_color=hex_to_rgb(self.DEFAULT_CARD_BG),
                outline_color=hex_to_rgb(self.DEFAULT_BORDER),
                outline_width=Pt(0.75),
            )
            add_shadow(card, blur=Pt(3), offset=Pt(2),
                       color=(0, 0, 0), opacity=0.1)
            animations.append((card.shape_id, "fade_in", delay_base, 500))

            # Icon circle on the left side of card
            icon_size = Inches(0.65)
            icon_left = cx + Inches(0.25)
            icon_top = cy + (card_h - icon_size) // 2

            icon_bg = self.add_shape(
                MSO_SHAPE.OVAL,
                icon_left, icon_top, icon_size, icon_size,
                fill_color=primary,
            )
            animations.append((icon_bg.shape_id, "fade_in", delay_base + 80, 400))

            # Icon text (emoji/abbreviation)
            icon_text_box = self.add_textbox(
                item.get("icon", ""),
                icon_left, icon_top + Inches(0.08),
                icon_size, icon_size - Inches(0.08),
                font_size=11,
                font_color=RGBColor(0xFF, 0xFF, 0xFF),
                bold=True,
                alignment=PP_ALIGN.CENTER,
            )

            # Label
            text_left = cx + Inches(1.1)
            text_width = card_w - Inches(1.3)

            label_box = self.add_textbox(
                item.get("label", "标签"),
                text_left, cy + Inches(0.3),
                text_width, Inches(0.4),
                font_size=13,
                font_color=hex_to_rgb(self.DEFAULT_TEXT_LIGHT),
                bold=False,
                alignment=PP_ALIGN.LEFT,
            )

            # Value
            value_box = self.add_textbox(
                item.get("value", "暂无"),
                text_left, cy + Inches(0.75),
                text_width, Inches(0.8),
                font_size=16,
                font_color=hex_to_rgb(self.DEFAULT_TEXT_DARK),
                bold=True,
                alignment=PP_ALIGN.LEFT,
            )

        # --- Decorative corner elements ---
        deco_d1 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(0.3), Inches(6.8), Inches(0.3), Inches(0.3),
            fill_color=light,
        )
        set_shape_transparency(deco_d1, 0.4)
        animations.append((deco_d1.shape_id, "fade_in", 800, 400))

        deco_d2 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(9.4), Inches(6.5), Inches(0.4), Inches(0.4),
            fill_color=accent,
        )
        set_shape_transparency(deco_d2, 0.45)
        animations.append((deco_d2.shape_id, "fade_in", 820, 400))

        # --- Bottom gradient bar ---
        bottom_bar = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(7.1), Inches(8.4), Inches(0.04),
            [light, accent],
        )
        animations.append((bottom_bar.shape_id, "fade_in", 850, 400))

        # --- Apply animations ---
        apply_animations_to_slide(self.slide, animations)

        return self


if __name__ == "__main__":
    gen = ContactPageGenerator()
    gen.set_data(
        title="联系方式",
        company_name="Example科技有限公司",
        items=[
            {"icon": "EMAIL", "label": "电子邮箱", "value": "contact@example.com"},
            {"icon": "TEL", "label": "联系电话", "value": "+86 138-0000-0000"},
            {"icon": "WEB", "label": "官方网站", "value": "www.example.com"},
            {"icon": "ADDR", "label": "办公地址", "value": "北京市朝阳区某某路100号"},
        ],
    )
    output = gen.generate().save("contact.pptx")
    print(f"已保存: {output}")
