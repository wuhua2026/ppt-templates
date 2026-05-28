"""层次深度封面生成器 - 多层叠加矩形，营造空间感"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb, set_shape_transparency


class LayeredDepthCover(TemplateGenerator):
    """层次深度封面"""

    def __init__(self, theme=None):
        super().__init__(theme)
        self._title = ""
        self._subtitle = ""
        self._title_font_size = 42
        self._subtitle_font_size = 18
        self._title_color = RGBColor(255, 255, 255)
        self._subtitle_color = RGBColor(200, 200, 200)
        self._layer_count = 4

    def set_title(self, title, font_size=None, color=None):
        """设置标题"""
        self._title = title
        if font_size is not None:
            self._title_font_size = font_size
        if color is not None:
            self._title_color = color
        return self

    def set_subtitle(self, subtitle, font_size=None, color=None):
        """设置副标题"""
        self._subtitle = subtitle
        if font_size is not None:
            self._subtitle_font_size = font_size
        if color is not None:
            self._subtitle_color = color
        return self

    def _get_theme_colors(self):
        """获取主题颜色配置"""
        if self.theme:
            primary = hex_to_rgb(self.theme.primary)
            secondary = hex_to_rgb(self.theme.secondary)
            accent = hex_to_rgb(self.theme.accent)
            highlight = hex_to_rgb(self.theme.secondary)
        else:
            primary = RGBColor(20, 30, 48)
            secondary = RGBColor(36, 59, 85)
            accent = RGBColor(255, 107, 107)
            highlight = RGBColor(78, 205, 196)
        return primary, secondary, accent, highlight

    def generate(self):
        """生成层次深度封面"""
        self.create_slide()
        slide_w = self.prs.slide_width
        slide_h = self.prs.slide_height
        primary, secondary, accent, highlight = self._get_theme_colors()

        # --- 底层深色背景 ---
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0), slide_w, slide_h,
            fill_color=primary
        )

        # --- 多层偏移矩形，营造层次深度 ---
        # 层参数: (宽比例, 高比例, X偏移, Y偏移, 透明度, 颜色)
        layer_configs = [
            (0.95, 0.90, 0.15, 0.12, 0.75, secondary),
            (0.85, 0.82, 0.25, 0.20, 0.60, RGBColor(40, 65, 100)),
            (0.72, 0.72, 0.35, 0.28, 0.40, RGBColor(50, 80, 120)),
            (0.60, 0.60, 0.42, 0.32, 0.18, RGBColor(60, 95, 140)),
        ]

        for i, (w_ratio, h_ratio, x_ratio, y_ratio, transp, color) in enumerate(layer_configs):
            layer_w = int(slide_w * w_ratio)
            layer_h = int(slide_h * h_ratio)
            layer_x = int(slide_w * x_ratio)
            layer_y = int(slide_h * y_ratio)

            layer = self.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                layer_x, layer_y, layer_w, layer_h,
                fill_color=color
            )
            set_shape_transparency(layer, transp)
            layer.line.fill.background()

        # --- 最顶层小装饰矩形 ---
        top_layer_w = Inches(3.8)
        top_layer_h = Inches(2.2)
        top_layer_x = (slide_w - top_layer_w) // 2
        top_layer_y = (slide_h - top_layer_h) // 2

        top_layer = self.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            top_layer_x, top_layer_y, top_layer_w, top_layer_h,
            fill_color=RGBColor(30, 50, 80)
        )
        set_shape_transparency(top_layer, 0.25)
        top_layer.line.color.rgb = accent
        top_layer.line.width = Pt(1.5)

        # --- 左上角装饰条 ---
        accent_bar_w = Inches(1.2)
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.5), Inches(0.5),
            accent_bar_w, Pt(4),
            fill_color=accent
        )

        # --- 右下角装饰条 ---
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            slide_w - accent_bar_w - Inches(0.5),
            slide_h - Inches(0.7),
            accent_bar_w, Pt(4),
            fill_color=highlight
        )

        # --- 标题（在最顶层矩形上） ---
        if self._title:
            self.add_textbox(
                self._title,
                top_layer_x + Inches(0.3), top_layer_y + Inches(0.3),
                top_layer_w - Inches(0.6), Inches(1.0),
                font_size=self._title_font_size,
                font_color=self._title_color,
                bold=True,
                alignment=PP_ALIGN.CENTER
            )

        # --- 副标题 ---
        if self._subtitle:
            self.add_textbox(
                self._subtitle,
                top_layer_x + Inches(0.3),
                top_layer_y + Inches(1.3),
                top_layer_w - Inches(0.6), Inches(0.6),
                font_size=self._subtitle_font_size,
                font_color=self._subtitle_color,
                bold=False,
                alignment=PP_ALIGN.CENTER
            )

        return self


if __name__ == "__main__":
    cover = LayeredDepthCover()
    cover.set_title("层次深度封面", font_size=44)
    cover.set_subtitle("Layered Depth Cover", font_size=20)
    cover.save("output/layered_depth_cover.pptx")
    print("层次深度封面已生成: output/layered_depth_cover.pptx")
