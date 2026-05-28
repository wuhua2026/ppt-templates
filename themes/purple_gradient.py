"""紫色渐变主题"""
from pptx.dml.color import RGBColor
from themes import BaseTheme


class PurpleGradientTheme(BaseTheme):
    name = "紫色渐变"
    primary = RGBColor(123, 47, 190)
    secondary = RGBColor(224, 64, 251)
    accent = RGBColor(168, 130, 255)
    background = RGBColor(255, 255, 255)
    text = RGBColor(33, 33, 33)
    muted = RGBColor(158, 158, 158)
    dark_bg = RGBColor(30, 15, 50)
