/**
 * 结束页生成器模块
 * 包含3种不同风格的结束页模板
 * - 感谢页、二维码页、联系方式页
 */

import pptxgen from 'pptxgenjs';
import { TemplateGenerator, Theme } from '../base';

/** 结束页数据接口 */
export interface EndingData {
  /** 主标题（如"谢谢"） */
  title?: string;
  /** 副标题 */
  subtitle?: string;
  /** 公司名称 */
  company?: string;
  /** 网站 */
  website?: string;
  /** 邮箱 */
  email?: string;
  /** 电话 */
  phone?: string;
  /** 地址 */
  address?: string;
  /** 二维码描述 */
  qrDescription?: string;
  /** 社交媒体 */
  social?: { platform: string; handle: string }[];
}

/** 基础结束页类 */
abstract class BaseEnding {
  protected generator: TemplateGenerator;
  protected theme: Theme;

  constructor(generator: TemplateGenerator, theme: Theme) {
    this.generator = generator;
    this.theme = theme;
  }

  /** 生成结束页 */
  abstract generate(data: EndingData): pptxgen.Slide;
}

/**
 * 感谢页
 * 简洁大气的感谢页面
 */
export class ThankYou extends BaseEnding {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: EndingData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 深色背景
    slide.background = { fill: this.theme.darkBg };

    // 装饰圆形
    slide.addShape(this.generator.getShapes().OVAL as any, {
      x: 5.165,
      y: 1.5,
      w: 3,
      h: 3,
      line: { color: this.theme.primary, width: 1, transparency: 60 },
      fill: { color: '000000', transparency: 100 },
    });

    slide.addShape(this.generator.getShapes().OVAL as any, {
      x: 4.665,
      y: 1.0,
      w: 4,
      h: 4,
      line: { color: this.theme.secondary, width: 0.5, transparency: 70 },
      fill: { color: '000000', transparency: 100 },
    });

    // 主标题
    this.generator.addText(slide, {
      x: 1,
      y: 2.5,
      w: 11.33,
      h: 1.5,
      text: data.title || '谢谢',
      fontSize: 52,
      fontFace: '微软雅黑',
      color: 'FFFFFF',
      bold: true,
      align: 'center',
      valign: 'middle',
    });

    // 装饰线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 5.165,
      y: 4.1,
      w: 3,
      h: 0,
      line: { color: this.theme.accent, width: 2 },
    });

    // 副标题
    this.generator.addText(slide, {
      x: 1,
      y: 4.3,
      w: 11.33,
      h: 0.8,
      text: data.subtitle || 'Thank You',
      fontSize: 22,
      fontFace: 'Arial',
      color: this.theme.primary,
      align: 'center',
      valign: 'middle',
    });

    // 公司名称
    if (data.company) {
      this.generator.addText(slide, {
        x: 1,
        y: 5.5,
        w: 11.33,
        h: 0.5,
        text: data.company,
        fontSize: 14,
        fontFace: '微软雅黑',
        color: '999999',
        align: 'center',
        valign: 'middle',
      });
    }

    return slide;
  }
}

/**
 * 二维码页
 * 包含二维码占位和联系方式
 */
export class QRCode extends BaseEnding {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: EndingData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 左侧深色区域
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 0,
      y: 0,
      w: 5,
      h: 7.5,
      fill: { color: this.theme.primary },
    });

    // 左侧标题
    this.generator.addText(slide, {
      x: 0.5,
      y: 2,
      w: 4,
      h: 1,
      text: data.title || '联系我们',
      fontSize: 30,
      fontFace: '微软雅黑',
      color: 'FFFFFF',
      bold: true,
      align: 'center',
      valign: 'middle',
    });

    // 左侧装饰线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 1.5,
      y: 3.2,
      w: 2,
      h: 0,
      line: { color: 'FFFFFF', width: 2, transparency: 50 },
    });

    // 左侧公司名
    if (data.company) {
      this.generator.addText(slide, {
        x: 0.5,
        y: 3.5,
        w: 4,
        h: 0.5,
        text: data.company,
        fontSize: 14,
        fontFace: '微软雅黑',
        color: 'CCCCCC',
        align: 'center',
        valign: 'middle',
      });
    }

    // 右侧二维码占位区域
    const qrX = 6.5;
    const qrY = 1.5;
    const qrSize = 2.5;

    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: qrX,
      y: qrY,
      w: qrSize,
      h: qrSize,
      fill: { color: 'FFFFFF' },
      rectRadius: 0.1,
      line: { color: this.theme.muted, width: 1 },
    });

    // 二维码占位符
    this.generator.addText(slide, {
      x: qrX,
      y: qrY + qrSize / 2 - 0.3,
      w: qrSize,
      h: 0.6,
      text: '[二维码]',
      fontSize: 14,
      fontFace: '微软雅黑',
      color: this.theme.muted,
      align: 'center',
      valign: 'middle',
    });

    // 二维码描述
    this.generator.addText(slide, {
      x: qrX,
      y: qrY + qrSize + 0.2,
      w: qrSize,
      h: 0.4,
      text: data.qrDescription || '扫码关注',
      fontSize: 11,
      fontFace: '微软雅黑',
      color: this.theme.muted,
      align: 'center',
      valign: 'top',
    });

    // 联系信息
    const infoItems: Array<{ icon: string; text: string }> = [];
    if (data.email) infoItems.push({ icon: 'Email', text: data.email });
    if (data.phone) infoItems.push({ icon: 'Tel', text: data.phone });
    if (data.website) infoItems.push({ icon: 'Web', text: data.website });
    if (data.address) infoItems.push({ icon: 'Addr', text: data.address });

    infoItems.forEach((item, i) => {
      const y = 4.5 + i * 0.6;

      // 图标圆圈
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: qrX,
        y: y,
        w: 0.4,
        h: 0.4,
        fill: { color: this.theme.primary, transparency: 85 },
      });

      this.generator.addText(slide, {
        x: qrX,
        y: y,
        w: 0.4,
        h: 0.4,
        text: item.icon.charAt(0),
        fontSize: 10,
        fontFace: 'Arial',
        color: this.theme.primary,
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 信息文本
      this.generator.addText(slide, {
        x: qrX + 0.6,
        y: y,
        w: 4,
        h: 0.4,
        text: item.text,
        fontSize: 12,
        fontFace: '微软雅黑',
        color: this.theme.text,
        align: 'left',
        valign: 'middle',
      });
    });

    return slide;
  }
}

