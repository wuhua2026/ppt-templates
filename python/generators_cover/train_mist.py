"""列车穿雾封面生成器

生成包含雾气氛围渐变背景、抽象轨道汇聚形状、
柔化渐变覆盖层和半透明深度层次的封面。
"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, set_shape_transparency
from python.animation import apply_animations_to_slide


class TrainMistCover(TemplateGenerator):
    """列车穿雾封面"""

    # 默认雾色调色板
    DEFAULT_BG_TOP = "#1A1A2E"
    DEFAULT_BG_MID = "#16213E"
    DEFAULT_BG_BOTTOM = "#0F3460"
    DEFAULT_MIST_LIGHT = "#E0E0E0"
    DEFAULT_MIST_MID = "#B0BEC5"
    DEFAULT_MIST_DARK = "#78909C"
    DEFAULT_TRACK = "#546E7A"
    DEFAULT_ACCENT = "#90A4AE"

    def __init__(self, theme=None, **kwargs):
        super().__init__(theme=theme, **kwargs)
        self._title = "列车穿雾封面"
        self._subtitle = "Train Through Mist Cover"

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
        """生成列车穿雾封面幻灯片"""
        self.create_slide()

        bg_top = self._get_color("bg_dark", self.DEFAULT_BG_TOP)
        bg_mid = self._get_color("bg_mid", self.DEFAULT_BG_MID)
        bg_bottom = self._get_color("accent", self.DEFAULT_BG_BOTTOM)
        mist_light = self._get_color("light", self.DEFAULT_MIST_LIGHT)
        mist_mid = self._get_color("highlight", self.DEFAULT_MIST_MID)
        mist_dark = self._get_color("secondary", self.DEFAULT_MIST_DARK)
        track_color = self._get_color("primary", self.DEFAULT_TRACK)
        accent = self._get_color("accent", self.DEFAULT_ACCENT)

        slide_width = Inches(10)
        slide_height = Inches(7.5)

        animations = []

        # --- 水平渐变背景（模拟雾气氛围） ---
        bg = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            0, 0, slide_width, slide_height,
            [bg_top, bg_bottom],
            angle=90,
        )
        animations.append((bg.shape_id, "fade_in", 0, 500))

        # --- 抽象"铁轨"：从底部汇聚到消失点 ---
        vanish_x = slide_width // 2
        vanish_y = Inches(3.0)

        track_configs = [
            # (底部左偏移, 底部右偏移, 宽度, 颜色, 透明度)
            (Inches(-0.5), Inches(0.5), Inches(0.15), track_color, 0.30),
            (Inches(-1.2), Inches(1.2), Inches(0.12), accent, 0.40),
            (Inches(-2.0), Inches(2.0), Inches(0.10), mist_dark, 0.50),
            (Inches(-2.8), Inches(2.8), Inches(0.08), track_color, 0.55),
        ]

        for left_off, right_off, rail_w, color, alpha in track_configs:
            # 左铁轨（梯形近似：用窄矩形旋转模拟）
            left_rail = self.add_shape(
                MSO_SHAPE.RECTANGLE,
                vanish_x + left_off,
                vanish_y,
                rail_w,
                slide_height - vanish_y,
            )
            left_rail.fill.solid()
            left_rail.fill.fore_color.rgb = color
            left_rail.line.fill.background()
            set_shape_transparency(left_rail, alpha)
            animations.append((left_rail.shape_id, "wipe", 300, 800))

            # 右铁轨
            right_rail = self.add_shape(
                MSO_SHAPE.RECTANGLE,
                vanish_x + right_off - rail_w,
                vanish_y,
                rail_w,
                slide_height - vanish_y,
            )
            right_rail.fill.solid()
            right_rail.fill.fore_color.rgb = color
            right_rail.line.fill.background()
            set_shape_transparency(right_rail, alpha)
            animations.append((right_rail.shape_id, "wipe", 400, 800))

        # 横向枕木
        for i in range(8):
            y_pos = vanish_y + Inches(0.5) + Inches(i * 0.45)
            spread = 0.3 + i * 0.25
            sleeper = self.add_shape(
                MSO_SHAPE.RECTANGLE,
                vanish_x - Inches(spread),
                y_pos,
                Inches(spread * 2),
                Inches(0.06),
            )
            sleeper.fill.solid()
            sleeper.fill.fore_color.rgb = track_color
            sleeper.line.fill.background()
            set_shape_transparency(sleeper, 0.40 + i * 0.05)
            animations.append((sleeper.shape_id, "fade_in", 500 + i * 100, 400))

        # --- 雾气覆盖层（半透明矩形叠加） ---
        fog_layers = [
            # (y偏移, 高度, 颜色, 透明度)
            (0, Inches(1.5), mist_light, 0.80),
            (Inches(1.2), Inches(1.8), mist_mid, 0.70),
            (Inches(2.5), Inches(1.2), mist_light, 0.75),
            (Inches(5.0), Inches(2.0), mist_mid, 0.65),
            (Inches(6.0), Inches(1.5), mist_dark, 0.60),
        ]

        for y_off, height, color, alpha in fog_layers:
            fog = self.add_gradient_shape(
                MSO_SHAPE.RECTANGLE,
                0, y_off, slide_width, height,
                [RGBColor(color[0], color[1], color[2]), bg_bottom],
                angle=0,
            )
            set_shape_transparency(fog, alpha)
            animations.append((fog.shape_id, "fade_in", 200, 600))

        # --- 深度层次：远景山形三角形 ---
        mountain_configs = [
            (Inches(0.5), Inches(3.8), Inches(4), Inches(2.5), mist_dark, 0.55),
            (Inches(3.5), Inches(3.5), Inches(3.5), Inches(2.8), mist_mid, 0.50),
            (Inches(6.5), Inches(3.7), Inches(3.5), Inches(2.6), mist_dark, 0.60),
        ]

        for mx, my, mw, mh, color, alpha in mountain_configs:
            mountain = self.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, mx, my, mw, mh)
            mountain.fill.gradient()
            mountain.fill.gradient_stops[0].color.rgb = color
            mountain.fill.gradient_stops[0].position = 0.0
            mountain.fill.gradient_stops[1].color.rgb = bg_bottom
            mountain.fill.gradient_stops[1].position = 1.0
            mountain.line.fill.background()
            set_shape_transparency(mountain, alpha)
            animations.append((mountain.shape_id, "fade_in", 100, 700))

        # --- 前景光束效果（窄矩形） ---
        beam = self.add_shape(
            MSO_SHAPE.RECTANGLE,
            vanish_x - Inches(0.8),
            Inches(2.8),
            Inches(1.6),
            Inches(0.15),
        )
        beam.fill.gradient()
        beam.fill.gradient_stops[0].color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        beam.fill.gradient_stops[0].position = 0.0
        beam.fill.gradient_stops[1].color.rgb = accent
        beam.fill.gradient_stops[1].position = 1.0
        beam.line.fill.background()
        set_shape_transparency(beam, 0.50)
        animations.append((beam.shape_id, "fade_in", 1500, 600))

        # --- 标题 ---
        title_box = self.add_textbox(
            self._title,
            Inches(1.5), Inches(2.2), Inches(7.0), Inches(1.0),
            font_size=38,
            font_color=RGBColor(0xFF, 0xFF, 0xFF),
            bold=True,
            alignment=PP_ALIGN.CENTER,
            font_name="Microsoft YaHei",
        )
        animations.append((title_box.shape_id, "fade_in", 1800, 800))

        # --- 副标题 ---
        subtitle_box = self.add_textbox(
            self._subtitle,
            Inches(1.5), Inches(3.3), Inches(7.0), Inches(0.7),
            font_size=18,
            font_color=RGBColor(0xB0, 0xBE, 0xC5),
            bold=False,
            alignment=PP_ALIGN.CENTER,
            font_name="Microsoft YaHei",
        )
        animations.append((subtitle_box.shape_id, "fade_in", 2000, 800))

        # --- 应用动画 ---
        apply_animations_to_slide(self.slide, animations)

        return self


if __name__ == "__main__":
    generator = TrainMistCover()
    generator.set_title("列车穿雾封面演示").set_subtitle("Misty Railway Atmosphere Design")
    output = generator.generate().save("train_mist_cover.pptx")
    print(f"已保存: {output}")
