---
title: "摘要-Claude Code 完全指南"
type: source
tags: [来源, Claude, AI编程, 开发工具]
sources: [raw/01-articles/Claude Code 完全指南 - 阿里云开发者社区.md]
last_updated: 2026-07-03
---

## 核心摘要

本文来自阿里云开发者社区，是一份 Claude Code（Anthropic 推出的终端 AI 编码助手）的全面使用指南。文章系统介绍了 Claude Code 的基础命令、界面布局、三种工作模式（Default/Auto-Accept/Plan）、完整的斜杠命令体系（/init、/memory、/compact、/clear、/status、/cost、/config、/model、/doctor 等），以及三层记忆系统（Project Memory / User Memory / Auto Memory）。在此基础上，文章提出了一套六步开发工作流方法论，涵盖项目初始化、代码理解、功能规划、分模块执行、性能优化和记忆沉淀，并给出了不同开发阶段模式与模型的选用建议。

## 关键要点

- **三种工作模式**：Default（逐次确认）、Auto-Accept（自动执行文件修改）、Plan（只读规划），通过 Shift+Tab 循环切换
- **核心斜杠命令**：/init（初始化项目记忆）、/memory（编辑记忆文件）、/compact（压缩上下文）、/clear（清空历史）、/status（状态检查）、/cost（费用统计）、/config（配置管理）、/model（切换模型）、/doctor（环境健康检查）
- **三层记忆体系**：
  - Project Memory（项目记忆 `./CLAUDE.md`）：项目专属规则与偏好
  - User Memory（用户记忆 `~/.claude/CLAUDE.md`）：个人全局习惯，跨项目通用
  - Auto Memory（自动记忆）：Claude 自动判断重要信息并写入
- **模型选项**：Sonnet（日常编码，性价比高）、Opus（复杂架构，最强最贵）、Haiku（快速查询，最快最便宜）
- **开发工作流六步法**：初始化项目认知 → Plan Mode 理解代码 → 规划新功能 → 分模块执行 → 性能分析 → 记忆沉淀
- **核心理念**："Plan Mode 想清楚 → Auto-Accept 执行 → /compact 或 /clear 管理上下文 → /memory 沉淀经验"

## 关联连接

- [[Claude_Code]] — Anthropic 推出的终端 AI 编码助手
- [[Anthropic]] — Claude Code 的开发商
- [[Claude_Code_Slash_Commands]] — Claude Code 斜杠命令体系
- [[Claude_Code_Memory_System]] — 三层记忆机制
- [[Claude_Code_Workflow]] — Claude Code 开发工作流方法论
- [[AGENT_MD]] — CLAUDE.md 作为项目记忆文件的相关概念
