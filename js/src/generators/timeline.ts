/**
 * 时间线生成器模块
 * 包含4种不同风格的时间线模板
 * - 双波浪时间线、水平时间线、垂直时间线、螺旋时间线
 */

import pptxgen from 'pptxgenjs';
import { TemplateGenerator, Theme } from '../base';

/** 时间线数据项接口 */
export interface TimelineItem {
  /** 时间/日期 */
  date: string;
  /** 标题 */
  title: string;
  /** 描述 */
  description?: string;
  /** 是否高亮 */
  highlight?: boolean;
}

/** 时间线数据接口 */
export interface TimelineData {
  /** 页面标题 */
  pageTitle: string;
  /** 时间线项目列表 */
  items: TimelineItem[];
}

/** 基础时间线类 */
abstract class BaseTimeline {
  protected generator: TemplateGenerator;
  protected theme: Theme;

  constructor(generator: TemplateGenerator, theme: Theme) {
    this.generator = generator;
    this.theme = theme;
  }

  /** 生成时间线页 */
  abstract generate(data: TimelineData): pptxgen.Slide;

  /** 添加页面标题 */
  protected addPageTitle(slide: pptxgen.Slide, title: string): void {
    this.generator.addText(slide, {
      x: 0.5,
      y: 0.3,
      w: 12,
      h: 0.7,
      text: title,
      fontSize: 24,
      fontFace: '微软雅黑',
      color: this.theme.primary,
      bold: true,
      align: 'left',
      valign: 'middle',
    });
  }
}

/**
 * 双波浪时间线
 * 上下交错排列的时间线，模拟波浪效果
 */
export class DualWave extends BaseTimeline {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: TimelineData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    const items = data.items;
    const totalWidth = 11.5;
    const startX = 0.9;
    const topY = 1.8;
    const bottomY = 4.8;
    const spacing = totalWidth / Math.max(items.length - 1, 1);

    // 中心波浪线（水平）
    const waveY = 3.75;
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: startX,
      y: waveY,
      w: totalWidth,
      h: 0,
      line: { color: this.theme.primary, width: 3 },
    });

    items.forEach((item, i) => {
      const x = startX + i * spacing;
      const isTop = i % 2 === 0;
      const cardY = isTop ? topY : bottomY;
      const cardW = 2.2;
      const cardH = 1.5;

      // 垂直连接线
      slide.addShape(this.generator.getShapes().LINE as any, {
        x: x + cardW / 2,
        y: isTop ? cardY + cardH : waveY,
        w: 0,
        h: isTop ? waveY - cardY - cardH : cardY - waveY,
        line: { color: this.theme.secondary, width: 1.5 },
      });

      // 时间线节点
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: x + cardW / 2 - 0.15,
        y: waveY - 0.15,
        w: 0.3,
        h: 0.3,
        fill: { color: item.highlight ? this.theme.accent : this.theme.primary },
      });

      // 卡片
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x,
        y: cardY,
        w: cardW,
        h: cardH,
        fill: { color: 'FFFFFF' },
        rectRadius: 0.08,
        shadow: {
          type: 'outer' as any,
          color: '000000',
          blur: 6,
          offset: 2,
          angle: 135,
          opacity: 0.1,
        },
      });

      // 日期
      this.generator.addText(slide, {
        x: x + 0.1,
        y: cardY + 0.1,
        w: cardW - 0.2,
        h: 0.35,
        text: item.date,
        fontSize: 11,
        fontFace: 'Arial',
        color: item.highlight ? this.theme.accent : this.theme.primary,
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: x + 0.1,
        y: cardY + 0.45,
        w: cardW - 0.2,
        h: 0.35,
        text: item.title,
        fontSize: 12,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 描述
      if (item.description) {
        this.generator.addText(slide, {
          x: x + 0.1,
          y: cardY + 0.85,
          w: cardW - 0.2,
          h: 0.55,
          text: item.description,
          fontSize: 9,
          fontFace: '微软雅黑',
          color: this.theme.muted,
          align: 'center',
          valign: 'top',
          wrap: true,
        });
      }
    });

    return slide;
  }
}

