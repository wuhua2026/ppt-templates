/**
 * 完整演示文稿组装器模块
 * 包含6种预设的完整演示文稿模板
 * - 商业计划、职业规划、产品发布、年度报告、教育课程、科技主题
 */

import { TemplateGenerator, Theme } from '../base';
import { blueTechnology, purpleGradient, darkGold, minimalistBW, oceanBlue, greenNature, redBusiness } from '../themes';
import { GeometricRotation, CircleRing, MinimalistGradient, SplitScreen } from './cover';
import { CardGrid, Sidebar, DiamondAnimated } from './directory';
import { TextImageLayout, ThreeColumn, FourGrid, Comparison, FullImageOverlay } from './content';
import { Horizontal, Vertical, DualWave, TimelineData, TimelineItem } from './timeline';
import { BarChart, PieChart, LineChart, ChartPageData, ChartDataItem } from './chart';
import { PersonCard, TeamGrid, TeamData, TeamMember } from './team';
import { ThankYou, Contact, EndingData } from './ending';
import { CoverData } from './cover';
import { DirectoryData, DirectoryItem } from './directory';
import { ContentData, ContentBlock } from './content';

/** 完整演示文稿配置接口 */
export interface DeckConfig {
  /** 演示文稿标题 */
  title: string;
  /** 副标题 */
  subtitle?: string;
  /** 作者/演讲者 */
  presenter?: string;
  /** 日期 */
  date?: string;
  /** 公司名称 */
  company?: string;
  /** 主题 */
  theme?: Theme;
  /** 自定义数据 */
  customData?: Record<string, any>;
}

/**
 * 基础完整演示文稿组装器
 * 提供通用的构建流程
 */
abstract class BaseCompleteDeck {
  protected config: DeckConfig;
  protected generator: TemplateGenerator;
  protected theme: Theme;

  constructor(config: DeckConfig) {
    this.theme = config.theme || blueTechnology;
    this.generator = new TemplateGenerator(this.theme);
    this.config = config;
  }

  /** 生成完整的演示文稿 */
  async generate(): Promise<void> {
    this.generator.setTitle(this.config.title);
    await this.addCover();
    await this.addDirectory();
    await this.addContent();
    await this.addTimeline();
    await this.addCharts();
    await this.addTeam();
    await this.addEnding();
  }

  /** 保存文件 */
  async save(fileName: string): Promise<string> {
    return this.generator.save(fileName);
  }

  /** 获取生成器实例 */
  getGenerator(): TemplateGenerator {
    return this.generator;
  }

  protected abstract addCover(): Promise<void>;
  protected abstract addDirectory(): Promise<void>;
  protected abstract addContent(): Promise<void>;
  protected abstract addTimeline(): Promise<void>;
  protected abstract addCharts(): Promise<void>;
  protected abstract addTeam(): Promise<void>;
  protected abstract addEnding(): Promise<void>;
}

/**
 * 商业计划演示文稿
 * 包含：封面、目录、市场分析、商业模式、团队介绍、财务预测、联系方式
 */
export class BusinessPlan extends BaseCompleteDeck {
  constructor(config: DeckConfig) {
    super({ ...config, theme: config.theme || blueTechnology });
  }

  protected async addCover(): Promise<void> {
    const cover = new GeometricRotation(this.generator, this.theme);
    cover.generate({
      title: this.config.title,
      subtitle: this.config.subtitle || '商业计划书',
      presenter: this.config.presenter,
      date: this.config.date,
      company: this.config.company,
    });
  }

  protected async addDirectory(): Promise<void> {
    const dir = new Sidebar(this.generator, this.theme);
    dir.generate({
      pageTitle: '目录',
      items: [
        { index: 1, title: '项目概述', description: '项目背景与愿景' },
        { index: 2, title: '市场分析', description: '行业趋势与竞争格局' },
        { index: 3, title: '商业模式', description: '盈利模式与价值主张' },
        { index: 4, title: '团队介绍', description: '核心团队成员' },
        { index: 5, title: '财务预测', description: '收入与支出预测' },
        { index: 6, title: '发展规划', description: '未来三年规划' },
      ],
    });
  }

