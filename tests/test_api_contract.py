"""数据注入契约测试

39 个生成器的 set_data / set_items 签名并不统一，这是刻意保留的兼容现状；
本测试用「类 -> 数据构造器」的显式契约表描述每个类的合法调用方式，
任何生成器的签名变更都会在这里失败，而不是等到批量生成时产出空模板。

契约表与 scripts/generate_all.py 的 sample 常量保持同步：
在注册表新增条目时，必须同时在这里登记数据契约。
"""

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from python.generators_chart import (
    AnimatedBarChart,
    BarChart,
    LineChart,
    PieChart,
)
from python.generators_content import (
    ComparisonGenerator,
    FourGridGenerator,
    FullImageOverlayGenerator,
    TextImageLayoutGenerator,
    ThreeColumnGenerator,
)
from python.generators_directory import (
    CardGridGenerator,
    CircularRingGenerator,
    DiamondAnimatedGenerator,
    HexagonGenerator,
    SidebarGenerator,
    TimelineStyleGenerator,
)
from python.generators_team import (
    OrgChartGenerator,
    PersonCardGenerator,
    TeamGridGenerator,
)
from python.generators_timeline import (
    DualWaveTimeline,
    HorizontalTimeline,
    SpiralTimeline,
    VerticalTimeline,
)

BAR_DATA = [{"label": f"Q{i}", "value": 100 + i} for i in range(1, 5)]
PIE_DATA = [{"label": f"区域{i}", "value": 10 + i} for i in range(1, 4)]
LINE_SERIES = [{"name": "2025", "data": [1.0, 2.0, 3.0]}]
X_LABELS = ["1月", "2月", "3月"]

DIR_ITEMS = [{"number": "01", "title": f"章节{i}", "description": "说明"} for i in range(1, 4)]
TIMELINE_ITEMS = [{"number": "01", "title": "启动", "subtitle": "调研"}]
EVENTS = [{"label": "成立", "date": "2020", "detail": "初创"}]
MEMBERS = [{"name": "张三", "title": "CEO"}]

CONTENT_ITEMS = {
    ComparisonGenerator: [{
        "left_title": "方案A", "left_items": ["快"],
        "right_title": "方案B", "right_items": ["稳"],
    }],
    FourGridGenerator: [{"number": "01", "title": "要点", "description": "说明"}],
    FullImageOverlayGenerator: [{"title": "主张", "subtitle": "Vision", "description": "描述"}],
    TextImageLayoutGenerator: [{"title": "标题", "description": "描述"}],
    ThreeColumnGenerator: [{"icon_text": "01", "title": "优势", "description": "描述"}],
}


def _instantiate(cls):
    """按各族的实际签名注入示例数据。"""
    if cls in (BarChart, AnimatedBarChart):
        data = cls()
        data.set_data(BAR_DATA, y_label="万元")
    elif cls is PieChart:
        data = cls()
        data.set_data(PIE_DATA)
    elif cls is LineChart:
        data = cls()
        data.set_data(LINE_SERIES, X_LABELS, y_label="万元")
    elif cls in (CardGridGenerator, SidebarGenerator, TimelineStyleGenerator):
        data = cls()
        data.set_title("目录")
        data.set_items(DIR_ITEMS if cls is not TimelineStyleGenerator else TIMELINE_ITEMS)
    elif cls in (CircularRingGenerator, DiamondAnimatedGenerator, HexagonGenerator):
        data = cls()
        data.set_title("目录")
        data.set_items(DIR_ITEMS)
    elif cls in (HorizontalTimeline, VerticalTimeline, SpiralTimeline, DualWaveTimeline):
        data = cls()
        data.set_data(EVENTS)
    elif cls is TeamGridGenerator:
        data = cls()
        data.set_members(MEMBERS)
        data.set_title("团队")
    elif cls is PersonCardGenerator:
        data = cls()
        data.set_data(name="张三", title="CEO", bio="创始人")
    elif cls is OrgChartGenerator:
        data = cls()
        data.set_title("组织架构")
        data.set_data([[{"name": "CEO", "title": "首席执行官"}]])
    elif cls in CONTENT_ITEMS:
        data = cls()
        data.set_title("标题")
        data.set_items(CONTENT_ITEMS[cls])
    else:
        raise AssertionError(f"契约表中缺少 {cls.__name__} 的数据构造方式")
    return data


CONTRACT_CLASSES = [
    BarChart, AnimatedBarChart, PieChart, LineChart,
    ComparisonGenerator, FourGridGenerator, FullImageOverlayGenerator,
    TextImageLayoutGenerator, ThreeColumnGenerator,
    CardGridGenerator, CircularRingGenerator, DiamondAnimatedGenerator,
    HexagonGenerator, SidebarGenerator, TimelineStyleGenerator,
    OrgChartGenerator, PersonCardGenerator, TeamGridGenerator,
    HorizontalTimeline, VerticalTimeline, SpiralTimeline, DualWaveTimeline,
]


@pytest.mark.parametrize("cls", CONTRACT_CLASSES, ids=lambda c: c.__name__)
def test_contract_generate_produces_slide(cls):
    """按契约注入数据后必须产出至少 1 页、首页形状数不少于 4 个。

    「至少 1 页」拦住 items 为空静默产出 0 页的问题；
    「形状 >= 4」拦住只有标题的空壳页面（对应 verify_templates.py 的口径）。
    """
    gen = _instantiate(cls)
    gen.generate()
    prs = gen.prs
    assert len(prs.slides) >= 1, f"{cls.__name__} 按契约注入数据后产出 0 页"
    assert len(prs.slides[0].shapes) >= 4, f"{cls.__name__} 首页形状数不足（疑似空壳）"


@pytest.mark.parametrize("cls", CONTRACT_CLASSES, ids=lambda c: c.__name__)
def test_contract_theme_is_optional(cls):
    """所有生成器都必须支持 theme=None（不传主题）。"""
    _instantiate(cls)


def test_theme_instantiation_contract():
    """ALL_THEMES 存放的是类而非实例——误用 ALL_THEMES['x'].primary 会静默产出无主题页面。"""
    from themes import ALL_THEMES

    for key, cls in ALL_THEMES.items():
        assert isinstance(cls, type), f"ALL_THEMES[{key!r}] 应为主题类"
        instance = cls()
        for attr in ("primary", "secondary", "accent", "background", "text", "muted", "dark_bg"):
            assert hasattr(instance, attr), f"主题 {key!r} 缺少属性 {attr}"
