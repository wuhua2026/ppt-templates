"""红色商务主题"""
from pptx.dml.color import RGBColor
from themes import BaseTheme


class RedBusinessTheme(BaseTheme):
    name = "红色商务"
    primary = RGBColor(192, 57, 43)
    secondary = RGBColor(231, 76, 60)
    accent = RGBColor(255, 107, 107)
    background = RGBColor(255, 255, 255)
    text = RGBColor(33, 33, 33)
    muted = RGBColor(158, 158, 158)
    dark_bg = RGBColor(50, 10, 10)