  protected async addContent(): Promise<void> {
    // 市场分析 - 三栏布局
    const threeCol = new ThreeColumn(this.generator, this.theme);
    threeCol.generate({
      pageTitle: '市场分析',
      blocks: [
        { index: 1, title: '市场规模', content: '目标市场规模预计在2025年达到500亿元，年均增长率达到25%。随着技术进步和消费升级，市场潜力巨大。' },
        { index: 2, title: '竞争格局', content: '当前市场竞争格局分散，头部企业占比不足20%。差异化竞争策略将是关键成功因素。' },
        { index: 3, title: '用户需求', content: '用户对产品品质和服务体验的要求不断提升，个性化和智能化成为主要需求方向。' },
      ],
    });

    // 商业模式 - 图文混排
    const textImage = new TextImageLayout(this.generator, this.theme);
    textImage.generate({
      pageTitle: '商业模式',
      blocks: [
        {
          title: '核心价值主张',
          content: '我们通过创新技术手段，为用户提供高效、便捷、智能的解决方案。以用户需求为导向，持续优化产品体验，建立长期价值。我们的商业模式建立在技术创新和用户体验的双重驱动之上，通过SaaS订阅模式实现可持续收入增长。',
        },
      ],
    });

    // 竞争对比
    const comparison = new Comparison(this.generator, this.theme);
    comparison.generate({
      pageTitle: '竞争优势',
      blocks: [
        { title: '我方优势', content: '- 技术领先，拥有核心专利\n- 用户体验优秀，满意度95%\n- 团队经验丰富，执行力强\n- 成本控制良好，利润率高\n- 生态布局完整，壁垒高' },
        { title: '竞品劣势', content: '- 技术更新缓慢，创新不足\n- 用户体验一般，投诉率高\n- 团队不稳定，人员流动大\n- 成本结构不合理\n- 市场定位模糊' },
      ],
    });
  }

  protected async addTimeline(): Promise<void> {
    const timeline = new Horizontal(this.generator, this.theme);
    timeline.generate({
      pageTitle: '发展规划',
      items: [
        { date: '2024 Q1', title: '产品发布', description: '完成产品开发并正式上线' },
        { date: '2024 Q3', title: '市场拓展', description: '进入主要目标市场' },
        { date: '2025 Q1', title: '用户增长', description: '达到10万用户里程碑' },
        { date: '2025 Q3', title: '盈利目标', description: '实现盈亏平衡' },
        { date: '2026 Q1', title: '规模扩张', description: '进入国际市场' },
      ],
    });
  }

  protected async addCharts(): Promise<void> {
    // 财务预测 - 柱状图
    const barChart = new BarChart(this.generator, this.theme);
    barChart.generate({
      pageTitle: '财务预测',
      chartTitle: '年度收入预测（万元）',
      data: [
        { label: '2024年', value: 500 },
        { label: '2025年', value: 1200 },
        { label: '2026年', value: 3000 },
        { label: '2027年', value: 5500 },
      ],
      description: '基于当前市场趋势和业务增长预期，预计未来四年收入将保持高速增长。',
    });

    // 收入结构 - 饼图
    const pieChart = new PieChart(this.generator, this.theme);
    pieChart.generate({
      pageTitle: '收入结构',
      chartTitle: '预计收入来源占比',
      data: [
        { label: 'SaaS订阅', value: 45 },
        { label: '企业定制', value: 25 },
        { label: '数据服务', value: 20 },
        { label: '培训咨询', value: 10 },
      ],
    });
  }

