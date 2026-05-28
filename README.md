# PPT模板资源库

> 现代PPT模板合集，包含动画模板和静态模板，支持Python和JavaScript编程生成。

## 特性

- **230 个预构建 .pptx 模板**（224个单页模板 + 6个完整演示文稿，动画 + 静态）
- **7 套配色主题**（蓝色科技、紫色渐变、暗金奢华、极简黑白、海洋蓝、自然绿、红色商务）
- **Python 生成脚本**（python-pptx）
- **JavaScript/TypeScript 生成脚本**（pptxgenjs）
- **完整演示文稿**（15-25页）× 6个场景
- **单页模板**可自由组合

## 快速开始

### 方式一：直接下载使用

1. 浏览 `templates/` 目录，按 `animated/`（动画）和 `static/`（静态）分类查找
2. 下载需要的 `.pptx` 文件
3. 用 PowerPoint 2016+ 或 WPS Office 打开

### 方式二：Python 生成

```bash
# 安装依赖
pip install -r requirements.txt

# 运行快速示例
python examples/quick_start.py

# 运行自定义配色示例
python examples/custom_colors.py

# 批量生成所有模板
python examples/batch_generate.py
```

### 方式三：JavaScript 生成

```bash
cd js && npm install && npx tsx examples/quick-start.ts
```

## 模板分类

### 封面模板

| 模板名称 | 类型 | 说明 |
|---------|------|------|
| 几何旋转封面 | 动画 | 多层几何图形旋转构图 |
| 圆环转场封面 | 动画 | 同心圆环渐变构图 |
| 列车穿雾封面 | 动画 | 极简雾气氛围封面 |
| 钻石揭示封面 | 动画 | 菱形主视觉封面 |
| 极简渐变封面 | 静态 | 简洁渐变风格 |
| 分屏封面 | 静态 | 左右分屏布局 |
| 镂空遮罩封面 | 静态 | 文字镂空效果 |
| 层次深度封面 | 静态 | 多层纵深感设计 |

### 目录模板

| 模板名称 | 类型 | 说明 |
|---------|------|------|
| 菱形动画目录 | 动画 | 菱形网格目录页 |
| 圆环目录 | 动画 | 圆形放射状目录 |
| 六边形目录 | 动画 | 蜂巢六边形目录 |
| 侧边栏目录 | 静态 | 左侧导航栏式目录 |
| 卡片网格目录 | 静态 | 卡片式网格目录 |
| 卡片网格目录 | 静态 | 圆角卡片网格 |

### 时间轴模板

| 模板名称 | 类型 | 说明 |
|---------|------|------|
| 水平时间轴 | 静态 | 经典水平线时间轴 |
| 垂直时间轴 | 静态 | 垂直瀑布式时间轴 |
| 螺旋时间轴 | 静态 | 螺旋路径时间轴 |
| 双波浪时间轴 | 静态 | 波浪形时间轴 |

### 团队介绍模板

| 模板名称 | 类型 | 说明 |
|---------|------|------|
| 团队网格 | 静态 | 网格排列成员卡片 |
| 人物卡片 | 静态 | 单人大幅人物介绍 |
| 组织架构 | 静态 | 树形组织结构图 |

### 完整演示文稿

| 场景名称 | 说明 | 页数 |
|---------|------|------|
| 商业计划书 | 完整商业计划演示 | ~20页 |
| 职业规划 | 个人职业规划展示 | ~18页 |
| 产品发布 | 新产品发布演示 | ~22页 |
| 年度报告 | 企业年度报告 | ~25页 |
| 教育课件 | 教学培训课件 | ~20页 |
| 科技主题 | 科技产品展示 | ~18页 |

## 配色主题

| 主题名 | 主色 | 副色 | 适合场景 |
|-------|------|------|---------|
| 蓝色科技 | `#0066CC` | `#00CC99` | 科技、互联网 |
| 紫色渐变 | `#7B2FBE` | `#E040FB` | 创意、设计 |
| 暗金奢华 | `#1A1A2E` | `#C9A96E` | 高端、商务 |
| 极简黑白 | `#000000` | `#333333` | 通用、学术 |
| 海洋蓝 | `#0077B6` | `#00B4D8` | 教育、培训 |
| 自然绿 | `#2D6A4F` | `#52B788` | 环保、健康 |
| 红色商务 | `#C0392B` | `#E74C3C` | 商务、营销 |

## Python API 使用示例

### 快速生成封面

