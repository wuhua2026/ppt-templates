/**
 * 封面页生成器模块
 * 包含8种不同风格的封面页模板
 * - 动画类：几何旋转、圆环旋转、火车迷雾、菱形揭示
 * - 静态类：极简渐变、分屏、镂空蒙版、层次叠加
 */

import pptxgen from 'pptxgenjs';
import { TemplateGenerator, Theme } from '../base';
import { lightenColor, darkenColor } from '../utils';

/** 封面数据接口 */
export interface CoverData {
  /** 标题 */
  title: string;
  /** 副标题 */
  subtitle?: string;
  /** 演讲者/作者 */
  presenter?: string;
  /** 日期 */
  date?: string;
  /** 公司/组织名称 */
  company?: string;
}

/** 基础封面类 */
abstract class BaseCover {
  protected generator: TemplateGenerator;
  protected theme: Theme;

  constructor(generator: TemplateGenerator, theme: Theme) {
    this.generator = generator;
    this.theme = theme;
  }

  /** 生成封面页 */
  abstract generate(data: CoverData): pptxgen.Slide;

  /** 添加标题文本 */
  protected addTitle(slide: pptxgen.Slide, data: CoverData, options: any = {}): void {
    this.generator.addText(slide, {
      x: options.x || 0.8,
      y: options.y || 2.5,
      w: options.w || 11.5,
      h: options.h || 1.5,
      text: data.title,
      fontSize: options.fontSize || 40,
      fontFace: '微软雅黑',
      color: options.color || this.theme.text,
      bold: true,
      align: options.align || 'center',
      valign: 'middle',
    });
  }

  /** 添加副标题 */
  protected addSubtitle(slide: pptxgen.Slide, data: CoverData, options: any = {}): void {
    if (!data.subtitle) return;
    this.generator.addText(slide, {
      x: options.x || 0.8,
      y: options.y || 4.0,
      w: options.w || 11.5,
      h: options.h || 0.8,
      text: data.subtitle,
      fontSize: options.fontSize || 20,
      fontFace: '微软雅黑',
      color: options.color || this.theme.muted,
      align: options.align || 'center',
      valign: 'middle',
    });
  }

  /** 添加日期和作者信息 */
  protected addInfo(slide: pptxgen.Slide, data: CoverData, options: any = {}): void {
    const info = [
      data.presenter,
      data.date,
      data.company,
    ].filter(Boolean).join(' | ');

    if (info) {
      this.generator.addText(slide, {
        x: options.x || 0.8,
        y: options.y || 5.5,
        w: options.w || 11.5,
        h: options.h || 0.5,
        text: info,
        fontSize: options.fontSize || 12,
        fontFace: '微软雅黑',
        color: options.color || this.theme.muted,
        align: options.align || 'center',
        valign: 'middle',
      });
    }
  }
}

/**
 * 几何旋转封面
 * 使用多个旋转的几何形状作为装饰
 */
export class GeometricRotation extends BaseCover {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: CoverData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 背景
    slide.background = { fill: this.theme.background };

    // 左侧装饰几何形状
    const shapes: Array<{ x: number; y: number; w: number; h: number; color: string; rotate: number }> = [
      { x: -0.5, y: -0.5, w: 3, h: 3, color: this.theme.primary, rotate: 15 },
      { x: -0.2, y: 4.5, w: 2.5, h: 2.5, color: this.theme.secondary, rotate: -30 },
      { x: 10.5, y: 0.5, w: 2, h: 2, color: this.theme.accent, rotate: 45 },
      { x: 11, y: 5, w: 2.5, h: 2.5, color: this.theme.primary, rotate: 60 },
      { x: 5, y: -0.3, w: 1.5, h: 1.5, color: this.theme.secondary, rotate: 30 },
      { x: 8, y: 6, w: 2, h: 2, color: this.theme.accent, rotate: -20 },
    ];

