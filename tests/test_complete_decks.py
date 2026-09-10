"""完整演示文稿（templates/complete/）契约测试

6 套完整文稿由 scripts/generate_decks.py 生成，页数在 generate() 中固定编排，
因此页数是确定值。这里的断言与 README「完整演示文稿」表格中的数字保持同步：
修改任一套文稿的页面编排时，必须同步更新 README 与本文件。
"""

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from python.generators_complete import (
    AnnualReportAssembler,
    BusinessPlanAssembler,
    CareerPlanningAssembler,
    EducationCourseAssembler,
    ProductLaunchAssembler,
    TechnologyThemeAssembler,
)

# 文件名 -> (组装器, 确定页数)
EXPECTED_DECKS = {
    "business_plan": (BusinessPlanAssembler, 18),
    "career_planning": (CareerPlanningAssembler, 16),
    "product_launch": (ProductLaunchAssembler, 20),
    "annual_report": (AnnualReportAssembler, 22),
    "education_course": (EducationCourseAssembler, 18),
    "technology_theme": (TechnologyThemeAssembler, 16),
}


@pytest.mark.parametrize("name", sorted(EXPECTED_DECKS), ids=str)
def test_deck_page_count(name):
    """页数为确定值：generate() 的页面序列固定，不含动态分支。"""
    cls, expected_pages = EXPECTED_DECKS[name]
    deck = cls()
    deck.set_title("契约测试").set_subtitle("Contract Test")
    deck.generate()
    assert len(deck.prs.slides) == expected_pages, (
        f"{name} 页数变为 {len(deck.prs.slides)}（预期 {expected_pages}）。"
        "若为有意调整，请同步更新 README 表格与本文件。"
    )


@pytest.mark.parametrize("name", sorted(EXPECTED_DECKS), ids=str)
def test_deck_default_theme_does_not_crash(name):
    """不传 theme 时使用内置默认配色，不能抛 AttributeError（历史缺陷回归防护）。

    DEFAULT_THEME 曾是 dict 而 _get_color 按对象属性访问，导致 README 示例
    `BusinessPlanAssembler()` 照抄即崩。此测试确保该缺陷不再复发。
    """
    cls, _ = EXPECTED_DECKS[name]
    deck = cls()
    deck.set_title("无主题测试").set_subtitle("No Theme")
    deck.generate()  # 不应抛出异常
    assert len(deck.prs.slides) > 0
