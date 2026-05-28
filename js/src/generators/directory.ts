/**
 * 目录页生成器模块
 * 包含6种不同风格的目录页模板
 * - 菱形动画、圆环目录、六边形目录
 * - 侧边栏目录、卡片网格目录、时间线目录
 */

import pptxgen from 'pptxgenjs';
import { TemplateGenerator, Theme } from '../base';
import { createCirclePositions, createGridPositions } from '../utils';

/** 目录项数据接口 */
export interface DirectoryItem {
  /** 序号 */
  index: number;
  /** 标题 */
  title: string;
  /** 描述 */
  description?: string;
  /** 图标（可选） */
  icon?: string;
}

/** 目录数据接口 */
export interface DirectoryData {
  /** 页面标题 */
  pageTitle?: string;
  /** 目录项列表 */
  items: DirectoryItem[];
}

/** 基础目录类 */
abstract class BaseDirectory {
  protected generator: TemplateGenerator;
  protected theme: Theme;

  constructor(generator: TemplateGenerator, theme: Theme) {
    this.generator = generator;
    this.theme = theme;
  }

  /** 生成目录页 */
  abstract generate(data: DirectoryData): pptxgen.Slide;

  /** 添加页面标题 */
  protected addPageTitle(slide: pptxgen.Slide, title: string): void {
    this.generator.addText(slide, {
      x: 0.5,
      y: 0.3,
      w: 12,
      h: 0.8,
      text: title,
      fontSize: 28,
      fontFace: '微软雅黑',
      color: this.theme.primary,
      bold: true,
      align: 'left',
      valign: 'middle',
    });
  }

  /** 添加页面装饰线 */
  protected addUnderline(slide: pptxgen.Slide, x: number, y: number, width: number): void {
    this.generator.getPresentation();
    slide.addShape((this.generator.getShapes().LINE as any), {
      x: x,
      y: y,
      w: width,
      h: 0,
      line: { color: this.theme.accent, width: 3 },
    });
  }
}

/**
 * 菱形动画目录
 * 使用菱形序号标记，带有层次感
 */
export class DiamondAnimated extends BaseDirectory {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: DirectoryData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle || '目录');
    this.addUnderline(slide, 0.5, 1.1, 2);

    const items = data.items;
    const startY = 1.8;
    const itemHeight = 0.85;

    items.forEach((item, i) => {
      const y = startY + i * itemHeight;

      // 菱形序号背景
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: 0.8,
        y: y,
        w: 0.5,
        h: 0.5,
        fill: { color: this.theme.primary },
        rotate: 45,
      });

      // 序号文本
      this.generator.addText(slide, {
        x: 0.8,
        y: y,
        w: 0.5,
        h: 0.5,
        text: String(item.index),
        fontSize: 14,
        fontFace: '微软雅黑',
        color: 'FFFFFF',
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: 1.8,
        y: y - 0.05,
        w: 5,
        h: 0.35,
        text: item.title,
        fontSize: 18,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });

      // 描述
      if (item.description) {
        this.generator.addText(slide, {
          x: 1.8,
          y: y + 0.3,
          w: 5,
          h: 0.3,
          text: item.description,
          fontSize: 11,
          fontFace: '微软雅黑',
          color: this.theme.muted,
          align: 'left',
          valign: 'top',
        });
      }

      // 连接线
      if (i < items.length - 1) {
        slide.addShape(this.generator.getShapes().LINE as any, {
          x: 1.05,
          y: y + 0.5,
          w: 0,
          h: itemHeight - 0.5,
          line: { color: this.theme.secondary, width: 1, dashType: 'dash' as any },
        });
      }
    });

    // 右侧装饰
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 10,
      y: 0,
      w: 3.33,
      h: 7.5,
      fill: { color: this.theme.primary, transparency: 90 },
    });

    // 右侧装饰大序号
    if (items.length > 0) {
      this.generator.addText(slide, {
        x: 10.5,
        y: 2,
        w: 2.5,
        h: 3.5,
        text: String(items.length).padStart(2, '0'),
        fontSize: 100,
        fontFace: 'Arial',
        color: this.theme.primary,
        bold: true,
        align: 'center',
        valign: 'middle',
      });
    }

    return slide;
  }
}

/**
 * 圆环目录
 * 使用圆形排列展示目录项
 */