/**
 * 水平时间线
 * 从左到右的线性时间线
 */
export class Horizontal extends BaseTimeline {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: TimelineData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    const items = data.items;
    const lineY = 3.5;
    const startX = 0.8;
    const endX = 12.5;
    const totalWidth = endX - startX;

    // 水平主线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: startX,
      y: lineY,
      w: totalWidth,
      h: 0,
      line: { color: this.theme.primary, width: 3 },
    });

    // 起点箭头
    slide.addShape(this.generator.getShapes().OVAL as any, {
      x: startX - 0.1,
      y: lineY - 0.1,
      w: 0.2,
      h: 0.2,
      fill: { color: this.theme.primary },
    });

    // 终点箭头
    slide.addShape(this.generator.getShapes().OVAL as any, {
      x: endX - 0.1,
      y: lineY - 0.1,
      w: 0.2,
      h: 0.2,
      fill: { color: this.theme.accent },
    });

    const spacing = totalWidth / (items.length + 1);

    items.forEach((item, i) => {
      const x = startX + spacing * (i + 1);
      const isAbove = i % 2 === 0;
      const cardW = 2;
      const cardH = 1.2;

      // 节点
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: x - 0.15,
        y: lineY - 0.15,
        w: 0.3,
        h: 0.3,
        fill: { color: item.highlight ? this.theme.accent : this.theme.primary },
      });

      // 垂直连接线
      const lineStart = isAbove ? lineY - 0.3 : lineY + 0.3;
      const lineLen = isAbove ? 0.8 : 0.8;

      slide.addShape(this.generator.getShapes().LINE as any, {
        x: x,
        y: lineStart,
        w: 0,
        h: lineLen,
        line: { color: this.theme.secondary, width: 1 },
      });

      // 卡片位置
      const cardX = x - cardW / 2;
      const cardY = isAbove ? lineY - 0.3 - lineLen - cardH : lineY + 0.3 + lineLen;

      // 卡片背景
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: cardX,
        y: cardY,
        w: cardW,
        h: cardH,
        fill: { color: 'FFFFFF' },
        rectRadius: 0.05,
        shadow: {
          type: 'outer' as any,
          color: '000000',
          blur: 5,
          offset: 2,
          angle: 135,
          opacity: 0.08,
        },
      });

      // 日期
      this.generator.addText(slide, {
        x: cardX + 0.05,
        y: cardY + 0.05,
        w: cardW - 0.1,
        h: 0.3,
        text: item.date,
        fontSize: 10,
        fontFace: 'Arial',
        color: this.theme.primary,
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: cardX + 0.05,
        y: cardY + 0.35,
        w: cardW - 0.1,
        h: 0.3,
        text: item.title,
        fontSize: 11,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 描述
      if (item.description) {
        this.generator.addText(slide, {
          x: cardX + 0.05,
          y: cardY + 0.65,
          w: cardW - 0.1,
          h: 0.5,
          text: item.description,
          fontSize: 8,
          fontFace: '微软雅黑',
          color: this.theme.muted,
          align: 'center',
          valign: 'top',
          wrap: true,
        });
      }
    });

    return slide;
  }
}

/**
 * 垂直时间线
 * 从上到下的垂直时间线
 */
export class Vertical extends BaseTimeline {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: TimelineData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    const items = data.items;
    const lineX = 6.665;
    const startY = 1.4;
    const itemSpacing = 1.15;

