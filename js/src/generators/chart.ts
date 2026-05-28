/**
 * 图表页生成器模块
 * 包含4种不同类型的图表模板
 * - 柱状图、饼图、折线图、动画图表
 */

import pptxgen from 'pptxgenjs';
import { TemplateGenerator, Theme } from '../base';

/** 图表数据项接口 */
export interface ChartDataItem {
  /** 标签 */
  label: string;
  /** 数值 */
  value: number;
  /** 颜色（可选） */
  color?: string;
}

/** 图表数据接口 */
export interface ChartPageData {
  /** 页面标题 */
  pageTitle: string;
  /** 图表标题 */
  chartTitle?: string;
  /** 图表数据 */
  data: ChartDataItem[];
  /** 图表描述/注释 */
  description?: string;
}

/** 基础图表类 */
abstract class BaseChart {
  protected generator: TemplateGenerator;
  protected theme: Theme;

  constructor(generator: TemplateGenerator, theme: Theme) {
    this.generator = generator;
    this.theme = theme;
  }

  /** 生成图表页 */
  abstract generate(data: ChartPageData): pptxgen.Slide;

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

  /** 获取调色板 */
  protected getColors(count: number): string[] {
    const palette = [
      this.theme.primary,
      this.theme.secondary,
      this.theme.accent,
      '4CAF50',
      'FF9800',
      '9C27B0',
      '00BCD4',
      'E91E63',
    ];
    const colors: string[] = [];
    for (let i = 0; i < count; i++) {
      colors.push(palette[i % palette.length]);
    }
    return colors;
  }
}

/**
 * 柱状图页面
 * 使用pptxgenjs内置图表功能创建柱状图
 */
export class BarChart extends BaseChart {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: ChartPageData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    // 图表标题
    if (data.chartTitle) {
      this.generator.addText(slide, {
        x: 0.5,
        y: 1.1,
        w: 12,
        h: 0.5,
        text: data.chartTitle,
        fontSize: 16,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });
    }

    // 柱状图
    const chartData = [
      {
        name: '数据',
        labels: data.data.map(d => d.label),
        values: data.data.map(d => d.value),
      },
    ];

    slide.addChart(this.generator.getCharts().BAR as any, chartData, {
      x: 0.8,
      y: 1.8,
      w: 11.5,
      h: 4.8,
      barDir: 'bar',
      barGrouping: 'clustered',
      chartColors: this.getColors(data.data.length),
      showLegend: true,
      legendPos: 'b',
      legendFontSize: 10,
      showValue: true,
      dataLabelFontSize: 10,
      catAxisLabelFontSize: 10,
      catAxisLabelColor: this.theme.text,
      valAxisLabelFontSize: 9,
      valAxisLabelColor: this.theme.muted,
      plotArea: { fill: { color: 'FFFFFF' } },
      showTitle: false,
    });

    // 描述
    if (data.description) {
      this.generator.addText(slide, {
        x: 0.8,
        y: 6.8,
        w: 11.5,
        h: 0.5,
        text: data.description,
        fontSize: 10,
        fontFace: '微软雅黑',
        color: this.theme.muted,
        align: 'left',
        valign: 'middle',
      });
    }

    return slide;
  }
}

/**
 * 饼图页面
 * 使用pptxgenjs内置图表功能创建饼图
 */
export class PieChart extends BaseChart {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: ChartPageData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    // 图表标题
    if (data.chartTitle) {
      this.generator.addText(slide, {
        x: 0.5,
        y: 1.1,
        w: 12,
        h: 0.5,
        text: data.chartTitle,
        fontSize: 16,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });
    }

    // 饼图
    const chartData = [
      {
        name: '数据',
        labels: data.data.map(d => d.label),
        values: data.data.map(d => d.value),
      },
    ];

    slide.addChart(this.generator.getCharts().PIE as any, chartData, {
      x: 0.5,
      y: 1.8,
      w: 7,
      h: 5.2,
      chartColors: this.getColors(data.data.length),
      showLegend: true,
      legendPos: 'r',
      legendFontSize: 11,
      showPercent: true,
      showTitle: false,
    });