export class CircularRing extends BaseDirectory {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: DirectoryData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle || '目录');
    this.addUnderline(slide, 0.5, 1.1, 2);

    const items = data.items;
    const centerX = 6.665;
    const centerY = 4.2;
    const radius = 2.5;

    const positions = createCirclePositions(centerX, centerY, radius, items.length);

    items.forEach((item, i) => {
      const pos = positions[i];
      const nodeSize = 1.4;

      // 圆形节点
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: pos.x - nodeSize / 2,
        y: pos.y - nodeSize / 2,
        w: nodeSize,
        h: nodeSize,
        fill: { color: i === 0 ? this.theme.primary : this.theme.secondary },
        shadow: {
          type: 'outer' as any,
          color: '000000',
          blur: 5,
          offset: 2,
          angle: 135,
          opacity: 0.1,
        },
      });

      // 序号
      this.generator.addText(slide, {
        x: pos.x - nodeSize / 2,
        y: pos.y - nodeSize / 2 - 0.1,
        w: nodeSize,
        h: 0.5,
        text: String(item.index),
        fontSize: 18,
        fontFace: 'Arial',
        color: 'FFFFFF',
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: pos.x - 1.2,
        y: pos.y + nodeSize / 2 - 0.1,
        w: 2.4,
        h: 0.4,
        text: item.title,
        fontSize: 12,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'center',
        valign: 'top',
      });
    });

    // 中心标题
    slide.addShape(this.generator.getShapes().OVAL as any, {
      x: centerX - 1,
      y: centerY - 1,
      w: 2,
      h: 2,
      fill: { color: this.theme.primary },
    });

    this.generator.addText(slide, {
      x: centerX - 1,
      y: centerY - 0.5,
      w: 2,
      h: 1,
      text: '目录',
      fontSize: 20,
      fontFace: '微软雅黑',
      color: 'FFFFFF',
      bold: true,
      align: 'center',
      valign: 'middle',
    });

    return slide;
  }
}

/**
 * 六边形目录
 * 使用六边形网格展示目录项
 */
export class Hexagon extends BaseDirectory {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: DirectoryData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle || '目录');
    this.addUnderline(slide, 0.5, 1.1, 2);

    const items = data.items;
    const cols = 3;
    const rows = Math.ceil(items.length / cols);
    const hexSize = 1.2;
    const startX = 1.5;
    const startY = 2.0;
    const gapX = 3.5;
    const gapY = 2.5;

    items.forEach((item, i) => {
      const col = i % cols;
      const row = Math.floor(i / cols);
      const offsetX = row % 2 === 1 ? gapX / 2 : 0;
      const x = startX + col * gapX + offsetX;
      const y = startY + row * gapY;

      // 六边形（用矩形近似）
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x,
        y: y,
        w: hexSize * 2,
        h: hexSize * 1.73,
        fill: { color: i === 0 ? this.theme.primary : this.theme.secondary },
        rectRadius: 0.1,
        rotate: 30,
        shadow: {
          type: 'outer' as any,
          color: '000000',
          blur: 8,
          offset: 3,
          angle: 135,
          opacity: 0.12,
        },
      });

      // 序号
      this.generator.addText(slide, {
        x: x,
        y: y - 0.2,
        w: hexSize * 2,
        h: 0.5,
        text: String(item.index).padStart(2, '0'),
        fontSize: 16,
        fontFace: 'Arial',
        color: 'FFFFFF',
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: x,
        y: y + 0.25,
        w: hexSize * 2,
        h: 0.4,
        text: item.title,
        fontSize: 12,
        fontFace: '微软雅黑',
        color: 'FFFFFF',
        bold: true,
        align: 'center',
        valign: 'middle',
      });
    });

    return slide;
  }
}

/**
 * 侧边栏目录
 * 左侧固定栏 + 右侧目录列表
 */
export class Sidebar extends BaseDirectory {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: DirectoryData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 左侧深色栏
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 0,
      y: 0,
      w: 4,
      h: 7.5,
      fill: { color: this.theme.primary },
    });

    // 左侧标题
    this.generator.addText(slide, {
      x: 0.5,
      y: 2,
      w: 3,
      h: 1,
      text: data.pageTitle || '目录',
      fontSize: 32,
      fontFace: '微软雅黑',
      color: 'FFFFFF',
      bold: true,
      align: 'left',
      valign: 'middle',
    });

    // 左侧装饰线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 0.5,
      y: 3.2,
      w: 2.5,
      h: 0,
      line: { color: 'FFFFFF', width: 2, transparency: 50 },
    });

    // 左侧项目数量
    this.generator.addText(slide, {
      x: 0.5,
      y: 3.5,
      w: 3,
      h: 0.5,
      text: `共 ${data.items.length} 个章节`,
      fontSize: 14,
      fontFace: '微软雅黑',
      color: 'CCCCCC',
      align: 'left',
      valign: 'top',
    });

    // 右侧目录列表
    const items = data.items;
    const startY = 0.8;
    const itemHeight = 1.0;

    items.forEach((item, i) => {
      const y = startY + i * itemHeight;

      // 序号圆圈
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: 5,
        y: y + 0.15,
        w: 0.5,
        h: 0.5,
        fill: { color: this.theme.primary },
      });

      this.generator.addText(slide, {
        x: 5,
        y: y + 0.15,
        w: 0.5,
        h: 0.5,
        text: String(item.index),
        fontSize: 12,
        fontFace: 'Arial',
        color: 'FFFFFF',
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: 5.8,
        y: y + 0.05,
        w: 6.5,
        h: 0.35,
        text: item.title,
        fontSize: 16,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });

      // 描述
      if (item.description) {
        this.generator.addText(slide, {
          x: 5.8,
          y: y + 0.4,
          w: 6.5,
          h: 0.3,
          text: item.description,
          fontSize: 11,
          fontFace: '微软雅黑',
          color: this.theme.muted,
          align: 'left',
          valign: 'top',
        });
      }

      // 分隔线
      if (i < items.length - 1) {
        slide.addShape(this.generator.getShapes().LINE as any, {
          x: 5,
          y: y + itemHeight - 0.05,
          w: 7.5,
          h: 0,
          line: { color: this.theme.muted, width: 0.5, transparency: 50 },
        });
      }
    });

    return slide;
  }
}