    // 垂直主线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: lineX,
      y: startY,
      w: 0,
      h: items.length * itemSpacing + 0.3,
      line: { color: this.theme.primary, width: 3 },
    });

    items.forEach((item, i) => {
      const y = startY + i * itemSpacing;
      const isLeft = i % 2 === 0;
      const cardW = 4.5;
      const cardH = 0.9;

      // 节点圆圈
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: lineX - 0.2,
        y: y + 0.15,
        w: 0.4,
        h: 0.4,
        fill: { color: item.highlight ? this.theme.accent : this.theme.primary },
        line: { color: 'FFFFFF', width: 2 },
      });

      // 卡片
      const cardX = isLeft ? lineX - cardW - 0.5 : lineX + 0.5;

      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: cardX,
        y: y,
        w: cardW,
        h: cardH,
        fill: { color: 'FFFFFF' },
        rectRadius: 0.05,
        shadow: {
          type: 'outer' as any,
          color: '000000',
          blur: 4,
          offset: 2,
          angle: 135,
          opacity: 0.08,
        },
      });

      // 左侧色条
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: cardX,
        y: y,
        w: 0.06,
        h: cardH,
        fill: { color: item.highlight ? this.theme.accent : this.theme.primary },
      });

      // 日期
      this.generator.addText(slide, {
        x: cardX + 0.2,
        y: y + 0.05,
        w: 1.2,
        h: 0.3,
        text: item.date,
        fontSize: 10,
        fontFace: 'Arial',
        color: this.theme.primary,
        bold: true,
        align: isLeft ? 'right' : 'left',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: cardX + 1.5,
        y: y + 0.05,
        w: cardW - 1.7,
        h: 0.3,
        text: item.title,
        fontSize: 13,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: isLeft ? 'right' : 'left',
        valign: 'middle',
      });

      // 描述
      if (item.description) {
        this.generator.addText(slide, {
          x: cardX + 0.2,
          y: y + 0.4,
          w: cardW - 0.4,
          h: 0.45,
          text: item.description,
          fontSize: 10,
          fontFace: '微软雅黑',
          color: this.theme.muted,
          align: isLeft ? 'right' : 'left',
          valign: 'top',
          wrap: true,
        });
      }
    });

    return slide;
  }
}

/**
 * 螺旋时间线
 * 使用螺旋状布局展示时间线
 */
export class Spiral extends BaseTimeline {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: TimelineData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    const items = data.items;
    const centerX = 6.665;
    const centerY = 4.2;
    const maxRadius = 2.8;

    // 螺旋装饰线（多个同心圆模拟）
    for (let r = 0.8; r <= maxRadius; r += 0.5) {
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: centerX - r,
        y: centerY - r * 0.6,
        w: r * 2,
        h: r * 1.2,
        line: { color: this.theme.primary, width: 0.5, transparency: 70 },
        fill: { color: '000000', transparency: 100 },
      });
    }

    // 项目沿着螺旋排列
    items.forEach((item, i) => {
      const angle = (i / items.length) * 2 * Math.PI - Math.PI / 2;
      const radius = 0.8 + (i / items.length) * (maxRadius - 0.8);
      const x = centerX + radius * Math.cos(angle) - 1;
      const y = centerY + radius * 0.6 * Math.sin(angle) - 0.35;

      // 节点
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: x + 0.8,
        y: y + 0.25,
        w: 0.3,
        h: 0.3,
        fill: { color: item.highlight ? this.theme.accent : this.theme.primary },
      });

      // 连接到中心的线
      slide.addShape(this.generator.getShapes().LINE as any, {
        x: x + 0.95,
        y: y + 0.4,
        w: centerX - x - 0.95,
        h: centerY - y - 0.4,
        line: { color: this.theme.secondary, width: 0.5, transparency: 60 },
      });

      // 日期
      this.generator.addText(slide, {
        x: x,
        y: y - 0.15,
        w: 2,
        h: 0.3,
        text: item.date,
        fontSize: 9,
        fontFace: 'Arial',
        color: this.theme.primary,
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: x,
        y: y + 0.6,
        w: 2,
        h: 0.3,
        text: item.title,
        fontSize: 11,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'center',
        valign: 'middle',
      });
    });

    // 中心标签
    slide.addShape(this.generator.getShapes().OVAL as any, {
      x: centerX - 0.6,
      y: centerY - 0.4,
      w: 1.2,
      h: 0.8,
      fill: { color: this.theme.primary },
    });

    this.generator.addText(slide, {
      x: centerX - 0.6,
      y: centerY - 0.4,
      w: 1.2,
      h: 0.8,
      text: '时间线',
      fontSize: 12,
      fontFace: '微软雅黑',
      color: 'FFFFFF',
      bold: true,
      align: 'center',
      valign: 'middle',
    });

    return slide;
  }
}