    // 右侧数据说明
    const total = data.data.reduce((sum, d) => sum + d.value, 0);
    const colors = this.getColors(data.data.length);
    const startY = 2.0;

    data.data.forEach((item, i) => {
      const y = startY + i * 0.6;
      const pct = ((item.value / total) * 100).toFixed(1);

      // 颜色方块
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: 8.2,
        y: y + 0.1,
        w: 0.3,
        h: 0.3,
        fill: { color: colors[i] },
        rectRadius: 0.03,
      });

      // 标签
      this.generator.addText(slide, {
        x: 8.7,
        y: y,
        w: 3,
        h: 0.25,
        text: item.label,
        fontSize: 12,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });

      // 数值和百分比
      this.generator.addText(slide, {
        x: 8.7,
        y: y + 0.25,
        w: 3,
        h: 0.25,
        text: `${item.value} (${pct}%)`,
        fontSize: 10,
        fontFace: 'Arial',
        color: this.theme.muted,
        align: 'left',
        valign: 'middle',
      });
    });

    // 描述
    if (data.description) {
      this.generator.addText(slide, {
        x: 0.8,
        y: 6.8,
        w: 11.5,
        h: 0.5,
        text: data.description,
        fontSize: 10,
        fontFace: '微软雅黑',
        color: this.theme.muted,
        align: 'left',
        valign: 'middle',
      });
    }

    return slide;
  }
}

/**
 * 折线图页面
 * 使用pptxgenjs内置图表功能创建折线图
 */
export class LineChart extends BaseChart {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: ChartPageData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    // 图表标题
    if (data.chartTitle) {
      this.generator.addText(slide, {
        x: 0.5,
        y: 1.1,
        w: 12,
        h: 0.5,
        text: data.chartTitle,
        fontSize: 16,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });
    }

    // 折线图
    const chartData = [
      {
        name: '趋势',
        labels: data.data.map(d => d.label),
        values: data.data.map(d => d.value),
      },
    ];

    slide.addChart(this.generator.getCharts().LINE as any, chartData, {
      x: 0.8,
      y: 1.8,
      w: 11.5,
      h: 4.5,
      lineSmooth: true,
      lineSize: 3,
      chartColors: [this.theme.primary],
      showLegend: false,
      showValue: true,
      dataLabelFontSize: 9,
      catAxisLabelFontSize: 10,
      catAxisLabelColor: this.theme.text,
      valAxisLabelFontSize: 9,
      valAxisLabelColor: this.theme.muted,
      plotArea: { fill: { color: 'FFFFFF' } },
      lineDataSymbol: 'circle',
      lineDataSymbolSize: 8,
      showTitle: false,
    });

    // 下方统计摘要
    const values = data.data.map(d => d.value);
    const max = Math.max(...values);
    const min = Math.min(...values);
    const avg = (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1);
    const maxItem = data.data.find(d => d.value === max);
    const minItem = data.data.find(d => d.value === min);

    const summaryItems = [
      { label: '最高值', value: `${max}`, detail: maxItem?.label || '' },
      { label: '最低值', value: `${min}`, detail: minItem?.label || '' },
      { label: '平均值', value: avg, detail: '' },
      { label: '数据点', value: String(data.data.length), detail: '' },
    ];

    summaryItems.forEach((item, i) => {
      const x = 0.8 + i * 3;

      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x,
        y: 6.5,
        w: 2.5,
        h: 0.8,
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

      this.generator.addText(slide, {
        x: x + 0.1,
        y: 6.5,
        w: 1,
        h: 0.35,
        text: item.label,
        fontSize: 9,
        fontFace: '微软雅黑',
        color: this.theme.muted,
        align: 'left',
        valign: 'middle',
      });

      this.generator.addText(slide, {
        x: x + 0.1,
        y: 6.8,
        w: 1.5,
        h: 0.4,
        text: item.value,
        fontSize: 18,
        fontFace: 'Arial',
        color: this.theme.primary,
        bold: true,
        align: 'left',
        valign: 'middle',
      });
    });

