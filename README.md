[![CI](https://github.com/wuhua2026/ppt-templates/actions/workflows/ci.yml/badge.svg)](https://github.com/wuhua2026/ppt-templates/actions/workflows/ci.yml)
# PPT模板资源库

> 现代PPT模板合集，包含动画模板和静态模板，支持Python和JavaScript编程生成。

## 特性

- **237 个预构建 .pptx 模板**（231个单页模板 + 6个完整演示文稿，动画 + 静态）
- **32 种单页板式 × 7 套配色主题**，另加 6 套完整演示文稿
- **7 套配色主题**（蓝色科技、紫色渐变、暗金奢华、极简黑白、海洋蓝、自然绿、红色商务）
- **Python 生成脚本**（python-pptx）
- **JavaScript/TypeScript 生成脚本**（pptxgenjs）
- **完整演示文稿**（16-22页）× 6个场景
- **单页模板**可自由组合
- **产物可复现**：全部模板由脚本生成，重跑后内容逐页一致（CI 已接入空壳模板自检）

## 快速开始

### 方式一：直接下载使用

1. 浏览 `templates/` 目录，按 `animated/`（动画）和 `static/`（静态）分类查找
2. 下载需要的 `.pptx` 文件
3. 用 PowerPoint 2016+ 或 WPS Office 打开

### 方式二：Python 生成

```bash
# 安装依赖
pip install -r requirements.txt

# 可选：以可编辑模式安装，之后可在任意位置 import
pip install -e .

# 运行快速示例
python examples/quick_start.py

# 运行自定义配色示例
python examples/custom_colors.py

# 批量生成所有模板
python examples/batch_generate.py
```

### 方式三：JavaScript 生成

```bash
cd js && npm install && npm run example
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
| 时间轴目录 | 静态 | 垂直时间轴式目录 |

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

页数为确定值——每套文稿的页面序列在 `generate()` 中固定编排，不含动态分支，因此每次生成结果一致。

| 场景名称 | 说明 | 页数 |
|---------|------|------|
| 商业计划书 | 完整商业计划演示 | 18页 |
| 职业规划 | 个人职业规划展示 | 16页 |
| 产品发布 | 新产品发布演示 | 20页 |
| 年度报告 | 企业年度报告 | 22页 |
| 教育课件 | 教学培训课件 | 18页 |
| 科技主题 | 科技产品展示 | 16页 |

## 配色主题

| 主题名 | 键名 | 主色 | 副色 | 背景 | 适合场景 |
|-------|------|------|------|------|---------|
| 蓝色科技 | `blue_technology` | `#0066CC` | `#00CC99` | `#FFFFFF` | 科技、互联网 |
| 紫色渐变 | `purple_gradient` | `#7B2FBE` | `#E040FB` | `#FFFFFF` | 创意、设计 |
| 暗金奢华 | `dark_gold` | `#C9A96E` | `#B48C50` | `#1A1A2E` | 高端、商务 |
| 极简黑白 | `minimalist_bw` | `#000000` | `#333333` | `#FFFFFF` | 通用、学术 |
| 海洋蓝 | `ocean_blue` | `#0077B6` | `#00B4D8` | `#FFFFFF` | 教育、培训 |
| 自然绿 | `green_nature` | `#2D6A4F` | `#52B788` | `#FFFFFF` | 环保、健康 |
| 红色商务 | `red_business` | `#C0392B` | `#E74C3C` | `#FFFFFF` | 商务、营销 |

> 取值以 `themes/*.py` 为准，上表由代码读出后填入。暗金奢华是唯一使用深色背景的主题，其主色为金色而非背景色。

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
from themes import ALL_THEMES
from python.generators_complete import BusinessPlanAssembler

# 生成完整商业计划书（固定 18 页）
prs = BusinessPlanAssembler(theme=ALL_THEMES["blue_technology"]())
prs.set_title("智能办公解决方案")
prs.set_subtitle("Smart Office Solution")
prs.generate().save("output/business_plan.pptx")
```

`theme` 参数可省略，此时使用组装器内置的默认配色。

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

单页模板按「模板名 + 主题」命名，存放在 `templates/[static|animated]/[类型]/` 下：

```
[模板名]_[主题键名].pptx
```

示例：
- `static/cover/split_screen_ocean_blue.pptx`
- `static/chart/bar_chart_ocean_blue.pptx`
- `animated/directory/diamond_animated_purple_gradient.pptx`

完整演示文稿不按主题展开，直接放在 `templates/complete/` 下，文件名即场景名：
- `complete/business_plan.pptx`

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
├── templates/              # 预生成的.pptx模板（237个）
│   ├── animated/           # 动画模板（70个）
│   │   ├── cover/          # 封面（28个）
│   │   ├── directory/      # 目录（21个）
│   │   ├── timeline/       # 时间轴（14个）
│   │   └── chart/          # 图表（7个）
│   ├── static/             # 静态模板（161个）
│   │   ├── cover/          # 封面（28个）
│   │   ├── directory/      # 目录（21个）
│   │   ├── content/        # 内容页（35个）
│   │   ├── timeline/       # 时间轴（14个）
│   │   ├── chart/          # 图表（21个）
│   │   ├── team/           # 团队介绍（21个）
│   │   └── ending/         # 结束页（21个）
│   └── complete/           # 完整演示文稿（6个）
├── examples/               # 示例脚本
├── scripts/                # 生成脚本
│   ├── generate_all.py     # 批量生成 231 个单页模板
│   ├── generate_decks.py   # 生成 6 套完整演示文稿
│   ├── verify_templates.py # 产物自检（空壳模板拦截）
│   └── check_parity.py     # Python / TypeScript 双端一致性
└── tests/                  # 测试文件
```

## 兼容性

- **PowerPoint 2016+** (Windows/Mac)
- **WPS Office 2019+**
- **Google Slides**（动画支持有限，静态模板完全兼容）

## 可验证性

仓库中的模板产物不是随手上传的二进制文件，而是由脚本确定性生成、且每次都可重新校验：

```bash
# 1) 重新生成全部 231 个单页模板（约 6 秒）
python scripts/generate_all.py --output ./out

# 2) 重新生成 6 套完整演示文稿
python scripts/generate_decks.py --output ./out_complete

# 3) 校验产物：任何 0 页、或首页只有标题的模板都会让命令以非零码退出
python scripts/verify_templates.py templates
```

第 3 步已接入 CI（job 名「产物自检」）。判断标准是**首页形状数不少于 4 个**——纯标题页通常只有 1~3 个形状，含实质内容的页面则有 12~53 个。

> 说明：直接比对 `.pptx` 的 MD5 会全部不相等，因为 zip 内嵌了时间戳。若需判断两次生成是否等价，应解压后比对 `ppt/slides/*` 与 `ppt/theme/*` 的内容签名。

## 环境要求

- Python 3.10+（Python端，CI 覆盖 3.10 / 3.11 / 3.12）
- Node.js 18+（JavaScript端）
- 系统需安装 Microsoft YaHei（微软雅黑）字体以获得最佳显示效果

## 常见问题

### Q: 动画在 WPS 中无法播放？
A: WPS Office 对OOXML动画支持有限。建议使用 Microsoft PowerPoint 2016+ 打开动画模板。

### Q: 如何自定义配色？
A: 继承 `BaseTheme` 类，覆盖 `primary`、`secondary` 等颜色属性即可创建自定义主题。详见 `examples/custom_colors.py`。

### Q: 生成的文件在哪里？
A: 默认保存在当前工作目录。可通过 `generator.save("output/path.pptx")` 指定输出路径。

### Q: 为什么我生成的图表页是空的？
A: 图表生成器没有内置默认数据，必须显式调用 `set_data()`。各图表的数据契约不同：柱状图/饼图是 `[{label, value}]`，而折线图是 `set_data(series, x_labels)`，其中 `series = [{name, data: [数值...]}]`——**`data` 是数值列表，不是 `{x, y}` 字典**。

### Q: 为什么内容页一张幻灯片都没生成？
A: 内容页生成器同样没有内置数据，且采用「遍历 items，每条一页」的模式。items 为空即产出 0 页，不会报错。可运行的样本数据见 `scripts/generate_all.py` 中的 `DEFAULT_CONTENT_*` 常量。

### Q: 内容页换主题为什么有些颜色没变？
A: 内容页的主色/副色/强调色已随主题变化，但**卡片底色与中性分隔线是刻意保留的固定配色**——浅色底保证了正文文字的对比度，若随之换成暗金等主题的深色会导致可读性下降。只有标题下划线、栏目标记、图标色这些「结构色」跟随主题。

### Q: Python 与 TypeScript 生成的版式尺寸一样吗？
A: 不一样，且这是已知差异：Python 基类默认 10×7.5 英寸（4:3），TypeScript 基类默认 13.33×7.5 英寸（16:9）。Python 侧 230 余个模板的坐标按 4:3 设计，统一画布需要重新排版，因此暂未合并。

### Q: 新增一个生成器要改哪些地方？
A: 三处：族目录的 `__init__.py`、根目录 `python/__init__.py`、以及 TypeScript 侧对应族。若希望它进入批量生成，还需在 `scripts/generate_all.py` 的 `TEMPLATE_REGISTRY` 中登记条目并附带 `sample` 示例数据——缺了示例数据会产出空模板，且会被 CI 拦下。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
