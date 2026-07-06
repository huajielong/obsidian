---
title: "ADK（Agent Development Kit）"
type: entity
tags: [Google, Agent框架, 开发工具, Skill, SkillToolset]
sources: 
  - wiki/sources/摘要-adk-agents-with-skills.md
last_updated: 2026-07-06
---

# ADK（Agent Development Kit）

## 定义

ADK（Agent Development Kit）是 Google 推出的 AI Agent 开发框架，支持 **Python** 和 **Go** 语言（Java 1.0 版本于 2026 年 3 月底发布）。其核心特色是通过 **SkillToolset** 实现 [[Progressive_Disclosure|渐进式披露（Progressive Disclosure）]] 架构，解决 Agent 系统提示词膨胀问题。

## 核心组件

### SkillToolset

ADK 通过 `SkillToolset` 类实现渐进式披露加载机制。开发者把 Skill 列表传给 `SkillToolset`，它会自动生成三个工具：

| 工具 | 对应层级 | 功能 |
|------|---------|------|
| `list_skills` | L1 | 列出所有可用 Skill（每次对话自动注入） |
| `load_skill` | L2 | 按需加载某个 Skill 的完整指令 |
| `load_skill_resource` | L3 | 按需加载 Skill 关联的参考资源文件 |

Agent 在运行过程中自主决定何时调用哪个工具，开发者不需要手动编写 if-else 逻辑来编排加载流程——**Agent 本身就是决策者**。

## Skill 构建模式

ADK 支持四种 Skill 构建模式，复杂度依次递增：

1. **内联 Skill（Inline Skill）** — 直接在代码中定义 Python 对象，适合小型稳定规则
2. **基于文件的 Skill（File-based Skill）** — 将 Skill 剥离到独立目录结构（SKILL.md + references/）
3. **外部导入 Skill（External Skill）** — 从社区仓库下载现成 Skill
4. **[[Skill_Factory|元 Skill / Skill Factory]]** — Agent 在运行时动态生成新 Skill 定义

## 生态兼容

ADK 的 Skill 系统建立在 **`agentskills.io`** 开放标准之上，已被 **40+ 产品**采用，包括 Gemini CLI、Claude Code、Cursor 等。一份 Skill 定义可以在不同厂商的 Agent 平台之间通用。

```bash
# 安装 Google 官方 ADK 开发 Skill
npx skills add google/adk-docs -y -g
```

## 关联连接

- [[Progressive_Disclosure]] — 渐进式披露架构，ADK 的核心设计理念
- [[Skill_Factory]] — 元 Skill / Skill Factory，ADK 支持的高级模式
- [[Claude_Code_Skills]] — Claude Code 的 Skill 系统，与 ADK 同属 agentskills.io 生态
- [[摘要-adk-agents-with-skills]] — Google Developers Blog 原文摘要
- [[Agentic_Coding]] — AI Agent 驱动编程范式
- [[Harness_Engineering]] — Agent 系统工程实践，ADK 是其具体实现框架之一
