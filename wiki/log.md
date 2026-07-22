## [2026-07-16] sync | 补全智能体研发工程师 JD 的六大知识缺口
- **变更**: 新增 [[Dify]]（entities）；新增 [[微服务与API网关设计]]、[[多租户SaaS架构]]、[[企业系统集成模式]]、[[Skills权限管理]]、[[Agent实例生命周期管理]]（concepts）；更新 [[index]]（Entities 添加 1 条目 + Concepts 添加 5 条目）
- **冲突**: 无（新概念均为新增知识域，与既有概念互补无矛盾——[[微服务与API网关设计]] 是 [[Harness_Engineering]] 的底层基础设施支撑；[[多租户SaaS架构]] 与 [[Memory_Agent]] 形成数据隔离的上下文参照；[[企业系统集成模式]] 与 [[MCP]]、[[Agent_Interfaces]] 形成"协议→接口→集成"三层互补关系；[[Skills权限管理]] 是 [[Claude_Code_Skills]] 的治理扩展；[[Agent实例生命周期管理]] 是 [[Agent_Loop]] 的平台工程维度展开）
- **网络**:
  - [[Dify]] 链接到 [[LangChain]]/[[OpenClaw]]/[[Claude_Code_Skills]]/[[MCP]]/[[RAG]]/[[摘要-算法应用开发工程师-jd]]/[[摘要-智能体研发工程师-jd]]
  - [[微服务与API网关设计]] 链接到 [[Harness_Engineering]]/[[Graceful_Degradation]]/[[Cost_Optimization]]/[[Agent_Observability]]/[[Agent_Loop]]/[[Claude_Code_Skills]]/[[MCP]]/[[Memory_Agent]]/[[OpenAI_Compatible_API]]/[[LiteLLM]]
  - [[多租户SaaS架构]] 链接到 [[微服务与API网关设计]]/[[Harness_Engineering]]/[[Cost_Aware_Budget_Gates]]/[[Memory_Agent]]/[[Claude_Code_Skills]]/[[Agent_Observability]]/[[Graceful_Degradation]]
  - [[企业系统集成模式]] 链接到 [[MCP]]/[[Agent_Interfaces]]/[[Slack]]/[[Telegram]]/[[微服务与API网关设计]]/[[多租户SaaS架构]]/[[Claude_Code_Skills]]/[[Harness_Engineering]]/[[摘要-智能体研发工程师-jd]]
  - [[Skills权限管理]] 链接到 [[Claude_Code_Skills]]/[[MCP]]/[[多租户SaaS架构]]/[[Work_Boundary]]/[[Harness_Engineering]]/[[Claude_Code_Hooks]]/[[Agent_As_Judge]]/[[Claude_Code_Plugins]]
  - [[Agent实例生命周期管理]] 链接到 [[Agent_Loop]]/[[Memory_Agent]]/[[多租户SaaS架构]]/[[微服务与API网关设计]]/[[Harness_Engineering]]/[[Agent_Observability]]/[[Cost_Aware_Budget_Gates]]/[[Work_Boundary]]/[[Graceful_Degradation]]

