---
title: "Claude Code Skills"
type: concept
tags: [Claude Code, Skills, 插件, 扩展]
sources: 
  - raw/01-articles/Claude Code/skill打包技巧.md
  - raw/01-articles/Claude Code/Claude Code常用功能.md
  - raw/01-articles/Claude Code/Claude code的基础及高级工作流.md
last_updated: 2026-07-03
---

# Claude Code Skills（技能系统）

## 定义

Claude Code Skills（技能）是给 AI 的专业说明书和操作手册，让 Claude Code 获得特定领域的知识、流程和工具能力。Skills 是 Claude Code 生态的核心扩展机制。

## Skills 分类

| 类型 | 说明 | 示例 |
|------|------|------|
| **知识型** | 提供领域知识 | remotion-dev/skills（Remotion 视频开发） |
| **流程型** | 定义执行步骤 | GSD Core（项目管理流程） |
| **工具型** | 封装工具调用 | playwright-cli（浏览器自动化） |
| **混合型** | 知识 + 流程 + 工具 | context7（文档查询） |

## 相关扩展机制对比

| 机制 | 说明 | 范围 |
|------|------|------|
| **Skills** | AI 专业知识库和操作手册 | 单领域能力 |
| **Subagents** | 独立上下文的专用 AI 助手，可并行 | 多任务并行 |
| **MCP** | Model Context Protocol，连接外部服务 | 外部系统集成 |
| **CLI 工具** | 命令行工具，AI 可直接调用 | 系统操作 |
| **Hooks** | 特定事件触发自定义脚本 | 事件驱动 |
| **Plugins** | 打包整合 Skills/Subagents/Hooks 的扩展包 | 综合扩展 |

## Skill 打包

可通过提示词将磨合好的工作流程一键打包成 Skill：
1. 创建完整的 Skill 文件夹结构
2. 编写 SKILL.md（职责、触发场景、执行步骤、输出标准）
3. references 放入格式要求和内容标准
4. scripts 放入可自动化的脚本
5. assets 放入复用模板

## 安装方式

- 手动复制到 `~/.claude/skills/` 或项目 `.claude/skills/`
- 插件市场安装：`/plugin install <skill-name>`
- `claude skills add <repo>`（如 `claude skills add remotion-dev/skills`）

## 关联连接
- [[Claude_Code]] — Claude Code 实体
- [[GSD_Core]] — GSD Core（流程型 Skills 实践）
- [[AGENT_MD]] — Agent 行为规范
