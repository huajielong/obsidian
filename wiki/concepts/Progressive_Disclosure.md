---
title: "渐进式披露（Progressive Disclosure）"
type: concept
tags: [架构模式, 知识管理, Skill, 上下文优化, 延迟加载]
sources: 
  - wiki/sources/摘要-adk-agents-with-skills.md
last_updated: 2026-07-06
---

# 渐进式披露（Progressive Disclosure）

## 定义

渐进式披露是一种知识加载架构模式，将 AI Agent 的能力知识组织为三个递进层级，仅在需要时加载深层内容。其核心思想借鉴了软件工程中的**延迟加载（Lazy Loading）** 理念，将上下文消耗从一次性全量加载变为按需逐步深入。最多可将基础上下文消耗降低 **90%**。

## 三层知识加载体系

| 层级 | 说明 | Token 消耗 | 加载方式 |
|------|------|-----------|---------|
| **L1: 元数据** | Skill 的名称 + 描述（Agent 浏览的"菜单"） | ~100 tokens/技能 | 始终在上下文中 |
| **L2: 指令** | 完整 Skill 主体（SKILL.md） | ~500 tokens，最高 ~5,000 | 通过 `load_skill` 按需加载 |
| **L3: 资源** | 外部参考文件（风格指南、API 规范等） | 可变 | 通过 `load_skill_resource` 按需加载 |

### 三层详解

**L1 元数据层**——每个 Skill 大约消耗 100 个 token。只包含 Skill 的名称和描述，没有任何具体的执行指令。Agent 启动时会加载所有 Skill 的 L1 元数据，相当于拿到一份餐厅菜单。Agent 浏览这份菜单来判断当前用户需求跟哪些 Skill 相关。

**L2 指令层**——每个 Skill 通常不超过 5000 个 token。这是 Skill 的完整指令体，详细描述了执行某项任务所需遵循的每一个步骤。只有当 Agent 通过 L1 判断某个 Skill 确实跟当前任务相关时，才会通过 API 调用显式加载该 Skill 的 L2 内容。

**L3 资源层**——完全按需加载。包括写作风格指南、API 接口规范文档、代码模板等外部参考文件。Agent 在执行过程中根据指令的具体需要才去加载对应的参考文件。

## Token 效率对比

一个拥有 10 项 Skill 的 Agent：

| 方式 | 每次调用消耗 | 对比 |
|------|-------------|------|
| 传统方式（全部加载） | ~10,000 tokens | 基准 |
| 渐进式披露（仅 L1） | ~1,000 tokens | 降低 ~90% |
| 触发 2 项 Skill 的任务 | ~3,000 tokens（L1+2×L2） | 节省 ~70% |

## 解决问题

传统的 AI Agent 开发中，系统提示词随着业务场景增多而不受控制地膨胀——SEO 规则、代码审查规范、API 接口文档等所有领域的知识被一股脑塞进一个巨大的指令字符串。这种做法导致：

- **Token 浪费**：大量无关指令占用上下文窗口
- **响应质量下降**：无关信息稀释模型对关键指令的关注度
- **扩展受限**：在功能丰富度和响应准确性之间难取舍

## 关联连接

- [[Skill_Factory]] — 元 Skill / Skill Factory，基于渐进式披露的自我扩展模式
- [[ADK]] — Google Agent Development Kit，渐进式披露的具体实现框架
- [[Claude_Code_Skills]] — Claude Code 的 Skill 系统，也遵循类似的能力组织原则
- [[摘要-adk-agents-with-skills]] — 该概念的来源文章摘要
- [[Harness_Engineering]] — Agent 系统工程实践，渐进式披露是其中的上下文管理策略
