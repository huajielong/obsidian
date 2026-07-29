---
title: "摘要-Claude Code六重境界"
type: source
tags: [来源, Claude Code, 能力进阶]
sources: [Clippings/Claude Code六重境界.md]
last_updated: 2026-07-28
---

## 核心摘要

该视频由 云桥网络 出品，提出了 Claude Code 使用的六层境界模型，从基础的提示词工程到高级的多 Agent 规模化编排。每层境界对应一组核心技能和常见陷阱：

- **第一层 · 提示工程师**：基础指令式使用，将 Claude Code 视为简单工具而非合作伙伴。陷阱是"回归平庸"——产出千篇一律的 AI 垃圾。核心技能：编写清晰具体的提示词、学会阅读和评判 AI 生成内容、基本终端知识。
- **第二层 · 规划者**：启用计划模式（Plan Mode），从单向指令转向双向协作。核心技能：掌握计划模式、协作式提问（"我漏掉了什么？"）、要求 Claude Code 对构思提出挑战/扮演对抗角色。
- **第三层 · 上下文工程师**：引入外部上下文信息（文件、截图、事例）。核心技能：上下文窗口管理、理解上下文腐败机制（50-60% 窗口填充即触发性能衰减）、使用 /clear 重置窗口（慎用 /compact）。
- **第四层 · MCP/工具集成**：接入 MCP 服务器、框架（如 GSD）等外部能力。核心技能：理解基本构建模块（前端/后端/数据库/认证等）、让 Claude Code 解释其工作原理、外科手术式精准选配工具而非盲目堆积。
- **第五层 · 技能/工作流**：创建和定制自定义 Skills，将重复性工作流封装。核心技能：Skill 编写能力、使用 Skill Creator 评估和优化技能、技能组合叠套。技能是让 Claude Code 真正成为"专属工具"的关键。
- **第六层 · 规模化编排**：同时协调多个 Claude Code 实例。四种方式：(1) 多终端会话并行工作；(2) Git Worktrees 隔离工作副本；(3) 子代理自动化（主终端派生子代理到不同 Worktree）；(4) 代理团队（Agent Teams）实验性功能——子代理之间可互相通信协作。

视频强调从"AI 工具使用者"到"AI 协作者"的思维转变是贯穿全文的核心主线，并重点介绍了上下文腐败机制、CLAUDE.md 的正确使用方法、以及代理团队（Agent Teams）功能。

## 关联连接

- [[Claude_Code]] — 视频核心对象
- [[Claude_Code_六重境界]] — 六层境界框架
- [[上下文腐败]] — 上下文窗口性能衰减机制
- [[Context_Window]] — 上下文窗口基础概念
- [[Context_Engineering]] — 三层工程模型的第二层
- [[Prompt_Engineering]] — 三层工程模型的第一层
- [[Claude_Code_Skills]] — 第五层技能系统的行为层
- [[Claude_Code_Subagent]] — 第六层子代理机制
- [[Multi_Agent_System]] — Agent Teams 所属的多 Agent 系统
- [[MCP]] — 第四层的核心扩展能力