    shapes.forEach(shape => {
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: shape.x,
        y: shape.y,
        w: shape.w,
        h: shape.h,
        fill: { color: shape.color, transparency: 85 },
        rotate: shape.rotate,
      });
    });

    // 中央分割线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 4.5,
      y: 2.0,
      w: 4.3,
      h: 0,
      line: { color: this.theme.primary, width: 2 },
    });

    // 标题
    this.addTitle(slide, data, { y: 2.2, fontSize: 44, color: this.theme.text });

    // 分割线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 4.5,
      y: 3.8,
      w: 4.3,
      h: 0,
      line: { color: this.theme.primary, width: 2 },
    });

    // 副标题
    this.addSubtitle(slide, data, { y: 4.0 });

    // 底部信息
    this.addInfo(slide, data, { y: 5.8 });

    return slide;
  }
}

/**
 * 圆环旋转封面
 * 使用同心圆环作为主要视觉元素
 */
export class CircleRing extends BaseCover {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: CoverData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 背景
    slide.background = { fill: this.theme.darkBg };

    // 同心圆环
    const rings = [
      { x: 4.16, y: 1.5, w: 5, h: 5, color: this.theme.primary, transparency: 70 },
      { x: 4.66, y: 2.0, w: 4, h: 4, color: this.theme.secondary, transparency: 60 },
      { x: 5.16, y: 2.5, w: 3, h: 3, color: this.theme.accent, transparency: 50 },
    ];

    rings.forEach(ring => {
      slide.addShape(this.generator.getShapes().OVAL as any, {
        x: ring.x,
        y: ring.y,
        w: ring.w,
        h: ring.h,
        line: { color: ring.color, width: 2, transparency: ring.transparency },
        fill: { color: ring.color, transparency: 95 },
      });
    });

    // 右侧装饰线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 10,
      y: 1,
      w: 0,
      h: 5.5,
      line: { color: this.theme.primary, width: 1, transparency: 50 },
    });

    // 标题（白色，适合深色背景）
    this.addTitle(slide, data, {
      y: 3.0,
      color: 'FFFFFF',
      fontSize: 42,
      align: 'center',
    });

    // 副标题
    this.addSubtitle(slide, data, {
      y: 4.2,
      color: 'CCCCCC',
    });

    // 底部信息
    this.addInfo(slide, data, {
      y: 6.0,
      color: '999999',
    });

    return slide;
  }
}

/**
 * 火车迷雾封面
 * 使用多层半透明矩形营造层次感
 */
export class TrainMist extends BaseCover {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: CoverData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 背景
    slide.background = { fill: this.theme.background };

    // 多层半透明矩形（营造迷雾效果）
    const layers = [
      { x: -1, y: 0, w: 6, h: 7.5, color: this.theme.primary, transparency: 90 },
      { x: 0, y: -0.5, w: 5, h: 8, color: this.theme.secondary, transparency: 85 },
      { x: 1, y: 0.5, w: 4, h: 6.5, color: this.theme.accent, transparency: 80 },
    ];

    layers.forEach(layer => {
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: layer.x,
        y: layer.y,
        w: layer.w,
        h: layer.h,
        fill: { color: layer.color, transparency: layer.transparency },
      });
    });

    // 右侧装饰条
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 10,
      y: 0,
      w: 3.33,
      h: 7.5,
      fill: { color: this.theme.primary, transparency: 80 },
    });

    // 标题
    this.addTitle(slide, data, {
      x: 3,
      y: 2.5,
      w: 8,
      fontSize: 38,
      align: 'left',
      color: this.theme.text,
    });

    // 副标题
    this.addSubtitle(slide, data, {
      x: 3,
      y: 4.0,
      w: 8,
      align: 'left',
    });

    // 底部信息
    this.addInfo(slide, data, {
      x: 3,
      y: 5.8,
      w: 8,
      align: 'left',
    });

    return slide;
  }
}

