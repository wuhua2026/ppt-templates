/**
 * 内容页生成器模块
 * 包含5种不同风格的内容页模板
 * - 图文混排、三栏布局、四宫格
 * - 全图叠加、对比布局
 */

import pptxgen from 'pptxgenjs';
import { TemplateGenerator, Theme } from '../base';
import { createGridPositions } from '../utils';

/** 内容块数据接口 */
export interface ContentBlock {
  /** 标题 */
  title: string;
  /** 内容文本 */
  content?: string;
  /** 图片路径 */
  image?: string;
  /** 序号/编号 */
  index?: number;
}

/** 内容页数据接口 */
export interface ContentData {
  /** 页面标题 */
  pageTitle: string;
  /** 内容块 */
  blocks?: ContentBlock[];
  /** 主要内容文本 */
  mainText?: string;
  /** 副文本 */
  subText?: string;
  /** 图片路径 */
  imagePath?: string;
}

/** 基础内容类 */
abstract class BaseContent {
  protected generator: TemplateGenerator;
  protected theme: Theme;

  constructor(generator: TemplateGenerator, theme: Theme) {
    this.generator = generator;
    this.theme = theme;
  }

  /** 生成内容页 */
  abstract generate(data: ContentData): pptxgen.Slide;

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

    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 0.5,
      y: 1.0,
      w: 2,
      h: 0,
      line: { color: this.theme.accent, width: 2 },
    });
  }
}

/**
 * 图文混排内容页
 * 左图右文或左文右图的布局
 */
export class TextImageLayout extends BaseContent {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: ContentData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    // 图片占位区域
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 0.5,
      y: 1.5,
      w: 5.5,
      h: 5.5,
      fill: { color: this.theme.primary, transparency: 85 },
      rectRadius: 0.1,
    });

    // 图片占位符文字
    this.generator.addText(slide, {
      x: 0.5,
      y: 3.5,
      w: 5.5,
      h: 1,
      text: '[图片占位]',
      fontSize: 16,
      fontFace: '微软雅黑',
      color: this.theme.muted,
      align: 'center',
      valign: 'middle',
    });

    // 右侧标题
    this.generator.addText(slide, {
      x: 6.5,
      y: 1.8,
      w: 6,
      h: 0.6,
      text: data.blocks?.[0]?.title || data.pageTitle,
      fontSize: 22,
      fontFace: '微软雅黑',
      color: this.theme.text,
      bold: true,
      align: 'left',
      valign: 'middle',
    });

    // 分隔线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 6.5,
      y: 2.5,
      w: 3,
      h: 0,
      line: { color: this.theme.accent, width: 2 },
    });

    // 右侧内容
    this.generator.addText(slide, {
      x: 6.5,
      y: 2.8,
      w: 6,
      h: 4,
      text: data.blocks?.[0]?.content || data.mainText || '',
      fontSize: 14,
      fontFace: '微软雅黑',
      color: this.theme.text,
      align: 'left',
      valign: 'top',
      wrap: true,
      lineSpacingMultiple: 1.5,
    });

    return slide;
  }
}

/**
 * 三栏布局内容页
 * 将内容分为三列展示
 */
export class ThreeColumn extends BaseContent {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: ContentData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    const blocks = data.blocks || [];
    const colWidth = 3.6;
    const startX = 0.65;
    const startY = 1.5;
    const colors = [this.theme.primary, this.theme.secondary, this.theme.accent];

