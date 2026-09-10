#!/usr/bin/env python3
"""生成 templates/complete/ 下的 6 套完整演示文稿。

generate_all.py 只负责单页模板（32 种 × 7 主题 = 224 个），
完整演示文稿由本脚本单独生成：每套一份，不按主题展开，因此 224 + 6 = 230。

这些文稿此前没有生成入口，仓库里的产物是由临时脚本写出的，无法复现。
本脚本固定了主题、标题与副标题，使 6 套文稿重新进入可复现体系。

运行方式：
    python scripts/generate_decks.py
    python scripts/generate_decks.py --output ./out
"""

import argparse
import os
import sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from themes import ALL_THEMES

from python.generators_complete import (
    AnnualReportAssembler,
    BusinessPlanAssembler,
    CareerPlanningAssembler,
    EducationCourseAssembler,
    ProductLaunchAssembler,
    TechnologyThemeAssembler,
)

# （输出文件名, 组装器, 主标题, 主题键）
#
# 主题与标题是从仓库既有产物反推出来的：对每套文稿遍历 7 套主题做语义签名比对，
# 命中组合即为其原始生成参数。因此本脚本重跑可 1:1 复现 templates/complete/ 下的文件。
DECKS = [
    ("annual_report", AnnualReportAssembler, "Annual Report Demo", "red_business"),
    ("business_plan", BusinessPlanAssembler, "Business Plan Demo", "blue_technology"),
    ("career_planning", CareerPlanningAssembler, "Career Planning Demo", "purple_gradient"),
    ("education_course", EducationCourseAssembler, "Education Course Demo", "green_nature"),
    ("product_launch", ProductLaunchAssembler, "Product Launch Demo", "ocean_blue"),
    ("technology_theme", TechnologyThemeAssembler, "Technology Theme Demo", "dark_gold"),
]

# 6 套文稿共用同一副标题
DEFAULT_SUBTITLE = "PPT Template Library"


def build(output_dir: str) -> int:
    os.makedirs(output_dir, exist_ok=True)

    success = 0
    for name, assembler_cls, title, theme_key in DECKS:
        start = time.time()
        filepath = os.path.join(output_dir, f"{name}.pptx")
        try:
            deck = assembler_cls(theme=ALL_THEMES[theme_key]())
            deck.set_title(title)
            deck.set_subtitle(DEFAULT_SUBTITLE)
            deck.generate()
            deck.save(filepath)
            success += 1
            print(f"  [OK] {title:<26} {os.path.basename(filepath):<28} {time.time() - start:.2f}s")
        except Exception as exc:  # 单套失败不应中断其余文稿
            print(f"  [FAIL] {title:<26} 错误: {exc}")

    print(f"\n  完成 {success}/{len(DECKS)} 套，输出目录: {output_dir}")
    return 0 if success == len(DECKS) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 6 套完整演示文稿")
    parser.add_argument(
        "--output",
        default=os.path.join(project_root, "templates", "complete"),
        help="输出目录（默认 templates/complete）",
    )
    args = parser.parse_args()

    print(f"\n  正在生成 {len(DECKS)} 套完整演示文稿...")
    return build(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