/**
 * 菱形揭示封面
 * 使用菱形组合揭示主题内容
 */
export class DiamondReveal extends BaseCover {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: CoverData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 背景
    slide.background = { fill: this.theme.background };

    // 菱形装饰
    const diamonds = [
      { x: 6, y: 1, w: 2.5, h: 2.5, color: this.theme.primary, transparency: 80 },
      { x: 7, y: 2, w: 2, h: 2, color: this.theme.secondary, transparency: 70 },
      { x: 5, y: 3.5, w: 3, h: 3, color: this.theme.accent, transparency: 85 },
      { x: 8, y: 4, w: 1.5, h: 1.5, color: this.theme.primary, transparency: 75 },
    ];

    diamonds.forEach(d => {
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: d.x,
        y: d.y,
        w: d.w,
        h: d.h,
        fill: { color: d.color, transparency: d.transparency },
        rotate: 45,
      });
    });

    // 左侧装饰线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 2,
      y: 0.5,
      w: 0,
      h: 6.5,
      line: { color: this.theme.primary, width: 3 },
    });

    // 标题
    this.addTitle(slide, data, {
      x: 0.5,
      y: 2.5,
      w: 6,
      fontSize: 36,
      align: 'left',
    });

    // 副标题
    this.addSubtitle(slide, data, {
      x: 0.5,
      y: 4.0,
      w: 6,
      align: 'left',
    });

    // 底部信息
    this.addInfo(slide, data, {
      x: 0.5,
      y: 5.8,
      w: 6,
      align: 'left',
    });

    return slide;
  }
}

/**
 * 极简渐变封面
 * 使用大面积渐变色块，简洁大气
 */
export class MinimalistGradient extends BaseCover {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: CoverData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 背景渐变（使用纯色近似）
    slide.background = { fill: this.theme.background };

    // 左侧大色块
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 0,
      y: 0,
      w: 6,
      h: 7.5,
      fill: { color: this.theme.primary },
    });

    // 色块上的装饰线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 0.8,
      y: 3.0,
      w: 4,
      h: 0,
      line: { color: 'FFFFFF', width: 1, transparency: 50 },
    });

    // 左侧标题（白色）
    this.addTitle(slide, data, {
      x: 0.8,
      y: 3.2,
      w: 4.5,
      fontSize: 36,
      align: 'left',
      color: 'FFFFFF',
    });

    // 左侧副标题（白色）
    this.addSubtitle(slide, data, {
      x: 0.8,
      y: 4.5,
      w: 4.5,
      align: 'left',
      color: 'DDDDDD',
    });

    // 右侧信息
    const info = [data.presenter, data.company].filter(Boolean).join('\n');
    if (info) {
      this.generator.addText(slide, {
        x: 7,
        y: 3.5,
        w: 5,
        h: 1.5,
        text: info,
        fontSize: 14,
        fontFace: '微软雅黑',
        color: this.theme.muted,
        align: 'left',
        valign: 'top',
        lineSpacingMultiple: 1.5,
      });
    }

    // 右侧日期
    if (data.date) {
      this.generator.addText(slide, {
        x: 7,
        y: 5.5,
        w: 5,
        h: 0.5,
        text: data.date,
        fontSize: 12,
        fontFace: '微软雅黑',
        color: this.theme.muted,
        align: 'left',
      });
    }

    return slide;
  }
}

/**
 * 分屏封面
 * 将画面分为左右两部分，一侧文字一侧图形
 */
export class SplitScreen extends BaseCover {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: CoverData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 背景
    slide.background = { fill: 'FFFFFF' };

