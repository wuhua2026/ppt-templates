"""PPT配色主题系统"""

from pptx.dml.color import RGBColor


class BaseTheme:
    """主题基类"""
    name = "Base"
    primary = RGBColor(0, 102, 204)
    secondary = RGBColor(0, 204, 153)
    accent = RGBColor(255, 193, 7)
    background = RGBColor(255, 255, 255)
    text = RGBColor(33, 33, 33)
    muted = RGBColor(158, 158, 158)
    dark_bg = RGBColor(26, 26, 46)

    title_font = "Microsoft YaHei"
    body_font = "Microsoft YaHei"
    en_font = "DIN Alternate"

    def get_gradient(self, variant="primary"):
        if variant == "primary":
            return [self.primary, self.secondary]
        elif variant == "accent":
            return [self.primary, self.accent]
        elif variant == "dark":
            return [self.dark_bg, self.primary]
        return [self.primary, self.secondary]


from themes.blue_technology import BlueTechnologyTheme
from themes.purple_gradient import PurpleGradientTheme
from themes.dark_gold import DarkGoldTheme
from themes.minimalist_bw import MinimalistBWTheme
from themes.ocean_blue import OceanBlueTheme
from themes.green_nature import GreenNatureTheme
from themes.red_business import RedBusinessTheme

ALL_THEMES = {
    "blue_technology": BlueTechnologyTheme,
    "purple_gradient": PurpleGradientTheme,
    "dark_gold": DarkGoldTheme,
    "minimalist_bw": MinimalistBWTheme,
    "ocean_blue": OceanBlueTheme,
    "green_nature": GreenNatureTheme,
    "red_business": RedBusinessTheme,
}
