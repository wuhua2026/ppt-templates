"""自然绿主题"""
from pptx.dml.color import RGBColor
from themes import BaseTheme


class GreenNatureTheme(BaseTheme):
    name = "自然绿"
    primary = RGBColor(45, 106, 79)
    secondary = RGBColor(82, 183, 136)
    accent = RGBColor(168, 218, 181)
    background = RGBColor(255, 255, 255)
    text = RGBColor(33, 33, 33)
    muted = RGBColor(158, 158, 158)
    dark_bg = RGBColor(15, 40, 30)