/**
 * 卡片网格目录
 * 使用卡片式网格布局展示目录
 */
export class CardGrid extends BaseDirectory {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: DirectoryData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle || '目录');
    this.addUnderline(slide, 0.5, 1.1, 2);

    const items = data.items;
    const cols = 3;
    const cardWidth = 3.5;
    const cardHeight = 2.5;
    const startX = 0.8;
    const startY = 1.8;
    const gapX = 0.5;
    const gapY = 0.4;

    items.forEach((item, i) => {
      const col = i % cols;
      const row = Math.floor(i / cols);
      const x = startX + col * (cardWidth + gapX);
      const y = startY + row * (cardHeight + gapY);

      // 卡片背景
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x,
        y: y,
        w: cardWidth,
        h: cardHeight,
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

      // 顶部色带
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x,
        y: y,
        w: cardWidth,
        h: 0.08,
        fill: { color: this.theme.primary },
        rectRadius: 0.1,
      });

      // 序号
      this.generator.addText(slide, {
        x: x + 0.3,
        y: y + 0.3,
        w: 0.6,
        h: 0.5,
        text: String(item.index).padStart(2, '0'),
        fontSize: 24,
        fontFace: 'Arial',
        color: this.theme.primary,
        bold: true,
        align: 'left',
        valign: 'middle',
      });

      // 标题
      this.generator.addText(slide, {
        x: x + 0.3,
        y: y + 0.9,
        w: cardWidth - 0.6,
        h: 0.4,
        text: item.title,
        fontSize: 16,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });

      // 描述
      if (item.description) {
        this.generator.addText(slide, {
          x: x + 0.3,
          y: y + 1.4,
          w: cardWidth - 0.6,
          h: 0.8,
          text: item.description,
          fontSize: 11,
          fontFace: '微软雅黑',
          color: this.theme.muted,
          align: 'left',
          valign: 'top',
          wrap: true,
        });
      }
    });

    return slide;
  }
}

/**
 * 时间线目录
 * 使用垂直时间线展示目录结构
 */
export class TimelineStyle extends BaseDirectory {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: DirectoryData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle || '目录');
    this.addUnderline(slide, 0.5, 1.1, 2);

    const items = data.items;
    const centerX = 6.665;
    const startY = 1.8;
    const itemHeight = 0.9;

    // 中心时间线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: centerX,
      y: startY,
      w: 0,
      h: items.length * itemHeight,
      line: { color: this.theme.primary, width: 3 },
    });

    items.forEach((item, i) => {
      const y = startY + i * itemHeight;
      const isLeft = i % 2 === 0;

      // 时间线节点圆圈
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: centerX - 0.2,
        y: y + 0.15,
        w: 0.4,
        h: 0.4,
        fill: { color: this.theme.primary },
        line: { color: 'FFFFFF', width: 2 },
      });

      // 连接线
      const lineStart = isLeft ? centerX - 0.2 : centerX + 0.6;
      const lineWidth = isLeft ? 2 : 2;

      slide.addShape(this.generator.getShapes().LINE as any, {
        x: isLeft ? centerX - 2.5 : centerX + 0.6,
        y: y + 0.35,
        w: 2.3,
        h: 0,
        line: { color: this.theme.secondary, width: 1, dashType: 'dash' as any },
      });

      // 文本（交替左右）
      const textX = isLeft ? centerX - 6 : centerX + 1.5;
      const textAlign = isLeft ? 'right' as const : 'left' as const;

      // 序号
      this.generator.addText(slide, {
        x: textX,
        y: y + 0.05,
        w: 3.5,
        h: 0.35,
        text: `${String(item.index).padStart(2, '0')} - ${item.title}`,
        fontSize: 14,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: textAlign,
        valign: 'middle',
      });

      // 描述
      if (item.description) {
        this.generator.addText(slide, {
          x: textX,
          y: y + 0.4,
          w: 3.5,
          h: 0.35,
          text: item.description,
          fontSize: 10,
          fontFace: '微软雅黑',
          color: this.theme.muted,
          align: textAlign,
          valign: 'top',
        });
      }
    });

    return slide;
  }
}
