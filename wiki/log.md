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
