---
title: "Claude Code Plugins"
type: concept
tags: [Claude Code, Plugins, Marketplace, 打包, 发布]
sources: [raw/01-articles/05-claude-code-ecosystem.md]
last_updated: 2026-07-10
---

# Claude Code Plugins & Marketplaces

## 定义

Plugin 是将 MCP Config + Skills + Slash Commands + Hooks + Subagents **打包成一个单位**的机制。通过 `/plugin install <name>@<marketplace>` 一次安装，是 Claude Code 生态的**散布层（L6 Workflow）**。

## Plugin 目录结构

```
Plugin
├── .mcp.json               ← MCP Server 配置
├── skills/<name>/SKILL.md   ← Skill 行为包
├── commands/<name>.md       ← 自定义 Slash Command
├── hooks/                   ← 触发点 Hook
├── agents/<name>.md         ← Subagent 定义
└── .claude-plugin/plugin.json ← 打包元数据
```

## Plugin vs Marketplace

| 概念 | 说明 |
|------|------|
| **Plugin** | 单一打包单位 |
| **Marketplace** | 多个 Plugin 的目录（如 `anthropics/claude-plugins-official` 含 35 个 Plugin）|

## 常用 Plugin 分类

### 开发 Workflow（开发者必装）
- `code-review` — 官方 Code Review Skill 集合
- `pr-review-toolkit` — PR Review 完整流程
- `commit-commands` — Git Commit 规范 + Branching Workflow
- `feature-dev` — 完整 Feature 开发 Cycle（Spec → Plan → Implement → Test）
- `frontend-design` — UI 设计 + Responsive Layout

### 语言工具
- `typescript-lsp` / `pyright-lsp` / `rust-analyzer-lsp` / `gopls-lsp` 等（35 个语言 Plugin）

### 自建工具
- `skill-creator` — 自动产生 Frontmatter + 结构
- `plugin-dev` — 自动产生 `.claude-plugin/` 结构
- `mcp-server-dev` — MCP Server 脚手架
- `hookify` — Hooks 规则工具

### 领域特化 Bundle
- `engineering` bundle — 10 个 Skill（architecture / code-review / debug / deploy-checklist / documentation / incident-response / standup / system-design / tech-debt / testing-strategy）
- `finance` bundle — 8 个 Skill
- 另有 sales / marketing / legal / hr / data / design 等 18 个垂直领域 Bundle

### 外部整合
- asana / github / gitlab / linear / firebase / playwright / terraform / discord 等

## 建议安装顺序

1. **必装 5 个**：`code-review` + `pr-review-toolkit` + `commit-commands` + `feature-dev` + 你的语言 LSP Plugin
2. **按工作领域**：工程团队装 `engineering`、财务装 `finance`，其他类推
3. **自建工具**：想写自己的 Skill/Plugin → 装 `skill-creator` + `plugin-dev`

## 主要 Marketplace 参考

| Marketplace | 特点 |
|-------------|------|
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 官方 35 个内部 Plugin + 15 个外部，★30k+ |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | 18 个领域 Plugin Bundle |
| [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | 最简 Marketplace Template（Curator-only Pattern）|
| [trailofbits/skills-curated](https://github.com/trailofbits/skills-curated) | Security-vetted Marketplace，经过审查 |
| [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal) | 完整 Vertical Plugin Suite 范本（10 个法律 Plugin + 100+ Skills + 20+ MCP Connectors）|

## 关联连接

- [[Claude_Code]] — Plugin 的宿主环境
- [[Claude_Code_Skills]] — Plugin 内含的核心组件之一
- [[MCP]] — Plugin 可封装的 MCP Server 配置
- [[Claude_Code_Hooks]] — Plugin 可包含的 Hook 定义
- [[Claude_Code_Subagent]] — Plugin 可包含的 Subagent 定义
- [[Claude_Code_Harness]] — Plugin 位于 L6 Workflow 层
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 核心来源