## [2026-07-16] ingest | 摄入智能体研发工程师 JD
- **变更**: 新增 [[摘要-智能体研发工程师-jd]]（sources）；更新 [[index]]（Sources 章节添加条目）
- **冲突**: 无（全新知识领域，与 [[摘要-算法应用开发工程师-jd]] 形成互补——一个偏应用层算法落地，一个偏平台层架构设计，清晰区分无重叠矛盾）
- **网络**:
  - [[摘要-智能体研发工程师-jd]] 链接到 [[Harness_Engineering]]/[[Agent_Loop]]/[[Memory_Agent]]/[[Claude_Code_Skills]]/[[Claude_Code_Memory_System]]/[[MCP]]/[[RAG]]/[[Agent_Interfaces]]/[[Agent_Orchestration_Patterns]]/[[Multi_Agent_System]]/[[Hierarchical_Task_Decomposition]]/[[LangChain]]/[[AutoGen]]/[[OpenClaw]]/[[Graceful_Degradation]]/[[Slack]]/[[Telegram]]/[[摘要-算法应用开发工程师-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[DeepSeek四份JD全景对比]]

## [2026-07-16] sync | 新增智能体研发工程师 JD 对标分析
- **变更**: 新增 [[智能体研发工程师JD对标分析]]（syntheses）；更新 [[index]]（Syntheses 章节添加条目）
- **冲突**: 无（全新综合分析，作为 [[DeepSeek四份JD全景对比]] 之外独立 JD 的补充对标）
- **网络**:
  - [[智能体研发工程师JD对标分析]] 链接到 [[摘要-智能体研发工程师-jd]]/[[摘要-算法应用开发工程师-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[摘要-deepseek-harness-team-jd]]/[[摘要-deepseek-agent-infra-jd]]/[[摘要-openclaw-info]]/[[DeepSeek四份JD全景对比]]/[[Harness_Engineering]]/[[Claude_Code_Skills]]/[[MCP]]/[[Memory_Agent]]/[[Agent_Orchestration_Patterns]]/[[Agent_Loop]]/[[Agent_Interfaces]]/[[RAG]]/[[Multi_Agent_System]]/[[LangChain]]/[[AutoGen]]/[[OpenClaw]]/[[Graceful_Degradation]]

## [2026-07-16] sync | 新增 LlamaIndex 实体页 + 升级 RAG 文档解析对比
- **变更**: 新增 [[LlamaIndex]]（entities）；更新 [[index]]（Entities 章节添加条目）；升级 [[RAG]]「文档解析工具对比」（从扁平工具列表→四维对比表含选型建议）
- **冲突**: 无（LlamaIndex 作为新的 RAG 数据框架实体，与 [[LangChain]]/[[LangGraph]] 定位互补不冲突；与现有 [[RAG]]/[[Chunking]] 页面的引用形成正向双向链接）
- **网络**: 
  - [[LlamaIndex]] 链接到 [[LangChain]]/[[LangGraph]]/[[RAG]]/[[LightRAG]]/[[ragas]]/[[Chunking]]/[[Agent_Orchestration_Patterns]]/[[Agent_Loop]]/[[Memory_Agent]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[摘要-awesome-agentic-ai-zh-agent-frameworks]]/[[摘要-awesome-agentic-ai-zh-memory-rag]]/[[摘要-算法应用开发工程师-jd]]
  - [[RAG]] 升级：新增文档解析工具对比表（[[LlamaIndex]] Loaders vs docling vs MarkItDown），含定位/强项/弱项/推荐场景四维对比 + 选型建议

## [2026-07-15] sync | 新增 Agent 沙箱工程体系 + 扩展 DeepSeek 全景对比至五 JD
- **变更**: 新增 [[摘要-deepseek-agent-infra-jd]]（sources）；新增 [[Agent沙箱工程]]（concepts）；大幅更新 [[DeepSeek四份JD全景对比]]（标题从"四份"→"五份"、新增 Agent Infra 一行、更新团队定位图/对比矩阵/产业链图/技术栈/三层模型归属/面试图/关联连接）；更新 [[index]]（Sources + Concepts + Syntheses 各添加条目）
- **冲突**: 无（[[Agent沙箱工程]] 作为 [[Harness_Engineering]] Safety Layer 的物理实现层，是互补的垂直分层关系；[[DeepSeek四份JD全景对比]] 更新为五 JD 版本为增量扩充无矛盾）
- **网络**: 
  - [[摘要-deepseek-agent-infra-jd]] 链接到 [[Agent沙箱工程]]/[[DeepSeek四份JD全景对比]]/[[Harness_Engineering]]/[[Agent_Loop]]/[[Agent_Observability]]/[[Eval_Harness]]/[[Cost_Optimization]]/[[摘要-deepseek-harness-team-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[摘要-预训练数据工程师-jd]]/[[摘要-deepseek-ai-search-jd]]
  - [[Agent沙箱工程]] 链接到 [[摘要-deepseek-agent-infra-jd]]/[[DeepSeek四份JD全景对比]]/[[Harness_Engineering]]/[[Agent_Loop]]/[[Agent_Observability]]/[[Eval_Harness]]/[[Cost_Optimization]]/[[Context_Window]]/[[Agent_Interfaces]]/[[Work_Boundary]]/[[Graceful_Degradation]]/[[Failure_Injection_Chaos_Eval]]/[[DeepSeek]]/[[摘要-deepseek-harness-team-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[摘要-预训练数据工程师-jd]]/[[摘要-deepseek-ai-search-jd]]

## [2026-07-15] sync | 新增 AI 搜索工程体系 + DeepSeek 四 JD 全景对比
- **变更**: 新增 [[摘要-deepseek-ai-search-jd]]（sources）；新增 [[AI搜索工程]]（concepts）；新增 [[DeepSeek四份JD全景对比]]（syntheses）；更新 [[index]]（Sources + Concepts + Syntheses 各添加条目）
- **冲突**: 无（全新知识领域；[[AI搜索工程]] 与现有 [[RAG]]/[[Context_Engineering]] 为互补拓展关系——RAG 是检索增强生成，AI 搜索工程是搜索引擎原生架构，两者互为补充无矛盾）
- **网络**: 
  - [[摘要-deepseek-ai-search-jd]] 链接到 [[AI搜索工程]]/[[DeepSeek四份JD全景对比]]/[[RAG]]/[[Context_Engineering]]/[[Harness_Engineering]]/[[摘要-deepseek-harness-team-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[摘要-预训练数据工程师-jd]]/[[DeepSeek]]/[[Eval_Harness]]/[[Cost_Optimization]]/[[Agent_Loop]]/[[Agent_Interfaces]]
  - [[AI搜索工程]] 链接到 [[摘要-deepseek-ai-search-jd]]/[[DeepSeek四份JD全景对比]]/[[RAG]]/[[Context_Engineering]]/[[Harness_Engineering]]/[[Context_Window]]/[[Cost_Optimization]]/[[Eval_Harness]]/[[Agent_Interfaces]]/[[Agent_Loop]]/[[Chunking]]/[[LightRAG]]/[[Memory_Agent]]/[[DeepSeek]]/[[摘要-deepseek-harness-team-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[摘要-预训练数据工程师-jd]]
  - [[DeepSeek四份JD全景对比]] 链接到 [[摘要-deepseek-harness-team-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[摘要-预训练数据工程师-jd]]/[[摘要-deepseek-ai-search-jd]]/[[DeepSeek]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[RAG]]/[[AI搜索工程]]/[[预训练数据工程]]/[[预训练数据四方向对比]]/[[Agent_Loop]]/[[Eval_Harness]]/[[Cost_Optimization]]/[[Agent_Observability]]/[[Agent_Interfaces]]

## [2026-07-15] sync | 新增预训练数据工程体系：来源 + 概念 + 综合报告
- **变更**: 新增 [[摘要-预训练数据工程师-jd]]（sources）；新增 [[预训练数据工程]]（concepts）；新增 [[预训练数据四方向对比]]（syntheses）；更新 [[index]]（Sources + Concepts + Syntheses 章节各添加一条目）
- **冲突**: 无（全新知识领域，与现有知识体系无矛盾；[[预训练数据工程]] 概念与 [[Harness_Engineering]]/[[Context_Engineering]] 的关联在页面中已建立）
- **网络**: 
  - [[摘要-预训练数据工程师-jd]] 链接到 [[预训练数据工程]]/[[预训练数据四方向对比]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[DeepSeek]]/[[摘要-deepseek-harness-team-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[RAG]]/[[Agent_Loop]]/[[Eval_Harness]]
  - [[预训练数据工程]] 链接到 [[摘要-预训练数据工程师-jd]]/[[预训练数据四方向对比]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[RAG]]/[[摘要-deepseek-harness-team-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[Eval_Harness]]/[[Agent_Loop]]/[[DeepSeek]]/[[Llama]]/[[Qwen]]
  - [[预训练数据四方向对比]] 链接到 [[摘要-预训练数据工程师-jd]]/[[预训练数据工程]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[摘要-deepseek-harness-team-jd]]/[[摘要-deepseek-service-engineer-jd]]/[[DeepSeek]]/[[RAG]]/[[Eval_Harness]]/[[Prompt_Engineering]]/[[Agent_Loop]]

## [2026-07-15] lint | 修复 3 个死链 + 消解 5 个孤岛
- **死链修复**: 新建 [[Hermes_Agent]]、[[Telegram]]、[[Slack]] 三个实体页面（被 [[AgentParadigms]] 引用）
- **孤岛消解**: 
  - [[LiteLLM]] → 在 [[Cost_Optimization]]、[[Graceful_Degradation]]、[[OpenAI_Compatible_API]] 添加反向链接
  - [[AgentParadigms]] → 在 [[Agent_Interfaces]]、[[Claude_Code_Subagent]] 添加反向链接
  - [[From_NoCode_To_Agent_Paradigm]] → 在 [[Harness_Engineering]]、[[Claude_Code_Workflow]]、[[Claude_Code_Skills]]、[[Developer_Agentic_Workflow]] 添加反向链接
  - [[Self_Organizing_Teams]] → 在 [[Agent_Orchestration_Patterns]]、[[Multi_Agent_System]] 添加反向链接
  - [[matt-pocock-skills-cheatsheet]] → 在 [[Claude_Code_Skills]] 添加反向链接
- **格式修复**: [[AgentParadigms]] 中 `[[Hermes Agent]]` → `[[Hermes_Agent]]`（TitleCase 规范对齐）
- **结果**: 0 死链、0 孤岛、知识库健康状态良好
- **冲突**: 无

## [2026-07-15] ingest | 摄入 Tool Error 处理 + Function Schema 设计两篇实践文章
- **变更**: 新增 [[摘要-tool-error-is-data]]（sources）；新增 [[摘要-function-schema-design]]（sources）；大幅更新 [[Tool_Calling]]（新增"错误处理模式"完整章节 + "Schema 设计深度指南"替换原有简表 + sources 更新 + 关联连接新增 2 个来源引用）；更新 [[index]]（Sources 章节添加 2 个条目）
- **冲突**: 无（新知识独立，[[Tool_Calling]] 已有 Schema 简表与 Description 原则，新增的"深度指南"和"错误处理"为互补增量合并无矛盾）
- **网络**: [[摘要-tool-error-is-data]] 链接到 [[Tool_Calling]]/[[Agent_Loop]]/[[Ollama]]/[[摘要-多步骤推理任务-连续-tool-调用]]/[[摘要-llm-tool-calling-practice]]；[[摘要-function-schema-design]] 链接到 [[Tool_Calling]]/[[Prompt_Engineering]]/[[Ollama]]/[[摘要-llm-tool-calling-practice]]/[[摘要-多步骤推理任务-连续-tool-调用]]/[[摘要-tool-error-is-data]]；[[Tool_Calling]] 新增与两个来源摘要的双向链接

## [2026-07-15] sync | 新增 "从无代码到Agent范式的转移" 概念页
- **变更**: 新增 [[From_NoCode_To_Agent_Paradigm]]（concepts）；更新 [[index]]（Concepts 章节添加条目）
- **冲突**: 无（新概念独立，与 [[Harness_Engineering]]/[[Claude_Code_Skills]]/[[Claude_Code_Workflow]] 互补无矛盾）
- **网络**: [[From_NoCode_To_Agent_Paradigm]] 链接到 [[Harness_Engineering]]/[[Claude_Code_Skills]]/[[Claude_Code_Workflow]]/[[Claude_Code_Dynamic_Workflows]]/[[Developer_Agentic_Workflow]]/[[Agent_Orchestration_Patterns]]/[[Claude_Code_Harness]]/[[Progressive_Disclosure]]/[[Work_Boundary]] 形成密集双向链接网络

## [2026-07-15] ingest | 摄入多步骤推理任务文章
- **变更**: 新增 [[摘要-多步骤推理任务-连续-tool-调用]]（sources）；更新 [[Tool_Calling]]（新增"多步调用的依赖链"章节）；更新 [[Agent_Loop]]（新增"多步依赖陷阱"提示）；更新 [[index]]（Sources + Concepts 章节）
- **冲突**: 无（新知识独立，与现有 [[Tool_Calling]]/[[Agent_Loop]] 内容互补无矛盾）
- **网络**: [[摘要-多步骤推理任务-连续-tool-调用]] 链接到 [[Tool_Calling]]/[[Agent_Loop]]/[[Ollama]]/[[Qwen]]/[[摘要-llm-tool-calling-practice]]；[[Tool_Calling]] 新增与 [[摘要-多步骤推理任务-连续-tool-调用]] 双向链接；[[Agent_Loop]] 新增跨页面锚点链接到 [[Tool_Calling#多步调用的依赖链]]
- **归档**: 1 个 raw/01-articles 文件 → raw/09-archive/

## [2026-07-15] sync | 新增 LiteLLM 实体页面
- **变更**: 新增 [[LiteLLM]]（entities）；更新 [[index]]（Entities 章节添加 LiteLLM）
- **冲突**: 无（新知识独立，与 [[OpenRouter]]/[[OpenAI_Compatible_API]]/[[MCP]] 互补无矛盾）
- **网络**: [[LiteLLM]] 链接到 [[Harness_Engineering]]/[[OpenAI_Compatible_API]]/[[OpenRouter]]/[[MCP]]/[[Cost_Optimization]]/[[Graceful_Degradation]]/[[Agent_Observability]]/[[langfuse]]/[[Claude_Code]]/[[Ollama]]

## [2026-07-15] ingest | 摄入 LLM Tool Calling 动手实践四连
- **变更**: 新增源 [[摘要-llm-tool-calling-practice]]（sources）；新增概念 [[Tool_Calling]]（concepts）；大幅更新 [[Agent_Loop]]（新增手写 ReAct 实现参考章节、更新 sources/关联连接）；更新 [[index]]（Sources + Concepts）
- **冲突**: 无（新知识独立，[[Tool_Calling]] 为全新概念；[[Agent_Loop]] 增量补充无矛盾）
- **网络**: [[摘要-llm-tool-calling-practice]] 链接到 [[Tool_Calling]]/[[Agent_Loop]]/[[Ollama]]/[[Qwen]]/[[Anthropic]]/[[OpenAI_Compatible_API]]/[[摘要-awesome-agentic-ai-zh-tool-use]]；[[Tool_Calling]] 链接到 [[Agent_Loop]]/[[OpenAI_Compatible_API]]/[[Anthropic]]/[[Ollama]]/[[Orchestration_Code_Examples]]；[[Agent_Loop]] 新增与 [[摘要-llm-tool-calling-practice]]/[[Tool_Calling]] 双向链接
- **归档**: 4 个 raw/01-articles 文件 → raw/09-archive/

## [2026-07-14] sync | 新增编排编程示例页面
- **变更**: 新增 [[Orchestration_Code_Examples]]（concepts）；更新 [[index]]（Concepts 章节添加 Orchestration_Code_Examples）
- **冲突**: 无
- **网络**: [[Orchestration_Code_Examples]] 与 [[Agent_Orchestration_Patterns]]/[[Multi_Agent_System]]/[[LangGraph]]/[[CrewAI]]/[[AutoGen]]/[[OpenAI_Agents_SDK]]/[[Agent_Loop]]/[[Harness_Engineering]] 形成密集双向链接网络

## [2026-07-14] sync | 扩展 Multi_Agent_System Framework 路线详解
- **变更**: 大幅更新 [[Multi_Agent_System]] — 扩展"两条实现路线"比较表（添加 安装方式/核心框架/编程范式/封装集成 维度 + 框架列表），新增 Framework 路线详解章节（本质定义、4 个选型场景、代表框架速查表）
- **冲突**: 无（增量补充，与现有 Subagent 路线内容互补无矛盾）
- **网络**: [[Multi_Agent_System]] 新增 Swarm/Strands 框架引用

## [2026-07-14] sync | 新增 AgentParadigms 概念页面
- **变更**: 新增 [[AgentParadigms]]（concepts）；更新 [[index]]（Concepts 章节添加 AgentParadigms）
- **冲突**: 无
- **网络**: [[AgentParadigms]] 与 [[Harness_Engineering]]/[[Agent_Interfaces]]/[[Agent_Loop]]/[[Claude_Code_Subagent]]/[[Multi_Agent_System]]/[[Agent_Orchestration_Patterns]]/[[Autonomy_Gradient]]/[[Cost_Aware_Budget_Gates]]/[[Context_Engineering]] 等形成密集双向链接网络

## [2026-07-14] ingest | 创建 LangChain 专有页面
- **变更**: 新增 [[LangChain]]（entities）；更新 [[index]]（Entities 章节添加 LangChain）
- **冲突**: 无（新知识独立，与已有 [[LangGraph]]/[[Harness_Engineering]]/[[Agent_Loop]]/[[Memory_Agent]]/[[Chunking]]/[[Reflexion]]/[[Agent_Observability]] 互补，通过双向链接深度整合）
- **网络**: [[LangChain]] 与 [[LangGraph]]/[[CrewAI]]/[[AutoGen]]/[[Harness_Engineering]]/[[Agent_Loop]]/[[Agent_Observability]]/[[Memory_Agent]]/[[RAG]]/[[Chunking]]/[[Reflexion]] 形成密集双向链接网络

## [2026-07-14] sync | 新增 mattpocock/skills 中文速查表
- **变更**: 新增 [[matt-pocock-skills-cheatsheet]]（syntheses）；更新 [[index]]（添加 Syntheses 章节）
- **冲突**: 无

## [2026-07-10] lint | 全面健康检查 — 死链/孤岛/Frontmatter/结构

- **修复**:
  - **死链修复**: log.md 中 10+ 处 `[[index.md]]` → `[[index]]`
  - **路径规范**: [[AI_Mastery_Compass]] 中 `[[wiki/index]]` → `[[index]]`、`[[wiki/log]]` → `[[log]]`
  - **补充 Frontmatter**: 为 [[AI_Mastery_Compass]]、[[Feynman_Technique]]、[[Nx]]、[[Turborepo]] 添加 `sources: []` 字段
  - **格式统一**: [[摘要-awesome-agentic-ai-zh-advanced-concepts]] 中 `source:` → `sources:`
  - **补充关联连接**: [[摘要-adk-agents-with-skills]] 新增 `## 关联连接` 区块
- **验证结果**: 0 死链、0 孤岛、100% Frontmatter 合规、142/142 页面完整
- **未修复（误报）**: log.md 中的 `[[wiki/index.md]]`、`[[Harness_Engineering.md]]`、`[[raw/09-archive/...]]`、`[[wikilink]]` 均为描述性/代码上下文，非真实链接

## [2026-07-10] lint | 知识库健康修复 — 死链/孤儿/索引

- **修复**:
  - **新建 6 个缺失页面**: [[Hamel_Husain]]（人物）、[[langfuse]]（可观测性平台）、[[OpenRouter]]（路由网关）、[[promptfoo]]（Eval 工具）、[[LightRAG]]（Graph RAG 框架）、[[ragas]]（RAG 评估框架）
  - **修复 2 个断链**: 源摘要中的 `raw/01-articles/` 引用改为对应的来源摘要链接
  - **修复 4 个格式问题**: log.md 中的 `[[wiki/index]]`、`[[wiki/index.md]]`、`[[wiki/sources/摘要-adk-agents-with-skills.md]]`、`[[raw/09-archive/...]]` 改为规范链接
  - **补充索引注册**: [[Feynman_Technique]] 已加入 [[index]]
  - **确认图片正常**: `![[Pasted image 20260706174748.png]]` 存在于 assets/ 目录，非断链
- **结果**: 6 新建 + 6 修复; 知识库健康状态良好

## [2026-07-10] sec | 移除 raw/09-archive/ 中 6 个 .py 文件的硬编码 API Key

- **修复**:
  - `error_handling_practice.py` — 替换硬编码 key 为环境变量读取 + 启动校验
  - `fewshot_practice.py` — 同上
  - `fewshot_practice_v2.py` — 同上
  - `fewshot_local_vs_deepseek.py` — 移除 fallback 默认值，强制环境变量
  - `system_prompt_practice.py` — 替换硬编码 key 为环境变量读取 + 启动校验
  - `system_prompt_practice_2.py` — 同上
- **残留**: `sk-fake-key-12345`（error_handling_practice.py）为故意错误的测试用 key，保留
- **冲突**: 无
- **影响**: 这些文件需通过环境变量 `DEEPSEEK_API_KEY` 设置真实 API Key 方可运行

## [2026-07-10] ingest | 摄入 DeepSeek API 错误处理实战与实验系列

- **变更**:
  - **新增源摘要 (3)**: [[摘要-deepseek-api-error-handling]] — DeepSeek API 认证/超长/重试三大场景; [[摘要-few-shot-experiment]] — 大模型 vs 小模型 few-shot 效果对比; [[摘要-system-prompt-experiment]] — System Prompt 三种人格输出对比
  - **新增概念**: [[Exponential_Backoff]] — 指数退避重试策略通用实现
  - **大幅更新**: [[DeepSeek]] — 追加 API 错误处理行为（认证错误、静默截断、Token 预检、重试策略表）、新增 3 个来源引用
  - **大幅更新**: [[Few_Shot_Prompting]] — 追加跨模型对比实验数据（llama 3B +10% vs deepseek ~0%）、4 项关键发现
  - **大幅更新**: [[Prompt_Engineering]] — 追加 System Prompt 控制力实验数据、风格与深度取舍分析
  - **增量更新**: [[BPE_Tokenizer]] — 追加实用 Token 估算方法; [[Agent_Loop]] — 追加 [[Exponential_Backoff]] 链接
  - **更新 [[index]]** — 新增 3 来源 + 1 概念; 更新 [[DeepSeek]] 描述
- **冲突**: 无（新知识独立或与现有页面互补，所有增量合并无矛盾）
- **网络**: 新增页面与 [[DeepSeek]]/[[Few_Shot_Prompting]]/[[Prompt_Engineering]]/[[Agent_Loop]]/[[BPE_Tokenizer]]/[[Exponential_Backoff]] 形成双向链接网络; 三篇实验来源互相链接形成实验系列网络

## [2026-07-10] ingest | 摄入 awesome-agentic-ai-zh for-developer 分支 — 开发者工作流

- **变更**:
  - **新增源摘要**: [[摘要-awesome-agentic-ai-zh-for-developer]] — 开发者延伸路线：7 场景分类 × 工具链映射 × Tier 升级路径 × Anti-patterns × 3 个 Workflow Recipe
  - **新增实体 (9)**: [[Cursor]] — 编辑器集成 AI 结对编程基准；[[Aider]] — git-native CLI pair-programmer 44k★；[[Cline]] — VS Code autonomous agent 61k★；[[Continue_Dev]] — CI source-controlled checks 33k★；[[OpenHands]] — 开源自主 agent 72k★；[[Goose_AI]] — 多接口可扩展 agent 43k★；[[Roo_Code]] — VS Code multi-mode agent 23k★；[[Repomix]] — codebase 打包 26k★；[[superpowers_obra]] — obra 20+ Skill 集合
  - **新增概念 (1)**: [[Developer_Agentic_Workflow]] — 开发者 Agentic AI 工作流框架
  - **大幅更新**: [[Agentic_Coding]] — 追加 Plan-First 模式、Anti-patterns 表、常用工具生态（9 个实体引用）
  - **增量更新**: [[Claude_Code]] — 追加 Tier 定位（Tier 1-3）和 6 个开发者场景映射
  - **增量更新**: [[Claude_Code_Skills]] — 追加 [[Developer_Agentic_Workflow]] 和 [[superpowers_obra]] 引用
  - **增量更新**: [[Harness_Engineering]] — 追加 CI review 自动化、[[Developer_Agentic_Workflow]]、[[Continue_Dev]]、[[Repomix]] 引用
  - **更新 [[index]]** — 新增 1 来源 + 9 实体 + 1 概念；更新 [[Claude_Code]] 描述
- **冲突**: 无（新知识独立，所有实体为首次引入；Agentic_Coding 的 Anti-patterns 与已有内容互补无矛盾）
- **网络**: 新增 11 个页面与 [[Claude_Code]]/[[Agentic_Coding]]/[[Claude_Code_Skills]]/[[Harness_Engineering]]/[[Developer_Agentic_Workflow]] 形成密集双向链接网络；[[Developer_Agentic_Workflow]] 作为中心概念页链接所有新实体
- **路线图**: 这是 awesome-agentic-ai-zh 的**开发者分支**（主路线图 Stage 0→8 已全部收录），为开发者工作流场景独立的一维

- **变更**:
  - **新增源摘要**: [[摘要-awesome-agentic-ai-zh-advanced-concepts]] — 进阶 Agentic 概念地图（12 进阶概念、四层工作边界、跨供应商 Harness 原则框架、Opus 4.8 Dynamic Workflows、Eval Rigor、Bitter Lesson）
  - **新增概念**: [[Work_Boundary]] — 四层工作边界模型（Types → Config → Repo → Service），跨所有层的根概念
  - **新增概念**: [[Legibility]] — OpenAI Harness 五原则之一：为 Agent 优化 Codebase/Tool 可读性
  - **新增概念**: [[System_of_Record]] — OpenAI Harness 五原则之二：知识权威来源
  - **新增概念**: [[Taste_Invariants]] — OpenAI Harness 五原则之四：品味不变量/Lint 强制约束
  - **新增概念**: [[Autonomy_Gradient]] — Suggest → Propose → Execute 三段授权梯度
  - **新增概念**: [[Contract_Driven_Handoffs]] — 契约驱动的 Agent 交接模式
  - **新增概念**: [[Agent_As_Judge]] — Agent 评审机制 & Constitutional AI
  - **新增概念**: [[Hierarchical_Task_Decomposition]] — Supervisor → Worker → Sub-worker 多层递归编排
  - **新增概念**: [[Cost_Aware_Budget_Gates]] — 成本感知预算门控
  - **新增概念**: [[Failure_Injection_Chaos_Eval]] — 故障注入与混沌评估
  - **新增概念**: [[Self_Organizing_Teams]] — Agent 运行时动态协商分工
  - **新增概念**: [[Spec_Driven_Development]] — Formal Spec 驱动的 Agent 开发
  - **新增概念**: [[Graceful_Degradation]] — Frontier Model 挂掉时的优雅降级
  - **大幅更新**: [[Harness_Engineering]] — 追加跨供应商 4 大类别原则框架、OpenAI 5 原则 × Anthropic 对照表、原则间 Enabling 关系图、5 原则 × 8 元件对照表、Eval Rigor 警告、Bitter Lesson/Model-Harness-Fit
  - **增量更新**: [[Progressive_Disclosure]] — 追加 OpenAI 视角（Small Entry Point + Navigation）和跨 Vendor 对照表
  - **增量更新**: [[Claude_Code_Dynamic_Workflows]] — 追加 Context Offloading 核心机制、16/1000 规模上限、Adversarial Propose/Refute/Converge 质量机制、诚实限制清单
  - **更新 [[index]]** — 新增 1 来源 + 13 概念；更新 [[Harness_Engineering]]/[[Progressive_Disclosure]] 描述
- **冲突**: 无（新知识独立或补充现有页面；[[Progressive_Disclosure]] 的 OpenAI 视角与原有 Google ADK 视角互补无矛盾；[[Harness_Engineering]] 已有 OpenAI 5 模块框架与新 5 原则展开互补）
- **网络**: 新增 13 个概念页面与 [[Harness_Engineering]]/[[Progressive_Disclosure]]/[[Claude_Code_Dynamic_Workflows]]/[[Work_Boundary]]/[[Agent_Orchestration_Patterns]]/[[Eval_Harness]]/[[Contract_Driven_Handoffs]]/[[Agent_As_Judge]]/[[Autonomy_Gradient]]/[[Cost_Optimization]]/[[Graceful_Degradation]] 等形成密集双向链接网络
- **路线图**: [[摘要-awesome-agentic-ai-zh-foundations]] → [[摘要-awesome-agentic-ai-zh-llm-basics]] → [[摘要-awesome-agentic-ai-zh-prompt-engineering]] → [[摘要-awesome-agentic-ai-zh-tool-use]] → [[摘要-awesome-agentic-ai-zh-agent-frameworks]] → [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] → [[摘要-awesome-agentic-ai-zh-memory-rag]] → [[摘要-awesome-agentic-ai-zh-multi-agent-production]] → **[[摘要-awesome-agentic-ai-zh-advanced-concepts]]** — **路线图 Stage 0→1→2→3→4→5→6→7→7.5 全部收录完成 🎉**

## [2026-07-10] ingest | 摄入 awesome-agentic-ai-zh Stage 7 — Multi-Agent & Production（最终章）

- **变更**:
  - **新增原始素材**: `raw/01-articles/07-multi-agent-production.zh-Hans.md`（从 GitHub 网页提取）
  - **新增源摘要**: [[摘要-awesome-agentic-ai-zh-multi-agent-production]] — Multi-Agent & Production 最终章：Harness 8 核心元件、Eval/Observability/Cost 优化、Benchmark Landscape
  - **新增概念**: [[Eval_Harness]] — Agent 自动化评估流水线（Benchmark Landscape + Reward-Hacking 警告 + pass^k）
  - **新增概念**: [[Agent_Observability]] — 智能体可观测性（Tracing / Logging / Token Counting / Cost Tracking）
  - **新增概念**: [[Cost_Optimization]] — LLM 成本与延迟优化（Prompt Caching / Model Routing / Batching / Semantic Caching）
  - **大幅更新**: [[Harness_Engineering]] — 追加 8 核心元件框架（前 6 Runtime + Eval + Cost/Latency）、三层工程分工定位（Prompt→Context→Harness）、反馈循环四时机、Cost/Latency 优化技术总览、参考实现说明
  - **增量更新**: [[Multi_Agent_System]] — 追加 Production 化注意事项表、MAST 失败模式分类参考
  - **增量更新**: [[Agent_Orchestration_Patterns]] — 追加 Production 化视角链接
  - **更新 [[index]]** — 新增 1 来源 + 3 概念；更新 [[Harness_Engineering]] 描述
- **冲突**: 无（新增知识独立或与现有页面互补；Harness_Engineering 的 OpenAI 框架与 awesome-agentic-ai-zh 八元件框架在各自段落共存、无矛盾）
- **网络**: 新增 4 个页面与 [[Harness_Engineering]]/[[Multi_Agent_System]]/[[Agent_Orchestration_Patterns]]/[[Agent_Loop]]/[[Agentic_Coding]]/[[Prompt_Engineering]]/[[Context_Engineering]] 等形成密集双向链接网络
- **路线图**: [[摘要-awesome-agentic-ai-zh-foundations]] → [[摘要-awesome-agentic-ai-zh-llm-basics]] → [[摘要-awesome-agentic-ai-zh-prompt-engineering]] → [[摘要-awesome-agentic-ai-zh-tool-use]] → [[摘要-awesome-agentic-ai-zh-agent-frameworks]] → [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] → [[摘要-awesome-agentic-ai-zh-memory-rag]] → **[[摘要-awesome-agentic-ai-zh-multi-agent-production]]** — **路线图 Stage 0→1→2→3→4→5→6→7 全部收录完成 🎉**

## [2026-07-09] ingest | 增量合并实验系列更新版（云端数据补全）

- **变更**:
  - 更新 [[摘要-ollama-style-comparison]] — 补全 DeepSeek + 豆包云端实际数据（原为"待补充"）
  - 更新 [[摘要-ollama-experiment-index]] — 补充云端 API 对比结论
  - 更新 [[DeepSeek]] — 增加 V4 Pro 风格对比基准 + 辩论式结构描述
  - 更新 [[Doubao]] — 增加风格对比基准数据 + 条理清晰描述
- **冲突**: 模型名称差异（实验五用 DeepSeek V4 Flash，实验七用 V4 Pro）→ 已在 DeepSeek 页面标注说明，两者分属不同版本
- **网络**: [[DeepSeek]] 和 [[Doubao]] 新增风格对比数据，与 [[Ollama]]/[[Llama]]/[[Qwen]] 对比更完整

## [2026-07-10] ingest | 摄入 awesome-agentic-ai-zh Stage 4 — Agent 框架

- **变更**:
  - 新增 [[摘要-awesome-agentic-ai-zh-agent-frameworks]]（来源摘要）
  - 新增实体：[[LangGraph]], [[CrewAI]], [[AutoGen]], [[OpenAI_Agents_SDK]]
  - 新增概念：[[Multi_Agent_System]], [[Agent_Orchestration_Patterns]]
  - 更新 [[Agent_Loop]] — 追加 Multi-agent 和编排模式反向链接
  - 更新 [[Anthropic]] — 追加 Building Effective Agents 引用链接
  - 更新 [[Claude_Code]] — 追加 Subagent 路线（Multi-agent 第二条路）链接
  - 更新 [[OpenAI]] — 追加 OpenAI Agents SDK 链接
  - 更新 [[摘要-awesome-agentic-ai-zh-tool-use]] — 追加 Stage 4 后继链接
  - 更新 [[index]] — 新增 2 概念 + 4 实体 + 1 来源
- **冲突**: 无（新知识独立，已通过双向链接整合到现有页面）
- **原始素材**: 已保存至 raw/01-articles/04-agent-frameworks.md

## [2026-07-09] lint | 知识库健康巡检与修复

- **结果**:
  - 修复 1 个死链：新建 [[Feynman_Technique]]（被 [[Naval_Rapid_Research_Method]]、[[Naval_Ravikant]] 引用）
  - 消除 9 个孤儿页面：在 [[Ollama]]、[[DeepSeek]]、[[Doubao]]、[[BPE_Tokenizer]]、[[Temperature_Parameter]]、[[Model_Fine_Tuning]] 中追加来源摘要反链
  - 修复 1 处格式：`[[Harness_Engineering.md]]` → `[[Harness_Engineering]]`
- **当前状态**: 0 死链、0 孤岛、0 知识冲突

## [2026-07-03] ingest | 引入 AI 时代 Git 版本管理文章

- **变更**: 新增 [[摘要-ai-era-git-management]]; 新增实体 [[TRAE_ai]], [[Jujutsu]], [[GitButler]]; 新增概念 [[Agentic_Coding]], [[Agent_Aware_Commit]], [[Atomic_Commit]], [[Checkpoint_Commit]], [[Commit_Trailer]], [[Stacked_PR]], [[Virtual_Branch]], [[Feature_Branch_Workflow]], [[AGENT_MD]], [[Monorepo]]; 更新 [[index]]
- **冲突**: 无（全新知识库，无已有页面冲突）

## [2026-07-03] ingest | 引入 Claude Code 完全指南

- **变更**: 新增 [[摘要-claude-code-guide]]; 新增实体 [[Claude_Code]], [[Anthropic]]; 新增概念 [[Claude_Code_Slash_Commands]], [[Claude_Code_Memory_System]], [[Claude_Code_Workflow]]; 更新 [[index]], [[AGENT_MD]]
- **冲突**: 无（全新知识库，无已有页面冲突）

## [2026-07-03] ingest | 摄入 OpenAI Harness Engineering 官方文章

- **变更**: 新增 [[Harness_Engineering]], [[摘要-openai-harness-engineering]]; 更新 [[index]]
- **冲突**: 与 [[Agentic_Coding]] 的关系已在 [[Harness_Engineering]] 页面中辨析对比

## [2026-07-03] ingest | 全量摄入 raw/01-articles 38个文件

- **变更**: 
  - 新增源摘要 [[摘要-agent-first-engineering]], [[摘要-claude-code-boris-cherny]], [[摘要-claude-code-hud]], [[摘要-claude-code-gsd-core]], [[摘要-agent-loop-guide]], [[摘要-openclaw-info]], [[摘要-agentic-ai-roadmap]]
  - 新增实体 [[OpenClaw]], [[Boris_Cherny]], [[GSD_Core]]
  - 新增概念 [[Agent_First_Engineering]], [[Agent_Loop]], [[Claude_Code_Skills]]
  - 更新 [[Claude_Code]], [[AGENT_MD]], [[index]]
- **冲突**: 无（新知识独立或已合并到现有页面）
- **归档**: 所有 raw/01-articles 文件已移至 raw/09-archive/

## [2026-07-06] lint | 知识库健康检查

- **新增**: [[Codex]], [[Nx]], [[Turborepo]] (修复 3 个死链)
- **修复**: 为 [[Agent_First_Engineering]], [[Claude_Code_Skills]], [[摘要-agentic-ai-roadmap]], [[摘要-claude-code-hud]] 添加反向链接 (修复 4 个孤岛)
- **已解决**: [[Harness_Engineering]] 中的知识冲突无需干预 (已标注对比)
- **结果**: 0 死链、0 孤岛、1 处知识冲突已标注

## [2026-07-06] lint | 知识库健康检查（二次验证）

- **变更**: 无新增页面
- **死链**: 0 个 — 所有 [[wikilink]] 均正确解析
- **孤岛**: 0 个 — 38 个内容页面均有 >=1 个反向链接
- **知识冲突**: 1 处 — [[Harness_Engineering]] 中已标注，无需干预
- **目录完整性**: 全部 38 个文件均在 [[index]] 中列出，无遗漏
- **微小问题**: [[摘要-openai-harness-engineering]] 有重复链接区块；[[Claude_Code_Workflow]] 中 [[Claude_Code]] 链接重复 — **已修复**
- **结果**: 知识库健康状态良好

## [2026-07-06] ingest | 引入 AI 大模型驾驭进阶罗盘

- **变更**: 新增 [[AI_Mastery_Compass]]；更新 [[index]]
- **冲突**: 无（全新概念，与传统 Prompt 模板收藏路线无直接冲突）

## [2026-07-06] lint | 修复死链和孤儿页面

- **新增**: [[Prompt_Engineering]] (修复 AI_Mastery_Compass 中的死链)
- **修复**: 为 [[AI_Mastery_Compass]] 在 [[Agentic_Coding]], [[Agent_Loop]], [[Harness_Engineering]], [[Claude_Code_Skills]] 中添加反向链接 (修复 1 个孤岛)
- **结果**: 1 死链已修复, 1 孤岛已消除; 知识库健康状态良好

## [2026-07-06] ingest | 引入 Google ADK Skill 系统文章并修复位置违规

- **变更**: 
  - **迁移**: 修复违规，将 `developers-guide-to-building-adk-agents-with-skills.md` 从 vault 根目录移至 [[摘要-adk-agents-with-skills]]
  - **新增**: 实体 [[ADK]]; 概念 [[Progressive_Disclosure]], [[Skill_Factory]]
  - **更新**: 为 [[Claude_Code_Skills]], [[Harness_Engineering]], [[Agentic_Coding]] 添加反向链接
  - **更新**: [[index]] 总目录
  - **归档**: 原始内容同时保存至 `raw/09-archive/`
- **冲突**: 无（新增概念与现有知识互补，无直接冲突）

## [2026-07-07] ingest | 引入纳瓦尔极速研究法

- **变更**:
  - 新增概念 [[Naval_Rapid_Research_Method]] — 纳瓦尔 7 步从零掌握任意新领域的方法论
  - 新增实体 [[Naval_Ravikant]] — 硅谷天使投资人与思想家
  - 更新 [[index]] 总目录，为 [[Naval_Ravikant]] 和 [[Naval_Rapid_Research_Method]] 建立条目
- **冲突**: 无（全新知识，与现有学习方法论框架互补）
- **关联**: 与 [[AI_Mastery_Compass]]（同为系统框架）、[[Andrej_Karpathy]]（同为硅谷思想家）、[[Feynman_Technique]]（内嵌于第 5 步）建立双向链接

## [2026-07-08] ingest | 引入 Ollama 本地 LLM Python 调用实战

- **变更**:
  - 新增源 [[摘要-ollama-local-llm-python]] — 四种 API 调用方式与 Windows 踩坑记录
  - 新增实体 [[Ollama]] — 本地大语言模型运行工具
  - 新增实体 [[Qwen]] — 阿里云通义千问开源模型系列
  - 新增实体 [[Llama]] — Meta 开源大语言模型系列
  - 新增概念 [[OpenAI_Compatible_API]] — 已成为 LLM 行业事实标准的接口规范
  - 新增概念 [[本地_LLM_推理]] — 在本地硬件上运行 LLM 的数据隐私优先方案
  - 更新 [[index]] 总目录
- **冲突**: 无（新知识独立，与已有实体/概念无直接冲突）
- **网络**: [[OpenAI_Compatible_API]] 与 [[GPT]] 建立链接；[[Ollama]]/[[Qwen]]/[[Llama]] 三者互链

## [2026-07-09] ingest | 引入 Ollama LLM 实验系列（7 项实验 + 索引）

- **变更**:
  - 新增源 [[摘要-ollama-experiment-index]] — 实验系列总索引
  - 新增源 [[摘要-ollama-token-diff]] — 中英文 Token 差异分析
  - 新增源 [[摘要-ollama-temperature-scan]] — 温度参数 0.0~1.5 扫描
  - 新增源 [[摘要-ollama-determinism-test]] — 温度=0 确定性 20/20 验证
  - 新增源 [[摘要-ollama-temperature-fluctuation]] — 温度=0.7 Token 波动分析
  - 新增源 [[摘要-ollama-cost-comparison]] — 本地 vs 云端成本对比
  - 新增源 [[摘要-ollama-tokenizer-personality]] — Tokenizer 效率与模型性格
  - 新增源 [[摘要-ollama-style-comparison]] — 多模型回答风格对比
  - 新增实体 [[DeepSeek]] — 云端 MoE 模型 API 服务商
  - 新增实体 [[Doubao]] — 字节跳动低延迟高性价比 LLM 产品
  - 新增概念 [[BPE_Tokenizer]] — 中英文 Token 差异的底层算法根因
  - 新增概念 [[Temperature_Parameter]] — 确定性与多样性的核心控制参数
  - 新增概念 [[Model_Fine_Tuning]] — 模型性格与回复风格的塑造因素
  - 更新 [[index]] 总目录
- **冲突**: 无（新知识独立，与现有 LLM 基础概念互补）
- **网络**: [[BPE_Tokenizer]] ↹ [[GPT]]/[[Transformer_Architecture]]；[[Temperature_Parameter]] ↹ [[OpenAI_Compatible_API]]；[[Model_Fine_Tuning]] ↹ [[Ollama]]/[[Qwen]]/[[Llama]]

## [2026-07-06] ingest | 引入 Karpathy GPT 从零构建视频教程

- **变更**: 
  - 新增源 [[摘要-gpt-from-scratch]] — Andrej Karpathy 的 Zero to Hero 系列 GPT 构建教程
  - 新增实体 [[Andrej_Karpathy]] — AI 研究科学家与教育者
  - 新增概念 [[GPT]], [[Transformer_Architecture]], [[Self_Attention]] — Transformer 核心知识体系
  - 更新 [[index]] 总目录
  - 为 [[Andrej_Karpathy]], [[GPT]], [[Transformer_Architecture]], [[Self_Attention]] 建立双向链接网络
- **冲突**: 无（全新领域知识，与现有 Agentic Coding 知识体系互补）
- **源**: YouTube 视频 https://www.youtube.com/watch?v=kCc8FmEb1nY

## [2026-07-10] ingest | 引入 awesome-agentic-ai-zh Stage 2 Prompt 工程指南
- **变更**: 
  - 新增源 [[摘要-awesome-agentic-ai-zh-prompt-engineering]] — 结构化提示词、Few-shot、CoT 与迭代优化的动手教程
  - 新增概念 [[Chain_of_Thought]] — 思维链推理增强技术（Zero-shot CoT / Few-shot CoT）
  - 新增概念 [[Few_Shot_Prompting]] — 少样本提示技术（0-shot / 1-shot / few-shot 对比）
  - 新增概念 [[Context_Engineering]] — 三层工程堆栈中间层（Karpathy 概念）
  - 更新 [[Prompt_Engineering]] — 增量合并结构化四要素、迭代 refinement、三层堆栈定位
  - 更新 [[index]] 总目录
- **冲突**: 无（已有 [[Prompt_Engineering]] 页面增量合并新内容，无矛盾；其余为新概念）
- **网络**: [[Chain_of_Thought]] ↹ [[Prompt_Engineering]]/[[Few_Shot_Prompting]]；[[Context_Engineering]] ↹ [[Prompt_Engineering]]/[[Harness_Engineering]]；所有新页指向[[摘要-awesome-agentic-ai-zh-prompt-engineering]]

## [2026-07-10] ingest | 引入 awesome-agentic-ai-zh Stage 1 LLM 基础指南
- **变更**: 
  - 新增源 [[摘要-awesome-agentic-ai-zh-llm-basics]] — Stage 1 LLM 三大核心概念、模型家族全景与 API 调用实践
  - 新增概念 [[Context_Window]] — LLM 上下文视窗概念（Claude 1M / GPT ~400k / Gemini 2M 对比）
  - 新增实体 [[OpenAI]] — GPT 系列模型开发商，OpenAI 兼容 API 标准的制定者
  - 更新 [[Anthropic]] — 增量合并模型家族定价表、Context Window 1M 信息、Fable 5 暂停说明
  - 更新 [[Llama]] — 增量合并 Llama 3.3 70B、Community License 信息
  - 更新 [[DeepSeek]] — 增量合并 V3/R1 推理模型产品线说明
  - 更新 [[index]] 总目录
- **冲突**: 无（所有增量合并无矛盾）
- **网络**: [[Context_Window]] ↹ [[BPE_Tokenizer]]/[[Context_Engineering]]/[[Temperature_Parameter]]；[[OpenAI]] ↹ [[GPT]]/[[Codex]]/[[OpenAI_Compatible_API]]；所有页面指向[[摘要-awesome-agentic-ai-zh-llm-basics]]

## [2026-07-10] ingest | 引入 awesome-agentic-ai-zh Stage 0 基础准备指南
- **变更**: 
  - 新增源 [[摘要-awesome-agentic-ai-zh-foundations]] — Stage 0 五大先修技能速览（Python/Git/CLI/REST API/YAML）
  - 更新 [[index]] 总目录
- **冲突**: 无
- **网络**: [[摘要-awesome-agentic-ai-zh-foundations]] ↹ [[摘要-awesome-agentic-ai-zh-llm-basics]]/[[摘要-awesome-agentic-ai-zh-prompt-engineering]]/[[Agentic_Coding]] — 完成 Stage 0→1→2 路线图收录

## [2026-07-10] ingest | 摄入 awesome-agentic-ai-zh Stage 6 — Context Engineering: RAG & Memory

- **变更**:
  - **新增原始素材**: `raw/01-articles/06-memory-rag.zh-Hans.md`（从 GitHub 网页提取）
  - **新增源摘要**: [[摘要-awesome-agentic-ai-zh-memory-rag]] — Context Engineering 核心：RAG 基础与进阶、Memory 系统设计、Chunking 与 Reflexion
  - **新增概念**: [[RAG]] — 检索增强生成架构全览（基础流水线 + 8 大进阶技巧 + Eval + 工具选型）
  - **新增概念**: [[Memory_Agent]] — Agent 记忆系统（Working/Long-term、CoALA 四层、3 种 Pattern、5 个 Production Memory Layer）
  - **新增概念**: [[Chunking]] — 文档分块策略（固定/滑动/递归/语义/混合 + 进阶变体）
  - **新增概念**: [[Reflexion]] — 基于持久 Episodic Memory 的反思机制（与 Self-Refine 对比）
  - **新增概念**: [[DSPy]] — Programming-not-Prompting 范式（Path 3 自动优化框架）
  - **大幅更新**: [[Context_Engineering]] — 扩展 4 个 Sub-problem 框架（Select/Write/Compress/Isolate）、Agent 双能力模型、相关概念体系对照表、密集双向链接网络
  - **更新 [[index]]** — 新增 1 来源 + 5 概念
- **冲突**: 无（新知识独立，所有增量合并无矛盾）
- **网络**: 新增 6 个页面与 [[Context_Engineering]]/[[Agent_Loop]]/[[Prompt_Engineering]]/[[Harness_Engineering]]/[[Claude_Code_Memory_System]]/[[Multi_Agent_System]] 等形成密集双向链接网络
- **路线图**: [[摘要-awesome-agentic-ai-zh-foundations]] → [[摘要-awesome-agentic-ai-zh-llm-basics]] → [[摘要-awesome-agentic-ai-zh-prompt-engineering]] → [[摘要-awesome-agentic-ai-zh-tool-use]] → [[摘要-awesome-agentic-ai-zh-agent-frameworks]] → [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] → **[[摘要-awesome-agentic-ai-zh-memory-rag]]** — 路线图 Stage 0→1→2→3→4→5→6 收录完成

- **变更**:
  - **新增原始素材**: `raw/01-articles/05-claude-code-ecosystem.md`（从 GitHub 网页提取）
  - **新增源摘要**: [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — Claude Code 生态系全景（MCP/Skills/Plugins/Subagents/7-Layer Architecture）
  - **新增实体**: [[Claude_Agent_SDK]] — Anthropic 官方 Agent Python SDK
  - **新增概念**: [[MCP]] — Model Context Protocol 协议层（L2.5 Tool Provider）
  - **新增概念**: [[Claude_Code_Hooks]] — L3 控制层事件钩子系统
  - **新增概念**: [[Claude_Code_Subagent]] — 原生 Multi-Agent 机制（L5 Coordination）
  - **新增概念**: [[Claude_Code_Dynamic_Workflows]] — Opus 4.8+ 动态 Workflow 编排
  - **新增概念**: [[Claude_Code_Plugins]] — Plugin 打包发布与 Marketplace（L6 Workflow）
  - **新增概念**: [[Claude_Code_Harness]] — 7-Layer Architecture Map 完整视图
  - **大幅更新**: [[Claude_Code]] — 扩展 7-Layer Architecture、`~/.claude/` 目录结构、Hooks 机制、Claude Cowork 对比
  - **大幅更新**: [[Claude_Code_Skills]] — 扩展 SKILL.md 结构、Skill vs MCP/Plugin/Subagent 对照、常用 Skills 推荐表、参考项目
  - **增量更新**: [[Anthropic]] — 补充 Claude Cowork 产品线、Agent 产品线对比表
  - **增量更新**: [[Multi_Agent_System]] — 补充三种 Subagent 机制、Dynamic Workflows 上层编排
  - **增量更新**: [[Claude_Code_Slash_Commands]] — 补充 /plan /agents /plugin install /permissions /resume /bg 等命令
  - **增量更新**: [[Claude_Code_Workflow]] — 补充 Skills 增强工作流、Subagent 并行工作流、Dynamic Workflows
  - **增量更新**: [[Agent_Orchestration_Patterns]] — 补充 Claude Code Subagent 编排模式对照表
  - **更新 [[index]]** — 新增 1 来源 + 1 实体 + 6 概念
- **冲突**: 无（新知识独立或与现有页面互补，所有增量合并无矛盾）
- **网络**: 新增 7 个页面与现有 [[Claude_Code]]/[[Multi_Agent_System]]/[[Agent_Orchestration_Patterns]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[Claude_Code_Skills]] 等形成密集双向链接网络
- **路线图**: [[摘要-awesome-agentic-ai-zh-foundations]] → [[摘要-awesome-agentic-ai-zh-llm-basics]] → [[摘要-awesome-agentic-ai-zh-prompt-engineering]] → [[摘要-awesome-agentic-ai-zh-tool-use]] → [[摘要-awesome-agentic-ai-zh-agent-frameworks]] → [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 路线图 Stage 0→1→2→3→4→5 收录完成

## [2026-07-10] ingest | 引入 awesome-agentic-ai-zh Stage 3 工具使用与第一个 Agent
- **变更**: 
  - 新增原始素材 [[摘要-awesome-agentic-ai-zh-tool-use]] — 从 GitHub 网站提取
  - 新增源 [[摘要-awesome-agentic-ai-zh-tool-use]] — Stage 3 Function Calling、ReAct 循环与 6 个动手练习教程
  - 更新 [[index]] 总目录
- **冲突**: 无（已有 [[Agent_Loop]] 页面涵盖 ReAct 概念，新摘要指向其作为补充）
- **网络**: [[摘要-awesome-agentic-ai-zh-tool-use]] ↹ [[Agent_Loop]]/[[Chain_of_Thought]]/[[Prompt_Engineering]]/[[Harness_Engineering]]/[[Ollama]]/[[Qwen]]/[[Anthropic]]/[[OpenAI]]/[[OpenAI_Compatible_API]]/[[本地_LLM_推理]] — 与已有 LLM/Agent 基础设施实体建立双向链接
- **路线图**: [[摘要-awesome-agentic-ai-zh-foundations]] → [[摘要-awesome-agentic-ai-zh-llm-basics]] → [[摘要-awesome-agentic-ai-zh-prompt-engineering]] → [[摘要-awesome-agentic-ai-zh-tool-use]] — 路线图 Stage 0→1→2→3 收录完成

## [2026-07-10] ingest | 摄入 awesome-agentic-ai-zh Stage 8 — Agent Interfaces（智能体接口）

- **变更**:
  - **新增原始素材**: `raw/01-articles/08-agent-interfaces.zh-Hans.md`（先重构，后通过 GitHub API 获取正式 SHA:9a40ea77 原文件并替换重建）
  - **新增源摘要**: [[摘要-awesome-agentic-ai-zh-agent-interfaces]] — Stage 8 共用 hub：Computer Use / Browser Use / Code Sandbox 三层接口详解
  - **新增概念**: [[Agent_Interfaces]] — 三层智能体接口模型概览（Computer Use / Browser Use / Code Sandbox），含与 Tool Use/MCP/Harness 区分、2024-2026 突破时间线、四强 CU 对比、沙箱术语词典、安全防护 4 模式
  - **大幅更新**: [[摘要-awesome-agentic-ai-zh-agent-interfaces]] — 补充原文更多细节（Tool Use/MCP/Harness 区分表、突破时间线、Accessibility Tree 模式、沙箱术语词典、安全案例与 4 防护模式、Voice/VLA 前沿展望）
  - **大幅更新**: [[Agent_Interfaces]] — 同步补充相同细节，增加 COU 四强对比 + OSWorld 数据解读 + AI 浏览器五强对比 + 隔离技术层级 + 安全案例 + Track A/B 实现路径
  - **更新 [[index]]** — 新增 1 来源 + 1 概念
- **冲突**: 无（新增知识独立，[[Agent_Interfaces]] 为全新概念，[[Harness_Engineering]] 中的 Sandbox 提及已存在但无矛盾）
- **网络**: [[Agent_Interfaces]] 与 [[Harness_Engineering]]/[[Agent_Loop]]/[[MCP]]/[[Claude_Agent_SDK]]/[[Codex]]/[[OpenAI_Agents_SDK]] 建立双向链接
- **路线图**: [[摘要-awesome-agentic-ai-zh-foundations]] → [[摘要-awesome-agentic-ai-zh-llm-basics]] → [[摘要-awesome-agentic-ai-zh-prompt-engineering]] → [[摘要-awesome-agentic-ai-zh-tool-use]] → [[摘要-awesome-agentic-ai-zh-agent-frameworks]] → [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] → [[摘要-awesome-agentic-ai-zh-memory-rag]] → [[摘要-awesome-agentic-ai-zh-multi-agent-production]] → [[摘要-awesome-agentic-ai-zh-advanced-concepts]] → **[[摘要-awesome-agentic-ai-zh-agent-interfaces]]** — **路线图 Stage 0→1→2→3→4→5→6→7→7.5→8 全部收录完成 🎉**

## [2026-07-15] ingest | DeepSeek Harness 团队职位描述 — 行业角色光谱与知识图谱
- **变更**:
  - **新增源摘要**: [[摘要-deepseek-harness-team-jd]] — DeepSeek Harness 团队 JD 全方向整理，含四个角色方向、技术知识图谱、三层工程模型行业验证、各方向特色技能、关键洞察
  - **大幅更新**: [[DeepSeek]] — 新增 "Harness 团队" 完整章节（团队使命、四个招聘方向与技术知识体系）；新增 tags（Harness、Agent、招聘）；更新 sources 和关联连接
  - **大幅更新**: [[Harness_Engineering]] — 新增 "行业视角：DeepSeek" 章节（行业验证表新增 DeepSeek 行、团队使命与公式、四角色光谱、全角色共享知识要求）；新增 "角色光谱" 章节（研究→工程→产品→PM 从科研深度到执行宽度的连续体）；新增 "Agent Harness 知识图谱" 表格（基础机制层 + 三层工程模型 + 应用层角色差异化 + AI 辅助开发能力 + 高强度用户门槛）
  - **更新 [[index]]** — 新增 [[摘要-deepseek-harness-team-jd]] 到 Sources 章节
- **冲突**: 无（新知识独立或补充现有页面；[[Harness_Engineering]] 已有"行业验证"表和"Harness 工程师"章节，新内容为互补增量合并无矛盾；[[DeepSeek]] 新增 Harness 团队章节为全新信息，与已有模型/API/实验数据内容互补无矛盾）
- **网络**:
  - [[摘要-deepseek-harness-team-jd]] 链接到 [[DeepSeek]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[Prompt_Engineering]]/[[Agent_Loop]]/[[MCP]]/[[Multi_Agent_System]]/[[Memory_Agent]]/[[Tool_Calling]]/[[Claude_Code_Subagent]]/[[Claude_Code_Skills]]/[[Skill_Factory]]/[[Agent_Observability]]/[[Eval_Harness]]/[[Work_Boundary]] — 形成与现有概念/实体体系的密集双向链接
  - [[DeepSeek]] 新增 ↹ [[摘要-deepseek-harness-team-jd]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[Prompt_Engineering]]
  - [[Harness_Engineering]] 新增 ↹ [[摘要-deepseek-harness-team-jd]]/[[DeepSeek]]

## [2026-07-15] ingest | DeepSeek 服务端工程师职位描述 — 生产 AI 系统三层架构与 Agent 后端工程实践
- **变更**:
  - **新增源摘要**: [[摘要-deepseek-service-engineer-jd]] — DeepSeek 服务端工程团队 JD 三个方向：线上核心服务（API 架构/性能优化）、Agent 后端（执行环境快照/框架评测/数据生成）、数据仓库（管道/流批/稳定性）；Agent 执行环境快照概念定义；三层生产 AI 系统架构模型；"工程即作品"哲学
  - **大幅更新**: [[DeepSeek]] — 新增 "服务端工程团队" 完整章节（团队使命、三个方向、Agent 后端课题拆解、Harness 团队 vs 工程团队对照表）；补充 tags（工程、后端、数据）；更新 sources 和关联连接
  - **大幅更新**: [[Harness_Engineering]] — 在"行业视角：DeepSeek"下新增"服务端工程团队"子章节（团队对照表、三层生产系统架构图、Agent 后端三个工程课题与 Harness 元件对照）；更新关联连接
  - **增量更新**: [[Agent_Loop]] — 扩展"状态持久化"为"状态持久化与执行环境快照"（新增执行环境快照定义、存储内容清单、DeepSeek 实践引用）
  - **更新 [[index]]** — 新增 [[摘要-deepseek-service-engineer-jd]] 到 Sources 章节
- **冲突**: 无（新知识独立或补充现有页面；[[DeepSeek]] 的服务端工程团队与已有 Harness 团队章节为互补对照关系无矛盾；[[Harness_Engineering]] 新增子章节与已有 DeepSeek 章节互补；[[Agent_Loop]] 的状态持久化内容扩展无矛盾）
- **网络**:
  - [[摘要-deepseek-service-engineer-jd]] 链接到 [[DeepSeek]]/[[Harness_Engineering]]/[[Agent_Loop]]/[[Eval_Harness]]/[[Memory_Agent]]/[[Checkpoint_Commit]]/[[Multi_Agent_System]]/[[Agent_Interfaces]]/[[Context_Engineering]]/[[Agent_Observability]]/[[摘要-deepseek-harness-team-jd]] — 形成与两个 DeepSeek 团队的完整知识网络
  - [[DeepSeek]] 服务端工程团队章节 <-> [[摘要-deepseek-service-engineer-jd]]/[[Harness_Engineering]]/[[Agent_Loop]]/[[Eval_Harness]]/[[Memory_Agent]]/[[Checkpoint_Commit]]/[[Agent_Observability]]/[[Agent_Interfaces]]
  - [[Harness_Engineering]] 新增 <-> [[摘要-deepseek-service-engineer-jd]]
  - [[Agent_Loop]] 新增 "执行环境快照" <-> [[摘要-deepseek-service-engineer-jd]]

## [2026-07-15] sync | 新增超算集群工程体系：来源 + 概念
- **变更**: 新增 [[摘要-hpc-cluster-engineer-jd]]（sources）；新增 [[超算集群工程]]（concepts）；更新 [[index]]（Sources + Concepts 章节各添加一条目）
- **冲突**: 无（全新知识领域，与现有 [[Harness_Engineering]] 为互补关系——超算集群工程是 Harness Engineering 的物理基础设施底座层；与 [[Agent沙箱工程]] 构成"单机沙箱→集群底座"互补；与 [[预训练数据工程]] 无矛盾）
- **网络**:
  - [[摘要-hpc-cluster-engineer-jd]] 链接到 [[超算集群工程]]/[[Harness_Engineering]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[DeepSeek五份JD全景对比]]/[[Agent_Loop]]/[[Eval_Harness]]/[[Cost_Optimization]]/[[Agent_Observability]]
  - [[超算集群工程]] 链接到 [[摘要-hpc-cluster-engineer-jd]]/[[Harness_Engineering]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[DeepSeek五份JD全景对比]]/[[Agent_Loop]]/[[Eval_Harness]]/[[Cost_Optimization]]/[[Agent_Observability]]/[[Context_Engineering]]/[[Agent_Interfaces]]/[[Work_Boundary]]

## [2026-07-15] sync | 新增 AI 计算引擎工程体系：来源 + 概念
- **变更**: 新增 [[摘要-hpc-operator-comm-compiler-jd]]（sources）；新增 [[AI计算引擎工程]]（concepts）；更新 [[超算集群工程]]（三层定位补充 AI 计算引擎对比、关联连接新增）；更新 [[index]]（Sources + Concepts 章节各添加一条目）
- **冲突**: 无（全新知识领域；[[AI计算引擎工程]] 与 [[超算集群工程]] 构成"怎么算 vs 在哪儿算"的垂直互补关系；与 [[Harness_Engineering]] 为 Cost/Latency #8 的底层依赖关系）
- **网络**:
  - [[摘要-hpc-operator-comm-compiler-jd]] 链接到 [[AI计算引擎工程]]/[[超算集群工程]]/[[Harness_Engineering]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[DeepSeek五份JD全景对比]]/[[Cost_Optimization]]/[[Eval_Harness]]
  - [[AI计算引擎工程]] 链接到 [[摘要-hpc-operator-comm-compiler-jd]]/[[超算集群工程]]/[[Harness_Engineering]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[DeepSeek五份JD全景对比]]/[[Cost_Optimization]]/[[Agent_Loop]]/[[Agent_Observability]]/[[Prompt_Engineering]]
  - [[超算集群工程]] 新增关联连接 [[AI计算引擎工程]]；三层定位新增对比表

## [2026-07-15] sync | 新增 AI 训练推理系统工程体系：来源 + 概念
- **变更**: 新增 [[摘要-training-inference-framework-jd]]（sources）；新增 [[AI训练推理系统工程]]（concepts）；更新 [[AI计算引擎工程]]（定位图增加 AI训练推理系统工程层、对比表改为三维）；更新 [[超算集群工程]]（定位图同步更新为四层体系、比较表更新、结论更新）；更新 [[index]]（Sources + Concepts 各添加一条目）
- **冲突**: 无（[[AI训练推理系统工程]] 位于 [[AI计算引擎工程]] 之上、[[Harness_Engineering]] 之下，形成"怎么训练/推理 → 怎么算 → 在哪儿跑"的垂直三层依赖；与现有页面为互补增量关系无矛盾）
- **网络**:
  - [[摘要-training-inference-framework-jd]] 链接到 [[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[Harness_Engineering]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[DeepSeek五份JD全景对比]]/[[Cost_Optimization]]/[[Eval_Harness]]/[[Agent_Loop]]
  - [[AI训练推理系统工程]] 链接到 [[摘要-training-inference-framework-jd]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[Harness_Engineering]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[DeepSeek五份JD全景对比]]/[[Cost_Optimization]]/[[Eval_Harness]]/[[Agent_Loop]]/[[Context_Window]]/[[Agent_Observability]]
  - [[AI计算引擎工程]] 定位图新增 AI训练推理系统工程层，对比表全面更新
  - [[超算集群工程]] 定位图同步更新为四层体系，对比表和结论同步刷新

## [2026-07-15] sync | 新增 AI 存储工程体系：来源 + 概念（横向底座层）
- **变更**: 新增 [[摘要-hpc-distributed-storage-jd]]（sources）；新增 [[AI存储工程]]（concepts，作为横向底座层）；更新 [[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[Agent沙箱工程]]（关联连接各新增 AI存储工程 引用）；更新 [[index]]（Sources + Concepts 各添加一条目，修复 Sources 误覆盖）
- **冲突**: 无（[[AI存储工程]] 与前五个基础设施概念不同——它是**横向底座层**而非垂直层，与所有现有概念为互补支撑关系）
- **网络**:
  - [[摘要-hpc-distributed-storage-jd]] 链接到 [[AI存储工程]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[DeepSeek五份JD全景对比]]/[[Cost_Optimization]]/[[Harness_Engineering]]
  - [[AI存储工程]] 链接到 [[摘要-hpc-distributed-storage-jd]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[DeepSeek五份JD全景对比]]/[[Harness_Engineering]]/[[Cost_Optimization]]/[[Eval_Harness]]/[[Agent_Loop]]/[[Memory_Agent]]
  - [[AI训练推理系统工程]] 等 4 个概念页面各新增 [[AI存储工程]] 关联连接

## [2026-07-15] sync | 新增 AI 集群可靠性工程体系：来源 + 概念（Build vs Run）
- **变更**: 新增 [[摘要-hpc-cluster-reliability-jd]]（sources）；新增 [[AI集群可靠性工程]]（concepts，作为超算集群工程的 Run 面）；更新 [[超算集群工程]]（定位图增加 AI集群可靠性工程层、新增 Build vs Run 对比表、结论更新）；更新 [[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[AI存储工程]]/[[Agent沙箱工程]]（关联连接各新增 AI集群可靠性工程 引用）；更新 [[index]]（Sources + Concepts 各添加一条目）
- **冲突**: 无（[[AI集群可靠性工程]] 与 [[超算集群工程]] 构成"Build vs Run"互补，与所有现有概念为互补关系）
- **网络**: 六工程概念页面全部与 [[AI集群可靠性工程]] 建立双向关联连接

## [2026-07-15] sync | 新增 AI 平台运维工程体系：来源 + 概念扩展（运维开发方向）
- **变更**: 新增 [[摘要-hpc-ops-platform-jd]]（sources，与前一份可靠性 JD 同团队）；扩展 [[AI集群可靠性工程]]（新增"内部双轨：集群运维 × 运维开发"定位、第 5 核心能力"运维开发平台工程"、挑战中的"快与稳平衡"；更新 frontmatter tags 和 sources）；更新 [[index]]（Sources 新增条目、Concepts 描述更新）
- **冲突**: 无（本 JD 的集群运维方向与现有 [[AI集群可靠性工程]] 冗余但无害；运维开发方向为全新内容，与 [[Harness_Engineering]] 的 Tool Registry/Observability 有直接交集，已在源摘要中标注对应关系）
- **网络**:
  - [[摘要-hpc-ops-platform-jd]] 链接到 [[AI集群可靠性工程]]/[[摘要-hpc-cluster-reliability-jd]]/[[超算集群工程]]/[[AI训练推理系统工程]]/[[Harness_Engineering]]/[[Agent_Observability]]/[[Eval_Harness]]/[[Cost_Optimization]]
  - [[AI集群可靠性工程]] 新增 sources、tags；新增运维开发平台工程完整章节

## [2026-07-15] sync | 新增 AI 基础设施硬件工程体系：来源 + 概念（物理底层）
- **变更**: 新增 [[摘要-it-infrastructure-jd]]（sources，系统硬件&网络 / IT桌面&信息化双方向）；新增 [[AI基础设施硬件工程]]（concepts，作为物理硬件最底层）；更新 [[超算集群工程]]/[[AI集群可靠性工程]]/[[AI存储工程]]（关联连接各新增 AI基础设施硬件工程 引用）；更新 [[index]]（Sources + Concepts 各添加一条目）
- **冲突**: 无（[[AI基础设施硬件工程]] 位于整个技术栈的最底层——低于超算集群工程和 AI 集群可靠性工程，高于 Agent 沙箱工程；IT 桌面方向为通用 ITIL 内容，仅在源摘要中记录不创建概念页面）
- **网络**:
  - [[摘要-it-infrastructure-jd]] 链接到 [[AI基础设施硬件工程]]/[[超算集群工程]]/[[AI集群可靠性工程]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[AI存储工程]]/[[Agent沙箱工程]]/[[Harness_Engineering]]
  - [[AI基础设施硬件工程]] 链接到 [[摘要-it-infrastructure-jd]]/[[超算集群工程]]/[[AI集群可靠性工程]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[AI存储工程]]/[[Agent沙箱工程]]/[[Harness_Engineering]]/[[Cost_Optimization]]

## [2026-07-15] sync | 新增 AI 数据中心工程体系：来源 + 概念（最底层物理设施）
- **变更**: 新增 [[摘要-idc-datacenter-jd]]（sources，供配电/液冷/设计/运营/现场三方向）；新增 [[AI数据中心工程]]（concepts，作为物理建筑设施最底层）；更新 [[超算集群工程]]/[[AI集群可靠性工程]]/[[AI存储工程]]/[[AI基础设施硬件工程]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[Agent沙箱工程]]（关联连接各新增 AI数据中心工程 引用）；更新 [[index]]（Sources + Concepts 各添加一条目）
- **冲突**: 无（[[AI数据中心工程]] 位于整个技术栈的最底部——低于 AI 基础设施硬件工程，与所有现有概念为"承载与被承载"的物理支撑关系）
- **网络**: 全部 8 个基础设施概念页面均与 [[AI数据中心工程]] 建立双向关联连接

## [2026-07-15] sync | 新增 AI 产品经理 JD + AI产品工程概念（最上层：产品化层）
- **变更**: 新增 [[摘要-ai-product-manager-jd]]（sources）；新增 [[AI产品工程]]（concepts——最上层产品化层）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[AI产品工程]] 作为"站在模型与世界之间"的最上层，与现有 [[Harness_Engineering]]/[[Prompt_Engineering]]/[[Context_Engineering]] 等技术层为互补的"产品化/技术化"分层关系；六个工程概念 [[AI产品工程]]→[[AI训练推理系统工程]]→[[AI计算引擎工程]]→[[超算集群工程]]→[[AI集群可靠性工程]]→[[AI基础设施硬件工程]]→[[AI数据中心工程]]→[[AI存储工程]]→[[Agent沙箱工程]] 形成完整的"从产品到设施"的纵向全栈体系无矛盾）
- **网络**:
  - [[摘要-ai-product-manager-jd]] 链接到 [[AI产品工程]]/[[Harness_Engineering]]/[[Agent沙箱工程]]/[[AI训练推理系统工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[超算集群工程]]/[[AI集群可靠性工程]]/[[DeepSeek五份JD全景对比]]/[[DeepSeek]]
  - [[AI产品工程]] 链接到 [[摘要-ai-product-manager-jd]]/[[Harness_Engineering]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[AI集群可靠性工程]]/[[AI存储工程]]/[[AI基础设施硬件工程]]/[[AI数据中心工程]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[预训练数据工程]]/[[Prompt_Engineering]]/[[Context_Engineering]]/[[DeepSeek五份JD全景对比]]/[[Agent_Loop]]/[[Agent_Observability]]/[[Cost_Optimization]]/[[DeepSeek]]

## [2026-07-15] sync | 新增 Code Agent 数据工程师 JD + Agent能力工程概念（第十份 JD，能力构建层）
- **变更**: 新增 [[摘要-code-agent-data-engineer-jd]]（sources）；新增 [[Agent能力工程]]（concepts——横跨数据/训练/评估三层的 Agent 能力塑造层）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[Agent能力工程]] 与 [[预训练数据工程]] 为互补关系——预训练数据是静态文本/Rt 训练环境是动态交互；与 [[Eval_Harness]] 为内容供给关系——Eval Harness 是评测框架/本层是评测内容；与 [[AI训练推理系统工程]] 为使用者关系——RL 训练系统是基础设施/本层是训练内容；与 [[Agent沙箱工程]] 为依赖关系——RL 环境需要在沙箱中安全执行）
- **网络**:
  - [[摘要-code-agent-data-engineer-jd]] 链接到 [[Agent能力工程]]/[[预训练数据工程]]/[[AI训练推理系统工程]]/[[Eval_Harness]]/[[Harness_Engineering]]/[[AI产品工程]]/[[Agent沙箱工程]]/[[DeepSeek四份JD全景对比]]/[[DeepSeek]]
  - [[Agent能力工程]] 链接到 [[摘要-code-agent-data-engineer-jd]]/[[预训练数据工程]]/[[AI训练推理系统工程]]/[[Eval_Harness]]/[[Harness_Engineering]]/[[AI产品工程]]/[[Agent沙箱工程]]/[[AI搜索工程]]/[[DeepSeek四份JD全景对比]]/[[Agent_Loop]]/[[Agent_Observability]]/[[Context_Window]]/[[DeepSeek]]/[[摘要-deepseek-harness-team-jd]]/[[预训练数据四方向对比]]

## [2026-07-15] sync | 新增通用Agent数据产品经理 JD + Agent数据产品工程概念（第十一份 JD，评测数据桥梁层）
- **变更**: 新增 [[摘要-agent-general-data-pm-jd]]（sources）；新增 [[Agent数据产品工程]]（concepts——产品层与能力构建层之间的评测数据桥梁层）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[Agent数据产品工程]] 与 [[AI产品工程]] 为上下游关系——产品层定义用户体验方向/本层提供数据驱动评测；与 [[Agent能力工程]] 为互补关系——能力工程构建底层能力/本层定义通用场景评测与数据；与 [[Eval_Harness]] 为内容供给关系——Eval_Harness 是评测框架/本层是评测内容和标准；与 [[预训练数据工程]] 为数据形态互补——静态文本 vs 动态交互数据）
- **网络**:
  - [[摘要-agent-general-data-pm-jd]] 链接到 [[Agent数据产品工程]]/[[AI产品工程]]/[[Agent能力工程]]/[[Eval_Harness]]/[[Harness_Engineering]]/[[AI搜索工程]]/[[预训练数据工程]]/[[Agent沙箱工程]]/[[DeepSeek]]
  - [[Agent数据产品工程]] 链接到 [[摘要-agent-general-data-pm-jd]]/[[AI产品工程]]/[[Agent能力工程]]/[[Eval_Harness]]/[[Harness_Engineering]]/[[AI搜索工程]]/[[预训练数据工程]]/[[AI训练推理系统工程]]/[[Agent沙箱工程]]/[[Prompt_Engineering]]/[[Agent_Loop]]/[[Agent_Observability]]/[[DeepSeek]]

## [2026-07-15] sync | 新增专业领域数据产品经理 JD + 专业领域数据工程概念（第十二份 JD，专业领域评测数据层）
- **变更**: 新增 [[摘要-domain-data-product-manager-jd]]（sources）；新增 [[专业领域数据工程]]（concepts——专业领域评测数据层，[[Agent数据产品工程]] 在专业领域的展开）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[专业领域数据工程]] 与 [[Agent数据产品工程]] 为"方法论框架 vs 专业展开"关系——共享同一套评测+数据方法论但面向不同场景；与 [[预训练数据工程]] 为数据形态互补——大规模网络文本 vs 小批量专家质控；与 [[Agent能力工程]] 为维度互补——通用底层能力构建 vs 专业领域评测数据注入）
- **网络**:
  - [[摘要-domain-data-product-manager-jd]] 链接到 [[专业领域数据工程]]/[[Agent数据产品工程]]/[[AI产品工程]]/[[Agent能力工程]]/[[Eval_Harness]]/[[预训练数据工程]]/[[Harness_Engineering]]/[[DeepSeek]]
  - [[专业领域数据工程]] 链接到 [[摘要-domain-data-product-manager-jd]]/[[Agent数据产品工程]]/[[AI产品工程]]/[[Agent能力工程]]/[[Eval_Harness]]/[[预训练数据工程]]/[[Harness_Engineering]]/[[AI训练推理系统工程]]/[[Prompt_Engineering]]/[[Agent沙箱工程]]/[[DeepSeek]]

## [2026-07-15] sync | 新增 AI创作数据产品经理 JD + AI创作数据工程概念（第十三份 JD，评测数据三部曲最终章：创作审美层）
- **变更**: 新增 [[摘要-ai-creative-data-pm-jd]]（sources）；新增 [[AI创作数据工程]]（concepts——评测数据三部曲最终章：将人类审美标准转化为可操作的评测体系与数据管线）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[AI创作数据工程]] 与 [[Agent数据产品工程]]/[[专业领域数据工程]] 构成"评测数据产品三部曲"——同一方法论框架、不同领域展开；与 [[AI搜索工程]] 为协同关系——搜索摘要文本质量依赖本层的写作标准）
- **网络**:
  - [[摘要-ai-creative-data-pm-jd]] 链接到 [[AI创作数据工程]]/[[Agent数据产品工程]]/[[专业领域数据工程]]/[[AI产品工程]]/[[AI搜索工程]]/[[Eval_Harness]]/[[Harness_Engineering]]/[[预训练数据工程]]/[[DeepSeek]]
  - [[AI创作数据工程]] 链接到 [[摘要-ai-creative-data-pm-jd]]/[[Agent数据产品工程]]/[[专业领域数据工程]]/[[AI产品工程]]/[[AI搜索工程]]/[[Eval_Harness]]/[[预训练数据工程]]/[[Agent沙箱工程]]/[[Harness_Engineering]]/[[DeepSeek]]

## [2026-07-15] sync | 新增情感智能数据产品经理 JD + 情感智能数据工程概念（第十四份 JD，评测数据四象限最终章：情感温度层）
- **变更**: 新增 [[摘要-emotional-intelligence-data-pm-jd]]（sources）；新增 [[情感智能数据工程]]（concepts——评测数据四象限最终章：以人类情感认知为基准提升 AI 互动温度）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[情感智能数据工程]] 与 [[Agent数据产品工程]]/[[专业领域数据工程]]/[[AI创作数据工程]] 构成"评测数据四象限"——同一方法论框架/四个不同质量维度；与 [[AI产品工程]] 为产品协作关系——情感陪伴功能的产品体验设计需要本层数据支撑）
- **网络**:
  - [[摘要-emotional-intelligence-data-pm-jd]] 链接到 [[情感智能数据工程]]/[[AI产品工程]]/[[AI创作数据工程]]/[[Agent数据产品工程]]/[[Agent能力工程]]/[[Harness_Engineering]]/[[Eval_Harness]]/[[DeepSeek]]
  - [[情感智能数据工程]] 链接到 [[摘要-emotional-intelligence-data-pm-jd]]/[[Agent数据产品工程]]/[[AI创作数据工程]]/[[专业领域数据工程]]/[[AI产品工程]]/[[Eval_Harness]]/[[Harness_Engineering]]/[[Agent沙箱工程]]/[[Prompt_Engineering]]/[[DeepSeek]]

## [2026-07-15] sync | 新增 Frontier 研究员 JD + Frontier 研究概念（第十五份 JD，范式层：整个堆栈的"种子层"）
- **变更**: 新增 [[摘要-frontier-researcher-jd]]（sources）；新增 [[Frontier研究]]（concepts——范式探索层：超越当前 Scaling Law，寻找下一代范式）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[Frontier研究]] 与所有其他概念的关系不是上下游而是"范式→范式内实践"——如果新范式出现，所有当前概念下的实践都可能需要重新审视；与 [[Agent能力工程]] 为互补——前沿研究定义方向，能力工程师执行）
- **网络**:
  - [[摘要-frontier-researcher-jd]] 链接到 [[Frontier研究]]/[[Agent能力工程]]/[[AI产品工程]]/[[Agent数据产品工程]]/[[知识冲突]]/[[DeepSeek]]
  - [[Frontier研究]] 链接到 [[摘要-frontier-researcher-jd]]/[[Agent能力工程]]/[[AI产品工程]]/[[Agent数据产品工程]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[AI基础设施硬件工程]]/[[Harness_Engineering]]/[[DeepSeek]]

## [2026-07-16] sync | 新增预训练研究员 JD + 预训练研究概念（第16份 JD，当前范式引擎室层）
- **变更**: 新增 [[摘要-pretraining-researcher-jd]]（sources）；新增 [[预训练研究]]（concepts，作为 Frontier 研究之下的"当前范式引擎室层"）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[预训练研究]] 与 [[Frontier研究]] 为"下一个范式 vs 当前范式做到极致"的互补关系——Frontier 质疑 Scaling Law 寻找突破，预训练研究使用 Scaling Law 科学规划；与 [[预训练数据工程]] 为"研究策略 vs 工程实现"的互补关系——前者关注数据与智能的映射关系，后者关注数据处理管线的工程实现；与 [[AI训练推理系统工程]] 为"算法创新 vs 工程化落地"的上下游关系）
- **网络**:
  - [[摘要-pretraining-researcher-jd]] 链接到 [[预训练研究]]/[[预训练数据工程]]/[[Frontier研究]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[AI产品工程]]/[[Agent数据产品工程]]/[[Agent能力工程]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[DeepSeek]]
  - [[预训练研究]] 链接到 [[摘要-pretraining-researcher-jd]]/[[预训练数据工程]]/[[Frontier研究]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[AI产品工程]]/[[Agent数据产品工程]]/[[Agent能力工程]]/[[AI创作数据工程]]/[[情感智能数据工程]]/[[专业领域数据工程]]/[[Harness_Engineering]]/[[Context_Engineering]]/[[DeepSeek]]

## [2026-07-16] sync | 新增后训练研究员 JD + 后训练研究概念（第17份 JD，基座模型释放层）
- **变更**: 新增 [[摘要-posttraining-researcher-jd]]（sources）；新增 [[后训练研究]]（concepts，作为预训练研究之下的"基座模型释放层"——通过 RL 算法、后训练数据与评测三元组释放 Base 模型潜力）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[后训练研究]] 与 [[预训练研究]] 为"基座模型生产 vs 潜力释放"的上下游关系——预训练产生知识渊博的 Base 模型，后训练使其可用、可靠、可控；与 [[Agent能力工程]] 为"教练 vs 训练营"的互补关系——能力工程构建 RL 训练环境，后训练研究提供训练算法和数据策略；与 [[AI训练推理系统工程]] 为"算法设计 vs 工程化落地"的上下游关系）
- **网络**:
  - [[摘要-posttraining-researcher-jd]] 链接到 [[后训练研究]]/[[预训练研究]]/[[Agent能力工程]]/[[AI训练推理系统工程]]/[[Agent数据产品工程]]/[[AI产品工程]]/[[AI创作数据工程]]/[[情感智能数据工程]]/[[专业领域数据工程]]/[[Frontier研究]]/[[Harness_Engineering]]/[[Eval_Harness]]/[[DeepSeek]]
  - [[后训练研究]] 链接到 [[摘要-posttraining-researcher-jd]]/[[预训练研究]]/[[Agent能力工程]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[AI产品工程]]/[[Agent数据产品工程]]/[[AI创作数据工程]]/[[情感智能数据工程]]/[[专业领域数据工程]]/[[Frontier研究]]/[[Harness_Engineering]]/[[Eval_Harness]]/[[Context_Engineering]]/[[DeepSeek]]

## [2026-07-16] sync | 新增多模态理解研究员 JD + 多模态理解研究概念（第18份 JD，与文本体系平行的多模态维度）
- **变更**: 新增 [[摘要-multimodal-understanding-researcher-jd]]（sources）；新增 [[多模态理解研究]]（concepts，作为与文本模型体系平行的"多模态维度"——视觉编码器/VLM/多模态预训练与后训练/多模态数据与评测全链路）；更新 [[index]]（Sources + Concepts 各添加条目）
- **冲突**: 无（全新知识领域；[[多模态理解研究]] 与所有现有概念不是"上下游"关系而是"平行维度"关系——多模态共享文本体系的基础设施（训练框架/计算/集群/存储），但在架构设计、训练方法、数据策略、评测标准上有其独特性；与 [[预训练数据工程]] 的多模态数据处理章节为"研究策略 vs 工程实现"的互补）
- **网络**:
  - [[摘要-multimodal-understanding-researcher-jd]] 链接到 [[多模态理解研究]]/[[预训练数据工程]]/[[后训练研究]]/[[Agent能力工程]]/[[Agent_Interfaces]]/[[AI产品工程]]/[[Agent数据产品工程]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[AI搜索工程]]/[[预训练研究]]/[[Frontier研究]]/[[Harness_Engineering]]/[[DeepSeek]]
  - [[多模态理解研究]] 链接到 [[摘要-multimodal-understanding-researcher-jd]]/[[预训练数据工程]]/[[后训练研究]]/[[预训练研究]]/[[Agent能力工程]]/[[Agent_Interfaces]]/[[AI产品工程]]/[[Agent数据产品工程]]/[[AI训练推理系统工程]]/[[AI计算引擎工程]]/[[超算集群工程]]/[[AI搜索工程]]/[[Frontier研究]]/[[AI创作数据工程]]/[[情感智能数据工程]]/[[Harness_Engineering]]/[[Eval_Harness]]/[[DeepSeek]]

## [2026-07-16] lint | 修复 15 个死链 + 创建 2 个缺失页面 + 索引对齐
- **修复死链**:
  - 10 处 `[[DeepSeek五份JD全景对比]]` → `[[DeepSeek四份JD全景对比]]`（AI产品工程/AI存储工程/AI计算引擎工程/AI训练推理系统工程/超算集群工程 + 5 个源摘要）
  - 1 处 `[[Agentic Coding]]` → `[[Agentic_Coding]]`（Agent能力工程）
  - 2 处 `[[Hermes Agent]]` → `[[Hermes_Agent]]`（Slack/Telegram）
- **创建缺失页面**: 新增 [[知识冲突]]（concepts——知识库中已有的冲突管理实践理论化文档化）；新增 [[API设计]]（entities——预留链接完整化）
- **索引对齐**: [[知识冲突]] 注册到 Concepts 章节；[[API设计]] 注册到 Entities 章节
- **其他修复**: 图片引用（[[Pasted image 20260706174748.png]]）排除为非死链；`\`结尾转义问题（GPT/Self_Attention/Transformer_Architecture）确认为正则匹配边界限制而非真实死链；已合并 1 处锚点链接触达（摘要-多模态理解研究 -> 预训练数据工程#3. 多模态数据处理）
- **结果**: 0 死链、0 孤岛、0 未同步索引、知识库健康状态良好
- **冲突**: 无

## [2026-07-16] sync | 补齐算法应用开发工程师 JD 相关知识库缺口（3 实体 + 1 概念 + 2 扩展）
- **变更**: 
  - **新增概念**: [[Parameter_Efficient_Fine_Tuning]] — 参数高效微调（PEFT/LoRA/QLoRA/P-Tuning），JD 中模型微调要求的最大知识缺口
  - **新增实体**: [[Weights_and_Biases]]、[[MLflow]]、[[Ray]] — MLOps 工具链三件套，JD 加分项
  - **大幅更新**: [[RAG]] — 新增完整 Embedding 模型选型指南章节（主流 9 模型对比/选型决策树/维度分析/检索模式对比/评估指标）
  - **大幅更新**: [[AI训练推理系统工程]] — 新增推理引擎横向对比表（vLLM/TGI/SGLang/TensorRT-LLM/llama.cpp 六大维度）
  - **更新 [[index]]** — Concepts 章节新增 [[Parameter_Efficient_Fine_Tuning]]；Entities 章节新增 [[Weights_and_Biases]]、[[MLflow]]、[[Ray]]；[[RAG]] 和 [[AI训练推理系统工程]] 描述更新
- **冲突**: 无（所有新内容为知识库增量补充，与现有页面无矛盾；[[Parameter_Efficient_Fine_Tuning]] 与 [[Model_Fine_Tuning]] 为"一般 vs 具体"的父子关系，[[Model_Fine_Tuning]] 侧重微调对模型性格的影响，[[Parameter_Efficient_Fine_Tuning]] 侧重参数高效微调的技术细节与工程实践，互补无矛盾）
- **网络**: 
  - [[Parameter_Efficient_Fine_Tuning]] 链接到 [[Model_Fine_Tuning]]/[[后训练研究]]/[[AI训练推理系统工程]]/[[预训练数据工程]]/[[RAG]]/[[Harness_Engineering]]/[[Cost_Optimization]]/[[摘要-算法应用开发工程师-jd]]
  - [[Weights_and_Biases]] 链接到 [[MLflow]]/[[Ray]]/[[Agent_Observability]]/[[Eval_Harness]]/[[Cost_Optimization]]/[[摘要-算法应用开发工程师-jd]]
  - [[MLflow]] 链接到 [[Weights_and_Biases]]/[[Ray]]/[[Eval_Harness]]/[[Agent_Observability]]/[[AI训练推理系统工程]]/[[摘要-算法应用开发工程师-jd]]
  - [[Ray]] 链接到 [[Weights_and_Biases]]/[[MLflow]]/[[AI训练推理系统工程]]/[[Eval_Harness]]/[[Cost_Optimization]]/[[Agent沙箱工程]]/[[摘要-算法应用开发工程师-jd]]
- **变更**: 新增 [[摘要-算法应用开发工程师-jd]]（sources）；更新 [[index]]（Sources 章节添加条目）
- **冲突**: 无（全新 JD，与已有 DeepSeek 系列 JD 形成"应用层 vs 基础设施/研究层"的垂直互补关系，无矛盾）
- **网络**: 
  - [[摘要-算法应用开发工程师-jd]] 链接到 [[Agent_Loop]]/[[Tool_Calling]]/[[RAG]]/[[Chunking]]/[[Context_Engineering]]/[[Harness_Engineering]]/[[Model_Fine_Tuning]]/[[Prompt_Engineering]]/[[Transformer_Architecture]]/[[Multi_Agent_System]]/[[Eval_Harness]]/[[Agent_Observability]]/[[Cost_Optimization]]/[[Agent_Orchestration_Patterns]]/[[LangChain]]/[[AutoGen]]/[[DeepSeek四份JD全景对比]]

## [2026-07-16] sync | 从 YouTube 转录 Karpathy micrograd 视频，生成 Obsidian 笔记 + Canvas 概念图
- **变更**: 新增 [[raw/01-articles/Karpathy_micrograd_neural_networks_backpropagation]]（sources——Karpathy micrograd 视频的结构化笔记，含 frontmatter/WikiLinks/Callouts）；新增 [[raw/01-articles/micrograd_concept_map]]（canvas——micrograd 概念关系可视化图）
- **冲突**: 无（笔记内容为教学性理论知识，与现有概念体系互补无矛盾——[[AI训练推理系统工程]]/[[预训练研究]]/[[后训练研究]]/[[Agent能力工程]]/[[Harness_Engineering]] 等均与本笔记建立关联）
- **网络**:
  - [[raw/01-articles/Karpathy_micrograd_neural_networks_backpropagation]] 链接到 [[AI训练推理系统工程]]/[[预训练研究]]/[[后训练研究]]/[[Agent能力工程]]/[[Prompt_Engineering]]/[[Harness_Engineering]]/[[预训练数据工程]]/[[Frontier研究]]
  - [[raw/01-articles/micrograd_concept_map]] 是 micrograd 的概念可视化 Canvas，呈现 Value 类 → 神经网络 → 训练循环 → 现实世界映射四层架构

## [2026-07-16] ingest | 摄入 Karpathy micrograd 文章 — 反向传播/自动求导/计算图
- **变更**: 新增 [[摘要-karpathy-micrograd-neural-networks-backpropagation]]（sources）；新增 [[Micrograd]]（entities）；新增 [[Backpropagation]]、[[Autograd]]、[[Computation_Graph]]（concepts）；更新 [[Andrej_Karpathy]]（补充 micrograd 项目 + 新来源引用）；更新 [[index]]（Sources + Entities + Concepts 各添加条目）
- **冲突**: 无（所有新概念均为首次引入的知识域，与现有概念体系互补无矛盾——[[Backpropagation]] 是 [[AI训练推理系统工程]]/[[预训练研究]]/[[后训练研究]] 的底层数学机制；[[Autograd]] 与 [[Micrograd]] 互为实现与抽象；[[Computation_Graph]] 是 [[Backpropagation]] 的数据结构基础）
- **网络**:
  - [[摘要-karpathy-micrograd-neural-networks-backpropagation]] 链接到 [[Micrograd]]/[[Andrej_Karpathy]]/[[Backpropagation]]/[[Autograd]]/[[Computation_Graph]]/[[AI训练推理系统工程]]/[[预训练研究]]/[[后训练研究]]/[[Agent能力工程]]/[[Harness_Engineering]]/[[Prompt_Engineering]]/[[预训练数据工程]]
  - [[Micrograd]] 链接到 [[Andrej_Karpathy]]/[[摘要-karpathy-micrograd-neural-networks-backpropagation]]/[[Backpropagation]]/[[Autograd]]/[[Computation_Graph]]/[[GPT]]/[[AI训练推理系统工程]]
  - [[Backpropagation]] 链接到 [[摘要-karpathy-micrograd-neural-networks-backpropagation]]/[[Micrograd]]/[[Autograd]]/[[Computation_Graph]]/[[AI训练推理系统工程]]/[[预训练研究]]/[[后训练研究]]/[[Agent能力工程]]
  - [[Autograd]] 链接到 [[摘要-karpathy-micrograd-neural-networks-backpropagation]]/[[Micrograd]]/[[Backpropagation]]/[[Computation_Graph]]/[[AI训练推理系统工程]]
  - [[Computation_Graph]] 链接到 [[摘要-karpathy-micrograd-neural-networks-backpropagation]]/[[Micrograd]]/[[Backpropagation]]/[[Autograd]]/[[AI训练推理系统工程]]

## [2026-07-17] query | 整理四位AI教育者（吴恩达/李宏毅/李沐/Karpathy）综合对比
- **变更**: 新增 [[四位AI教育者对比-吴恩达-李宏毅-李沐-Karpathy]]（syntheses）；新增 [[Andrew_Ng]]、[[Hung_yi_Lee]]、[[Mu_Li]]（entities）；更新 [[index]]（Entities 添加 3 条目 + Syntheses 添加 1 条目）
- **冲突**: 无（三位教育者知识域独立，与 Karpathy 已有实体形成互补关系）
- **网络**:
  - [[四位AI教育者对比-吴恩达-李宏毅-李沐-Karpathy]] 链接到 [[Andrew_Ng]]/[[Hung_yi_Lee]]/[[Mu_Li]]/[[Andrej_Karpathy]]/[[GPT]]/[[Transformer_Architecture]]/[[Backpropagation]]/[[Micrograd]]/[[摘要-gpt-from-scratch]]/[[摘要-karpathy-micrograd-neural-networks-backpropagation]]
  - [[Andrew_Ng]] 链接到 [[Mu_Li]]/[[Andrej_Karpathy]]/[[Hung_yi_Lee]]
  - [[Hung_yi_Lee]] 链接到 [[Andrew_Ng]]/[[Andrej_Karpathy]]/[[Mu_Li]]
  - [[Mu_Li]] 链接到 [[Andrew_Ng]]/[[Andrej_Karpathy]]/[[Hung_yi_Lee]]

## [2026-07-17] query | 补充李飞飞（Fei-Fei Li）至 AI 教育者对比文档
- **变更**: 新增 [[Fei-Fei_Li]]（entities）；大幅更新 [[四位AI教育者对比-吴恩达-李宏毅-李沐-Karpathy]]（新增李飞飞人物简介、课程对照列、CS231n 详情章节、人群匹配、风格对比 — 从四→五位教育者）；更新 [[Andrej_Karpathy]]（关联连接添加 [[Fei-Fei_Li]]）；更新 [[index]]（Entities + Syntheses 更新）
- **冲突**: 无（李飞飞知识域独立，与 Karpathy 的师生关系已在双方页面标注）
- **网络**:
  - [[Fei-Fei_Li]] 链接到 [[Andrej_Karpathy]]/[[Andrew_Ng]]/[[Mu_Li]]/[[Hung_yi_Lee]]/[[Transformer_Architecture]]/[[GPT]]
  - [[四位AI教育者对比-吴恩达-李宏毅-李沐-Karpathy]] 新增 [[Fei-Fei_Li]] 链接


## [2026-07-22] sync | 补充五个知识缺口：KV Cache 存储系统/Plan-Execute 展开/可编程 Skills/Benchmark 对比/Agent DX 设计
- **变更**:
  - **新增概念 (3)**: [[KV_Cache_Storage_Systems]] — KV Cache 分布式存储独立概念页（从 [[AI存储工程]] 分离展开）；[[Programmable_Skills]] — Skill 动态加载/热更新/权限管控/生命周期管理等工程化治理；[[Agent_DX_Design]] — Agent 场景下的开发者体验设计六项核心要求
  - **新增综合报告 (1)**: [[Agent_Benchmark_Landscape]] — SWE-bench/GAIA/AgentBench/WebArena/OSWorld/τ-bench/RE-bench 等 7 大主流 Agent 评测基准的深度对比分析
  - **大幅扩展 (1)**: [[Hierarchical_Task_Decomposition]] — 追加完整的 Plan-Execute 工程实践章节（Plan 契约输出/Execute 执行模式对比/反馈循环与 Replan 触发/三种实现模式/常见陷阱）
  - **更新 [[index]]** — Concepts 添加 3 条目 + Syntheses 添加 1 条目
- **冲突**: 无（所有新增页面均为现有知识框架的补充展开，与既有概念互补无矛盾——KV_Cache_Storage_Systems 是 AI存储工程 子系统的独立深化；Programmable_Skills 是 Claude_Code_Skills 的工程化治理层，Skills权限管理 是其权限维度的子集；Agent_DX_Design 是 API设计 在 Agent 场景的扩展；Agent_Benchmark_Landscape 是 Eval_Harness 中 Benchmark Landscape 的独立展开；Hierarchical_Task_Decomposition 的 Plan-Execute 展开与 Agent_Loop/Spec_Driven_Development 互补无矛盾）
- **网络**:
  - [[KV_Cache_Storage_Systems]] 链接到 [[AI存储工程]]/[[AI训练推理系统工程]]/[[Harness_Engineering]]/[[Cost_Optimization]]/[[Agent_Loop]]/[[超算集群工程]]/[[AI搜索工程]]/[[Agent沙箱工程]]/[[摘要-hpc-distributed-storage-jd]]
  - [[Programmable_Skills]] 链接到 [[Claude_Code_Skills]]/[[Skills权限管理]]/[[Skill_Factory]]/[[MCP]]/[[Claude_Code_Plugins]]/[[Claude_Code_Hooks]]/[[Claude_Code_Dynamic_Workflows]]/[[Progressive_Disclosure]]/[[Agent沙箱工程]]/[[Harness_Engineering]]/[[Claude_Code_Harness]]
  - [[Agent_DX_Design]] 链接到 [[API设计]]/[[Progressive_Disclosure]]/[[Agent_Observability]]/[[Harness_Engineering]]/[[Claude_Code_Skills]]/[[Claude_Code_Hooks]]/[[Claude_Code_Subagent]]/[[MCP]]/[[Contract_Driven_Handoffs]]/[[Work_Boundary]]/[[Skills权限管理]]/[[From_NoCode_To_Agent_Paradigm]]/[[Agent沙箱工程]]
  - [[Agent_Benchmark_Landscape]] 链接到 [[Eval_Harness]]/[[Harness_Engineering]]/[[Agent能力工程]]/[[Agent数据产品工程]]/[[后训练研究]]/[[Agent_Observability]]/[[Cost_Optimization]]/[[promptfoo]]/[[langfuse]]/[[AI产品工程]]
  - [[Hierarchical_Task_Decomposition]] 新增链接到 [[Agent_Loop]]/[[Spec_Driven_Development]]/[[Cost_Aware_Budget_Gates]]/[[Claude_Code_Subagent]]/[[Tool_Calling]]/[[摘要-agent-loop-guide]]

## [2026-07-22] ingest | 摄入 DevOps AI 架构师 JD（厦门）
- **变更**: 新增 [[摘要-devops-ai-architect-xiamen]]（sources）；更新 [[index]]（Sources 章节添加条目）
- **冲突**: 无（该 JD 聚焦 **LLM × DevOps 融合**方向，与已有 [[摘要-智能体研发工程师-jd]]（Agent Infra 平台）和 [[摘要-算法应用开发工程师-jd]]（算法落地）形成互补——三者覆盖 AI 工程化的三个不同截面：平台层、应用层、效能层）
- **网络**:
  - [[摘要-devops-ai-architect-xiamen]] 链接到 [[Harness_Engineering]]/[[企业级LLM应用架构]]/[[AI驱动的CICD]]/[[智能排障系统]]/[[LLM Gateway模式]]/[[Agent_Loop]]/[[Agent_Observability]]/[[MCP]]/[[Agent_Orchestration_Patterns]]/[[Multi_Agent_System]]/[[Tool_Calling]]/[[RAG]]/[[Cost_Optimization]]/[[摘要-智能体研发工程师-jd]]/[[摘要-算法应用开发工程师-jd]]/[[摘要-deepseek-agent-infra-jd]]

## [2026-07-22] sync | 补充三个缺失概念：LLM Gateway 模式/AI 驱动 CICD/智能排障系统
- **变更**: 新增 [[LLM_Gateway模式]]、[[AI驱动的CICD]]、[[智能排障系统]]（concepts）；更新 [[index]]（Concepts 章节添加 3 条目）
- **冲突**: 无（三个新概念均为 [[摘要-devops-ai-architect-xiamen]] 中引用的知识域，与既有概念体系互补——LLM Gateway 模式是 Cost_Optimization/MCP 的基础设施承接层；AI驱动的CICD 是 Agent_Loop/Agent_Orchestration_Patterns 在 DevOps 场景的垂直实践；智能排障系统 是 Agent_Observability/AI集群可靠性工程 在故障处理场景的工程化展开）
- **网络**:
  - [[LLM_Gateway模式]] 链接到 [[Harness_Engineering]]/[[MCP]]/[[微服务与API网关设计]]/[[Cost_Optimization]]/[[Agent_Observability]]/[[Agent沙箱工程]]/[[摘要-devops-ai-architect-xiamen]]
  - [[AI驱动的CICD]] 链接到 [[Harness_Engineering]]/[[Agent_Loop]]/[[Agent_Orchestration_Patterns]]/[[Tool_Calling]]/[[MCP]]/[[Eval_Harness]]/[[Agent_Observability]]/[[Cost_Optimization]]/[[AI集群可靠性工程]]/[[摘要-devops-ai-architect-xiamen]]
  - [[智能排障系统]] 链接到 [[Harness_Engineering]]/[[Agent_Loop]]/[[Agent_Observability]]/[[AI集群可靠性工程]]/[[Tool_Calling]]/[[MCP]]/[[RAG]]/[[Cost_Optimization]]/[[摘要-devops-ai-architect-xiamen]]

## [2026-07-22] sync | 补充两个知识缺口：Vue 在效能平台中的应用 / Redis 在效能平台中的应用
- **变更**: 新增 [[Vue在效能平台中的应用]]、[[Redis在效能平台中的应用]]（concepts）；更新 [[index]]（Concepts 章节添加 2 条目）
- **冲突**: 无（两个新概念均为 [[摘要-devops-ai-architect-xiamen]] 的标签补充，与既有概念体系互补——Vue 概念是效能平台的前端技术层展开；Redis 概念是中间件层展开，与 Cost_Optimization/微服务与API网关设计 形成缓存策略的完整链路）
- **网络**:
  - [[Vue在效能平台中的应用]] 链接到 [[AI驱动的CICD]]/[[智能排障系统]]/[[Agent_Observability]]/[[微服务与API网关设计]]/[[摘要-devops-ai-architect-xiamen]]
  - [[Redis在效能平台中的应用]] 链接到 [[AI驱动的CICD]]/[[智能排障系统]]/[[LLM_Gateway模式]]/[[Cost_Optimization]]/[[Vue在效能平台中的应用]]/[[微服务与API网关设计]]/[[摘要-devops-ai-architect-xiamen]]

## [2026-07-22] lint | 知识库健康检查
- **变更**: 修复 [[摘要-devops-ai-architect-xiamen]] 中 1 个死链（[[LLM Gateway模式]] → [[LLM_Gateway模式]]）；移除 2 个不存在的链接引用
- **冲突**: 无
- **发现**:
  - 索引一致性：✅ 所有链接均有对应文件，所有文件均已注册
  - 全库死链 27 个（多数为节级锚点链接 `[[Page#Heading]]` 的语法误报，少量为确实不存在的页面如 [[知识管理]]、[[SWE-bench]]、[[Function_Calling]]）
  - 孤儿页面 9 个（为近期新增的概念页，尚未被广泛引用）
  - 知识冲突 20 个（均为既有、设计内的知识冲突记录，非新增问题）

## [2026-07-22] sync | 新增 DevOps AI 架构师 JD 全景对标分析
- **变更**: 新增 [[DevOpsAI架构师JD全景对标分析]]（syntheses）；更新 [[index]]（Syntheses 章节添加条目）
- **冲突**: 无（该报告与 [[智能体研发工程师JD对标分析]] 和 [[DeepSeek四份JD全景对比]] 形成三足鼎立——分别覆盖 Agent 平台方向、DeepSeek 系列方向、DevOps AI 架构师方向）
- **网络**:
  - [[DevOpsAI架构师JD全景对标分析]] 链接到 [[摘要-devops-ai-architect-xiamen]]/[[摘要-智能体研发工程师-jd]]/[[摘要-算法应用开发工程师-jd]]/[[摘要-deepseek-harness-team-jd]]/[[DeepSeek四份JD全景对比]]/[[智能体研发工程师JD对标分析]]/[[Harness_Engineering]]

## [2026-07-22] sync | 新增 DevOps AI 架构师面试深度准备
- **变更**: 新增 [[DevOpsAI架构师面试深度准备]]（syntheses）；更新 [[index]]（Syntheses 章节添加条目）
- **冲突**: 无（与 [[DevOpsAI架构师JD全景对标分析]] 形成互补——对标报告回答"这是什么岗位"，面试准备回答"怎么准备这个岗位的面试"）
- **网络**:
  - [[DevOpsAI架构师面试深度准备]] 链接到 [[摘要-devops-ai-architect-xiamen]]/[[DevOpsAI架构师JD全景对标分析]]/[[Harness_Engineering]]/[[AI驱动的CICD]]/[[智能排障系统]]/[[LLM_Gateway模式]]/[[Cost_Optimization]]/[[Graceful_Degradation]]/[[Agent_Loop]]/[[Agent_Observability]]/[[Vue在效能平台中的应用]]/[[Redis在效能平台中的应用]]

## [2026-07-22] sync | 补全 K8s/CI-CD 平台知识 + 修复死链 + 打破孤儿页面
- **变更**:
  - **新增概念 (2)**: [[Kubernetes在效能平台中的应用]] — K8s 在 DevOps Agent 场景的核心应用（CI Runner 集群/Agent 沙箱/Operator 模式）；[[CICD平台对比与AI集成]] — Jenkins/GitLab CI/GitHub Actions 的对比与 AI 集成模式
  - **新增概念 (1)**: [[知识管理]] — 知识管理基础方法论，与 [[知识冲突]] 形成互补
  - **新增实体 (1)**: [[SWE-bench]] — 软件工程 Agent 评测基准
  - **修复死链 (5)**: [[Function_Calling]]→[[Tool_Calling]]（API设计.md）；[[Skills]]→[[Claude_Code_Skills]]（智能体研发工程师JD对标分析）；[[摘要-预训练数据工程师-jd.md]]→[[摘要-预训练数据工程师-jd]]（预训练数据工程.md + 预训练数据四方向对比.md）；[[企业级LLM应用架构]]/[[效能研发工程师技能图谱]] 移除（摘要-devops-ai-architect-xiamen）
  - **打破孤儿页面 (7)**: [[Agent_DX_Design]] ← Harness_Engineering；[[Agent实例生命周期管理]] ← Agent_Loop；[[Programmable_Skills]] ← Claude_Code_Skills；[[KV_Cache_Storage_Systems]] ← AI存储工程；[[Dify]] ← LangChain；[[Agent_Benchmark_Landscape]] ← Eval_Harness；[[四位AI教育者对比]] ← Andrej_Karpathy
  - **修复孤岛交叉链接 (2)**: [[企业系统集成模式]] ← MCP + CICD平台对比与AI集成
- **更新 [[index]]** — Concepts 添加 4 条目（K8s/CICD平台/Vue/Redis）+ Entities 添加 1 条目（SWE-bench）+ 修复 1 条死链（指数退避→Exponential_Backoff）
- **冲突**: 无（所有新增页面均为既有框架的补充展开）
