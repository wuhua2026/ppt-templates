# 贡献指南

感谢你愿意为 PPT 模板资源库贡献内容。本文件说明仓库结构与贡献方式。

## 仓库结构

```
templates/                  230 个预构建 .pptx（由 scripts/generate_all.py 生成）
python/                     Python 生成器（基于 python-pptx）
  base.py                   所有生成器的基类 TemplateGenerator
  animation.py              动画 XML 注入
  utils.py                  颜色、布局、阴影等工具函数
  generators_<族>/          8 个生成器族，共 39 个生成器类
themes/                     7 套配色主题（BaseTheme 派生）
js/                         TypeScript 生成器（基于 pptxgenjs），与 Python 端一一对应
scripts/                    构建与校验脚本
tests/                      pytest 用例
```

## 本地开发

```bash
# Python 端
pip install -r requirements.txt
pip install -e .
pytest

# TypeScript 端
cd js && npm install && npx tsc --noEmit

# 双端一致性校验
python scripts/check_parity.py
```

## 提交前请确认

1. `pytest` 全部通过
2. `npx tsc --noEmit` 无类型错误
3. `python scripts/check_parity.py` 报告双端一致
4. 若新增生成器，**Python 与 TypeScript 两侧都要实现**，否则 CI 的一致性校验会失败

## 约定

### 新增生成器

1. 在对应的 `python/generators_<族>/` 下新建模块，类继承 `TemplateGenerator`
2. 在该族的 `__init__.py` 中导出，并加入 `__all__`
3. 在 `python/__init__.py` 的汇总导出中同步添加
4. 在 `js/src/generators/<族>.ts` 中实现等价版本并 `export`
5. 补一个测试用例

### 新增主题

1. 在 `themes/` 下新建模块，继承 `BaseTheme`
2. 至少覆盖 `primary / secondary / accent / background / text / muted` 六个颜色属性
3. 在 `themes/__init__.py` 的 `ALL_THEMES` 中注册
4. 主题测试会自动覆盖新主题，无需额外改动

> 注意：`ALL_THEMES` 中存放的是**主题类**而非实例，使用时需要 `ALL_THEMES["xxx"]()`。

### 不要提交

- `output_*.pptx` 等生成产物（已在 `.gitignore` 中）
- 字体文件、图片素材等二进制大文件
- API 密钥或个人配置

## 提交信息

使用 Conventional Commits 前缀，便于生成 CHANGELOG：

```
feat:     新功能
fix:      缺陷修复
docs:     文档
test:     测试
chore:    构建/依赖/杂项
refactor: 重构
```

## 许可证

贡献内容默认以 MIT 许可发布。
