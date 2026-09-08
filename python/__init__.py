"""PPT 模板生成器（Python 端）—— 统一公开 API

推荐用法：

    from python import BarChart, ALL_THEMES

    theme = ALL_THEMES["blue_technology"]()
    chart = BarChart(theme=theme)
    chart.set_title("季度营收").set_data([{"label": "Q1", "value": 120}])
    chart.generate()
    chart.save("out.pptx")

本模块不改变任何既有子模块路径（``python.base``、``python.generators_cover`` 等
仍可直接导入），仅在此处做一次汇总导出，方便外部使用。
"""

from python.base import TemplateGenerator

from python.utils import (
    hex_to_rgb,
    create_circle_positions,
    create_grid_positions,
    add_shadow,
    set_shape_transparency,
    format_text,
)

from python.animation import (
    apply_animations_to_slide,
    add_slide_morph_transition,
)

from themes import BaseTheme, ALL_THEMES

# ---------------- 封面（8） ----------------
from python.generators_cover import (
    GeometricRotationCover,
    CircleRingCover,
    TrainMistCover,
    DiamondRevealCover,
    MinimalistGradientCover,
    SplitScreenCover,
    HollowMaskCover,
    LayeredDepthCover,
)

# ---------------- 目录（6） ----------------
from python.generators_directory import (
    DiamondAnimatedGenerator,
    CircularRingGenerator,
    HexagonGenerator,
    SidebarGenerator,
    CardGridGenerator,
    TimelineStyleGenerator,
)

# ---------------- 内容页（5） ----------------
from python.generators_content import (
    TextImageLayoutGenerator,
    ThreeColumnGenerator,
    FourGridGenerator,
    FullImageOverlayGenerator,
    ComparisonGenerator,
)

# ---------------- 图表（4） ----------------
from python.generators_chart import (
    BarChart,
    PieChart,
    LineChart,
    AnimatedBarChart,
)

# ---------------- 时间轴（4） ----------------
from python.generators_timeline import (
    DualWaveTimeline,
    HorizontalTimeline,
    VerticalTimeline,
    SpiralTimeline,
)

# ---------------- 团队（3） ----------------
from python.generators_team import (
    PersonCardGenerator,
    TeamGridGenerator,
    OrgChartGenerator,
)

# ---------------- 结尾（3） ----------------
from python.generators_ending import (
    ThankYouGenerator,
    QRCodeGenerator,
    ContactPageGenerator,
)

# ---------------- 完整演示文稿组装器（6） ----------------
from python.generators_complete import (
    BusinessPlanAssembler,
    CareerPlanningAssembler,
    ProductLaunchAssembler,
    AnnualReportAssembler,
    EducationCourseAssembler,
    TechnologyThemeAssembler,
)

__version__ = "1.1.0"

__all__ = [
    # 基础
    "TemplateGenerator",
    "BaseTheme",
    "ALL_THEMES",
    "hex_to_rgb",
    "create_circle_positions",
    "create_grid_positions",
    "add_shadow",
    "set_shape_transparency",
    "format_text",
    "apply_animations_to_slide",
    "add_slide_morph_transition",
    # 封面
    "GeometricRotationCover",
    "CircleRingCover",
    "TrainMistCover",
    "DiamondRevealCover",
    "MinimalistGradientCover",
    "SplitScreenCover",
    "HollowMaskCover",
    "LayeredDepthCover",
    # 目录
    "DiamondAnimatedGenerator",
    "CircularRingGenerator",
    "HexagonGenerator",
    "SidebarGenerator",
    "CardGridGenerator",
    "TimelineStyleGenerator",
    # 内容页
    "TextImageLayoutGenerator",
    "ThreeColumnGenerator",
    "FourGridGenerator",
    "FullImageOverlayGenerator",
    "ComparisonGenerator",
    # 图表
    "BarChart",
    "PieChart",
    "LineChart",
    "AnimatedBarChart",
    # 时间轴
    "DualWaveTimeline",
    "HorizontalTimeline",
    "VerticalTimeline",
    "SpiralTimeline",
    # 团队
    "PersonCardGenerator",
    "TeamGridGenerator",
    "OrgChartGenerator",
    # 结尾
    "ThankYouGenerator",
    "QRCodeGenerator",
    "ContactPageGenerator",
    # 完整演示文稿
    "BusinessPlanAssembler",
    "CareerPlanningAssembler",
    "ProductLaunchAssembler",
    "AnnualReportAssembler",
    "EducationCourseAssembler",
    "TechnologyThemeAssembler",
    "__version__",
]
