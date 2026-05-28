"""团队网格生成器

网格排列的团队成员卡片（2x3 或 3x2），每张卡片包含头像圆圈、姓名和职位，
卡片带细微边框和阴影效果，顶部带板块标题。
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, add_shadow, set_shape_transparency
from python.animation import apply_animations_to_slide


class TeamGridGenerator(TemplateGenerator):
    """团队网格"""

    DEFAULT_PRIMARY = "#1A237E"
    DEFAULT_SECONDARY = "#283593"
    DEFAULT_ACCENT = "#3F51B5"
    DEFAULT_LIGHT = "#C5CAE9"
    DEFAULT_BG = "#F5F7FA"
    DEFAULT_CARD_BG = "#FFFFFF"
    DEFAULT_BORDER = "#E0E0E0"
    DEFAULT_TEXT_DARK = "#212121"
    DEFAULT_TEXT_MID = "#555555"

    # Avatar placeholder colors (cycling)
    AVATAR_COLORS = [
        "#3F51B5", "#5C6BC0", "#7986CB",
        "#1E88E5", "#42A5F5", "#64B5F6",
        "#00897B", "#26A69A", "#4DB6AC",
        "#7B1FA2", "#AB47BC", "#CE93D8",
    ]

    def __init__(self, theme=None, **kwargs):
        super().__init__(theme=theme, **kwargs)
        self._title = "核心团队"
        self._members = []
        self._cols = 3  # default 3 columns
        self._rows = 2  # default 2 rows

    def set_members(self, members):
        """设置团队成员列表
        members: list of dict with keys 'name', 'title', optional 'avatar_color'
        """
        self._members = members
        total = len(members)
        if total <= 3:
            self._cols = 3
            self._rows = 1
        elif total <= 6:
            self._cols = 3
            self._rows = 2
        elif total <= 9:
            self._cols = 3
            self._rows = 3
        else:
            self._cols = 4
            self._rows = (total + 3) // 4
        return self

    def set_title(self, title):
        self._title = title
        return self

    def _get_color(self, attr, default_hex):
        if self.theme and hasattr(self.theme, attr):
            return getattr(self.theme, attr)
        return hex_to_rgb(default_hex)

    def generate(self):
        """生成团队网格幻灯片"""
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

        # --- Section title ---
        title_box = self.add_textbox(
            self._title,
            Inches(0.5), Inches(0.4), Inches(9.0), Inches(0.7),
            font_size=30, font_color=hex_to_rgb(self.DEFAULT_TEXT_DARK),
            bold=True, alignment=PP_ALIGN.CENTER,
        )
        animations.append((title_box.shape_id, "fade_in", 100, 500))

        # --- Decorative line under title ---
        deco_line = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(3.8), Inches(1.15), Inches(2.4), Inches(0.04),
            [primary, accent],
        )
        animations.append((deco_line.shape_id, "fade_in", 200, 400))

        # --- Grid of member cards ---
        cols = self._cols
        rows = self._rows
        card_w = Inches(2.6)
        card_h = Inches(3.4)
        gap_x = Inches(0.4)
        gap_y = Inches(0.4)

        total_w = cols * card_w + (cols - 1) * gap_x
        total_h = rows * card_h + (rows - 1) * gap_y
        start_x = (slide_w - total_w) // 2
        start_y = Inches(1.5) + (Inches(5.8) - total_h) // 2

        for idx, member in enumerate(self._members):
            row, col = divmod(idx, cols)
            cx = start_x + col * (card_w + gap_x)
            cy = start_y + row * (card_h + gap_y)

            delay_base = 300 + idx * 120

            # Card background (rounded rectangle)
            card = self.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                cx, cy, card_w, card_h,
                fill_color=hex_to_rgb(self.DEFAULT_CARD_BG),
                outline_color=hex_to_rgb(self.DEFAULT_BORDER),
                outline_width=Pt(0.75),
            )
            add_shadow(card, blur=Pt(4), offset=Pt(2),
                       color=(0, 0, 0), opacity=0.12)
            animations.append((card.shape_id, "fade_in", delay_base, 500))

            # Avatar circle
            avatar_size = Inches(1.2)
            avatar_left = cx + (card_w - avatar_size) // 2
            avatar_top = cy + Inches(0.3)

            color_idx = idx % len(self.AVATAR_COLORS)
            avatar_color = member.get("avatar_color", self.AVATAR_COLORS[color_idx])

            avatar = self.add_shape(
                MSO_SHAPE.OVAL,
                avatar_left, avatar_top, avatar_size, avatar_size,
                fill_color=hex_to_rgb(avatar_color),
            )
            set_shape_transparency(avatar, 0.1)
            animations.append((avatar.shape_id, "fade_in", delay_base + 100, 500))

            # Person silhouette hint in avatar
            person_head = self.add_shape(
                MSO_SHAPE.OVAL,
                avatar_left + Inches(0.35), avatar_top + Inches(0.2),
                Inches(0.5), Inches(0.5),
                fill_color=RGBColor(255, 255, 255),
            )
            set_shape_transparency(person_head, 0.4)

            person_shoulders = self.add_shape(
                MSO_SHAPE.OVAL,
                avatar_left + Inches(0.15), avatar_top + Inches(0.7),
                Inches(0.9), Inches(0.5),
                fill_color=RGBColor(255, 255, 255),
            )
            set_shape_transparency(person_shoulders, 0.35)

            # Name
            name_top = cy + Inches(1.65)
            self.add_textbox(
                member.get("name", "姓名"),
                cx + Inches(0.1), name_top, card_w - Inches(0.2), Inches(0.45),
                font_size=16, font_color=hex_to_rgb(self.DEFAULT_TEXT_DARK),
                bold=True, alignment=PP_ALIGN.CENTER,
            )

            # Title
            title_top = cy + Inches(2.15)
            self.add_textbox(
                member.get("title", "职位"),
                cx + Inches(0.1), title_top, card_w - Inches(0.2), Inches(0.4),
                font_size=12, font_color=accent,
                bold=False, alignment=PP_ALIGN.CENTER,
            )

            # Small decorative accent line under title
            line_w = Inches(0.8)
            line_left = cx + (card_w - line_w) // 2
            self.add_shape(
                MSO_SHAPE.RECTANGLE,
                line_left, title_top + Inches(0.4), line_w, Inches(0.025),
                fill_color=light,
            )

        # --- Apply animations ---
        apply_animations_to_slide(self.slide, animations)

        return self


if __name__ == "__main__":
    gen = TeamGridGenerator()
    gen.set_title("核心团队")
    gen.set_members([
        {"name": "张三", "title": "CEO"},
        {"name": "李四", "title": "CTO"},
        {"name": "王五", "title": "CPO"},
        {"name": "赵六", "title": "CFO"},
        {"name": "孙七", "title": "COO"},
        {"name": "周八", "title": "CMO"},
    ])
    output = gen.generate().save("team_grid.pptx")
    print(f"已保存: {output}")
