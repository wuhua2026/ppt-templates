"""极简黑白主题"""
from pptx.dml.color import RGBColor
from themes import BaseTheme


class MinimalistBWTheme(BaseTheme):
    name = "极简黑白"
    primary = RGBColor(0, 0, 0)
    secondary = RGBColor(51, 51, 51)
    accent = RGBColor(200, 200, 200)
    background = RGBColor(255, 255, 255)
    text = RGBColor(0, 0, 0)
    muted = RGBColor(128, 128, 128)
    dark_bg = RGBColor(0, 0, 0)
