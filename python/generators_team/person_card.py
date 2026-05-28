"""人物介绍卡片生成器

左侧圆形头像占位符，右侧姓名/职位/简介，带装饰性几何元素和渐变色块分隔。
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, set_shape_transparency
from python.animation import apply_animations_to_slide


class PersonCardGenerator(TemplateGenerator):
    """人物介绍卡片"""

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
        self._name = "姓名"
        self._title = "职位"
        self._bio = "个人简介信息，可包含多行描述内容。"
        self._avatar_color = None  # Optional override

    def set_data(self, name=None, title=None, bio=None, avatar_color=None):
        """设置人物数据"""
        if name is not None:
            self._name = name
        if title is not None:
            self._title = title
        if bio is not None:
            self._bio = bio
        if avatar_color is not None:
            self._avatar_color = avatar_color
        return self

    def _get_color(self, attr, default_hex):
        if self.theme and hasattr(self.theme, attr):
            return getattr(self.theme, attr)
        return hex_to_rgb(default_hex)

    def generate(self):
        """生成人物介绍卡片"""
        self.create_slide()

        primary = self._get_color("primary", self.DEFAULT_PRIMARY)
        secondary = self._get_color("secondary", self.DEFAULT_SECONDARY)
        accent = self._get_color("accent", self.DEFAULT_ACCENT)
        light = self._get_color("light", self.DEFAULT_LIGHT)

        slide_w = Inches(10)
        slide_h = Inches(7.5)

        animations = []

        # --- Background ---
        bg = self.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, slide_w, slide_h,
                            fill_color=hex_to_rgb(self.DEFAULT_BG))

        # --- Left accent gradient bar ---
        bar = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            0, 0, Inches(0.12), slide_h,
            [primary, accent],
        )
        animations.append((bar.shape_id, "fade_in", 0, 500))

        # --- Decorative geometric elements (top-left) ---
        deco1 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(0.4), Inches(0.4), Inches(0.35), Inches(0.35),
            fill_color=light,
        )
        set_shape_transparency(deco1, 0.4)
        animations.append((deco1.shape_id, "fade_in", 100, 500))

        deco2 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(0.9), Inches(0.25), Inches(0.2), Inches(0.2),
            fill_color=accent,
        )
        set_shape_transparency(deco2, 0.5)
        animations.append((deco2.shape_id, "fade_in", 150, 500))

        # --- Small decorative line ---
        deco_line = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(1.2), Inches(5.8), Inches(2.0), Inches(0.04),
            fill_color=light,
        )
        set_shape_transparency(deco_line, 0.3)
        animations.append((deco_line.shape_id, "fade_in", 300, 500))

        # --- Decorative diamond bottom-right ---
        deco3 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(8.8), Inches(6.5), Inches(0.5), Inches(0.5),
            fill_color=light,
        )
        set_shape_transparency(deco3, 0.35)
        animations.append((deco3.shape_id, "fade_in", 350, 500))

        deco4 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(9.2), Inches(6.2), Inches(0.25), Inches(0.25),
            fill_color=accent,
        )
        set_shape_transparency(deco4, 0.45)
        animations.append((deco4.shape_id, "fade_in", 400, 500))

        # --- Avatar circle (left side) ---
        avatar_size = Inches(2.8)
        avatar_left = Inches(0.8)
        avatar_top = Inches(1.5)

        # Outer ring
        avatar_ring = self.add_shape(
            MSO_SHAPE.OVAL,
            avatar_left - Inches(0.08), avatar_top - Inches(0.08),
            avatar_size + Inches(0.16), avatar_size + Inches(0.16),
        )
        avatar_ring.fill.background()
        avatar_ring.line.color.rgb = accent
        avatar_ring.line.width = Pt(2)
        animations.append((avatar_ring.shape_id, "fade_in", 50, 600))

        # Avatar placeholder circle
        avatar_fill = self._avatar_color or primary
        avatar = self.add_shape(
            MSO_SHAPE.OVAL,
            avatar_left, avatar_top,
            avatar_size, avatar_size,
            fill_color=avatar_fill,
        )
        set_shape_transparency(avatar, 0.15)
        animations.append((avatar.shape_id, "fade_in", 100, 600))

        # Avatar icon (person silhouette hint - small oval)
        person_icon = self.add_shape(
            MSO_SHAPE.OVAL,
            avatar_left + Inches(0.85), avatar_top + Inches(0.5),
            Inches(1.1), Inches(1.1),
            fill_color=secondary,
        )
        set_shape_transparency(person_icon, 0.3)
        animations.append((person_icon.shape_id, "fade_in", 150, 600))

        person_body = self.add_shape(
            MSO_SHAPE.OVAL,
            avatar_left + Inches(0.55), avatar_top + Inches(1.6),
            Inches(1.7), Inches(1.0),
            fill_color=secondary,
        )
        set_shape_transparency(person_body, 0.25)
        animations.append((person_body.shape_id, "fade_in", 200, 600))

        # --- Right side: text area ---
        text_left = Inches(4.2)
        text_width = Inches(5.2)

        # Name
        name_box = self.add_textbox(
            self._name,
            text_left, Inches(1.6), text_width, Inches(0.8),
            font_size=36, font_color=hex_to_rgb(self.DEFAULT_TEXT_DARK),
            bold=True, alignment=PP_ALIGN.LEFT,
        )
        animations.append((name_box.shape_id, "fade_in", 250, 600))

        # Title
        title_box = self.add_textbox(
            self._title,
            text_left, Inches(2.5), text_width, Inches(0.6),
            font_size=20, font_color=accent,
            bold=False, alignment=PP_ALIGN.LEFT,
        )
        animations.append((title_box.shape_id, "fade_in", 350, 600))

        # Gradient accent bar separating name/title from bio
        sep_bar = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            text_left, Inches(3.3), Inches(2.5), Inches(0.05),
            [primary, accent],
        )
        animations.append((sep_bar.shape_id, "wipe", 400, 400))

        # Bio
        bio_box = self.add_textbox(
            self._bio,
            text_left, Inches(3.6), text_width, Inches(2.5),
            font_size=14, font_color=hex_to_rgb(self.DEFAULT_TEXT_MID),
            bold=False, alignment=PP_ALIGN.LEFT,
        )
        animations.append((bio_box.shape_id, "fade_in", 450, 600))

        # --- Bottom decorative line ---
        bottom_line = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(6.8), Inches(8.4), Inches(0.03),
            [light, accent],
        )
        animations.append((bottom_line.shape_id, "fade_in", 500, 500))

        # --- Apply all animations ---
        apply_animations_to_slide(self.slide, animations)

        return self


if __name__ == "__main__":
    gen = PersonCardGenerator()
    gen.set_data(
        name="张三",
        title="高级产品经理",
        bio="拥有10年互联网产品管理经验，专注于用户体验设计和产品策略规划。\n曾主导多个大型产品的从0到1设计与落地。",
    )
    output = gen.generate().save("person_card.pptx")
    print(f"已保存: {output}")
