# Agent Fiverr 计划草案

研究日期：2026-05-06

## 1. 结论摘要

“覆盖所有 Fiverr 服务”可行，但不能理解为“所有服务都由 AI 完全自动交付”。更合理的定义是：每个服务都有一个 agent 化 storefront/workspace，负责获客问诊、报价、需求澄清、计划、交付物生成、质量检查、修订和归档；其中一部分服务可完全自动化，一部分需要工具链，一部分必须保留人类专家或线下履约。

Fiverr 官方目前覆盖 Graphics & Design、Programming & Tech、Digital Marketing、Video & Animation、Writing & Translation、Music & Audio、Business、Finance、AI Services、Personal Growth、Consulting、Data、Photography、End-to-End Projects 等大类，并称平台有 750+ skilled categories。Fiverr 自己也已经在做 Fiverr Go 和 AI-native 转型，所以差异化不能只做“AI 生成”，而要做“可验收、可追责、可复用工作流”的服务 agent 市场。

推荐策略：先做 20 个高频、高可验收、数字化交付的服务 agent，建立统一服务规格、评测、工单、交付和风控系统；然后用 taxonomy generator 扩展到长尾服务；对线下、强监管、高情感风险服务采用 agent + human / agent broker 模式覆盖。

## 2. 参考模板观察

附件 `/Users/monster/Downloads/agent-template.tar.gz` 不是普通代码模板，而是一个“人格化 agent workspace”：

- `IDENTITY.md` / `SOUL.md` / `OWNER.md`：定义 agent 身份、边界、owner 关系和信任模型。
- `MEMORY.md` / `memory/`：支持长期记忆和用户偏好沉淀。
- `HEARTBEAT.md`：支持定期检查、跟进和主动触发。
- `skills/bloome`：支持 widget、document、data table、profile、conversation、delegate、cron 等 IM 原生能力。
- `skills/bloome-playbook`：包含结构化输出、自动化 webhook、多 agent 协作、记忆、分享、生命周期等产品能力说明。

这套模板适合改造成“每个服务一个工作空间”的 agent 标准包。缺的不是基础人格，而是服务交易需要的模块：服务规格、报价、权限、工具清单、交付物 schema、质量评测、安全策略、修订协议、争议处理。

建议新增标准文件：

```text
SERVICE.md              # 服务定义、目标客户、范围、非范围
BRIEF_SCHEMA.json       # 买家需求输入结构
DELIVERABLE_SCHEMA.json # 交付物结构
QUOTE_RULES.md          # 报价、套餐、SLA、加急规则
QA_RUBRIC.md            # 质量评分标准
EVALS.md                # 样例任务、golden output、自动评测
TOOLS.md                # 可用工具、权限、外部账号授权
POLICY.md               # 禁止事项、高风险升级、人审条件
REVISION.md             # 修订次数、变更边界、重新报价条件
HANDOFF.md              # 需要人类专家/其他 agent 时的交接协议
```

## 3. Fiverr 服务的 agent 化任务类型

| 任务类型 | 典型 Fiverr 服务 | Agent 化方式 | 可行性 |
|---|---|---|---|
| 文本生成与编辑 | blog、copywriting、resume、press release、script、translation | LLM + 风格/事实检查 + plagiarism/SEO 检查 | 高 |
| 设计与图像 | logo、social posts、book cover、AI image editing、presentation design | 生成/编辑工具 + brand kit + 人审 | 中高 |
| 代码与技术 | website、bug fix、automation、API、AI agent、chatbot、DevOps | coding agent + repo sandbox + test runner + deploy gate | 高，但需测试和权限控制 |
| 数据工作 | data entry、cleaning、scraping、dashboard、analytics、ML | ETL 工具 + notebook + schema validator + dashboard | 高 |
| 数字营销 | SEO、SEM、email、social calendar、CRO、GEO、campaign management | audit + content + campaign draft；投放动作需授权 | 中高 |
| 视频与动画 | editing、captions、repurposing、UGC script、AI video、explainer | 生成/剪辑工具 + storyboard + render QA | 中 |
| 音频与音乐 | voiceover、podcast、audio editing、jingle、TTS | 音频模型 + loudness/format QA；原创音乐需版权策略 | 中 |
| 商业与咨询 | market research、business plan、pitch deck、PM、VA | research + doc/deck + checklist；战略结论需人审 | 中 |
| 金融/法务/税务 | bookkeeping、tax、legal docs、financial model、valuation | agent 起草/检查；必须免责声明和专家复核 | 低到中 |
| 摄影/线下服务 | product photo、event photo、real estate photo、drone | agent 负责 brief、shot list、供应商调度、后期 | 低，需人/线下履约 |
| 个人成长/健康 | tutoring、fitness、nutrition、life coaching、career | agent 可做教练/计划；健康、心理、法律边界严格 | 中低 |
| End-to-End Projects | app build、brand launch、book launch、video campaign | orchestrator agent + 多 agent + PM + QA + 人类专家 | 中高 |

