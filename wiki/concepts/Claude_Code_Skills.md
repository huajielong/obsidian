---
title: "Claude Code Skills"
type: concept
tags: [Claude Code, Skills, 插件, 扩展, 行为层]
sources: 
  - raw/01-articles/Claude Code/skill打包技巧.md
  - raw/01-articles/Claude Code/Claude Code常用功能.md
  - raw/01-articles/Claude Code/Claude code的基础及高级工作流.md
  - raw/01-articles/05-claude-code-ecosystem.md
last_updated: 2026-07-10
---

# Claude Code Skills（技能系统/行为层）

## 定义

Skill 是 Claude Code 生态的**行为层（L6 Workflow）**——本质上是一个 Markdown 文件（`.claude/skills/<name>/SKILL.md`），告诉 Claude "**遇到某情境 → 走某流程**"。Claude 每次 Inference 前扫描所有可用 Skill 的 `description` Frontmatter，看是否匹配当前情境，**匹配就把 SKILL.md 自动加载到 Context**。

Skill 是 **Claude Code Power User 与普通用户的分水岭**——熟练 Skill 写作的人能把 1 小时的工作压到 5 分钟。

## Skill 文件结构

```markdown
---
name: skill-name
description: 何时触发（Claude 匹配 description 自动加载）
tools:    # 可选，限制可用工具
model:    # 可选，指定模型
---

# Skill Name

## 执行步骤

1. ...
2. ...

## References（可选）
- `references/<topic>.md` 存放详细规则
- 主文件保持 < 200 行
```

## Skills 分类

| 类型 | 说明 | 示例 |
|------|------|------|
| **知识型** | 提供领域知识 | remotion-dev/skills（Remotion 视频开发） |
| **流程型** | 定义执行步骤 | GSD Core（项目管理流程） |
| **工具型** | 封装工具调用 | playwright-cli（浏览器自动化） |
| **混合型** | 知识 + 流程 + 工具 | context7（文档查询） |

## Skill 目录约定

```
skills/<name>/
├── SKILL.md         ← 主文件（< 200 行）
├── references/      ← 详细规则、范例、Edge Cases
├── scripts/         ← 可自动化的脚本
├── evals/           ← 自测 Case（evals.json）
└── assets/          ← 复用模板
```

## 核心区分：MCP vs Skill vs Plugin vs Subagent

| 组件 | 本质 | 触发方式 |
|------|------|---------|
| **MCP Server** | 提供 Tool/Data 的协议 Server（能力） | Server 启动后可随时调用 |
| **Skill** | 特定情境的行为包（行为） | Description 匹配自动加载 |
| **Plugin** | 打包 Skills+Commands+MCP+Hooks（散布） | `/plugin install` |
| **Subagent** | 独立 Context 的子 Claude Session（独立 Worker） | 自动/手动 Delegate |

> **MCP = 能力**（让 LLM 能做什么）、**Skill = 行为**（什么时候用什么能力）、**Plugin = 散布**、**Subagent = 独立 Worker**。

## Skill vs Subagent vs CLAUDE.md 对照

| 组件 | 是什么 | 何时用 | 触发方式 |
|------|--------|--------|---------|
| **CLAUDE.md** | Repo/Project 的 Baseline 行为 | Repo-wide Convention | **每个 Session 都加载**、不分情境 |
| **Skill** | 特定情境的行为包 | 设置"遇到 X 情境 → 走 Y 流程" | **Description 匹配自动加载** |
| **Subagent** | 独立 Context 的 Sub-Claude Session | Delegate 大 Context 任务 | Description 匹配自动 Delegate |
| **Plugin** | 打包散布单位 | 想 Share/Install 一整套设置 | `/plugin install` |

**怎么选**：
- 一句话设置 → 写进 `CLAUDE.md`
- 多步骤流程、某情境才用 → 写 **Skill**
- 需要访问外部资源（API/DB）→ 写 **MCP Server**
- Skill 跑起来太大、会吃光主 Session Window → 改成 **Subagent**
- Skill/Command/MCP/Hook 想打包送人 → 包成 **Plugin**

## 常用 Skills 推荐

