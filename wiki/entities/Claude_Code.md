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
- **工作模式**（权限层级）：
  - **Default（默认模式）**：敏感操作需确认，一般操作直接执行
  - **Plan Mode（计划模式）**：只读分析和规划，不修改代码（Shift+Tab 或 /plan）
  - **Accept Edits（自动编辑模式）**：文件修改自动执行，Shell 命令仍需确认
  - **Auto Mode（自动模式）**：AI 分类器自动判断操作安全性
  - **Dangerously Skip Permissions**：所有操作自动执行，需 `--dangerously-skip-permissions` 启动
- **核心斜杠命令**：/init、/memory、/compact、/clear、/status、/cost、/config、/model、/doctor、/model、/rewind、/BTW、/simplify、/help、/vibe 等
- **快捷键**：Shift+Tab（切换模式）、#（创建记忆）、!（Bash 模式）、@（添加文件/文件夹）、Esc（取消）、Ctrl+R（详细输出）
- **输入方式**：文本交互、@文件精准传递上下文、图片输入（Ctrl+V 粘贴多模态）
- **记忆系统**：三层记忆体系（Project Memory / User Memory / Auto Memory），手动 + `/memory` 自动记录
- **扩展机制**：
  - **Skills**：领域专业知识库和操作手册
  - **Subagents**：独立上下文可并行处理的专用 AI 助手
  - **MCP（Model Context Protocol）**：连接外部服务的协议
  - **CLI 工具**：厂商提供的命令行工具
  - **Hooks**：特定事件触发自定义脚本
  - **Plugins**：打包整合 Skills/Subagents/Hooks 的扩展包
- **并行运行方式**：多终端标签页 + 多副本、Git Worktrees、SSH+Tmux、GitHub Actions
- **平台支持**：跨平台终端工具，支持 Windows、macOS、Linux

## 关联连接

- [[Anthropic]] — Claude Code 的开发商
- [[Agentic_Coding]] — Claude Code 所属的 AI 编程范式
- [[Claude_Code_Slash_Commands]] — 斜杠命令体系
- [[Claude_Code_Memory_System]] — 记忆系统
- [[Claude_Code_Workflow]] — 开发工作流方法论
- [[Claude_Code_Skills]] — Skills 技能系统架构与扩展机制
- [[AGENT_MD]] — Claude Code 项目记忆文件
- [[摘要-claude-code-guide]] — Claude Code 完全指南
- [[摘要-claude-code-hud]] — claude-hud 终端状态监控插件