    // 描述
    if (data.description) {
      this.generator.addText(slide, {
        x: 11.3,
        y: 6.55,
        w: 2,
        h: 0.5,
        text: data.description,
        fontSize: 9,
        fontFace: '微软雅黑',
        color: this.theme.muted,
        align: 'right',
        valign: 'middle',
      });
    }

    return slide;
  }
}

/**
 * 动画图表页面
 * 带有渐进效果的图表展示
 */
export class AnimatedChart extends BaseChart {
  constructor(generator: TemplateGenerator, theme: Theme) {
    super(generator, theme);
  }

  generate(data: ChartPageData): pptxgen.Slide {
    const slide = this.generator.createSlide();
    const pptx = this.generator.getPresentation();

    slide.background = { fill: this.theme.background };

    // 页面标题
    this.addPageTitle(slide, data.pageTitle);

    // 图表标题
    if (data.chartTitle) {
      this.generator.addText(slide, {
        x: 0.5,
        y: 1.1,
        w: 12,
        h: 0.5,
        text: data.chartTitle,
        fontSize: 16,
        fontFace: '微软雅黑',
        color: this.theme.text,
        bold: true,
        align: 'left',
        valign: 'middle',
      });
    }

    // 手绘柱状图效果（带渐变色）
    const items = data.data;
    const maxValue = Math.max(...items.map(d => d.value));
    const chartX = 1.0;
    const chartY = 2.0;
    const chartW = 10;
    const chartH = 4.5;
    const barWidth = chartW / (items.length * 1.5);
    const gap = barWidth * 0.5;
    const colors = this.getColors(items.length);

    // 背景网格线
    for (let i = 0; i <= 5; i++) {
      const gridY = chartY + (chartH / 5) * i;
      slide.addShape(this.generator.getShapes().LINE as any, {
        x: chartX,
        y: gridY,
        w: chartW,
        h: 0,
        line: { color: this.theme.muted, width: 0.3, transparency: 70 },
      });

      // Y轴标签
      const value = Math.round(maxValue * (5 - i) / 5);
      this.generator.addText(slide, {
        x: chartX - 0.6,
        y: gridY - 0.15,
        w: 0.5,
        h: 0.3,
        text: String(value),
        fontSize: 8,
        fontFace: 'Arial',
        color: this.theme.muted,
        align: 'right',
        valign: 'middle',
      });
    }

    items.forEach((item, i) => {
      const barHeight = (item.value / maxValue) * chartH;
      const x = chartX + i * (barWidth + gap) + gap / 2;
      const y = chartY + chartH - barHeight;

      // 柱状条
      slide.addShape(this.generator.getShapes().RECTANGLE as any, {
        x: x,
        y: y,
        w: barWidth,
        h: barHeight,
        fill: { color: colors[i] },
        rectRadius: 0.05,
        shadow: {
          type: 'outer' as any,
          color: '000000',
          blur: 4,
          offset: 2,
          angle: 135,
          opacity: 0.1,
        },
      });

      // 数值标签
      this.generator.addText(slide, {
        x: x,
        y: y - 0.3,
        w: barWidth,
        h: 0.3,
        text: String(item.value),
        fontSize: 10,
        fontFace: 'Arial',
        color: this.theme.text,
        bold: true,
        align: 'center',
        valign: 'middle',
      });

      // X轴标签
      this.generator.addText(slide, {
        x: x - 0.2,
        y: chartY + chartH + 0.1,
        w: barWidth + 0.4,
        h: 0.35,
        text: item.label,
        fontSize: 9,
        fontFace: '微软雅黑',
        color: this.theme.text,
        align: 'center',
        valign: 'top',
      });
    });

    // 底部描述
    if (data.description) {
      this.generator.addText(slide, {
        x: 0.8,
        y: 6.8,
        w: 11.5,
        h: 0.5,
        text: data.description,
        fontSize: 10,
        fontFace: '微软雅黑',
        color: this.theme.muted,
        align: 'left',
        valign: 'middle',
      });
    }

    return slide;
  }
}
