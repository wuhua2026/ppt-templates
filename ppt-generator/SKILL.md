---
name: ppt-generator
description: "Generate PowerPoint presentations from a template library with 230+ templates, 7 color themes, Python and JavaScript generators. Triggers on PPT, slides, or presentation creation requests."
---

# PPT模板生成器

## 概述

本skill用于调用GitHub上的PPT模板库（https://github.com/wuhua2026/ppt-templates），
通过Python或JavaScript代码生成专业的PowerPoint演示文稿。

模板库包含：
- 230个预构建.pptx模板（动画 + 静态 + 完整文稿）
- 7套配色主题
- Python（python-pptx）和 JavaScript（pptxgenjs）双语言支持

## 第一步：环境准备

每次使用前，确认模板库已安装。运行安装脚本：

```bash
d:/python/miniconda/python.exe "path/to/ppt-generator/scripts/setup.py"
```

模板库安装在 `~/.ppt-templates/` 目录下。如果已存在则自动更新。

## 第二步：确定使用Python还是JavaScript

- **Python**（推荐）：功能更完整，支持动画XML操作，模板更多
- **JavaScript**：适合Web开发者，基于pptxgenjs

## Python使用方式

模板库路径：`~/.ppt-templates/`

### 基本导入

```python
import sys
sys.path.insert(0, os.path.expanduser("~/.ppt-templates"))

# 导入主题
from themes import ALL_THEMES
theme = ALL_THEMES["blue_technology"]()  # 蓝色科技主题

# 导入生成器
from python.generators_cover import GeometricRotationCover
from python.generators_complete import BusinessPlanAssembler
```

### 7套可用主题

| 键名 | 中文名 | 主色 | 适合场景 |
|------|--------|------|---------|
| `blue_technology` | 蓝色科技 | #0066CC | 科技、互联网 |
| `purple_gradient` | 紫色渐变 | #7B2FBE | 创意、设计 |
| `dark_gold` | 暗金奢华 | #1A1A2E | 高端、商务 |
| `minimalist_bw` | 极简黑白 | #000000 | 通用、学术 |
| `ocean_blue` | 海洋蓝 | #0077B6 | 教育、培训 |
| `green_nature` | 自然绿 | #2D6A4F | 环保、健康 |
| `red_business` | 红色商务 | #C0392B | 商务、营销 |

### 可用生成器

**封面生成器（8个）：**
- `GeometricRotationCover` - 几何旋转封面（动画）
- `CircleRingCover` - 圆环转场封面（动画）
- `TrainMistCover` - 列车穿雾封面（动画）
- `DiamondRevealCover` - 钻石揭示封面（动画）
- `MinimalistGradientCover` - 极简渐变封面（静态）
- `SplitScreenCover` - 分屏封面（静态）
- `HollowMaskCover` - 镂空遮罩封面（静态）
- `LayeredDepthCover` - 层次深度封面（静态）

**目录生成器（6个）：**
- `DiamondAnimatedGenerator` - 菱形动画目录
- `CircularRingGenerator` - 圆环目录
- `HexagonGenerator` - 六边形目录
- `SidebarGenerator` - 侧边栏目录
- `CardGridGenerator` - 卡片网格目录
- `TimelineStyleGenerator` - 时间轴目录

**内容页生成器（5个）：**
- `TextImageLayoutGenerator` - 图文排版
- `ThreeColumnGenerator` - 三栏布局
- `FourGridGenerator` - 四宫格布局
- `FullImageOverlayGenerator` - 全图叠加
- `ComparisonGenerator` - 对比布局

**时间轴生成器（4个）：**
- `DualWaveTimeline` - 双波形时间轴（动画）
- `HorizontalTimeline` - 水平时间轴
- `VerticalTimeline` - 垂直时间轴
- `SpiralTimeline` - 螺旋时间轴（动画）