/**
 * 联系方式页
 * 集中展示所有联系信息
 */
export class Contact extends BaseEnding {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: EndingData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 顶部装饰条
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 0,
      y: 0,
      w: 13.33,
      h: 0.1,
      fill: { color: this.theme.primary },
    });

    // 标题
    this.generator.addText(slide, {
      x: 0.5,
      y: 0.8,
      w: 12,
      h: 1,
      text: data.title || '联系方式',
      fontSize: 32,
      fontFace: '微软雅黑',
      color: this.theme.primary,
      bold: true,
      align: 'center',
      valign: 'middle',
    });

    // 副标题
    this.generator.addText(slide, {
      x: 0.5,
      y: 1.8,
      w: 12,
      h: 0.5,
      text: data.subtitle || '期待与您的合作',
      fontSize: 16,
      fontFace: '微软雅黑',
      color: this.theme.muted,
      align: 'center',
      valign: 'middle',
    });

    // 装饰线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 5.165,
      y: 2.5,
      w: 3,
      h: 0,
      line: { color: this.theme.accent, width: 2 },
    });

    // 联系信息网格
    const infoGrid: Array<{ label: string; value: string; icon: string }> = [
      { label: '公司', value: data.company || '-', icon: 'C' },
      { label: '网站', value: data.website || '-', icon: 'W' },
      { label: '邮箱', value: data.email || '-', icon: 'E' },
      { label: '电话', value: data.phone || '-', icon: 'T' },
      { label: '地址', value: data.address || '-', icon: 'A' },
    ];

    const cols = 2;
    const cardW = 5.5;
    const cardH = 0.9;
    const startX = 1.5;
    const startY = 3.0;
    const gapX = 4.5;
    const gapY = 0.2;

    infoGrid.forEach((item, i) => {
      const col = i % cols;
      const row = Math.floor(i / cols);
      const x = startX + col * gapX;
      const y = startY + row * (cardH + gapY);

      // 背景
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x,
        y: y,
        w: cardW,
        h: cardH,
        fill: { color: 'FFFFFF' },
        rectRadius: 0.05,
        shadow: {
          type: 'outer' as any,
          color: '000000',
          blur: 4,
          offset: 1,
          angle: 135,
          opacity: 0.06,
        },
      });

      // 图标圆圈
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: x + 0.2,
        y: y + (cardH - 0.5) / 2,
        w: 0.5,
        h: 0.5,
        fill: { color: this.theme.primary },
      });

      this.generator.addText(slide, {
        x: x + 0.2,
        y: y + (cardH - 0.5) / 2,
        w: 0.5,
        h: 0.5,
        text: item.icon,
        fontSize: 14,
        fontFace: 'Arial',
        color: 'FFFFFF',
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 标签
      this.generator.addText(slide, {
        x: x + 0.9,
        y: y + 0.05,
        w: 1.5,
        h: 0.35,
        text: item.label,
        fontSize: 11,
        fontFace: '微软雅黑',
        color: this.theme.muted,
        align: 'left',
        valign: 'middle',
      });

      // 值
      this.generator.addText(slide, {
        x: x + 0.9,
        y: y + 0.4,
        w: cardW - 1.2,
        h: 0.4,
        text: item.value,
        fontSize: 14,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });
    });

    // 社交媒体
    if (data.social && data.social.length > 0) {
      const socialY = 5.5;
      const socialStartX = (13.33 - data.social.length * 1.5) / 2;

      this.generator.addText(slide, {
        x: 0.5,
        y: socialY - 0.3,
        w: 12,
        h: 0.4,
        text: '关注我们',
        fontSize: 12,
        fontFace: '微软雅黑',
        color: this.theme.muted,
        align: 'center',
        valign: 'middle',
      });

      data.social.forEach((s, i) => {
        const x = socialStartX + i * 1.5;

        slide.addShape(this.generator.getShapes().OVAL as any, {
          x: x,
          y: socialY + 0.2,
          w: 0.6,
          h: 0.6,
          fill: { color: this.theme.primary },
        });

        this.generator.addText(slide, {
          x: x,
          y: socialY + 0.2,
          w: 0.6,
          h: 0.6,
          text: s.platform.charAt(0),
          fontSize: 14,
          fontFace: 'Arial',
          color: 'FFFFFF',
          bold: true,
          align: 'center',
          valign: 'middle',
        });

        this.generator.addText(slide, {
          x: x - 0.2,
          y: socialY + 0.9,
          w: 1,
          h: 0.3,
          text: s.handle,
          fontSize: 8,
          fontFace: '微软雅黑',
          color: this.theme.muted,
          align: 'center',
          valign: 'middle',
        });
      });
    }

    return slide;
  }
}
