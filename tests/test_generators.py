"""图表生成器与主题系统的单元测试

注意：各生成器的 set_data 签名并不统一，因此按类分别构造数据：
- BarChart / AnimatedBarChart : set_data(data, y_label)
- PieChart                   : set_data(data)
- LineChart                  : set_data(series, x_labels, y_label)
"""

import os
import sys

import pytest
from pptx import Presentation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from python.generators_chart import (
    AnimatedBarChart,
    BarChart,
    LineChart,
    PieChart,
)
from themes import ALL_THEMES

BAR_DATA = [
    {"label": "Q1", "value": 120},
    {"label": "Q2", "value": 180},
    {"label": "Q3", "value": 95},
    {"label": "Q4", "value": 210},
]

PIE_DATA = [
    {"label": "华东", "value": 42},
    {"label": "华南", "value": 28},
    {"label": "华北", "value": 30},
]

LINE_SERIES = [
    {"name": "2024", "data": [12.0, 18.0, 9.5, 21.0]},
    {"name": "2025", "data": [15.0, 22.0, 13.0, 25.5]},
]

X_LABELS = ["Q1", "Q2", "Q3", "Q4"]


def _theme(name="blue_technology"):
    """ALL_THEMES 中存放的是主题类，需要实例化后使用。"""
    return ALL_THEMES[name]()


def _assert_valid_pptx(path, expected_slides=1):
    assert path.exists(), f"未生成文件: {path}"
    assert path.stat().st_size > 0, "生成的 PPTX 为空"
    reopened = Presentation(str(path))
    assert len(reopened.slides) == expected_slides
    return reopened


def test_bar_chart_roundtrip(tmp_path):
    chart = BarChart(theme=_theme())
    chart.set_title("季度营收", "单元测试")
    chart.set_data(BAR_DATA, y_label="万元")
    chart.generate()
    out = tmp_path / "bar.pptx"
    chart.save(str(out))
    _assert_valid_pptx(out)


def test_animated_bar_chart_roundtrip(tmp_path):
    chart = AnimatedBarChart(theme=_theme())
    chart.set_title("季度营收（动画）", "单元测试")
    chart.set_data(BAR_DATA, y_label="万元")
    chart.generate()
    out = tmp_path / "animated.pptx"
    chart.save(str(out))
    _assert_valid_pptx(out)


def test_pie_chart_roundtrip(tmp_path):
    chart = PieChart(theme=_theme())
    chart.set_title("区域占比", "单元测试")
    chart.set_data(PIE_DATA)
    chart.generate()
    out = tmp_path / "pie.pptx"
    chart.save(str(out))
    _assert_valid_pptx(out)


def test_line_chart_roundtrip(tmp_path):
    chart = LineChart(theme=_theme())
    chart.set_title("年度趋势", "单元测试")
    chart.set_data(LINE_SERIES, X_LABELS, y_label="万元")
    chart.generate()
    out = tmp_path / "line.pptx"
    chart.save(str(out))
    _assert_valid_pptx(out)


@pytest.mark.parametrize("name", sorted(ALL_THEMES))
def test_theme_exposes_required_colors(name):
    theme = ALL_THEMES[name]()
    for attr in ("primary", "secondary", "accent", "background", "text", "muted"):
        assert getattr(theme, attr, None) is not None, f"{name} 缺少颜色属性 {attr}"


@pytest.mark.parametrize("name", sorted(ALL_THEMES))
def test_theme_gradient_returns_color_pair(name):
    theme = ALL_THEMES[name]()
    for variant in ("primary", "accent", "dark"):
        gradient = theme.get_gradient(variant)
        assert isinstance(gradient, list) and len(gradient) >= 2


@pytest.mark.parametrize(
    "cls",
    [BarChart, PieChart, LineChart, AnimatedBarChart],
    ids=lambda c: c.__name__,
)
def test_generator_accepts_every_theme(cls):
    """每个生成器都应能用全部主题实例化，避免主题缺少字段导致运行期崩溃。"""
    for name in ALL_THEMES:
        assert cls(theme=ALL_THEMES[name]()) is not None
