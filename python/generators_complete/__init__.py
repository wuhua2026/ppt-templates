"""完整演示文稿组装器

将各类页面生成器组合成完整的15-25页演示文稿。
每个组装器负责一种特定类型的演示文稿，包含封面、目录、内容页和结束页。
"""

from python.generators_complete.business_plan import BusinessPlanAssembler
from python.generators_complete.career_planning import CareerPlanningAssembler
from python.generators_complete.product_launch import ProductLaunchAssembler
from python.generators_complete.annual_report import AnnualReportAssembler
from python.generators_complete.education_course import EducationCourseAssembler
from python.generators_complete.technology_theme import TechnologyThemeAssembler

__all__ = [
    "BusinessPlanAssembler",
    "CareerPlanningAssembler",
    "ProductLaunchAssembler",
    "AnnualReportAssembler",
    "EducationCourseAssembler",
    "TechnologyThemeAssembler",
]