**图表生成器（4个）：**
- `BarChart` - 柱状图
- `PieChart` - 饼图
- `LineChart` - 折线图
- `AnimatedBarChart` - 动画柱状图

**团队页生成器（3个）：**
- `PersonCardGenerator` - 人物介绍卡片
- `TeamGridGenerator` - 团队网格
- `OrgChartGenerator` - 组织架构图

**结尾页生成器（3个）：**
- `ThankYouGenerator` - 感谢页
- `QRCodeGenerator` - 二维码页
- `ContactPageGenerator` - 联系方式页

**完整演示文稿组装器（6个）：**
- `BusinessPlanAssembler` - 商业计划书（18页）
- `CareerPlanningAssembler` - 职业生涯规划（16页）
- `ProductLaunchAssembler` - 产品发布会（20页）
- `AnnualReportAssembler` - 年度报告（22页）
- `EducationCourseAssembler` - 教育课件（18页）
- `TechnologyThemeAssembler` - 科技主题（16页）

### 生成单页模板示例

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.ppt-templates"))

from python.generators_cover.geometric_rotation import GeometricRotationCover
from themes.blue_technology import BlueTechnologyTheme

# 创建封面
cover = GeometricRotationCover(theme=BlueTechnologyTheme())
cover.set_title("我的演示文稿")
cover.set_subtitle("副标题内容")
cover.generate()
cover.save("output_cover.pptx")
```

### 生成完整演示文稿示例

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.ppt-templates"))

from python.generators_complete.business_plan import BusinessPlanAssembler
from themes.blue_technology import BlueTechnologyTheme

deck = BusinessPlanAssembler(theme=BlueTechnologyTheme())
deck.set_title("项目商业计划")
deck.set_subtitle("2026年度规划")
deck.generate()
deck.save("output_business_plan.pptx")
```

### 自定义主题

```python
from themes import BaseTheme
from pptx.dml.color import RGBColor

class MyTheme(BaseTheme):
    name = "自定义主题"
    primary = RGBColor(255, 107, 107)    # 自定义主色
    secondary = RGBColor(78, 205, 196)   # 自定义副色
    accent = RGBColor(255, 195, 0)       # 自定义强调色

cover = GeometricRotationCover(theme=MyTheme())
```

## JavaScript使用方式

```bash
cd ~/.ppt-templates/js
npm install
```

```javascript
const pptxgen = require("pptxgenjs");
const { GeometricRotation } = require("./src/generators/cover");
const { blueTechnology } = require("./src/themes");

const gen = new GeometricRotation({ theme: blueTechnology });
gen.setTitle("我的演示文稿");
gen.setSubtitle("副标题");
const pres = gen.generate();
pres.writeFile({ fileName: "output.pptx" });
```

## 直接使用预构建模板

如果不需要编程生成，可以直接使用 `~/.ppt-templates/templates/` 目录下的.pptx文件：

```
templates/
├── animated/          # 动画模板（70个）
│   ├── cover/         # 封面（28个）
│   ├── directory/     # 目录（21个）
│   ├── timeline/      # 时间轴（14个）
│   └── chart/         # 图表（7个）
├── static/            # 静态模板（154个）
│   ├── cover/         # 封面（28个）
│   ├── directory/     # 目录（14个）
│   ├── content/       # 内容页（35个）
│   ├── timeline/      # 时间轴（14个）
│   ├── chart/         # 图表（21个）
│   ├── team/          # 团队页（21个）
│   └── ending/        # 结尾页（21个）
└── complete/          # 完整演示文稿（6个）
```

文件命名规则：`{类型}_{主题名}.pptx`
例如：`geometric_rotation_blue_technology.pptx`

## 注意事项

- 动画效果仅在 Microsoft PowerPoint 2016+ 中完整播放
- WPS Office 对动画支持有限，建议使用静态模板
- 所有生成器支持链式调用：`generator.set_title("...").set_subtitle("...").generate()`
- 输出文件默认保存在当前工作目录
