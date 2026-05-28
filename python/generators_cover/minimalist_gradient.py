"""极简渐变封面生成器 - 全幅渐变背景，简洁现代设计"""

from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from python.base import TemplateGenerator
from python.utils import hex_to_rgb


class MinimalistGradientCover(TemplateGenerator):
    """极简渐变封面"""

    def __init__(self, theme=None):
        super().__init__(theme)
        self._title = ""
        self._subtitle = ""
        self._title_font_size = 44
        self._subtitle_font_size = 18
        self._title_color = RGBColor(255, 255, 255)
        self._subtitle_color = RGBColor(255, 255, 255)
        self._gradient_colors = None
        self._accent_color = None

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
        else:
            primary = RGBColor(26, 26, 46)
            secondary = RGBColor(22, 33, 62)
            accent = RGBColor(233, 69, 96)
        return primary, secondary, accent

    def generate(self):
        """生成极简渐变封面"""
        self.create_slide()
        slide_w = self.prs.slide_width
        slide_h = self.prs.slide_height
        primary, secondary, accent = self._get_theme_colors()

        if self._gradient_colors is None:
            self._gradient_colors = [primary, secondary]

        # --- 全幅渐变背景 ---
        bg = self.add_gradient_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0), slide_w, slide_h,
            self._gradient_colors, angle=45
        )

        # --- 微妙的装饰圆弧（右上角） ---
        circle_size = Inches(4.5)
        self.add_shape(
            MSO_SHAPE.OVAL,
            slide_w - circle_size + Inches(0.5),
            Inches(-1.5),
            circle_size, circle_size,
            fill_color=accent if self._accent_color is None else self._accent_color
        )
        # 设置圆的透明度（10%）
        from python.utils import set_shape_transparency
        set_shape_transparency(self.slide.shapes[-1], 0.88)

        # --- 水平细线装饰 ---
        line_y = slide_h // 2 + Inches(1.2)
        line_w = Inches(3)
        self.add_shape(
            MSO_SHAPE.RECTANGLE,
            (slide_w - line_w) // 2,
            line_y,
            line_w, Pt(2),
            fill_color=self._title_color
        )

        # --- 标题（居中） ---
        title_y = slide_h // 2 - Inches(1.0)
        if self._title:
            self.add_textbox(
                self._title,
                Inches(1), title_y, slide_w - Inches(2), Inches(1.2),
                font_size=self._title_font_size,
                font_color=self._title_color,
                bold=True,
                alignment=PP_ALIGN.CENTER
            )

        # --- 副标题（居中，位于细线下方） ---
        if self._subtitle:
            self.add_textbox(
                self._subtitle,
                Inches(1), line_y + Inches(0.3),
                slide_w - Inches(2), Inches(0.8),
                font_size=self._subtitle_font_size,
                font_color=self._subtitle_color,
                bold=False,
                alignment=PP_ALIGN.CENTER
            )

        return self


if __name__ == "__main__":
    cover = MinimalistGradientCover()
    cover.set_title("极简渐变封面", font_size=48)
    cover.set_subtitle("Minimalist Gradient Cover", font_size=20)
    cover.save("output/minimalist_gradient_cover.pptx")
    print("极简渐变封面已生成: output/minimalist_gradient_cover.pptx")