    // 右半部分色块
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 6.5,
      y: 0,
      w: 6.83,
      h: 7.5,
      fill: { color: this.theme.primary },
    });

    // 右侧装饰圆
    slide.addShape(this.generator.getShapes().OVAL as any, {
      x: 7.5,
      y: 1.5,
      w: 4.5,
      h: 4.5,
      fill: { color: this.theme.secondary, transparency: 60 },
    });

    // 中间分割线
    slide.addShape(this.generator.getShapes().LINE as any, {
      x: 6.5,
      y: 0.5,
      w: 0,
      h: 6.5,
      line: { color: this.theme.accent, width: 3 },
    });

    // 左侧标题
    this.addTitle(slide, data, {
      x: 0.5,
      y: 2.5,
      w: 5.5,
      fontSize: 38,
      align: 'left',
    });

    // 左侧副标题
    this.addSubtitle(slide, data, {
      x: 0.5,
      y: 4.0,
      w: 5.5,
      align: 'left',
    });

    // 左侧底部信息
    this.addInfo(slide, data, {
      x: 0.5,
      y: 5.8,
      w: 5.5,
      align: 'left',
    });

    // 右侧装饰性文本
    this.generator.addText(slide, {
      x: 7.5,
      y: 6.2,
      w: 4.5,
      h: 0.5,
      text: data.date || '',
      fontSize: 12,
      fontFace: '微软雅黑',
      color: 'FFFFFF',
      align: 'center',
    });

    return slide;
  }
}

/**
 * 镂空蒙版封面
 * 使用镂空效果展示背景
 */
export class HollowMask extends BaseCover {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: CoverData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 背景
    slide.background = { fill: this.theme.darkBg };

    // 外层蒙版矩形
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 0,
      y: 0,
      w: 13.33,
      h: 7.5,
      fill: { color: this.theme.darkBg },
    });

    // 镂空区域 - 中心浅色矩形
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 2.5,
      y: 1.5,
      w: 8.33,
      h: 4.5,
      fill: { color: this.theme.background },
      rectRadius: 0.1,
    });

    // 镂空区域边框
    slide.addShape(this.generator.getShapes().RECTANGLE as any, {
      x: 2.5,
      y: 1.5,
      w: 8.33,
      h: 4.5,
      line: { color: this.theme.primary, width: 2 },
      fill: { color: '000000', transparency: 100 },
      rectRadius: 0.1,
    });

    // 标题
    this.addTitle(slide, data, {
      y: 2.5,
      fontSize: 40,
      color: this.theme.text,
    });

    // 副标题
    this.addSubtitle(slide, data, { y: 3.8 });

    // 底部信息
    this.addInfo(slide, data, {
      y: 6.5,
      color: 'CCCCCC',
    });

    return slide;
  }
}

/**
 * 层次叠加封面
 * 多层矩形叠加创造深度效果
 */
export class LayeredDepth extends BaseCover {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: CoverData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    // 背景
    slide.background = { fill: this.theme.background };

    // 多层叠加矩形
    const layers = [
      { x: 0.5, y: 0.5, w: 12, h: 6.5, color: this.theme.primary, transparency: 90 },
      { x: 1.0, y: 1.0, w: 11, h: 5.5, color: this.theme.secondary, transparency: 85 },
      { x: 1.5, y: 1.5, w: 10, h: 4.5, color: this.theme.accent, transparency: 80 },
    ];

    layers.forEach((layer, i) => {
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: layer.x,
        y: layer.y,
        w: layer.w,
        h: layer.h,
        fill: { color: layer.color, transparency: layer.transparency },
        rectRadius: 0.05,
        shadow: i === 2 ? {
          type: 'outer' as any,
          color: '000000',
          blur: 10,
          offset: 3,
          angle: 135,
          opacity: 0.15,
        } : undefined,
      });
    });

    // 标题
    this.addTitle(slide, data, {
      y: 2.5,
      fontSize: 42,
      color: this.theme.text,
    });

    // 副标题
    this.addSubtitle(slide, data, { y: 4.0 });

    // 底部信息
    this.addInfo(slide, data, { y: 5.8 });

    return slide;
  }
}
