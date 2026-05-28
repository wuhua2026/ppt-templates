/**
 * 主题模块
 * 预定义7种PPT主题配色方案
 */

import { Theme } from '../base';

/** 蓝色科技主题 - 适合科技、互联网行业 */
export const blueTechnology: Theme = {
  name: '蓝色科技',
  primary: '2B579A',
  secondary: '4472C4',
  accent: '00B4D8',
  background: 'F0F4F8',
  text: '1A1A2E',
  muted: '7B8794',
  darkBg: '0D1B2A',
};

/** 紫色渐变主题 - 适合创意、设计类 */
export const purpleGradient: Theme = {
  name: '紫色渐变',
  primary: '6C3483',
  secondary: '9B59B6',
  accent: 'E74C3C',
  background: 'F5F0FF',
  text: '2C003E',
  muted: '8E7BA5',
  darkBg: '1A0025',
};

/** 暗金主题 - 适合高端、奢华品牌 */
export const darkGold: Theme = {
  name: '暗金',
  primary: 'C9A96E',
  secondary: 'D4AF37',
  accent: 'F39C12',
  background: '1C1C1C',
  text: 'F5F5DC',
  muted: 'A0936E',
  darkBg: '0D0D0D',
};

/** 极简黑白主题 - 适合正式商务场合 */
export const minimalistBW: Theme = {
  name: '极简黑白',
  primary: '333333',
  secondary: '666666',
  accent: 'E74C3C',
  background: 'FFFFFF',
  text: '1A1A1A',
  muted: 'AAAAAA',
  darkBg: '000000',
};

/** 海洋蓝主题 - 适合环保、海洋相关 */
export const oceanBlue: Theme = {
  name: '海洋蓝',
  primary: '0077B6',
  secondary: '0096C7',
  accent: 'FFB703',
  background: 'F0F8FF',
  text: '023047',
  muted: '5E81AC',
  darkBg: '001D3D',
};

/** 绿色自然主题 - 适合农业、环保、健康 */
export const greenNature: Theme = {
  name: '绿色自然',
  primary: '2D6A4F',
  secondary: '40916C',
  accent: 'D4A373',
  background: 'F0FFF4',
  text: '1B4332',
  muted: '74A57F',
  darkBg: '081C15',
};

/** 红色商务主题 - 适合金融、企业宣传 */
export const redBusiness: Theme = {
  name: '红色商务',
  primary: 'C0392B',
  secondary: 'E74C3C',
  accent: 'F39C12',
  background: 'FFF5F5',
  text: '2C0000',
  muted: 'A04040',
  darkBg: '1A0000',
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
