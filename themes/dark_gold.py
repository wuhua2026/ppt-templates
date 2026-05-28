"""暗金奢华主题"""
from pptx.dml.color import RGBColor
from themes import BaseTheme


class DarkGoldTheme(BaseTheme):
    name = "暗金奢华"
    primary = RGBColor(201, 169, 110)
    secondary = RGBColor(180, 140, 80)
    accent = RGBColor(255, 215, 0)
    background = RGBColor(26, 26, 46)
    text = RGBColor(240, 240, 240)
    muted = RGBColor(160, 160, 160)
    dark_bg = RGBColor(15, 15, 30)