  protected async addTeam(): Promise<void> {
    const team = new PersonCard(this.generator, this.theme);
    team.generate({
      pageTitle: '核心团队',
      members: [
        { name: '张明', title: 'CEO / 创始人', description: '10年互联网行业经验，曾任某上市公司VP' },
        { name: '李华', title: 'CTO', description: '人工智能领域专家，拥有多项技术专利' },
        { name: '王芳', title: 'COO', description: '资深运营管理专家，擅长企业战略规划' },
      ],
    });
  }

  protected async addEnding(): Promise<void> {
    const contact = new Contact(this.generator, this.theme);
    contact.generate({
      title: '联系我们',
      subtitle: '期待与您的合作',
      company: this.config.company || '示例公司',
      email: 'contact@example.com',
      phone: '400-888-8888',
      website: 'www.example.com',
      address: '北京市朝阳区示例大厦',
    });
  }
}

/**
 * 职业规划演示文稿
 */
export class CareerPlanning extends BaseCompleteDeck {
  constructor(config: DeckConfig) {
    super({ ...config, theme: config.theme || purpleGradient });
  }

  protected async addCover(): Promise<void> {
    const cover = new CircleRing(this.generator, this.theme);
    cover.generate({
      title: this.config.title,
      subtitle: this.config.subtitle || '我的职业规划',
      presenter: this.config.presenter,
      date: this.config.date,
    });
  }

  protected async addDirectory(): Promise<void> {
    const dir = new DiamondAnimated(this.generator, this.theme);
    dir.generate({
      pageTitle: '目录',
      items: [
        { index: 1, title: '自我分析', description: '性格与能力评估' },
        { index: 2, title: '职业目标', description: '短期与长期目标' },
        { index: 3, title: '行动计划', description: '具体实施步骤' },
        { index: 4, title: '评估调整', description: '定期复盘与修正' },
      ],
    });
  }

  protected async addContent(): Promise<void> {
    const fourGrid = new FourGrid(this.generator, this.theme);
    fourGrid.generate({
      pageTitle: '自我分析',
      blocks: [
        { index: 1, title: '性格特点', content: '外向型性格，善于沟通协调，具有较强的领导力和团队协作能力。' },
        { index: 2, title: '专业技能', content: '计算机科学专业背景，掌握编程语言和数据分析能力。' },
        { index: 3, title: '兴趣爱好', content: '对人工智能和新兴技术有浓厚兴趣，热衷于技术创新。' },
        { index: 4, title: '价值观念', content: '追求工作与生活的平衡，重视个人成长和社会贡献。' },
      ],
    });
  }

  protected async addTimeline(): Promise<void> {
    const timeline = new DualWave(this.generator, this.theme);
    timeline.generate({
      pageTitle: '职业发展路径',
      items: [
        { date: '第1年', title: '初级工程师', description: '积累项目经验' },
        { date: '第3年', title: '高级工程师', description: '技术深耕' },
        { date: '第5年', title: '技术主管', description: '带领团队' },
        { date: '第8年', title: '技术总监', description: '战略规划' },
        { date: '第10年', title: 'CTO', description: '技术决策' },
      ],
    });
  }

  protected async addCharts(): Promise<void> {
    const chart = new BarChart(this.generator, this.theme);
    chart.generate({
      pageTitle: '能力评估',
      chartTitle: '核心能力评分（满分10分）',
      data: [
        { label: '编程能力', value: 8 },
        { label: '沟通能力', value: 9 },
        { label: '领导力', value: 7 },
        { label: '创新思维', value: 8 },
        { label: '抗压能力', value: 7 },
      ],
    });
  }

  protected async addTeam(): Promise<void> {
    const team = new TeamGrid(this.generator, this.theme);
    team.generate({
      pageTitle: '导师与榜样',
      members: [
        { name: '陈教授', title: '学术导师', description: '计算机学院教授' },
        { name: '刘总', title: '行业导师', description: '某科技公司CTO' },
        { name: '张学长', title: '职业榜样', description: '成功创业者' },
      ],
    });
  }

