## 变更类型

- [ ] 缺陷修复（fix）
- [ ] 新功能（feat）
- [ ] 文档（docs）
- [ ] 测试（test）
- [ ] 重构（refactor）
- [ ] 构建 / 依赖 / 杂项（chore）

## 说明

<!-- 这次改动做了什么，为什么需要 -->

## 关联 Issue

<!-- 例如 Closes #1 -->

## 自检清单

在提交前请确认：

- [ ] `pytest` 全部通过
- [ ] `cd js && npx tsc --noEmit` 无类型错误
- [ ] `python scripts/check_parity.py` 报告双端一致
- [ ] 若新增/删除生成器，**Python 与 TypeScript 两侧已同步**
- [ ] 若新增主题，已在 `themes/__init__.py` 的 `ALL_THEMES` 中注册
- [ ] 未提交 `output_*.pptx` 等生成产物
- [ ] 已更新 README / CHANGELOG（如适用）

## 影响面

- [ ] 不破坏既有 API
- [ ] 破坏既有 API（请在下方说明迁移方式）

## 补充

- 截图 / 生成效果对比：
- 需要 reviewers 特别关注的地方：
