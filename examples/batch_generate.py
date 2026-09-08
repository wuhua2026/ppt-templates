"""
批量生成示例 - PPT模板资源库

本示例演示如何批量生成所有模板。

实现说明：早期版本这里维护了一份与 scripts/generate_all.py 重复的生成逻辑，
两份逻辑并行维护容易出现漂移。现改为直接委托给主构建脚本，
本文件只保留「示例」的入口语义，生成逻辑统一由 scripts/generate_all.py 承载。

运行方式：
    python examples/batch_generate.py              # 生成全部模板到 templates/
    python examples/batch_generate.py --theme blue  # 只生成指定主题
    python examples/batch_generate.py --type cover  # 只生成指定类型
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN_SCRIPT = ROOT / "scripts" / "generate_all.py"


def main():
    if not MAIN_SCRIPT.is_file():
        print(f"[错误] 未找到主构建脚本：{MAIN_SCRIPT}")
        return 1
    # 透传所有命令行参数，行为与直接调用主脚本一致
    return subprocess.call([sys.executable, str(MAIN_SCRIPT)] + sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