| 用途 | Skill | 来源 | 为什么推荐 |
|------|-------|------|-----------|
| **🛡 装 Skill 前安全检查**（必装） | `skill-vetter` | anthropics/skills | 检查红旗、Permission Scope、Suspicious Pattern |
| **🔍 找/安装 Skill** | `find-skills` / `skill-lookup` | anthropics/skills | 自然语言查询、自动安装 |
| **✍ 写自己的 Skill** | `skill-creator` | anthropics/skills | 自动产生 Frontmatter + 子目录结构 |
| **📄 Office 文档处理** | `pdf` / `docx` / `xlsx` / `pptx` | anthropics/skills | **必装 Set** |
| **🔧 Code Review** | `code-reviewer` / `code-review-excellence` | claude-plugins-official | Staged Diff 安全/风格/测试 Review |
| **🐛 Debug** | `debugger` / `systematic-debugging` | claude-plugins-official | 系统化 Root Cause 分析 |
| **🔌 MCP 整合** | `mcp-builder` / `mcp-integration` | claude-plugins-official | 写 MCP Server 的脚手架 |
| **💻 Frontend** | `frontend-developer` / `fullstack-developer` | claude-plugins-official | React 组件/全栈架构辅助 |
| **⚙ 权限/设置整理** | `update-config` / `fewer-permission-prompts` | claude-plugins-official | Hooks/Permissions/Env Var 管理 |

**建议入手顺序**：
1. `skill-vetter`（装其他 Skill 前先用它检查）
2. `skill-creator` + `find-skills`（写/找 Skill）
3. 按工作领域：Office 加 `pdf`/`docx`/`xlsx`、开发加 `code-reviewer`/`debugger`

## Skill 写作建议

两个 Prompt 可直接使用（摘自 awesome-agentic-ai-zh Stage 5）：

- **Prompt 1 — Audit 现有 SKILL.md**：检查 Legibility / Progressive Disclosure / System of Record / Taste Invariants / Throughput
- **Prompt 2 — 生成新 SKILL.md**：要求 description 写清楚触发条件、主档 < 200 行、references/ 结构、Success Criteria 表

## Skill 参考项目

| Project | 适合谁 | 备注 |
|---------|--------|------|
| [anthropics/skills](https://github.com/anthropics/skills) ⭐ 官方 | 写 SKILL.md 前必读 | 官方 Skills Repo，含 spec/ + template/ + pdf/docx/xlsx/pptx/skill-creator/skill-vetter，★158k+ |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 想看来真实工程师的 SKILL.md | 每个 10-50 行极短、不过度工程化，★157k+ |
| [obra/superpowers](https://github.com/obra/superpowers) | Power User Setup | 20+ 实战 Skill |
| [wshobson/agents](https://github.com/wshobson/agents) | 中阶 Skill+Subagent 组合 | Skill 向 Subagent 进化的 Pattern，★35k+ |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | 先找现成的 | 社区 Claude Skills 精选目录 |

## 开发者工作流中的 Skills

在 [[Developer_Agentic_Workflow]] 的 Tier 路径中，Skills 写作对应 **Tier 2**——将重复性开发流程封装成可复用的行为包。

Skill 参考项目 [[superpowers_obra]]（obra 的 20+ 实战 Skill 集合）是设计 code-review / debug / TDD Skill 时的重要参考。

## 关联连接
- [[Claude_Code]] — Skills 的宿主环境
- [[Developer_Agentic_Workflow]] — 开发者工作流场景分类（Tier 2 涉及 Skills）
- [[superpowers_obra]] — obra 的 20+ 实战 Skill 集合
- [[MCP]] — MCP = 能力层，与 Skills 行为层互补
- [[Claude_Code_Subagent]] — Subagent vs Skill 决策对比
- [[Claude_Code_Plugins]] — Plugin 可封装 Skill
- [[Claude_Code_Hooks]] — Skill 执行中 Hook 也会触发
- [[Claude_Code_Harness]] — Skill 位于 L6 Workflow
- [[Claude_Code_Workflow]] — Skill 在工作流中的运用
- [[GSD_Core]] — 流程型 Skills 实践
- [[AGENT_MD]] — Agent 行为规范
- [[AI_Mastery_Compass]] — 罗盘方法论的具体工程化实现
- [[Progressive_Disclosure]] — Skill 系统实现三层知识加载的核心设计模式
- [[ADK]] — Google ADK，同属 Agent 开发框架
- [[Skill_Factory]] — 元 Skill / Agent 自我扩展的设计模式
- [[摘要-awesome-agentic-ai-zh-claude-code-ecosystem]] — Skills 深度来源