```python
from python.generators_cover import GeometricRotationCover

# 创建几何旋转封面
cover = GeometricRotationCover()
cover.set_title("年度报告").set_subtitle("Annual Report 2026")
cover.generate().save("output/report_cover.pptx")
print("封面已生成！")
```

### 使用主题生成目录

```python
from themes import ALL_THEMES
from python.generators_directory.diamond_animated import DiamondAnimatedGenerator

# 使用紫色渐变主题
theme = ALL_THEMES["purple_gradient"]()

gen = DiamondAnimatedGenerator(theme=theme)
gen.set_title("内容概览")
gen.set_items([
    {"number": "01", "title": "市场分析"},
    {"number": "02", "title": "产品设计"},
    {"number": "03", "title": "运营策略"},
])
gen.generate()
gen.save("output/themed_directory.pptx")
```

### 使用完整演示文稿组装器

```python
from python.generators_complete import BusinessPlanAssembler

# 生成完整商业计划书（20+页）
prs = BusinessPlanAssembler()
prs.set_title("智能办公解决方案")
prs.set_subtitle("Smart Office Solution")
prs.generate().save("output/business_plan.pptx")
```

## JavaScript API 使用示例

```typescript
import { TemplateGenerator } from './src/base';
import { blueTechnology } from './src/themes';

// 创建生成器并使用主题
const gen = new TemplateGenerator(blueTechnology);
const slide = gen.createSlide();

// 添加文本
gen.addText(slide, {
  x: 1, y: 2, w: 8, h: 1,
  text: 'Hello PPT',
  fontSize: 36,
  bold: true,
  align: 'center',
  color: gen.getTheme().primary,
});

// 保存文件
await gen.save('output/js_example');
```

## 文件命名规范

```
[类别]_[类型]_[名称].pptx
```

示例：
- `cover_animated_geometric_rotation.pptx`
- `directory_static_card_grid.pptx`
- `timeline_horizontal.pptx`
- `complete_business_plan.pptx`

## 目录结构

```
PPT项目/
├── python/                  # Python生成器源码
│   ├── base.py             # 基类TemplateGenerator
│   ├── utils.py            # 工具函数
│   ├── animation.py        # 动画引擎
│   ├── generators_cover/   # 封面生成器
│   ├── generators_directory/ # 目录生成器
│   ├── generators_timeline/  # 时间轴生成器
│   ├── generators_chart/     # 图表生成器
│   ├── generators_team/      # 团队介绍生成器
│   ├── generators_ending/    # 结束页生成器
│   └── generators_complete/  # 完整演示文稿组装器
├── js/                     # JavaScript生成器源码
│   ├── src/
│   │   ├── base.ts         # TypeScript基类
│   │   ├── utils.ts        # 工具函数
│   │   └── themes/         # 主题定义
│   └── package.json
├── themes/                 # Python配色主题
├── templates/              # 预生成的.pptx模板（230个）
│   ├── animated/           # 动画模板（70个）
│   │   ├── cover/          # 封面（28个）
│   │   ├── directory/      # 目录（21个）
│   │   ├── timeline/       # 时间轴（14个）
│   │   └── chart/          # 图表（7个）
│   ├── static/             # 静态模板（154个）
│   │   ├── cover/          # 封面（28个）
│   │   ├── directory/      # 目录（14个）
│   │   ├── content/        # 内容页（35个）
│   │   ├── timeline/       # 时间轴（14个）
│   │   ├── chart/          # 图表（21个）
│   │   ├── team/           # 团队介绍（21个）
│   │   └── ending/         # 结束页（21个）
│   └── complete/           # 完整演示文稿（6个）
├── examples/               # 示例脚本
├── scripts/                # 生成脚本
└── tests/                  # 测试文件
```

## 兼容性

- **PowerPoint 2016+** (Windows/Mac)
- **WPS Office 2019+**
- **Google Slides**（动画支持有限，静态模板完全兼容）

## 环境要求

- Python 3.8+（Python端）
- Node.js 18+（JavaScript端）
- 系统需安装 Microsoft YaHei（微软雅黑）字体以获得最佳显示效果

## 常见问题

### Q: 动画在 WPS 中无法播放？
A: WPS Office 对OOXML动画支持有限。建议使用 Microsoft PowerPoint 2016+ 打开动画模板。

### Q: 如何自定义配色？
A: 继承 `BaseTheme` 类，覆盖 `primary`、`secondary` 等颜色属性即可创建自定义主题。详见 `examples/custom_colors.py`。

### Q: 生成的文件在哪里？
A: 默认保存在当前工作目录。可通过 `generator.save("output/path.pptx")` 指定输出路径。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
