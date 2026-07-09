## [2026-07-09] ingest | 增量合并实验系列更新版（云端数据补全）

- **变更**:
  - 更新 [[摘要-ollama-style-comparison]] — 补全 DeepSeek + 豆包云端实际数据（原为"待补充"）
  - 更新 [[摘要-ollama-experiment-index]] — 补充云端 API 对比结论
  - 更新 [[DeepSeek]] — 增加 V4 Pro 风格对比基准 + 辩论式结构描述
  - 更新 [[Doubao]] — 增加风格对比基准数据 + 条理清晰描述
- **冲突**: 模型名称差异（实验五用 DeepSeek V4 Flash，实验七用 V4 Pro）→ 已在 DeepSeek 页面标注说明，两者分属不同版本
- **网络**: [[DeepSeek]] 和 [[Doubao]] 新增风格对比数据，与 [[Ollama]]/[[Llama]]/[[Qwen]] 对比更完整

## [2026-07-09] lint | 知识库健康巡检与修复

- **结果**:
  - 修复 1 个死链：新建 [[Feynman_Technique]]（被 [[Naval_Rapid_Research_Method]]、[[Naval_Ravikant]] 引用）
  - 消除 9 个孤儿页面：在 [[Ollama]]、[[DeepSeek]]、[[Doubao]]、[[BPE_Tokenizer]]、[[Temperature_Parameter]]、[[Model_Fine_Tuning]] 中追加来源摘要反链
  - 修复 1 处格式：`[[Harness_Engineering.md]]` → `[[Harness_Engineering]]`
- **当前状态**: 0 死链、0 孤岛、0 知识冲突

## [2026-07-03] ingest | 引入 AI 时代 Git 版本管理文章

- **变更**: 新增 [[摘要-ai-era-git-management]]; 新增实体 [[TRAE_ai]], [[Jujutsu]], [[GitButler]]; 新增概念 [[Agentic_Coding]], [[Agent_Aware_Commit]], [[Atomic_Commit]], [[Checkpoint_Commit]], [[Commit_Trailer]], [[Stacked_PR]], [[Virtual_Branch]], [[Feature_Branch_Workflow]], [[AGENT_MD]], [[Monorepo]]; 更新 [[index.md]]
- **冲突**: 无（全新知识库，无已有页面冲突）

## [2026-07-03] ingest | 引入 Claude Code 完全指南

- **变更**: 新增 [[摘要-claude-code-guide]]; 新增实体 [[Claude_Code]], [[Anthropic]]; 新增概念 [[Claude_Code_Slash_Commands]], [[Claude_Code_Memory_System]], [[Claude_Code_Workflow]]; 更新 [[index.md]], [[AGENT_MD]]
- **冲突**: 无（全新知识库，无已有页面冲突）

## [2026-07-03] ingest | 摄入 OpenAI Harness Engineering 官方文章

- **变更**: 新增 [[Harness_Engineering]], [[摘要-openai-harness-engineering]]; 更新 [[index.md]]
- **冲突**: 与 [[Agentic_Coding]] 的关系已在 [[Harness_Engineering]] 页面中辨析对比

## [2026-07-03] ingest | 全量摄入 raw/01-articles 38个文件

- **变更**: 
  - 新增源摘要 [[摘要-agent-first-engineering]], [[摘要-claude-code-boris-cherny]], [[摘要-claude-code-hud]], [[摘要-claude-code-gsd-core]], [[摘要-agent-loop-guide]], [[摘要-openclaw-info]], [[摘要-agentic-ai-roadmap]]
  - 新增实体 [[OpenClaw]], [[Boris_Cherny]], [[GSD_Core]]
  - 新增概念 [[Agent_First_Engineering]], [[Agent_Loop]], [[Claude_Code_Skills]]
  - 更新 [[Claude_Code]], [[AGENT_MD]], [[index.md]]
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
- **目录完整性**: 全部 38 个文件均在 [[wiki/index]] 中列出，无遗漏
- **微小问题**: [[摘要-openai-harness-engineering]] 有重复链接区块；[[Claude_Code_Workflow]] 中 [[Claude_Code]] 链接重复 — **已修复**
- **结果**: 知识库健康状态良好

## [2026-07-06] ingest | 引入 AI 大模型驾驭进阶罗盘

- **变更**: 新增 [[AI_Mastery_Compass]]；更新 [[index.md]]
- **冲突**: 无（全新概念，与传统 Prompt 模板收藏路线无直接冲突）

## [2026-07-06] lint | 修复死链和孤儿页面

- **新增**: [[Prompt_Engineering]] (修复 AI_Mastery_Compass 中的死链)
- **修复**: 为 [[AI_Mastery_Compass]] 在 [[Agentic_Coding]], [[Agent_Loop]], [[Harness_Engineering]], [[Claude_Code_Skills]] 中添加反向链接 (修复 1 个孤岛)
- **结果**: 1 死链已修复, 1 孤岛已消除; 知识库健康状态良好

## [2026-07-06] ingest | 引入 Google ADK Skill 系统文章并修复位置违规

- **变更**: 
  - **迁移**: 修复违规，将 `developers-guide-to-building-adk-agents-with-skills.md` 从 vault 根目录移至 [[wiki/sources/摘要-adk-agents-with-skills.md]]
  - **新增**: 实体 [[ADK]]; 概念 [[Progressive_Disclosure]], [[Skill_Factory]]
  - **更新**: 为 [[Claude_Code_Skills]], [[Harness_Engineering]], [[Agentic_Coding]] 添加反向链接
  - **更新**: [[wiki/index.md]] 总目录
  - **归档**: 原始内容同时保存至 `raw/09-archive/`
- **冲突**: 无（新增概念与现有知识互补，无直接冲突）

## [2026-07-07] ingest | 引入纳瓦尔极速研究法

- **变更**:
  - 新增概念 [[Naval_Rapid_Research_Method]] — 纳瓦尔 7 步从零掌握任意新领域的方法论
  - 新增实体 [[Naval_Ravikant]] — 硅谷天使投资人与思想家
  - 更新 [[index.md]] 总目录，为 [[Naval_Ravikant]] 和 [[Naval_Rapid_Research_Method]] 建立条目
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
  - 更新 [[index.md]] 总目录
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
  - 更新 [[index.md]] 总目录
- **冲突**: 无（新知识独立，与现有 LLM 基础概念互补）
- **网络**: [[BPE_Tokenizer]] ↹ [[GPT]]/[[Transformer_Architecture]]；[[Temperature_Parameter]] ↹ [[OpenAI_Compatible_API]]；[[Model_Fine_Tuning]] ↹ [[Ollama]]/[[Qwen]]/[[Llama]]

## [2026-07-06] ingest | 引入 Karpathy GPT 从零构建视频教程

- **变更**: 
  - 新增源 [[摘要-gpt-from-scratch]] — Andrej Karpathy 的 Zero to Hero 系列 GPT 构建教程
  - 新增实体 [[Andrej_Karpathy]] — AI 研究科学家与教育者
  - 新增概念 [[GPT]], [[Transformer_Architecture]], [[Self_Attention]] — Transformer 核心知识体系
  - 更新 [[index.md]] 总目录
  - 为 [[Andrej_Karpathy]], [[GPT]], [[Transformer_Architecture]], [[Self_Attention]] 建立双向链接网络
- **冲突**: 无（全新领域知识，与现有 Agentic Coding 知识体系互补）
- **源**: YouTube 视频 https://www.youtube.com/watch?v=kCc8FmEb1nY
