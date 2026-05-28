/**
 * PPT生成器主入口
 * 导出所有模块和功能
 */

// 基础模块
export { TemplateGenerator, Theme, SlideSize, TextBoxOptions, ShapeOptions, ImageOptions } from './base';

// 工具函数
export {
  hexToRgb,
  rgbToHex,
  blendColors,
  lightenColor,
  darkenColor,
  createCirclePositions,
  createGridPositions,
  createHexagonPositions,
  distributeHorizontal,
  distributeVertical,
  formatNumberedTitle,
  truncateText,
  generateId,
  estimateTextLines,
  safeDivide,
  clamp,
} from './utils';

// 主题
export {
  blueTechnology,
  purpleGradient,
  darkGold,
  minimalistBW,
  oceanBlue,
  greenNature,
  redBusiness,
  allThemes,
  getThemeByName,
} from './themes';

// 封面生成器
export {
  GeometricRotation,
  CircleRing,
  TrainMist,
  DiamondReveal,
  MinimalistGradient,
  SplitScreen,
  HollowMask,
  LayeredDepth,
  CoverData,
} from './generators/cover';

// 目录生成器
export {
  DiamondAnimated,
  CircularRing,
  Hexagon,
  Sidebar,
  CardGrid,
  TimelineStyle,
  DirectoryData,
  DirectoryItem,
} from './generators/directory';

// 内容生成器
export {
  TextImageLayout,
  ThreeColumn,
  FourGrid,
  FullImageOverlay,
  Comparison,
  ContentData,
  ContentBlock,
} from './generators/content';

// 时间线生成器
export {
  DualWave,
  Horizontal,
  Vertical,
  Spiral,
  TimelineData,
  TimelineItem,
} from './generators/timeline';

// 图表生成器
export {
  BarChart,
  PieChart,
  LineChart,
  AnimatedChart,
  ChartPageData,
  ChartDataItem,
} from './generators/chart';

// 团队生成器
export {
  PersonCard,
  TeamGrid,
  OrgChart,
  TeamData,
  TeamMember,
} from './generators/team';

// 结束页生成器
export {
  ThankYou,
  QRCode,
  Contact,
  EndingData,
} from './generators/ending';

// 完整演示文稿
export {
  BusinessPlan,
  CareerPlanning,
  ProductLaunch,
  AnnualReport,
  EducationCourse,
  TechnologyTheme,
  DeckConfig,
} from './generators/complete';
