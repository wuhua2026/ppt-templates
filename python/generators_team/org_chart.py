"""组织架构图生成器

层级树形结构：顶层（CEO/负责人）连接到中层，中层连接到底层，
节点间以连线连接，每个节点为圆角矩形，包含姓名和职位。
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, set_shape_transparency
from python.animation import apply_animations_to_slide


class OrgChartGenerator(TemplateGenerator):
    """组织架构图"""

    DEFAULT_PRIMARY = "#1A237E"
    DEFAULT_SECONDARY = "#283593"
    DEFAULT_ACCENT = "#3F51B5"
    DEFAULT_LIGHT = "#C5CAE9"
    DEFAULT_BG = "#F5F7FA"
    DEFAULT_CARD_BG = "#FFFFFF"
    DEFAULT_TEXT_DARK = "#212121"
    DEFAULT_TEXT_WHITE = "#FFFFFF"
    DEFAULT_LINE_COLOR = "#90A4AE"

    def __init__(self, theme=None, **kwargs):
        super().__init__(theme=theme, **kwargs)
        self._title = "组织架构"
        # Hierarchical data: list of layers
        # layer 0: top node(s), layer 1: middle, layer 2: bottom
        self._layers = [
            [{"name": "张三", "title": "CEO"}],
            [
                {"name": "李四", "title": "技术总监"},
                {"name": "王五", "title": "产品总监"},
                {"name": "赵六", "title": "运营总监"},
            ],
            [
                {"name": "钱七", "title": "前端组长"},
                {"name": "孙八", "title": "后端组长"},
                {"name": "周九", "title": "产品经理"},
                {"name": "吴十", "title": "市场经理"},
            ],
        ]

    def set_title(self, title):
        self._title = title
        return self

    def set_data(self, layers):
        """设置层级数据
        layers: list of list of dicts, each dict has 'name' and 'title'.
        Example: [[{"name":"CEO","title":"CEO"}], [{"name":"A","title":"CTO"}, ...], ...]
        """
        self._layers = layers
        return self

    def _get_color(self, attr, default_hex):
        if self.theme and hasattr(self.theme, attr):
            return getattr(self.theme, attr)
        return hex_to_rgb(default_hex)

    def _draw_node(self, cx, cy, name, title, w, h, fill_color, text_color,
                   delay, animations):
        """绘制一个组织节点并记录动画"""
        left = cx - w // 2
        top = cy - h // 2

        node = self.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left, top, w, h,
            fill_color=fill_color,
        )
        animations.append((node.shape_id, "fade_in", delay, 500))

        # Name text
        name_box = self.add_textbox(
            name,
            left + Inches(0.05), top + Inches(0.05),
            w - Inches(0.1), Inches(0.4),
            font_size=13, font_color=text_color,
            bold=True, alignment=PP_ALIGN.CENTER,
        )

        # Title text
        title_box = self.add_textbox(
            title,
            left + Inches(0.05), top + Inches(0.4),
            w - Inches(0.1), Inches(0.35),
            font_size=10, font_color=text_color,
            bold=False, alignment=PP_ALIGN.CENTER,
        )

        return node

    def _draw_connector(self, x1, y1, x2, y2, line_color, delay, animations):
        """绘制连接线（用细矩形近似）"""
        # Draw vertical + horizontal lines using thin rectangles
        mid_y = y1 + (y2 - y1) // 2

        # Vertical from parent to mid
        v_line = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            x1 - Pt(1), min(y1, mid_y), Pt(2), abs(mid_y - y1),
            fill_color=line_color,
        )
        animations.append((v_line.shape_id, "fade_in", delay, 300))

        # Horizontal at mid
        h_left = min(x1, x2)
        h_right = max(x1, x2)
        h_line = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            h_left, mid_y - Pt(1), h_right - h_left, Pt(2),
            fill_color=line_color,
        )
        animations.append((h_line.shape_id, "fade_in", delay + 100, 300))

        # Vertical from mid to child
        v2_line = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            x2 - Pt(1), min(mid_y, y2), Pt(2), abs(y2 - mid_y),
            fill_color=line_color,
        )
        animations.append((v2_line.shape_id, "fade_in", delay + 200, 300))

    def generate(self):
        """生成组织架构图幻灯片"""
        self.create_slide()

        primary = self._get_color("primary", self.DEFAULT_PRIMARY)
        accent = self._get_color("accent", self.DEFAULT_ACCENT)
        light = self._get_color("light", self.DEFAULT_LIGHT)

        slide_w = Inches(10)
        slide_h = Inches(7.5)

        animations = []
        line_color = hex_to_rgb(self.DEFAULT_LINE_COLOR)

        # --- Background ---
        self.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, slide_w, slide_h,
                       fill_color=hex_to_rgb(self.DEFAULT_BG))

        # --- Top accent bar ---
        top_bar = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            0, 0, slide_w, Inches(0.06),
            [primary, accent],
        )
        animations.append((top_bar.shape_id, "fade_in", 0, 400))

        # --- Title ---
        title_box = self.add_textbox(
            self._title,
            Inches(0.5), Inches(0.35), Inches(9.0), Inches(0.65),
            font_size=30, font_color=hex_to_rgb(self.DEFAULT_TEXT_DARK),
            bold=True, alignment=PP_ALIGN.CENTER,
        )
        animations.append((title_box.shape_id, "fade_in", 100, 500))

        # --- Title underline ---
        deco = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(3.8), Inches(1.08), Inches(2.4), Inches(0.04),
            [primary, accent],
        )
        animations.append((deco.shape_id, "fade_in", 200, 400))

        # --- Layout parameters ---
        num_layers = len(self._layers)
        # Vertical spacing based on layer count
        layer_gap = Inches(1.6) if num_layers <= 3 else Inches(1.3)
        top_y = Inches(1.5)

        node_w = Inches(1.8)
        node_h = Inches(0.8)

        # Compute positions for each node in each layer
        layer_positions = []  # list of list of (cx, cy) per layer

        for layer_idx, layer in enumerate(self._layers):
            n = len(layer)
            cy = top_y + layer_idx * layer_gap
            total_w = n * node_w + (n - 1) * Inches(0.4)
            start_x = (slide_w - total_w) // 2
            positions = []
            for i in range(n):
                cx = start_x + i * (node_w + Inches(0.4)) + node_w // 2
                positions.append((cx, cy))
            layer_positions.append(positions)

        # --- Draw connectors first (behind nodes) ---
        for layer_idx in range(1, num_layers):
            parent_positions = layer_positions[layer_idx - 1]
            child_positions = layer_positions[layer_idx]
            n_parents = len(parent_positions)
            n_children = len(child_positions)

            # Distribute children among parents
            for c_idx, (child_cx, child_cy) in enumerate(child_positions):
                p_idx = int(c_idx * n_parents / n_children)
                parent_cx, parent_cy = parent_positions[p_idx]
                parent_bottom = parent_cy + node_h // 2
                child_top = child_cy - node_h // 2
                delay = 300 + layer_idx * 200 + c_idx * 50
                self._draw_connector(
                    parent_cx, parent_bottom,
                    child_cx, child_top,
                    line_color, delay, animations,
                )

        # --- Draw nodes (on top of connectors) ---
        for layer_idx, layer in enumerate(self._layers):
            positions = layer_positions[layer_idx]
            for i, member in enumerate(layer):
                cx, cy = positions[i]

                if layer_idx == 0:
                    # Top node: primary color
                    fill = primary
                    text_col = hex_to_rgb(self.DEFAULT_TEXT_WHITE)
                    w = Inches(2.2)
                    h = Inches(0.9)
                elif layer_idx == 1:
                    # Middle: accent color
                    fill = accent
                    text_col = hex_to_rgb(self.DEFAULT_TEXT_WHITE)
                    w = Inches(1.9)
                    h = Inches(0.85)
                else:
                    # Bottom: light with dark text
                    fill = hex_to_rgb(self.DEFAULT_CARD_BG)
                    text_col = hex_to_rgb(self.DEFAULT_TEXT_DARK)
                    w = Inches(1.7)
                    h = Inches(0.8)

                delay = 300 + layer_idx * 200 + i * 80
                self._draw_node(
                    cx, cy,
                    member.get("name", ""),
                    member.get("title", ""),
                    w, h, fill, text_col,
                    delay, animations,
                )

        # --- Decorative corner elements ---
        deco_d1 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(0.3), Inches(6.8), Inches(0.3), Inches(0.3),
            fill_color=light,
        )
        set_shape_transparency(deco_d1, 0.4)
        animations.append((deco_d1.shape_id, "fade_in", 600, 400))

        deco_d2 = self.add_shape(
            MSO_SHAPE.DIAMOND,
            Inches(9.5), Inches(0.2), Inches(0.25), Inches(0.25),
            fill_color=accent,
        )
        set_shape_transparency(deco_d2, 0.45)
        animations.append((deco_d2.shape_id, "fade_in", 650, 400))

        # --- Apply animations ---
        apply_animations_to_slide(self.slide, animations)

        return self


if __name__ == "__main__":
    gen = OrgChartGenerator()
    gen.set_title("组织架构")
    gen.set_data([
        [{"name": "张三", "title": "CEO"}],
        [
            {"name": "李四", "title": "技术总监"},
            {"name": "王五", "title": "产品总监"},
            {"name": "赵六", "title": "运营总监"},
        ],
        [
            {"name": "钱七", "title": "前端组长"},
            {"name": "孙八", "title": "后端组长"},
            {"name": "周九", "title": "产品经理"},
            {"name": "吴十", "title": "市场经理"},
        ],
    ])
    output = gen.generate().save("org_chart.pptx")
    print(f"已保存: {output}")