    for (let i = 0; i < Math.min(3, blocks.length); i++) {
      const x = startX + i * (colWidth + 0.45);
      const block = blocks[i];
      const color = colors[i % colors.length];

      // 列顶部色块
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x,
        y: startY,
        w: colWidth,
        h: 0.08,
        fill: { color: color },
      });

      // 卡片背景
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x,
        y: startY + 0.08,
        w: colWidth,
        h: 5.4,
        fill: { color: 'FFFFFF' },
        rectRadius: 0.05,
        shadow: {
          type: 'outer' as any,
          color: '000000',
          blur: 6,
          offset: 2,
          angle: 135,
          opacity: 0.08,
        },
      });

      // 序号圆圈
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: x + 0.3,
        y: startY + 0.4,
        w: 0.6,
        h: 0.6,
        fill: { color: color },
      });

      this.generator.addText(slide, {
        x: x + 0.3,
        y: startY + 0.4,
        w: 0.6,
        h: 0.6,
        text: String(block.index || i + 1),
        fontSize: 16,
        fontFace: 'Arial',
        color: 'FFFFFF',
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: x + 1.1,
        y: startY + 0.45,
        w: colWidth - 1.4,
        h: 0.5,
        text: block.title,
        fontSize: 16,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });

      // 图片占位
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x + 0.3,
        y: startY + 1.3,
        w: colWidth - 0.6,
        h: 2,
        fill: { color: color, transparency: 88 },
        rectRadius: 0.05,
      });

      // 内容文本
      this.generator.addText(slide, {
        x: x + 0.3,
        y: startY + 3.5,
        w: colWidth - 0.6,
        h: 1.8,
        text: block.content || '',
        fontSize: 11,
        fontFace: '微软雅黑',
        color: this.theme.text,
        align: 'left',
        valign: 'top',
        wrap: true,
        lineSpacingMultiple: 1.4,
      });
    }

    return slide;
  }
}

/**
 * 四宫格布局内容页
 * 2x2网格展示四个内容块
 */
export class FourGrid extends BaseContent {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: ContentData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    const blocks = data.blocks || [];
    const gridWidth = 5.8;
    const gridHeight = 2.6;
    const startX = 0.6;
    const startY = 1.4;
    const gap = 0.4;
    const positions = createGridPositions(startX, startY, gridWidth, gridHeight, 2, 2, gap, gap);

    for (let i = 0; i < Math.min(4, blocks.length); i++) {
      const pos = positions[i];
      const block = blocks[i];
      const color = i % 2 === 0 ? this.theme.primary : this.theme.secondary;

      // 卡片背景
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: pos.x,
        y: pos.y,
        w: gridWidth,
        h: gridHeight,
        fill: { color: 'FFFFFF' },
        rectRadius: 0.1,
        shadow: {
          type: 'outer' as any,
          color: '000000',
          blur: 8,
          offset: 3,
          angle: 135,
          opacity: 0.1,
        },
      });

      // 左侧色条
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: pos.x,
        y: pos.y,
        w: 0.1,
        h: gridHeight,
        fill: { color: color },
      });

      // 序号
      this.generator.addText(slide, {
        x: pos.x + 0.3,
        y: pos.y + 0.2,
        w: 0.8,
        h: 0.5,
        text: String(block.index || i + 1).padStart(2, '0'),
        fontSize: 28,
        fontFace: 'Arial',
        color: color,
        bold: true,
        align: 'left',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: pos.x + 1.2,
        y: pos.y + 0.25,
        w: gridWidth - 1.5,
        h: 0.4,
        text: block.title,
        fontSize: 16,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });

      // 分隔线
      slide.addShape(this.generator.getShapes().LINE as any, {
        x: pos.x + 0.3,
        y: pos.y + 0.85,
        w: gridWidth - 0.6,
        h: 0,
        line: { color: this.theme.muted, width: 0.5, transparency: 50 },
      });

      // 内容文本
      this.generator.addText(slide, {
        x: pos.x + 0.3,
        y: pos.y + 1.0,
        w: gridWidth - 0.6,
        h: 1.4,
        text: block.content || '',
        fontSize: 12,
        fontFace: '微软雅黑',
        color: this.theme.text,
        align: 'left',
        valign: 'top',
        wrap: true,
        lineSpacingMultiple: 1.4,
      });
    }

    return slide;
  }
}

/**
 * 全图叠加内容页
 * 大面积图片背景上叠加文字
 */
export class FullImageOverlay extends BaseContent {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: ContentData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 深色背景模拟图片
    slide.background = { fill: this.theme.darkBg };

