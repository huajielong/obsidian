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
- **知识冲突**: 1 处 — [[Harness_Engineering.md]] 中已标注，无需干预
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

## [2026-07-06] ingest | 引入 Karpathy GPT 从零构建视频教程

- **变更**: 
  - 新增源 [[摘要-gpt-from-scratch]] — Andrej Karpathy 的 Zero to Hero 系列 GPT 构建教程
  - 新增实体 [[Andrej_Karpathy]] — AI 研究科学家与教育者
  - 新增概念 [[GPT]], [[Transformer_Architecture]], [[Self_Attention]] — Transformer 核心知识体系
  - 更新 [[index.md]] 总目录
  - 为 [[Andrej_Karpathy]], [[GPT]], [[Transformer_Architecture]], [[Self_Attention]] 建立双向链接网络
- **冲突**: 无（全新领域知识，与现有 Agentic Coding 知识体系互补）
- **源**: YouTube 视频 https://www.youtube.com/watch?v=kCc8FmEb1nY