  protected async addEnding(): Promise<void> {
    const thankYou = new ThankYou(this.generator, this.theme);
    thankYou.generate({
      title: '感谢聆听',
      subtitle: '我的未来，我做主',
      company: this.config.presenter || '演讲者',
    });
  }
}

/**
 * 产品发布演示文稿
 */
export class ProductLaunch extends BaseCompleteDeck {
  constructor(config: DeckConfig) {
    super({ ...config, theme: config.theme || redBusiness });
  }

  protected async addCover(): Promise<void> {
    const cover = new MinimalistGradient(this.generator, this.theme);
    cover.generate({
      title: this.config.title,
      subtitle: this.config.subtitle || '全新产品发布会',
      presenter: this.config.presenter,
      date: this.config.date,
      company: this.config.company,
    });
  }

  protected async addDirectory(): Promise<void> {
    const dir = new CardGrid(this.generator, this.theme);
    dir.generate({
      pageTitle: '发布议程',
      items: [
        { index: 1, title: '产品理念', description: '为什么做这个产品' },
        { index: 2, title: '核心功能', description: '产品亮点展示' },
        { index: 3, title: '技术架构', description: '底层技术揭秘' },
        { index: 4, title: '用户案例', description: '真实使用场景' },
        { index: 5, title: '价格方案', description: '定价与套餐' },
      ],
    });
  }

  protected async addContent(): Promise<void> {
    const fullImage = new FullImageOverlay(this.generator, this.theme);
    fullImage.generate({
      pageTitle: '产品理念',
      mainText: '我们相信科技应该让生活更简单。这款产品从用户痛点出发，通过创新设计和先进技术，打造极致的使用体验。',
    });

    const threeCol = new ThreeColumn(this.generator, this.theme);
    threeCol.generate({
      pageTitle: '核心功能',
      blocks: [
        { index: 1, title: '智能推荐', content: '基于AI算法，为用户提供个性化的内容推荐，准确率达到95%以上。' },
        { index: 2, title: '实时协作', content: '支持多人实时协作编辑，延迟低于100毫秒，提升团队效率。' },
        { index: 3, title: '数据分析', content: '强大的数据可视化工具，帮助用户快速洞察数据价值。' },
      ],
    });
  }

  protected async addTimeline(): Promise<void> {
    const timeline = new Vertical(this.generator, this.theme);
    timeline.generate({
      pageTitle: '发布计划',
      items: [
        { date: '2024.01', title: '内测阶段', description: '邀请500名用户参与内测' },
        { date: '2024.03', title: '公测阶段', description: '开放注册，收集反馈' },
        { date: '2024.06', title: '正式发布', description: '全渠道上线' },
        { date: '2024.09', title: '版本迭代', description: '推出2.0版本' },
      ],
    });
  }

  protected async addCharts(): Promise<void> {
    const pieChart = new PieChart(this.generator, this.theme);
    pieChart.generate({
      pageTitle: '目标用户分布',
      chartTitle: '用户群体占比',
      data: [
        { label: '个人用户', value: 40 },
        { label: '中小企业', value: 35 },
        { label: '大型企业', value: 20 },
        { label: '政府机构', value: 5 },
      ],
    });
  }

  protected async addTeam(): Promise<void> {
    const team = new PersonCard(this.generator, this.theme);
    team.generate({
      pageTitle: '产品团队',
      members: [
        { name: '赵强', title: '产品负责人', description: '10年产品设计经验' },
        { name: '周敏', title: '技术负责人', description: '全栈工程师，架构师' },
        { name: '吴静', title: '设计负责人', description: 'UI/UX设计专家' },
      ],
    });
  }

  protected async addEnding(): Promise<void> {
    const thankYou = new ThankYou(this.generator, this.theme);
    thankYou.generate({
      title: '即刻体验',
      subtitle: 'www.product-example.com',
      company: this.config.company || '产品公司',
    });
  }
}

/**
 * 年度报告演示文稿
 */
