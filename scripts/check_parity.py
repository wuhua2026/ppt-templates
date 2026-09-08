#!/usr/bin/env python3
"""校验 Python 与 TypeScript 两侧生成器的数量是否对等。

双语言实现是本项目的主要维护成本来源，一旦某一侧新增/删除生成器而另一侧没有同步，
长期必然出现功能漂移。本脚本在 CI 中做一次结构性比对，尽早暴露不对等。

用法：
    python scripts/check_parity.py
退出码 0 表示两侧一致，1 表示存在差异。
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


def main() -> int:
    mismatched = False
    total_py = total_ts = 0

    print(f"{'生成器族':<12}{'Python':>8}{'TS':>8}{'状态':>10}")
    print("-" * 40)

    for family in FAMILIES:
        py = python_classes(family)
        ts = typescript_classes(family)
        total_py += len(py)
        total_ts += len(ts)

        if len(py) == len(ts):
            status = "OK"
        else:
            status = "不一致"
            mismatched = True

        print(f"{family:<12}{len(py):>8}{len(ts):>8}{status:>10}")
        if status != "OK":
            print(f"    Python: {', '.join(py) or '（无）'}")
            print(f"    TS    : {', '.join(ts) or '（无）'}")

    print("-" * 40)
    print(f"{'合计':<12}{total_py:>8}{total_ts:>8}")

    if mismatched:
        print("\n[FAIL] 双端生成器数量不一致，请补齐缺失的一侧。", file=sys.stderr)
        return 1

    print(f"\n[OK] 双端一致，共 {total_py} 个生成器。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
