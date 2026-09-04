---
title: "Claude Code"
type: entity
tags: [AI编程, 开发工具, Anthropic, 终端工具, Agent生态]
sources: 
  - raw/01-articles/Claude Code 完全指南 - 阿里云开发者社区.md
  - raw/01-articles/05-claude-code-ecosystem.md
  - raw/09-archive/The AI-Native SDLC playbook  Claude by Anthropic.md
last_updated: 2026-09-04
---

## 定义

Claude Code 是 Anthropic 推出的**终端 AI 编码 Agent**——跑在 Terminal 里的 Claude agent，拥有完整 File System / Shell / Git / Subprocess 访问权限，可以自主完成多步骤工作（读文件 → 改文件 → 跑 Test → Commit → 发 PR）。它是 Agentic AI 生态中 **Terminal · 给工程师** 形态的代表产品。

## 与其他 Claude 界面的区别

| 界面 | 跑在哪 | 能做什么 |
|------|--------|---------|
| **claude.ai（Web）** | 浏览器 | 纯对话 + 上传文件，无 File System 操作 |
| **Claude API** | 你的 Server/Script | LLM Call，自己包 Agent Loop |
| **Claude Agent SDK** | 你的 Python/TS 环境 | 完整 Agent Runtime + Tool Use + 多 Session |
| **Claude Code** | 你的 Terminal | **完整 OS-level Agent**（File/Shell/Git/Subprocess）+ Skill/Plugin/Subagent 生态 |

## 关键信息

- **开发商**：[[Anthropic]]
- **类型**：终端 AI 编码代理（Agentic Coding 工具），Anthropic 的工程师向产品（与 Claude Cowork 桌面 App 互补）
- **启动方式**：在项目目录下运行 `claude` 命令
- **模型支持**：Sonnet（日常编码）、Opus（复杂架构）、Haiku（快速查询）
- **工作模式**（权限层级）：
  - **Default（默认模式）**：敏感操作需确认，一般操作直接执行
  - **Plan Mode（计划模式）**：只读分析和规划，不修改代码（Shift+Tab 或 /plan）
  - **Accept Edits（自动编辑模式）**：文件修改自动执行，Shell 命令仍需确认
  - **Auto Mode（自动模式）**：AI 分类器自动判断操作安全性
  - **Dangerously Skip Permissions**：所有操作自动执行，需 `--dangerously-skip-permissions` 启动
- **核心斜杠命令**：/help、/clear、/compact、/plan、/model、/agents、/plugin install、/permissions、/resume、/bg、/init、/memory、/status、/cost、/config、/doctor、/rewind、/BTW、/simplify、/vibe 等
- **快捷键**：Shift+Tab（切换模式）、#（创建记忆）、!（Bash 模式）、@（添加文件/文件夹）、Esc（取消）、Ctrl+R（详细输出）、Ctrl+B（后台运行）、Ctrl+T（任务面板）
- **输入方式**：文本交互、@文件精准传递上下文、图片输入（Ctrl+V 粘贴多模态）
- **记忆系统**：三层记忆体系（Project Memory / User Memory / Auto Memory），手动 + `/memory` 自动记录

## `~/.claude/` 目录结构

```
~/.claude/ ← 全局 User-level
├── settings.json ← 全局行为（Env / Hooks / Permissions / Model 预设）
├── settings.local.json ← 机器特定（不入 Git）
├── CLAUDE.md ← 全局 Baseline（每个 Session 都加载）
├── skills/<name>/SKILL.md ← User-level Skills
├── agents/<name>.md ← User-level Subagents
├── plugins/ ← 已安装的 Plugin
├── hooks/ ← User-level Hook Scripts
└── jobs/<id>/ ← Background Sessions 状态

<project-root>/.claude/ ← Project-level（随 Repo）
├── settings.local.json ← Project 行为（含 Permissions）
├── skills/<name>/SKILL.md ← Project-level Skills
├── agents/<name>.md ← Project-level Subagents
├── commands/<name>.md ← Project-level Slash Command
└── hooks/ ← Project-level Hook

<project-root>/CLAUDE.md ← Project Baseline（每个 Session 都加载）
```

**优先顺序**（冲突时谁赢）：Project > User > Built-in Default。

## 扩展机制

| 组件 | 本质 | 触发方式 |
|------|------|---------|
| **CLAUDE.md**（5.1） | 项目 Baseline 行为规则 | 每个 Session 都加载，不分情境 |
| **MCP Server**（5.2） | 标准化 Tool/Data 协议 Server | Server 启动后可随时调用 |
| **Skill**（5.3） | 特定情境的行为包 | Description 匹配自动加载 |
| **Plugin**（5.4） | 打包 Skills+Commands+MCP+Hooks | `/plugin install` |
| **Subagent**（5.5） | 独立 Context 的子 Claude Session | Description 匹配自动 Delegate |
| **Hooks**（5.1） | 事件生命周期拦截脚本 | 在 PreToolUse/PostToolUse 等时机触发 |
| **Dynamic Workflows**（5.6） | Claude 自生成 Workflow 脚本 | Opus 4.8+ 内置 |

## 7-Layer Architecture

Claude Code 拥有**最完整的 7-Layer Stack**（其他 CLI Agent 如 Codex / Gemini CLI 仅部分具备）：