export class AnnualReport extends BaseCompleteDeck {
  constructor(config: DeckConfig) {
    super({ ...config, theme: config.theme || darkGold });
  }

  protected async addCover(): Promise<void> {
    const cover = new SplitScreen(this.generator, this.theme);
    cover.generate({
      title: this.config.title,
      subtitle: this.config.subtitle || '2024年度报告',
      presenter: this.config.presenter,
      date: this.config.date,
      company: this.config.company,
    });
  }

  protected async addDirectory(): Promise<void> {
    const dir = new Sidebar(this.generator, this.theme);
    dir.generate({
      pageTitle: '年度回顾',
      items: [
        { index: 1, title: '业绩概览', description: '关键业绩指标' },
        { index: 2, title: '业务分析', description: '各业务线表现' },
        { index: 3, title: '团队发展', description: '人才建设成果' },
        { index: 4, title: '未来展望', description: '新年战略规划' },
      ],
    });
  }

  protected async addContent(): Promise<void> {
    const fourGrid = new FourGrid(this.generator, this.theme);
    fourGrid.generate({
      pageTitle: '业绩概览',
      blocks: [
        { index: 1, title: '营业收入', content: '全年实现营业收入12.5亿元，同比增长35%，超额完成年初制定的增长目标。' },
        { index: 2, title: '净利润', content: '全年净利润2.8亿元，利润率达到22.4%，较去年提升3个百分点。' },
        { index: 3, title: '用户规模', content: '注册用户突破500万，月活跃用户达到150万，用户留存率85%。' },
        { index: 4, title: '市场份额', content: '国内市场占有率达到15%，较去年提升5个百分点，稳居行业前三。' },
      ],
    });
  }

  protected async addTimeline(): Promise<void> {
    const timeline = new Horizontal(this.generator, this.theme);
    timeline.generate({
      pageTitle: '年度里程碑',
      items: [
        { date: 'Q1', title: '融资完成', description: '完成B轮融资2亿元' },
        { date: 'Q2', title: '产品升级', description: '3.0版本发布' },
        { date: 'Q3', title: '市场突破', description: '进入海外市场' },
        { date: 'Q4', title: '战略合作', description: '与头部企业达成合作' },
      ],
    });
  }

  protected async addCharts(): Promise<void> {
    const lineChart = new LineChart(this.generator, this.theme);
    lineChart.generate({
      pageTitle: '增长趋势',
      chartTitle: '月度收入增长趋势（万元）',
      data: [
        { label: '1月', value: 800 },
        { label: '3月', value: 950 },
        { label: '5月', value: 1100 },
        { label: '7月', value: 1050 },
        { label: '9月', value: 1200 },
        { label: '11月', value: 1350 },
        { label: '12月', value: 1500 },
      ],
      description: '全年收入保持稳定增长态势，下半年加速明显。',
    });
  }

  protected async addTeam(): Promise<void> {
    const team = new TeamGrid(this.generator, this.theme);
    team.generate({
      pageTitle: '管理团队',
      members: [
        { name: '孙总', title: 'CEO', description: '公司创始人' },
        { name: '钱总', title: 'CFO', description: '财务管理专家' },
        { name: '郑总', title: 'CMO', description: '市场营销专家' },
        { name: '冯总', title: 'CTO', description: '技术负责人' },
      ],
    });
  }

  protected async addEnding(): Promise<void> {
    const thankYou = new ThankYou(this.generator, this.theme);
    thankYou.generate({
      title: '砥砺前行',
      subtitle: '共创辉煌2025',
      company: this.config.company || '示例公司',
    });
  }
}

/**
 * 教育课程演示文稿
 */
export class EducationCourse extends BaseCompleteDeck {
  constructor(config: DeckConfig) {
    super({ ...config, theme: config.theme || greenNature });
  }

  protected async addCover(): Promise<void> {
    const cover = new MinimalistGradient(this.generator, this.theme);
    cover.generate({
      title: this.config.title,
      subtitle: this.config.subtitle || '课程介绍',
      presenter: this.config.presenter,
      date: this.config.date,
      company: this.config.company,
    });
  }

