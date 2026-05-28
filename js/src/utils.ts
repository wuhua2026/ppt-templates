/**
 * 工具函数模块
 * 提供颜色转换、位置计算、形状辅助等通用功能
 */

/** RGB颜色对象 */
export interface RGBColor {
  r: number;
  g: number;
  b: number;
}

/**
 * 将十六进制颜色转换为RGB对象
 * @param hex - 十六进制颜色值（如 "FF5733" 或 "#FF5733"）
 * @returns RGB颜色对象
 */
export function hexToRgb(hex: string): RGBColor {
  const cleanHex = hex.replace('#', '');
  return {
    r: parseInt(cleanHex.substring(0, 2), 16),
    g: parseInt(cleanHex.substring(2, 4), 16),
    b: parseInt(cleanHex.substring(4, 6), 16),
  };
}

/**
 * 将RGB对象转换为十六进制颜色字符串
 * @param rgb - RGB颜色对象
 * @returns 十六进制颜色字符串（不含#）
 */
export function rgbToHex(rgb: RGBColor): string {
  const toHex = (n: number) => Math.max(0, Math.min(255, Math.round(n))).toString(16).padStart(2, '0');
  return `${toHex(rgb.r)}${toHex(rgb.g)}${toHex(rgb.b)}`;
}

/**
 * 颜色混合（线性插值）
 * @param color1 - 起始颜色
 * @param color2 - 目标颜色
 * @param factor - 混合因子（0~1）
 * @returns 混合后的十六进制颜色
 */
export function blendColors(color1: string, color2: string, factor: number): string {
  const rgb1 = hexToRgb(color1);
  const rgb2 = hexToRgb(color2);
  return rgbToHex({
    r: rgb1.r + (rgb2.r - rgb1.r) * factor,
    g: rgb1.g + (rgb2.g - rgb1.g) * factor,
    b: rgb1.b + (rgb2.b - rgb1.b) * factor,
  });
}

/**
 * 生成颜色的浅色变体
 * @param hex - 原始颜色
 * @param factor - 变浅程度（0~1，值越大越浅）
 * @returns 浅色变体
 */
export function lightenColor(hex: string, factor: number = 0.3): string {
  const rgb = hexToRgb(hex);
  return rgbToHex({
    r: rgb.r + (255 - rgb.r) * factor,
    g: rgb.g + (255 - rgb.g) * factor,
    b: rgb.b + (255 - rgb.b) * factor,
  });
}

/**
 * 生成颜色的深色变体
 * @param hex - 原始颜色
 * @param factor - 变深程度（0~1，值越大越深）
 * @returns 深色变体
 */
export function darkenColor(hex: string, factor: number = 0.3): string {
  const rgb = hexToRgb(hex);
  return rgbToHex({
    r: rgb.r * (1 - factor),
    g: rgb.g * (1 - factor),
    b: rgb.b * (1 - factor),
  });
}

/** 位置坐标 */
export interface Position {
  x: number;
  y: number;
}

/**
 * 创建圆形排列的位置坐标
 * @param centerX - 圆心X坐标
 * @param centerY - 圆心Y坐标
 * @param radius - 圆的半径
 * @param count - 元素数量
 * @param startAngle - 起始角度（度，默认-90，即从顶部开始）
 * @returns 位置坐标数组
 */
export function createCirclePositions(
  centerX: number,
  centerY: number,
  radius: number,
  count: number,
  startAngle: number = -90
): Position[] {
  const positions: Position[] = [];
  const angleStep = (2 * Math.PI) / count;
  for (let i = 0; i < count; i++) {
    const angle = (startAngle * Math.PI) / 180 + i * angleStep;
    positions.push({
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
    });
  }
  return positions;
}

/**
 * 创建网格排列的位置坐标
 * @param startX - 起始X坐标
 * @param startY - 起始Y坐标
 * @param itemWidth - 每个元素宽度
 * @param itemHeight - 每个元素高度
 * @param cols - 列数
 * @param rows - 行数
 * @param gapX - 水平间距
 * @param gapY - 垂直间距
 * @returns 位置坐标数组
 */
