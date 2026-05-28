"""封面生成器模块

提供8种风格的PPT封面生成器：

动画封面：
- GeometricRotationCover: 几何旋转封面
- CircleRingCover: 圆环转场封面
- TrainMistCover: 列车穿雾封面
- DiamondRevealCover: 钻石揭示封面

静态封面：
- MinimalistGradientCover: 极简渐变封面
- SplitScreenCover: 分屏封面
- HollowMaskCover: 镂空遮罩封面
- LayeredDepthCover: 层次深度封面
"""

from python.generators_cover.geometric_rotation import GeometricRotationCover
from python.generators_cover.circle_ring import CircleRingCover
from python.generators_cover.train_mist import TrainMistCover
from python.generators_cover.diamond_reveal import DiamondRevealCover
from python.generators_cover.minimalist_gradient import MinimalistGradientCover
from python.generators_cover.split_screen import SplitScreenCover
from python.generators_cover.hollow_mask import HollowMaskCover
from python.generators_cover.layered_depth import LayeredDepthCover

__all__ = [
    # 动画封面
    "GeometricRotationCover",
    "CircleRingCover",
    "TrainMistCover",
    "DiamondRevealCover",
    # 静态封面
    "MinimalistGradientCover",
    "SplitScreenCover",
    "HollowMaskCover",
    "LayeredDepthCover",
]
