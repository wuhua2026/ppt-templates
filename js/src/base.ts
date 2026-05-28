/**
 * PPT生成器基础类
 * 提供幻灯片创建、元素添加、主题配置等核心功能
 */

import pptxgen from 'pptxgenjs';

/** 主题颜色配置接口 */
export interface Theme {
  /** 主题名称 */
  name: string;
  /** 主色调 */
  primary: string;
  /** 辅助色 */
  secondary: string;
  /** 强调色 */
  accent: string;
  /** 背景色 */
  background: string;
  /** 文字颜色 */
  text: string;
  /** 浅灰色文字 */
  muted: string;
  /** 深色背景 */
  darkBg: string;
}

/** 幻灯片尺寸选项 */
export interface SlideSize {
  /** 宽度（英寸） */
  width: number;
  /** 高度（英寸） */
  height: number;
}

/** 文本框选项 */
export interface TextBoxOptions {
  x: number;
  y: number;
  w: number;
  h: number;
  text: string;
  fontSize?: number;
  fontFace?: string;
  color?: string;
  bold?: boolean;
  italic?: boolean;
  align?: 'left' | 'center' | 'right';
  valign?: 'top' | 'middle' | 'bottom';
  wrap?: boolean;
  lineSpacingMultiple?: number;
}

/** 形状选项 */
export interface ShapeOptions {
  x: number;
  y: number;
  w: number;
  h: number;
  fill?: { color: string };
  line?: { color: string; width: number };
  shadow?: {
    type: 'outer';
    color: string;
    blur: number;
    offset: number;
    angle: number;
    opacity: number;
  };
  rectRadius?: number;
}

/** 图片选项 */
export interface ImageOptions {
  x: number;
  y: number;
  w: number;
  h: number;
  path?: string;
  data?: string;
  rounding?: boolean;
}

/**
 * PPT模板生成器基础类
 * 封装pptxgenjs的核心功能，提供简化的API
 */
export class TemplateGenerator {
  /** pptxgenjs演示文稿实例 */
  protected pptx: pptxgen;
  /** 当前主题 */
  protected theme: Theme;
  /** 幻灯片尺寸 */
  protected slideSize: SlideSize;

  /**
   * 创建模板生成器实例
   * @param theme - 主题配置
   * @param slideSize - 幻灯片尺寸，默认16:9宽屏
   */
  constructor(theme?: Theme, slideSize?: SlideSize) {
    this.pptx = new pptxgen();
    this.theme = theme || {
      name: '默认主题',
      primary: '2B579A',
      secondary: '4472C4',
      accent: 'ED7D31',
      background: 'FFFFFF',
      text: '333333',
      muted: '999999',
      darkBg: '1F1F1F'
    };
    this.slideSize = slideSize || { width: 13.33, height: 7.5 };
    this.configurePresentation();
  }

  /**
   * 配置演示文稿基础属性
   */
  private configurePresentation(): void {
    this.pptx.defineLayout({
      name: 'CUSTOM',
      width: this.slideSize.width,
      height: this.slideSize.height
    });
    this.pptx.layout = 'CUSTOM';
    this.pptx.author = 'PPT Generator';
    this.pptx.company = 'PPT Generator';
    this.pptx.subject = '自动生成演示文稿';
    this.pptx.title = '演示文稿';
  }

  /**
   * 设置演示文稿标题
   * @param title - 标题文本
   */
  setTitle(title: string): void {
    this.pptx.title = title;
  }

  /**
   * 创建新幻灯片
   * @returns 新幻灯片对象
   */
  createSlide(): pptxgen.Slide {
    return this.pptx.addSlide();
  }

  /**
   * 添加形状到幻灯片
   * @param slide - 目标幻灯片
   * @param shapeType - 形状类型
   * @param options - 形状选项
   */
  addShape(
    slide: pptxgen.Slide,
    shapeType: pptxgen.ShapeType,
    options: ShapeOptions
  ): void {
    slide.addShape(shapeType, options as any);
  }

  /**
   * 添加文本框到幻灯片
   * @param slide - 目标幻灯片
   * @param options - 文本框选项
   */
  addText(slide: pptxgen.Slide, options: TextBoxOptions): void {
    const textOptions: any = {
      x: options.x,
      y: options.y,
      w: options.w,
      h: options.h,
      fontSize: options.fontSize || 14,
      fontFace: options.fontFace || '微软雅黑',
      color: options.color || this.theme.text,
      bold: options.bold || false,
      italic: options.italic || false,
      align: options.align || 'left',
      valign: options.valign || 'top',
      wrap: options.wrap !== false,
    };
    if (options.lineSpacingMultiple) {
      textOptions.lineSpacingMultiple = options.lineSpacingMultiple;
    }
    slide.addText(options.text, textOptions);
  }

  /**
   * 添加图片到幻灯片
   * @param slide - 目标幻灯片
   * @param options - 图片选项
   */
  addImage(slide: pptxgen.Slide, options: ImageOptions): void {
    const imageOptions: any = {
      x: options.x,
      y: options.y,
      w: options.w,
      h: options.h,
    };
    if (options.path) imageOptions.path = options.path;
    if (options.data) imageOptions.data = options.data;
    if (options.rounding !== undefined) imageOptions.rounding = options.rounding;
    slide.addImage(imageOptions);
  }

  /**
   * 保存演示文稿到文件
   * @param fileName - 文件名（不含扩展名）
   * @returns Promise，resolve时返回文件路径
   */
  async save(fileName: string): Promise<string> {
    const filePath = `${fileName}.pptx`;
    await this.pptx.writeFile({ fileName: filePath });
    return filePath;
  }

  /**
   * 获取演示文稿实例（用于高级操作）
   * @returns pptxgenjs演示文稿对象
   */
  getPresentation(): pptxgen {
    return this.pptx;
  }

  /**
   * 获取当前主题
   * @returns 主题配置对象
   */
  getTheme(): Theme {
    return this.theme;
  }

  /**
   * 获取形状类型常量
   * 运行时从pptx实例获取，绕过TypeScript类型限制
   */
  get shapes(): any {
    return (this.pptx as any).shapes;
  }

  /**
   * 获取图表类型常量
   * 运行时从pptx实例获取，绕过TypeScript类型限制
   */
  get charts(): any {
    return (this.pptx as any).charts;
  }

  /**
   * 获取演示文稿实例的shapes属性
   */
  getShapes(): any {
    return (this.pptx as any).shapes;
  }

  /**
   * 获取演示文稿实例的charts属性
   */
  getCharts(): any {
    return (this.pptx as any).charts;
  }
}