  protected async addDirectory(): Promise<void> {
    const dir = new DiamondAnimated(this.generator, this.theme);
    dir.generate({
      pageTitle: '课程大纲',
      items: [
        { index: 1, title: '课程简介', description: '课程目标与内容概览' },
        { index: 2, title: '知识体系', description: '核心知识点梳理' },
        { index: 3, title: '实践案例', description: '真实项目案例分析' },
        { index: 4, title: '学习路径', description: '推荐学习进度' },
        { index: 5, title: '考核方式', description: '评估标准说明' },
      ],
    });
  }

  protected async addContent(): Promise<void> {
    const threeCol = new ThreeColumn(this.generator, this.theme);
    threeCol.generate({
      pageTitle: '知识体系',
      blocks: [
        { index: 1, title: '基础理论', content: '系统讲解核心概念和基本原理，建立扎实的理论基础。包括基本定义、发展历史和应用场景。' },
        { index: 2, title: '技术方法', content: '深入介绍关键技术方法和工具使用，培养实际操作能力。包含主流框架和最佳实践。' },
        { index: 3, title: '项目实战', content: '通过真实项目案例，综合运用所学知识解决实际问题。包含完整项目开发流程。' },
      ],
    });

    const comparison = new Comparison(this.generator, this.theme);
    comparison.generate({
      pageTitle: '课程特色',
      blocks: [
        { title: '传统课程', content: '- 理论为主，缺少实践\n- 内容更新缓慢\n- 单向讲授，互动少\n- 统一进度，不个性化\n- 考核方式单一' },
        { title: '本课程', content: '- 理论与实践并重\n- 每月更新内容\n- 互动式教学\n- 个性化学习路径\n- 多维度评估' },
      ],
    });
  }

  protected async addTimeline(): Promise<void> {
    const timeline = new DualWave(this.generator, this.theme);
    timeline.generate({
      pageTitle: '学习路径',
      items: [
        { date: '第1-2周', title: '入门阶段', description: '基础知识学习' },
        { date: '第3-4周', title: '进阶阶段', description: '核心技术掌握' },
        { date: '第5-6周', title: '实战阶段', description: '项目动手实践' },
        { date: '第7-8周', title: '总结阶段', description: '知识体系整合' },
      ],
    });
  }

  protected async addCharts(): Promise<void> {
    const chart = new BarChart(this.generator, this.theme);
    chart.generate({
      pageTitle: '学习效果',
      chartTitle: '往期学员能力提升幅度（%）',
      data: [
        { label: '理论知识', value: 85 },
        { label: '实操能力', value: 90 },
        { label: '项目经验', value: 75 },
        { label: '就业竞争力', value: 88 },
      ],
    });
  }

  protected async addTeam(): Promise<void> {
    const team = new PersonCard(this.generator, this.theme);
    team.generate({
      pageTitle: '师资团队',
      members: [
        { name: '王教授', title: '主讲教师', description: '清华大学教授，20年教学经验' },
        { name: '刘工程师', title: '实践导师', description: '资深架构师，主导多个大型项目' },
        { name: '陈博士', title: '助教', description: '博士研究员，学术功底扎实' },
      ],
    });
  }

  protected async addEnding(): Promise<void> {
    const thankYou = new ThankYou(this.generator, this.theme);
    thankYou.generate({
      title: '加入我们',
      subtitle: '开启你的学习之旅',
      company: this.config.company || '教育机构',
    });
  }
}

/**
 * 科技主题演示文稿
 */
export class TechnologyTheme extends BaseCompleteDeck {
  constructor(config: DeckConfig) {
    super({ ...config, theme: config.theme || oceanBlue });
  }