## 4. 可行性分层

L5：纯 agent 可交付。例：摘要、翻译初稿、SEO audit、data cleaning、dashboard prototype、resume rewrite、presentation draft、caption/subtitle。

L4：agent 主导，人审后交付。例：品牌文案、营销 campaign、logo concepts、视频剪辑、landing page、market research、financial model draft。

L3：agent + 工具 + 客户授权。例：投放广告、部署网站、CRM 自动化、邮件营销、爬虫、社媒发布、GitHub PR。

L2：agent 协调人类专家。例：法律、税务、医疗/营养、复杂财务、网络安全、建筑/工程、专业咨询。

L1：agent broker/concierge。例：摄影、现场活动、建模表演、旅行/签证提交、线下采购和运输。agent 负责需求、匹配、计划、验收，不直接完成核心履约。

## 5. 产品架构

核心不是“一个超级 agent”，而是三层系统：

1. Marketplace Orchestrator：买家入口、需求澄清、服务匹配、报价、支付/托管、状态追踪、争议处理。
2. Service Agent Workspace：每个服务一个 workspace，包含身份、技能、工具、交付物 schema、质量标准、记忆和修订策略。
3. Fulfillment Graph：按任务动态编排 planner、worker、critic、compliance、delivery、human expert。

每个订单建议固定生命周期：

```text
Intake -> Scope Check -> Quote -> Plan -> Work -> QA -> Delivery -> Revision -> Close -> Memory
```

关键产品对象：

- Service Spec：服务卡，声明输入、输出、价格、SLA、边界。
- Brief：结构化需求表，避免开放式聊天反复问。
- Workroom：订单上下文、文件、权限、进度和交付物。
- Deliverable：可下载文件、文档、widget、代码仓库、表格、视频、音频等。
- Eval Pack：每个服务的自动/人工验收标准。
- Trust Ledger：工具调用、外部发布、授权、审计日志。

## 6. MVP 服务优先级

第一批不要追求全量，先选“高频、数字化、可验收、低监管”的 20 个：

1. SEO / GEO audit agent
2. Blog & article writer
3. Resume / LinkedIn profile agent
4. Translation & localization agent
5. Social media calendar agent
6. Email marketing copy agent
7. Landing page copy + wireframe agent
8. Presentation / pitch deck agent
9. Market research brief agent
10. Data cleaning & formatting agent
11. Data scraping + enrichment agent
12. Dashboard prototype agent
13. Website bug fix agent
14. WordPress / Shopify small task agent
15. API integration / automation agent
16. AI chatbot / AI agent builder
17. Logo concept / brand kit draft agent
18. Product image editing agent
19. Video caption + repurpose agent
20. Podcast show notes + audio cleanup agent

第二批扩展到更复杂的多 agent 项目：MVP app build、brand launch、book launch、e-commerce setup、paid ads、DevOps deployment、financial model、legal document draft。

第三批覆盖长尾和线下：摄影、活动、旅行、建模、实体制作，以 agent broker + 人类供应网络方式完成。

## 7. 执行路线图

### Phase 0：分类和规格化，1-2 周

- 抓取/维护 Fiverr 服务 taxonomy。
- 建立 `service_spec` schema。
- 把所有服务映射到任务类型、可行性层级、风险等级、所需工具。
- 产出 20 个 MVP 服务 spec。

验收：

- 覆盖 100% 顶层类目。
- 至少 80% 子类目完成 archetype 映射。
- 每个 MVP 服务都有 brief schema、deliverable schema、QA rubric、policy。

### Phase 1：Agent Workspace 标准包，2-3 周

- 基于附件模板扩展服务 workspace。
- 实现订单生命周期和状态机。
- 实现工具权限、审计日志、交付物版本、修订协议。
- 实现文档/表格/widget 三类结构化交付。

验收：

