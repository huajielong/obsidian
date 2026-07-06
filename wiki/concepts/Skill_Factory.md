---
title: "Skill Factory（元 Skill / Meta Skill）"
type: concept
tags: [Skill, 元技能, 自我扩展, Agent, 动态生成]
sources: 
  - wiki/sources/摘要-adk-agents-with-skills.md
last_updated: 2026-07-06
---

# Skill Factory（元 Skill / Meta Skill）

## 定义

Skill Factory（也称**元 Skill / Meta Skill**）是一种特殊设计的 Skill，其用途不是执行某项具体任务，而是专门用来**生成新的 `SKILL.md` 文件**。配备元 Skill 的 Agent 变成了**自我扩展的系统**——它可以在运行时编写新的 Skill 定义并立即使用，整个过程不需要人工干预。

## 工作原理

### 完整运作流程

1. 用户对 Agent 提出需求："我需要一个新 Skill，用来审查 Python 代码中的安全漏洞。"
2. Agent 调用 `list_skills` 浏览已有的 Skill 列表，发现没有匹配的 Skill
3. Agent 激活 `skill-creator` 元 Skill，调用 `load_skill_resource` 读取 `agentskills.io` 规范和示例
4. Agent 根据用户需求生成 Skill 定义，包含合规的命名、结构化指令、特定报告格式
5. 生成的 Skill 遵循 `agentskills.io` 规范，可在 40+ 产品中使用

### 关键实现细节

元 Skill 内嵌了两份 L3 参考文档：
- **skill-spec.md**：`agentskills.io` 完整规范
- **example-skill.md**：一个可运行的代码审查 Skill 示例

当 Agent 被要求创建新 Skill 时，它通过 `load_skill_resource` 工具读取这两份参考文档，理解规范的格式要求和最佳实践，然后根据用户的具体需求生成一份符合规范的 SKILL.md。

## 设计意义

Skill Factory 代表了 AI Agent 能力边界的质变：

- **从被动到主动**：Agent 从被动执行人类编写的指令，拓展到主动为自己编写新指令
- **从静态到动态**：能力集合不再在部署时固化，可在运行时按需扩展
- **从封闭到开放**：遇到未知场景时不再只能报错，可以现场编写新 Skill 补齐能力缺口

## 安全提醒

> ⚠️ 自动生成的 Skill 建议保留**人工审核环节**。生成的 SKILL.md 应该像代码审查一样认真过一遍再部署上线。

## 关联连接

- [[Progressive_Disclosure]] — 渐进式披露架构，Skill Factory 依赖的三层知识加载基础
- [[ADK]] — Google Agent Development Kit，Skill Factory 的实现框架
- [[Claude_Code_Skills]] — Claude Code 的 Skill 系统对比参考
- [[摘要-adk-agents-with-skills]] — 该概念的来源文章摘要
- [[Harness_Engineering]] — Agent 系统工程，Skill Factory 是其中的高级编排模式
