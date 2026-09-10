#!/usr/bin/env python3
"""校验 Python 与 TypeScript 双端的契约一致性。

双语言实现是本项目的主要维护成本来源。本脚本在 CI 中做三层校验：

1. 数量对等：每族生成器在两侧的数量一致（原有逻辑）
2. 类名映射：每个 Python 类都能按规则或例外表映射到 TS 类；映射不到即失败
3. 主题色一致：7 套主题的 name 与 7 个色值逐项比对，任一不一致即失败

已知且刻意保留的差异（只标注、不判失败）：
- 画布比例：Python 基类 10x7.5 英寸（4:3），TS 基类 13.33x7.5 英寸（16:9）。
  Python 侧 230+ 个模板坐标按 4:3 设计，统一画布需要重新排版（见 README FAQ）。

用法：
    python scripts/check_parity.py
退出码 0 表示一致，1 表示存在差异。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FAMILIES = [
    "chart",
    "complete",
    "content",
    "cover",
    "directory",
    "ending",
    "team",
    "timeline",
]

PY_CLASS_RE = re.compile(r"^class\s+(\w+)", re.MULTILINE)
TS_CLASS_RE = re.compile(r"^export\s+class\s+(\w+)", re.MULTILINE)

# 规则无法覆盖的双端类名差异（Python 名 -> TS 名）
CLASS_NAME_EXCEPTIONS = {
    "AnimatedBarChart": "AnimatedChart",
}

# 类名映射规则：循环剥离后缀直到不再变化（XxxGenerator -> Xxx、XxxCover -> Xxx、
# XxxTimeline -> Xxx、ContactPageGenerator -> ContactPage -> Contact），同名直通
SUFFIXES = ("Generator", "Assembler", "Cover", "Timeline", "Page")

# 主题键在两侧的对应关系（Python 属性名 -> TS 对象键名）
THEME_KEYS = ["primary", "secondary", "accent", "background", "text", "muted", "dark_bg"]
TS_KEY_OF = {k: ("darkBg" if k == "dark_bg" else k) for k in THEME_KEYS}

# Python 主题文件名 -> TS 导出变量名
THEME_FILES = {
    "blue_technology": "blueTechnology",
    "purple_gradient": "purpleGradient",
    "dark_gold": "darkGold",
    "minimalist_bw": "minimalistBW",
    "ocean_blue": "oceanBlue",
    "green_nature": "greenNature",
    "red_business": "redBusiness",
}

PY_THEME_RE = re.compile(r"^\s*(\w+)\s*=\s*RGBColor\((\d+),\s*(\d+),\s*(\d+)\)", re.MULTILINE)
PY_NAME_RE = re.compile(r'^\s*name\s*=\s*"([^"]+)"', re.MULTILINE)
TS_THEME_RE = re.compile(r"(\w+):\s*'([0-9A-Fa-f]{6})'", re.MULTILINE)
TS_NAME_RE = re.compile(r"name:\s*'([^']+)'", re.MULTILINE)


def python_classes(family: str) -> list[str]:
    pkg = ROOT / "python" / f"generators_{family}"
    if not pkg.is_dir():
        return []
    names: list[str] = []
    for path in sorted(pkg.glob("*.py")):
        if path.name == "__init__.py":
            continue
        names.extend(PY_CLASS_RE.findall(path.read_text(encoding="utf-8")))
    return sorted(names)


def typescript_classes(family: str) -> list[str]:
    path = ROOT / "js" / "src" / "generators" / f"{family}.ts"
    if not path.is_file():
        return []
    return sorted(TS_CLASS_RE.findall(path.read_text(encoding="utf-8")))


def py_to_ts_class(name: str) -> str:
    """按规则把 Python 类名映射到 TS 类名，例外走显式表。"""
    if name in CLASS_NAME_EXCEPTIONS:
        return CLASS_NAME_EXCEPTIONS[name]
    changed = True
    while changed:
        changed = False
        for suffix in SUFFIXES:
            if name.endswith(suffix):
                name = name[: -len(suffix)]
                changed = True
    return name


def parse_python_themes() -> dict[str, dict]:
    """解析 themes/*.py 的 name 与 RGBColor 色值为 hex。"""
    themes = {}
    for stem, _ in THEME_FILES.items():
        path = ROOT / "themes" / f"{stem}.py"
        src = path.read_text(encoding="utf-8")
        entry: dict[str, str] = {}
        m = PY_NAME_RE.search(src)
        if m:
            entry["name"] = m.group(1)
        for key, r, g, b in PY_THEME_RE.findall(src):
            if key in THEME_KEYS:
                entry[key] = f"{int(r):02X}{int(g):02X}{int(b):02X}"
        themes[stem] = entry
    return themes


def parse_typescript_themes() -> dict[str, dict]:
    """解析 js/src/themes/index.ts 的 7 个主题对象。"""
    src = (ROOT / "js" / "src" / "themes" / "index.ts").read_text(encoding="utf-8")
    themes = {}
    for stem, var in THEME_FILES.items():
        m = re.search(rf"export const {var}: Theme = \{{(.*?)\}};", src, re.DOTALL)
        if not m:
            themes[stem] = {}
            continue
        body = m.group(1)
        entry: dict[str, str] = {}
        mn = TS_NAME_RE.search(body)
        if mn:
            entry["name"] = mn.group(1)
        for key, hexv in TS_THEME_RE.findall(body):
            py_key = [pk for pk, tk in TS_KEY_OF.items() if tk == key]
            if py_key:
                entry[py_key[0]] = hexv.upper()
        themes[stem] = entry
    return themes


def main() -> int:
    failed = False
    total_py = total_ts = 0

    print(f"{'生成器族':<12}{'Python':>8}{'TS':>8}{'状态':>10}")
    print("-" * 40)

    # ---- 1+2. 数量与类名映射 ----
    for family in FAMILIES:
        py = python_classes(family)
        ts = typescript_classes(family)
        total_py += len(py)
        total_ts += len(ts)

        ts_set = set(ts)
        unmapped = [name for name in py if py_to_ts_class(name) not in ts_set]
        mapped_ts = {py_to_ts_class(p) for p in py}
        extra = [name for name in ts if name not in mapped_ts]

        if len(py) == len(ts) and not unmapped and not extra:
            status = "OK"
        else:
            status = "不一致"
            failed = True

        print(f"{family:<12}{len(py):>8}{len(ts):>8}{status:>10}")
        if unmapped:
            print(f"    Python 侧无法映射到 TS: {', '.join(unmapped)}")
        if extra:
            print(f"    TS 侧缺少 Python 对应: {', '.join(extra)}")

    print("-" * 40)
    print(f"{'合计':<12}{total_py:>8}{total_ts:>8}")

    # ---- 3. 主题一致性 ----
    py_themes = parse_python_themes()
    ts_themes = parse_typescript_themes()
    print("\n主题一致性（Python themes/*.py vs js/src/themes/index.ts）")
    for stem in THEME_FILES:
        p, t = py_themes.get(stem, {}), ts_themes.get(stem, {})
        diffs = [k for k in ["name"] + THEME_KEYS if p.get(k) != t.get(k)]
        if diffs:
            theme_bad = True
            failed = True
            print(f"  [FAIL] {stem}: 不一致项 {', '.join(diffs)}")
            for k in diffs:
                print(f"         {k}: Python={p.get(k)}  TS={t.get(k)}")
        else:
            print(f"  [OK]   {stem}")

    # ---- 已知差异标注（不判失败）----
    print("\n已知差异（仅标注）")
    print("  [WARN] 画布比例：Python 10x7.5 英寸(4:3) vs TS 13.33x7.5 英寸(16:9)。")
    print("         Python 侧模板坐标按 4:3 设计，统一画布需重新排版，暂不合并（见 README FAQ）。")

    if failed:
        print("\n[FAIL] 双端契约存在不一致，请补齐缺失的一侧。", file=sys.stderr)
        return 1

    print(f"\n[OK] 双端契约一致：{total_py} 个生成器、7 套主题逐项对齐。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