  protected async addCover(): Promise<void> {
    const cover = new CircleRing(this.generator, this.theme);
    cover.generate({
      title: this.config.title,
      subtitle: this.config.subtitle || '技术创新分享',
      presenter: this.config.presenter,
      date: this.config.date,
      company: this.config.company,
    });
  }

  protected async addDirectory(): Promise<void> {
    const dir = new CardGrid(this.generator, this.theme);
    dir.generate({
      pageTitle: '内容导航',
      items: [
        { index: 1, title: '技术趋势', description: '行业前沿技术动态' },
        { index: 2, title: '架构设计', description: '系统架构最佳实践' },
        { index: 3, title: '性能优化', description: '性能调优方法论' },
        { index: 4, title: '安全防护', description: '网络安全体系建设' },
        { index: 5, title: '未来展望', description: '技术发展方向' },
      ],
    });
  }

  protected async addContent(): Promise<void> {
    const textImage = new TextImageLayout(this.generator, this.theme);
    textImage.generate({
      pageTitle: '技术趋势',
      blocks: [
        {
          title: '人工智能与大模型',
          content: '大语言模型正在重塑软件开发范式。从代码生成到智能调试，AI辅助开发工具正在大幅提升开发效率。预计到2025年，超过80%的开发工作将涉及AI辅助工具的使用。',
        },
      ],
    });

    const threeCol = new ThreeColumn(this.generator, this.theme);
    threeCol.generate({
      pageTitle: '架构设计原则',
      blocks: [
        { index: 1, title: '微服务架构', content: '采用微服务架构，实现服务解耦和独立部署。通过容器化和Kubernetes编排，实现弹性伸缩。' },
        { index: 2, title: '事件驱动', content: '使用事件驱动架构处理异步任务，通过消息队列实现服务间的松耦合通信。' },
        { index: 3, title: '云原生', content: '全面拥抱云原生技术栈，包括容器化、服务网格、声明式API等。' },
      ],
    });
  }

  protected async addTimeline(): Promise<void> {
    const timeline = new Vertical(this.generator, this.theme);
    timeline.generate({
      pageTitle: '技术演进路线',
      items: [
        { date: 'Phase 1', title: '单体架构', description: '快速原型验证', highlight: false },
        { date: 'Phase 2', title: '服务拆分', description: '核心服务独立', highlight: false },
        { date: 'Phase 3', title: '微服务', description: '全面微服务化', highlight: true },
        { date: 'Phase 4', title: '云原生', description: '容器化与编排', highlight: false },
        { date: 'Phase 5', title: '智能运维', description: 'AIOps实践', highlight: false },
      ],
    });
  }

  protected async addCharts(): Promise<void> {
    const lineChart = new LineChart(this.generator, this.theme);
    lineChart.generate({
      pageTitle: '性能指标',
      chartTitle: '系统响应时间趋势（ms）',
      data: [
        { label: 'v1.0', value: 500 },
        { label: 'v1.5', value: 350 },
        { label: 'v2.0', value: 200 },
        { label: 'v2.5', value: 120 },
        { label: 'v3.0', value: 80 },
        { label: 'v3.5', value: 50 },
      ],
      description: '通过持续优化，系统响应时间降低了90%。',
    });
  }

  protected async addTeam(): Promise<void> {
    const team = new TeamGrid(this.generator, this.theme);
    team.generate({
      pageTitle: '技术团队',
      members: [
        { name: '林工', title: '首席架构师', description: '分布式系统专家' },
        { name: '黄工', title: 'AI负责人', description: '机器学习专家' },
        { name: '杨工', title: '安全负责人', description: '网络安全专家' },
        { name: '马工', title: '运维负责人', description: 'DevOps专家' },
      ],
    });
  }

  protected async addEnding(): Promise<void> {
    const contact = new Contact(this.generator, this.theme);
    contact.generate({
      title: '技术交流',
      subtitle: '欢迎探讨技术问题',
      company: this.config.company || '技术团队',
      email: 'tech@example.com',
      website: 'github.com/example',
    });
  }
}
