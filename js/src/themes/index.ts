/**
 * 主题模块
 * 预定义7种PPT主题配色方案
 *
 * 色值与 Python 侧 themes/*.py 逐项对齐（由 scripts/check_parity.py 校验）。
 * 修改任一侧时必须同步另一侧，否则 CI 会失败。
 */

import { Theme } from '../base';

/** 蓝色科技主题 - 适合科技、互联网行业 */
export const blueTechnology: Theme = {
  name: '蓝色科技',
  primary: '0066CC',
  secondary: '00CC99',
  accent: '00B4D8',
  background: 'FFFFFF',
  text: '212121',
  muted: '9E9E9E',
  darkBg: '0A1931',
};

/** 紫色渐变主题 - 适合创意、设计类 */
export const purpleGradient: Theme = {
  name: '紫色渐变',
  primary: '7B2FBE',
  secondary: 'E040FB',
  accent: 'A882FF',
  background: 'FFFFFF',
  text: '212121',
  muted: '9E9E9E',
  darkBg: '1E0F32',
};

/** 暗金奢华主题 - 适合高端、商务；唯一使用深色背景的主题 */
export const darkGold: Theme = {
  name: '暗金奢华',
  primary: 'C9A96E',
  secondary: 'B48C50',
  accent: 'FFD700',
  background: '1A1A2E',
  text: 'F0F0F0',
  muted: 'A0A0A0',
  darkBg: '0F0F1E',
};

/** 极简黑白主题 - 适合通用、学术 */
export const minimalistBW: Theme = {
  name: '极简黑白',
  primary: '000000',
  secondary: '333333',
  accent: 'C8C8C8',
  background: 'FFFFFF',
  text: '000000',
  muted: '808080',
  darkBg: '000000',
};

/** 海洋蓝主题 - 适合教育、培训 */
export const oceanBlue: Theme = {
  name: '海洋蓝',
  primary: '0077B6',
  secondary: '00B4D8',
  accent: '90E0EF',
  background: 'FFFFFF',
  text: '212121',
  muted: '9E9E9E',
  darkBg: '081E34',
};

/** 自然绿主题 - 适合环保、健康 */
export const greenNature: Theme = {
  name: '自然绿',
  primary: '2D6A4F',
  secondary: '52B788',
  accent: 'A8DAB5',
  background: 'FFFFFF',
  text: '212121',
  muted: '9E9E9E',
  darkBg: '0F281E',
};

/** 红色商务主题 - 适合商务、营销 */
export const redBusiness: Theme = {
  name: '红色商务',
  primary: 'C0392B',
  secondary: 'E74C3C',
  accent: 'FF6B6B',
  background: 'FFFFFF',
  text: '212121',
  muted: '9E9E9E',
  darkBg: '320A0A',
};

/** 所有主题集合 */
export const allThemes: Theme[] = [
  blueTechnology,
  purpleGradient,
  darkGold,
  minimalistBW,
  oceanBlue,
  greenNature,
  redBusiness,
];

/**
 * 根据名称获取主题
 * @param name - 主题名称
 * @returns 对应的主题对象，未找到则返回蓝色科技主题
 */
export function getThemeByName(name: string): Theme {
  const theme = allThemes.find(t => t.name === name);
  return theme || blueTechnology;
}
