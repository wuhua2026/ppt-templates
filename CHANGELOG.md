# 变更日志

本文件记录项目的显著变更。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.1.0] - 2026-09-08

### 新增

- **分支保护**：`main` 要求 CI 通过（Python 3.12 / TypeScript / 双端一致性）后才能合并
- **仓库治理文件**：Issue 模板（缺陷报告 / 功能建议）与 PR 模板

### 变更

- `examples/batch_generate.py` 改为委托 `scripts/generate_all.py`，消除两份重复的生成逻辑

## [1.0.0] - 2026-09-08

首个正式版本。

### 新增

- **统一公开 API**：`python/__init__.py` 汇总导出 39 个生成器类、`TemplateGenerator`、
  `ALL_THEMES` 及常用工具函数，可直接使用 `from python import BarChart, ALL_THEMES`
- **Python 打包支持**：新增 `pyproject.toml`，支持 `pip install -e .` 与构建分发
- **单元测试**：新增 31 个 pytest 用例，覆盖基类、四大图表生成器与全部 7 套主题
- **CI 工作流**：`.github/workflows/ci.yml`，在 Python 3.10 / 3.11 / 3.12 上运行测试，
  并对 TypeScript 端做 `tsc --noEmit` 类型检查
- **双端一致性校验**：新增 `scripts/check_parity.py`，比对 Python 与 TypeScript 两侧
  生成器数量，防止长期功能漂移

### 修复

- 修正 README 中无法执行的 JS 快速开始命令（`npx tsx` → `npm run example`；
  `tsx` 不在依赖中，实际可用的是 `ts-node`）
- 移除误提交的三个示例输出文件 `output_quick_*.pptx`
- 补全 `.gitignore`，新增 Python 与 Node 的构建产物、缓存与虚拟环境规则

### 变更

- Python 版本要求由「3.8+」收窄为「3.10+」：3.8 已于 2024-10 结束支持，且 CI 从未覆盖
- JS 包名由 `ppt-generator` 改为 `@wuhua2026/ppt-templates`：原名称已被 npm 上
  其他项目占用，无法发布

### 文档

- 新增 `CONTRIBUTING.md`、`CHANGELOG.md`、Issue 与 PR 模板
- README 补充可编辑安装方式

[1.0.0]: https://github.com/wuhua2026/ppt-templates/releases/tag/v1.0.0
