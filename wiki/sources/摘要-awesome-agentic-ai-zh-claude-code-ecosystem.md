---
title: "摘要-awesome-agentic-ai-zh-claude-code-ecosystem"
type: source
tags: [Claude Code, MCP, Skills, Plugins, Subagents, Agent生态, 学习路线]
sources: [raw/01-articles/05-claude-code-ecosystem.md]
last_updated: 2026-07-10
---

# 摘要：Claude Code 生态系（Stage 5）

> **来源**：awesome-agentic-ai-zh 学习路线图 Stage 5，作者 WenyuChiou
> **原始素材**：已保存至 `raw/01-articles/05-claude-code-ecosystem.md`

## 核心主旨

本文是 Agentic AI 学习路线图的第 5 阶段（Hub 节点），系统介绍 **Claude Code 生态系的完整堆栈**——从 CLI 基础到 MCP 协议、Skills 行为层、Plugins 打包发布、Subagents 多 Agent 机制、Dynamic Workflows 以及 SDK 编程接口，构建了 Claude Code 的 **7-Layer Architecture Map**。

## 章节概要

### 5.1 Claude Code 基础
Claude Code 是跑在终端中的 Claude agent，拥有完整 File System / Shell / Git / Subprocess 访问权限。与 claude.ai（浏览器对话）、Claude API（程序调用）、Claude Agent SDK（生产级 Agent Runtime）形成四种不同粒度的使用方式。核心结构包括：CLAUDE.md（项目记忆层）、Slash Commands（控制层）、`~/.claude/` 目录（设置层）、settings.json（行为层）、Hooks（事件拦截层）。

### 5.2 MCP（Model Context Protocol）
MCP 是标准化 LLM 工具调用的开放协议，定义三个抽象：**Tools**（LLM 可调用的 function）、**Resources**（LLM 可读的数据源）、**Prompts**（预定义 Prompt 模板）。MCP 让任何 LLM Host（Claude / Codex / Cursor）都能使用任何 Tool Server。2026 年生态已包含官方 Registry、FastMCP 框架（25k+ stars）等工具。

### 5.3 Skills（行为层）
Skill 本质是一个 markdown 文件（`SKILL.md`），通过 frontmatter `description` 字段匹配情境自动加载。Skills 是 **Claude Code Power User 与普通用户的分水岭**。核心区分：MCP = 能力（给 LLM 能做什么），Skill = 行为（教 LLM 什么时候用什么能力）。官方 skills repo 含 pdf/docx/xlsx/pptx/skill-creator/skill-vetter 等参考实现。

### 5.4 Plugins & Marketplaces
Plugin 将 MCP Config + Skills + Slash Commands + Hooks + Subagents 打包为一个单位，通过 `/plugin install` 一次安装。Marketplace 是 Plugin 的目录。官方 marketplace（claude-plugins-official）含 35 个内部 Plugin + 15 个外部 Plugin。还有 knowledge-work-plugins（18 个垂直领域 bundle）、obra/superpowers-marketplace（社区范本）等。

### 5.5 Subagents（原生 Multi-Agent）
Claude Code 提供三种 Multi-Agent 机制：**Subagent**（稳定版，独立 Context 隔离 Worker）、**Agent Team**（多 Worker 互相沟通/辩论）、**Background Agent**（研究预览版，多独立任务后台并行）。核心差异：Subagent vs Skill = 新 Context Window vs 同 Context 行为注入。内置 subagent 包括 Explore/Plan/code-reviewer/frontend-developer/general-purpose 等。

### 5.6 Dynamic Workflows（Opus 4.8+）
让 Claude 自己生成 Workflow 脚本再执行——比手动派 Subagent 更上层，适合大型、穷举或多阶段验证任务（Migration / Audit / 跨文件 Review）。建立在 Subagent 之上，Workflow 脚本 Orchestrate 一群 Subagent。

### 5.7 Claude Code Source 解剖
将 Claude Code 作为 Harness Engineering 的 Reference Implementation 进行案例研究，在 `claude-agent-sdk-python` 的源码中标出 6 个 Runtime-Internal Harness 元件：Agent Loop / Tool Registry / Context Manager / Safety Layer / Retry / Telemetry。

### 5.8 SDK（Claude Agent SDK）
三阶路径：CLI（现成车子）→ CLI+自定义（调车子性能）→ SDK（从引擎开始重造）。Claude Agent SDK 适合将 Agent 嵌入 Web App、Cron 调度、公司内部封装等场景。核心 API 仅 4 行 Python 即可运行。

## 核心概念框架

### 7-Layer Architecture Map

| Layer | 名称 | Claude 的版本 | 对应 Engineering Discipline |
|-------|------|--------------|---------------------------|
| L7 | Interface | claude-code CLI / Desktop | Harness Engineering |
| L6 | Workflow | Skills + Slash Commands + Plugins | Prompt Engineering |
| L5 | Coordination | Subagents + Agent Team + Background | Harness Engineering |
| L4 | Memory/Context | History / /compact / Memory hooks | Context Engineering |
| L3 | Control Plane | Hooks (PreToolUse/PostToolUse) | Harness Engineering |
| L2.5 | Tool Provider | MCP servers | Context Engineering + Tool Design |
| L2 | Tool Use | Anthropic Tool Use (input_schema) | Tool Design |
| L1 | Foundation | Anthropic API | Prompt Engineering |

### 组件对照表

| 组件 | 本质 | 触发方式 |
|------|------|---------|
| CLAUDE.md | 项目 baseline 行为 | 每个 Session 都加载 |
| MCP Server | 提供 Tool/Data 的协议 Server | Server 启动后可随时调用 |
| Skill | 特定情境行为包 | Description 匹配自动加载 |
| Plugin | 打包 Skills+Commands+MCP+Hooks | `/plugin install` |
| Subagent | 独立 Context 的子 Claude | Description 匹配自动派遣 |

## 关联连接

- [[Claude_Code]] — 本生态系统的核心宿主
- [[MCP]] — Model Context Protocol 协议层
- [[Claude_Code_Skills]] — Skills 行为层（需大幅扩展）
- [[Claude_Code_Subagent]] — Subagent 多 Agent 机制
- [[Claude_Code_Plugins]] — Plugin 打包与市场
- [[Claude_Code_Hooks]] — Hooks 控制层
- [[Claude_Code_Dynamic_Workflows]] — 动态 Workflow 机制
- [[Claude_Code_Harness]] — 7-Layer Architecture 与 Harness 实现
- [[Claude_Agent_SDK]] — Agent SDK 实体
- [[Multi_Agent_System]] — Multi-Agent 概念框架对比
- [[Agent_Orchestration_Patterns]] — 编排模式对比
- [[Anthropic]] — Claude Code 的开发商
- [[Claude_Code_Slash_Commands]] — Slash 命令体系
- [[Claude_Code_Workflow]] — 开发工作流方法论