    // 图片占位区域（全屏）
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 0,
      y: 0,
      w: 13.33,
      h: 7.5,
      fill: { color: this.theme.primary, transparency: 70 },
    });

    // 占位符
    this.generator.addText(slide, {
      x: 4,
      y: 3,
      w: 5,
      h: 1,
      text: '[背景图片占位]',
      fontSize: 18,
      fontFace: '微软雅黑',
      color: 'FFFFFF',
      align: 'center',
      valign: 'middle',
    });

    // 底部半透明遮罩
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 0,
      y: 4.5,
      w: 13.33,
      h: 3,
      fill: { color: '000000', transparency: 40 },
    });

    // 标题
    this.generator.addText(slide, {
      x: 0.8,
      y: 4.8,
      w: 11.5,
      h: 0.8,
      text: data.pageTitle,
      fontSize: 28,
      fontFace: '微软雅黑',
      color: 'FFFFFF',
      bold: true,
      align: 'left',
      valign: 'middle',
    });

    // 内容文本
    const content = data.blocks?.map(b => `${b.title}: ${b.content || ''}`).join('\n') || data.mainText || '';
    this.generator.addText(slide, {
      x: 0.8,
      y: 5.6,
      w: 11.5,
      h: 1.5,
      text: content,
      fontSize: 14,
      fontFace: '微软雅黑',
      color: 'DDDDDD',
      align: 'left',
      valign: 'top',
      wrap: true,
      lineSpacingMultiple: 1.5,
    });

    return slide;
  }
}

/**
 * 对比布局内容页
 * 左右两栏对比展示
 */
export class Comparison extends BaseContent {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: ContentData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    const leftBlock = data.blocks?.[0];
    const rightBlock = data.blocks?.[1];

    // 左半部分背景
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 0.5,
      y: 1.5,
      w: 5.8,
      h: 5.5,
      fill: { color: this.theme.primary, transparency: 90 },
      rectRadius: 0.1,
    });

    // 右半部分背景
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 6.8,
      y: 1.5,
      w: 5.8,
      h: 5.5,
      fill: { color: this.theme.accent, transparency: 90 },
      rectRadius: 0.1,
    });

    // 中间VS分隔
    slide.addShape(this.generator.getShapes().OVAL as any, {
      x: 6.05,
      y: 3.5,
      w: 1.2,
      h: 1.2,
      fill: { color: this.theme.primary },
    });

    this.generator.addText(slide, {
      x: 6.05,
      y: 3.5,
      w: 1.2,
      h: 1.2,
      text: 'VS',
      fontSize: 20,
      fontFace: 'Arial',
      color: 'FFFFFF',
      bold: true,
      align: 'center',
      valign: 'middle',
    });

    // 左侧标题
    this.generator.addText(slide, {
      x: 1,
      y: 1.8,
      w: 4.8,
      h: 0.5,
      text: leftBlock?.title || '方案 A',
      fontSize: 18,
      fontFace: '微软雅黑',
      color: this.theme.primary,
      bold: true,
      align: 'center',
      valign: 'middle',
    });

    // 左侧内容
    this.generator.addText(slide, {
      x: 1,
      y: 2.5,
      w: 4.8,
      h: 4,
      text: leftBlock?.content || '',
      fontSize: 13,
      fontFace: '微软雅黑',
      color: this.theme.text,
      align: 'left',
      valign: 'top',
      wrap: true,
      lineSpacingMultiple: 1.5,
    });

    // 右侧标题
    this.generator.addText(slide, {
      x: 7.3,
      y: 1.8,
      w: 4.8,
      h: 0.5,
      text: rightBlock?.title || '方案 B',
      fontSize: 18,
      fontFace: '微软雅黑',
      color: this.theme.accent,
      bold: true,
      align: 'center',
      valign: 'middle',
    });

    // 右侧内容
    this.generator.addText(slide, {
      x: 7.3,
      y: 2.5,
      w: 4.8,
      h: 4,
      text: rightBlock?.content || '',
      fontSize: 13,
      fontFace: '微软雅黑',
      color: this.theme.text,
      align: 'left',
      valign: 'top',
      wrap: true,
      lineSpacingMultiple: 1.5,
    });

    return slide;
  }
}