export function createGridPositions(
  startX: number,
  startY: number,
  itemWidth: number,
  itemHeight: number,
  cols: number,
  rows: number,
  gapX: number = 0.2,
  gapY: number = 0.2
): Position[] {
  const positions: Position[] = [];
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      positions.push({
        x: startX + col * (itemWidth + gapX),
        y: startY + row * (itemHeight + gapY),
      });
    }
  }
  return positions;
}

/**
 * 创建六边形网格排列的位置坐标
 * @param startX - 起始X坐标
 * @param startY - 起始Y坐标
 * @param size - 六边形尺寸
 * @param cols - 列数
 * @param rows - 行数
 * @returns 位置坐标数组
 */
export function createHexagonPositions(
  startX: number,
  startY: number,
  size: number,
  cols: number,
  rows: number
): Position[] {
  const positions: Position[] = [];
  const hexWidth = size * 2;
  const hexHeight = size * Math.sqrt(3);

  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const offsetX = row % 2 === 1 ? size : 0;
      positions.push({
        x: startX + col * (hexWidth * 0.75) + offsetX,
        y: startY + row * (hexHeight * 0.5),
      });
    }
  }
  return positions;
}

/**
 * 生成均匀分布的水平位置数组
 * @param startX - 起始X
 * @param endX - 结束X
 * @param count - 数量
 * @returns X坐标数组
 */
export function distributeHorizontal(startX: number, endX: number, count: number): number[] {
  if (count <= 1) return [(startX + endX) / 2];
  const step = (endX - startX) / (count - 1);
  return Array.from({ length: count }, (_, i) => startX + i * step);
}

/**
 * 生成均匀分布的垂直位置数组
 * @param startY - 起始Y
 * @param endY - 结束Y
 * @param count - 数量
 * @returns Y坐标数组
 */
export function distributeVertical(startY: number, endY: number, count: number): number[] {
  if (count <= 1) return [(startY + endY) / 2];
  const step = (endY - startY) / (count - 1);
  return Array.from({ length: count }, (_, i) => startY + i * step);
}

/**
 * 文本格式化辅助 - 创建带序号的标题文本
 * @param index - 序号
 * @param title - 标题文本
 * @param format - 格式模板，{index} 为序号占位符，{title} 为标题占位符
 * @returns 格式化后的文本
 */
export function formatNumberedTitle(index: number, title: string, format?: string): string {
  const template = format || '{index}. {title}';
  return template.replace('{index}', String(index)).replace('{title}', title);
}

/**
 * 截断文本到指定长度
 * @param text - 原始文本
 * @param maxLength - 最大长度
 * @param suffix - 截断后缀
 * @returns 截断后的文本
 */
export function truncateText(text: string, maxLength: number, suffix: string = '...'): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - suffix.length) + suffix;
}

/**
 * 生成随机ID
 * @param length - ID长度
 * @returns 随机字符串
 */
export function generateId(length: number = 8): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * 计算文本行数（根据宽度和字体大小估算）
 * @param text - 文本内容
 * @param width - 可用宽度（英寸）
 * @param fontSize - 字体大小（磅）
 * @returns 估算行数
 */
export function estimateTextLines(text: string, width: number, fontSize: number): number {
  const avgCharWidth = fontSize * 0.012; // 近似字符宽度
  const charsPerLine = Math.floor(width / avgCharWidth);
  return Math.ceil(text.length / charsPerLine);
}

/**
 * 安全除法，避免除以零
 * @param a - 被除数
 * @param b - 除数
 * @param defaultVal - 除数为零时的默认值
 * @returns 除法结果
 */
export function safeDivide(a: number, b: number, defaultVal: number = 0): number {
  return b === 0 ? defaultVal : a / b;
}

/**
 * 将数值限制在指定范围内
 * @param value - 输入值
 * @param min - 最小值
 * @param max - 最大值
 * @returns 限制后的值
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}