| Layer | 名称 | Claude Code 实现 |
|-------|------|-----------------|
| L7 Interface | 用户入口 | claude-code CLI / Desktop |
| L6 Workflow | 流程模板 | Skills + Slash Commands + Plugins |
| L5 Coordination | 多 Agent 协作 | Subagents + Agent Team + Background |
| L4 Memory/Context | 跨对话记忆 | History / /compact / Memory hooks |
| L3 Control Plane | 守门员层 | Hooks（PreToolUse/PostToolUse 等）|
| L2.5 Tool Provider | 外部工具接入 | MCP Servers |
| L2 Tool Use | Function 调用协议 | Anthropic Tool Use（input_schema）|
| L1 Foundation | LLM 本体 | Anthropic API |

## 六重境界进阶路径

[[Claude_Code_六重境界|Claude Code 六重境界]] 将用户技能划分为六个递进层次：

| 层级 | 核心能力 | 与现有框架对齐 |
|:----:|---------|---------------|
| L1 · 提示工程师 | 基础提示词编写、输出质量评判 | [[Prompt_Engineering]] |
| L2 · 规划者 | 计划模式、协作式提问 | — |
| L3 · 上下文工程师 | 上下文窗口管理、腐败控制 | [[Context_Engineering]] + [[上下文腐败]] |
| L4 · MCP/工具集成 | 外科手术式精准选配 MCP | [[MCP]] |
| L5 · 技能/工作流 | Skill 编写与组合 | [[Claude_Code_Skills]] |
| L6 · 规模化编排 | 多实例协调、Agent Teams | [[Claude_Code_Subagent]] + [[Multi_Agent_System]] |

> 此框架提示了 Claude Code 的能力进阶远不止于工具操作——从"AI 工具使用者"到"AI 协作者"的思维转变是贯穿全文的核心主线。

## 并行运行方式

- 多终端标签页 + 多副本
- Git Worktrees
- SSH+Tmux
- Background Agent（`claude --bg "..."`，v2.1.139+）
- GitHub Actions
- 平台支持：跨平台（Windows / macOS / Linux）

## 在 AI-Native SDLC 中的角色

在 [[AI_SDLC|AI-Native SDLC]]（Anthropic Playbook）中，Claude Code 是横跨多个阶段的执行工具：

- **Build**：Plan Mode 作为默认起点——先产出可提交的 `plan.md` 再实现；guardrails 成熟后在 Auto Mode 下对 routine 工作 auto-accept；配合 git worktree 跑并行会话、用 `.claude/agents/` 定义 verifier/simplifier/researcher 等 subagent。
- **Deploy**：在 PR review loop 中以 `@claude` 处理 review 意见并推送修复；经 claude-code-action / `claude -p` 非交互式进入 CI/CD，负责 triage、changelog、review 修复等判断步骤（一切写入走分支保护、无直通 main 路径）。
- **Maintain**：作为非交互式无状态步骤被确定性监控脚本触发（诊断写回 `intent.md`），或承载 Claude Security 补丁的 review 与应用。
- **CLAUDE.md / Skills / Hooks** 三者构成其「制度知识 + 顾问性控制 + 确定性护栏」的组合，是组织级治理的载体。

## 开发者工作流定位

在 [[Developer_Agentic_Workflow|开发者 Agentic AI 工作流]] 的 **Tier 升级路径** 中，Claude Code 横跨 **Tier 1（CLI agent 入门）** 到 **Tier 2（Skill/MCP 生态扩展）**：

| Tier | Claude Code 角色 |
|------|-----------------|
| Tier 1 | CLI 接 file system，human-in-the-loop 编码助理 |
| Tier 2 | Skills + MCP server + Plugin 生态，团队 workflow 封装 |
| Tier 3 | CI 自动 review（Claude Code Action）+ production observability |

覆盖的开发者场景：
- **AI 结对编程**：plan-first 模式，先写 plan 再写 code
- **多文件重构**：batch refactor 保持风格一致
- **Code review**：审查自己的 diff，找 bug/smell
- **写测试**：从 signature/spec 生成 pytest
- **Debug**：解释 trace、生成 hypothesis
- **文档生成**：从 code 生成 doc

## 关联连接

- [[Anthropic]] — Claude Code 的开发商（含 Claude Cowork 对比）
- [[AI_SDLC]] — AI-Native SDLC 中 Claude Code 的执行角色（plan mode/auto mode/PR/CI）
- [[摘要-ai-native-sdlc-playbook]] — Anthropic AI-Native SDLC Playbook 来源
- [[Agentic_Coding]] — Claude Code 所属的 AI 编程范式
- [[Developer_Agentic_Workflow]] — 开发者场景分类与 Tier 路径
- [[MCP]] — Model Context Protocol，Claude Code 的 L2.5 Tool Provider
- [[Claude_Code_Skills]] — Skills 行为层（L6 Workflow）
- [[Claude_Code_Subagent]] — Subagent 多 Agent 机制（L5 Coordination）
- [[Claude_Code_Hooks]] — Hooks 控制层（L3 Control Plane）
- [[Claude_Code_Plugins]] — Plugin 打包与市场（L6 Workflow）
- [[Claude_Code_Dynamic_Workflows]] — 动态 Workflow（L6 进阶）
- [[Claude_Code_Harness]] — 7-Layer Architecture 完整视图
- [[Claude_Code_Slash_Commands]] — 斜杠命令体系
- [[Claude_Code_Memory_System]] — 记忆系统
- [[Claude_Code_Workflow]] — 开发工作流方法论
- [[Claude_Agent_SDK]] — 程序化使用方式
- [[Multi_Agent_System]] — Subagent 是 Multi-agent 的两条路线之一
- [[AGENT_MD]] — 项目记忆文件
- [[摘要-claude-code-guide]] — Claude Code 完全指南
- [[摘要-claude-code-hud]] — claude-hud 终端状态监控插件
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — 生态系全景来源
