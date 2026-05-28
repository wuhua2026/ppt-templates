/**
 * 快速入门示例
 * 展示如何使用PPT生成器创建一个简单的演示文稿
 *
 * 运行方式：
 *   npx ts-node examples/quick-start.ts
 */

import { TemplateGenerator, blueTechnology } from '../src';
import { GeometricRotation } from '../src/generators/cover';
import { Sidebar } from '../src/generators/directory';
import { ThreeColumn, Comparison } from '../src/generators/content';
import { Horizontal } from '../src/generators/timeline';
import { BarChart, PieChart } from '../src/generators/chart';
import { PersonCard } from '../src/generators/team';
import { ThankYou } from '../src/generators/ending';

/**
 * 主函数 - 生成示例演示文稿
 */
async function main(): Promise<void> {
  console.log('开始生成PPT...');

  // 创建生成器实例，使用蓝色科技主题
  const generator = new TemplateGenerator(blueTechnology);
  generator.setTitle('示例演示文稿');

  // 1. 封面页
  console.log('  - 生成封面页...');
  const cover = new GeometricRotation(generator, blueTechnology);
  cover.generate({
    title: '产品介绍与市场分析',
    subtitle: '2024年度汇报',
    presenter: '张三',
    date: '2024年6月',
    company: '示例科技有限公司',
  });

  // 2. 目录页
  console.log('  - 生成目录页...');
  const directory = new Sidebar(generator, blueTechnology);
  directory.generate({
    pageTitle: '目录',
    items: [
      { index: 1, title: '项目概述', description: '项目背景与目标' },
      { index: 2, title: '市场分析', description: '行业趋势与竞争格局' },
      { index: 3, title: '产品方案', description: '核心功能与技术架构' },
      { index: 4, title: '团队介绍', description: '核心成员展示' },
      { index: 5, title: '财务预测', description: '收入与支出规划' },
    ],
  });

  // 3. 内容页 - 三栏布局
  console.log('  - 生成内容页...');
  const threeCol = new ThreeColumn(generator, blueTechnology);
  threeCol.generate({
    pageTitle: '项目概述',
    blocks: [
      {
        index: 1,
        title: '项目背景',
        content: '随着数字化转型的加速，企业对智能化解决方案的需求日益增长。本项目旨在提供一站式智能办公平台。',
      },
      {
        index: 2,
        title: '项目目标',
        content: '打造行业领先的智能办公平台，帮助企业提升30%的工作效率，降低20%的运营成本。',
      },
      {
        index: 3,
        title: '核心价值',
        content: '通过AI技术和大数据分析，为企业提供智能化决策支持，实现业务流程自动化和数据驱动运营。',
      },
    ],
  });

  // 4. 内容页 - 对比布局
  console.log('  - 生成对比页...');
  const comparison = new Comparison(generator, blueTechnology);
  comparison.generate({
    pageTitle: '竞争优势分析',
    blocks: [
      {
        title: '我方方案',
        content: '- 智能化程度高\n- 用户体验优秀\n- 7x24小时服务\n- 成本效益比高\n- 定制化能力强',
      },
      {
        title: '传统方案',
        content: '- 依赖人工操作\n- 效率较低\n- 服务时间有限\n- 运维成本高\n- 标准化程度低',
      },
    ],
  });

  // 5. 时间线页
  console.log('  - 生成时间线页...');
  const timeline = new Horizontal(generator, blueTechnology);
  timeline.generate({
    pageTitle: '项目里程碑',
    items: [
      { date: '2024 Q1', title: '需求调研', description: '完成用户需求分析' },
      { date: '2024 Q2', title: '产品设计', description: '完成UI/UX设计' },
      { date: '2024 Q3', title: '开发测试', description: '核心功能开发完成' },
      { date: '2024 Q4', title: '正式上线', description: '产品正式发布' },
    ],
  });

  // 6. 图表页 - 柱状图
  console.log('  - 生成图表页...');
  const barChart = new BarChart(generator, blueTechnology);
  barChart.generate({
    pageTitle: '市场预测',
    chartTitle: '预计年度收入（万元）',
    data: [
      { label: '2024年', value: 800 },
      { label: '2025年', value: 1500 },
      { label: '2026年', value: 2800 },
      { label: '2027年', value: 4500 },
    ],
    description: '基于市场调研和业务增长预期，预计未来四年收入保持高速增长。',
  });

  // 7. 图表页 - 饼图
  console.log('  - 生成饼图页...');
  const pieChart = new PieChart(generator, blueTechnology);
  pieChart.generate({
    pageTitle: '收入结构分析',
    chartTitle: '收入来源占比',
    data: [
      { label: 'SaaS订阅', value: 45 },
      { label: '企业定制', value: 25 },
      { label: '数据服务', value: 20 },
      { label: '培训咨询', value: 10 },
    ],
  });

  // 8. 团队页
  console.log('  - 生成团队页...');
  const team = new PersonCard(generator, blueTechnology);
  team.generate({
    pageTitle: '核心团队',
    members: [
      { name: '张明', title: 'CEO', description: '10年互联网行业经验，曾任某上市公司VP' },
      { name: '李华', title: 'CTO', description: '人工智能领域专家，拥有多项技术专利' },
      { name: '王芳', title: 'CPO', description: '资深产品专家，擅长用户体验设计' },
    ],
  });

  // 9. 结束页
  console.log('  - 生成结束页...');
  const ending = new ThankYou(generator, blueTechnology);
  ending.generate({
    title: '谢谢',
    subtitle: 'Thank You',
    company: '示例科技有限公司',
  });

  // 保存文件
  console.log('保存文件中...');
  const filePath = await generator.save('示例演示文稿');
  console.log(`演示文稿已生成: ${filePath}`);
  console.log('完成！');
}

// 执行
main().catch(err => {
  console.error('生成失败:', err);
  process.exit(1);
});
