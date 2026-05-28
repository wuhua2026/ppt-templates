"""双波形时间轴 - 两条正弦波路径横跨幻灯片，节点位于波峰/波谷"""

import math
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from python.base import TemplateGenerator
from python.utils import hex_to_rgb


class DualWaveTimeline(TemplateGenerator):
    """双波形时间轴"""

    def __init__(self, theme=None):
        super().__init__(theme)
        self._title = ""
        self._subtitle = ""
        self._events = []  # list of dicts: {label, date, detail, is_future}
        self._wave_amplitude = Inches(0.6)
        self._node_radius = Inches(0.18)
        self._past_color = RGBColor(52, 152, 219)       # 蓝色 - 过去
        self._future_color = RGBColor(231, 76, 60)      # 红色 - 未来
        self._wave1_color = RGBColor(52, 152, 219)
        self._wave2_color = RGBColor(46, 204, 113)
        self._line_color = RGBColor(189, 195, 199)

    def set_title(self, title, subtitle=""):
        self._title = title
        self._subtitle = subtitle
        return self

    def set_data(self, events):
        """设置事件列表

        Args:
            events: list of dict, 每项包含:
                label (str): 事件名称
                date (str): 日期
                detail (str): 详细描述
                is_future (bool): 是否为未来事件
                wave (int): 所在波形 1 或 2
        """
        self._events = events
        return self

    def _draw_wave_path(self, start_x, end_x, center_y, amplitude,
                        phase_shift, color, num_segments=80):
        """绘制波浪线路径"""
        from lxml import etree
        nsmap = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        }

        points = []
        for i in range(num_segments + 1):
            t = i / num_segments
            x = start_x + int((end_x - start_x) * t)
            y_offset = int(amplitude * math.sin(2 * math.pi * t * 1.5 + phase_shift))
            y = center_y + y_offset
            points.append((x, y))

        # Build freeform XML
        path_data = f'M {points[0][0]},{points[0][1]} '
        for px, py in points[1:]:
            path_data += f'L {px},{py} '

        freeform_xml = f'''<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                                 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <p:nvSpPr><p:cNvPr id="{self._get_next_shape_id()}" name="WavePath"/>
            <p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></a:xfrm>
            <a:prstGeom prst="line"><a:avLst/></a:prstGeom>
            <a:ln w="{Pt(2.5)}" cap="round" cmpd="sng">
              <a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
            </a:ln>
          </p:spPr>
          <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="zh-CN"/></a:p></p:txBody>
          <p:spPr>
            <a:pathLst>
              <a:path w="0" h="0">
                <a:moveTo><a:pt x="{points[0][0]}" y="{points[0][1]}"/></a:moveTo>'''

        for px, py in points[1:]:
            freeform_xml += f'''
                <a:lnTo><a:pt x="{px}" y="{py}"/></a:lnTo>'''

        freeform_xml += f'''
              </a:path>
            </a:pathLst>
          </p:spPr>
        </p:sp>'''

        elem = etree.fromstring(freeform_xml)
        self.slide._element.append(elem)

    def _get_wave_y(self, t, amplitude, phase_shift):
        """计算波形在t处的Y坐标偏移"""
        return int(amplitude * math.sin(2 * math.pi * t * 1.5 + phase_shift))

    def generate(self):
        """生成双波形时间轴"""
        self.create_slide()
        slide_w = self.prs.slide_width
        slide_h = self.prs.slide_height

        # 标题
        if self._title:
            self.add_textbox(
                self._title, Inches(0.5), Inches(0.3),
                slide_w - Inches(1), Inches(0.6),
                font_size=28, bold=True,
                font_color=RGBColor(44, 62, 80),
                alignment=PP_ALIGN.LEFT
            )
        if self._subtitle:
            self.add_textbox(
                self._subtitle, Inches(0.5), Inches(0.85),
                slide_w - Inches(1), Inches(0.4),
                font_size=14,
                font_color=RGBColor(127, 140, 141),
                alignment=PP_ALIGN.LEFT
            )

        margin_x = Inches(0.8)
        wave_start_x = int(margin_x)
        wave_end_x = int(slide_w - margin_x)
        wave_center_y_1 = int(slide_h * 0.4)
        wave_center_y_2 = int(slide_h * 0.6)

        # 绘制两条波浪线
        self._draw_wave_path(
            wave_start_x, wave_end_x, wave_center_y_1,
            self._wave_amplitude, 0,
            self._wave1_color
        )
        self._draw_wave_path(
            wave_start_x, wave_end_x, wave_center_y_2,
            self._wave_amplitude, math.pi,
            self._wave2_color
        )

        # 在波形上放置节点和事件
        n = len(self._events)
        if n > 0:
            for i, event in enumerate(self._events):
                t = (i + 0.5) / n
                x = wave_start_x + int((wave_end_x - wave_start_x) * t)

                wave_num = event.get("wave", 1 if i % 2 == 0 else 2)
                if wave_num == 1:
                    y_offset = self._get_wave_y(t, self._wave_amplitude, 0)
                    center_y = wave_center_y_1
                else:
                    y_offset = self._get_wave_y(t, self._wave_amplitude, math.pi)
                    center_y = wave_center_y_2

                node_y = center_y + y_offset
                is_future = event.get("is_future", False)
                node_color = self._future_color if is_future else self._past_color

                # 节点圆形
                r = self._node_radius
                self.add_shape(
                    MSO_SHAPE.OVAL,
                    x - r, node_y - r, r * 2, r * 2,
                    fill_color=node_color
                )

                # 连接线（到另一个波形的对应位置）
                other_center_y = wave_center_y_2 if wave_num == 1 else wave_center_y_1
                other_phase = math.pi if wave_num == 1 else 0
                other_y_offset = self._get_wave_y(t, self._wave_amplitude, other_phase)
                other_y = other_center_y + other_y_offset

                connector = self.slide.shapes.add_connector(
                    1,  # straight connector
                    x, node_y,
                    x, other_y
                )
                connector.line.color.rgb = self._line_color
                connector.line.width = Pt(1)
                connector.line.dash_style = 2  # dash

                # 事件标签 - 上方或下方交替
                above = (wave_num == 1)
                label = event.get("label", "")
                date_str = event.get("date", "")
                detail = event.get("detail", "")

                label_y = node_y - r - Inches(1.2) if above else node_y + r + Inches(0.15)
                label_h = Inches(1.0)

                # 日期
                self.add_textbox(
                    date_str,
                    x - Inches(0.8), label_y,
                    Inches(1.6), Inches(0.25),
                    font_size=10, bold=True,
                    font_color=node_color,
                    alignment=PP_ALIGN.CENTER
                )
                # 标题
                self.add_textbox(
                    label,
                    x - Inches(0.8), label_y + Inches(0.25),
                    Inches(1.6), Inches(0.3),
                    font_size=12, bold=True,
                    font_color=RGBColor(44, 62, 80),
                    alignment=PP_ALIGN.CENTER
                )
                # 描述
                if detail:
                    self.add_textbox(
                        detail,
                        x - Inches(0.8), label_y + Inches(0.55),
                        Inches(1.6), Inches(0.35),
                        font_size=9,
                        font_color=RGBColor(127, 140, 141),
                        alignment=PP_ALIGN.CENTER
                    )

        # 图例
        legend_y = slide_h - Inches(0.5)
        legend_x = Inches(0.5)
        self.add_shape(MSO_SHAPE.OVAL, legend_x, legend_y, Inches(0.15), Inches(0.15),
                        fill_color=self._past_color)
        self.add_textbox("Past", legend_x + Inches(0.2), legend_y - Inches(0.02),
                          Inches(0.6), Inches(0.2), font_size=9,
                          font_color=RGBColor(127, 140, 141))

        self.add_shape(MSO_SHAPE.OVAL, legend_x + Inches(0.9), legend_y,
                        Inches(0.15), Inches(0.15), fill_color=self._future_color)
        self.add_textbox("Future", legend_x + Inches(1.1), legend_y - Inches(0.02),
                          Inches(0.6), Inches(0.2), font_size=9,
                          font_color=RGBColor(127, 140, 141))

        return self


if __name__ == "__main__":
    timeline = DualWaveTimeline()
    timeline.set_title("项目发展历程", "Dual Wave Timeline")
    timeline.set_data([
        {"label": "项目启动", "date": "2024-01", "detail": "需求分析完成", "is_future": False, "wave": 1},
        {"label": "原型设计", "date": "2024-03", "detail": "UI/UX设计交付", "is_future": False, "wave": 2},
        {"label": "开发阶段", "date": "2024-06", "detail": "核心功能开发", "is_future": False, "wave": 1},
        {"label": "内测上线", "date": "2024-09", "detail": "内部测试", "is_future": False, "wave": 2},
        {"label": "公测发布", "date": "2024-12", "detail": "开放注册", "is_future": True, "wave": 1},
        {"label": "版本迭代", "date": "2025-03", "detail": "功能扩展", "is_future": True, "wave": 2},
    ])
    timeline.save("output/dual_wave_timeline.pptx")
    print("双波形时间轴已生成: output/dual_wave_timeline.pptx")
