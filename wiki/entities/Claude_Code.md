---
title: "Claude Code"
type: entity
tags: [AI编程, 开发工具, Anthropic, 终端工具]
sources: [raw/01-articles/Claude Code 完全指南 - 阿里云开发者社区.md]
last_updated: 2026-07-03
---

## 定义

Claude Code 是 Anthropic 推出的终端 AI 编码助手，通过在命令行界面中与开发者自然语言交互，实现代码理解、编写、重构、测试等全流程的 AI 辅助开发。它直接运行在终端中，支持多种工作模式、斜杠命令体系和持久记忆机制。

## 关键信息

- **开发商**：[[Anthropic]]
- **类型**：终端 AI 编码代理（Agentic Coding 工具）
- **启动方式**：在项目目录下运行 `claude` 命令
- **模型支持**：Sonnet（日常编码）、Opus（复杂架构）、Haiku（快速查询）
- **工作模式**：
  - **Default（默认模式）**：每次操作需用户确认
  - **Auto-Accept（自动接受模式）**：文件修改自动执行
  - **Plan（计划模式）**：只读分析和规划，不修改代码
- **核心斜杠命令**：/init、/memory、/compact、/clear、/status、/cost、/config、/model、/doctor 等
- **记忆系统**：三层记忆体系（Project Memory / User Memory / Auto Memory）
- **平台支持**：跨平台终端工具，支持 Windows、macOS、Linux

## 关联连接

- [[Anthropic]] — Claude Code 的开发商
- [[Agentic_Coding]] — Claude Code 所属的 AI 编程范式
- [[Claude_Code_Slash_Commands]] — 斜杠命令体系
- [[Claude_Code_Memory_System]] — 记忆系统
- [[Claude_Code_Workflow]] — 开发工作流方法论
- [[AGENT_MD]] — Claude Code 项目记忆文件
- [[摘要-claude-code-guide]] — 来源文章