- 任意服务可通过模板一键生成 workspace。
- 每个 workspace 可运行 5 个 golden sample。
- 工具调用有可追溯日志；外部副作用必须显式授权。

### Phase 2：20 个 MVP agent，4-6 周

- 每个服务构建 10-20 个样例订单。
- 建立自动评测 + 人工评审闭环。
- 做订单页、买家 brief、交付页、修订入口。

验收：

- 20 个 agent 每个至少通过 10 个样例订单。
- 首次交付达标率 >= 80%。
- 自动完成率 >= 60%。
- 严重质量/安全事故为 0。

### Phase 3：Marketplace Alpha，4 周

- 上线买家入口、服务目录、报价、支付/托管、订单状态。
- 引入人工 QA 池和专家接管机制。
- 做真实客户小流量测试。

验收：

- 100 个真实订单。
- 订单取消率 < 10%。
- 退款率 < 5%。
- 平均首次响应 < 2 分钟。
- 数字类 MVP 任务平均交付时间比传统 freelancer 缩短 50% 以上。

### Phase 4：长尾扩展，持续

- 用 taxonomy generator 批量生成服务 agent 草稿。
- 按需求和失败率排序扩展。
- 对高风险类目强制专家认证和人审。

验收：

- 500+ 服务 spec 覆盖。
- 100+ 可售卖 agent。
- 每个新 agent 上架前必须通过最低 eval pack。

## 8. 统一验收标准

### 服务级验收

- Scope：明确服务包含/不包含什么。
- Inputs：brief 字段完整，缺失信息能自动追问。
- Output：交付物符合 schema，可下载/可复用。
- Quality：达到 rubrics，低于阈值不得交付。
- Revision：能区分免费修订和范围变更。
- Safety：高风险场景自动升级人审。
- Traceability：能回放订单、工具调用、文件版本和决策。

### 平台级验收

- 覆盖率：顶层类目 100%，MVP 子类目 100%，长尾逐步扩展。
- 成功率：MVP 首次达标 >= 80%，修订后达标 >= 92%。
- 自动化率：L5 服务 >= 85%，L4 服务 >= 60%，L3 服务视授权而定。
- 成本：单次 agent 成本低于对应服务售价的 20%-30%。
- 时效：报价 < 2 分钟，标准数字服务首稿 < 1 小时或 < 24 小时。
- 信任：所有外部发布、转账、广告投放、邮件发送、生产部署必须二次确认。
- 合规：法律、金融、医疗、税务、心理健康不得伪装成持牌专业意见。

## 9. 主要风险

1. 质量不稳定：需要服务级 eval，而不是泛泛“看起来不错”。
2. 版权/IP：设计、音乐、图片、视频需要素材来源和商用授权记录。
3. 平台责任：agent 如果直接操作客户账号，必须有权限边界和审计。
4. 高风险服务：法律、税务、财务、健康类必须人审或仅限草稿/教育用途。
5. 供给冷启动：不能只靠通用模型，需要把优秀 freelancer 的 workflow 产品化。
6. Fiverr 正在自我 AI 化：差异化要落在跨工具履约、质量担保、可验收交付和端到端项目。

## 10. 推荐的下一步

1. 先把 Fiverr taxonomy 抽成 `services.csv/json`，每行包含 category、subcategory、task_type、automation_level、risk_level、required_tools、deliverable_type。
2. 基于附件模板做 `agent-service-template`，加入 `SERVICE.md`、`BRIEF_SCHEMA.json`、`QA_RUBRIC.md`、`POLICY.md`。
3. 选 3 个试点 agent：SEO audit、data cleaning、presentation deck。它们分别代表营销、数据、创意/商业交付，验收相对清楚。
4. 跑 30 个模拟订单，记录失败原因，再决定是否扩到 20 个。

## 信息来源

- Fiverr Services Directory: https://www.fiverr.com/categories
- Fiverr 2026 Form 20-F press release: https://www.fiverr.com/news/fiverr-20-f-2026
- Fiverr Q4/FY 2025 results: https://investors.fiverr.com/news-releases/news-release-details/fiverr-announces-fourth-quarter-and-full-year-2025-results
- Fiverr Go launch: https://www.fiverr.com/news/fiverr-go
- Fiverr 2025 Spring Business Trends Index press release: https://investors.fiverr.com/news-releases/news-release-details/businesses-rush-harness-ai-agents-fueling-18347-surge-freelancer

