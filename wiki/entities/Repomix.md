---
title: "Repomix"
type: entity
tags: [工具, codebase, 打包, AI, review, 开源]
sources: [https://github.com/yamadashy/repomix, https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/branches/for-developer.zh-Hans.md]
last_updated: 2026-07-10
---

# Repomix

> ★ 26k+ · [GitHub](https://github.com/yamadashy/repomix)

**典型开发者用途**：打包整个 codebase 给 reviewer / refactor agent。输出单个 AI-friendly 文件（XML / Markdown / JSON），方便 [[Claude_Code]] 或 [[Codex]] 做 code review / refactoring。

## 核心特性

- **输入**: 整个 codebase 目录
- **输出**: 单个 AI-friendly 文件（XML / Markdown / JSON）
- **高级功能**:
  - MCP server mode
  - tree-sitter 压缩（按 AST 结构精简代码）
  - secretlint 过滤（防止 API key 泄漏）

## 在开发者工作流中的角色

- **Track A 的必备 daily-driver 工具**
- **Code review**: 打包 codebase 给 AI reviewer
- **Refactoring**: 提供完整上下文给 refactor agent
- **调试**: 给 Debug agent 完整项目视图

## 关联链接

- [[Claude_Code]] — Anthropic 官方 coding 助理（常与 Repomix 配合）
- [[Codex]] — OpenAI 编码智能体
- [[Aider]] — CLI pair-programmer
- [[Cline]] — VS Code autonomous agent
- [[Developer_Agentic_Workflow]] — 开发者工作流场景分类
- [[Harness_Engineering]] — Agent 系统工程实践
